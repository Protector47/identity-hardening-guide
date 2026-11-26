# Control index

Generated from [controls/controls.yaml](../controls/controls.yaml) by `scripts/build_index.py`. Do not edit by hand.

51 controls: 15 critical, 24 high, 12 medium.

## Tenant baseline and emergency access

| ID | Control | Severity | Platforms | Verify |
| --- | --- | --- | --- | --- |
| [IDH-BASE-01](01-tenant-baseline.md) | Keep two cloud-only break glass accounts excluded from every Conditional Access or sign-on policy except one that requires phishing resistant MFA | critical | Entra ID, Okta | List policy exclusions. Only the break glass group is excluded. Both accounts have a FIDO2 key stored in separate safes. |
| [IDH-BASE-02](01-tenant-baseline.md) | Alert on every sign-in by a break glass account | critical | Entra ID, Okta | Run the monthly break glass test sign-in and confirm the SOC ticket opens within 15 minutes. |
| [IDH-BASE-03](01-tenant-baseline.md) | Disable self service tenant creation, user app registration, and user consent to unverified publishers | high | Entra ID | Authorization policy shows allowedToCreateApps false, allowedToCreateTenants false, and the consent policy is not the legacy allow all setting. |
| [IDH-BASE-04](01-tenant-baseline.md) | Restrict guest invitations to named inviter roles and limit guest directory visibility | high | Entra ID, Okta | External collaboration settings show invites limited to admins and Guest Inviter role. Guest user access is set to the most restrictive level. |
| [IDH-BASE-05](01-tenant-baseline.md) | Send identity provider logs to the SIEM with at least 365 days retention | high | Entra ID, Okta | Query the SIEM for sign-in and audit events older than 90 days. Diagnostic settings or log streaming config exists for sign-in, audit, service principal sign-in, and risk logs. |

## Authentication and MFA

| ID | Control | Severity | Platforms | Verify |
| --- | --- | --- | --- | --- |
| [IDH-MFA-01](02-authentication-and-mfa.md) | Block legacy authentication protocols for all users | critical | Entra ID, Okta | Sign-in logs for 30 days show zero successful sign-ins with a legacy client app (IMAP, POP, SMTP AUTH, ActiveSync basic, other clients). |
| [IDH-MFA-02](02-authentication-and-mfa.md) | Require MFA for every interactive sign-in, with no trusted network bypass | critical | Entra ID, Okta | Sign-in logs show no successful interactive sign-in with single factor authentication outside the break glass accounts. |
| [IDH-MFA-03](02-authentication-and-mfa.md) | Require phishing resistant MFA (FIDO2, Windows Hello for Business, platform passkeys, certificate based) for admins | critical | Entra ID, Okta | Authentication strength or authenticator policy applied to all privileged roles. Admin sign-ins show only phishing resistant methods. |
| [IDH-MFA-04](02-authentication-and-mfa.md) | Turn on number matching and application context for push, and disable SMS and voice where an alternative exists | high | Entra ID, Okta | Authenticator method policy shows number matching enforced. SMS and voice are disabled or scoped to a small exception group with an expiry. |
| [IDH-MFA-05](02-authentication-and-mfa.md) | Protect MFA registration and recovery with the same or stronger assurance than sign-in | critical | Entra ID, Okta | A policy covers the security info registration action. Help desk reset requires verified identity, not knowledge of employee data. |
| [IDH-MFA-06](02-authentication-and-mfa.md) | Enforce banned password lists and remove periodic password expiry | medium | Entra ID, Okta, Any IdP | Custom banned list contains company, product, and city names. Password expiry is off. Minimum length is 14 for workforce accounts. |
| [IDH-MFA-07](02-authentication-and-mfa.md) | Enable sign-in and user risk detection and act on high risk automatically | high | Entra ID, Okta | High user risk forces secure password change. High sign-in risk forces MFA or blocks. Risky users report has no high risk users older than 7 days. |

## Conditional Access and sign-on policy

