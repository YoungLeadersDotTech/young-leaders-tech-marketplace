---
solution-id: opencode-sync-marketplace-continuation
opportunity: null
title: opencode-sync continuation after standalone-to-marketplace migration
phase: Phase 2 (Continue)
status: in_progress
status-emoji: 🔵
created: 2026-06-19
updated: 2026-06-25
project-type: plugin maintenance + cross-repo continuation
authored_on: opencode
source-thread: null
---

# 🔵 Solution Plan: opencode-sync-marketplace-continuation

## Context

This plan replaces the older private handoff at
`/Users/john.conneely/Projects/ai-os-personal/docs/CONTINUE-HERE.md` as the active continuation
point for `opencode-sync` work.

The private handoff correctly captured WS1 through WS6 on 2026-06-15, but it is now stale in two
ways:

1. The standalone repo at `/Users/john.conneely/Projects/opencode-sync` has since merged more work
   than the handoff records.
2. `opencode-sync` now also exists as a marketplace plugin at
   `/Users/john.conneely/Projects/young-leaders-tech-marketplace/plugins/opencode-sync`, which is
   where future marketplace-facing continuation should happen.

## Canonical sources

- **Historical narrative / private context**:
  `/Users/john.conneely/Projects/ai-os-personal/docs/CONTINUE-HERE.md`
- **Original workstream plan**:
  `/Users/john.conneely/Projects/ai-os-personal/docs/opencode-parity-plan.md`
- **Standalone public repo**:
  `/Users/john.conneely/Projects/opencode-sync`
- **Marketplace continuation point**:
  `/Users/john.conneely/Projects/young-leaders-tech-marketplace/plugins/opencode-sync`

## Reconciliation summary

Treat the following as already done. Do not re-do them unless a regression is found:

- [x] WS1 `--respect-claude-settings` shipped in standalone PR #4 (`2668ac9`).
- [x] WS2 `--wire-memory` shipped in standalone PR #4 (`2668ac9`).
- [x] Mode E enablement prompt update shipped in standalone PR #4.
- [x] WS3 OpenCode `todowrite` degradation hardening shipped in standalone PR #5 (`496a509`).
- [x] WS6 work-PC runbook shipped in standalone PR #5 (`496a509`).
- [x] Plugin packaging migration shipped in standalone PR #8 (`be37e36`) and marketplace PR #23
  (`33e77d4`).
- [x] Post-packaging drift fixes shipped in standalone PRs #9 and #11, then ported into the
  marketplace plugin on 2026-06-19:
  stale path pruning, marketplace enablement scoping, plugin-cache `.mcp.json` support, global
  agent output default, doc refresh, and ingest regression tests.

## What remains

### Phase 3: WS4 memory-os OpenCode support  [status: pending]

- [ ] T-P3-01: Decide whether WS4 stops at `--wire-memory` as the operational answer or continues
  into a true OpenCode-native memory plugin.
- [x] T-P3-02: Read the memory-os hooks and template in
  `/Users/john.conneely/Projects/ai-os-jc-toast/plugins/toast-memory-os/` and document the exact
  behaviour still missing on OpenCode. Captured in
  `plugins/opencode-sync/skills/opencode-sync/references/memory-wiring.md` and shipped in
  `feat: improve opencode memory wiring`.
- [ ] T-P3-03: If a plugin is still needed, implement it in the canonical memory-os location,
  not inside `opencode-sync`.

### Phase 4: WS5 downstream AIOS / skill fixes  [status: pending]

- [ ] T-P4-01: Update AIOS and related skill prompts to reference MCP by intent instead of
  hardcoded tool names.
- [ ] T-P4-02: Replace Task* "surface and stop" fallbacks with `todowrite` degradation where still
  needed.
- [ ] T-P4-03: Sanitize path-heavy metadata and validate transcript aliases where the old handoff
  flagged those issues.

### Phase 5: Optional future opencode-sync extensions  [status: pending]

- [ ] T-P5-01: Consider command-wrapper generation only if prompt-box autocomplete becomes a real
  user need. This was documented on 2026-06-19 but is not committed scope.
- [x] T-P5-02: Reuse catalogue-style enumeration as a verification pass for `opencode-sync` so
  scans can compare expected versus discovered skills, agents, commands, and hooks.
- [x] T-P5-03: Add a diff check that verifies `ingest_source.py` retains all enabled skills and
  agents after enablement filtering, and reports any mismatch between verification output and
  ingest output.
- [x] T-P5-04: Extend MCP verification to include project and local Claude `mcpServers` sources,
  not just `.mcp.json` files and user-scope home settings.
