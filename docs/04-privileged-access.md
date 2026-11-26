# 04. Privileged access

Identity admins own the keys to everything else. Fewer of them, with less standing access, on cleaner devices.

## How many standing admins

Control: IDH-PRIV-01.

- Standing Global Administrator (Entra) or Super Admin (Okta): the two break glass accounts and at most two named people.
- Everyone else is eligible through Privileged Identity Management (Entra) or an access request with time bound group membership (Okta Identity Governance or your IGA tool).
- Export assignments monthly. Entra: `GET /roleManagement/directory/roleAssignments` for active and `roleEligibilitySchedules` for eligible. Okta: `GET /api/v1/iam/assignees/users` or the admin roles report.

## Admin accounts

Control: IDH-PRIV-02.

- Separate account for admin work, for example `adm-firstname.lastname@tenant.onmicrosoft.com`.
- Cloud only. A synced account means anyone who owns on prem AD owns the cloud tenant too.
- No mailbox, no Teams, no license that lets it browse or read mail. Phishing lands in mailboxes.
- Phishing resistant MFA (IDH-MFA-03).

## Just in time

Control: IDH-PRIV-03.

| Role tier | Examples | Activation | Max duration | Approval |
| --- | --- | --- | --- | --- |
| Tier 0 | Global Admin, Privileged Role Admin, Privileged Authentication Admin, Hybrid Identity Admin, Super Admin | Phishing resistant MFA, justification, ticket | 4 hours | Yes, by another tier 0 admin |
| Tier 1 | Exchange, SharePoint, Intune, Security Admin, Application Admin, Cloud App Admin, Org Admin | MFA, justification | 8 hours | Optional |
| Tier 2 | Help desk, User Admin scoped by admin unit, Group Admin | MFA, justification | 8 hours | No |

Notes:

- Application Administrator and Cloud Application Administrator can add credentials to any service principal. If a service principal holds a powerful permission, those roles are tier 0 in practice. Scope them with custom roles or app ownership instead.
- Privileged Authentication Administrator can reset MFA for Global Admins. Tier 0.
- PIM notifications go to a shared mailbox the security team reads, not to each approver only.

## Tier 0 infrastructure

Control: IDH-PRIV-04.

These systems can mint or change identities, so they sit at the same level as Global Admin:

- Entra Connect or Cloud Sync servers
- AD FS or any federation server, and their signing certificates
- Domain controllers and the AD tier 0 groups
- Okta AD agents and LDAP agents
- PIM approvers and the accounts that can change PIM settings
- The pipeline or repo that deploys Conditional Access as code

Manage them only from tier 0 admin devices. Local admin list on each host matches the register. Patch them on the critical schedule.

## Admin devices

Control: IDH-PRIV-05.

- Dedicated privileged access workstation for tier 0. No email, no general browsing, application allow listing.
- If full PAWs are not possible, use a hardened, compliant device with a separate profile, and enforce it with a device filter in Conditional Access (CA011 in [03-conditional-access.md](03-conditional-access.md)).

## Least privilege roles

Control: IDH-PRIV-06.

- Help desk gets User Administrator or Authentication Administrator scoped to an administrative unit, not Global Admin.
- Use role assignable groups for PIM so membership itself is protected.
- Prefer custom roles for app management that cover only the apps the team owns.
- In Okta, use custom admin roles with resource sets instead of Super Admin or Org Admin.

## Reviews

Control: IDH-PRIV-07.

- Monthly access review on each privileged role and each role assignable group.
- Reviewer is the role owner, not the person being reviewed.
- Auto apply denials. Unreviewed means removed.
- Track the number of eligible and active assignments over time. It should go down or stay flat.
