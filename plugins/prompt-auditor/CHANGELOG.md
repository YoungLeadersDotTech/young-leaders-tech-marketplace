# Changelog

All notable changes to `prompt-auditor` are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-12

### Added
- Initial plugin, vendored from [YoungLeadersDotTech/left-the-chat](https://github.com/YoungLeadersDotTech/left-the-chat) (built for the AI Tinkerers Dublin hackathon, 12 September 2026). Ships the `audit` skill, which runs 19 deterministic offline static checks (`CFG-*`, `STYLE-*`, `PROMPT-*`) against a directory of `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, `agents/*.md`, or `skills/*.md` files and prints findings grouped critical, then major, then minor.
- Optional pre-commit hook (`skills/audit/scripts/audit-staged.mjs`), disabled by default, that runs the same checks against staged agent files.
- Two example prompts (`examples/find-ai-events.md` and its corrected counterpart) for exercising the full check set without writing a prompt from scratch.

### Fixed (pre-merge, same PR)
- `C8-TRIGGER-LANGUAGE`: `skills/audit/SKILL.md`'s description now leads with "Use this skill when...".
- `C16-ORPHAN-REFERENCE-FILE` (x2): the two example prompts are now real markdown links from `skills/audit/SKILL.md` and `README.md`, not plain text mentions.
