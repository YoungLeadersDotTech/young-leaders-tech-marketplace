# Changelog

All notable changes to `update-readme` are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-06-26

### Changed
- Reframed `update-readme` from a detail-level-first README generator into a type-driven workflow
  that detects the README family first, confirms it with the user, then asks for style,
  audience, and depth.
- Added explicit guidance for README families, presentation controls, and audience-aware section
  bias so the skill produces a better fit for each target repo type.
- Strengthened privacy and output-safety guidance: public README output must avoid private
  individual names or personal email addresses, must prefer TODO comments over invention, and must
  keep preview-before-write as a hard gate.

## [1.0.3] - 2026-06-19

### Changed
- Added explicit OpenCode/Cowork degradation wording for AskUserQuestion and Task* phase tracking
  so the shipped skill matches its cross-runtime contract.

## [1.0.2] - 2026-06-19

### Changed
- Scrubbed product-specific public wording from the plugin description, README, and SKILL.md.
- Reframed the repo-type language around a generic service repository so the public plugin docs do
  not point at internal-only workflows.

## [1.0.1] - 2026-05-12

### Changed
- README.md install section rewritten to the canonical Claude Code plugin marketplace flow (`/plugin marketplace add` + `/plugin install update-readme@young-leaders-tech-marketplace` + `/reload-plugins`). Removed the legacy `./install-plugin.sh install update-readme` builder-style invocation and the raw-URL fallback.

## [1.0.0] - 2026-05-10

### Added
- Initial plugin: universal README updater that classifies repo type (plugin, marketplace, library, monorepo, service repo, personal), asks detail level, and generates a README using a section catalogue keyed on type plus detail level. `/update-readme` slash command and the `update-readme` skill.
