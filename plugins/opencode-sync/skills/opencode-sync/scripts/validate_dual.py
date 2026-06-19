#!/usr/bin/env python3
"""validate_dual.py - dual-runtime validator for skills, agents and commands.

Part of the opencode-sync skill. Runs the mechanical rule inventory documented
in references/validator-rules.md against SKILL.md, agent and command files, for
one or both runtimes. Point it at a single file, a plugin, a whole repo, or a
.claude tree - it discovers the assessable tools and skips plain docs/READMEs.

Rule families:
  SH-*  shared      apply to both Claude Code and OpenCode
  CC-*  claude      Claude Code packaging rules
  OC-*  opencode    OpenCode schema rules
  TR-*  translation portability / drift-trap rules (Claude -> OpenCode)

--target selects the families:
  claude    -> SH + CC
  opencode  -> SH + OC + TR
  both      -> all (default)

--depth controls discovery when a directory is given:
  shallow   one plugin/skill: <dir>/SKILL.md, <dir>/skills/*/SKILL.md,
            <dir>/agents/*.md, <dir>/commands/*.md (no recursion into nested repos)
  standard  whole tree, source only: every skills/*/SKILL.md, */agents/*.md,
            */commands/*.md, skipping hidden dirs (including .claude caches),
            .git, node_modules and build dirs (default)
  deep      everything standard finds PLUS hidden dirs - .claude/skills,
            .claude/agents, submodules, installed-skill caches

Discovery classifies by location, mirroring the catalogue-tools convention:
  SKILL.md                 -> skill
  *.md inside an agents/    -> agent
  *.md inside a commands/   -> command
Anything else (README.md, docs, references) is not a tool and is ignored.

Severities: FAIL (blocks), WARN (should fix), INFO (awareness). Exit is non-zero
if any FAIL is present, so this doubles as a CI gate.

Usage:
  python3 validate_dual.py --target both --depth standard <path> [more paths ...]
  python3 validate_dual.py --list --depth deep <repo>        # preview, no validation
  python3 validate_dual.py --target both --json report.json <repo>

Exit codes: 0 no FAIL | 1 one or more FAIL | 2 nothing assessable found
"""

import argparse
import collections
import json
import os
import re
import sys
from pathlib import Path

KNOWN_CLAUDE_TOOLS = {
    "Read", "Write", "Edit", "Bash", "Glob", "Grep", "WebFetch", "WebSearch",
    "Task", "Agent", "TaskCreate", "TaskUpdate", "TaskGet", "TaskList", "Skill",
    "AskUserQuestion", "NotebookEdit", "ToolSearch", "SendMessage",
    "ScheduleWakeup", "EnterPlanMode", "ExitPlanMode",
}

CLAUDE_ONLY_IN_BODY = [
    "AskUserQuestion", "TaskCreate", "TaskUpdate", "TaskGet", "TaskList",
    "SendMessage", "ScheduleWakeup", "EnterPlanMode", "ToolSearch",
]

HARD_CONSTRUCTS = {
    "SendMessage": r"\bSendMessage\b",
    "ScheduleWakeup": r"\bScheduleWakeup\b",
    "EnterPlanMode": r"\bEnterPlanMode\b",
    "ExitPlanMode": r"\bExitPlanMode\b",
    "EnterWorktree": r"\bEnterWorktree\b",
    "ExitWorktree": r"\bExitWorktree\b",
    "hooks.json": r"\bhooks\.json\b",
    "CLAUDE_PLUGIN_ROOT": r"\$\{?CLAUDE_PLUGIN_ROOT\}?",
}

MITIGATION = re.compile(
    r"(runtime compatibility|graceful[- ]?degrad|fallback|todowrite|plain[- ]?text|"
    r"if .{0,40}(unavailable|not available|is available))",
    re.IGNORECASE,
)

OPENCODE_AGENT_MODES = {"primary", "subagent", "all"}
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Directories never worth walking into, at any depth.
ALWAYS_PRUNE = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", ".pytest_cache",
    ".mypy_cache", ".idea", "dist", "build", ".skills-build", "site-packages",
}


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------


def classify(path):
    """Return 'skill' / 'agent' / 'command' for an assessable file, else None."""
    p = Path(path)
    if p.name == "SKILL.md":
        return "skill"
    if p.suffix == ".md" and not p.name.startswith("."):
        if p.parent.name == "agents":
            return "agent"
        if p.parent.name == "commands":
            return "command"
    return None


