# 07. Lifecycle and access reviews

Most excess access is not granted by mistake. It is granted correctly and never taken away.

## Joiner, mover, leaver from HR

Control: IDH-LC-01.

- HR is the source of truth for who works here. Provision from it (Workday, SuccessFactors, or your HRMS into Entra or Okta), not from tickets.
- Joiner: account created disabled, enabled on start date, Temporary Access Pass issued for first sign-in and MFA registration.
- Leaver: disable at the HR termination time, not at end of business. For involuntary exits, HR triggers it before the meeting.
- Contractors have an end date in the record. No end date, no account.
- Sample ten leavers a quarter and check disable time against HR time. Target: within 4 hours, within 15 minutes for involuntary.

## Revoke sessions, not just the account

Control: IDH-LC-02.

Disabling the account stops new sign-ins. Existing refresh tokens and app sessions can keep working until they expire unless you revoke them.

| Event | Entra ID | Okta |
| --- | --- | --- |
| Leaver | Disable, then `POST /users/{id}/revokeSignInSessions` | Deactivate, then `DELETE /api/v1/users/{id}/sessions?oauthTokens=true` |
| Password reset after compromise | Reset, revoke sessions, review MFA methods | Reset, clear sessions, reset factors if needed |
| MFA reset | Remove methods, revoke sessions, issue TAP | Reset factors, clear sessions |
| Lost device | Revoke sessions, retire device in Intune | Clear sessions, remove Okta Verify enrollment |

Apps with their own sessions (SaaS with long lived cookies, mobile apps) need SCIM deprovisioning or their own revoke call. Put those apps in the leaver runbook by name.

## Movers

Control: IDH-LC-03.

- A department change triggers removal of the old department's access packages and groups, with a short overlap (up to 7 days) if the manager asks.
- Access based on attributes (department, cost center, job code) in dynamic groups removes itself. Prefer it for birthright access.
- Anything requested by hand goes through an access package with an expiry, so it ends without a review.

## Stale accounts

Control: IDH-LC-04.

- Enabled member accounts with no successful sign-in for 60 days: disable. 90 days: delete, after the owner confirms.
- Use the `signInActivity` property in Graph (`lastSuccessfulSignInDateTime`) or Okta's `lastLogin` field.
- Exceptions (long leave, seasonal staff) go in a group with an end date.
- Guests follow the same rule, with a shorter clock if your business allows it.

## Access reviews

Control: IDH-LC-05.

| What | Frequency | Reviewer |
| --- | --- | --- |
| Privileged roles | Monthly (IDH-PRIV-07) | Role owner |
| Guests | Quarterly | Inviting team or sponsor |
| Groups granting sensitive app access | Quarterly | App owner |
| Service accounts and app owners | Twice a year | Owning team lead |
| Exclusion groups in Conditional Access | Monthly (IDH-CA-08) | Identity team lead |

Make reviews useful:

- Show last sign-in to the reviewer. People approve what they do not understand.
- Auto apply results. Denied and not reviewed both mean removed.
- Track the denial rate. A review with zero denials for a year is probably being clicked through.
