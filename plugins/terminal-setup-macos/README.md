# terminal-setup-macos

Idempotent installer for a kitted macOS terminal: Ghostty, Oh My Zsh, Powerlevel10k,
Glow, MesloLGS Nerd Font, plus an optional markdown-preview kit (MacDown 3000, grip,
entr, OSC 8 clickable paths).

The companion to the
[**"Print this PDF, drop it in Claude Code, get a fully kitted terminal"** blog post](https://www.youngleaders.tech/p/7982b16d-9aa5-4281-b370-6647134cdf7d?postPreview=paid).
<!-- TODO-DEEPLINK: blog post is currently a Substack draft preview URL. Replace
with the canonical published URL `https://www.youngleaders.tech/terminal-setup-pdf-meta-guide`
once the post is live. -->


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
6. **Wires the markdown-preview kit** if you opted in: installs **MacDown 3000**
   (a notarised fork of MacDown that auto-refreshes the preview when the file is
   changed externally - the original MacDown requires close+reopen), registers it
   as the default `.md` handler using bundle ID `app.macdown.macdown3000`, adds
   `preview`, `mdwatch`, `mdls`, and `o` aliases.
7. **Runs sanity tests** on the new shell config before declaring victory.

## Known gotchas the skill handles for you

- This plugin uses **MacDown 3000** (cask `macdown-3000`), not the original
  MacDown. The original does not auto-refresh on external file edits - close and
  reopen the file is required - which breaks the "watch your agent edit live"
  use case. MacDown 3000 is a notarised fork (MIT, by Schuyler Erle) that refreshes
  live.
- The MacDown 3000 bundle ID is `app.macdown.macdown3000`. The skill uses this and
  rebuilds LaunchServices if a phantom `com.uranusjr.macdown` or `io.macdown.MacDown`
  registration is cached from an older install.
- The `macdown` and `macdown-3000` casks conflict. If `macdown` is already
  installed, the skill uninstalls it first.
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