def _plugin_files(base):
    """Shallow: treat base as one plugin or one skill dir."""
    base = Path(base)
    out = []
    if (base / "SKILL.md").exists():
        out.append((base / "SKILL.md", "skill"))
    skills = base / "skills"
    if skills.is_dir():
        for sd in sorted(skills.iterdir()):
            if sd.is_dir() and not sd.name.startswith(".") and (sd / "SKILL.md").exists():
                out.append((sd / "SKILL.md", "skill"))
    for sub, kind in (("agents", "agent"), ("commands", "command")):
        d = base / sub
        if d.is_dir():
            for f in sorted(d.glob("*.md")):
                if not f.name.startswith("."):
                    out.append((f, kind))
    return out


def discover(root, depth):
    """Return a sorted, de-duplicated list of (Path, kind)."""
    root = Path(root).expanduser()
    if root.is_file():
        k = classify(root)
        return [(root, k or "skill")]
    if not root.exists():
        return []
    if depth == "shallow":
        return _plugin_files(root)

    include_hidden = depth == "deep"
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if d not in ALWAYS_PRUNE and (include_hidden or not d.startswith("."))
        ]
        for fn in filenames:
            full = Path(dirpath) / fn
            kind = classify(full)
            if kind:
                found.append((full, kind))
    seen, uniq = set(), []
    for f, k in sorted(found, key=lambda x: str(x[0])):
        if f not in seen:
            seen.add(f)
            uniq.append((f, k))
    return uniq


def collect(paths, depth):
    out, seen = [], set()
    for raw in paths:
        for f, k in discover(raw, depth):
            if f not in seen:
                seen.add(f)
                out.append((f, k))
    return out


# ---------------------------------------------------------------------------
# Frontmatter helpers
# ---------------------------------------------------------------------------


def split_frontmatter(text):
    if not text.startswith("---"):
        return None, text, 0
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return None, text, 0
    return m.group(1), text[m.end():], 0


def fm_get(fm, key):
    m = re.search(rf"^{re.escape(key)}:\s*(.*)$", fm, re.MULTILINE)
    if not m:
        return None
    val = m.group(1).strip()
    if val in (">", ">-", "|", "|-", ""):
        lines = fm.splitlines()
        idx = next((i for i, ln in enumerate(lines) if re.match(rf"^{re.escape(key)}:", ln)), None)
        collected = []
        for ln in lines[idx + 1:]:
            if re.match(r"^\s+\S", ln):
                collected.append(ln.strip().lstrip("- ").strip())
            elif ln.strip() == "":
                continue
            else:
                break
        return " ".join(collected) if collected else ""
    return val.strip("'\"")


def fm_list(fm, key):
    lines = fm.splitlines()
    idx = next((i for i, ln in enumerate(lines) if re.match(rf"^{re.escape(key)}:\s*$", ln)), None)
    if idx is None:
        return None
    out = []
    for ln in lines[idx + 1:]:
        if re.match(r"^\s*-\s+", ln):
            out.append(re.sub(r"^\s*-\s+", "", ln).strip().strip("'\""))
        elif ln.strip() == "":
            continue
        else:
            break
    return out


def line_of(text, pattern):
    m = re.search(pattern, text)
    if not m:
        return None
    return text[:m.start()].count("\n") + 1


class Finding:
    def __init__(self, sev, rule, msg, line=None):
        self.sev, self.rule, self.msg, self.line = sev, rule, msg, line

    def as_row(self, path):
        loc = f"{path}:{self.line}" if self.line else path
        return f"{self.sev:4} [{self.rule}] {loc}  {self.msg}"

    def as_dict(self, path, kind):
        return {"severity": self.sev, "rule": self.rule, "file": path,
                "kind": kind, "line": self.line, "message": self.msg}


# ---------------------------------------------------------------------------
# Rule families
# ---------------------------------------------------------------------------


def rules_shared(path, fm, body, full, kind):
    f = []
    if fm is None:
        f.append(Finding("FAIL", "SH-01", "no parseable YAML frontmatter", 1))
        return f
    if kind == "skill":
        name = fm_get(fm, "name")
        folder = Path(path).resolve().parent.name
        if not name:
            f.append(Finding("FAIL", "SH-03", "skill has no name field"))
        elif not KEBAB.match(name):
            f.append(Finding("FAIL", "SH-02", f"name '{name}' is not kebab-case"))
        elif name != folder:
            f.append(Finding("FAIL", "SH-02", f"name '{name}' does not match folder '{folder}'"))
    if not fm_get(fm, "description"):
        f.append(Finding("FAIL", "SH-03", "missing description"))
    if "—" in full:
        f.append(Finding("FAIL", "SH-04", "em dash present - replace with ' - '", line_of(full, "—")))
    if re.search(r"/Users/[A-Za-z]", full):
        f.append(Finding("WARN", "SH-05", "hardcoded /Users/ path - use ~ or a config value", line_of(full, r"/Users/[A-Za-z]")))
    if kind == "skill" and Path(path).name != "SKILL.md":
        f.append(Finding("WARN", "SH-06", f"skill file should be SKILL.md, found {Path(path).name}"))
    return f


