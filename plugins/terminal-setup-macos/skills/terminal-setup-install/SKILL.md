---
name: terminal-setup-install
description: Idempotent macOS terminal installer for Ghostty, Oh My Zsh, Powerlevel10k, Glow, MesloLGS Nerd Font, plus optional markdown preview and clickable-path extras.
allowed-tools: [Bash, Read, Write, Edit, AskUserQuestion, TaskCreate, TaskUpdate, TaskGet, TaskList]
version: 1.5.0
category: Setup
tags: [terminal, macos, ghostty, ohmyzsh, powerlevel10k, glow, markdown, tmux]
last-updated: 2026-09-16
---

# terminal-setup-install

## When to auto-invoke

Auto-invoke when the user says any of:
- "set up my terminal", "install ghostty", "install oh my zsh", "set up p10k"
- "run the terminal setup guide", "install the meta-guide stack"
- "I want clickable file paths in my terminal", "install the markdown preview kit"

## When NOT to invoke

Do NOT invoke for:
- Editing `~/.zshrc` for unrelated reasons (use Edit directly)
- Adding individual zsh plugins (use `git clone` + Edit)
- Linux or Windows terminal setup (this is macOS-specific)
- Already-installed full stacks where the user just wants to tweak one thing

## What this skill does

If `AskUserQuestion` is unavailable (for example on OpenCode or Cowork), present the same extras
choice as a plain-text lettered list and continue from the user's written answer instead of
stopping.

**A note on the commands shown throughout this skill.** Every command below is shown as
`Raw terminal:` and `Claude Code:`. Typing it straight into a terminal prompt (Ghostty, Terminal.app,
etc.) is the `Raw terminal:` form. Typing it into a Claude Code session needs a leading `!` -
without it, the text goes to Claude as a chat message instead of running as a shell command. An
interactive wizard like `p10k configure` should always be run in a raw terminal - interactive
prompts don't render reliably through the `!` passthrough.

1. **Preflight & classify.** Detects what's already installed and classifies the run - full
   install, extras-only, or already-current - before any install step runs.
2. **Core install** in this exact order (sequential to avoid Homebrew portable-Ruby lock conflicts):
   1. Ghostty (cask)
   2. MesloLGS Nerd Font (cask)
   3. Glow (formula)
   4. Dracula theme for Ghostty (`git clone`)
   5. Ghostty config at `~/.config/ghostty/config`
   6. Oh My Zsh (curl installer with `RUNZSH=no KEEP_ZSHRC=no`)
   7. Powerlevel10k theme (`git clone` into custom themes)
   8. zsh-autosuggestions + fast-syntax-highlighting plugins
3. **Restore `.zshrc`.** OMZ overwrites `~/.zshrc`; the skill copies user customisations from `~/.zshrc.pre-oh-my-zsh` back into the new file (PATH exports, aliases, tool inits). SDKMAN goes at the very end.
4. **Set ZSH_THEME and plugins line:**
   - `ZSH_THEME="powerlevel10k/powerlevel10k"`
   - `plugins=(git brew macos zsh-autosuggestions fast-syntax-highlighting)`
   - `docker` plugin only if `docker` is on PATH
5. **AskUserQuestion** about optional markdown-preview extras (multi-select).
6. **Per-extra installs** for each chosen option.
7. **Sanity tests.** Run `zsh -i -c` checks for parse, claude alias (if present), tool inits.
8. **Hand off.** Tell the user to open Ghostty (Spotlight) and run `p10k configure` interactively.

## Task Tracking Protocol

(ghostty-terminal-improvements--2026-08-28, T-12) Create the full Step 1-12 chain before Step 1
runs, so progress survives a mid-run interruption:

