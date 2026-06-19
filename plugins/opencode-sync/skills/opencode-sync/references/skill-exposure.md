# Skill Exposure - getting plugin skills into OpenCode

How skills that live inside Claude Code plugins (`plugins/<name>/skills/<skill>/SKILL.md`)
become discoverable and runnable in OpenCode. Verified against opencode.ai docs and the
`/anomalyco/opencode` source via Context7, June 2026. Re-verify the config shape against
your installed OpenCode version before a big run.

## The problem

OpenCode discovers skills ONLY from these locations, walking up from the working
directory to the git worktree:

- `.opencode/skills/<name>/SKILL.md`, `~/.config/opencode/skills/<name>/SKILL.md`
- `.claude/skills/<name>/SKILL.md`, `~/.claude/skills/<name>/SKILL.md`
- `.agents/skills/<name>/SKILL.md`, `~/.agents/skills/<name>/SKILL.md`

OpenCode has no concept of Claude Code plugins or `marketplace.json`. So skills under
`plugins/<name>/skills/` are invisible to it - which is most of a plugin ecosystem.

## Why not symlinks

Symlinking each plugin skill into `.opencode/skills/` looks tempting but is unreliable:
OpenCode's core glob utility defaults to NOT following symlinks (`follow: options.symlink ?? false`
in `glob.ts`), and the skill loader does not opt in. A symlinked skill folder may simply
not be discovered. Do not depend on it.

## The mechanism: skills.paths + permission.skill

OpenCode's config takes an additional skills source that is recursively scanned for
`**/SKILL.md`. The schema is the object form (`skills.ts` defines `{ paths, urls }`):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "skills": { "paths": ["./plugins"] }
}
```

That one entry exposes every plugin skill - no copies, no symlinks, single-source (the
config points straight at the canonical folders).

Recursive discovery would also expose the reference-only skills you want hidden. Control
that with `permission.skill`, where `deny` means "hidden from the agent, access rejected":

```jsonc
{
  "skills": { "paths": ["./plugins"] },
  "permission": {
    "skill": {
      "*": "allow",
      "email-classifier": "deny",
      "stakeholder-templates": "deny"
    }
  }
}
```

## What to hide

On OpenCode, discovery (plus the deny-list) is the enable/disable lever, because
`disable-model-invocation` is ignored. Hide a skill only when it is invocable by
NEITHER the model NOR the user:

```
hide  iff  disable-model-invocation: true  AND  user-invocable: false
```

Everything else stays exposed (a user-invocable skill is reachable as `/name` on OpenCode
even if the model cannot auto-trigger it). `ingest_source.py` applies this rule and writes
the deny-list for you.

## Reference-only skills still load by path

A denied skill is hidden from the skill tool, but the `read` tool is separate - so a
consuming skill or agent can still load it by reading its `SKILL.md` path directly. That is
how reference-only skills keep working. Teach OpenCode to resolve the path tokens by adding
this block to `AGENTS.md`:

```
## OpenCode cross-runtime resolution

- `${CLAUDE_PLUGIN_ROOT}` means `plugins/<that-plugin>/` from the repo root.
- A `plugin:skill` reference resolves to `plugins/<plugin>/skills/<skill>/SKILL.md` -
  Read it on a need-to-know basis, or invoke a discovered skill by its bare name.
- Reference-only skills (denied in permission.skill) load by reading their SKILL.md path.
```

OpenCode does not expand `${VAR}` or `@import` references itself, so this explicit
instruction is what makes them resolvable.

## Caveats

- **Name uniqueness**: OpenCode's skill namespace is flat (no `plugin:` prefix). If two
  plugins use the same skill folder name, they collide - deny one or rename. Run
  `validate_dual.py` to surface duplicates.
- **Project vs global path**: a project `opencode.json` should use a relative `skills.paths`
  (portable when committed); a global config uses the absolute source path.
- **Recursion picks up test fixtures**: a `tests/fixtures/.../SKILL.md` with a name that does
  not match its folder is rejected by OpenCode's name check, so it self-excludes. Deny it
  explicitly if it is noisy.
