---
name: opencode-sync
description: Generates OpenCode agents, commands, and MCP config from canonical Claude Code sources, validates both runtimes' rule sets, and detects drift. Use when adding OpenCode support, converting agents between runtimes, or checking cross-runtime compliance.
version: 1.6.0
user-invocable: true
category: Cross-Runtime Tooling
tags:
  - opencode
  - cross-runtime
  - sync
  - validation
  - drift-detection
last-updated: 2026-06-18
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - Skill
  - TaskCreate
  - TaskUpdate
  - TaskGet
  - TaskList
---

# opencode-sync

Keeps one canonical source of truth (skills, agents, commands, MCP config, rules files) usable on BOTH Claude Code and OpenCode. Skills and rules are single-source by design (OpenCode reads `.claude/skills/` and `AGENTS.md` natively); agents, commands, and MCP config are generated from the canonical Claude-side files by the bundled scripts. Plugin skills are exposed to OpenCode via `skills.paths` (see Mode E). The canonical copy always lives on the open side of the fence - if Claude Code access is capped, everything here still runs.

## MANDATORY FIRST ACTION - Task Chain Bootstrap

> On Claude Code, run these TaskCreate calls before anything else:

```python
t0 = TaskCreate("Phase 0: Pre-Flight checks")
t1 = TaskCreate("Phase 1: Mode selection (Ingest / Sync / Validate / Drift / Setup)")
t2 = TaskCreate("Phase 2: Execute selected mode")
t3 = TaskCreate("Phase 3: Report, ledger, commit")

TaskUpdate(t1, addBlockedBy=[t0])
TaskUpdate(t2, addBlockedBy=[t1])
TaskUpdate(t3, addBlockedBy=[t2])
```

Mark t0 `in_progress` immediately, mark each phase `completed` at its boundary.

> **OpenCode or Cowork runtime**: `TaskCreate` does not exist there. Mirror the same four phases as a `todowrite` checklist (OpenCode) or a visible markdown checklist (Cowork) instead. Full translation recipe: `references/tool-translation.md`. Do not skip phase tracking just because Task* is unavailable.

## When to Use

- Onboarding a marketplace, plugin, or repo so OpenCode can find and run its skills/agents/tools (Mode E)
- Adding OpenCode support to a repo or plugin that currently targets Claude Code only
- Converting Claude Code subagents into OpenCode agent files (frontmatter translation)
- Checking whether skills are portable across both runtimes before shipping
- Running a drift check after editing canonical sources, or wiring that check into CI

## Skip when

- Creating a brand new skill or agent from scratch - use the **skills-toolkit** creation workflows, then run this skill's Validate mode on the result
- Syncing the local skill registry or marketplace versions - use **aios-sync-skills** and the 4/5-file version rule directly
- Validating a single Claude-only skill with no OpenCode target - use **skill-validation-workflow**
- Pushing pages or tickets to external systems - this skill only touches local runtime config and artifact files

## Runtime Compatibility

This skill is itself dual-runtime. Detect capabilities before acting, never assume:

```text
CAPABILITY CHECK (run mentally at start):
- Task* tools available?        yes -> use the bootstrap chain above
                                no  -> todowrite / markdown checklist
- AskUserQuestion available?    yes -> use it (4 options max)
                                no  -> ask in plain text with lettered options
- Bash available?               yes -> run bundled scripts
                                no  -> follow the manual tables in references/
```

The bundled scripts are plain Python 3 stdlib (PyYAML optional, with graceful fallback) so they run identically from either runtime's bash tool.

## Preference Storage

Stored at `<repo>/.opencode-sync/config.json` (recommend committing it so CI can use it):

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

The model map MUST be verified against the live models.dev registry on first run - model ids change and this skill never hardcodes a guess silently (see E5).

## Phase 1: Mode Selection

There are five modes: Ingest, Sync, Validate, Drift, and Setup. Skip this phase when a Happy Path trigger already names one (for example "ingest this marketplace", "is this repo opencode-ready", "check drift"). Otherwise ask (AskUserQuestion, these 4 options; plain-text lettered fallback on OpenCode):

- **(A) Ingest** - onboard a marketplace, plugin, or repo (local path or URL): discover its skills/agents/commands/MCP and emit the OpenCode config that makes them work
- **(B) Sync** - generate OpenCode artifacts from canonical sources and update the manifest
- **(C) Validate** - run the dual-runtime rule set against skills and agents
- **(D) Drift status** - compare manifest hashes, report stale or hand-edited generated files

