# Changelog

All notable changes to `update-readme` are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
