# Skills Toolkit for Claude Code

Author and validate Claude Code skills and agents for this marketplace - with a real deterministic script doing the checking, not a model self-grading its own homework.

## What it does

Building a skill or agent by hand means re-deriving the same rules every time: description length, PII, frontmatter shape, whether a "5-file rule" version bump actually happened. This plugin turns those rules into a script (`scripts/validate_skills.py`) that a skill runs and relays verbatim - so "does this pass?" has one real answer instead of a model's best guess. It also ships reusable templates for common skill types and agent/hook infrastructure, so new artefacts start from a working shape instead of a blank file.

## Getting started

```text
/plugin marketplace add git@github.com:YoungLeadersDotTech/young-leaders-tech-marketplace.git
/plugin install skills-toolkit@young-leaders-tech-marketplace
/reload-plugins
```

Then just ask for what you want - "create a skill for X" or "validate this SKILL.md" - the `skills-toolkit` skill picks it up automatically. See its own `SKILL.md` for the exact trigger phrases.

## Skills

| Skill | Description |
|-------|-------------|
| `skills-toolkit` | Create and validate SKILL.md and agent `.md` files. Runs `scripts/validate_skills.py` (description-cap, PII, em-dash, frontmatter shape, Task* completeness, command-wrapper detection) and relays real findings - never a self-scored rubric. |
| `stakeholder-templates` | Scaffold for team/person context skills - roles, goals, pain points, communication preferences. |
| `ground-truth-template` | Scaffold for canonical reference documentation - verified facts, process flows, error codes. |
| `product-context-template` | Scaffold for product vision/goals/constraints skills - target users, features, UX principles. |
| `initiative-overview-template` | Scaffold for cross-functional initiative coordination - charter, work streams, dependencies. |

## Agents (legacy, kept for now)

Four prose-based agents predate the script-backed `skills-toolkit` skill and are still installed - their command-wrapper entry points (`/create-skill`, `/validate-skill`, `/list-skills`) were removed in 3.0.0, but the agent files themselves were not superseded:

- **skill-creator-agent** - interactive skill creation walkthrough
- **skill-validator-agent** - read-only skill validator (prose-based; use the `skills-toolkit` skill's script-backed validation instead for a verifiable result)
- **agent-author** - agent creation/edit/package modes
- **agent-validator** - agent validation against `references/marketplace-guidelines.md`

New work should go through the `skills-toolkit` skill. These agents are not yet on a removal date.

## Architecture

```
plugins/skills-toolkit/
  skills/skills-toolkit/       # primary interface - script-backed create + validate
    SKILL.md
    scripts/validate_skills.py
  skills/{stakeholder,ground-truth,product-context,initiative-overview}-templates/
  agents/                      # legacy prose-based agents (see above)
  templates/                   # 13 ready-to-crib agent/hook/infra templates
  references/
    marketplace-guidelines.md  # 5-file rule, semver table, severity taxonomy
    to-scale-prototype-showcase.md
  scripts/check_plugin_version_sync.py  # deterministic 5-file version-sync gate
  examples/                    # sample-subagent.md, sample-portable-agent/
```

### Templates (`templates/`)

Ready-to-crib scaffolds `agent-author` consumes during create/package modes: canonical subagent and portable-agent skeletons, an install-script template (`--global`/`--project`/`--sync-back`), a bundle README template, four hook templates (generic, SessionStart, PreToolUse, PostToolUse), an agent-coordination pattern doc, a change-propagation guide, a logging skeleton, a validation-checklist template, and a structured-choice (`AskUserQuestion`) template.

### `references/marketplace-guidelines.md`

The single ground-truth doc `agent-validator` and `skill-validator-agent` cite: 5-file rule, semver decision table, same-commit ordering rule, CHANGELOG format (Keep a Changelog), description cap (<=250 chars), em-dash ban, migration pattern (global skill -> plugin skill), and the BLOCKER/WARNING/INFO severity taxonomy.

### `scripts/check_plugin_version_sync.py`

A deterministic 5-file gate for marketplace plugins - checks `VERSION`, `CHANGELOG.md`, `plugin.json`, the marketplace.json entry, and the README version header all agree. `agent-validator` runs this first for plugin-bound artefacts, falling back to a manual checklist only if the script is unavailable.

## How validation works

`validate_skills.py` checks description length/PII/em-dash/frontmatter shape and Task* completeness against real code, not model judgment - `skills-toolkit` relays its findings and exit code verbatim rather than inventing a PASS/FAIL verdict. `Q8-VAGUE-ASK-USER` (added 3.1.0) additionally flags "ask the user" prose with no real `AskUserQuestion` behind it, using `references/askuserquestion-protocol.md` as the canonical structured-question shape.

## Development

No test suite ships with this plugin yet - validate changes by running `scripts/validate_skills.py` and `scripts/check_plugin_version_sync.py` directly against the plugin's own files before committing.

## Version

**Version**: 3.1.0

See [CHANGELOG.md](./CHANGELOG.md) for full release notes.
