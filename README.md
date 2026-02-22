# Claude Code Plugin Marketplace

Personal marketplace for Claude Code plugins.

## Available Plugins

| Plugin | Description |
|--------|-------------|
| [skills-toolkit](./plugins/skills-toolkit/README.md) | Complete toolkit for creating, validating, and managing Claude Code skills |

## Installing via Marketplace URL

Add this marketplace to Claude Code using the raw URL:

```
https://github.com/YoungLeadersDotTech/young-leaders-tech-marketplace/raw/master/.claude-plugin/marketplace.json
```

> **Note:** Use the `raw` URL, not the `blob` URL, or the marketplace will fail to load.

## Adding Plugins

To add a plugin to this marketplace:

1. Create your plugin directory under `plugins/`:
   ```
   plugins/your-plugin-name/
   ├── .claude-plugin/
   │   └── plugin.json
   ├── commands/
   ├── agents/
   ├── skills/
   └── README.md
   ```

2. Ensure `.claude-plugin/plugin.json` has the correct format:
   ```json
   {
     "name": "your-plugin-name",
     "description": "What this plugin does",
     "author": {
       "name": "Your Name",
       "email": "your@email.com"
     },
     "homepage": "https://github.com/YoungLeadersDotTech/young-leaders-tech-marketplace",
     "version": "1.0.0",
     "commands": ["./commands/command-name.md"],
     "agents": ["./agents/agent-name.md"],
     "skills": ["./skills/skill-name"]
   }
   ```

3. Register the plugin in `.claude-plugin/marketplace.json` at the repo root.

4. Commit and push:
   ```bash
   git add plugins/your-plugin-name/ .claude-plugin/marketplace.json
   git commit -m "Add your-plugin-name plugin"
   git push
   ```

## Plugin Requirements

All plugins must include:
- `.claude-plugin/plugin.json` - Plugin manifest (5 core fields: name, description, author, homepage, version)
- `README.md` - Documentation
- `commands/`, `agents/`, and/or `skills/` directories as applicable

## Maintenance

After adding or updating plugins, update `marketplace.json`:
```bash
# Edit .claude-plugin/marketplace.json to add/update plugin entries
```