```
t1  = TaskCreate("Step 1: Preflight")
t2  = TaskCreate("Step 2: Backup .zshrc")
t3  = TaskCreate("Step 3: Install Ghostty")
t4  = TaskCreate("Step 4: Install MesloLGS Nerd Font")
t5  = TaskCreate("Step 5: Install Glow")
t6  = TaskCreate("Step 6: Configure Ghostty")
t6b = TaskCreate("Step 6b: AskUserQuestion - optional Ghostty config tweaks")
t7  = TaskCreate("Step 7: Install Oh My Zsh + Powerlevel10k + plugins")
t8  = TaskCreate("Step 8: Restore .zshrc customisations")
t9  = TaskCreate("Step 9: AskUserQuestion - optional extras")
t10 = TaskCreate("Step 10: Per-extra installs")
t10b= TaskCreate("Step 10b: Apply selected Ghostty config-tweak bundles")
t11 = TaskCreate("Step 11: Sanity tests")
t12 = TaskCreate("Step 12: Hand off")

TaskUpdate(t2.id, addBlockedBy=[t1.id])
TaskUpdate(t3.id, addBlockedBy=[t2.id])
TaskUpdate(t4.id, addBlockedBy=[t3.id])
TaskUpdate(t5.id, addBlockedBy=[t4.id])
TaskUpdate(t6.id, addBlockedBy=[t5.id])
TaskUpdate(t6b.id, addBlockedBy=[t6.id])
TaskUpdate(t7.id, addBlockedBy=[t6b.id])
TaskUpdate(t8.id, addBlockedBy=[t7.id])
TaskUpdate(t9.id, addBlockedBy=[t8.id])
TaskUpdate(t10.id, addBlockedBy=[t9.id])
TaskUpdate(t10b.id, addBlockedBy=[t10.id])
TaskUpdate(t11.id, addBlockedBy=[t10b.id])
TaskUpdate(t12.id, addBlockedBy=[t11.id])
```

Mark each task `in_progress` on entry to its step and `completed` on exit. If Step 1 reports
everything already installed, mark Steps 2-5, 7, and 8 `completed` immediately (no-op) rather than
leaving them `pending` - matches the "nothing to install" shortcut Step 1 documents below. Steps
6b and 9 are NOT part of that shortcut - both are `AskUserQuestion` prompts for opt-in choices
independent of what's already installed, and always run.

## Step-by-step

### Step 1 - Preflight (classify what needs to run)

Detect what's already installed on this machine and classify the run: full install, extras-only,
or already-current. Everything downstream (which steps run, which are skipped) follows from this
classification, not from re-checking state ad hoc in later steps.

```bash
brew --version >/dev/null 2>&1 || { echo "Homebrew not installed; install it first: https://brew.sh"; exit 1; }
[ -d /Applications/Ghostty.app ] && GHOSTTY_INSTALLED=yes || GHOSTTY_INSTALLED=no
[ -d "$HOME/.oh-my-zsh" ] && OMZ_INSTALLED=yes || OMZ_INSTALLED=no
[ -d "$HOME/.oh-my-zsh/custom/themes/powerlevel10k" ] && P10K_INSTALLED=yes || P10K_INSTALLED=no
which glow >/dev/null 2>&1 && GLOW_INSTALLED=yes || GLOW_INSTALLED=no
ls "$HOME/Library/Fonts/" 2>/dev/null | grep -qi meslolgs && FONT_INSTALLED=yes || FONT_INSTALLED=no
# MacDown check - must be MacDown 3000 (the auto-refreshing fork), not the original MacDown
[ -d "/Applications/MacDown 3000.app" ] && MACDOWN3000_INSTALLED=yes || MACDOWN3000_INSTALLED=no
[ -d "/Applications/MacDown.app" ] && brew list --cask macdown >/dev/null 2>&1 && MACDOWN_ORIGINAL=yes || MACDOWN_ORIGINAL=no
```

Report each as a tick or "skip - already installed". If everything is already installed, skip
Steps 2-5, 7, and 8 (nothing to install or back up) - but still run **Step 6b** and **Step 9**.
Those two are `AskUserQuestion` prompts for opt-in choices (Ghostty config tweaks, markdown
extras) that apply regardless of whether the core stack already exists; they are not gated on this
shortcut.

