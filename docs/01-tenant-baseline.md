# 01. Tenant baseline and emergency access

Do this first. Most identity incidents I have worked started with a tenant setting nobody owned: users allowed to register apps, guests able to read the whole directory, logs kept for 30 days and gone before anyone looked.

## Break glass accounts

Controls: IDH-BASE-01, IDH-BASE-02.

You need a way in when Conditional Access, federation, or MFA breaks. Without it, the first bad policy change locks out every admin.

Set up:

- Two accounts. Cloud only, on the `onmicrosoft.com` domain (Entra) or a local Okta user, never synced from AD and never federated.
- Global Administrator (Entra) or Super Admin (Okta), permanent assignment. These are the only standing assignments outside the short list in [04-privileged-access.md](04-privileged-access.md).
- One FIDO2 security key per account, plus a backup key. Store each account's keys in a different physical safe. If you keep a password, split it between two custodians.
- Excluded from every Conditional Access policy except one: a policy that targets only the break glass group and requires phishing resistant MFA authentication strength. Microsoft now enforces MFA on admin portals, so a break glass account with password only will not work anyway.
- No mailbox, no license, no group membership other than the exclusion group.

Operate:

- Alert on any sign-in by either account. Route it to the SOC as high severity, not to an email folder.
- Test once a month. Sign in, confirm the alert opens, sign out, record the result in the break glass log.
- Rotate keys when a custodian leaves.

Use [templates/break-glass-runbook.md](../templates/break-glass-runbook.md) for the procedure.

## Tenant settings

Control: IDH-BASE-03.

| Setting | Entra ID | Target |
| --- | --- | --- |
| Users can register applications | User settings | No |
| Users can create tenants | User settings | No |
| Users can create security groups | Groups settings | No, unless you have self service group governance |
| User consent for apps | Consent and permissions | Verified publishers, low impact permissions only (see [05-applications-and-oauth.md](05-applications-and-oauth.md)) |
| Restrict access to admin portal | User settings | Yes (this is a UI control, not a security boundary) |
| LinkedIn account connections | User settings | No for regulated orgs |
| Self service sign-up for email verified users | Authorization policy | Off |

To check from Graph without the portal:

```text
GET https://graph.microsoft.com/v1.0/policies/authorizationPolicy
```

Look at `defaultUserRolePermissions.allowedToCreateApps`, `allowedToCreateTenants`, `allowedToCreateSecurityGroups`, and `permissionGrantPoliciesAssigned`.

For Okta, the equivalent review points are: self service registration off for the workforce org, end user dashboard app requests routed through an approval flow, and API token creation limited to admins who need it.

## Guests and external users

Control: IDH-BASE-04.

- Only admins and the Guest Inviter role can invite.
- Guest user access set to the most restrictive option, so guests see only their own object and groups they belong to.
- Allow list of partner domains if your business has a stable partner set. Otherwise deny list known free mail domains for B2B.
- Cross tenant access settings: trust MFA from partner tenants only after you check the partner enforces it. Do not trust compliant device claims from tenants you do not manage.
- Guests go into quarterly access reviews (IDH-LC-05).

## Logs

Control: IDH-BASE-05.

The default retention is short. Entra keeps sign-in and audit logs for 30 days on P1/P2. Okta keeps System Log for 90 days. Incidents are usually found later than that.

Send to the SIEM:

| Source | Entra ID | Okta |
| --- | --- | --- |
| Interactive sign-ins | SigninLogs | System Log, `user.session.start`, `user.authentication.*` |
| Non interactive sign-ins | AADNonInteractiveUserSignInLogs | System Log, token events |
| Service principal sign-ins | AADServicePrincipalSignInLogs, AADManagedIdentitySignInLogs | System Log, `app.oauth2.*` |
| Directory changes | AuditLogs | System Log, `user.*`, `group.*`, `application.*`, `policy.*` |
| Risk | AADUserRiskEvents, AADRiskyUsers | ThreatInsight and behavior detection events |
| Graph activity | MicrosoftGraphActivityLogs | Not applicable |

Keep at least 365 days searchable. If cost is the blocker, keep audit and sign-in logs hot and move non interactive logs to cheaper storage. Do not drop them. Token replay and service principal abuse show up there.
