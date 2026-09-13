# Changelog

All notable changes to the diy-build-companion plugin.

Releases up to and including 1.0.1 were published as the `standalone-skills` plugin; the
rename is recorded in 2.0.0 below.

## [2.0.0] - 2026-09-13

### Changed
- **BREAKING - the plugin is renamed from `standalone-skills` to `diy-build-companion`.** The
  container held exactly one skill, so the bundle name hid what it actually did and would have
  forced anyone wanting this skill to take every future unrelated skill with it. The plugin
  directory moves from `plugins/standalone-skills/` to `plugins/diy-build-companion/`, and the
  marketplace entry is renamed and re-sourced. Existing installs must remove `standalone-skills`
  and install `diy-build-companion`; the skill itself is unchanged by the rename.

### Changed
- **BREAKING - diy-build-companion no longer uses Google Drive.** The single source of truth is
  now the project folder in the build repo, read from and written to disk directly. The previous
  model declared Drive authoritative and instructed the skill not to trust local files, which was
  wrong in practice: the Drive `DIY/` folder was empty while live project state sat committed in
  the repo. Anyone who genuinely kept state in Drive must move those files into `projects/active/`
  before upgrading.
- `## Drive layout` is now `## Project layout`, describing `projects/active/<slug>/` and
  `projects/completed/<slug>/` with the real file set, and noting the top-level `PROJECTS.md`
  index. Completed builds move rather than being deleted.
- The read/write asymmetry rule is replaced by "sync before you read, commit after you write".
  The honest-handback rule is kept for sessions with no file-write ability, and the prohibition on
  claiming a write that did not happen is unchanged.
- Triage now runs at session start and on external-change signals, not at the top of every turn.
  State written earlier in the same session is trusted, which removes a per-turn re-read.

### Added
- A not-found branch in triage (step 2). After a failed lookup the skill lists both project
  directories, checks for a near-miss slug, and pulls, and only then asks an open question. It is
  explicitly barred from offering to start fresh over state it has not found. This was the
  proximate cause of the observed failure: five empty searches led to a closed three-option
  question that offered "start fresh" while the real `state.md` was committed in the repo.

### Fixed
- Mode 3 read the whole of the append-only `progress-log.md` while Mode 2 correctly read only the
  tail. Mode 3 now reads the last ~10 entries, and the layout section gains a rotation rule
  (archive to `progress-log-<year>.md` past roughly 50 entries).

## [1.0.1] - 2026-07-25

### Added
- diy-build-companion: `## First: triage the request` section, inserted between the Drive
  layout section and `## Modes`. Mode selection, the safety-critical determination, and the
  Drive write-capability check were previously implicit or buried inside individual modes;
  this lifts all four decisions into one explicit classify-first step so scope and safety are
  settled before any mode body runs. No behaviour change.

### Fixed
- Version metadata for the change above, which merged without the five-file update. Recorded
  here rather than backdated into 1.0.0 so the release history stays honest.

## [1.0.0] - 2026-06-14

### Added
- Initial release of the standalone-skills plugin.
- diy-build-companion skill: plan and run DIY builds with energy-aware work blocks, enforced
  breaks, cross-device project state in Google Drive, and an inline child-safety veto gate.
- Self-check rule in diy-build-companion: never present a design visual that is not to scale;
  lead with a to-scale prototype (elevation plus plan), then to-scale finish swatches.
