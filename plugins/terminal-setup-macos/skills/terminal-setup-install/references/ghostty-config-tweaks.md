# Ghostty opt-in config tweaks reference

(ghostty-terminal-improvements--2026-08-28, T-07/T-12) Confirmed fixes and community-survey
findings from Phase 1 research, offered as opt-in additions to `~/.config/ghostty/config` from
SKILL.md Step 6b - none of these are applied by default.

## Step 6b question bundles

Fire all four questions in a single `AskUserQuestion` call (multiSelect), then append the config
lines for every selected bundle to `~/.config/ghostty/config` per "Applying selected bundles"
below.

- **Question 1 - "Issue fixes"** (header "Issue fixes"):
  1. **Pane divider visibility + resize keybinds** (fix, config key) - dividers between splits
     are hard to see and resizing has no visible shortcut. Adds `split-divider-color` (hex or
     named colour), `unfocused-split-opacity` + `unfocused-split-fill` (dim inactive panes), and
     `keybind` entries for `resize_split:<direction>,<pixels>`, `equalize_splits`, and
     `goto_split:<next|previous|top|left|bottom|right>`.
  2. **Session persistence via tmux-resurrect** (workaround, third-party tool) - Ghostty has no
     native split-layout restore; this is the lightest-weight real option. See Step 10 - if
     picked, this is installed as a full extra (like grip/mdwatch), not just a config line.

- **Question 2 - "Appearance tweaks"** (header "Appearance"), 2 options (AskUserQuestion needs 2
  to 4 per question):
  1. **Cursor** - `cursor-style: block`, `cursor-style-blink`.
  2. **Window chrome** - `macos-titlebar-style: hidden`, `window-theme: system`.

  Theme, background and font are not offered here: Step 6 already sets them (Dracula, 0.98
  opacity with blur, MesloLGS NF at 16pt), and a bundle that only repeats them changes nothing.

- **Question 3 - "Behaviour tweaks"** (header "Behaviour"), up to 4 bundles:
  1. **Shell integration & cwd** - `shell-integration` (already set in Step 6), `window-inherit-working-directory`.
  2. **Mouse & selection** - `mouse-hide-while-typing`, `copy-on-select: clipboard`, `macos-option-as-alt: left`.
  3. **Window/session behaviour** - `confirm-close-surface: false`, `quick-terminal-size` (Ghostty
     1.2+).
  4. **Custom keybinds** (comment-only: adds a commented heading and no active lines, for you
     to fill in) - tmux-style pane/tab navigation `keybind` entries. No defaults ship because a
     tmux-style prefix such as `ctrl+b` set in Ghostty would never reach tmux.

- **Question 4 - "Performance tweaks"** (header "Performance"), 2 options: `window-vsync`,
  `resize-overlay: never`. Scrollback is not offered: Ghostty's 10 MB default is sensible, and
  raising it costs memory per pane, the opposite of a performance tweak.

If `AskUserQuestion` is unavailable, fall back to the same plain-text lettered-list pattern the
skill already uses elsewhere (see SKILL.md "What this skill does").

## Applying selected bundles (SKILL.md Step 10b)

For every bundle selected in Question 1's divider/resize option and Questions 2-4, append the
matching config lines below to `~/.config/ghostty/config` (use Edit, not a heredoc, to avoid
clobbering earlier Step 6 content). Only append the specific lines for bundles the user actually
selected - do not write the whole block unconditionally. Every line below has a working value
(colours match the Step 6 Dracula theme and its `#141026` background), and none of them repeats a
key Step 6 already wrote. Never write a `<placeholder>` onto an active line: Ghostty rejects it
and shows a "Configuration Errors" dialog on every launch.

After appending, run this one line. It finds Ghostty itself (`/Applications` or
`~/Applications`) and needs no variable from an earlier step:

```bash
G=/Applications/Ghostty.app/Contents/MacOS/ghostty; [ -x "$G" ] || G="$HOME/Applications/Ghostty.app/Contents/MacOS/ghostty"; [ -x "$G" ] || { echo "ghostty MISSING"; false; } && "$G" +validate-config
```

It must print nothing. `ghostty MISSING` means the app is not installed, not a bad line. Any
other output names a config line: fix or comment out that line and run it again before moving on.

```
# --- Issue fixes: Pane divider visibility + resize keybinds ---
split-divider-color = #6272a4
unfocused-split-opacity = 0.7
unfocused-split-fill = #141026
keybind = super+ctrl+shift+up=resize_split:up,10
keybind = super+ctrl+shift+equal=equalize_splits
keybind = super+ctrl+right_bracket=goto_split:next
keybind = super+ctrl+left_bracket=goto_split:previous

# --- Appearance: Cursor ---
cursor-style = block
cursor-style-blink = true

# --- Appearance: Window chrome ---
macos-titlebar-style = hidden
window-theme = system

# --- Behaviour: Shell integration & cwd ---
window-inherit-working-directory = true

# --- Behaviour: Mouse & selection ---
mouse-hide-while-typing = true
copy-on-select = clipboard
macos-option-as-alt = left

# --- Behaviour: Window/session behaviour ---
confirm-close-surface = false
quick-terminal-size = 40%

# --- Behaviour: Custom keybinds ---
# (comment-only bundle: no active lines; add your own keybind = ... lines here)

# --- Performance ---
window-vsync = true
resize-overlay = never
```