**MacDown preflight rules:**
- MacDown 3000 installed → `✓ MacDown 3000 - skip`
- Original MacDown installed but NOT MacDown 3000 → `⚠️ MacDown (original) found - will replace with MacDown 3000 in Step 10`
- Neither installed → `○ MacDown 3000 - not installed`

Do NOT treat the original MacDown as equivalent to MacDown 3000. The original does not auto-refresh on external file edits and uses a different bundle ID (`com.uranusjr.macdown` vs `app.macdown.macdown3000`).

### Step 2 - Backup .zshrc

If `~/.zshrc` exists and `~/.zshrc.pre-oh-my-zsh` does not, the OMZ installer will create the backup itself. If `~/.zshrc.pre-oh-my-zsh` already exists from a prior run, leave it alone; the prior backup is more authoritative than the current `.zshrc`.

Read the current `~/.zshrc` end-to-end and capture every `export PATH=`, `alias`, `eval "$(...)"`, and `source` line. These need to be merged into the new file post-install.

### Step 3 - Install Ghostty

```bash
[ "$GHOSTTY_INSTALLED" = "no" ] && brew install --cask ghostty
```

### Step 4 - Install MesloLGS Nerd Font

```bash
[ "$FONT_INSTALLED" = "no" ] && brew install --cask font-meslo-lg-nerd-font
```

Run sequentially after Step 3. Parallel `brew install --cask` calls hit a Ruby lock and one will fail with "Another `brew vendor-install ruby` process is already running."

### Step 5 - Install Glow

```bash
[ "$GLOW_INSTALLED" = "no" ] && brew install glow
```

### Step 6 - Configure Ghostty

```bash
mkdir -p "$HOME/.config/ghostty/themes"
TEMP=$(mktemp -d)
git clone --depth=1 https://github.com/dracula/ghostty.git "$TEMP/d"
cp "$TEMP/d/dracula" "$HOME/.config/ghostty/themes/"
rm -rf "$TEMP"
```

Then write `~/.config/ghostty/config` (use the Write tool, not heredocs):

```
theme = dracula
background = #141026
background-opacity = 0.98
background-blur = true
working-directory = ~/Projects

font-family = "MesloLGS NF"
font-size = 16
font-feature = -liga
font-thicken = true

window-padding-x = 10
window-padding-y = 10

shell-integration = zsh
```

**Critical:** `shell-integration` must be a shell name (`zsh`, `bash`, `fish`), NOT `true`. The latter triggers a Configuration Errors dialog when Ghostty starts.

