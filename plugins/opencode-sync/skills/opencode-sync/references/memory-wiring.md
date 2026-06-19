# Memory Wiring - what OpenCode gets from `--wire-memory`

What the Claude memory-os hooks inject today, what `opencode-sync --wire-memory`
reproduces on OpenCode, and what still remains outside opencode-sync.

## Claude memory-os behaviour today

Memory-os currently splits the read path across two Claude hooks:

### SessionStart hook

`session-start-init-memory-prompt.sh` fires once per session when
`~/.claude/memory/` is absent or empty. It emits a consent banner explaining what
`/toast-memory-os:init-memory` would create.

What it does:

- one-shot per session via `/tmp/memory-os-init-prompt-<PPID>`
- checks whether `~/.claude/memory/` contains any markdown files
- if not, emits an init banner and plugin homepage link

This is an onboarding prompt, not memory injection.

### PreToolUse hook

`pre-tool-memory.sh` plus `pre-tool-memory.py` inject the actual memory context.

What it does:

- first tool call of the process context, then refresh every 30 minutes
- repo-root `MEMORY.md` first, if present
- otherwise `~/.claude/projects/<mapped-project>/memory/MEMORY.md`
- global memory index appended after project memory
- lock + flag files to avoid double injection under parallel tool calls

The Python hook currently emits:

1. project memory (repo root first, scratch-path second)
2. global memory index (`~/.claude/memory/memory.md`)

## What `--wire-memory` reproduces on OpenCode

When you pass `--wire-memory`, opencode-sync writes an `instructions` array into the
generated OpenCode config.

Current behaviour:

- if the source repo tracks `MEMORY.md` at its root, include `MEMORY.md` first
- always include `AGENTS.md`
- always include `~/.claude/memory/memory.md`

So the practical read order becomes:

1. repo-root `MEMORY.md` (when tracked)
2. `AGENTS.md`
3. global memory index

This is the safest portable approximation because:

- `MEMORY.md` in the repo is portable across machines and branches
- `AGENTS.md` is already a native OpenCode auto-read surface
- the global memory index path is stable under `~/`

## What it does NOT reproduce

`--wire-memory` is not a full replacement for memory-os hooks.

Still missing:

- the SessionStart init banner when the global memory corpus is empty
- 30-minute re-injection / refresh behaviour
- auto-loading the scratch-path project memory at
  `~/.claude/projects/<mapped-project>/memory/MEMORY.md`
- lock / flag coordination across parallel tool calls
- PreToolUse-style injection after changing working directories inside the same app session

## Why the scratch-path memory is not wired directly

The scratch-path memory location depends on the local absolute checkout path:

`/Users/alice/Projects/foo` -> `~/.claude/projects/-Users-alice-Projects-foo/memory/MEMORY.md`

That mapping is user- and machine-specific. Baking it into a committed project config would
either be wrong on another machine or leak local path shape into public config.

## Operational guidance

- If a repo tracks `MEMORY.md` at its root, `--wire-memory` is a good approximation.
- If a repo relies mainly on scratch-path memory under `~/.claude/projects/...`,
  `--wire-memory` alone is incomplete.
- A true OpenCode-native memory plugin belongs in memory-os, not in opencode-sync.

That is the boundary:

- opencode-sync can wire stable read surfaces into config
- memory-os owns full session lifecycle behaviour
