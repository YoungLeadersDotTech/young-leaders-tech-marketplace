# Changelog

All notable changes to the opencode-sync skill.

## [1.6.1] - 2026-06-19

### Fixed
- Synced the post-1.6.0 ingest fixes from the standalone `opencode-sync` repo:
  marketplace ingests now respect the enabled plugin allow-list, prune stale `skills.paths`
  entries on re-run, keep discovered agents and MCP scoped to the enabled plugin roots, and
  read both `{"mcpServers": {...}}` and direct plugin-cache `.mcp.json` shapes.
- Generated agents now default to `~/.config/opencode/agent` whenever any global config target
  is involved, matching the documented global-visibility behaviour.

### Changed
- Synced the canonical `SKILL.md`, ingest implementation, and regression coverage from the
  standalone Claude-side repo. Kept the marketplace `README.md` public-safe instead of copying
  over product-specific narrative verbatim.
- Added `tests/test_ingest_source.py` to lock the ingest behaviour that drifted after the
  marketplace migration.

## [1.6.0] - 2026-06-18

### Changed
- Repo restructured into a proper Claude Code plugin. The skill content (`SKILL.md`,
  `scripts/`, `references/`) moved down a level into `skills/opencode-sync/`, and the repo
  root now carries `.claude-plugin/plugin.json` (lists `./skills/opencode-sync`) plus
  `.claude-plugin/marketplace.json`, so the repo installs directly with
  `claude plugin marketplace add YoungLeadersDotTech/opencode-sync`.
- `skills/opencode-sync/` is self-contained, so it still works as a standalone skill: drop it
  into `.claude/skills/`, point OpenCode `skills.paths` at it, or zip it for a Cowork upload.
- CI (`.github/workflows/ci.yml`) updated to the new `skills/opencode-sync/scripts/` and
  `skills/opencode-sync/SKILL.md` paths; the drift manifest stays at repo root.
- Added a root `VERSION` file (1.6.0) and the local build directory to `.gitignore`.

### Notes
- No skill logic changed. This is a packaging change (plugin wrapper added), so the skill body,
  scripts, and validator rules are byte-identical aside from the version bump.

## [1.5.0] - 2026-06-16

### Added
- `references/capability-preamble.md` strengthened (WS3a): on OpenCode every phase AND every task
  becomes its own `todowrite` item (visible in the TUI sidebar), mirroring the Claude task list
  one-to-one. Added an explicit "Degrade, never abort" rule - the absence of `TaskCreate` is not a
  stop condition; a skill that halts or "surfaces and stops" when Task* is unavailable is broken on
  OpenCode.
- `scripts/validate_dual.py` OC-06 rule (WS3c): flags a skill that stops/aborts when Task* is
  unavailable (instead of degrading to a todowrite checklist) as OpenCode-hostile, with a
  forward-order match so a skill that merely embeds the capability preamble is not false-flagged.
  Rule inventory updated (OC family 5 -> 6, automated total 19 -> 20, OpenCode-facing 15 -> 16).
- `docs/work-pc-runbook.md` (WS6): a plain-markdown, Chat-drivable work-PC install guide - clone
  root-opencode into `~/.config/opencode`, `opencode auth login`, then `ingest_source.py` per repo
  with `--respect-claude-settings --wire-memory --apply`.

## [1.4.0] - 2026-06-15

### Added
- `ingest_source.py --respect-claude-settings` (WS1): mirrors Claude's enablement - reads
  `~/.claude/settings.json` plus the repo's `.claude/settings.json` / `.local.json`, exposes only
  enabled plugins, denies the disabled ones, and emits user-scope MCP servers. OpenCode inherits
  exactly what Claude Code has enabled on the machine instead of an enable-everything default.
- `ingest_source.py --wire-memory` (WS2): adds an `instructions` array
  (`["AGENTS.md", "~/.claude/memory/memory.md"]`) so OpenCode auto-loads memory at session start,
  replacing the Claude Code SessionStart hook OpenCode cannot run. `merge_opencode` now unions
  `instructions` across runs.
- Mode E enablement question reworked: the config-target step now leads with **Respect Claude
  settings (recommended)** (`--respect-claude-settings`), with **Per-repo** (global / project /
  both / per-plugin) and **Enable-all override** (`--no-deny`) as the alternatives, and surfaces
  `--wire-memory`.

