# opencode-sync

Keep one canonical source of truth for your agent ecosystem usable on **both**
Claude Code and OpenCode. Skills and `AGENTS.md` are single-source by design
(OpenCode reads `.claude/skills/` and `AGENTS.md` natively); agents, commands and
MCP config are generated from the canonical Claude-side files by the bundled scripts.

The canonical copy lives on the open side of the fence, so if Claude Code access is
capped, everything here still runs.

## Repository layout

This marketplace plugin wraps a single skill. The skill folder is
self-contained, so it also works on its own (OpenCode, or a Cowork upload):

```
.claude-plugin/
  plugin.json            plugin manifest (lists ./skills/opencode-sync)
skills/opencode-sync/    the skill (this folder is the standalone unit)
  SKILL.md               the workflow: Setup, Sync, Validate, Drift, Ingest
  scripts/               sync_agents, validate_dual, check_drift, ingest_source
  references/            field mapping, tool translation, rule inventory, preamble
tests/                   focused regression tests for ingest behaviour
VERSION  CHANGELOG.md  README.md
```

## What is in here

- `skills/opencode-sync/SKILL.md` - the workflow, with five modes: Setup, Sync, Validate,
  Drift, Ingest. Runs on Claude Code (Task* phase chains, AskUserQuestion) and degrades
  gracefully on OpenCode / Cowork.
- `skills/opencode-sync/scripts/sync_agents.py` - generate OpenCode agent files from
  canonical Claude Code agents. Config-driven or direct. Translates tool names, maps models,
  writes a drift manifest, and reports every degradation.
- `skills/opencode-sync/scripts/validate_dual.py` - dual-runtime validator. Mechanical rules
  across four families (SH / CC / OC / TR), selectable per target. Non-zero exit on FAIL, so
  it doubles as a CI gate.
- `skills/opencode-sync/scripts/check_drift.py` - manifest-based drift detection
  (`--check` / `--update`).
- `skills/opencode-sync/scripts/ingest_source.py` - onboard a marketplace, plugin, or repo so
  OpenCode can find and run its skills, agents, and tools (Mode E).
- `skills/opencode-sync/references/` - field mapping, tool translation, the full validator
  rule inventory, skill-exposure mechanics, and the copy-paste capability-detection preamble.

## Quick start

Scripts live under `skills/opencode-sync/scripts/`. Run them from the repo root:

```bash
# 1. Validate a single skill or agent for both runtimes
python3 skills/opencode-sync/scripts/validate_dual.py --target both path/to/SKILL.md

# 1b. Point it at a whole repo or plugin - it discovers every SKILL.md,
#     agents/*.md and commands/*.md and skips docs/READMEs.
#     Depth: shallow (one plugin) | standard (repo source) | deep (incl .claude caches)
python3 skills/opencode-sync/scripts/validate_dual.py --list --depth standard ~/Projects/my-repo   # preview
python3 skills/opencode-sync/scripts/validate_dual.py --target both --depth standard ~/Projects/my-repo

# 2. Generate OpenCode agents from your canonical Claude agents
python3 skills/opencode-sync/scripts/sync_agents.py --config .opencode-sync/config.json

# 3. Check for drift (CI-friendly, exits 1 on drift)
python3 skills/opencode-sync/scripts/check_drift.py --check
```

`.opencode-sync/config.json` example:

```json
{
  "canonical_agent_dirs": [".claude/agents", "plugins/work/agents"],
  "opencode_agent_dir": ".opencode/agent",
  "default_agent_mode": "subagent",
  "model_map": {
    "sonnet": "anthropic/claude-sonnet-4-5",
    "opus": "anthropic/claude-opus-4-1",
    "haiku": "anthropic/claude-haiku-4-5"
  },
  "mcp_servers": [],
  "claude_plugin_roots": ["plugins"],
  "skip_paths": []
}
```

## Validator rule families

| Family | Prefix | Applies to | Automated rules |
|---|---|---|---|
| Shared | SH | both runtimes | 6 |
| Claude Code | CC | Claude packaging | 4 |
| OpenCode | OC | OpenCode schema | 5 |
| Translation / drift | TR | portability | 4 |

Claude side runs SH + CC (10), OpenCode side runs SH + OC + TR (15), sharing the 6 SH
rules. Full inventory with severities in `references/validator-rules.md`.

## Install

**As a Claude Code plugin (recommended).** In this marketplace, install it with:

```bash
claude plugin marketplace add YoungLeadersDotTech/young-leaders-tech-marketplace
claude plugin install opencode-sync@young-leaders-tech-marketplace
```

**As a standalone skill folder.** `skills/opencode-sync/` is self-contained, so you can also
use it without the plugin wrapper:

- **Claude Code / OpenCode**: drop `skills/opencode-sync/` into `.claude/skills/` (or
  `~/.claude/skills/`), or point OpenCode `skills.paths` at it. Both runtimes discover it
  natively.
- **Cowork**: zip the folder (root must be `opencode-sync/` with `SKILL.md` inside) and upload
  it under Customize -> Skills.

No PyYAML required - the scripts are stdlib Python 3 with a graceful fallback parser.

## Source Strategy

When deciding what path to ingest, use this precedence:

1. **Local development clone under `~/Projects/`** - use this when you are actively editing the plugin or marketplace. OpenCode should mirror the working tree you are changing, not a cached install snapshot.
2. **Claude plugin cache under `~/.claude/plugins/cache/...`** - use this when you want exact parity with what Claude Code currently has installed. This is especially important for version-pinned installs and MCP-only plugins that do not have a normal marketplace checkout.
3. **Fresh clone** - use this when you do not already have the source locally. Prefer a normal repo checkout (`~/Projects` or `~/.opencode-sources`) over editing the cache directly.

Practical rule:

- **Installed plugin parity** -> ingest from the Claude cache snapshot.
- **Local development** -> ingest from the repo clone.

The cache is the right source of truth for "what Claude has installed right now". A repo clone is the right source of truth for "what I am developing locally".

## Visibility Rules

There are two separate visibility surfaces in OpenCode:

- **Skills** come from `skills.paths` in `opencode.json`.
- **Agents** come from generated files under an OpenCode agent discovery directory.

`opencode-sync` defaults the generated agent output directory based on the config target:

- `--config-target global` -> `~/.config/opencode/agent`
- `--config-target project` -> `.opencode/agent`
- explicit `--opencode-agent-dir` overrides both

If your skills are visible but your agents are not, the first thing to check is **where the sync wrote the generated agent files**.

## Memory Wiring

`--wire-memory` is the OpenCode-side replacement for the read half of memory-os.

- If the source repo tracks `MEMORY.md` at its root, opencode-sync now wires that first.
- It then wires `AGENTS.md`.
- It finally wires the global memory index at `~/.claude/memory/memory.md`.

That gets OpenCode closer to memory-os's project-memory-first behaviour, but it does not fully
replace the Claude hooks. The exact gap is documented in `references/memory-wiring.md`.

## Prompt Box Autocomplete

Skills and commands are different in OpenCode:

- Skills appear under `/skills` and can be invoked by name there.
- Skills do **not** currently get the same prompt-box autocomplete behaviour as commands.

If prompt-box autocomplete matters, the current workaround is to expose that workflow as a **command** instead of only a skill. There is upstream OpenCode work in flight, but it is not something a plugin can fully patch around today.

That means command wrappers are a valid future extension for `opencode-sync`, but they are not emitted by default today.

## Requirements

Python 3.8+. No third-party dependencies.
