# 06. Workload identities

Service principals, managed identities, CI pipelines, and service accounts usually outnumber people. They skip MFA and most of them skip Conditional Access. Treat them as their own population.

## Managed identities first

Control: IDH-WL-01.

- Any workload running in Azure (App Service, Functions, VMs, AKS with workload identity, Container Apps) uses a managed identity.
- User assigned identities when several resources share access and lifecycle. System assigned when the identity should die with the resource.
- No app registration secret for a workload that could use a managed identity. Find them by joining your secret inventory against hosting location.

## Federation for CI/CD

Control: IDH-WL-02.

Long lived cloud keys in CI secrets are one of the most common findings in our reviews. Workload identity federation removes them: the CI platform issues a short lived OIDC token, the cloud trusts it for a specific subject, and no secret is stored.

GitHub Actions to Entra ID, federated credential on the app registration:

```json
{
  "name": "github-prod-deploy",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:your-org/payments-api:environment:production",
  "audiences": ["api://AzureADTokenExchange"]
}
```

Workflow side:

```yaml
permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
```

Pin the action to a commit SHA in real use.

Rules:

- Subject pinned to a repo plus environment, or repo plus a protected branch. Never `repo:your-org/*` style wildcards through flexible federated credentials unless you understand exactly which repos match.
- The `production` environment has required reviewers and branch protection, so the federated subject only works after approval.
- One app registration per repo and environment pair. Shared deploy identities across repos make blast radius impossible to reason about.
- Same idea for AWS (IAM OIDC provider with `sub` condition) and GCP (workload identity pool with attribute conditions).

## Scope

Control: IDH-WL-03.

- Assign roles at resource group or resource level.
- No Owner or User Access Administrator on subscriptions for pipelines. If a pipeline needs to assign roles, use a constrained role assignment condition (delegate only specific roles).
- No directory roles on service principals unless it is in the approved list with a named owner.
- Review Graph application permissions with the same list as [05-applications-and-oauth.md](05-applications-and-oauth.md).

## Monitoring

Control: IDH-WL-04.

- Alert on "Add service principal credentials" and certificate or secret changes on applications. Attackers who get Application Administrator add a credential to an existing powerful app instead of creating a new one.
- Watch service principal sign-ins from IPs outside your cloud ranges and CI ranges.
- Use Conditional Access for workload identities (Entra Workload ID) to restrict single tenant service principals to known IP ranges where it fits.
- KQL is in [08-monitoring-and-verification.md](08-monitoring-and-verification.md).

## Ownership and expiry

Control: IDH-WL-05.

Every non human account in the register has:

- Owner (person) and owning team
- System it serves
- Credential type and rotation date
- Review date, at most 12 months out

Accounts without an owner get disabled after one notice period. On prem service accounts in AD go in the same register. Prefer gMSA over static passwords there.
