# diy-sketchup-mcp

**Version**: 0.1.0

Registers the [SketchUp MCP server](https://github.com/mhyrr/sketchup-mcp) (`sketchup-mcp` on
PyPI) so Claude can drive SketchUp directly - create, modify, and inspect geometry, run Ruby code
against a live SketchUp document, and take screenshots. Scoped to this plugin only: the MCP server
activates when you enable `diy-sketchup-mcp`, not for every `diy-build-companion` user.

## What it does

- **Registers the MCP server**: `.mcp.json` declares `command: uvx, args: [sketchup-mcp]` -
  Claude Code spawns it on demand, the same way `npx -y <package>` works for Node-based MCP
  servers.
- **No bundled skill**: this plugin's entire payload is the MCP registration plus this README.
  For usage patterns, connection-flakiness triage, and known geometry bugs once the MCP is
  running, see `diy-build-companion`'s
  [`reference/sketchup-mcp-tips.md`](https://github.com/YoungLeadersDotTech/young-leaders-tech-marketplace/blob/master/plugins/diy-build-companion/skills/diy-continue/reference/sketchup-mcp-tips.md).

## Setup

1. **Prerequisite**: `uv` must be installed (`brew install uv` if you don't have it already).
   `uvx` fetches and runs `sketchup-mcp` transparently on first use - no separate install step.
2. **Enable this plugin** in Claude Code - the MCP server becomes available automatically.
3. **Install the SketchUp-side extension** (the one step with no CLI path - GUI only, per
   upstream's own README):
   - Download or build the `.rbz` file from
     [mhyrr/sketchup-mcp](https://github.com/mhyrr/sketchup-mcp).
   - In SketchUp: `Window > Extension Manager > Install Extension`, select the `.rbz` file.
   - Restart SketchUp.
   - In SketchUp: `Extensions > SketchupMCP > Start Server` (default port 9876).

Once both sides are running, Claude can call the `sketchup` MCP tools directly.
