#!/usr/bin/env bash
# Fails if any Markdown or YAML file contains an em dash or en dash.
set -euo pipefail
cd "$(dirname "$0")/.."
pattern=$'\u2014|\u2013'
if grep -rnP "$pattern" --include='*.md' --include='*.yml' --include='*.yaml' --include='*.svg' . --exclude-dir=node_modules --exclude-dir=.git; then
  echo "Found em/en dash characters. Replace them with commas, periods, or parentheses." >&2
  exit 1
fi
echo "Style check passed."
