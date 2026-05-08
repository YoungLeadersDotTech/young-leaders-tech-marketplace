# terminal-setup-macos

Idempotent installer for a kitted macOS terminal: Ghostty, Oh My Zsh, Powerlevel10k,
Glow, MesloLGS Nerd Font, plus an optional markdown-preview kit (MacDown, grip, entr,
OSC 8 clickable paths).

The companion to the
[**"Print this PDF, drop it in Claude Code, get a fully kitted terminal"** blog post](https://YOURBLOG.example.com/terminal-setup-meta-guide).

The blog post is the explainer with screenshots. This plugin is the executable. Both
end at the same place; pick whichever entry point suits.

## Install

```bash
# From the marketplace root
./install-plugin.sh terminal-setup-macos
```

Or, if the marketplace is already added to Claude Code, just run the slash command:

```text
/terminal-setup-install
```

## What it does

1. **Preflights.** Checks what's already installed. Won't reinstall things you already have.
2. **Backs up `~/.zshrc`** before Oh My Zsh rewrites it. Restores your existing PATH
   exports, aliases, and tool inits (SDKMAN stays at the very end as required).
3. **Installs the core stack** sequentially (parallel `brew install` calls hit a
   portable-Ruby lock; this skill avoids that pitfall).
4. **Configures Ghostty** at `~/.config/ghostty/config` with the dracula theme,
   MesloLGS NF font, and `shell-integration = zsh` (NOT `true` - that triggers a
   Configuration Errors dialog).
5. **Asks you about optional extras** via a multi-select picker. Each option's
   description includes a deep-link to the relevant screenshot in the blog post.
6. **Wires the markdown-preview kit** if you opted in: registers MacDown as the
   default `.md` handler using the correct bundle ID `com.uranusjr.macdown` (some
   guides have the wrong one), adds `preview`, `mdwatch`, `mdls`, and `o` aliases.
7. **Runs sanity tests** on the new shell config before declaring victory.

## Known gotchas the skill handles for you

- The MacDown bundle ID is `com.uranusjr.macdown`, not `io.macdown.MacDown`. Older
  guides have the wrong one. The skill uses the right one and rebuilds LaunchServices
  if a phantom registration was already cached.
- Ghostty `shell-integration = true` triggers a Configuration Errors dialog. The
  skill writes `shell-integration = zsh` instead.
- SDKMAN must remain at the very end of `~/.zshrc`. The skill enforces this when
  restoring previous customisations.
- The Powerlevel10k wizard cannot run unattended; the skill installs the theme +
  plugin and instructs you to run `p10k configure` interactively in Ghostty after.
- Parallel `brew install` calls cause portable-Ruby lock conflicts. Installs run sequentially.

## Troubleshooting

If something goes wrong, your original `~/.zshrc` is at `~/.zshrc.pre-oh-my-zsh`.
Restore with `mv ~/.zshrc.pre-oh-my-zsh ~/.zshrc && rm -rf ~/.oh-my-zsh`.

## Source material

- Blog post (with screenshots): [link]
- Original install guide PDF, FAQ PDF: see the blog post for credits.
