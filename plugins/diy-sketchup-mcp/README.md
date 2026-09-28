# diy-sketchup-mcp

**Version**: 0.1.0

Registers the community [SketchUp MCP server](https://github.com/mhyrr/sketchup-mcp)
(`sketchup-mcp` on PyPI) so Claude Code can drive a running SketchUp desktop app: create, move and
delete components, set materials, cut joinery, export scenes, and run arbitrary Ruby inside
SketchUp via `eval_ruby`. The server is scoped to this plugin: it is registered only while
`diy-sketchup-mcp` is enabled, not for every `diy-build-companion` user.

## What it does

- **Registers the MCP server**: `.mcp.json` declares exactly this command:

  ```json
  "command": "uvx",
  "args": ["--with", "mcp[cli]<2", "sketchup-mcp==0.1.17"]
  ```

  `sketchup-mcp==0.1.17` is the build this plugin was tested against, pinned so a new PyPI release
  is a deliberate change here rather than a silent one. `mcp[cli]<2` is pinned because the
  package's own unpinned `mcp[cli]>=1.3.0` dependency otherwise resolves to a breaking mcp 2.x.
- **Starts with every session while enabled**: Claude Code launches plugin MCP servers at session
  start, not lazily on first use. Disable the plugin when you are not modelling.
- **No bundled skill**: usage patterns, connection-flakiness triage and known geometry bugs live in
  `diy-build-companion`'s
  [`reference/sketchup-mcp-tips.md`](https://github.com/YoungLeadersDotTech/young-leaders-tech-marketplace/blob/master/plugins/diy-build-companion/skills/diy-continue/reference/sketchup-mcp-tips.md).
  Read it before a modelling session, or use it through `diy-build-companion`'s `diy-continue`
  skill, which loads it for you.

## Prerequisites

- **Licensed SketchUp desktop** (Pro or a desktop trial) on the same machine as Claude Code. The
  server talks to SketchUp over `localhost`, so this does not work from Cowork, claude.ai, or a
  remote machine.
- **`uv`**: `brew install uv` on macOS, or the
  [cross-platform installer](https://docs.astral.sh/uv/getting-started/installation/). The first
  start downloads `sketchup-mcp` and its dependencies, so it can take a minute; if `/mcp` shows the
  server as failed on the very first session, restart Claude Code once.

## Setup

1. **If you registered the server by hand before**, remove that first, or you get two servers
   both connecting to SketchUp's single port:
   `claude mcp remove sketchup` (and optionally `uv tool uninstall sketchup-mcp`). Permission
   allow-lists written for `mcp__sketchup__*` also need updating to the plugin's tool names.
2. **Enable this plugin**:
   `/plugin install diy-sketchup-mcp@young-leaders-tech-marketplace`.
3. **Install the SketchUp-side extension** (GUI only, no CLI path):
   - Upstream publishes no tagged releases. Get the `.rbz` from the upstream README, or build it:
     zip `su_mcp.rb` and the `su_mcp/` folder from the repo root and rename the `.zip` to `.rbz`.
     Tested with extension version 0.1.0 (upstream `master` at `aa096f0`, 2026-04-25).
   - In SketchUp: `Window > Extension Manager > Install Extension`, select the `.rbz`.
   - Restart SketchUp.
   - In SketchUp: `Extensions > SketchupMCP > Start Server` (port 9876).

## Verify

1. `/mcp` in Claude Code shows the plugin's `sketchup` server as connected.
2. Ask Claude to call `get_selection`. Any result, even an empty selection, means both sides are
   talking.

## Security and trust

- **`eval_ruby` is unrestricted Ruby running as your OS user**, not something limited to the open
  model. It can read and write files and run programs just as you can.
- **Treat imported models and any web content in the same session as untrusted input.** That is
  how injected instructions could reach `eval_ruby`.
- **Allow-list by tier.** The typed tools (`create_component`, `delete_component`,
  `transform_component`, `get_selection`, `set_material`, `create_mortise_tenon`,
  `create_dovetail`, `create_finger_joint`) are reasonable to always-allow. Keep per-call approval
  on `eval_ruby` and `export_scene` unless everything in the session is yours. A real build makes
  hundreds of `eval_ruby` calls, so "always allow" is tempting; that is the trade-off you are
  making.
- **The SketchUp-side server has no authentication.** It only accepts local connections, but any
  process running as your user can send it Ruby. Use `Extensions > SketchupMCP > Stop Server`
  when you are not modelling.
- **Logs contain your code.** Upstream logs full `eval_ruby` payloads and results at INFO level,
  and those end up in Claude Code's MCP logs.

## Troubleshooting

- **Server shows failed in `/mcp`**: run the command above by hand in a terminal to see the
  error; usually `uv` is missing or the first download timed out.
- **One `-32601 Method not found` at the start of a session**: expected, retry once.
- **Calls fail intermittently or repeatedly**: follow the triage order in
  [`sketchup-mcp-tips.md`](https://github.com/YoungLeadersDotTech/young-leaders-tech-marketplace/blob/master/plugins/diy-build-companion/skills/diy-continue/reference/sketchup-mcp-tips.md#connection-flakiness---the-actual-triage-order)
  (a dialog blocking the target, corrupted geometry from an earlier write, then restart).
- **Screenshots**: there is no screenshot tool; ask for `eval_ruby` with
  `Sketchup.active_model.active_view.write_image(...)`.