### Changed
- User-scope MCP routing tightened: MCP servers from `~/.claude/settings.json` are a per-user
  concern and now route to the GLOBAL `opencode.json` only, never duplicated into each project's
  config (a project-scoped run emits a global fragment for them). Matches the WS1 scope table
  (user -> global, project -> project).

## [1.3.0] - 2026-06-14

### Added
- Per-plugin config routing in `ingest_source.py`: `--global-plugins` / `--project-plugins`
  route individual plugins to the global or project config, and `--config-target both`
  sends every plugin to both. One ingest can now populate both config files.
- `--no-deny` enables every skill (skips the reference-only deny-list) for an enable-all,
  prune-later workflow.
- Global writes degrade gracefully: if the global config path is not writable, the fragment
  is printed for manual application instead of failing.
- Mode E config-target question expanded to All global / All project / Both / Per-plugin.

## [1.2.1] - 2026-06-14

### Added
- Mode E now offers to add the AGENTS.md resolution block when the source has none.
  `ingest_source.py --add-resolution-block` appends to AGENTS.md (or CLAUDE.md so it is
  not shadowed), or creates AGENTS.md if neither exists; the preview reports rules-file state.

## [1.2.0] - 2026-06-13

### Added
- Mode E (Ingest): onboard a marketplace, plugin, or repo (local path or git URL) and
  emit the OpenCode config that exposes its skills/agents/commands/MCP.
- `scripts/ingest_source.py` - resolves the source (reuse-local-clone-if-current, or
  clone on confirmation), auto-detects marketplace / plugin / repo, discovers and
  classifies, and emits `skills.paths` + `permission.skill` deny-list + `mcp` blocks
  (preview-first, `--apply` writes and delegates agents to sync_agents.py).
- `references/skill-exposure.md` - how plugin skills reach OpenCode via `skills.paths`
  and `permission.skill`, why symlinks are unreliable, and the AGENTS.md resolution block.

### Changed
- Corrected field-mapping: plugin skills need EXPOSURE (skills.paths), not just
  single-source discovery - they live outside OpenCode's native skill paths.
- Hide rule refined: a skill is hidden only when `disable-model-invocation: true` AND
  `user-invocable: false`; anything a user can still invoke stays exposed.

## [1.1.1] - 2026-06-13

### Changed
- CC-03 recalibrated to match the marketplace skill-validator ground truth: `TodoWrite` in
  allowed-tools is FAIL (use Task* variants), generic `Task` is now WARN not FAIL
  (Task / Agent is a valid subagent-dispatch tool). Added `Agent` to known tools.

## [1.1.0] - 2026-06-13

### Added
- `validate_dual.py` discovery layer: point it at a file, plugin, repo or `.claude`
  tree and it finds every assessable tool by location (SKILL.md, `agents/*.md`,
  `commands/*.md`), skipping docs and READMEs. Mirrors the catalogue-tools convention.
- `--depth` flag (shallow / standard / deep) controlling how far discovery walks
  and whether hidden dirs and `.claude` caches are included.
- `--list` preview mode, `--verbose` per-finding output, and an automatic aggregate
  report (counts by rule, FAIL file list, tally by kind) for scans over 15 files.
- Command files are now assessed as a distinct kind.
- SKILL.md Mode C now opens with a "how deep to scan" AskUserQuestion mapped to `--depth`.

## [1.0.0] - 2026-06-13

### Added
- Initial release. Keeps one canonical source of truth usable on both Claude Code
  and OpenCode.
- `SKILL.md` with four modes: Setup, Sync, Validate, Drift status, plus dual-runtime
  capability detection and a consultation / happy-path split.
- `scripts/sync_agents.py` - generates OpenCode agent files from canonical Claude Code
  agents (config-driven or direct), with tool-name translation, model mapping, drift
  manifest output, and graceful degradation warnings.
- `scripts/validate_dual.py` - dual-runtime validator implementing 19 mechanical rules
  across four families (SH / CC / OC / TR), selectable per target, non-zero exit on FAIL.
- `scripts/check_drift.py` - manifest-based drift detection (--check / --update) for CI.
- `references/field-mapping.md` - frontmatter, model, command, MCP and rules-file maps.
- `references/tool-translation.md` - tool inventory, mapping, degradation recipes,
  portable-authoring rules.
- `references/validator-rules.md` - the full rule inventory with counts and severities.
- `references/capability-preamble.md` - copy-paste runtime-compatibility block.
- `.github/workflows/ci.yml` - runs validate_dual.py (and check_drift.py when a
  manifest exists) on every push and pull request.
