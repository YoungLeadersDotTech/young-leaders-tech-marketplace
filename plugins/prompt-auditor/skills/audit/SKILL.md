---
name: audit
description: Runs a deterministic offline static audit on a directory of skills, agents, or prompts (SKILL.md, AGENTS.md, CLAUDE.md) and prints findings. Use for local review of these. Not for runtime telemetry comparison or unrelated code review.
allowed-tools: Read, Glob, Grep, Bash
---

# Audit

Run the same static checks the upstream Left the Chat page and its pre-commit hook use,
at full local depth, against a directory the user names.

## Steps

1. Ask which directory to audit if not given. Default to the current directory.
2. Run: `node "${CLAUDE_PLUGIN_ROOT}/skills/audit/scripts/audit.mjs" <directory>`
3. Print the output as-is: findings grouped critical, then major, then minor.
4. If this is the first time this skill has run in this repo, offer to enable a
   pre-commit hook that calls `"${CLAUDE_PLUGIN_ROOT}/skills/audit/scripts/audit-staged.mjs"`
   against files staged in the target repo. Disabled by default. Ask before enabling it;
   never enable it unasked. A minimal hook body:

   ```bash
   #!/usr/bin/env bash
   node "${CLAUDE_PLUGIN_ROOT}/skills/audit/scripts/audit-staged.mjs" || exit 1
   ```

   Write it to `.git/hooks/pre-commit` (or a hooks directory pointed at by
   `git config core.hooksPath`) in the target repo, and mark it executable.

## Notes

- This is the static half only. Declared-versus-actual findings (a tool granted but
  never called, a skill that never fires) need runtime telemetry, which this CLI
  does not have.
- Read-only against the audited files. This skill never edits, moves, or deletes a file
  in the target repo, other than the hook file it is explicitly asked to write in step 4.
- `examples/find-ai-events.md` (with `examples/find-ai-events-fixed.md` alongside it as
  the corrected version) is a task prompt written to trip every `PROMPT-*` check - useful
  for seeing the full report shape without writing a prompt from scratch.