| ID | Control | Severity | Platforms | Verify |
| --- | --- | --- | --- | --- |
| [IDH-CA-01](03-conditional-access.md) | Build policies from a documented baseline set with named owners and change records | high | Entra ID, Okta | Each policy name maps to a row in the policy register. Last change has a ticket. |
| [IDH-CA-02](03-conditional-access.md) | Run every new or changed policy in report only mode for at least 7 days before enforcement | medium | Entra ID | Change record contains report only results and the affected user count before the switch to on. |
| [IDH-CA-03](03-conditional-access.md) | Require compliant or managed devices for admin portals and sensitive applications | high | Entra ID, Okta | Admin portal sign-ins from unmanaged devices fail in a test with a non compliant device. |
| [IDH-CA-04](03-conditional-access.md) | Block sign-in from countries the business does not operate in, with a time boxed travel exception group | medium | Entra ID, Okta | Named location list is reviewed quarterly. Travel group members have an end date. |
| [IDH-CA-05](03-conditional-access.md) | Set sign-in frequency and disable persistent browser sessions for admins and unmanaged devices | medium | Entra ID, Okta | Admin session lifetime is 4 hours or less. Unmanaged device sessions are not persistent. |
| [IDH-CA-06](03-conditional-access.md) | Restrict device code flow and authentication transfer to named exception groups | high | Entra ID | Sign-in logs show device code flow only for accounts in the exception group. |
| [IDH-CA-07](03-conditional-access.md) | Enable token protection or continuous access evaluation where the platform supports it | medium | Entra ID, Okta | CAE is not disabled tenant wide. Token protection or Okta session binding is applied to supported apps for admins. |
| [IDH-CA-08](03-conditional-access.md) | Review policy exclusions monthly and keep them group based | high | Entra ID, Okta | No policy excludes an individual user. Each exclusion group has an owner and an access review. |

## Privileged access

| ID | Control | Severity | Platforms | Verify |
| --- | --- | --- | --- | --- |
| [IDH-PRIV-01](04-privileged-access.md) | Keep standing Global Administrator or Super Admin assignments to the break glass accounts and at most two named admins | critical | Entra ID, Okta | Role assignment export shows the count. Everyone else is eligible through PIM or an access request flow. |
| [IDH-PRIV-02](04-privileged-access.md) | Use separate cloud-only admin accounts with no mailbox and no license for daily work | critical | Entra ID, Okta | No privileged role holder is a synced account. Admin accounts have no Exchange or Teams license. |
| [IDH-PRIV-03](04-privileged-access.md) | Require just in time activation with justification, approval for tier 0 roles, and maximum activation of 8 hours | high | Entra ID, Okta | PIM role settings show approval on tier 0 roles, MFA on activation, and max duration. |
| [IDH-PRIV-04](04-privileged-access.md) | Treat identity sync servers, federation servers, and PIM approvers as tier 0 | critical | Entra ID, Any IdP | Sync and federation hosts are in the tier 0 management boundary with tier 0 admins only. Local admin list on those hosts matches the register. |
| [IDH-PRIV-05](04-privileged-access.md) | Use privileged access workstations or hardened admin devices for tier 0 work | high | Any IdP | Conditional Access for tier 0 roles requires a device filter or compliant PAW device. |
| [IDH-PRIV-06](04-privileged-access.md) | Use role assignable groups or custom roles with least privilege instead of broad built in admin roles | medium | Entra ID, Okta | Assignments to Global Administrator, Privileged Role Administrator, and Super Admin are justified in the register. Help desk uses scoped roles. |
| [IDH-PRIV-07](04-privileged-access.md) | Review privileged role assignments monthly | high | Entra ID, Okta | Completed access review for each privileged role in the last 31 days, with removals applied. |

## Applications and OAuth

| ID | Control | Severity | Platforms | Verify |
| --- | --- | --- | --- | --- |
| [IDH-APP-01](05-applications-and-oauth.md) | Require admin consent for high impact delegated and all application permissions, with a consent request workflow | critical | Entra ID, Okta | User consent is limited to verified publishers and low impact permissions. Admin consent workflow has named reviewers. |
| [IDH-APP-02](05-applications-and-oauth.md) | Inventory every enterprise app and service principal with an owner, data class, and last sign-in | high | Entra ID, Okta | Inventory export matches the directory count. Apps with no sign-in for 90 days are disabled. |
| [IDH-APP-03](05-applications-and-oauth.md) | Prefer certificates or federated credentials over client secrets, and cap secret lifetime at 6 months | high | Entra ID, Okta | App credential report shows no secret with an expiry more than 180 days out. App management policy enforces the cap. |
| [IDH-APP-04](05-applications-and-oauth.md) | Register exact redirect URIs over HTTPS with no wildcards and no unused entries | high | Entra ID, Okta, Any IdP | App registration review shows only HTTPS redirect URIs (localhost allowed for native dev apps) and each one resolves to a domain the company owns. |
| [IDH-APP-05](05-applications-and-oauth.md) | Use authorization code with PKCE for all public and confidential clients, and disable implicit grant and ROPC | high | Entra ID, Okta, Any IdP | No app registration has implicit ID or access token issuance enabled. Allow public client flows is off unless documented. |
| [IDH-APP-06](05-applications-and-oauth.md) | Require assignment for enterprise apps that hold sensitive data | medium | Entra ID, Okta | Assignment required is set to yes. Assigned groups match the app owner list. |
| [IDH-APP-07](05-applications-and-oauth.md) | Sign SAML responses and assertions with SHA-256, and track signing certificate expiry | medium | Entra ID, Okta, Any IdP | SAML app settings show SHA-256 and a certificate expiry alert at 60 days. |
| [IDH-APP-08](05-applications-and-oauth.md) | Validate tokens fully in the relying application (issuer, audience, signature, expiry, tenant) | critical | Any IdP | Unit tests reject tokens with wrong audience, wrong issuer, expired exp, alg none, and a different tenant id in multi tenant apps. |

