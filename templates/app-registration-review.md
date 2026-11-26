# Application registration review

Related controls: IDH-APP-01 to IDH-APP-08, IDH-WL-03, IDH-WL-05.

| Field | Value |
| --- | --- |
| App name | |
| App (client) id | |
| Owner (person) | |
| Owning team | |
| Business purpose | |
| Data classification | |
| Last sign-in | |

## Permissions

| Permission | Type (delegated or application) | Admin consented by | Still needed |
| --- | --- | --- | --- |
| | | | |

## Credentials

| Type | Created | Expires | Stored in |
| --- | --- | --- | --- |
| | | | |

## Checks

- [ ] No secret with expiry beyond 180 days (IDH-APP-03)
- [ ] Redirect URIs exact, HTTPS, owned domains (IDH-APP-04)
- [ ] Implicit grant and public client flows off, or justified (IDH-APP-05)
- [ ] Assignment required for sensitive data (IDH-APP-06)
- [ ] SAML signing SHA-256 and cert expiry tracked, if SAML (IDH-APP-07)
- [ ] Token validation tests exist in the app repo (IDH-APP-08)
- [ ] No subscription Owner or directory role on the service principal (IDH-WL-03)
- [ ] Owner and review date in the register (IDH-WL-05)

## Decision

Keep, reduce permissions, rotate credentials, or disable. Reviewer and date.
