# Changelog

All notable changes to the diy-sketchup-mcp plugin.

## [0.1.0] - 2026-09-28

### Added
- **`.mcp.json`**: registers the SketchUp MCP server (`uvx sketchup-mcp`, source
  `github.com/mhyrr/sketchup-mcp`), scoped to this plugin so it only activates when the plugin is
  enabled rather than being registered globally for every user.
- **`README.md`**: setup instructions - the `brew install uv` prerequisite and the one
  unavoidable manual step (installing the SketchUp-side `.rbz` extension via
  Window > Extension Manager, no CLI path exists for this).
