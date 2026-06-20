#!/usr/bin/env python3
"""
check_plugin_version_sync.py - enforce the marketplace 5-file version-sync rule.

The rule (see references/marketplace-guidelines.md): when any file inside plugins/<name>/
changes, all five of these must agree in the same commit or PR:
  1. <plugin>/VERSION
  2. <plugin>/CHANGELOG.md      (a heading for the VERSION must exist)
  3. <plugin>/.claude-plugin/plugin.json   ("version" field)
  4. <marketplace>/.claude-plugin/marketplace.json   (this plugin's entry "version")
  5. <plugin>/README.md        (a version header that names the current VERSION)

marketplace.json carries two version fields and both move on a plugin change: the per-plugin
entry (must equal VERSION) and the top-level version (a patch bump on any plugin change).
When --prev-marketplace is given, this gate also checks that the top-level version advanced.

Usage:
    check_plugin_version_sync.py --plugin <plugin-dir> --marketplace <marketplace.json>
                                 [--prev-marketplace <old.json>]
Exit codes:
    0 = the five files agree
    1 = a mismatch (printed)
    2 = could not run (bad args / unreadable files / unparseable JSON)
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys


def read_version(path: pathlib.Path) -> str | None:
    try:
        return path.read_text().strip()
    except OSError:
        return None


def load_json(path: pathlib.Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def changelog_has_heading(path: pathlib.Path, version: str) -> bool:
    try:
        text = path.read_text()
    except OSError:
        return False
    return bool(re.search(rf"^##\s*\[?{re.escape(version)}\]?", text, re.M))


def readme_names_version(path: pathlib.Path, version: str) -> bool:
    try:
        text = path.read_text()
    except OSError:
        return False
    patterns = [
        rf"^\s*\*\*Version:?\*\*\s*:?\s*v?{re.escape(version)}\s*$",
        rf"^\s*\*\*Version:?\s+v?{re.escape(version)}\*\*\s*$",
        rf"^\s*#+\s+Version:?\s+v?{re.escape(version)}\s*$",
        rf"^\s*#+\s+.+\s+-\s+v?{re.escape(version)}\s*$",
    ]
    return any(re.search(pattern, text, re.M) for pattern in patterns)


def marketplace_entry_version(marketplace: dict, plugin_name: str) -> str | None:
    for entry in marketplace.get("plugins", []):
        if entry.get("name") == plugin_name:
            return entry.get("version")
    return None


def parse_semver(version: str | None) -> tuple[int, int, int] | None:
    if not version:
        return None
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version.strip())
    return tuple(int(part) for part in match.groups()) if match else None


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin", required=True)
    parser.add_argument("--marketplace", required=True)
    parser.add_argument("--prev-marketplace")
    args = parser.parse_args(argv)

    plugin_dir = pathlib.Path(args.plugin)
    if not plugin_dir.is_dir():
        print(f"Plugin dir not found: {plugin_dir}", file=sys.stderr)
        return 2

    marketplace_path = pathlib.Path(args.marketplace)
    if not marketplace_path.exists():
        print(f"marketplace.json not found: {marketplace_path}", file=sys.stderr)
        return 2

    plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
    plugin_json = load_json(plugin_json_path)
    marketplace = load_json(marketplace_path)
    if plugin_json is None:
        print(f"Could not parse plugin.json at {plugin_json_path}", file=sys.stderr)
        return 2
    if marketplace is None:
        print(f"Could not parse marketplace.json at {marketplace_path}", file=sys.stderr)
        return 2

    version_file = read_version(plugin_dir / "VERSION")
    plugin_name = plugin_json.get("name") or plugin_dir.name
    plugin_json_version = plugin_json.get("version")
    marketplace_version = marketplace_entry_version(marketplace, plugin_name)

    problems: list[str] = []
    if version_file is None:
        problems.append("VERSION file missing or unreadable")
    if plugin_json_version is None:
        problems.append("plugin.json has no version field")
    if marketplace_version is None:
        problems.append(f"no marketplace entry named '{plugin_name}'")

    versions = {
        "VERSION": version_file,
        "plugin.json": plugin_json_version,
        "marketplace.json": marketplace_version,
    }
    distinct_versions = {value for value in versions.values() if value is not None}
    if len(distinct_versions) > 1:
        problems.append("version mismatch: " + ", ".join(f"{key}={value}" for key, value in versions.items()))

    if version_file and not changelog_has_heading(plugin_dir / "CHANGELOG.md", version_file):
        problems.append(f"CHANGELOG.md has no heading for version {version_file}")

    if version_file and not readme_names_version(plugin_dir / "README.md", version_file):
        problems.append(f"README.md has no version header naming {version_file}")

    if args.prev_marketplace:
        previous = load_json(pathlib.Path(args.prev_marketplace))
        if previous is None:
            print("Could not parse --prev-marketplace JSON", file=sys.stderr)
            return 2
        previous_top = parse_semver(previous.get("version"))
        current_top = parse_semver(marketplace.get("version"))
        if previous_top is None or current_top is None:
            problems.append("could not parse top-level marketplace semver")
        elif current_top == previous_top:
            problems.append(
                f"top-level marketplace version did not change ({marketplace.get('version')}); "
                "the 5-file rule requires a patch bump on any plugin change"
            )
        elif current_top < previous_top:
            problems.append(
                f"top-level marketplace version went backwards ({previous.get('version')} -> {marketplace.get('version')})"
            )

    if problems:
        print(f"5-file version-sync FAILED for '{plugin_name}':", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    print(
        f"5-file version-sync ok for '{plugin_name}': VERSION, CHANGELOG, plugin.json, marketplace entry, "
        f"and README all name {version_file}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
