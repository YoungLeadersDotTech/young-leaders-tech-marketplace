#!/usr/bin/env python3
"""Repo-wide marketplace consistency check.

Errors (exit 1):
  - any plugin JSON file (plugin.json, .mcp.json, hooks.json) or marketplace.json fails to parse
  - a plugin's VERSION, plugin.json "version" and marketplace.json entry "version" disagree
  - a marketplace entry points at a missing plugin directory, or a plugin directory has no entry
  - .mcp.json has no top-level "mcpServers" object

Warnings (printed as GitHub annotations, never fail the run - several existing plugins
predate these rules):
  - description over 250 chars, or containing a forward slash or an em dash
  - root README "Available plugins" table missing a plugin or showing a stale version

Usage: python3 scripts/validate_marketplace.py [repo_root]
"""
import json
import re
import sys
from pathlib import Path

MAX_DESC = 250
EM_DASH = chr(0x2014)

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        err(f"{path}: invalid JSON ({exc})")
        return None


def check_description(where, desc):
    if not isinstance(desc, str):
        return
    if len(desc) > MAX_DESC:
        warn(f"{where}: description is {len(desc)} chars (max {MAX_DESC})")
    if "/" in desc:
        warn(f"{where}: description contains a forward slash")
    if EM_DASH in desc:
        warn(f"{where}: description contains an em dash")


def main(root):
    market_path = root / ".claude-plugin" / "marketplace.json"
    market = load_json(market_path)
    if market is None:
        return
    entries = {p.get("name"): p for p in market.get("plugins", [])}
    plugin_dirs = {d.name: d for d in (root / "plugins").iterdir() if d.is_dir()}

    for name in sorted(set(plugin_dirs) - set(entries)):
        err(f"plugins/{name}: no entry in marketplace.json")

    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").exists() else ""
    readme_versions = dict(re.findall(r"^\|\s*\[([^\]]+)\]\([^)]*\)\s*\|\s*([0-9][^|\s]*)\s*\|", readme, re.M))

    for name, entry in sorted(entries.items()):
        src = entry.get("source", "")
        pdir = (root / src).resolve() if isinstance(src, str) else None
        if pdir is None or not pdir.is_dir():
            err(f"marketplace.json: '{name}' source {src!r} is not a directory")
            continue
        check_description(f"marketplace.json[{name}]", entry.get("description"))

        versions = {"marketplace.json": entry.get("version")}
        vfile = pdir / "VERSION"
        if vfile.exists():
            versions["VERSION"] = vfile.read_text(encoding="utf-8").strip()
        else:
            err(f"plugins/{name}: missing VERSION")
        pjson = load_json(pdir / ".claude-plugin" / "plugin.json")
        if pjson is not None:
            versions["plugin.json"] = pjson.get("version")
            check_description(f"plugins/{name}/.claude-plugin/plugin.json", pjson.get("description"))
        if len(set(versions.values())) > 1:
            err(f"plugins/{name}: version mismatch {versions}")

        mcp = pdir / ".mcp.json"
        if mcp.exists():
            data = load_json(mcp)
            if data is not None and not isinstance(data.get("mcpServers"), dict):
                err(f"plugins/{name}/.mcp.json: missing top-level 'mcpServers' object")
        for hooks in pdir.rglob("hooks.json"):
            load_json(hooks)

        if readme:
            shown = readme_versions.get(name)
            if shown is None:
                warn(f"README.md: plugin '{name}' missing from Available plugins table")
            elif shown != versions.get("VERSION"):
                warn(f"README.md: '{name}' shows {shown}, VERSION is {versions.get('VERSION')}")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve())
    for w in warnings:
        print(f"::warning::{w}")
    for e in errors:
        print(f"::error::{e}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)
