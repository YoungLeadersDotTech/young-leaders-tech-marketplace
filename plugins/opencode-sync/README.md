# opencode-sync

**Version**: 1.6.5
**Author**: Young Leaders Tech
**License**: MIT

## Overview

`opencode-sync` keeps one canonical agent ecosystem usable across Claude Code and OpenCode.
Skills and rules stay single-source where possible, while agents, MCP config, and discovery wiring
 are translated or exposed in the places OpenCode actually reads.

The plugin is built around a single skill, `opencode-sync`, which covers setup, sync, validation,
 drift detection, and marketplace or repo ingest.

## What is included

- **1 skill** - `skills/opencode-sync/SKILL.md`
- **5 scripts** - `sync_agents.py`, `sync_commands.py`, `validate_dual.py`, `check_drift.py`, `ingest_source.py`
- **Reference docs** - field mapping, tool translation, validator rules, memory wiring,
  skill exposure, and capability guidance
- **Regression tests** - focused ingest tests under `plugins/opencode-sync/tests/`

## Install

Add the marketplace once:

```text
/plugin marketplace add git@github.com:YoungLeadersDotTech/young-leaders-tech-marketplace.git
```

Install this plugin:

```text
/plugin install opencode-sync@young-leaders-tech-marketplace
```

Activate it in the current session:

```text
/reload-plugins
```

## Quick start

Run the scripts from the marketplace repo root:

```bash
# Validate one skill or agent for both runtimes
python3 plugins/opencode-sync/skills/opencode-sync/scripts/validate_dual.py --target both path/to/SKILL.md

# Preview discovery across a repo or plugin tree
python3 plugins/opencode-sync/skills/opencode-sync/scripts/validate_dual.py --list --depth standard ~/Projects/my-repo

# Run full validation
python3 plugins/opencode-sync/skills/opencode-sync/scripts/validate_dual.py --target both --depth standard ~/Projects/my-repo

# Generate OpenCode agents from canonical Claude agents
python3 plugins/opencode-sync/skills/opencode-sync/scripts/sync_agents.py --config .opencode-sync/config.json

# Generate OpenCode command wrappers from canonical Claude commands
python3 plugins/opencode-sync/skills/opencode-sync/scripts/sync_commands.py plugins/skills-toolkit/commands

# Check drift
python3 plugins/opencode-sync/skills/opencode-sync/scripts/check_drift.py --check
```

If you use the skill standalone outside the plugin wrapper, the same scripts live under
`skills/opencode-sync/scripts/` relative to that standalone skill folder.

## Ingest behaviour

`ingest_source.py` is the main runtime bridge for marketplaces, plugins, and repos.

It now does five important things:

1. keeps non-disabled sibling plugins available when `--respect-claude-settings` is used
2. exposes plugin skills through `skills.paths`
3. generates OpenCode agents into the correct discovery directory
4. generates OpenCode command wrappers from canonical `commands/*.md` files
5. prints a verification summary that checks expected versus discovered coverage

## Command wrappers

`opencode-sync` now generates an OpenCode-first command layer from canonical `commands/*.md` files.

These generated command wrappers:

- preserve the command body template, including `$ARGUMENTS`, `$1`, `$2`, and similar placeholders
- drop Claude-only frontmatter such as `argument-hint`
- write to `~/.config/opencode/command` for global sync targets
- write to `.opencode/command` for project-local sync targets
- share the same drift manifest model as generated agents

This gives OpenCode a first-class command surface for explicit `/name` workflows without forcing the
canonical source to become OpenCode-only.

## Verification coverage

The ingest preview uses the same location rules as the `catalogue-tools` scanner to compare what a
 repo appears to contain versus what ingest actually discovered:

- `skills/*/SKILL.md`
- `agents/*.md`
- `commands/*.md`
- `hooks/*`

Skills, agents, and commands are expected to match after filtering. Hooks are reported, but remain
 verification-only because this plugin does not materialise a hook surface into OpenCode config.

## MCP routing

`opencode-sync` now separates Claude MCP sources by scope:

- user-scope `~/.claude/settings.json` `mcpServers` -> global OpenCode config
- repo `.claude/settings.json` `mcpServers` -> project `opencode.json`
- repo `.claude/settings.local.json` `mcpServers` -> project `opencode.json`
- plugin `.mcp.json` files -> whichever config target the ingest run is writing

That keeps machine-wide auth and personal tools global, while preserving repo-specific MCP wiring
 in the checkout that actually depends on it.

## Visibility rules

OpenCode has three separate discovery surfaces:

- **Skills** come from `skills.paths` in `opencode.json`
- **Agents** come from generated files under an OpenCode agent directory
- **Commands** come from generated files under an OpenCode command directory

Default agent output:

- `--config-target global` -> `~/.config/opencode/agent`
- `--config-target project` -> `.opencode/agent`
- `--opencode-agent-dir` overrides both

Default command output:

- `--config-target global` -> `~/.config/opencode/command`
- `--config-target project` -> `.opencode/command`
- `--opencode-command-dir` overrides both

If skills are visible but agents or commands are missing, check where the sync wrote the generated
agent and command files first.

## Memory wiring

`--wire-memory` is the OpenCode-side replacement for the read half of memory-os.

Read order:

1. repo-root `MEMORY.md` when present
2. `AGENTS.md`
3. `~/.claude/memory/memory.md`

This gets OpenCode closer to the project-memory-first behaviour of memory-os, but it does not
 recreate Claude's hooks in full. The exact boundary is documented in
 `references/memory-wiring.md`.

## Prompt box autocomplete

OpenCode treats skills and commands differently:

- skills appear under `/skills`
- skills do not automatically get the same prompt-box autocomplete behaviour as commands

That is why `opencode-sync` now ships a command-wrapper layer for canonical `commands/*.md` files,
while still keeping skills single-source.

## Requirements

Python 3.8+ with no required third-party dependencies.

## Maintainer

Young Leaders Tech &middot; <https://youngleaders.tech>

## License

MIT
