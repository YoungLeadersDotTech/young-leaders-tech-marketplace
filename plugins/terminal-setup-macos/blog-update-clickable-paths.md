# Blog update — Clickable paths section (v1.2.0)

Replace the entire **"Clickable paths"** section (from the `### Clickable paths`
heading down to, but not including, the `* * *` divider before Troubleshooting)
with the text below.

---

### Clickable paths

> _Screenshot: a list of short .md filenames in a Bash tool result inside Claude Code — each one underlined and Cmd-clickable._

Two modes, both using the same OSC 8 formatter at
`~/.claude/global-utils/clickable-paths/format-clickable-path.js`.

---

**Mode 1: automatic (Claude Code hook)**

This is the new thing in v1.2.0. When you pick this extra, the installer drops a
PostToolUse hook into `~/.claude/hooks/` and wires it into `~/.claude/settings.json`.
After that, every Bash tool result in Claude Code is scanned for bare filenames with
known extensions (`.md`, `.yaml`, `.py`, `.ts`, `.json`, and more). Each one is
resolved to an absolute path and rewritten as an OSC 8 hyperlink — but the short
filename is the display text. So when Claude prints a summary table that says
`btt-ai-ways-of-working-faq.md`, that's what you see: the short name, Cmd-clickable,
no full path needed.

Nothing to type. It just works.

---

**Mode 2: manual (shell aliases)**

For use outside of Claude Code — in a plain terminal session. Add to `~/.zshrc`:

```zsh
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

Usage:

```
mdls            # list .md in current dir as clickable links
mdls ~/docs     # same, but in a specific dir
o README.md     # print clickable link + open in MacDown 3000
```

---

**Terminal support**

Works in Ghostty (explicitly supported from v1.2.0), iTerm2, WezTerm, and VS Code's
integrated terminal. Falls back gracefully to plain text in terminals that don't support
OSC 8 — no visual corruption. Set `FORCE_HYPERLINK=1` before launching Claude Code to
force OSC 8 on any terminal.

Best for: terminal-heavy workflows where you want to jump straight to a file without the copy-paste-open dance — and for Claude Code users who want filenames in agent output to be first-class clickable links.
