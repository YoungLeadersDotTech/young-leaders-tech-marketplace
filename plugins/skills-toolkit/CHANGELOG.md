# Changelog

All notable changes to `skills-toolkit` are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-05-08

### Added
- `agent-author` agent: end-to-end agent authoring with three modes (create, edit, package). Selected via `AskUserQuestion` at session start. Six-phase lifecycle (Analyse, Design, Generate, Bundle, Validate, Document). Replaces the former three-agent `agent-builder` + `agent-editor` + `agent-packager` chain from the legacy bundle.
- `agent-validator` agent: rewritten clean to validate Claude Code subagent files against `references/marketplace-guidelines.md`. Six-phase lifecycle. Reports findings with severity (BLOCKER, WARNING, INFO) and section citation.
- `references/marketplace-guidelines.md`: ground-truth doc that both validator agents cite. Codifies 4-file rule, semver, ordering rule, two-version-fields rule, CHANGELOG format, frontmatter cap, em-dash ban, migration pattern, and Claude Code plugin schema.
- `templates/`: 13 generic templates (claude-subagent, install-script, bundle-readme, hook-template, hook-sessionstart, hook-pretooluse, hook-posttooluse, portable-agent, agent-coordination, change-propagation-guide, agent-builder-logging, validation-checklist, structured-choice).
- `examples/`: `sample-subagent.md` and `sample-portable-agent/` for users to crib from.

### Changed
- `skill-creator-agent`: tools migrated `TodoWrite` -> `TaskCreate, TaskUpdate, TaskGet, TaskList`. Description trimmed to 227 chars. Body references updated. Employer-flavoured example replaced with generic placeholder.
- `skill-validator-agent`: tools migrated `TodoWrite` -> `TaskCreate, TaskUpdate, TaskGet, TaskList`. Body references updated. Project codename references replaced with generic placeholders.
- `skills/shared/stakeholder-templates/SKILL.md`: description trimmed 312 -> 225 chars. `name:` field corrected to match folder. Project codename references replaced with generic placeholders.
- `skills/shared/ground-truth-template/SKILL.md`: description trimmed 287 -> 213 chars. Project codename references replaced.
- `skills/shared/product-context-template/SKILL.md`: description trimmed 286 -> 225 chars. Employer-flavoured product example replaced with generic placeholder.
- `skills/shared/initiative-overview-template/SKILL.md`: description trimmed 300 -> 239 chars.
- `commands/list-skills.md`: removed non-canonical `pattern: direct` frontmatter field.
- `README.md`: rewritten to reflect 2.0.0 scope (4 agents, templates, references). Tools list updated to reflect Task* migration.
- `plugin.json`: description rewritten to cover skills + agents + templates scope.

### Removed
- Three legacy agents from the source bundle (`agent-builder`, `agent-editor`, `agent-packager`) merged into `agent-author`.
- `agent-builder-context` agent absorbed into `agent-author` Phase 1.
- `confluence-jira-analysis-agent` not ported (employer-coupled, out of scope for a personal marketplace).
- Plugin and marketplace management commands not ported (`marketplace-add`, `marketplace-setup`, `plugin-build`, `plugin-package`).
- All employer-specific and project-specific terminology removed from ported and existing artefacts; replaced with generic placeholder names where examples were needed.

### Security
- New `agent-author` and `agent-validator` agents include explicit security boundary sections: untrusted-input handling for agent specifications, scoped Bash usage, no execution of strings assembled from user input.

## [1.0.0] - 2026-03-01

### Added
- Initial plugin: `skill-creator-agent`, `skill-validator-agent`, `create-skill`, `validate-skill`, `list-skills` commands, four shared skill templates (stakeholder, ground-truth, product-context, initiative-overview).
