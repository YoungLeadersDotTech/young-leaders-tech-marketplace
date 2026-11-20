# Changelog

All notable changes to the diy-sketchup-mcp plugin.

## [0.1.0] - 2026-09-29

### Added
- **`.mcp.json`**: registers the SketchUp MCP server as
  `uvx --with "mcp[cli]<2" sketchup-mcp==0.1.17` (upstream: mhyrr/sketchup-mcp on GitHub), scoped
  to this plugin so it is only registered while the plugin is enabled. `sketchup-mcp` is pinned to
  the tested 0.1.17; `mcp[cli]<2` avoids the breaking mcp 2.x that the package's unpinned
  dependency otherwise resolves to.
- **`README.md`**: prerequisites (licensed SketchUp desktop, `uv`), setup including migration from
  a hand-registered `sketchup` server, the one manual step (building the `.rbz` from the tested
  upstream commit and installing it via Window > Extension Manager; the menu is
  `Extensions > MCP Server`), a verify step that can actually fail (a real `eval_ruby` call, not
  just `/mcp` connected), a one-session-at-a-time rule (an idle session holds SketchUp's single
  connection), a security and trust section for `eval_ruby` with the exact plugin-prefixed
  allow-list, and troubleshooting.
