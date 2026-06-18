# Tool Translation - Claude Code to OpenCode

How tool names and tool-driven constructs map across the two runtimes, the recipes
for degrading the ones with no clean equivalent, and the rules for writing a
canonical skill body that survives on both sides. Used by `scripts/sync_agents.py`
(the tool map) and `scripts/validate_dual.py` (the TR and OC-05 rules). Verify the
builtin list against https://opencode.ai/docs/tools before a big migration.

## Tool inventories

**Claude Code builtins** (the set this skill knows about): Read, Write, Edit, Bash,
Glob, Grep, WebFetch, WebSearch, Task, TaskCreate, TaskUpdate, TaskGet, TaskList,
Skill, AskUserQuestion, NotebookEdit, ToolSearch, SendMessage, ScheduleWakeup,
EnterPlanMode, ExitPlanMode, plus `mcp__*` connector tools.

**OpenCode builtins** (Jun 2026): bash, edit, write, read, grep, glob, list, skill,
todowrite, todoread, webfetch, websearch, question, task, apply_patch, plus MCP
tools named per server config.

## Direct mapping

| Claude Code | OpenCode | Notes |
|---|---|---|
| Read | read | |
| Write | write | |
| Edit | edit | |
| Bash | bash | |
| Glob | glob | |
| Grep | grep | |
| WebFetch | webfetch | |
| WebSearch | websearch | |
| Skill | skill | `Skill("name")` becomes `skill` tool; reference the skill by name |
| AskUserQuestion | question | OpenCode `question` tool; same intent, simpler schema |
| Task | task | sub-agent dispatch; OpenCode `task` spawns a subagent |
| TodoWrite | todowrite | casing differs only |
| (none) | todoread | OpenCode splits read/write of the todo list |
| (none) | list | OpenCode directory listing builtin |
| (none) | apply_patch | OpenCode patch-apply builtin |

## Degraded mapping (works, but weaker)

| Claude Code | OpenCode | What is lost |
|---|---|---|
| TaskCreate / TaskUpdate | todowrite | Dependency chains (`addBlockedBy`, `addBlocks`) collapse to a flat checklist. Phase gates become advisory, not enforced. |
| TaskGet / TaskList | todoread | No structured per-task status or owner; you read back a flat list. |

Recipe for a phase chain. Where the Claude body says:

```python
t1 = TaskCreate("Phase 1: Discovery")
t2 = TaskCreate("Phase 2: Build")
TaskUpdate(t2, addBlockedBy=[t1])
```

the portable body should add the OpenCode path beside it:

> On OpenCode (no Task* tools): write the same phases with `todowrite` as an ordered
> checklist and do not start a phase until the previous item is checked. The ordering
> is the gate; there is no automatic blocking.

## No equivalent - drop with a warning

SendMessage, ScheduleWakeup, EnterPlanMode, ExitPlanMode, EnterWorktree, ExitWorktree,
NotebookEdit, KillShell, ToolSearch. `sync_agents.py` drops these from the generated
`tools` map and records a warning. ToolSearch in particular has no analogue: OpenCode
loads every tool schema up front, so there is no deferred-schema search step.

A body that depends on one of these (for example an agent that hands off via
SendMessage) is genuinely Claude-only. `validate_dual.py` flags it TR-02 and the
report classes it as not portable - keep it on the Claude side or redesign the handoff.

## AskUserQuestion to plain prose

OpenCode has `question`, but the schema is simpler (no multi-select, no per-option
preview). For a body shared across both, the safest portable form is lettered prose:

> Pick one and reply with the letter:
> (A) Setup   (B) Sync   (C) Validate   (D) Drift

On Claude Code you may still call AskUserQuestion for the nicer widget; just make sure
the same choice is expressible in text so the OpenCode path is not blocked.

## MCP tools

MCP tool names are assigned by each client from its own server config, so the exact
`mcp__server__tool` string is not portable. In a shared body, reference MCP tools by
intent ("the Slack search tool", "the Jira create-issue tool") rather than by their
Claude-side identifier. `validate_dual.py` raises TR-03 (INFO) when it sees an
`mcp__` prefix in a body.

## Capability-detection preamble

Every canonical skill that uses any degradable construct should open with a short
capability check so the same file behaves correctly on either runtime. The
copy-paste block lives in `references/capability-preamble.md`. `validate_dual.py`
treats the presence of that wording (or any "fallback / graceful degradation /
todowrite / plain text" phrasing) as the mitigation that turns OC-05 and the
portability class from NEEDS-PREAMBLE into PORTABLE-WITH-NOTES.

## Portable authoring rules

1. Universal frontmatter only in the canonical file: `name`, `description`. Everything
   else (`allowed-tools`, `version`, `tags`) is Claude-side convention that OpenCode
   ignores - harmless, but do not rely on it for behaviour.
2. Never rely on `disable-model-invocation` for safety. OpenCode ignores it and also
   exposes every skill as a `/name` command, so a side-effecting skill is reachable
   regardless. Gate side effects with an explicit confirmation step in the body.
3. Phrase tool use by intent, then name the concrete tool. "Search the web (WebSearch
   on Claude Code, websearch on OpenCode)" survives translation; a bare "call
   WebSearch" reads as Claude-only.
4. Always pair a Claude-only construct with its degradation path in the same paragraph.
   That single habit is what moves a file from NEEDS-PREAMBLE to portable in the audit.
