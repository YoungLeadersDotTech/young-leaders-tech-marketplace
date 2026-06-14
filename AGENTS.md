# young-leaders-tech-marketplace - Instructions

Claude Code skill/plugin marketplace. Auto-loaded when working anywhere in this repo,
and read by OpenCode as the canonical rules file.

## OpenCode cross-runtime resolution (added by opencode-sync)

When you encounter these Claude Code tokens, resolve them yourself - OpenCode does not expand them automatically:

- `${CLAUDE_PLUGIN_ROOT}` means `plugins/<that-plugin>/` from the repo root.
- A `plugin:skill` reference (for example `Skill("plugin:skill")`) resolves to `plugins/<plugin>/skills/<skill>/SKILL.md`. Read it on a need-to-know basis, or invoke a discovered skill by its bare name via the skill tool.
- Reference-only skills (denied in `permission.skill`) are not in the skill list - load them by reading their SKILL.md path directly when a body references them.
