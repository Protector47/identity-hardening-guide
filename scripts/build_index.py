"""Generate docs/control-index.md from controls/controls.yaml.

CI regenerates the file and fails if the committed copy differs.
"""
from catalog import DOMAINS, ROOT, domain_of, load

OUT = ROOT / "docs" / "control-index.md"
LABELS = {"entra": "Entra ID", "okta": "Okta", "generic": "Any IdP"}


def main():
    controls = load()
    lines = [
        "# Control index",
        "",
        "Generated from [controls/controls.yaml](../controls/controls.yaml) by `scripts/build_index.py`. Do not edit by hand.",
        "",
    ]
    counts = {s: sum(1 for c in controls if c["severity"] == s) for s in ("critical", "high", "medium")}
    lines.append(
        f"{len(controls)} controls: {counts['critical']} critical, {counts['high']} high, {counts['medium']} medium."
    )
    lines.append("")
    for key, name in DOMAINS.items():
        rows = [c for c in controls if domain_of(c["id"]) == key]
        if not rows:
            continue
        lines += [f"## {name}", "", "| ID | Control | Severity | Platforms | Verify |", "| --- | --- | --- | --- | --- |"]
        for c in rows:
            doc = c["doc"].replace("docs/", "")
            platforms = ", ".join(LABELS[p] for p in c["platforms"])
            lines.append(
                f"| [{c['id']}]({doc}) | {c['title']} | {c['severity']} | {platforms} | {c['verify']} |"
            )
        lines.append("")
    OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(controls)} controls.")


if __name__ == "__main__":
    main()
