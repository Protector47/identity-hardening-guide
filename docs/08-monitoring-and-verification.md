# 08. Monitoring and verification

Controls drift. A policy gets an exclusion during an outage, a new app gets consent on a Friday, someone assigns Global Admin directly because PIM was slow. These queries catch that in your own tenant.

The KQL targets Microsoft Sentinel or a Log Analytics workspace with Entra diagnostic logs. Field names and operation names can differ slightly between tenants and log versions, so run each query against a known event before you turn it into an alert. The Okta entries list System Log event types to filter on in whatever SIEM receives the log stream.

## Break glass sign-in

Control: IDH-BASE-02.

```kql
let breakGlass = dynamic(["bg-01@contoso.onmicrosoft.com", "bg-02@contoso.onmicrosoft.com"]);
union SigninLogs, AADNonInteractiveUserSignInLogs
| where TimeGenerated > ago(1h)
| where UserPrincipalName in~ (breakGlass)
| project TimeGenerated, UserPrincipalName, ResultType, IPAddress, AppDisplayName, UserAgent
```

Okta: `user.session.start` or `user.authentication.sso` where `actor.alternateId` is a break glass account.

## Legacy auth still succeeding

Control: IDH-MFA-01.

```kql
SigninLogs
| where TimeGenerated > ago(30d)
| where ResultType == "0"
| where ClientAppUsed in ("Exchange ActiveSync", "Other clients", "IMAP4", "POP3",
    "Authenticated SMTP", "Exchange Web Services", "Outlook Anywhere (RPC over HTTP)",
    "MAPI Over HTTP", "Offline Address Book", "AutoDiscover")
| summarize Signins = count(), LastSeen = max(TimeGenerated) by UserPrincipalName, ClientAppUsed
| order by Signins desc
```

Expected result after enforcement: empty.

## Single factor successes

Control: IDH-MFA-02.

```kql
SigninLogs
| where TimeGenerated > ago(7d)
| where ResultType == "0"
| where AuthenticationRequirement == "singleFactorAuthentication"
| where UserType == "Member"
| summarize Signins = count() by UserPrincipalName, AppDisplayName, ConditionalAccessStatus
| order by Signins desc
```

Anything here other than break glass means a policy gap. Check `ConditionalAccessStatus == "notApplied"` rows first.

## Device code flow

Control: IDH-CA-06.

```kql
SigninLogs
| where TimeGenerated > ago(7d)
| where AuthenticationProtocol == "deviceCode"
| project TimeGenerated, UserPrincipalName, AppDisplayName, IPAddress, ResultType, ConditionalAccessStatus
```

Compare the users with your exception group.

## Policy changes

Control: IDH-MON-01.

```kql
AuditLogs
| where TimeGenerated > ago(1d)
| where OperationName in ("Add conditional access policy", "Update conditional access policy",
    "Delete conditional access policy", "Authentication Methods Policy Update")
| extend Actor = coalesce(tostring(InitiatedBy.user.userPrincipalName), tostring(InitiatedBy.app.displayName))
| extend Target = tostring(TargetResources[0].displayName)
| project TimeGenerated, OperationName, Actor, Target, Result
```

Okta: `policy.lifecycle.create`, `policy.lifecycle.update`, `policy.lifecycle.delete`, `policy.lifecycle.deactivate`, `policy.rule.create`, `policy.rule.update`, `policy.rule.delete`, `policy.rule.deactivate`.

Match each event against an open change ticket. No ticket, page the identity on call.

## Role assignment outside PIM

Control: IDH-MON-02.

```kql
AuditLogs
| where TimeGenerated > ago(1d)
| where Category == "RoleManagement"
| where OperationName == "Add member to role"
| extend Actor = coalesce(tostring(InitiatedBy.user.userPrincipalName), tostring(InitiatedBy.app.displayName))
| where Actor != "MS-PIM"
| extend Role = tostring(TargetResources[0].modifiedProperties[1].newValue)
| extend Member = tostring(TargetResources[2].userPrincipalName)
| project TimeGenerated, Actor, Role, Member, TargetResources
```

The position of the role name inside `TargetResources` varies. Keep the raw column in the output until you have confirmed the layout in your tenant.

Okta: `user.account.privilege.grant`, `group.privilege.grant`, `iam.role.create`, `iam.resourceset.bindings.add`.

## Federation and domain changes

Control: IDH-MON-03.

```kql
AuditLogs
| where TimeGenerated > ago(1d)
| where OperationName in ("Set domain authentication", "Set federation settings on domain",
    "Add unverified domain", "Verify domain", "Add domain to company")
| extend Actor = coalesce(tostring(InitiatedBy.user.userPrincipalName), tostring(InitiatedBy.app.displayName))
| project TimeGenerated, OperationName, Actor, TargetResources
```

