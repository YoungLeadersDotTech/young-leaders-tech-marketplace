# Validator Rule Inventory - Claude Code and OpenCode

The full rule set `scripts/validate_dual.py` enforces, plus the manual-judgement
rules a human or LLM pass should add. This is the answer to "how many different
rules are there for my validators on either side": four families, counted below.

The validator discovers what to assess by location - `SKILL.md` (skill),
`agents/*.md` (agent), `commands/*.md` (command) - so plain docs and READMEs are
never assessed. Point it at a file, a plugin, a repo, or a `.claude` tree and
choose a `--depth` (shallow / standard / deep); see SKILL.md Mode C for the depth
question. The rules below apply per discovered tool regardless of depth.

## Families and counts

| Family | Prefix | Applies to | Automated rules | Runs when --target is |
|---|---|---|---|---|
| Shared | SH | both runtimes | 6 | claude, opencode, both |
| Claude Code | CC | Claude packaging | 4 | claude, both |
| OpenCode | OC | OpenCode schema | 6 | opencode, both |
| Translation / drift | TR | Claude to OpenCode portability | 4 | opencode, both |

Automated total: **20 mechanical rules**. Manual-judgement rules add **6 more**
(MJ family below) for a working inventory of **25**. The Claude-facing surface is
SH + CC = 10 automated; the OpenCode-facing surface is SH + OC + TR = 16 automated;
they share the 6 SH rules, so roughly 57 percent of the Claude side overlaps the
OpenCode side. That overlap is why a single canonical source is viable: most of what
makes a good Claude artifact also makes a good OpenCode one.

## Shared rules (SH) - both runtimes

| ID | Severity | Check |
|---|---|---|
| SH-01 | FAIL | Frontmatter present and parseable as YAML |
| SH-02 | FAIL | Skill `name` is kebab-case and matches its folder |
| SH-03 | FAIL | `description` present (and `name` present for skills) |
| SH-04 | FAIL | No em dash anywhere in the file (use ' - ') |
| SH-05 | WARN | No hardcoded `/Users/...` path (use ~ or config) |
| SH-06 | WARN | Skill file is named `SKILL.md` |

## Claude Code rules (CC)

| ID | Severity | Check |
|---|---|---|
| CC-01 | WARN / FAIL | `description` within 250 working cap (WARN 251-1024, FAIL over 1024) |
| CC-02 | WARN | Every `allowed-tools` entry is a known Claude tool or `mcp__*` |
| CC-03 | FAIL / WARN | `TodoWrite` in `allowed-tools` is FAIL (use Task* variants); generic `Task` is WARN (prefer specific Task*; Task / Agent itself is valid for subagent dispatch) |
| CC-04 | INFO | `allowed-tools` present when the body invokes bracketed tools |

CC-04 is advisory and reported by the manual pass; CC-01 to CC-03 are mechanical.

## OpenCode rules (OC)

| ID | Severity | Check |
|---|---|---|
| OC-01 | FAIL | `description` within OpenCode's 1024-char cap |
| OC-02 | FAIL | Agent `mode` is one of primary / subagent / all (if present) |
| OC-03 | WARN | Agent `model` carries a `provider/model-id` prefix |
| OC-04 | INFO | Lists skill frontmatter fields OpenCode silently ignores |
| OC-05 | WARN | Body uses a Claude-only tool with no degradation wording |
| OC-06 | WARN | Body stops / aborts when Task* is unavailable instead of degrading to a todowrite checklist (OpenCode-hostile) |

OC-04 is the quiet one that matters: OpenCode drops unknown fields without error, so a
skill leaning on `disable-model-invocation` changes behaviour with no warning unless
something flags it.

## Translation / drift rules (TR)

| ID | Severity | Check |
|---|---|---|
| TR-01 | WARN | Soft constructs (Task*, AskUserQuestion, Skill(), ToolSearch) present without a capability preamble |
| TR-02 | WARN | Hard constructs (SendMessage, ScheduleWakeup, plan mode, worktree, hooks.json, CLAUDE_PLUGIN_ROOT) with no OpenCode equivalent |
| TR-03 | INFO | `mcp__` tool prefix in a shared body (names differ per server) |
| TR-04 | WARN | `disable-model-invocation: true` (ignored by OpenCode - the drift trap) |

TR-01 is folded into the OC-05 check in the current script (one warning per file once
unmitigated body usage is found); it is listed separately here because conceptually it
is a portability rule, not an OpenCode-schema rule.

## Manual-judgement rules (MJ) - not mechanical

These need a reading pass (a human, or an LLM scoring pass via skills-toolkit). The
validator cannot decide them reliably, so it does not try.

| ID | Check |
|---|---|
| MJ-01 | `When to Use` and `Skip when` are concrete and mutually exclusive |
| MJ-02 | Graceful-degradation claims are real (the body never claims a write that did not happen) |
| MJ-03 | Description is specific enough to trigger correctly and not over-broadly (description-quality rubric) |
| MJ-04 | Ground-truth / instruction blocks are not contradicted later in the body |
| MJ-05 | Preset / team specifics are opt-in, not baked into the generic path |
| MJ-06 | Model map values were verified against models.dev this cycle (ids go stale) |

## How the families compose per target

- `--target claude` runs SH + CC (10 automated). Use before shipping a Claude-only artifact.
- `--target opencode` runs SH + OC + TR (16 automated). Use before generating or trusting an OpenCode copy.
- `--target both` runs everything (20 automated). Use in CI and before any cross-runtime release.

Exit is non-zero whenever any FAIL is present, so `--target both` doubles as the CI gate.
