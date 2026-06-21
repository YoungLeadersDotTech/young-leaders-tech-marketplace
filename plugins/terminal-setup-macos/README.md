# terminal-setup-macos

Current version: `1.2.2`

Idempotent installer for a kitted macOS terminal: Ghostty, Oh My Zsh, Powerlevel10k,
Glow, MesloLGS Nerd Font, plus an optional markdown-preview kit (MacDown 3000, grip,
entr, OSC 8 clickable paths).

The companion to the
[**"Print this PDF, drop it in Claude Code, get a fully kitted terminal"** blog post](https://www.youngleaders.tech/p/terminal-setup-pdf-meta-guide).

The blog post is the explainer with screenshots. This plugin is the executable. Both
end at the same place; pick whichever entry point suits.

## Install

In Claude Code, add the marketplace once (SSH form - see [root README](../../README.md#quick-install) for HTTPS and other options):

```text
/plugin marketplace add git@github.com:YoungLeadersDotTech/young-leaders-tech-marketplace.git
```

Then install this plugin:

```text
/plugin install terminal-setup-macos@young-leaders-tech-marketplace
```

Activate in the current session:

```text
/reload-plugins
```

Then run the installer slash command:

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
7. **Wires the Claude Code PostToolUse hook** if you picked the Clickable file paths
   extra: drops `post-bash-filename-links.py` into `~/.claude/hooks/` and patches
   `~/.claude/settings.json` so every Bash tool result is scanned for bare filenames
   and rewritten as OSC 8 links with the short name as display text — automatically,
   with no manual `mdls` needed.
8. **Runs sanity tests** on the new shell config before declaring victory.

## Optional extras — what each one installs

| Extra | What you get |
|-------|-------------|
| MacDown 3000 + .md handler | Native split-view markdown editor that auto-refreshes on external file edits; registered as default `.md` opener |
| grip — live browser preview | `preview` alias → GitHub-flavoured localhost:6419 preview that reloads on save |
| mdwatch — live terminal re-render | `mdwatch` alias → `entr` + `glow -p` re-renders the terminal preview on every save |
| Clickable file paths | OSC 8 hyperlinks in Ghostty and other modern terminals; `mdls` and `o` shell aliases for manual use; **automatic Claude Code hook** that linkifies bare filenames in Bash tool output |

## Clickable file paths — two modes

**Automatic (Claude Code hook):** After install, every Bash tool result in Claude Code
is scanned for bare filenames with known extensions (`.md`, `.yaml`, `.py`, `.ts`,
etc.). Each one is resolved to an absolute path and rewritten as an OSC 8 hyperlink
with the short filename as display text. A bare `btt-ai-ways-of-working-faq.md` in
output becomes a short, clickable link — no full path printed.

**Manual (shell aliases):** Outside of Claude Code, use:
- `mdls [dir]` — list `.md` files in a directory as clickable terminal links
- `o <file>` — print a clickable link and open the file

Both modes use the same OSC 8 formatter at
`~/.claude/global-utils/clickable-paths/format-clickable-path.js` and work in Ghostty,
iTerm2, WezTerm, and VS Code's integrated terminal. They gracefully degrade to plain
text in unsupported terminals or when `FORCE_HYPERLINK` is not set.

## Known gotchas the skill handles for you

- This plugin uses **MacDown 3000** (cask `macdown-3000`), not the original
  MacDown. The original does not auto-refresh on external file edits — close and
  reopen the file is required — which breaks the "watch your agent edit live"
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
- `ghostty` is explicitly listed as a supported terminal in the OSC 8 formatter
  (v1.2.0+). Set `FORCE_HYPERLINK=1` before launching Claude Code to force OSC 8
  on any terminal.

## Troubleshooting

If something goes wrong, your original `~/.zshrc` is at `~/.zshrc.pre-oh-my-zsh`.
Restore with `mv ~/.zshrc.pre-oh-my-zsh ~/.zshrc && rm -rf ~/.oh-my-zsh`.

If the Claude Code hook was installed but filenames aren't linking, check that
`~/.claude/settings.json` contains a `PostToolUse > Bash` entry for
`post-bash-filename-links.py`, and that `~/.claude/global-utils/clickable-paths/format-clickable-path.js`
exists. Re-run `/terminal-setup-install` to repair either.

## Source material

- Blog post (with screenshots): [youngleaders.tech/p/terminal-setup-pdf-meta-guide](https://www.youngleaders.tech/p/terminal-setup-pdf-meta-guide)
- Original install guide PDF, FAQ PDF: see the blog post for credits.