def rules_claude(path, fm, body, full, kind):
    f = []
    if fm is None:
        return f
    desc = fm_get(fm, "description") or ""
    n = len(desc)
    if n > 1024:
        f.append(Finding("FAIL", "CC-01", f"description {n} chars exceeds the 1024 hard cap"))
    elif n > 250:
        f.append(Finding("WARN", "CC-01", f"description {n} chars over the 250 working cap (listing truncates)"))
    tools = fm_list(fm, "allowed-tools") or fm_list(fm, "tools")
    if tools:
        for t in tools:
            if t == "TodoWrite":
                f.append(Finding("FAIL", "CC-03", "'TodoWrite' in allowed-tools - replace with TaskCreate / TaskUpdate / TaskGet / TaskList"))
            elif t == "Task":
                f.append(Finding("WARN", "CC-03", "generic 'Task' in allowed-tools - prefer specific TaskCreate / TaskUpdate / TaskGet / TaskList (Task / Agent itself is valid for subagent dispatch)"))
            elif t not in KNOWN_CLAUDE_TOOLS and not t.startswith("mcp__"):
                f.append(Finding("WARN", "CC-02", f"unknown tool name '{t}' in allowlist"))
    return f


def rules_opencode(path, fm, body, full, kind):
    f = []
    if fm is None:
        return f
    desc = fm_get(fm, "description") or ""
    if len(desc) > 1024:
        f.append(Finding("FAIL", "OC-01", f"description {len(desc)} chars exceeds OpenCode's 1024 cap"))
    if kind in ("agent", "command"):
        mode = fm_get(fm, "mode")
        if mode and mode not in OPENCODE_AGENT_MODES:
            f.append(Finding("FAIL", "OC-02", f"agent mode '{mode}' not in {sorted(OPENCODE_AGENT_MODES)}"))
        model = fm_get(fm, "model")
        if model and "/" not in model:
            f.append(Finding("WARN", "OC-03", f"model '{model}' has no provider/ prefix - OpenCode needs provider/model-id"))
    if kind == "skill":
        ignored = []
        for fld in ("allowed-tools", "disable-model-invocation", "version", "category", "tags", "user-invocable", "last-updated"):
            if re.search(rf"^{re.escape(fld)}:", fm, re.MULTILINE):
                ignored.append(fld)
        if ignored:
            f.append(Finding("INFO", "OC-04", "fields OpenCode ignores silently: " + ", ".join(ignored)))
    mitigated = bool(MITIGATION.search(full))
    for tool in CLAUDE_ONLY_IN_BODY:
        if re.search(rf"\b{tool}\b", body) and not mitigated:
            f.append(Finding("WARN", "OC-05", f"body uses {tool} with no degradation wording for OpenCode", line_of(body, rf"\b{tool}\b")))
            break
    # OC-06: a skill that STOPS when Task* is unavailable is OpenCode-hostile. OpenCode has no
    # TaskCreate, so the correct behaviour is to degrade to a todowrite checklist, never to halt.
    # Forward-order match (Task* ... unavailable ... halt) within one sentence keeps the capability
    # preamble itself - which describes the anti-pattern in the reverse order - from false-positiving.
    if re.search(r"\bTask(Create|Update|Get|List)?\b", body):
        hostile = re.search(
            r"\bTask(Create|Update|Get|List)?\b[^.\n]{0,160}?"
            r"\b(unavailable|not available|missing|absent|does not exist|isn'?t available|is not available)\b"
            r"[^.\n]{0,160}?\b(stop|abort|halt|bail|refuse|cannot (proceed|continue)|do not (proceed|continue))\b",
            full, re.IGNORECASE)
        if hostile:
            f.append(Finding("WARN", "OC-06",
                             "OpenCode-hostile: stops/aborts when Task* is unavailable instead of degrading "
                             "to a todowrite checklist (see references/capability-preamble.md)",
                             line_of(full, r"(unavailable|not available|abort|halt|stop)")))
    return f


