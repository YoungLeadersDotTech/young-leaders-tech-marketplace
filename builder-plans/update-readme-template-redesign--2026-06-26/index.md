---
solution-id: update-readme-template-redesign
opportunity: null
title: update-readme type-driven redesign
phase: Phase 1 (Plan)
status: ready
status-emoji: ⚪
created: 2026-06-26
updated: 2026-06-26
project-type: plugin maintenance
authored_on: opencode
source-thread: null
---

# ⚪ Solution Plan: update-readme-template-redesign

## Context

This plan captures the redesign of the `update-readme` skill so it behaves like a guided README
authoring workflow rather than a generic regenerator.

The desired product shape is:

- detect what kind of README the target repo needs
- confirm that detected type with the user
- let the user choose the README style and depth
- generate from the matching template family
- preview before writing

This work should also explicitly include a Context7 checkpoint and an eval checkpoint so the final
skill behaviour is grounded and reviewed before any write-heavy rollout.

## Key File Paths (All Absolute - No Discovery Needed)

- **Skill file**: /Users/john.conneely/Projects/young-leaders-tech-marketplace/plugins/update-readme/skills/update-readme/SKILL.md
- **Plugin README**: /Users/john.conneely/Projects/young-leaders-tech-marketplace/plugins/update-readme/README.md
- **Marketplace README**: /Users/john.conneely/Projects/young-leaders-tech-marketplace/README.md
- **Plan file**: /Users/john.conneely/Projects/young-leaders-tech-marketplace/builder-plans/update-readme-template-redesign--2026-06-26/index.md
- **Plan state**: /Users/john.conneely/Projects/young-leaders-tech-marketplace/builder-plans/update-readme-template-redesign--2026-06-26/state.json

## Solution Description

Refactor `update-readme` into a type-driven README workflow with explicit template families,
style modifiers, and audience-aware generation rules. The skill should treat README creation as a
structured choice system, not a one-size-fits-all prose generator.

## Acceptance Criteria

- The skill can distinguish at least these README families: marketplace root, single plugin,
  service repository, generic library or app, monorepo, and personal repo or dotfiles.
- The skill confirms the detected family with the user before generation.
- The skill offers style modifiers that include at least minimal, standard, comprehensive, and
  diagram-aware or no-diagram behaviour.
- The skill can incorporate audience choice when useful, such as user-facing, contributor-facing,
  maintainer-facing, or mixed.
- The workflow includes an explicit Context7 checkpoint for any library, framework, CLI, or
  external API claims that the README would make.
- The workflow includes an explicit eval checkpoint before finalising the updated skill text.
- The updated skill instructions remain free of private contact details or user-specific personal
  notes.
- The skill keeps preview-before-write as a hard gate.

## Approach

### Phase I: Audit current workflow

- [x] T-01: Audit the current `update-readme` skill flow and list where it already supports type
  detection, confirmation, detail level, and preview.
- [x] T-02: Compare the current workflow against the desired product shape and identify the minimum
  structural changes needed to support template families and style modifiers.

### Phase II: Grounding checkpoint

- [x] T-03: Run a Context7 checkpoint for any library, framework, CLI, or external-doc assumptions
  that should influence README generation rules or examples.
- [x] T-04: Convert the grounded findings into explicit generation constraints for the redesigned
  skill.

### Phase III: Redesign the skill

- [x] T-05: Redesign the skill's type-confirmation flow so README family detection is the primary
  routing decision.
- [x] T-06: Add style and depth selection rules, including minimal, standard, comprehensive, and
  diagram-aware or no-diagram variants.
- [x] T-07: Add audience-aware template guidance so the skill can shape sections for user,
  contributor, maintainer, or mixed readership.

### Phase IV: Review and polish

- [x] T-08: Run an eval checkpoint on the redesigned skill to assess whether the workflow is clear,
  feasible, and aligned with the intended user experience.
- [x] T-09: Verify the updated skill text contains no private names, emails, or personal-only
  guidance that should not live in a public marketplace plugin.
- [x] T-10: Summarize the final behaviour changes and decide whether any follow-up work belongs in
  README examples, plugin docs, or tests.

## Notes

- This is separate from the `opencode-sync` continuation plan.
- The focus is the `update-readme` skill design, not a full rewrite of every README in the
  marketplace.
- If the redesign grows into testable helper scripts or references, add them only when the new
  workflow is stable enough to justify the extra maintenance surface.

## Current session outcome

- [x] Audited the shipped `update-readme` workflow and confirmed it already had the skeleton for
  type detection, confirmation, and preview-before-write.
- [x] Reframed the skill from detail-level-first generation into a type-driven workflow that asks
  for README family first, then style, audience, and depth.
- [x] Completed the Context7 checkpoint as a no-op: this redesign introduced no new
  library-specific or framework-specific external claims that needed grounding, so no extra
  constraints were required from docs lookup.
- [x] Ran an eval checkpoint with Practical Jack and Dr Nakamura. Both supported the redesign and
  emphasised deterministic family routing, strong defaults, and privacy-safe public output.
- [x] Verified the updated skill text does not contain private names or personal email addresses.
- [x] Used the redesigned workflow shape to refresh the `opencode-sync` plugin README as a
  follow-on target README update.
- [x] Merged the redesign and README refresh via marketplace PR `#28`.

## Merge status

- Local implementation branch merged into `master`.
- No further follow-up branch is open for this plan at the moment.
- The remaining work, if any, is future refinement rather than unfinished delivery from this run.
