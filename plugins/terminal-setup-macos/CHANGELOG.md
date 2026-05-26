# Changelog

All notable changes to `terminal-setup-macos` are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-05-26

### Added
- **Automatic Claude Code hook for clickable filenames** (`scripts/post-bash-filename-links.py`). When the "Clickable file paths" extra is selected, the installer now also drops this PostToolUse hook into `~/.claude/hooks/` and patches `~/.claude/settings.json` to wire it up. The hook scans every Bash tool's stdout for bare filenames with known extensions, resolves them to absolute paths (cwd → work-registry → Projects → home, with a depth-5 fallback walk), and rewrites them as OSC 8 hyperlinks with the short filename as display text - so `btt-ai-ways-of-working-faq.md` appears as a short clickable link rather than a full path.
- **`ghostty` added to `supportsClickablePaths()`** in `format-clickable-path.js`. Ghostty was previously only matched via the fallback `xterm-ghostty` → `includes('xterm')` check; it is now an explicit entry in the supported terminals list.
- **`FORCE_HYPERLINK=1` environment variable support** in `format-clickable-path.js`. Mirrors the official Claude Code `FORCE_HYPERLINK` override mechanism so the utility and Claude Code agree on whether OSC 8 is active.
- Bundled scripts now live under `scripts/` in the plugin:
  - `scripts/post-bash-filename-links.py` - the Claude Code PostToolUse hook
  - `scripts/global-utils/format-clickable-path.js` - updated OSC 8 formatter (installed to `~/.claude/global-utils/clickable-paths/` as before)

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
