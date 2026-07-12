#!/usr/bin/env python3
"""
Deterministic quality gate for young-leaders-tech-marketplace SKILL.md / agent
.md files. Scans real markdown, applies a fixed set of pattern checks, and
prints machine-readable findings - it never asks a model to self-score or
self-certify a file. Independently written for this repo; not derived from
or dependent on any other repo's validator code.

Usage:
    python3 validate_skills.py --all --root /path/to/marketplace [--json out.json]
    python3 validate_skills.py --file /path/to/SKILL.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

DESC_CAP = 250
PII_SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
PII_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PII_EMAIL_SAFE_DOMAINS = {"example.com", "example.org", "example.net"}
EM_DASH = "—"
CANONICAL_TASK_SET = {"TaskCreate", "TaskUpdate", "TaskGet", "TaskList"}
XML_TAG_RE = re.compile(r"</?[a-zA-Z][a-zA-Z0-9_:-]*(?:\s[^<>]*)?/?>")
BLOCK_SCALAR_RE = re.compile(r":\s*[|>][+-]?\s*$", re.MULTILINE)


@dataclass
class Finding:
    check_id: str
    severity: str  # FAIL | WARN | INFO
    artifact: str
    message: str

    def to_dict(self) -> dict:
        return {
            "check_id": self.check_id,
            "severity": self.severity,
            "artifact": self.artifact,
            "message": self.message,
        }


@dataclass
class Artifact:
    path: Path
    kind: str  # skill | agent | command
    raw: str
    frontmatter_raw: str
    body: str
    frontmatter: dict = field(default_factory=dict)


def _split_frontmatter(raw: str) -> tuple[str, str]:
    if not raw.startswith("---"):
        return "", raw
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return "", raw
    return parts[1], parts[2]


def _parse_flat_frontmatter(fm_raw: str) -> dict:
    """Minimal flat-key YAML reader - enough for name/description/version/tools.
    Does not attempt full YAML; block scalars and lists are captured as raw text."""
    result: dict = {}
    lines = fm_raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, value = m.group(1), m.group(2).strip()
        if value in ("|", ">", "|-", ">-", "|+", ">+"):
            block_lines = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or lines[i].strip() == ""):
                block_lines.append(lines[i][2:] if lines[i].startswith("  ") else "")
                i += 1
            result[key] = " ".join(l.strip() for l in block_lines if l.strip())
            continue
        if value.startswith("[") and value.endswith("]"):
            result[key] = [v.strip().strip('"\'') for v in value[1:-1].split(",") if v.strip()]
        elif value == "":
            items = []
            i += 1
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:].strip())
                i += 1
            if items:
                result[key] = items
                continue
        else:
            result[key] = value.strip('"\'')
        i += 1
    return result


def discover_artifacts(root: Path) -> list[Artifact]:
    artifacts = []
    for path in sorted(root.glob("plugins/*/**/*.md")):
        if "tests" in path.parts or "node_modules" in path.parts:
            continue
        rel = path.relative_to(root)
        parts = rel.parts
        if path.name == "SKILL.md":
            kind = "skill"
        elif "agents" in parts:
            kind = "agent"
        elif "commands" in parts:
            kind = "command"
        else:
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        fm_raw, body = _split_frontmatter(raw)
        fm = _parse_flat_frontmatter(fm_raw) if fm_raw else {}
        artifacts.append(Artifact(path=path, kind=kind, raw=raw, frontmatter_raw=fm_raw, body=body, frontmatter=fm))
    return artifacts


def check_description_cap(a: Artifact) -> list[Finding]:
    desc = a.frontmatter.get("description")
    if not isinstance(desc, str):
        return []
    if len(desc) > DESC_CAP:
        return [Finding("Q1-DESC-CAP", "FAIL", str(a.path),
                         f"description is {len(desc)} chars (cap is {DESC_CAP}) - trim or move detail to the body")]
    return []


def check_pii(a: Artifact) -> list[Finding]:
    findings = []
    if PII_SSN_RE.search(a.raw):
        findings.append(Finding("Q2-PII-SSN", "FAIL", str(a.path),
                                 "possible SSN-shaped string found - replace with a placeholder"))
    for m in PII_EMAIL_RE.finditer(a.raw):
        domain = m.group(0).split("@", 1)[1].lower()
        if domain not in PII_EMAIL_SAFE_DOMAINS:
            findings.append(Finding("Q3-PII-EMAIL", "FAIL", str(a.path),
                                     f"real-looking email domain '{domain}' found - use example.com/.org/.net in examples"))
            break
    return findings


def check_em_dash(a: Artifact) -> list[Finding]:
    if EM_DASH in a.body:
        return [Finding("Q4-EM-DASH", "FAIL", str(a.path),
                         "em dash found in body - use ' - ' (space-hyphen-space) instead")]
    return []


def check_xml_tag_in_frontmatter(a: Artifact) -> list[Finding]:
    if not a.frontmatter_raw:
        return []
    scrubbed = BLOCK_SCALAR_RE.sub(":", a.frontmatter_raw)
    if XML_TAG_RE.search(scrubbed):
        return [Finding("Q5-XML-TAG", "FAIL", str(a.path),
                         "tag-shaped text found in frontmatter - move example markup to the body")]
    return []


def check_task_set(a: Artifact) -> list[Finding]:
    if a.kind not in ("skill", "agent"):
        return []
    tools = a.frontmatter.get("allowed-tools") or a.frontmatter.get("tools")
    if not isinstance(tools, list):
        return []
    present = set(tools) & CANONICAL_TASK_SET
    if present and present != CANONICAL_TASK_SET:
        missing = sorted(CANONICAL_TASK_SET - present)
        return [Finding("Q6-TASK-SET", "FAIL", str(a.path),
                         f"incomplete canonical Task* set - has {sorted(present)}, missing {missing}")]
    return []


def check_command_wrapper(a: Artifact, all_skill_paths: set[str]) -> list[Finding]:
    if a.kind != "command":
        return []
    invokes_agent = "@" in a.body and re.search(r"@[a-z][a-z0-9-]*-agent\b", a.body)
    plugin_name = a.path.parts[a.path.parts.index("plugins") + 1] if "plugins" in a.path.parts else None
    has_sibling_skill = plugin_name is not None and any(
        f"plugins/{plugin_name}/skills/" in p for p in all_skill_paths
    )
    if invokes_agent or has_sibling_skill:
        return [Finding("Q7-COMMAND-WRAPPER", "WARN", str(a.path),
                         "command wraps an agent or duplicates a sibling skill - consider retiring in favour of direct skill invocation")]
    return []


def run_checks(artifacts: list[Artifact]) -> list[Finding]:
    all_skill_paths = {str(a.path) for a in artifacts if a.kind == "skill"}
    findings: list[Finding] = []
    for a in artifacts:
        findings += check_description_cap(a)
        findings += check_pii(a)
        findings += check_em_dash(a)
        findings += check_xml_tag_in_frontmatter(a)
        findings += check_task_set(a)
        findings += check_command_wrapper(a, all_skill_paths)
    return findings


def exit_code_for(findings: list[Finding], strict: bool) -> int:
    if any(f.severity == "FAIL" for f in findings):
        return 1
    if strict and any(f.severity == "WARN" for f in findings):
        return 1
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="scan every SKILL.md/agent/command under --root")
    parser.add_argument("--file", type=Path, help="scan a single file")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", type=Path, help="write findings JSON to this path")
    parser.add_argument("--strict", action="store_true", help="WARN findings also fail the exit code")
    args = parser.parse_args(argv)

    if args.file:
        raw = args.file.read_text(encoding="utf-8", errors="replace")
        fm_raw, body = _split_frontmatter(raw)
        fm = _parse_flat_frontmatter(fm_raw) if fm_raw else {}
        kind = "skill" if args.file.name == "SKILL.md" else ("agent" if "agents" in args.file.parts else "command")
        artifacts = [Artifact(path=args.file, kind=kind, raw=raw, frontmatter_raw=fm_raw, body=body, frontmatter=fm)]
    elif args.all:
        artifacts = discover_artifacts(args.root)
    else:
        parser.error("pass --all or --file")
        return 2

    findings = run_checks(artifacts)
    counts = {"FAIL": 0, "WARN": 0, "INFO": 0}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1

    if args.json:
        args.json.write_text(json.dumps({"findings": [f.to_dict() for f in findings], "counts": counts}, indent=2))

    for f in findings:
        print(f"[{f.severity}] {f.check_id} | {f.artifact} | {f.message}")
    print(f"\n{len(artifacts)} artifacts scanned. FAIL={counts['FAIL']} WARN={counts['WARN']} INFO={counts['INFO']}")

    return exit_code_for(findings, args.strict)


if __name__ == "__main__":
    sys.exit(main())
