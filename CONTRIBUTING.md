# Contributing

Pull requests are welcome, especially from people who run Entra ID or Okta tenants in production.

## Good contributions

- A setting that moved or was renamed in the admin portal, with the new path
- Verify steps that are faster or more reliable than the current ones
- KQL or SIEM queries that you have run against real events, with the field layout you saw
- Mappings for other identity providers (Google Workspace, Ping, OneLogin) added as a separate section, not mixed into the Entra and Okta text
- Corrections where a control is wrong, weak, or causes outages you have seen

## Adding a control

1. Add it to `controls/controls.yaml` with the next number in its domain. Fill every field.
2. Explain it in the doc page named in `doc`, and mention the control id on that page.
3. Run the checks below and commit the regenerated `docs/control-index.md`.

## Out of scope

This repo is for people hardening identity systems they own. Attack tooling, token theft techniques, phishing kits, or steps for testing tenants you do not control will not be merged. Examples use placeholder domains like `contoso.onmicrosoft.com`. Never commit real tenant ids, user names, or exported logs.

## Checks

```bash
pip install -r requirements.txt
python scripts/validate_controls.py
python scripts/build_index.py && git diff --exit-code docs/control-index.md
npx markdownlint-cli2 "**/*.md"
bash scripts/check-style.sh
```

## Style

- Short, direct sentences. Write like notes for your own team.
- No em dashes or en dashes as punctuation. Use commas, periods, or parentheses.
- Every control has a verify step someone can actually run.
