# Young Leaders Tech Marketplace

A small, opinionated Claude Code plugin marketplace. Works with both Claude Code and [OpenCode](https://opencode.ai) (each plugin's skills are exposed via `opencode.json`, and `AGENTS.md` carries the cross-runtime resolution rules).

## What this is

A personal marketplace shipping plugins for authoring Claude Code skills and agents,
setting up a kitted macOS terminal in one shot, refreshing READMEs, packaging enablement
into self-contained HTML, syncing Claude Code assets into OpenCode, and shipping
standalone Cowork-friendly skills. Each plugin is self-contained with its own version,
manifest, and README. Add the marketplace once and Claude Code picks up everything in
`plugins/`.

## Quick install

In Claude Code, add this marketplace once. **Use the SSH form** - the plugin
marketplace install path requires SSH auth even if HTTPS works for everything else:

```text
/plugin marketplace add git@github.com:YoungLeadersDotTech/young-leaders-tech-marketplace.git
```

Then install whichever plugins you want by name:

```text
/plugin install skills-toolkit@young-leaders-tech-marketplace
/plugin install terminal-setup-macos@young-leaders-tech-marketplace
/plugin install update-readme@young-leaders-tech-marketplace
```

Or browse interactively:

```text
/plugin
```

After installing, run `/reload-plugins` to activate them in the current session.

### "Permission denied (publickey)" when adding the marketplace?

You don't have SSH auth set up for GitHub yet. The fix: run `gh auth login` once
for HTTPS and once for SSH (pick the SSH protocol on the second run, accept the
default key). HTTPS handles regular Git operations; SSH is what
`/plugin marketplace add git@github...` actually uses.

> HTTPS is used for regular Git operations. SSH is required for the plugin
> marketplace install command (`/plugin marketplace add git@github...`). If you
> skip SSH auth, you'll see "Permission denied (publickey)" when trying to
> install plugins.
>
> - adapted from `FULL-SETUP-GUIDE.md` section 1.4

### Other ways to add the marketplace

| Form | Command | When |
|---|---|---|
| SSH (recommended above) | `/plugin marketplace add git@github.com:YoungLeadersDotTech/young-leaders-tech-marketplace.git` | Works once SSH auth is set up |
| HTTPS git URL | `/plugin marketplace add https://github.com/YoungLeadersDotTech/young-leaders-tech-marketplace.git` | If you only have HTTPS auth and the marketplace download path doesn't trip on it |
| GitHub shorthand | `/plugin marketplace add YoungLeadersDotTech/young-leaders-tech-marketplace` | Works when `gh` is authenticated |
| Local path | `/plugin marketplace add ./local-clone-path` | For local development |
| Direct JSON URL | `/plugin marketplace add https://github.com/YoungLeadersDotTech/young-leaders-tech-marketplace/raw/master/.claude-plugin/marketplace.json` | Fallback only |

Verify with `/plugin marketplace list`.

## Available plugins

| Plugin | Version | What it does |
|---|---|---|
| [skills-toolkit](./plugins/skills-toolkit/README.md) | 2.0.7 | Toolkit for authoring and validating Claude Code skills and agents. Ships `agent-author`, `agent-validator`, reusable templates, validator references, and installable commands for common authoring flows. |
| [terminal-setup-macos](./plugins/terminal-setup-macos/README.md) | 1.2.2 | Idempotent macOS terminal installer covering Ghostty, Oh My Zsh, Powerlevel10k, Glow, and MesloLGS Nerd Font, plus optional markdown-preview and clickable-path extras. |
| [update-readme](./plugins/update-readme/README.md) | 1.1.0 | Type-driven README updater. Detects repo family, confirms it with the user, asks for style, audience, and depth, then generates a matched README preview before writing. |
| [standalone-skills](./plugins/standalone-skills/README.md) | 1.0.0 | Self-contained, Cowork-friendly skills with no cross-plugin dependencies. |
| [opencode-sync](./plugins/opencode-sync/README.md) | 1.6.4 | Sync and validate Claude Code assets for OpenCode: ingest marketplaces or repos, validate dual-runtime portability, generate agents, verify discovery coverage, and route MCP config by scope. |
| [enablement-html-renderer](./plugins/enablement-html-renderer/README.md) | 1.2.3 | Packages finished enablement content into one self-contained HTML handoff with multiple reader-selectable formats. |

## Local development helper

If you've cloned this marketplace and want to install a plugin straight from disk
(useful while authoring), the bundled helper script wraps each plugin's own
`install.sh`:

```bash
./install-plugin.sh list
./install-plugin.sh install skills-toolkit
```

Each plugin's `install.sh` runs in `--global` mode by default. This path is for
local development; published consumers should use `/plugin marketplace add`
above instead.

## Adding a plugin

1. Create a new directory under `plugins/<name>/` with this layout:
   ```text
   plugins/<name>/
   ├── .claude-plugin/
   │   └── plugin.json
   ├── commands/         # optional
   ├── agents/           # optional
   ├── skills/           # optional
   ├── README.md
   └── VERSION
   ```

2. `plugin.json` requires the standard five fields plus arrays for whichever artefact
   types you ship:
   ```json
   {
     "name": "your-plugin-name",
     "description": "Clear description front-loading auto-invoke triggers. Max 250 chars. No em dashes. No forward slashes in description.",
     "author": {
       "name": "Young Leaders Tech",
       "url": "https://youngleaders.tech"
     },
     "homepage": "https://github.com/YoungLeadersDotTech/young-leaders-tech-marketplace",
     "version": "1.0.0",
     "commands": ["./commands/your-command.md"],
     "agents": ["./agents/your-agent.md"],
     "skills": ["./skills/your-skill"]
   }
   ```

3. Skills live directly under `plugins/<name>/skills/<skill>/` (flat layout).
   The `~/.claude/skills/{personal, projects, shared}/` three-scope convention is
   user-side only; do not mirror it in plugin source.

4. Register the plugin in `.claude-plugin/marketplace.json` at the repo root.

5. Open a PR. Once merged, run `/reload-plugins` to pick up the changes.

For the full authoring + validation workflow with description quality scoring and PII
checks, install `skills-toolkit` and use `/create-skill` or the `skill-creator-agent` workflow.

## Marketplace structure

```text
.claude-plugin/marketplace.json     # registry (semver, plugin entries)
.marketplace-config.json            # extended metadata (categories, features)
install-plugin.sh                   # browse + install helper
plugins/
├── skills-toolkit/
├── terminal-setup-macos/
└── update-readme/
README.md                           # this file
```

## License

MIT - see [LICENSE](./LICENSE). You are free to use, modify, and distribute these plugins; attribution appreciated.

## Maintainer

Young Leaders Tech &middot; <https://youngleaders.tech>

<!-- Last verified: 2026-06-14 -->