Mode A (Setup - AGENTS.md canonicalisation, provider notes) runs as the first-run step of ingesting your own repo, or name "setup" to run it on its own.

## Mode A: Setup

1. **Rules file canonicalisation**: `CLAUDE.md` exists, `AGENTS.md` does not -> `mv CLAUDE.md AGENTS.md && ln -s AGENTS.md CLAUDE.md`, commit the symlink. Both exist and differ -> STOP (E2), show a diff, user merges into AGENTS.md. Symlink already in place -> report OK.
2. **Global rules awareness**: OpenCode also reads `~/.claude/CLAUDE.md` as a global fallback (unless `~/.config/opencode/AGENTS.md` exists, which takes precedence). Symlink the global if you want it canonical.
3. **Skill discovery**: plugin skills are NOT in OpenCode's native paths - expose them via Mode E (`skills.paths`). Global `~/.claude/skills/` skills are discovered natively.
4. **Provider check**: subscription OAuth is Claude-Code-only (April 2026). OpenCode needs `opencode auth login` with an API key, Copilot, OpenCode Zen, or a local model. Do not auth on the user's behalf.

## Mode B: Sync

All writes preview-first. Work on a branch, never commit to main, open a PR.

1. **Skills**: single-source; run `validate_dual.py --target opencode <paths>` and fix-forward portability warnings in the canonical file.
2. **Agents**: `sync_agents.py --config .opencode-sync/config.json` emits translated files with a GENERATED header. Per-file failures (E3, E4, E5) skip and continue.
3. **Commands** (optional): most ecosystems are skills-only; OpenCode exposes each skill as `/name`.
4. **MCP config**: emit the `opencode.json` `mcp` block, diff-first (MCP runs code).
5. **Manifest**: `check_drift.py --update`.
6. **Claude plugin housekeeping**: apply the 4/5-file version rule before the PR.

## Mode C: Validate

Point the assessor at a file, plugin, repo, or `.claude` tree. It discovers SKILL.md, `agents/*.md`, `commands/*.md` by location and skips docs/READMEs.

1. **Ask how deep** (AskUserQuestion -> `--depth`): (A) this folder `shallow`, (B) whole repo source `standard` (recommended), (C) everything incl caches `deep`, (D) a single file. Preview with `--list`.
2. `python3 scripts/validate_dual.py --target both --depth <d> <paths>` - FAIL/WARN/INFO with rule IDs. Scans over 15 files print an aggregate; `--verbose` for per-finding, `--json` for machine output.
3. Apply the manual-judgement rules and report alongside.
4. Summarise rule ID, severity, line, one-line fix. Note when a scan crosses into a submodule or work-owned tree.

## Mode D: Drift Status

`python3 scripts/check_drift.py --check` compares hashes against the manifest: CANONICAL_CHANGED (re-sync), GENERATED_EDITED (canonical wins; regenerate or back-port, E8), MISSING (regenerate). CI wiring runs the same `--check`.

## Mode E: Ingest a source

Onboard any Claude Code marketplace, plugin, or plain repo so OpenCode can find and run its skills, agents, and tools. One entry point, three source types, auto-detected. Driven by `scripts/ingest_source.py`; full exposure mechanics in `references/skill-exposure.md`.

1. **Resolve the source** (`python3 scripts/ingest_source.py <path-or-url>`). Local path is used directly. For a URL the script searches `--search-roots` (default `~/Projects`) for an existing clone:
   - **Found**: reports currency (uncommitted, ahead/behind; add `--fetch`). Confirm it is current before using.
   - **Not found** (exit 3, `URL_NOT_FOUND_LOCALLY`): ask the user (AskUserQuestion): **(A) I already have it** -> `--local-path <dir>`; **(B) Clone it** -> a second question confirms where (`~/.opencode-sources` recommended, `~/Projects`, or typed) -> `--clone-into <dir>`.
