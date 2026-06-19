# Capability-Detection Preamble

Paste this block near the top of any canonical skill or agent body that uses a
degradable construct (Task* phase chains, AskUserQuestion, Skill dispatch). It makes
the same file behave correctly on Claude Code and OpenCode, and it is the wording
`validate_dual.py` looks for when it decides a file is mitigated (clears OC-05 / TR-01,
and moves the portability class from NEEDS-PREAMBLE to PORTABLE-WITH-NOTES).

---

## Runtime compatibility

This skill runs on both Claude Code and OpenCode. Detect what is available before
acting, and degrade gracefully - never assume a tool exists.

- **Phase AND task tracking.** If `TaskCreate` / `TaskUpdate` exist (Claude Code),
  create one task per phase AND one per discrete action, chaining them with
  `addBlockedBy` so a phase cannot start before its predecessor completes. If they do
  not (OpenCode), write the SAME items with `todowrite`: every phase becomes a
  `todowrite` entry and every task/action becomes its own `todowrite` entry too, so the
  whole plan is visible in the TUI sidebar and progress is legible. Mark each item
  in_progress when you start it and completed at its boundary, exactly mirroring the
  Claude task list one-to-one. There is no automatic blocking on OpenCode, so treat the
  order as the gate: do not start the next item until the current one is checked.

- **Degrade, never abort.** The absence of `TaskCreate` is NOT a stop condition. A skill
  that halts, "surfaces and stops", or otherwise refuses to run when the Task* tools are
  unavailable is broken on OpenCode - the correct behaviour is always to fall back to the
  `todowrite` checklist above and keep going. Track phases differently; never skip phase
  tracking and never abort the run just because Task* is missing.

- **User choices.** If `AskUserQuestion` exists, use it (four options maximum). If not,
  ask in plain text and have the user reply with a letter:
  `(A) ...  (B) ...  (C) ...  (D) ...`. The same choice must be expressible both ways.

- **Skill dispatch.** `Skill("name")` on Claude Code maps to the `skill` tool on
  OpenCode - reference the target skill by name either way.

- **Shell and files.** `Read` / `Write` / `Edit` / `Bash` map directly to
  `read` / `write` / `edit` / `bash`. Bundled scripts are stdlib Python 3 and run
  identically from either runtime's shell.

- **No equivalent.** This skill does not depend on `SendMessage`, `ScheduleWakeup`,
  plan mode, or worktrees; if a future edit adds one, gate it behind a Claude-Code
  capability check and provide an OpenCode fallback or mark the section Claude-only.

---

Keep the wording above intact when you adapt it - the validator matches on the
"runtime compatibility", "graceful", "fallback", and "todowrite / plain text" phrases,
and OC-06 flags any skill that stops or aborts when Task* is unavailable instead of
degrading to the todowrite checklist.
