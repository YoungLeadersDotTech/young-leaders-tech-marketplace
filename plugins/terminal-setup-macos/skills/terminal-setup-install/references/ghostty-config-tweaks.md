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
  1. **Theme & colour overrides** (asks one follow-up) - follow the system light or dark mode
     with a `light:X,dark:Y` theme pair. Default pair: `light:GitHub Light Default,dark:dracula`.
  2. **Background effects** (asks one follow-up) - a see-through terminal: `background-opacity`
     (Step 6 writes 0.98; default here 0.85). `custom-shader` (GLSL CRT/cursor-trail effects) stays
     a commented line because it can silently break `background-opacity` if the shader draws over
     the background - [GH Discussion #4835](https://github.com/ghostty-org/ghostty/discussions/4835).
  3. **Font tuning** (asks one follow-up) - `font-size` (Step 6 writes 16; 14-18pt common) and
     extra line spacing via `adjust-cell-height` (default 10%).
  4. **Cursor & window chrome** - `cursor-style`/`cursor-style-blink`/`adjust-cursor-thickness`,
     `macos-titlebar-style: hidden`, `window-theme: system`.

- **Question 3 - "Behaviour tweaks"** (header "Behaviour"), up to 4 bundles:
  1. **Shell integration & cwd** - `shell-integration` (already set in Step 6), `window-inherit-working-directory`.
  2. **Mouse & selection** - `mouse-hide-while-typing`, `copy-on-select: clipboard`, `macos-option-as-alt: left`.
  3. **Window/session behaviour** - `confirm-close-surface: false`, `quick-terminal-size` (Ghostty
     1.2+), `command` (launch straight into tmux).
  4. **Custom keybinds** (comment-only: adds a commented heading and no active lines, for you
     to fill in) - tmux-style pane/tab navigation `keybind` entries. No defaults ship because a
     tmux-style prefix such as `ctrl+b` set in Ghostty would never reach tmux.

- **Question 4 - "Performance tweaks"** (header "Performance"), up to 3 options (no bundling
  needed - fits the 4-option cap directly): `window-vsync`, `scrollback-limit` (raised to 100 MB
  of history, ten times Ghostty's 10 MB default), `resize-overlay: never`.

**Follow-ups for the three Appearance bundles that take a value.** After the four questions,
for each of Theme, Background effects and Font tuning that was ticked, ask one free-text
question that states its default, for example "Opacity for the see-through background, from 0.5
to 1? Press enter for 0.85." An empty answer takes the default. If the user wants no more
questions, use the defaults. Never write the Step 6 value back as the bundle's "change": a
ticked bundle must change something.

If `AskUserQuestion` is unavailable, fall back to the same plain-text lettered-list pattern the
skill already uses elsewhere (see SKILL.md "What this skill does").

## Applying selected bundles (SKILL.md Step 10b)

For every bundle selected in Question 1's divider/resize option and Questions 2-4, append the
matching config lines below to `~/.config/ghostty/config` (use Edit, not a heredoc, to avoid
clobbering earlier Step 6 content). Only append the specific lines for bundles the user actually
selected - do not write the whole block unconditionally. Every active line below has a working
value (Dracula colours, to match the Step 6 theme). The three lines marked `# answer:` take the
user's follow-up answer, or the default shown. A bundle never repeats a key Step 6 already wrote
with the same value: that would look like a change and do nothing. A shader path stays commented
out. Never write a `<placeholder>` onto an active line: Ghostty rejects it and shows a
"Configuration Errors" dialog on every launch.

For the Theme pair, also comment out Step 6's `background = #141026` line, or the light theme
keeps the dark background. Theme names come from
`/Applications/Ghostty.app/Contents/MacOS/ghostty +list-themes` (a Homebrew cask install does not
put `ghostty` on PATH).

After appending, run `/Applications/Ghostty.app/Contents/MacOS/ghostty +validate-config`. It
must print nothing. If it names a line, fix or comment out that line and run it again before
moving on.

```
# --- Issue fixes: Pane divider visibility + resize keybinds ---
split-divider-color = #6272a4
unfocused-split-opacity = 0.7
unfocused-split-fill = #141026
keybind = super+ctrl+shift+up=resize_split:up,10
keybind = super+ctrl+shift+equal=equalize_splits
keybind = super+ctrl+right_bracket=goto_split:next
keybind = super+ctrl+left_bracket=goto_split:previous

# --- Appearance: Theme & colour overrides ---
# answer: the theme pair (also comment out Step 6's background line)
theme = light:GitHub Light Default,dark:dracula

# --- Appearance: Background effects ---
# answer: the opacity, 0.5 to 1
background-opacity = 0.85
# custom-shader = <path-to-shader.glsl>

# --- Appearance: Font tuning ---
# answer: the font size
font-size = 16
adjust-cell-height = 10%

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
# (comment-only bundle: no active lines; add your own keybind = ... lines here)

# --- Performance ---
window-vsync = true
scrollback-limit = 100000000
resize-overlay = never
```