Before this step, use `AskUserQuestion` (header "Working dir"; recommended option "Use ~/Projects (default)"; other option "Something else" - the tool's free-text fallback covers a custom path) to confirm the `working-directory` value rather than assuming the default.

### Step 6b - AskUserQuestion: optional Ghostty config tweaks

(ghostty-terminal-improvements--2026-08-28, T-07) Confirmed fixes and community-survey findings
from Phase 1 research, offered as opt-in additions to `~/.config/ghostty/config` - none of these
are applied by default. Fire 4 questions (Issue fixes / Appearance / Behaviour / Performance) in
a single `AskUserQuestion` call (multiSelect); full question text and every config key is in
`references/ghostty-config-tweaks.md`. Then append the config lines for every selected bundle to
`~/.config/ghostty/config` in Step 10b (same reference file has the exact lines to apply).

If `AskUserQuestion` is unavailable, fall back to the same plain-text lettered-list pattern the
skill already uses elsewhere (see "What this skill does" above).

### Step 7 - Install Oh My Zsh + Powerlevel10k + plugins

```bash
RUNZSH=no KEEP_ZSHRC=no sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

CUSTOM="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "$CUSTOM/themes/powerlevel10k"
git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions.git "$CUSTOM/plugins/zsh-autosuggestions"
git clone --depth=1 https://github.com/zdharma-continuum/fast-syntax-highlighting.git "$CUSTOM/plugins/fast-syntax-highlighting"
```

`RUNZSH=no` stops the OMZ installer from spawning a child zsh that blocks scripted flows. `KEEP_ZSHRC=no` lets it back up and replace `~/.zshrc`.

### Step 8 - Restore .zshrc customisations

Edit the new `~/.zshrc` to:

1. Replace `ZSH_THEME="robbyrussell"` with `ZSH_THEME="powerlevel10k/powerlevel10k"`.
2. Replace `plugins=(git)` with `plugins=(git brew macos zsh-autosuggestions fast-syntax-highlighting)` (add `docker` only if `which docker` returns a path).
3. After the `# Example aliases` block, append every customisation captured in Step 2, in this order:
   - PATH exports (claude, .local, claude-code-docs, etc.)
   - bun init block
   - Other tool inits (nvm, pyenv, rbenv) EXCEPT SDKMAN
   - User aliases
4. **At the very end of the file**, append the SDKMAN init. The SDKMAN installer is explicit: it must be the last `PATH`-mutating init. Place a marker comment for clarity:

```bash
# === SDKMAN MUST BE AT THE END OF THE FILE ===
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$SDKMAN_DIR/bin/sdkman-init.sh" ]] && source "$SDKMAN_DIR/bin/sdkman-init.sh"
```

### Step 9 - AskUserQuestion: optional extras

Use this exact AskUserQuestion (multi-select):

- **Question:** "Which optional markdown-preview extras would you like installed?"
- **Header:** "MD extras"
- **multiSelect:** `true`
- **Options:**
  1. **MacDown 3000 + .md handler** - Native macOS split-view markdown editor (notarised fork of MacDown that auto-refreshes when the file is changed externally). After install, double-clicking any .md in Finder opens it. Screenshots and details: `https://www.youngleaders.tech/i/196949342/macdown-3000`
  2. **grip - live browser preview** - Serves a GitHub-flavoured preview at localhost:6419 and auto-reloads on save. Screenshots and details: `https://www.youngleaders.tech/i/196949342/grip`
  3. **mdwatch - live terminal re-render** - Pairs entr with glow -p so the terminal preview re-renders the moment you save. Screenshots and details: `https://www.youngleaders.tech/i/196949342/mdwatch`
  4. **Clickable file paths (mdls + o)** - manual `mdls`/`o` zsh aliases for Cmd-clickable OSC 8 links. The automatic version (every bare filename in Bash output becomes clickable, no alias needed) is not part of this choice - it ships as the plugin's own hook and is always on while `terminal-setup-macos` is enabled. Screenshots and details: `https://www.youngleaders.tech/i/196949342/clickable-paths`


### Step 10 - Per-extra installs

If user picked **MacDown 3000 + .md handler**:

Why MacDown 3000 instead of the original MacDown: the original does not refresh
its preview when the file is changed by an external process (e.g. an agent
editing the file while MacDown has it open). You have to close and reopen the
file to see changes. MacDown 3000 (notarised fork by Schuyler Erle, MIT,
official Homebrew cask) refreshes live. Same look and feel, fixes the one
limitation that matters.

The casks conflict, so uninstall the original first if it's there:

```bash
brew list --cask macdown >/dev/null 2>&1 && brew uninstall --cask macdown
brew install --cask macdown-3000
brew install duti
# Launch MacDown 3000 once so LaunchServices registers its bundle ID
open -g "/Applications/MacDown 3000.app"
sleep 2
osascript -e 'tell application "MacDown 3000" to quit' 2>/dev/null || true
# Bundle ID for MacDown 3000 (different from the original MacDown):
duti -s app.macdown.macdown3000 .md all
duti -s app.macdown.macdown3000 .markdown all
duti -x md   # verify
```

If a phantom `com.uranusjr.macdown` or `io.macdown.MacDown` registration is
cached from an older install, rebuild LaunchServices:

```bash
/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister -r -domain local -domain system -domain user
/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister "/Applications/MacDown 3000.app"
duti -s app.macdown.macdown3000 .md all
```

If user picked **grip**:

```bash
brew install grip
```

Append to `~/.zshrc`:

```bash
alias preview="grip"
```

Usage after install:

```
Raw terminal:  preview
Claude Code:   !preview
```

If user picked **mdwatch**:

```bash
brew install entr
```

Append to `~/.zshrc`:

```bash
alias mdwatch='f() { echo "$1" | entr -c glow -p "$1" }; f'
```

Usage after install:

```
Raw terminal:  mdwatch somefile.md
Claude Code:   !mdwatch somefile.md
```

If user picked **Session persistence via tmux-resurrect** (Step 6b, Question 1):

```bash
which tmux >/dev/null 2>&1 || brew install tmux
CUSTOM_TMUX="$HOME/.tmux/plugins"
mkdir -p "$CUSTOM_TMUX"
git clone --depth=1 https://github.com/tmux-plugins/tmux-resurrect "$CUSTOM_TMUX/tmux-resurrect"
git clone --depth=1 https://github.com/tmux-plugins/tmux-continuum "$CUSTOM_TMUX/tmux-continuum"
```

**What "prefix" means** (ghostty-terminal-improvements--2026-08-28, T-16): tmux commands aren't
typed - they're triggered by a two-key combo. You press the "prefix" key first (a signal to tmux
that the next keystroke is a tmux command, not something to send to the running program), release
it, then press the command key. tmux's own default prefix is `Ctrl-b`, which is awkward to reach
one-handed - a lot of people remap it to `Ctrl-a` instead. `tmux-resurrect` uses whatever prefix is
currently set: save is `prefix` then `Ctrl-s`, restore is `prefix` then `Ctrl-r` (e.g. with the
default prefix: `Ctrl-b`, release, `Ctrl-s`).

