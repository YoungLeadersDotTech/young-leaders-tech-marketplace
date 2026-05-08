# Marketplace Guidelines

> Last reviewed: 2026-05-08
> Schema version: 1.0
> Applies to: `young-leaders-tech-marketplace` v1.x

Rules every plugin in this marketplace must follow. The `agent-validator` and `skill-validator-agent` cite this file as ground truth before approving any plugin-bound artefact.

## Severity Taxonomy

Validators classify findings using these levels and quote the section that defines the rule.

| Severity | Sections | Behaviour |
|---|---|---|
| BLOCKER | 1, 3, 6, 7 | Refuse to advance; commit must be fixed before merge |
| WARNING | 5, 9 (cosmetic fields), 8 | Surface to user; allow override with explicit acknowledgement |
| INFO | 2 (semver judgement calls), 4 (description rewrites), 10 | Note in report; no action required |

## 1. The 4-File Rule

Any change inside `plugins/<name>/` MUST update all four of these files in the same commit:

```
plugins/<name>/CHANGELOG.md            # add a new dated semver entry
plugins/<name>/VERSION                 # single line, semver only
plugins/<name>/.claude-plugin/plugin.json  # bump "version" field
.claude-plugin/marketplace.json        # bump plugin entry version + top-level version
```

Missing any one of the four = stale plugin cache for users. The plugin manager keys off `version` to decide whether to re-download; if `marketplace.json` says a version users already have, no update fires.

**New plugin (first commit)**: create all four files in the introducing commit. Treat absence of prior VERSION as `0.0.0 -> 1.0.0` (a marketplace-level MINOR bump because a new plugin entered the catalogue).

**VERSION file format**: single line, semver, with a trailing newline. Comparisons must strip trailing whitespace before equality checks (`VERSION` content `1.2.0\n` equals plugin.json `"version": "1.2.0"`).

## 2. Semver Decision Table

| Change type | Bump |
|---|---|
| Bug fix, typo correction, description trim | PATCH (x.y.Z) |
| New skill, agent, command, template, or reference | MINOR (x.Y.z) |
| Breaking change, file removal, agent merge, scope change | MAJOR (X.y.z) |

A skill or agent rename counts as MAJOR (existing invocations break). Rename is defined as a change to the `name:` frontmatter field or the file path. A rewrite of the `description:` field that preserves `name:` is NOT a rename.

## 3. Same-Commit Ordering Rule

Never bump `marketplace.json` before content lands. The 4 file updates and the new content go in the SAME commit (or PR), not separate commits.

Why: if `marketplace.json` is bumped first, users install the empty version, then when content lands the plugin manager sees the same version number and never re-downloads.

Recovery if violated: bump version again (e.g. v1.2.0 -> v1.2.1) and re-commit with content. Document the slip in CHANGELOG.

## 4. Two Version Fields in marketplace.json

```json
{
  "version": "1.2.0",
  "plugins": [
    {
      "name": "skills-toolkit",
      "source": "./plugins/skills-toolkit",
      "version": "2.0.0",
      "description": "..."
    }
  ]
}
```

Both fields bump when any plugin changes:
- Top-level `version`: marketplace-wide; PATCH for any plugin change, MINOR if a new plugin enters, MAJOR if a plugin is removed or restructured.
- Plugin entry `version`: must match `plugins/<name>/VERSION` exactly.

## 5. CHANGELOG Format (Keep a Changelog)

```markdown
## [2.0.0] - 2026-05-08

### Added
- agent-author: merged agent from former agent-builder, agent-editor, agent-packager
- references/marketplace-guidelines.md: validators ground-truth for plugin rules
- templates/: 9 generic templates (claude-subagent, hooks, install-script, bundle-readme)

### Changed
- skill-creator-agent: TodoWrite -> Task* tools; description trimmed to <=250 chars
- skill-validator-agent: TodoWrite -> Task* tools

### Removed
- 3 separate agent-builder/editor/packager agents (merged into agent-author)
```

Permitted sections per release: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`. Use only the ones that apply this release - omit empty sections rather than including blank headings. Date is ISO YYYY-MM-DD.

Each entry should name the file or component changed and explain WHY in one clause, not just what.

## 6. Frontmatter Description Cap

Anthropic enforces a 250-character cap on every `description:` field in agent, skill, and command frontmatter. The rule is `len(description) <= 250` after YAML parse (NOT raw line length, which counts `description: ` prefix and quote characters). Over the cap and the description is truncated mid-word in the skill listing Claude uses for auto-invocation matching, which breaks trigger matching for any keywords past the cap.

Source citations (Anthropic Claude Code docs, `skills.md`):
- "To optimize context usage, descriptions exceeding 250 characters are truncated in the skill listing."
- "Optimize descriptions by placing the key use case at the beginning, as each entry is capped at 250 characters."
- See https://github.com/ericbuess/claude-code-docs/blob/main/docs/skills.md

Front-load the most discriminating triggers - the tail of the description is what gets cut.

Validation:

```bash
python3 -c "
import yaml, sys, pathlib
for p in pathlib.Path('plugins').rglob('*.md'):
    text = p.read_text()
    if not text.startswith('---'):
        continue
    fm = yaml.safe_load(text.split('---', 2)[1])
    desc = (fm or {}).get('description', '')
    if len(desc) > 250:
        print(f'{p}: {len(desc)} chars')
