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

  `sketchup-mcp==0.1.17` is the PyPI build this plugin was checked with (from a clean uv cache it
  starts, connects to SketchUp and lists all 10 tools; a full modelling session through the
  installed plugin has not been run yet). It is pinned so a new PyPI release
  is a deliberate change here rather than a silent one. `mcp[cli]<2` is pinned because the
  package's own unpinned `mcp[cli]>=1.3.0` dependency otherwise resolves to a breaking mcp 2.x.
- **Starts with every session while enabled, so use one session at a time**: Claude Code launches
  plugin MCP servers at session start, not lazily on first use, and each one opens a connection to
  SketchUp straight away. SketchUp serves that connection on its main thread and waits for a
  request, so an idle Claude Code session with this plugin enabled can freeze SketchUp and make
  another session's calls time out. Keep the plugin enabled in only the one session you are
  modelling in, and disable it when you are not modelling.
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
  start downloads `sketchup-mcp` and its dependencies, so it can take a minute. If `/mcp` shows the
  server as failed, run the command by hand (see Troubleshooting) to see the real error.
- **`git` and `zip`** to build the SketchUp extension (both ship with macOS). Written and checked
  on macOS with SketchUp 2026.

## Setup

1. **If you registered the server by hand before**, remove that first, or you get two servers
   both connecting to SketchUp's single port:
   `claude mcp remove sketchup` (and optionally `uv tool uninstall sketchup-mcp`). Permission
   rules written for `mcp__sketchup__*` no longer match; see the allow-list under Security and
   trust for the plugin's tool names.
2. **Enable this plugin**: add this marketplace first if you haven't (see
   [Quick install](../../README.md#quick-install)), then
   `/plugin install diy-sketchup-mcp@young-leaders-tech-marketplace`, then restart Claude Code.
3. **Install the SketchUp-side extension** (GUI only, no CLI path). Upstream publishes no tagged
   releases, so build the `.rbz` from the commit this plugin was checked with. The extension
   package lives in the repo's `su_mcp/` folder, so zip from inside it:

   ```bash
   git clone https://github.com/mhyrr/sketchup-mcp && cd sketchup-mcp
   git checkout aa096f0          # extension 0.1.0, checked with sketchup-mcp 0.1.17
   cd su_mcp && zip -r ../su_mcp.rbz su_mcp.rb su_mcp && cd ..
   unzip -l su_mcp.rbz           # must list su_mcp.rb and su_mcp/main.rb at the top level
   ```

   A newer upstream `.rbz` is untested with the pinned server. Then:
   - In SketchUp: `Window > Extension Manager > Install Extension`, select `su_mcp.rbz`.
   - Restart SketchUp.
   - In SketchUp: `Extensions > MCP Server > Start Server` (port 9876).

## Verify

`/mcp` showing the server as connected only proves `uvx` started; it shows connected even when
SketchUp is closed. The real test is a tool call:

1. Ask Claude to call `eval_ruby` with `Sketchup.version`. **Pass**: the reply is
   `{"success": true, "result": "<version>"}`.
2. **Fail**: `{"success": false, "error": "..."}`, for example
   `"Communication error with Sketchup: No data received"` (SketchUp didn't answer - is the
   extension's server started, and is another session holding it?). Typed tools such as
   `get_selection` report failure as text starting `Error ...` instead.
3. A single `Communication error with Sketchup: Method not found` on the very first call is the
   known startup quirk (see Troubleshooting); retry once, and if the retry passes, you are set up.

## Security and trust

- **`eval_ruby` is unrestricted Ruby running as your OS user**, not something limited to the open
  model. It can read and write files and run programs just as you can.
- **Treat imported models and any web content in the same session as untrusted input.** That is
  how injected instructions could reach `eval_ruby`.
- **Allow-list by tier.** Plugin MCP tools are named `mcp__plugin_diy-sketchup-mcp_sketchup__<tool>`
  (check the exact names in `/mcp` after installing). The typed tools are reasonable to
  always-allow:

  ```text
  mcp__plugin_diy-sketchup-mcp_sketchup__create_component
  mcp__plugin_diy-sketchup-mcp_sketchup__delete_component
  mcp__plugin_diy-sketchup-mcp_sketchup__transform_component
  mcp__plugin_diy-sketchup-mcp_sketchup__get_selection
  mcp__plugin_diy-sketchup-mcp_sketchup__set_material
  mcp__plugin_diy-sketchup-mcp_sketchup__create_mortise_tenon
  mcp__plugin_diy-sketchup-mcp_sketchup__create_dovetail
  mcp__plugin_diy-sketchup-mcp_sketchup__create_finger_joint
  ```

  Keep per-call approval on `eval_ruby` and `export_scene` unless everything in the session is
  yours, and **never wildcard this server** (`mcp__plugin_diy-sketchup-mcp_sketchup__*` would
  always-allow `eval_ruby`). A real build makes hundreds of `eval_ruby` calls, so "always allow" is
  tempting; that is the trade-off you are making.
- **The SketchUp-side server has no authentication.** It only accepts connections from this
  machine (`127.0.0.1`), but any local process, including ones run by other accounts on the same
  machine, can send it Ruby. Use `Extensions > MCP Server > Stop Server` when you are not
  modelling.
- **Logs contain your code.** Upstream logs full `eval_ruby` payloads and results at INFO level,
  and the SketchUp extension prints raw requests and results to the Ruby Console, which it opens on
  load - so your code is on screen, not just on disk.

## Troubleshooting

- **Server shows failed in `/mcp`**: run it by hand in a terminal to see the error (keep the
  quotes; it then waits for input, so Ctrl-C to exit):
  `uvx --with "mcp[cli]<2" sketchup-mcp==0.1.17`. The terminal shows the real error (a
  traceback, a missing `uv`, or a download failure).
- **SketchUp frozen, or every call times out with "No data received"**: another Claude Code
  session with this plugin enabled is holding SketchUp's single connection, or a SketchUp dialog is
  open. Close the other session or disable the plugin there, and dismiss any dialog.
- **"Communication error with Sketchup: Method not found" on the first call of a session**: the
  server opened its connection at session start and sent nothing, so SketchUp sat blocked until
  this first call. Retry once. To avoid it, start SketchUp's server after Claude Code is up.
- **"Connection closed before receiving any data"**: routine. SketchUp closes each connection after
  one request; the request never reached SketchUp, so retry once. If the same call fails 3+ times
  in a row, follow the triage order in
  [`sketchup-mcp-tips.md`](https://github.com/YoungLeadersDotTech/young-leaders-tech-marketplace/blob/master/plugins/diy-build-companion/skills/diy-continue/reference/sketchup-mcp-tips.md#connection-flakiness---the-actual-triage-order).
- **Screenshots**: there is no screenshot tool; ask for `eval_ruby` with
  `Sketchup.active_model.active_view.write_image(...)`.