A domain switched to federated, or a new federation trust, gives whoever controls the signing key the ability to sign in as any user in that domain. Treat these as critical.

Okta: `system.idp.lifecycle.create`, `system.idp.lifecycle.update`, `system.idp.lifecycle.activate`.

## Consent and app permissions

Control: IDH-MON-04.

```kql
AuditLogs
| where TimeGenerated > ago(1d)
| where OperationName in ("Consent to application", "Add app role assignment to service principal",
    "Add delegated permission grant")
| extend Actor = coalesce(tostring(InitiatedBy.user.userPrincipalName), tostring(InitiatedBy.app.displayName))
| extend App = tostring(TargetResources[0].displayName)
| mv-expand Prop = TargetResources[0].modifiedProperties
| where tostring(Prop.displayName) in ("ConsentContext.IsAdminConsent", "ConsentAction.Permissions", "AppRole.Value", "DelegatedPermissionGrant.Scope")
| project TimeGenerated, OperationName, Actor, App, Property = tostring(Prop.displayName), Value = tostring(Prop.newValue)
```

Raise severity when the value contains any permission from the review list in [05-applications-and-oauth.md](05-applications-and-oauth.md).

Okta: `app.oauth2.as.consent.grant`, `app.oauth2.client.lifecycle.create`, `system.api_token.create`.

## New credentials on apps

Control: IDH-WL-04.

```kql
AuditLogs
| where TimeGenerated > ago(1d)
| where OperationName has "Certificates and secrets management"
    or OperationName == "Add service principal credentials"
| extend Actor = coalesce(tostring(InitiatedBy.user.userPrincipalName), tostring(InitiatedBy.app.displayName))
| extend App = tostring(TargetResources[0].displayName)
| project TimeGenerated, OperationName, Actor, App, TargetResources
```

## Service principal sign-in from a new IP

Control: IDH-WL-04.

```kql
let lookback = 30d;
let known = AADServicePrincipalSignInLogs
    | where TimeGenerated between (ago(lookback) .. ago(1d))
    | where ResultType == "0"
    | distinct AppId, IPAddress;
AADServicePrincipalSignInLogs
| where TimeGenerated > ago(1d)
| where ResultType == "0"
| join kind=leftanti known on AppId, IPAddress
| summarize FirstSeen = min(TimeGenerated), Signins = count() by ServicePrincipalName, AppId, IPAddress
```

Expect noise from CI runners with dynamic IPs. Exclude their published ranges or use federated identities with subject pinning instead.

## MFA fatigue

Control: IDH-MON-05.

```kql
SigninLogs
| where TimeGenerated > ago(1d)
| where ResultType == "500121"
| extend Detail = tostring(Status.additionalDetails)
| where Detail has "denied" or Detail has "declined"
| summarize Denials = count(), IPs = make_set(IPAddress, 10) by UserPrincipalName, bin(TimeGenerated, 1h)
| where Denials >= 3
```

Okta: `user.mfa.okta_verify.deny_push` and `system.push.send_factor_verify_push` counts per user per hour.

## MFA method change then sensitive action

Control: IDH-MON-05.

```kql
let methodChanges = AuditLogs
    | where TimeGenerated > ago(1d)
    | where OperationName in ("User registered security info", "Admin registered security info",
        "User deleted security info", "Admin deleted security info")
    | extend User = tostring(TargetResources[0].userPrincipalName)
    | project ChangeTime = TimeGenerated, User, MethodChange = OperationName;
AuditLogs
| where TimeGenerated > ago(1d)
| where OperationName in ("Consent to application", "Add member to role", "Update user")
| extend User = coalesce(tostring(InitiatedBy.user.userPrincipalName), "")
| join kind=inner methodChanges on User
| where TimeGenerated between (ChangeTime .. (ChangeTime + 1h))
| project ChangeTime, User, MethodChange, ActionTime = TimeGenerated, Action = OperationName
```

Extend the sensitive action list with your own business events, for example payee changes in the banking app, by joining the application logs.

Okta: `user.mfa.factor.activate`, `user.mfa.factor.deactivate`, `user.mfa.factor.reset_all` followed within an hour by `user.account.privilege.grant` or `app.oauth2.as.consent.grant` by the same actor.

## Quarterly verification

Control: IDH-MON-06.

Alerts tell you about changes. They do not tell you a control that was never built is missing. Once a quarter, walk the [control index](control-index.md), run each "verify" step, and record pass, fail, or exception with an owner and date in [templates/quarterly-verification.md](../templates/quarterly-verification.md). Failures become tickets with the severity from the catalog.
