---
name: skills-toolkit
description: Create and validate Claude Code skills and agents. Runs a real deterministic script for quality checks, never a self-scored rubric. Use when adding a skill or agent, or checking one against this repo's standards.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
  - AskUserQuestion
  - TaskCreate
  - TaskUpdate
  - TaskGet
  - TaskList
version: 1.0.0
category: Developer Tooling
---

# Skills Toolkit

Author and validate SKILL.md files and agent `.md` files for this marketplace. Replaces the old `skill-creator-agent`, `skill-validator-agent`, `agent-author`, and `agent-validator` prose-based agents (retired 2026-07-12) and their 5 command wrappers.

## When to use

- "create a skill", "new SKILL.md", "add an agent"
- "validate this skill", "check this agent"
- Before opening a PR that adds or changes a skill/agent in this marketplace

## Design principle

The old agents asked the model to self-score a description 0-100 against a rubric, simulate PII regex mentally, and print a "6-Phase Validation" report that had drifted from its own real step count. None of that is verifiable. This skill instead:

1. Runs `scripts/validate_skills.py` - a real script, not a prompt
2. Relays its findings verbatim
3. Never invents a PASS/FAIL verdict beyond what the script's exit code says

## Task* protocol

```
TaskCreate "Gather requirements"          -> mark in_progress immediately
TaskCreate "Draft SKILL.md content"       -> blocked_by Gather requirements
TaskCreate "Run validate_skills.py"       -> blocked_by Draft SKILL.md content
TaskCreate "Fix findings, re-run if FAIL" -> blocked_by Run validate_skills.py
TaskCreate "Write file, confirm with user" -> blocked_by Fix findings, re-run if FAIL
```

## Creating a new skill

1. Gather the skill's shape via `AskUserQuestion` rather than open prose - at minimum, name (kebab-case), one-line purpose, and the tool set. Example block (adapt options to context):
   ```json
   {
     "questions": [
       {
         "question": "What tools does this skill need?",
         "header": "Tool set",
         "multiSelect": true,
         "options": [
           {"label": "Read/Write/Edit", "description": "Reads and writes files directly"},
           {"label": "Bash", "description": "Runs shell commands or scripts"},
           {"label": "AskUserQuestion", "description": "Needs to ask the user structured questions mid-run"},
           {"label": "Task* set", "description": "Tracks multi-step work with TaskCreate/TaskUpdate/TaskGet/TaskList"}
         ]
       }
     ]
   }
   ```
   For open-ended fields (skill name, one-line purpose, WHEN/WHEN NOT to trigger) that don't reduce to a short option list, ask directly in prose - `AskUserQuestion` free-text entry covers this. See `references/askuserquestion-protocol.md` for the full shape and when prose-only is fine.
2. Draft frontmatter:
   ```yaml
   ---
   name: <kebab-case-name>
   description: <WHEN it triggers>. <WHEN NOT>. Keep under 250 chars total.
   allowed-tools:
     - Read
     - ...
   version: 1.0.0
   ---
   ```
3. Draft the body: a `## When to use` section, a workflow, and a `## Task* protocol` block if the skill does multi-step work with `TaskCreate`/`TaskUpdate` in its `allowed-tools`.
4. Write the file to `plugins/<plugin>/skills/<name>/SKILL.md`.
5. Run validation (below) before telling the user it's done.

## Creating a new agent

Same shape as a skill, at `plugins/<plugin>/agents/<name>.md`, with `tools:` (not `allowed-tools:`) in frontmatter. Agents are dispatched via the `Task` tool, never invoked directly by name the way skills are.

## Validating a skill or agent

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/skills-toolkit/scripts/validate_skills.py" --file <absolute-path-to-SKILL.md-or-agent.md>
```

Relay the script's output exactly as printed. If it exits non-zero (FAIL findings present), do not tell the user the file is ready - fix the specific findings listed, then re-run.

## Validating the whole marketplace

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/skills-toolkit/scripts/validate_skills.py" --all --root <repo-root> --json /tmp/findings.json
```

Checks implemented (see `scripts/validate_skills.py` for the source of truth - this list is descriptive, not authoritative):

| Check | Severity | What it catches |
|---|---|---|
| Q1-DESC-CAP | FAIL | `description:` over 250 characters |
| Q2-PII-SSN | FAIL | SSN-shaped strings (`NNN-NN-NNNN`) |
| Q3-PII-EMAIL | FAIL | Email addresses not on an example.com/.org/.net domain |
| Q4-EM-DASH | FAIL | The em dash character (Unicode U+2014) in the body - this repo uses ` - ` |
| Q5-XML-TAG | FAIL | Tag-shaped markup left in YAML frontmatter |
| Q6-TASK-SET | FAIL | A partial Task* set (e.g. `TaskCreate` without `TaskGet`/`TaskList`) |
| Q7-COMMAND-WRAPPER | WARN | A `commands/*.md` file that just wraps an agent or duplicates a sibling skill |
| Q8-VAGUE-ASK-USER | WARN | "ask the user" / "ask user" prose with no nearby `AskUserQuestion` reference - see `references/askuserquestion-protocol.md` |

## Completion signal

After validating a skill or agent, write a one-line JSON completion record so downstream tooling (or a future orchestrator) has something machine-readable to pick up - a lightweight, single-file analogue of the internal marketplace's completion-payload pattern, deliberately not the full mesh:

```bash
python3 -c "
import json, pathlib, datetime
pathlib.Path('.claude-plugin/validation-log.jsonl').open('a').write(
  json.dumps({
    'artifact': '<path>',
    'exit_code': <exit code from validate_skills.py>,
    'checked_at': datetime.datetime.utcnow().isoformat() + 'Z',
  }) + '\n'
)
"
```

## Not in scope

- Cross-plugin reference-following (an internal-only capability elsewhere; this skill validates one artifact or the whole repo, not a link graph).
- Any orchestrator dispatch, phase-gate enforcement, or state.json ownership - this is a standalone authoring/validation skill, not a mesh participant.

## Version History

### 1.0.0 (2026-07-12)
- Initial release, replacing `skill-creator-agent`, `skill-validator-agent`, `agent-author`, `agent-validator`, and their 5 command wrappers (`create-skill`, `list-skills`, `validate-skill`, `terminal-setup-install`, `update-readme`). Independently authored - not derived from any other repo's validator code.
