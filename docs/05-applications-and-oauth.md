# 05. Applications and OAuth

Applications are the quiet path into a tenant. A consented app with `Mail.Read` keeps reading mail after the user changes their password. A service principal with `RoleManagement.ReadWrite.Directory` is a Global Admin that never signs in interactively.

## Consent

Control: IDH-APP-01.

- User consent: allowed only for apps from verified publishers, and only for permissions you classify as low impact (for example `User.Read`, `openid`, `profile`, `email`, `offline_access`).
- Everything else goes to the admin consent workflow. Reviewers are named people in security and identity, not a distribution list.
- Never grant tenant wide admin consent for a delegated permission you would not give every user yourself.

Permissions that should always need security review:

| Permission | Why |
| --- | --- |
| `RoleManagement.ReadWrite.Directory` | Can assign any directory role, including Global Admin |
| `AppRoleAssignment.ReadWrite.All` | Can grant itself or others any application permission |
| `Application.ReadWrite.All` | Can add credentials to other apps |
| `Directory.ReadWrite.All` | Broad write across the directory |
| `Mail.ReadWrite`, `Mail.Send` (application) | Access to every mailbox unless scoped with RBAC for Applications |
| `Files.ReadWrite.All`, `Sites.FullControl.All` | Every file in SharePoint and OneDrive |
| `full_access_as_app` (EWS) | Every mailbox |
| Okta `okta.users.manage`, `okta.apps.manage`, `okta.roles.manage` scopes | Admin level changes through API |

For Exchange application permissions, scope with RBAC for Applications or application access policies so the app sees only the mailboxes it needs.

## Inventory

Control: IDH-APP-02.

Every enterprise app and service principal needs:

- Owner (a person and a team)
- Business purpose
- Data classification of what it can reach
- Permissions granted and who approved them
- Last sign-in (from service principal sign-in logs)
- Credential type and expiry

Disable apps with no sign-in for 90 days. Delete after a further 30 days if nobody asks for them back. Use [templates/app-registration-review.md](../templates/app-registration-review.md) for each app.

## Credentials

Control: IDH-APP-03.

| Credential | Use | Notes |
| --- | --- | --- |
| Managed identity | Workload runs in Azure | No credential to leak. First choice. |
| Federated credential | CI/CD, Kubernetes, other clouds | No stored secret. See [06-workload-identities.md](06-workload-identities.md). |
| Certificate | Everything else | Key in a vault or HSM, non exportable where possible. |
| Client secret | Only when nothing else works | Max 6 months. Stored in a vault, never in code or pipeline variables. |

Enforce lifetimes with an app management policy (Entra) so people cannot create a two year secret through the portal. Alert on new credentials (IDH-WL-04).

## Redirect URIs

Control: IDH-APP-04.

A loose redirect URI turns your app into a token delivery service for whoever controls the target.

- Exact match only. No wildcards.
- HTTPS only. `http://localhost` is fine for native and developer apps, with a dynamic port where the platform supports it.
- Every host belongs to a domain your company owns and still has DNS for. Dangling entries pointing at deleted cloud apps or expired domains are a takeover risk.
- Remove staging and test URIs from production registrations.
- Review on each release that changes auth, and quarterly otherwise.

## Flows

Control: IDH-APP-05.

- Authorization code with PKCE for web, SPA, mobile, and desktop. Confidential web clients use PKCE as well.
- Implicit grant off. Uncheck "Access tokens" and "ID tokens" under implicit grant in Entra app registrations. In Okta, do not enable the implicit grant type.
- Resource owner password credentials (ROPC) off. It skips MFA and Conditional Access in many configurations.
- "Allow public client flows" off unless the app is a native client that needs device code, with that documented.
- Client credentials only for daemon services, with application permissions scoped as above.

## Assignment

Control: IDH-APP-06.

Set "Assignment required" for apps that hold sensitive data. Otherwise any user in the tenant can get a token for them. Assign groups, not users. Match the group to the app owner's access list.

## SAML

Control: IDH-APP-07.

- Sign the response and the assertion. SHA-256.
- Encrypt assertions when the SP supports it and the assertion carries sensitive attributes.
- Track signing certificate expiry with a 60 day alert. Expired certificates cause outages, and outages cause rushed fixes.
- Send only the attributes the app needs. Do not send group lists the app does not use.

## Token validation in your own apps

Control: IDH-APP-08.

This one is for the teams building apps that accept tokens. The identity provider can be perfect and the app still accepts a forged or misdirected token.

Validate on every request:

- Signature with keys from the issuer's JWKS endpoint, cached and refreshed on unknown `kid`.
- `alg` is the expected value. Reject `none` and any HMAC algorithm when you expect RS256 or ES256.
- `iss` exactly matches your tenant or authorization server. For multi tenant Entra apps, validate the `tid` claim against an allow list.
- `aud` is your API's client id or App ID URI. A token for another API must fail.
- `exp` and `nbf` with a small clock skew (60 seconds or less).
- Scopes (`scp`) for delegated calls and roles (`roles`) for application calls. Check them per endpoint.

Write unit tests for each rejection case. Use your framework's validation library (Microsoft.Identity.Web, MSAL, Spring Security resource server, jose, PyJWT with explicit algorithms) rather than parsing JWTs by hand.
