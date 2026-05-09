# Changelog

All notable changes to `skills-toolkit` are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.4] - 2026-05-09

### Changed
- Flattened plugin source layout: 4 skill folders moved from `plugins/skills-toolkit/skills/shared/<name>/` to `plugins/skills-toolkit/skills/<name>/`. Brings skills-toolkit into line with the marketplace's other plugins (terminal-setup-macos, update-readme), which use the flat `skills/<name>/` convention.
- `plugin.json` `skills:` array updated to drop the `/shared` path prefix (4 entries).
- `install.sh` source-side glob updated from `skills/shared/*/` to `skills/*/`. Install destination unchanged: templates still install to `~/.claude/skills/shared/<name>/` so the user-side three-scope convention (personal / projects / shared) is preserved.

### Notes
- The `shared/` wrapper at the plugin source level mirrored the install destination, but Claude Code reads plugin source paths from `plugin.json` directly - the wrapper added nothing for plugin consumers and visually misled readers browsing the repo. The user-side install location keeps `shared/` because that scope convention is real and load-bearing.
- No SKILL.md content changes. No agent or command file changes. No behaviour change for anyone installing via the marketplace.

## [2.0.3] - 2026-05-08

### Changed
- `plugin.json` `agents`, `commands`, and `skills` arrays are now alphabetically sorted (CI naming validator rule per the canonical Claude Code skill frontmatter reference). Zero behaviour change.
- All 4 shared SKILL.md files declare `disable-model-invocation: true`. They are static templates with verbatim output - this loads them as context only (no LLM reasoning pass), saving tokens on auto-invoke.
- `references/marketplace-guidelines.md` section 6 (Frontmatter Description Cap) now cites the Anthropic Claude Code docs source for the 250-character rule and explains the truncation behaviour ("descriptions exceeding 250 characters are truncated in the skill listing"). Front-loading guidance added.

## [2.0.2] - 2026-05-08

### Fixed
- `skill-creator-agent` frontmatter `tools:` was missing `AskUserQuestion` despite the agent being described as an interactive guide. Added per the canonical tools reference rule that every interactive agent must include `AskUserQuestion`.
- `agent-validator` Phase 3 canonical tool registry was incomplete and the previous v2.0.1 attempt to fix it conflated two separate tool primitives. Rebuilt the registry against the canonical Claude Code tools reference with named groups: file ops (4), search (2), execution (2 - now including `KillShell`), web (2), orchestration (7), task management (4), subagent lifecycle (2 - `TaskOutput`/`TaskStop`), MCP and tool discovery (3 - now including `ListMcpResourcesTool`, `ReadMcpResourceTool`), background and scheduling, and pass-through MCP server tools.
- `agent-validator` Phase 3 flags now include explicit warnings for: `TaskOutput`/`TaskStop` listed without `Task` (over-permissioning antipattern; these tools manage background subagents and have no effect without a `Task` invocation using `run_in_background: true`); deprecated `MCPSearch` (use `ToolSearch`); interactive agents missing `AskUserQuestion`.

### Reverted
- v2.0.1 changes were reverted: that release added `TaskOutput` and `TaskStop` to all four agent frontmatters under the assumption that the Task* family is six tools. Per the canonical tools reference, task management (`TaskCreate, TaskUpdate, TaskGet, TaskList`) and subagent lifecycle (`TaskOutput, TaskStop`) are separate primitives. The latter pair only has effect when `Task` (subagent spawning) is also present in the `tools:` list. None of the four plugin agents spawn background subagents, so v2.0.1 was the over-permissioning antipattern that the validator should now detect.

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