Before writing `~/.tmux.conf`, use `AskUserQuestion` (header "tmux prefix"):
- **Keep default (`Ctrl-b`)** (recommended) - no config change, matches tmux's out-of-the-box behaviour and most online tmux guides.
- **Remap to `Ctrl-a`** - common alternative, easier to reach with one hand, closer to screen's default prefix if migrating from screen.
- **Something else** (free text) - the tool's free-text fallback covers a custom key.

If the user picks a remap, prepend these lines to `~/.tmux.conf` (before the resurrect/continuum
lines below, so the prefix is set before the plugins load):

```
set -g prefix C-a
unbind C-b
bind C-a send-prefix
```

(substitute the chosen key for `C-a` if "something else" was picked). Append to `~/.tmux.conf`
(create if absent):

```
run-shell ~/.tmux/plugins/tmux-resurrect/resurrect.tmux
set -g @continuum-restore 'on'
run-shell ~/.tmux/plugins/tmux-continuum/continuum.tmux
```

`tmux-continuum` auto-saves every 15 minutes and auto-restores on tmux server start, so the
prefix+Ctrl-s/Ctrl-r keys above are for a manual save/restore on demand. This is a third-party
workaround, not a native Ghostty feature - Ghostty's own `window-save-state` is macOS-only and
does not reliably restore split-pane layout (T-02 finding).

Starting and using tmux itself is a raw-terminal-only workflow (tmux is its own interactive
program, not something the `!` passthrough runs sensibly):

```
Raw terminal:  tmux                      (starts a new tmux session)
Raw terminal:  <prefix> then Ctrl-s      (save the session)
Raw terminal:  <prefix> then Ctrl-r      (restore the session)
```

If user picked **Clickable file paths**:

**Step A - Install the OSC 8 formatter utility:**

```bash
mkdir -p "$HOME/.claude/global-utils/clickable-paths"
SKILL_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
# Copy the bundled (fixed) formatter - includes Ghostty + FORCE_HYPERLINK support
cp "$SKILL_DIR/../../scripts/global-utils/format-clickable-path.js" \
   "$HOME/.claude/global-utils/clickable-paths/format-clickable-path.js"
```