- [x] T-P5-05: Decide whether hooks should remain verification-only or gain an explicit
  OpenCode-side representation, and document the runtime boundary either way.
- [x] T-P5-06: Route project and local Claude `mcpServers` into the appropriate OpenCode config
  target when present, so MCP capture moves from verification-only to applied behaviour.

## Acceptance Criteria (refined 2026-06-25)

- Primary output for the current fix unit is a marketplace plugin fix in
  `plugins/opencode-sync/skills/opencode-sync/scripts/ingest_source.py` with any required
  regression coverage under `plugins/opencode-sync/tests/`.
- When `ingest_source.py --respect-claude-settings` runs against this marketplace, valid plugins are
  retained unless they are explicitly disabled, so plugin-level filtering no longer hides eligible
  sibling skills or agents such as `plugins/skills-toolkit/agents/*.md`.
- The failing discovery and generation path is covered by regression tests, and the non-flagged
  execution path remains intact.
- Out of scope for this refinement pass: building a new OpenCode-native memory plugin or reopening
  optional command-wrapper work.
- Broad WS4 and WS5 cleanup stays pending unless it is directly required to land the current fix.
- Before any broader scope is taken on, the current fix unit should pass user review on the refined
  acceptance criteria and resulting implementation.

## Refinement Notes

2026-06-25:

- Primary output locked: marketplace plugin fixes.
- Done criteria locked: bug fixed plus tests pass.
- Out of scope locked: no new memory plugin.
- Blockers locked: eval/advisory only, plus a user review gate.
- Practical feasibility advisory: keep the work at the ingest boundary, prove the rule with
  regression coverage, and avoid broad discovery or memory refactors in this pass.
- AI systems advisory: make plugin-level versus file-level filtering semantics explicit, assert the
  downstream generation result, and preserve the unflagged execution path.
- Advisory outcome accepted as-is by the user before write-back.

## Current session outcome

- [x] Compared standalone `opencode-sync` against the marketplace plugin copy.
- [x] Confirmed no saved `builder-plans/.../state.json` existed for this work in AIOS,
  `ai-os-jc-toast`, or `work-registry-autocommit-worktree`.
- [x] Recreated the continuation plan in this repo so `/continue-plan` can pick it up here next.
- [x] Improved `--wire-memory` so OpenCode reads repo-root `MEMORY.md` first when present, then
  `AGENTS.md`, then the global memory index. Added regression coverage and a reference note for the
  remaining gap vs memory-os hooks.
- [x] Started WS5 downstream cleanup in AIOS with commit `8fdbc06` (`docs: reference slack tools
  by intent`).
- [x] Fixed `--respect-claude-settings` so non-disabled sibling plugins remain available during
  marketplace ingest, restoring discovery and generation for assets such as `skills-toolkit`
  agents.
- [x] Added catalogue-style verification to `ingest_source.py`, comparing expected versus
  discovered skills, agents, commands, and hooks during ingest preview.
- [x] Split Claude MCP routing by scope: user `mcpServers` remain global, while repo
  `.claude/settings.json` and `.claude/settings.local.json` `mcpServers` now route to the project
  `opencode.json` fragment.
- [x] Explicitly decided that hooks remain verification-only for now and documented that runtime
  boundary in the plugin docs and references.
- [x] Refreshed `plugins/opencode-sync/README.md` using the new type-driven README workflow shape,
  correcting the marketplace-repo script paths and aligning the public docs with the shipped
  ingest, verification, and MCP-routing behaviour.
- [ ] T-P5-01 remains pending until prompt-box autocomplete becomes a real user need that justifies
  command-wrapper generation.
- [x] The shipped `opencode-sync` follow-up work landed on `master` via merged marketplace PRs
  `#27` and `#28`.

## Merge status

- The delivered `opencode-sync` work from this continuation plan is merged.
- `T-P5-01` remains intentionally open as a future opportunity-driven follow-up, not a blocked
  implementation item.

## Notes

- The standalone repo may still carry additional repo-only files such as `.github/`, `.git/`,
  `LICENSE`, and local scratch/config directories. Those are not continuation blockers for the
  marketplace plugin unless a future change explicitly needs them.
- The private `CONTINUE-HERE.md` is now best treated as historical context, not the active status
  ledger.
- For multi-session repos, evaluate branch freshness and worktree state before every new fix unit.
  If the primary checkout is dirty or clearly active elsewhere, prefer a fresh worktree from the
  latest fetched refs and commit from there.
