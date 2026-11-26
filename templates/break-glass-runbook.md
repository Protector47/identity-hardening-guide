# Break glass runbook

Related controls: IDH-BASE-01, IDH-BASE-02.

## Accounts

| Account | Key serials | Safe location | Custodians |
| --- | --- | --- | --- |
| bg-01@ | | | |
| bg-02@ | | | |

## When to use

- All admins locked out by a Conditional Access or sign-on policy change
- Federation or sync outage blocks admin sign-in
- MFA provider outage

Not for: routine admin work, PIM being slow, a single admin forgetting their key.

## Procedure

1. Incident commander approves use and opens an incident ticket.
2. Two custodians retrieve the key. Log the time.
3. Sign in from a known clean device. Note the IP.
4. Make the minimum change to restore normal admin access. Record each change.
5. Sign out. Return the key to the safe.
6. SOC confirms the alert fired and links it to the ticket.
7. Within 24 hours: review every audit event from the session, rotate anything exposed, write up the cause.

## Monthly test

| Date | Account | Tester | Alert fired (yes/no, minutes) | Notes |
| --- | --- | --- | --- | --- |
| | | | | |
