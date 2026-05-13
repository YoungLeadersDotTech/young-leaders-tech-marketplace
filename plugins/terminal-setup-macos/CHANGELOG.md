# Changelog

All notable changes to `terminal-setup-macos` are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.2] - 2026-05-13

### Fixed
- Preflight now explicitly checks for MacDown 3000 (`/Applications/MacDown 3000.app`)
  separately from the original MacDown. Previously the preflight had no MacDown check
  at all, causing the installer to miss the case where the original MacDown was present
  but MacDown 3000 was not.
- Added preflight report rules: original MacDown triggers a warning that it will be
  replaced; MacDown 3000 already installed skips cleanly; neither = not installed.
- Added explicit note that original MacDown (bundle ID com.uranusjr.macdown) is NOT
  equivalent to MacDown 3000 (bundle ID app.macdown.macdown3000).

## [1.1.1] - 2026-05-12

### Changed
- README.md install section rewritten to the canonical Claude Code plugin marketplace flow (`/plugin marketplace add` + `/plugin install terminal-setup-macos@young-leaders-tech-marketplace` + `/reload-plugins`). Removed the legacy `./install-plugin.sh terminal-setup-macos` builder-style invocation.

## [1.1.0] - 2026-05-11

### Added
- Initial plugin landed via PR with skill, slash command (`/terminal-setup-install`), README.

<!-- Older internal history pre-dates the CHANGELOG; this file starts at v1.1.0. -->
