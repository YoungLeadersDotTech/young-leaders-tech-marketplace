#!/usr/bin/env python3
"""check_drift.py - detect drift between canonical sources and generated OpenCode files.

Part of the opencode-sync skill. Reads the manifest written by sync_agents.py
(default .opencode-sync/manifest.json), which records, per generated file, the
sha256 of both its canonical source and the generated output at sync time.

Modes:
  --check    Compare current on-disk hashes against the manifest and report drift.
             Exit 0 if everything is in sync, 1 if any drift is found (CI gate).
  --update   Re-baseline: recompute and store current hashes for every tracked
             file. Use after an intentional manual change you want to bless, or
             to bootstrap a manifest from already-generated files.

Drift classes (per file):
  OK                 source and generated both match the manifest
  CANONICAL_CHANGED  the source .md changed since the last sync - regenerate
  GENERATED_EDITED   the generated file was hand-edited - canonical wins;
                     regenerate, or back-port the edit into the source first (E8)
  MISSING            the generated file is gone - regenerate
  SOURCE_MISSING     the canonical source is gone - stale manifest entry

First-run behaviour (E7): if the manifest does not exist, --check prints a
first-run note and exits 0 (nothing has been synced yet, so nothing can drift).

Usage:
  python3 check_drift.py --check  [--manifest .opencode-sync/manifest.json]
  python3 check_drift.py --update [--manifest .opencode-sync/manifest.json]

Exit codes: 0 in sync (or first run) | 1 drift found | 2 bad manifest / bad args
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_manifest(path):
    p = Path(path)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        print(f"ERROR: manifest {p} is not valid JSON", file=sys.stderr)
        sys.exit(2)


def classify(generated_path, entry):
    """Return a drift class string for one manifest entry."""
    gen = Path(generated_path)
    src = Path(entry.get("source", ""))
    if not gen.exists():
        return "MISSING"
    if not src.exists():
        return "SOURCE_MISSING"
    if sha256_file(gen) != entry.get("generated_sha256"):
        return "GENERATED_EDITED"
    if sha256_file(src) != entry.get("source_sha256"):
        return "CANONICAL_CHANGED"
    return "OK"


HINTS = {
    "CANONICAL_CHANGED": "source edited - re-run sync_agents.py for this file",
    "GENERATED_EDITED": "hand-edited output - canonical wins; regenerate or back-port first (E8)",
    "MISSING": "generated file deleted - regenerate",
    "SOURCE_MISSING": "canonical source gone - stale entry; remove from manifest or restore source",
}


def cmd_check(manifest, manifest_path):
    if manifest is None:
        print(f"first run: no manifest at {manifest_path} - nothing synced yet, no drift possible (E7)")
        return 0
    generated = manifest.get("generated", {})
    if not generated:
        print("manifest has no tracked files - nothing to check")
        return 0
    drift = []
    for gen_path, entry in sorted(generated.items()):
        cls = classify(gen_path, entry)
        flag = "OK  " if cls == "OK" else "DRIFT"
        print(f"{flag} {cls:18} {gen_path}")
        if cls != "OK":
            print(f"      -> {HINTS.get(cls, '')}")
            drift.append((gen_path, cls))
    print()
    if drift:
        print(f"DRIFT: {len(drift)} of {len(generated)} tracked file(s) out of sync")
        return 1
    print(f"in sync: {len(generated)} tracked file(s)")
    return 0


def cmd_update(manifest, manifest_path):
    if manifest is None:
        print(f"ERROR: no manifest at {manifest_path} - run sync_agents.py first to create one", file=sys.stderr)
        return 2
    generated = manifest.get("generated", {})
    rebased, dropped = 0, 0
    for gen_path, entry in sorted(generated.items()):
        gen, src = Path(gen_path), Path(entry.get("source", ""))
        if not gen.exists() or not src.exists():
            print(f"drop {gen_path} (missing file) - leaving entry, fix manually")
            dropped += 1
            continue
        entry["source_sha256"] = sha256_file(src)
        entry["generated_sha256"] = sha256_file(gen)
        rebased += 1
        print(f"rebaselined {gen_path}")
    Path(manifest_path).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"\nmanifest updated: {rebased} rebaselined, {dropped} need attention")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="report drift, exit 1 if any found")
    g.add_argument("--update", action="store_true", help="re-baseline current hashes into the manifest")
    ap.add_argument("--manifest", default=".opencode-sync/manifest.json")
    args = ap.parse_args()

    manifest = load_manifest(args.manifest)
    if args.check:
        return cmd_check(manifest, args.manifest)
    return cmd_update(manifest, args.manifest)


if __name__ == "__main__":
    sys.exit(main())
