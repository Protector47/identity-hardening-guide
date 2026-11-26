# 03. Conditional Access and sign-on policy

Conditional Access (Entra) and authentication or global session policies (Okta) are where most of the identity controls actually live. Treat them like firewall rules: a register, an owner per rule, change records, and testing before enforcement.

## Policy register

Control: IDH-CA-01.

Name policies so the purpose is obvious in a sign-in log. A pattern that works:

```text
CA<NNN>-<Persona>-<Apps>-<Control>
CA001-All-AllApps-BlockLegacyAuth
CA010-Admins-AllApps-PhishResistantMFA
```

Keep the register next to the policies, in a repo if you manage them as code. Each row: policy name, purpose, persona, apps, conditions, grant or session control, exclusions, owner, last review date, change ticket.

Use [templates/conditional-access-change.md](../templates/conditional-access-change.md) for every change.

## Baseline policy set

This is the starting set I hand to teams. Adjust personas to your org.

| Policy | Users | Apps | Conditions | Control | Related |
| --- | --- | --- | --- | --- | --- |
| CA001 Block legacy auth | All | All | Client apps: EAS, other | Block | IDH-MFA-01 |
| CA002 MFA all users | All, minus break glass | All | Any | Require MFA strength | IDH-MFA-02 |
| CA003 Break glass phishing resistant | Break glass group only | All | Any | Phishing resistant strength | IDH-BASE-01 |
| CA010 Admins phishing resistant | Privileged roles | All | Any | Phishing resistant strength | IDH-MFA-03 |
| CA011 Admins compliant device | Privileged roles | Admin portals, Azure management | Any | Compliant device or PAW filter | IDH-CA-03 |
| CA012 Admin session | Privileged roles | All | Any | Sign-in frequency 4h, no persistent browser | IDH-CA-05 |
| CA020 Register security info | All | User action: register security info | Not compliant device | Require MFA or TAP | IDH-MFA-05 |
| CA030 Block unsupported countries | All, minus travel group | All | Location not in allowed list | Block | IDH-CA-04 |
| CA040 High user risk | All | All | User risk high | Password change plus MFA | IDH-MFA-07 |
| CA041 Sign-in risk | All | All | Sign-in risk medium and high | Require MFA | IDH-MFA-07 |
| CA050 Device code flow | All, minus exception group | All | Authentication flows: device code, auth transfer | Block | IDH-CA-06 |
| CA060 Sensitive apps managed device | All | Finance, HR, core banking back office | Device not compliant | Block or app enforced restrictions | IDH-CA-03 |
| CA061 Unmanaged session | All | All | Device not compliant | Sign-in frequency 12h, no persistent browser | IDH-CA-05 |
| CA070 Guests | Guests | All | Any | Require MFA, terms of use | IDH-BASE-04 |

Okta mapping:

- CA001, CA002, CA010: authentication policies on each app plus the global session policy. Set the Admin Console policy separately.
- CA011, CA060: device assurance policies and managed device conditions in authentication policy rules.
- CA012, CA061: global session policy, maximum session lifetime and "persist session cookies" off.
- CA030: network zones with a blocklist zone, or dynamic zones.
- CA040, CA041: risk scoring and behavior detection in authentication policy rules.

## Report only first

Control: IDH-CA-02.

- New or changed policies run in report only mode for at least 7 days. 14 for anything touching all users.
- Pull the report only results with the workbook or KQL: who would have been blocked, which apps, which devices.
- Fix the gaps, then switch on. Keep the report only numbers in the change record.
- For Okta, test the rule against a pilot group first, then widen. Use the policy simulation tool before saving.

## Device trust

Control: IDH-CA-03.

- Admin portals require a compliant device (Intune) or a device filter that matches your PAW group.
- Sensitive line of business apps (finance, HR, payments back office) require a compliant or hybrid joined device. For BYOD, use app protection policies and browser restrictions, not full access.
- Test with a non compliant device after every change. The common failure is an "All cloud apps" exclusion that quietly leaves the Azure management endpoint open.

## Locations

Control: IDH-CA-04.

- Location blocking is a noise reducer, not a strong control. VPNs and residential proxies get around it.
- Keep the allowed country list small. Review quarterly with the business.
- Travel exceptions go in a group with an end date set by the access package or the ticket. Not a permanent exclusion.
- Never use "trusted location" to skip MFA (IDH-MFA-02).

## Sessions

Control: IDH-CA-05.

| Persona | Sign-in frequency | Persistent browser |
| --- | --- | --- |
| Admins | 4 hours or less | Never |
| Staff on compliant device | Default (rolling, CAE covered) | Allowed |
| Staff on unmanaged device | 12 hours | Never |
| Guests | 12 hours | Never |

## Device code flow and authentication transfer

Control: IDH-CA-06.

Device code phishing works because the victim signs in on the real Microsoft page and approves a code the attacker generated. Block the flow for everyone who does not need it. Conference room devices and some CLI use cases need it; put them in a named exception group with an owner.

## Token binding and CAE

Control: IDH-CA-07.

- Do not disable Continuous Access Evaluation tenant wide. It lets Exchange, SharePoint, and Teams reject tokens after a user is disabled or a password changes, without waiting for token expiry.
- Apply token protection (sign-in session binding) for admins on supported Windows clients. Start in report only mode; unsupported clients will fail.
- In Okta, bind sessions to the device with Okta Verify and FastPass where available.

## Exclusions

Control: IDH-CA-08.

Exclusions are where policies fail. Every incident review I have done on a CA bypass found an exclusion someone added for a test and never removed.

- Exclude groups, never individual users.
- Each exclusion group has an owner, a reason, and an access review.
- Monthly: export policies, list every exclusion, compare with the register. The Graph call is `GET /identity/conditionalAccess/policies`.
- Alert when an exclusion is added (IDH-MON-01).
