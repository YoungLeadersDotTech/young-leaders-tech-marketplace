# AskUserQuestion Protocol

Canonical shape for asking the user something inside a skill or agent in this marketplace. If a skill or agent needs to ask the user anything, it should follow this shape rather than the bare prose "ask the user" or "ask user".

## The governing rule (when and how, not just the JSON shape)

```
Use AskUserQuestion to make sure we are aligned before you build anything non-trivial.

When to trigger it:
- before you start building, any time a requirement is ambiguous or you are relying on an assumption
- the moment you sense we are drifting on scope or approach
- only ask what you genuinely cannot settle yourself from the code, the files or the docs

How to ask:
- max 4 questions per window, 2 to 4 options each
- batch independent questions as tabs in one window; if one answer changes the next, ask, wait, then ask the next
- make every option a real, distinct path. No filler, no "it depends"
- put your recommended option first and give the reason in its description
- single-select for "pick one", multi-select for "pick any that apply"
- use preview mode to show options side by side when the user is choosing between copy, layouts or code
- remember there is always an "Other" box, so phrase options so an answer you did not predict still fits

After the user answers:
- restate what was decided in one line, then build. Do not re-ask what has already been settled.
```

The four rules this adds on top of the raw mechanics: **trigger conditions** (without a "when", the tool sits dormant outside plan mode), **only ask what you genuinely cannot settle yourself** (stops permission theatre over things already answered by the code or docs), **recommended option first** (turns a blind menu into a steer - one-click agree or override), and **restate then build, never re-ask** (kills the loop where a settled decision gets re-litigated).

## Why prose alone isn't enough

"Ask the user whether to X" is an instruction to the model, not a structured interaction. Left as prose it:
- Gives the model no fixed option set, so the phrasing (and therefore what counts as a valid answer) drifts between runs
- Can't be validated mechanically - `validate_skills.py`'s `Q8-VAGUE-ASK-USER` check exists specifically to catch this
- Loses the built-in behaviors of the real `AskUserQuestion` tool: a fixed option list, an automatic "Other" free-text fallback, and (when the option has a `preview` field) a side-by-side comparison view

Every "ask the user" moment in a skill or agent should instead specify: the exact question text, a short header label, and 2-4 concrete options with descriptions.

## The block shape

```json
{
  "questions": [
    {
      "question": "<the exact question, ending in a question mark>",
      "header": "<max ~12 chars, shown as a chip/tag>",
      "multiSelect": false,
      "options": [
        {
          "label": "<1-5 words>",
          "description": "<what happens if the user picks this>"
        }
      ]
    }
  ]
}
```

Rules:
- **4 options max per question.** This is a hard cap on the underlying tool, not a style preference. If there are genuinely 5+ real choices, group the least common ones behind a `"More options"` entry and fire a second question if the user picks it - never silently truncate the list.
- **Every option needs a description**, not just a label. The label is what the user clicks; the description is what tells them what actually happens.
- Do not add an explicit "Other" option - the tool provides free-text entry automatically.
- Use `multiSelect: true` only when the choices are genuinely not mutually exclusive.

## Preview-before-write pattern

When the question is confirming a write (a file edit, a delete, a version bump) rather than a design choice, use this specific three-option shape so the user always sees the draft before it lands:

```json
{
  "questions": [
    {
      "question": "About to write the following to <absolute-path>. Proceed?",
      "header": "Confirm write",
      "multiSelect": false,
      "options": [
        {"label": "Approve", "description": "Write exactly what was shown above."},
        {"label": "Edit then write", "description": "Let me adjust the content first, then write."},
        {"label": "Cancel", "description": "Don't write anything."}
      ]
    }
  ]
}
```

Never call a write tool (Write, Edit, `git rm`, a delete script) on the basis of an assumed default - if the action is destructive or hard to reverse, this pattern is mandatory, not optional.

## When NOT to ask

- If there is a single clear correct answer given the context already gathered, proceed - don't ask a question whose answer is already implied by the conversation.
- If a skill can be dispatched non-interactively (invoked by something other than a person watching the session), it should not block on a question with no answerer - fall back to a documented, named default and say so in its output, rather than hang.

## Timing

Ask before starting work when the choice shapes the whole approach (which of several valid designs to build). Ask after a discovery step when the choice depends on what was found (e.g. "found 3 command wrappers that duplicate existing skills - delete all, or review each first?"). Don't interrupt mid-task for something that could have been asked up front or deferred to the end.

## Cross-runtime surfaces (relevant to `opencode-sync`)

Not every surface that can run a skill from this marketplace supports the same `AskUserQuestion` feature set. Single-select, multi-select, and the automatic free-text fallback work everywhere Claude Code's skills run. Per-option `description` text and the `preview` side-by-side pane are Claude Code (terminal/desktop) features and should not be assumed present when a skill is synced to a different runtime (see `opencode-sync`). If a skill in this repo may run outside Claude Code, stick to the common subset - single-select, multi-select, free-text - rather than depending on `preview` or leaning entirely on description text to carry meaning that the question/option labels alone don't convey.
