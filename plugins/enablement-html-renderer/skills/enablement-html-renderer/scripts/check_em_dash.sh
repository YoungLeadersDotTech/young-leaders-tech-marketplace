#!/usr/bin/env bash
# check_em_dash.sh - fail if an em dash (U+2014) appears in the given path(s).
# Matches the raw UTF-8 bytes (E2 80 94) so it works regardless of locale.
# Em dashes are banned in frontmatter and authored bodies.
# Usage: check_em_dash.sh <path> [path...]
set -uo pipefail
[ $# -ge 1 ] || { echo "Usage: $0 <path> [path...]" >&2; exit 1; }
if grep -rInP '\xe2\x80\x94' "$@" 2>/dev/null; then
  echo "" >&2
  echo "Em dash(es) found above. Replace with ' - ', ': ', or a rewrite." >&2
  exit 1
fi
echo "No em dashes."
exit 0