def rules_translation(path, fm, body, full, kind):
    f = []
    for label, pat in HARD_CONSTRUCTS.items():
        if re.search(pat, full, re.MULTILINE):
            f.append(Finding("WARN", "TR-02", f"Claude-only construct '{label}' has no OpenCode equivalent", line_of(full, pat)))
    if re.search(r"\bmcp__[A-Za-z0-9_]+", full):
        f.append(Finding("INFO", "TR-03", "mcp__ tool prefix in a shared body - MCP tool names differ per OpenCode server config", line_of(full, r"\bmcp__[A-Za-z0-9_]+")))
    if fm and re.search(r"^disable-model-invocation:\s*true", fm, re.MULTILINE):
        f.append(Finding("WARN", "TR-04", "disable-model-invocation: true is ignored by OpenCode - skill becomes model-invocable there"))
    return f


def validate_file(path, kind, target):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    fm, body, _ = split_frontmatter(text)
    findings = rules_shared(str(path), fm, body, text, kind)
    if target in ("claude", "both"):
        findings += rules_claude(str(path), fm, body, text, kind)
    if target in ("opencode", "both"):
        findings += rules_opencode(str(path), fm, body, text, kind)
        findings += rules_translation(str(path), fm, body, text, kind)
    return findings


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def print_aggregate(rows, kind_counts):
    byrule = collections.Counter((r["rule"], r["severity"]) for r in rows)
    order = {"FAIL": 0, "WARN": 1, "INFO": 2}
    print("Findings by rule:")
    for (rule, sev), n in sorted(byrule.items(), key=lambda kv: (order[kv[0][1]], -kv[1])):
        print(f"  {n:5}  {sev:4} {rule}")
    fails = collections.defaultdict(list)
    for r in rows:
        if r["severity"] == "FAIL":
            loc = f'{r["rule"]} (line {r["line"]})' if r["line"] else r["rule"]
            fails[r["file"]].append(loc)
    if fails:
        print(f"\nFiles with FAIL ({len(fails)}):")
        for fp, rs in sorted(fails.items()):
            print(f"  {fp}\n        {', '.join(rs)}")
    print("\nAssessed by kind: " + ", ".join(f"{v} {k}" for k, v in sorted(kind_counts.items())))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--target", choices=["claude", "opencode", "both"], default="both")
    ap.add_argument("--depth", choices=["shallow", "standard", "deep"], default="standard",
                    help="discovery depth when a directory is given (default: standard)")
    ap.add_argument("--list", action="store_true", help="list what would be assessed, then exit")
    ap.add_argument("--verbose", action="store_true", help="print every finding even on large scans")
    ap.add_argument("--json", dest="json_out", help="write findings as JSON")
    args = ap.parse_args()

    items = collect(args.paths, args.depth)
    if not items:
        print(f"nothing assessable found (depth={args.depth}). "
              f"Looked for SKILL.md, agents/*.md, commands/*.md.", file=sys.stderr)
        return 2

    kind_counts = {}
    for _, k in items:
        kind_counts[k] = kind_counts.get(k, 0) + 1

    if args.list:
        for f, k in items:
            print(f"{k:8} {f}")
        print(f"\n{len(items)} assessable: "
              + ", ".join(f"{v} {k}" for k, v in sorted(kind_counts.items()))
              + f"  (depth={args.depth})")
        return 0

    all_rows, n_fail, n_warn, n_info = [], 0, 0, 0
    detailed = args.verbose or len(items) <= 15
    for fpath, kind in items:
        findings = validate_file(fpath, kind, args.target)
        if detailed and not findings:
            print(f"OK   {fpath}")
        for fd in sorted(findings, key=lambda x: {"FAIL": 0, "WARN": 1, "INFO": 2}[x.sev]):
            if detailed:
                print(fd.as_row(str(fpath)))
            all_rows.append(fd.as_dict(str(fpath), kind))
            n_fail += fd.sev == "FAIL"
            n_warn += fd.sev == "WARN"
            n_info += fd.sev == "INFO"

    if not detailed:
        print_aggregate(all_rows, kind_counts)

    print(f"\n{len(items)} file(s): {n_fail} FAIL, {n_warn} WARN, {n_info} INFO  "
          f"(target: {args.target}, depth: {args.depth})")
    if args.json_out:
        Path(args.json_out).write_text(json.dumps({
            "summary": {"files": len(items), "fail": n_fail, "warn": n_warn, "info": n_info,
                        "by_kind": kind_counts, "depth": args.depth, "target": args.target},
            "findings": all_rows,
        }, indent=2) + "\n")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
