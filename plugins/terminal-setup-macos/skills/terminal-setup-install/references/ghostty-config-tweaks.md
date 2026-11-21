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

- **Question 2 - "Appearance tweaks"** (header "Appearance"), up to 4 bundles from the T-06
  community survey:
  1. **Theme & colour overrides** - `theme` (light:X,dark:Y pair syntax supported), custom
     `background`/`foreground` hex.
  2. **Background effects** - `background-opacity` (~0.80-0.85 typical), `background-blur`,
     `custom-shader` (GLSL CRT/cursor-trail effects; can silently break `background-opacity` if
     the shader draws over the background - [GH Discussion #4835](https://github.com/ghostty-org/ghostty/discussions/4835)).
  3. **Font tuning** - `font-family`/`font-size` (14-16pt common), `font-thicken`/
     `font-thicken-strength`, `adjust-cell-height`.
  4. **Cursor & window chrome** - `cursor-style`/`cursor-style-blink`/`adjust-cursor-thickness`,
     `macos-titlebar-style: hidden`, `window-theme: system`.

- **Question 3 - "Behaviour tweaks"** (header "Behaviour"), up to 4 bundles:
  1. **Shell integration & cwd** - `shell-integration` (already set in Step 6), `window-inherit-working-directory`.
  2. **Mouse & selection** - `mouse-hide-while-typing`, `copy-on-select: clipboard`, `macos-option-as-alt: left`.
  3. **Window/session behaviour** - `confirm-close-surface: false`, `quick-terminal-size` (Ghostty
     1.2+), `command` (launch straight into tmux).
  4. **Custom keybinds** - tmux-style pane/tab navigation `keybind` entries.

- **Question 4 - "Performance tweaks"** (header "Performance"), up to 3 options (no bundling
  needed - fits the 4-option cap directly): `window-vsync`, `scrollback-limit`, `resize-overlay: never`.

If `AskUserQuestion` is unavailable, fall back to the same plain-text lettered-list pattern the
skill already uses elsewhere (see SKILL.md "What this skill does").

## Applying selected bundles (SKILL.md Step 10b)

For every bundle selected in Question 1's divider/resize option and Questions 2-4, append the
matching config lines below to `~/.config/ghostty/config` (use Edit, not a heredoc, to avoid
clobbering earlier Step 6 content). Only append the specific lines for bundles the user actually
selected - do not write the whole block unconditionally. Every active line below has a working value (Dracula colours, to match the Step 6 theme). Lines
that need a user-specific choice (a light theme name, a shader path) stay commented out; ask via
free text if the user wants one filled in now. Never write a `<placeholder>` onto an active line:
Ghostty rejects it and shows a "Configuration Errors" dialog on every launch.

After appending, run `/Applications/Ghostty.app/Contents/MacOS/ghostty +validate-config`. It must print nothing. If it names a line,
fix or comment out that line and run it again before moving on.

```
# --- Issue fixes: Pane divider visibility + resize keybinds ---
split-divider-color = #6272a4
unfocused-split-opacity = 0.7
unfocused-split-fill = #282a36
keybind = super+ctrl+shift+up=resize_split:up,10
keybind = super+ctrl+shift+equal=equalize_splits
keybind = super+ctrl+right_bracket=goto_split:next
keybind = super+ctrl+left_bracket=goto_split:previous

# --- Appearance: Theme & colour overrides ---
theme = dracula
# Light and dark pair instead (names from `ghostty +list-themes`):
# theme = light:<light theme>,dark:dracula
# background = #hex
# foreground = #hex

# --- Appearance: Background effects ---
background-opacity = 0.85
background-blur = true
# custom-shader = <path-to-shader.glsl>

# --- Appearance: Font tuning ---
font-family = "MesloLGS NF"
font-size = 15
font-thicken = true
# adjust-cell-height = 0

# --- Appearance: Cursor & window chrome ---
cursor-style = block
cursor-style-blink = true
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
# (tmux-style pane/tab navigation - fill in to taste)

# --- Performance ---
window-vsync = true
scrollback-limit = 10000
resize-overlay = never
```
