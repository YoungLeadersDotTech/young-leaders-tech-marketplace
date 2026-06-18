# opencode-sync

Keep one canonical agent ecosystem usable on **both** Claude Code and OpenCode. Skills and
`AGENTS.md` are single-source by design (OpenCode reads `.claude/skills/` and `AGENTS.md`
natively); agents, commands, and MCP config are generated from the canonical Claude-side files
by the bundled scripts. The canonical copy lives on the open side of the fence, so if Claude
Code access is capped, everything here still runs.

## Skill

- **opencode-sync** - five modes: Setup, Sync, Validate, Drift, and Ingest. Generates OpenCode
  agents from canonical Claude agents, runs a dual-runtime validator (SH / CC / OC / TR rule
  families), detects drift against a manifest, and ingests a marketplace, plugin, or repo so
  OpenCode can find and run its skills. Runs on Claude Code (Task* phase chains, AskUserQuestion)
  and degrades gracefully on OpenCode / Cowork.

The skill is self-contained: its `scripts/` and `references/` live inside
`skills/opencode-sync/`, with no dependency on other plugins. Stdlib Python 3 only, no PyYAML
required.

## Install

Published in the young-leaders-tech-marketplace. Add that marketplace and install the
`opencode-sync` plugin:

```bash
claude plugin marketplace add YoungLeadersDotTech/young-leaders-tech-marketplace
claude plugin install opencode-sync@young-leaders-tech-marketplace
```

You can also use the skill folder on its own: drop `skills/opencode-sync/` into `.claude/skills/`,
point OpenCode `skills.paths` at it (this marketplace's root `opencode.json` already does), or zip
it for a Cowork upload.

## Quick start

Scripts live under `skills/opencode-sync/scripts/`:

```bash
# Validate a skill or agent for both runtimes
python3 skills/opencode-sync/scripts/validate_dual.py --target both path/to/SKILL.md

# Generate OpenCode agents from your canonical Claude agents
python3 skills/opencode-sync/scripts/sync_agents.py --config .opencode-sync/config.json

# Check for drift (CI-friendly, exits non-zero on drift)
python3 skills/opencode-sync/scripts/check_drift.py --check
```

See `skills/opencode-sync/SKILL.md` for the full workflow and `skills/opencode-sync/references/`
for the field-mapping, tool-translation, and validator-rule inventories.
