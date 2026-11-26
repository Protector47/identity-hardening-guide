# 02. Authentication and MFA

Goal: every human sign-in needs a second factor, admins need a factor that cannot be phished, and the recovery path is not weaker than the front door.

## Kill legacy authentication

Control: IDH-MFA-01.

Legacy protocols (IMAP, POP, SMTP AUTH, Exchange ActiveSync with basic auth, older Office clients) cannot do MFA. Password spray tools target them because of that.

Steps:

1. Find who still uses it. In Entra, filter sign-in logs on client app = "Other clients", "IMAP4", "POP3", "Authenticated SMTP", "Exchange ActiveSync". The KQL is in [08-monitoring-and-verification.md](08-monitoring-and-verification.md).
2. Move those users and devices to modern auth. Printers and scanners that send mail are the usual leftovers. Give them a relay connector or OAuth, not an exception.
3. Create a Conditional Access policy: all users, all cloud apps, client apps = Exchange ActiveSync and other clients, grant = block.
4. In Okta, use an authentication policy rule that denies legacy clients, and turn off the legacy protocols in the Office 365 app settings.

## MFA for everyone

Control: IDH-MFA-02.

- One policy, all users, all cloud apps, require MFA (or an authentication strength). Exclude only the break glass group.
- No trusted IP or "corporate network" bypass. An attacker on the VPN or a compromised internal host is exactly the case MFA should cover.
- Guests included. If a partner cannot do MFA, that is a business decision someone signs, with an expiry.

## Phishing resistant MFA for admins

Control: IDH-MFA-03.

Push, OTP, and SMS can all be relayed through an adversary in the middle proxy. FIDO2 and certificate based auth bind the sign-in to the real origin, so a proxy cannot reuse them.

| Method | Phishing resistant | Notes |
| --- | --- | --- |
| FIDO2 security key | Yes | Best default for admins. Buy two per admin. |
| Passkey in Authenticator app (device bound) | Yes | Good when security keys are hard to issue. |
| Windows Hello for Business | Yes | Tied to the device. Pair with a key for other devices. |
| Certificate based auth (smart card) | Yes | Common in banks and government. Mind CRL and OCSP availability. |
| Okta FastPass with phishing resistance | Yes | Requires Okta Verify on managed devices. |
| Authenticator push with number matching | No | Better than plain push, still relayable. |
| TOTP | No | |
| SMS and voice | No | SIM swap and relay risk. |

In Entra, create a Conditional Access policy targeting directory roles (or the privileged groups from [04-privileged-access.md](04-privileged-access.md)), grant = require authentication strength "Phishing-resistant MFA". In Okta, set an authentication policy on the Admin Console app requiring a phishing resistant possession factor.

Roll out to all staff after admins. Start with finance, HR, executives, and people who approve payments.

## Method policy

Control: IDH-MFA-04.

- Number matching and app context on for push. In current Entra this is enforced, but check older Okta Verify configs.
- SMS and voice off. If you must keep them, scope to a named group and review it quarterly.
- Email OTP off for members. It is fine for guest one time passcode flows only.
- Temporary Access Pass on for onboarding and recovery, single use, lifetime of 1 to 8 hours.

## Registration and recovery

Control: IDH-MFA-05.

If an attacker with a stolen password can register their own authenticator, MFA did nothing.

- Entra: Conditional Access policy on user action "Register security information" requiring MFA or a compliant device or a trusted location for first time registration. Combine with Temporary Access Pass for new joiners.
- Okta: enrollment policy requires an existing factor or an admin issued temporary code.
- Help desk resets: verify identity with something the caller cannot get from LinkedIn or the HR record. A video call with the manager on the line, an in person check, or a verified ID check. Log every reset and send the user a notification to their manager.
- After any MFA reset, revoke sessions (IDH-LC-02) and watch the account for 24 hours (IDH-MFA-07, IDH-MON-05).

## Passwords

Control: IDH-MFA-06.

- Minimum 14 characters for workforce accounts. No composition rules beyond that.
- No forced periodic expiry. Change on evidence of compromise.
- Banned password list with the company name, product names, city names, and sports teams staff talk about. Entra Password Protection also covers on prem AD if you deploy the agent.
- Check against breached password lists. Entra leaked credential detection and Okta's breached password feature both do this.

## Risk based policies

Control: IDH-MFA-07.

- High user risk: require secure password change with MFA, or block if users are not yet registered for SSPR.
- High sign-in risk: require MFA, block for admins.
- Medium sign-in risk: require MFA. Monitor false positives for two weeks before tightening.
- Someone owns the risky users report. Dismissing risk without investigation is how real compromises get closed as noise.
