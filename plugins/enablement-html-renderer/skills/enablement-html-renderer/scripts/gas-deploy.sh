#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: gas-deploy.sh [bundle_dir] [script_title]

Deploy an enablement HTML Apps Script bundle in place.

Expected files in bundle_dir:
  - Index.html
  - Code.gs
  - appsscript.json

Optional environment variables:
  GAS_WEBAPP_ACCESS       Override webapp.access in appsscript.json (default bundle uses DOMAIN)
  GAS_SCRIPT_ID           Reuse an existing Apps Script project when .clasp.json is absent
  GAS_DEPLOYMENT_ID       Redeploy an existing web app deployment to preserve its /exec URL
  GAS_DEPLOY_DESCRIPTION  Description used for clasp version/deploy

Example:
  GAS_WEBAPP_ACCESS=ANYONE ./gas-deploy.sh ./my-bundle "Enablement handoff"
  GAS_SCRIPT_ID=abc123 GAS_DEPLOYMENT_ID=AKfycb... ./gas-deploy.sh ./my-bundle "Enablement handoff"
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if ! command -v clasp >/dev/null 2>&1; then
  printf 'clasp is not installed. Install with: npm install -g @google/clasp\n' >&2
  exit 1
fi

BUNDLE_DIR="${1:-$(pwd)}"
SCRIPT_TITLE="${2:-Enablement HTML Renderer}"
DEPLOY_DESCRIPTION="${GAS_DEPLOY_DESCRIPTION:-Enablement HTML Renderer web app}"

for required in Index.html Code.gs appsscript.json; do
  if [[ ! -f "$BUNDLE_DIR/$required" ]]; then
    printf 'Missing required file: %s\n' "$BUNDLE_DIR/$required" >&2
    exit 1
  fi
done

pushd "$BUNDLE_DIR" >/dev/null

manifest_backup="$(mktemp)"
cp appsscript.json "$manifest_backup"
cleanup() {
  rm -f "$manifest_backup"
}
trap cleanup EXIT

if [[ -n "${GAS_WEBAPP_ACCESS:-}" ]]; then
  python3 - "$PWD/appsscript.json" "$GAS_WEBAPP_ACCESS" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
access = sys.argv[2]
data = json.loads(path.read_text())
data.setdefault("webapp", {})["access"] = access
path.write_text(json.dumps(data, indent=2) + "\n")
PY
fi

if [[ ! -f .clasp.json ]]; then
  if [[ -n "${GAS_SCRIPT_ID:-}" ]]; then
    printf 'No .clasp.json found. Reusing GAS_SCRIPT_ID=%s\n' "$GAS_SCRIPT_ID"
    printf '{"scriptId":"%s","rootDir":"."}\n' "$GAS_SCRIPT_ID" > .clasp.json
  else
    printf 'No .clasp.json found. Creating a new standalone Apps Script project...\n'
    clasp create --title "$SCRIPT_TITLE" --type standalone
    cp "$manifest_backup" appsscript.json
  fi
  if [[ -n "${GAS_WEBAPP_ACCESS:-}" ]]; then
    python3 - "$PWD/appsscript.json" "$GAS_WEBAPP_ACCESS" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
access = sys.argv[2]
data = json.loads(path.read_text())
data.setdefault("webapp", {})["access"] = access
path.write_text(json.dumps(data, indent=2) + "\n")
PY
  fi
fi

printf 'Pushing bundle with clasp...\n'
clasp push --force

printf 'Creating version...\n'
version_output="$(clasp version "$DEPLOY_DESCRIPTION" 2>&1)"
printf '%s\n' "$version_output"
version_number="$(VERSION_OUTPUT="$version_output" python3 - <<'PY'
import os
import re

text = os.environ.get("VERSION_OUTPUT", "")
match = re.search(r'version\s+(\d+)', text, re.I)
if match:
    print(match.group(1))
PY
)"

printf 'Deploying web app...\n'
if [[ -n "${GAS_DEPLOYMENT_ID:-}" && -n "$version_number" ]]; then
  deploy_output="$(clasp redeploy "$GAS_DEPLOYMENT_ID" --versionNumber "$version_number" --description "$DEPLOY_DESCRIPTION" 2>&1)"
elif [[ -n "$version_number" ]]; then
  deploy_output="$(clasp deploy --versionNumber "$version_number" --description "$DEPLOY_DESCRIPTION" 2>&1)"
else
  deploy_output="$(clasp deploy --description "$DEPLOY_DESCRIPTION" 2>&1)"
fi
printf '%s\n' "$deploy_output"

deployment_id="${GAS_DEPLOYMENT_ID:-}"
if [[ -z "$deployment_id" ]]; then
  deployment_id="$(DEPLOY_OUTPUT="$deploy_output" python3 - <<'PY'
import os
import re

text = os.environ.get("DEPLOY_OUTPUT", "")
match = re.search(r'(AK[A-Za-z0-9_-]+)', text)
if match:
    print(match.group(1))
PY
)"
fi

if [[ -n "$deployment_id" ]]; then
  printf '\nLive URL: https://script.google.com/macros/s/%s/exec\n' "$deployment_id"
  if [[ -z "${GAS_DEPLOYMENT_ID:-}" ]]; then
    printf 'Reuse this URL next time by setting GAS_DEPLOYMENT_ID=%s\n' "$deployment_id"
  fi
else
  printf '\nDeployment created, but the deploy output did not expose a deployment id.\n' >&2
  printf 'Run `clasp deployments` here and open the matching web app URL.\n' >&2
fi

popd >/dev/null
