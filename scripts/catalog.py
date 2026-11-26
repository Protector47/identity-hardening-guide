"""Shared loader for controls/controls.yaml."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "controls" / "controls.yaml"

DOMAINS = {
    "BASE": "Tenant baseline and emergency access",
    "MFA": "Authentication and MFA",
    "CA": "Conditional Access and sign-on policy",
    "PRIV": "Privileged access",
    "APP": "Applications and OAuth",
    "WL": "Workload identities",
    "LC": "Lifecycle and access reviews",
    "MON": "Monitoring and verification",
}
SEVERITIES = ("critical", "high", "medium")
PLATFORMS = ("entra", "okta", "generic")
FIELDS = ("id", "title", "severity", "platforms", "doc", "verify")


def load():
    with CATALOG.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return data["controls"]


def domain_of(control_id):
    return control_id.split("-")[1]
