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

`opencode-sync` now defaults the generated agent output directory based on the config target:

- `--config-target global` -> `~/.config/opencode/agent`
- `--config-target project` -> `.opencode/agent`
- explicit `--opencode-agent-dir` overrides both

If your skills are visible but your agents are not, the first thing to check is **where the sync wrote the generated agent files**.

## Prompt Box Autocomplete

Skills and commands are different in OpenCode:

- Skills appear under `/skills` and can be invoked by name there.
- Skills do **not** currently get the same prompt-box autocomplete behaviour as commands.

From the Toast Slack discussion on 2026-06-19: if prompt-box autocomplete matters, the current workaround is to expose that workflow as a **command** instead of only a skill. There is upstream OpenCode work in flight, but it is not something a plugin can fully patch around today.

That means command wrappers are a valid future extension for `opencode-sync`, but they are not emitted by default today.

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
