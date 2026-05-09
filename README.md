# Young Leaders Tech Marketplace

A small, opinionated Claude Code plugin marketplace.

## What this is

A personal marketplace shipping plugins for authoring Claude Code skills and agents,
setting up a kitted macOS terminal in one shot, and refreshing READMEs across any kind
of repo. Each plugin is self-contained with its own version, manifest, and README.
Add the marketplace once and Claude Code picks up everything in `plugins/`.

## Quick install

Add this marketplace to Claude Code using the raw URL of `marketplace.json`:

```text
https://github.com/YoungLeadersDotTech/young-leaders-tech-marketplace/raw/master/.claude-plugin/marketplace.json
```

> Use the `raw` URL, not the `blob` URL, or the marketplace fails to load.

Then `/plugin install <name>` for whichever plugins you want.

## Available plugins

| Plugin | Version | What it does |
|---|---|---|
| [skills-toolkit](./plugins/skills-toolkit/README.md) | 2.0.4 | Toolkit for authoring and validating Claude Code skills and agents. Ships `agent-author` (build / edit / package), `agent-validator` (cites `marketplace-guidelines.md` for findings), four shared skill templates, and 13 author and infrastructure templates. |
| [terminal-setup-macos](./plugins/terminal-setup-macos/README.md) | 1.0.0 | Idempotent macOS terminal installer covering Ghostty, Oh My Zsh, Powerlevel10k, Glow, and MesloLGS Nerd Font, plus an optional markdown-preview kit (MacDown, grip, entr, OSC 8 clickable paths). Encodes the gotchas the original install guides got wrong. |
| [update-readme](./plugins/update-readme/README.md) | 1.0.0 | Universal README updater. Scans the target, classifies repo type (plugin, marketplace, library, monorepo), asks detail level, then generates. Six-phase workflow with `Task*` tracking and `AskUserQuestion` gates at type confirmation, detail level, and write-or-dry-run. |

## Browse and install via the helper script

If you have the marketplace cloned locally:

```bash
./install-plugin.sh list
./install-plugin.sh install skills-toolkit
./install-plugin.sh install terminal-setup-macos
./install-plugin.sh install update-readme
```

Each plugin's `install.sh` runs in `--global` mode by default.

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
checks, install `skills-toolkit` and use `/skills-toolkit:create-skill`.

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

## Maintainer

Young Leaders Tech &middot; <https://youngleaders.tech>

<!-- Last verified: 2026-05-09 -->
<!-- TODO: add LICENSE file at repo root (plugin READMEs reference MIT but no LICENSE file is committed) -->