## Workload identities

| ID | Control | Severity | Platforms | Verify |
| --- | --- | --- | --- | --- |
| [IDH-WL-01](06-workload-identities.md) | Use managed identities for workloads that run in the cloud provider | high | Entra ID, Any IdP | No app registration secret is used by a workload that could run with a managed identity. |
| [IDH-WL-02](06-workload-identities.md) | Use workload identity federation for CI/CD, scoped to repository, branch, or environment | critical | Entra ID, Okta, Any IdP | Federated credential subject is pinned to a specific repo and environment. No long lived cloud keys in CI secrets. |
| [IDH-WL-03](06-workload-identities.md) | Grant workload identities resource scoped roles, never subscription or tenant wide owner | high | Entra ID, Any IdP | Role assignment export shows no Owner, User Access Administrator, or directory role on service principals outside the approved list. |
| [IDH-WL-04](06-workload-identities.md) | Monitor service principal sign-ins and credential additions | high | Entra ID, Okta | Alert fires on new credential added to an app or service principal, tested once per quarter. |
| [IDH-WL-05](06-workload-identities.md) | Give every non human account an owner and an expiry date | medium | Entra ID, Okta, Any IdP | Service account register has owner and review date for every entry. Accounts without an owner are disabled. |

## Lifecycle and access reviews

| ID | Control | Severity | Platforms | Verify |
| --- | --- | --- | --- | --- |
| [IDH-LC-01](07-lifecycle-and-reviews.md) | Drive joiner, mover, and leaver from the HR system of record | high | Entra ID, Okta, Any IdP | Sample ten leavers. All were disabled within 4 hours of HR termination time. |
| [IDH-LC-02](07-lifecycle-and-reviews.md) | Revoke sessions and refresh tokens on leaver, password reset, and MFA reset | critical | Entra ID, Okta | Leaver runbook calls session revoke. Sign-in logs show no token based access after the disable time. |
| [IDH-LC-03](07-lifecycle-and-reviews.md) | Remove access on mover events instead of only adding new access | medium | Any IdP | Mover sample shows old department groups removed within 7 days. |
| [IDH-LC-04](07-lifecycle-and-reviews.md) | Disable accounts with no sign-in for 60 days and delete after 90 | medium | Entra ID, Okta | Stale account report has no enabled member accounts above 60 days except documented exceptions. |
| [IDH-LC-05](07-lifecycle-and-reviews.md) | Run quarterly access reviews for guests and for groups that grant access to sensitive apps | high | Entra ID, Okta | Review history shows completion and auto apply of denials. |

## Monitoring and verification

| ID | Control | Severity | Platforms | Verify |
| --- | --- | --- | --- | --- |
| [IDH-MON-01](08-monitoring-and-verification.md) | Alert on changes to Conditional Access, sign-on policies, and authentication method policies | high | Entra ID, Okta | Change a test policy in a non production tenant or a disabled policy and confirm the alert. |
| [IDH-MON-02](08-monitoring-and-verification.md) | Alert on privileged role assignment outside the PIM flow | critical | Entra ID, Okta | Audit query for permanent role assignments returns only approved changes. |
| [IDH-MON-03](08-monitoring-and-verification.md) | Alert on new federation trust or domain authentication changes | critical | Entra ID, Okta | Alert rule exists for domain federation settings and new identity provider changes. |
| [IDH-MON-04](08-monitoring-and-verification.md) | Alert on admin consent grants and new high privilege application permissions | high | Entra ID, Okta | Grant a low impact permission to a test app and confirm the alert includes the permission list. |
| [IDH-MON-05](08-monitoring-and-verification.md) | Track MFA fatigue patterns and MFA method changes followed by sensitive actions | high | Entra ID, Okta | Query for repeated MFA denials per user per hour returns results to the SOC queue. |
| [IDH-MON-06](08-monitoring-and-verification.md) | Re-run the control verification checklist every quarter and record results | medium | Any IdP | Filled templates/quarterly-verification.md exists for the last quarter with owners and dates. |
