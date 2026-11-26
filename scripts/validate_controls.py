"""Validate the control catalog and its links to the docs.

Checks:
  - every control has the required fields with allowed values
  - ids are unique, well formed, and numbered without gaps per domain
  - the doc page exists and mentions the control id
  - every IDH id mentioned anywhere in docs/ or templates/ exists in the catalog
"""
import re
import sys

from catalog import DOMAINS, FIELDS, PLATFORMS, ROOT, SEVERITIES, load

ID_RE = re.compile(r"^IDH-([A-Z]+)-(\d{2})$")
REF_RE = re.compile(r"IDH-[A-Z]+-\d{2}")


def main():
    errors = []
    controls = load()
    seen = {}
    numbers = {}
    for c in controls:
        cid = c.get("id", "<missing id>")
        for field in FIELDS:
            if not c.get(field):
                errors.append(f"{cid}: missing field '{field}'")
        m = ID_RE.match(cid)
        if not m:
            errors.append(f"{cid}: id does not match IDH-<DOMAIN>-NN")
            continue
        if m.group(1) not in DOMAINS:
            errors.append(f"{cid}: unknown domain {m.group(1)}")
        if cid in seen:
            errors.append(f"{cid}: duplicate id")
        seen[cid] = c
        numbers.setdefault(m.group(1), []).append(int(m.group(2)))
        if c.get("severity") not in SEVERITIES:
            errors.append(f"{cid}: severity must be one of {SEVERITIES}")
        bad = [p for p in c.get("platforms", []) if p not in PLATFORMS]
        if bad:
            errors.append(f"{cid}: unknown platforms {bad}")
        doc = ROOT / c.get("doc", "")
        if not doc.is_file():
            errors.append(f"{cid}: doc {c.get('doc')} not found")
        elif cid not in doc.read_text(encoding="utf-8"):
            errors.append(f"{cid}: not mentioned in {c['doc']}")
        if len(c.get("title", "")) > 200:
            errors.append(f"{cid}: title longer than 200 characters")

    for domain, nums in numbers.items():
        expected = list(range(1, len(nums) + 1))
        if sorted(nums) != expected:
            errors.append(f"{domain}: control numbers have gaps or are out of order: {sorted(nums)}")

    for folder in ("docs", "templates"):
        for path in sorted((ROOT / folder).rglob("*.md")):
            if path.name == "control-index.md":
                continue
            for ref in sorted(set(REF_RE.findall(path.read_text(encoding="utf-8")))):
                if ref not in seen:
                    errors.append(f"{path.relative_to(ROOT)}: references unknown control {ref}")

    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} problem(s) found.")
        sys.exit(1)
    print(f"Catalog OK: {len(controls)} controls across {len(numbers)} domains.")


if __name__ == "__main__":
    main()