2. **Choose the enablement strategy** (AskUserQuestion; plain-text lettered fallback on OpenCode). This is the headline choice - it decides which plugins/skills/MCP get exposed:
   - **(A) Respect Claude settings (recommended)** - mirror what Claude Code has enabled on this machine: pass `--respect-claude-settings`. Exposes only the enabled plugins, denies the disabled ones, and emits user-scope MCP to the GLOBAL config. The turnkey path - OpenCode inherits exactly the machine's Claude enablement, so nothing that is on is silently missing and nothing that is off leaks in.
   - **(B) Per-repo routing** - place things yourself. A follow-up AskUserQuestion offers **All global** (`~/.config/opencode/opencode.json`, everywhere), **All project** (`opencode.json` in the checkout, portable relative paths), **Both**, or **Per-plugin**. Pass `--config-target global|project|both`; for per-plugin, list the discovered plugins with a default target and let the user name exceptions as `--global-plugins NAME...` / `--project-plugins NAME...`. Routing is per plugin, so one ingest can populate both config files.
   - **(C) Enable-all override** - expose every skill and skip the reference-only deny-list: pass `--no-deny`. Use when the user wants everything on to prune later.

   These compose: `--respect-claude-settings` decides *what* is exposed, `--config-target` decides *where* the enabled plugins land (default project; user-scope MCP always goes global), and `--no-deny` is the escape hatch when mirroring is too strict. Add `--wire-memory` with any strategy to wire OpenCode's session-start memory read (`instructions: ["AGENTS.md", "~/.claude/memory/memory.md"]`), replacing the Claude SessionStart hook.
3. **Preview** (dry-run, the default): the script prints the detected type, discovered counts, the deny-list, and the exact config fragment(s) to merge per target. Confirm before writing.
4. **Apply** (`--apply`): merges `skills.paths` + `permission.skill` deny-list + `mcp` blocks into each target config, then delegates agent generation to `sync_agents.py`. A non-writable target (for example a global config the runtime cannot reach) degrades gracefully - the fragment is printed for manual application. The hide set is skills that are BOTH `disable-model-invocation: true` AND `user-invocable: false`.
5. **Offer the resolution block.** The preview reports the source's rules-file state. If the source has no `AGENTS.md`/`CLAUDE.md`, or one missing the block, ask the user: add the `${CLAUDE_PLUGIN_ROOT}` / `plugin:skill` resolution block? On yes, pass `--add-resolution-block` - it appends to `AGENTS.md` (or to `CLAUDE.md` so it is not shadowed), or creates `AGENTS.md` if neither exists.
6. **Verify**: open OpenCode and run `/skills` - the invocable skills appear, the denied reference-only ones do not. Generated agents land in `.opencode/agent/`.

Skills are never copied or symlinked - `skills.paths` points OpenCode at the canonical folders (symlinks are unreliable: OpenCode's glob defaults to not following them). Single-source preserved.

## Error Handling

| ID | Error | Resolution |
|----|-------|-----------|
| E1 | Config file missing | Switch to Consultation wizard, create `.opencode-sync/config.json` on approval |
| E2 | AGENTS.md and CLAUDE.md both exist and differ | Show diff, user merges into AGENTS.md, re-run. Never auto-merge |
| E3 | PyYAML unavailable, block-scalar frontmatter | Script skips the file with a message and continues |
| E4 | Agent has no `description` | FAIL that file, list it, continue with the rest |
| E5 | Model not in model_map | Emit `anthropic/<original>` + `TODO-VERIFY` - never silently guess |
| E6 | `opencode` binary not found | Author-only mode: generate and validate, mark UNTESTED ON OPENCODE |
| E7 | Manifest missing on drift check | Build a fresh manifest, exit 0, note first-run |
| E8 | Generated file hand-edited | Canonical wins. Regenerate, or back-port the edit then regenerate |
| E9 | Ingest URL has no local clone | Exit 3 `URL_NOT_FOUND_LOCALLY`. Ask: `--local-path` or `--clone-into`. Never clone without confirmation |
| E10 | Marketplace entry points at an external (non `./`) source | Skipped with a note. Ingest that plugin/repo separately |

## Related References

- `references/field-mapping.md` - frontmatter, model, command, MCP, and rules-file mapping tables
- `references/tool-translation.md` - tool-name map, degradation recipes, capability preamble
- `references/validator-rules.md` - the dual-runtime rule inventory (SH / CC / OC / TR)
- `references/skill-exposure.md` - how plugin skills reach OpenCode (skills.paths, permission.skill, AGENTS.md resolution)
- `scripts/ingest_source.py` - Mode E: resolve a source, discover, emit OpenCode config
- `scripts/sync_agents.py`, `scripts/validate_dual.py`, `scripts/check_drift.py` - the executable side of Modes B, C, D