"
```

Style guidance for descriptions:
- Lead with concrete trigger phrases, not feature lists.
- State when NOT to invoke (negation reduces false positives).
- No em dashes. No marketing adjectives ("comprehensive", "powerful", "intelligent").
- Plain text. Markdown bold or italics in frontmatter is non-standard YAML and brittle.

## 7. No Em Dashes

The character U+2014 (em dash) is banned anywhere in any file in this marketplace. Use ` - ` (space-hyphen-space) instead.

Why: cross-tool consistency, search-friendliness, and a personal style rule documented in `~/.claude/CLAUDE.md`.

Detection:

```bash
grep -rlP '\x{2014}' plugins/ .claude-plugin/
```

The output of that command should always be empty before commit. Add it to your pre-commit hook if you are repeatedly forgetting.

## 8. Migration Pattern: Global Skill or External Bundle to Plugin

When porting a global skill (`~/.claude/skills/X/`) or external bundle into a marketplace plugin:

1. Apply any pending fixes to the source FIRST (so the plugin copy is the fixed version, not the bug-laden one).
2. Create the plugin directory and copy files.
3. Apply the 4-file rule (CHANGELOG, VERSION, plugin.json, marketplace.json).
4. Push commit.
5. Run `/reload-plugins` to confirm the plugin loads.
6. ONLY THEN delete the source (global skill or original bundle).

Never delete the source before `/reload-plugins` confirms the plugin loads. Otherwise you are one cache-clear away from losing the work entirely.

## 9. Plugin Schema (Claude Code canonical)

Per Claude Code documentation (current as of 2026-05):

```
plugin-name/
  .claude-plugin/
    plugin.json              # required
  commands/                  # optional
    *.md                     # slash command definitions
  agents/                    # optional
    *.md                     # subagent definitions
  skills/                    # optional
    skill-name/
      SKILL.md
      references/            # optional reference files
      examples/              # optional examples
      scripts/               # optional helper scripts
  hooks/                     # optional
    hooks.json
  .mcp.json                  # optional
  README.md                  # required for human-readable docs
```

`plugin.json` recommended fields:

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "<= 250 chars, no em dashes",
  "author": { "name": "...", "url": "..." },
  "homepage": "https://...",
  "repository": "https://github.com/...",
  "license": "MIT",
  "keywords": ["..."],
  "commands": ["./commands/foo.md"],
  "agents": ["./agents/bar.md"],
  "skills": ["./skills/baz"]
}
```

Agent frontmatter (canonical fields):

```yaml
---
name: agent-identifier
description: <=250 chars, concrete triggers
model: inherit            # optional, defaults to inherit
color: blue               # optional, cosmetic
tools: Read, Write, Glob  # optional, comma-separated or array
---
```

Slash command frontmatter (all optional):

```yaml
---
description: Short description for /help (~60 chars recommended for /help display, hard cap 250)
allowed-tools: Read, Write, Bash(git:*)
model: sonnet
argument-hint: [arg1] [arg2]
---
```

Skill `SKILL.md` frontmatter:

```yaml
---
name: Skill Name
description: When to use this skill (<=250 chars)
version: 1.0.0
---
```

**Name format rules**:
- Skills accept human-readable names (Title Case with spaces permitted): `name: Stakeholder Discovery Template`.
- Agents require kebab-case identifiers (lowercase, hyphenated, no spaces): `name: agent-author`.
- Plugins require kebab-case (matches directory name): `name: skills-toolkit`.

**Auto-discovery vs explicit arrays**: Claude Code auto-discovers skills, agents, and commands from their canonical directories. The `commands`, `agents`, `skills` arrays in plugin.json are explicit overrides used when the directory layout differs from canonical. Either form is valid; do NOT flag plugins that omit the arrays as non-compliant.

## 10. Validator Citation Pattern

Both `agent-validator` and `skill-validator-agent` should cite this file when reporting findings:

```
Finding: description exceeds 250 chars (file:line)
Rule: marketplace-guidelines.md section 6 (Frontmatter Description Cap)
Fix: trim to <=250, lead with trigger phrases
```

The citation makes failures actionable for the user without re-explaining policy.

## Quick Pre-Commit Checklist

Before committing any change to `plugins/<name>/`:

- [ ] CHANGELOG.md has a new dated entry naming what changed and why
- [ ] VERSION file bumped
- [ ] plugin.json `version` matches VERSION
- [ ] marketplace.json plugin entry `version` matches VERSION
- [ ] marketplace.json top-level `version` bumped
- [ ] All frontmatter `description` fields <=250 chars
- [ ] `grep -rlP '\x{2014}' plugins/<name>/` is empty
- [ ] No employer-specific or client-specific terminology has leaked into a generic plugin (run a grep against any keywords from your work context that should not appear in personal-marketplace artefacts; pattern is repo-specific)
- [ ] No real PII (emails, phone numbers, secrets, real names other than the user's own)
- [ ] All four file updates and the new content are in the SAME commit
