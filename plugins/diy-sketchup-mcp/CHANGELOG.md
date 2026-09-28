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
  a hand-registered `sketchup` server, the one manual step (installing the `.rbz` via
  Window > Extension Manager, tested with extension 0.1.0), a verify step, a security and trust
  section for `eval_ruby`, and troubleshooting.
