---
name: terminal-setup-install
description: Idempotent macOS terminal installer for Ghostty, Oh My Zsh, Powerlevel10k, Glow, MesloLGS Nerd Font, plus optional markdown-preview kit (MacDown 3000, grip, entr, OSC 8 paths). Auto-invoke when user is setting up a Mac terminal stack from scratch or running the meta-guide install flow.
allowed-tools: [Bash, Read, Write, Edit, AskUserQuestion]
version: 1.1.0
category: Setup
tags: [terminal, macos, ghostty, ohmyzsh, powerlevel10k, glow, markdown]
last-updated: 2026-05-10
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

1. **Preflight.** Detects what's already installed and skips it.
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

## Step-by-step

### Step 1 - Preflight

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

Report each as a tick or "skip - already installed". If everything is already installed, skip to Step 8 (extras).

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

Ask the user before this step if they want a different `working-directory` (default `~/Projects`).

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
  4. **Clickable file paths (mdls + o)** - OSC 8 hyperlinks in any modern terminal; mdls lists .md files as Cmd-clickable links. Screenshots and details: `https://www.youngleaders.tech/i/196949342/clickable-paths`


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

If user picked **mdwatch**:

```bash
brew install entr
```

Append to `~/.zshrc`:

```bash
alias mdwatch='f() { echo "$1" | entr -c glow -p "$1" }; f'
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

**Step B - Install the Claude Code PostToolUse hook:**

This hook makes bare filenames in Bash tool output clickable automatically - no manual `mdls` needed.

```bash
# Copy the hook script
cp "$SKILL_DIR/../../scripts/post-bash-filename-links.py" \
   "$HOME/.claude/hooks/post-bash-filename-links.py"
```

Then patch `~/.claude/settings.json` to wire up the hook. Use Python to read/write so JSON stays valid:

```python
import json, os

settings_path = os.path.expanduser('~/.claude/settings.json')

# Load existing settings (create minimal structure if missing)
if os.path.exists(settings_path):
    with open(settings_path) as f:
        settings = json.load(f)
else:
    settings = {}

settings.setdefault('hooks', {})
settings['hooks'].setdefault('PostToolUse', [])

# Find or create the Bash PostToolUse entry
bash_entry = next(
    (e for e in settings['hooks']['PostToolUse'] if e.get('matcher') == 'Bash'),
    None
)
if bash_entry is None:
    bash_entry = {'matcher': 'Bash', 'hooks': []}
    settings['hooks']['PostToolUse'].append(bash_entry)

bash_entry.setdefault('hooks', [])

new_hook = {
    'type': 'command',
    'command': 'python3 ~/.claude/hooks/post-bash-filename-links.py',
    'timeout': 8
}

# Idempotent - don't add twice
already = any('post-bash-filename-links' in h.get('command', '')
               for h in bash_entry['hooks'])
if not already:
    bash_entry['hooks'].append(new_hook)
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=4)
    print('✓ Claude Code hook wired up in ~/.claude/settings.json')
else:
    print('✓ Claude Code hook already present - skipped')
```

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

**How the two approaches differ:**
- **Hook** (Step B): automatic - every Bash tool call in Claude Code scans stdout for bare filenames and makes them clickable without any manual action
- **`mdls`/`o` aliases** (Step C): manual - run `mdls docs/workflows/` or `o somefile.md` explicitly in a terminal

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
> 2. Run `p10k configure` - interactive wizard for prompt style, character set, colours, icons, git status, time display.
> 3. If icons render as boxes or `?`: Cmd+Q out of Ghostty and reopen. New tabs alone don't reload the font.
> 4. Optional smoke tests: `glow README.md`, type `gi` (autosuggestions kick in), `cd ` then a dir name (highlighting).

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

## Failure modes

- **Homebrew not installed**: Abort with link to brew.sh.
- **Already-installed core stack, just want extras**: Skip Steps 3-8 entirely, jump straight to Step 9.
- **Custom `~/.zshrc` is too unusual to safely re-merge**: Surface the captured customisations to the user as a diff and ask them to confirm before applying.
- **MacDown 3000 registration fails after LS rebuild**: Tell user to manually open MacDown 3000 once via Spotlight, then re-run the skill from Step 10 onwards.
- **`format-clickable-path.js` missing for the OSC 8 option**: Skip with a clear message; do not add `mdls`/`o` aliases that will error out.

## See also

- The companion blog post (with screenshots): the meta-guide that taught this pattern.
- The original install PDF and FAQ PDF (April 2026 internal Toast guide; this skill encodes both their happy paths and their bugs).