If the script location can't be determined, fall back to checking whether `~/.claude/global-utils/clickable-paths/format-clickable-path.js` already exists. If absent in both cases, warn the user and offer to skip.

**Step B - none needed.** The Bash PostToolUse hook that makes bare filenames clickable is declared
in the plugin's own `hooks/hooks.json` (`${CLAUDE_PLUGIN_ROOT}/scripts/post-bash-filename-links.py`)
and is registered automatically whenever `terminal-setup-macos` is enabled - it applies to every
user of the plugin, not only users who pick this extra, and it deregisters cleanly if the plugin is
disabled. There is nothing to copy into `~/.claude/hooks/` or patch into `~/.claude/settings.json`.
(ghostty-terminal-improvements--2026-08-28, T-15: a prior version of this skill copied the hook
script to `~/.claude/hooks/` and hand-patched the user's global `settings.json` - if the plugin was
then disabled, the copied script and the settings.json entry both stayed behind and kept running.)

**Step C - Add zsh aliases for manual use:**

Append to `~/.zshrc`:

```bash
mdls() {
  local dir="${1:-.}"
  local util="$HOME/.claude/global-utils/clickable-paths/format-clickable-path.js"
  if [[ ! -f "$util" ]]; then
    echo "format-clickable-path.js not found at $util" >&2
    return 1
  fi
  for f in "$dir"/*.md(N); do
    node -e "console.log(require('$util').formatClickablePathSafe('$(realpath "$f")'));"
  done
}

o() {
  if [[ -z "$1" ]]; then echo "usage: o <file>" >&2; return 1; fi
  local util="$HOME/.claude/global-utils/clickable-paths/format-clickable-path.js"
  local abs="$(realpath "$1" 2>/dev/null || echo "$1")"
  if [[ -f "$util" ]]; then
    node -e "console.log(require('$util').formatClickablePathSafe('$abs'));"
  else
    echo "$abs"
  fi
  open "$abs"
}
```

Usage after install:

```
Raw terminal:  mdls docs/workflows/       Claude Code:  !mdls docs/workflows/
Raw terminal:  o somefile.md              Claude Code:  !o somefile.md
```

**How the two approaches differ:**
- **Hook** (plugin-native, always on): every Bash tool call in Claude Code scans stdout for bare filenames and makes them clickable without any manual action. Not gated on this Step 9 choice at all - see "Step B - none needed" above.
- **`mdls`/`o` aliases** (Step C, gated on this choice): manual - run `mdls docs/workflows/` or `o somefile.md` explicitly in a terminal

### Step 10b - Apply selected Ghostty config-tweak bundles

For every bundle selected in Step 6b, append the matching config lines to
`~/.config/ghostty/config` (use Edit, not a heredoc, to avoid clobbering earlier Step 6 content).
The exact config block for every bundle - Issue fixes, Appearance, Behaviour, Performance - is in
`references/ghostty-config-tweaks.md` under "Applying selected bundles". Only append the lines
for bundles the user actually selected; comment out or omit any line needing a user-specific
value (theme names, shader path) and ask via free text if the user wants it filled in now.

### Step 11 - Sanity tests

```bash
zsh -i -c 'echo OK'
zsh -i -c 'type p10k >/dev/null && echo "p10k OK" || echo "p10k MISSING"'
zsh -i -c 'glow --version'
# If user has SDKMAN:
[ -d "$HOME/.sdkman" ] && zsh -i -c 'type sdk >/dev/null && echo "sdk OK" || echo "sdk MISSING"'
```

### Step 12 - Hand off

Tell the user:

> 1. Open Ghostty (Spotlight, type "Ghostty"). It should start in dracula theme with the Nerd Font.
> 2. Run `p10k configure` in that Ghostty window - interactive wizard for prompt style, character
>    set, colours, icons, git status, time display. This one is raw-terminal-only; an interactive
>    wizard doesn't work through Claude Code's `!` passthrough.
> 3. If icons render as boxes or `?`: Cmd+Q out of Ghostty and reopen. New tabs alone don't reload the font.
> 4. Optional smoke tests - both work equally well from either place:
>    - `glow README.md` (raw terminal) or `!glow README.md` (Claude Code)
>    - Type `gi` at a raw terminal prompt and pause - autosuggestions should offer to complete it
>      (this one only makes sense typed live at a prompt, not via `!`)
>    - `cd ` then start typing a directory name at a raw terminal prompt - tab-completion should
>      highlight as you type (same - live-typing only)

## Known gotchas (encoded in this skill)

| Gotcha | Encoded behaviour |
|---|---|
| Parallel `brew install --cask` hits Ruby lock | Installs run sequentially |
| Original MacDown does not auto-refresh on external file edits | Skill installs MacDown 3000 (notarised fork) which does |
| Original `macdown` cask conflicts with `macdown-3000` | Skill uninstalls the original first when present |
| MacDown 3000 bundle ID is `app.macdown.macdown3000` (not `com.uranusjr.macdown`) | Skill uses the new ID for `duti` |
| Phantom LaunchServices entry from older MacDown installs | Skill rebuilds LS database when needed |
| `shell-integration = true` triggers Ghostty config error | Skill writes `shell-integration = zsh` |
| OMZ overwrites `~/.zshrc` and loses customisations | Skill captures customisations Step 2, restores Step 8 |
| SDKMAN must be last in `~/.zshrc` | Skill places SDKMAN init at end with marker comment |
| `docker` plugin warns when docker not installed | Skill conditionally adds `docker` to plugins line |
| New tabs don't reload Ghostty font | Skill instructs user to fully Cmd+Q and reopen |
| Powerlevel10k wizard needs interactive input | Skill installs theme then hands off to user for `p10k configure` |
| A clickable OSC 8 link's display text wraps across a terminal line break and loses grouping | `format-clickable-path.js` and `post-bash-filename-links.py` set an `id=` param on the OSC 8 link so wrapped text still resolves as one logical hyperlink (ghostty-terminal-improvements--2026-08-28, T-01/T-07) |

## Known limitations (investigated, not fixable at config level)

(ghostty-terminal-improvements--2026-08-28, Phase 1)

- **Claude Code statusline truncation on narrow windows**: not a Ghostty config issue - root cause
  is in Claude Code itself. Multi-line custom statuslines get truncated on narrow terminals; no
  scroll/config workaround exists. Closed "not planned" by Anthropic
  ([#26371](https://github.com/anthropics/claude-code/issues/26371),
  [#28750](https://github.com/anthropics/claude-code/issues/28750)). Mitigation: keep custom
  statuslines to a single line, or widen the terminal past ~100 columns.
- **Full-screen feature breaking mouse clicks**: ruled out within a 20-minute timebox - no
  changelog entry found for the reported date. `cursor-click-to-move` is the most plausible
  candidate for "mouse clicks behave unexpectedly" reports but wasn't confirmed as the cause and
  is not applied automatically. If you hit this, try `cursor-click-to-move = false` manually.

## Failure modes

- **Homebrew not installed**: Abort with link to brew.sh.
- **Already-installed core stack, just want extras**: Skip Steps 3-8 entirely, jump straight to Step 9.
- **Custom `~/.zshrc` is too unusual to safely re-merge**: Surface the captured customisations to the user as a diff and ask them to confirm before applying.
- **MacDown 3000 registration fails after LS rebuild**: Tell user to manually open MacDown 3000 once via Spotlight, then re-run the skill from Step 10 onwards.
- **`format-clickable-path.js` missing for the OSC 8 option**: Skip with a clear message; do not add `mdls`/`o` aliases that will error out.

## See also

- The companion blog post (with screenshots): the meta-guide that taught this pattern.
- The original install PDF and FAQ PDF (April 2026 guide; this skill encodes both their happy paths and their bugs).
