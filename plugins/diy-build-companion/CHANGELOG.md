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
- **BREAKING - the skill no longer uses Google Drive.** The single source of truth is
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
- **The skill is renamed from `diy-build-companion` to `diy-continue`**, so it is invoked as
  `/diy-build-companion:diy-continue`. The plugin keeps its name. The skill now scans the project
  set and works out where you are rather than inferring a mode from phrasing, so "continue" is
  what it actually does. A command wrapper was considered and rejected: command wrappers are
  deprecated and fail validation (`C14-COMMAND-WRAPPER`), and skills are directly invokable as
  `/plugin:skill-name`, so renaming the skill is the supported way to get the trigger.
- **Domain 3 rebuilt in `reference/safety-standards.md`.** It was seven lines of judgement prose.
  It now carries tool risk tiers (very high, high, medium, low) with named tools and per-tier
  protocol, builder capability levels with the alternative to offer when a design outruns them, and
  a required safety equipment checklist: ANSI Z87.1 eye protection, hearing protection above 85dB,
  dust mask for sanding and for cutting treated lumber, gloves for handling but **not** for power
  tools, a stable work surface, and a first aid kit on site. Stated physical limitations now come
  with accommodations to offer rather than only an instruction to take them into account.
- Domain 5 gains the practices and red flags behind the tolerances: measure twice from a consistent
  reference point, 3-4-5 for square, account for material thickness explicitly, test-fit before
  assembly. Red flags: a safety-critical dimension measured once, imprecision in the stated
  dimension itself, accumulating error across a multi-step build, and no written cut list.
- A short record-keeping section: receipts for structural timber, fixings and finishes as the only
  durable proof that what went in is what was approved at the gate, and photographs of connections
  that end up hidden.
- **`reference/field-notes.md` gains the craft content**: the cutting checklist (blade depth set to
  material thickness plus about 3mm, roughly 3 seconds to full speed before contact, midpoint
  on-line check, wait for the blade to stop before moving, 20-25 minutes per large panel); the
  wrong-cut decision table (under 3mm carry on if non-structural, 3-6mm stop and evaluate, over 6mm
  re-cut) plus reject warped stock and stop on a wrong delivery rather than substituting at the
  bench; nominal versus actual timber and sheet sizes; the plywood grade time trade-off (roughly 3
  extra hours for construction grade against about 30 minutes for pre-sanded); a tiered kit list;
  break mechanics (warn at 40 minutes, stop at 45, never past 60, 15-minute break, 5-minute
  micro-break every 20-30); task sizing with never more than 90 minutes continuous and ending on a
  completion rather than mid-task; re-asking energy after each break with named low-energy work and
  ending the day early as a legitimate outcome; and a pre-break workspace safety check.
- **Optional `tools.yaml` in the build repo.** The skill reads it when present for what tools are
  owned, the builder's proficiency, PPE and any stated limitations, and uses it for the Domain 3
  check. It is never required, never created unprompted, and a missing key means unknown rather
  than absent. It lives beside `projects/` in the builder's own repo and never in this plugin, so
  a tool inventory is never published with the skill; whether to commit it is the owner's choice.
  Documented in the project layout with the schema under Domain 3.
- **Scan-first triage.** Triage now opens by scanning every project in `projects/active/` rather
  than starting from a project the request happened to name: read each `state.md`'s header line
  and `READ FIRST` band only (not whole files, not `progress-log.md`), then select - zero active
  goes to the start flow, exactly one resumes it, two or more asks once with at most four options
  ordered by most recently updated. This is the "continue my build" entry point: one request that
  works out where you are, instead of five modes inferred from phrasing.
- A safety-gate check at triage time, separate from the gate itself. One read of `safety.md` on
  every pass, and if the project is safety-critical with no recorded PASS, every cut, drill,
  fixing and assembly is treated as blocked. **Fail closed**: a missing or unreadable `safety.md`
  blocks, and is never read as a PASS or as silence. The full five-domain evaluation still runs
  inline and is never handed to a separate agent. Cheap check every time, expensive evaluation
  only when it fails.
- Two robustness rules the scan needs because real repos contain both cases: the `**Updated**`
  header is not at a fixed line number, so scan the top of the file for the marker rather than
  indexing a line; and a project folder with no `state.md` pre-dates the schema and is reported as
  archived rather than treated as an error.
- A not-found branch in triage (step 2). After a failed lookup the skill lists both project
  directories, checks for a near-miss slug, and pulls, and only then asks an open question. It is
  explicitly barred from offering to start fresh over state it has not found. This was the
  proximate cause of the observed failure: five empty searches led to a closed three-option
  question that offered "start fresh" while the real `state.md` was committed in the repo.

### Fixed
- The project layout section told the model to hand-update a top-level `PROJECTS.md` index when a
  project was created or moved. That instruction produced the drift it was meant to prevent: in
  the reference build repo the index listed three completed projects as active with dead links,
  and omitted both live projects. `PROJECTS.md` is now documented as derived output that is never
  a source of truth, to be regenerated by the repo's own script if it ships one and otherwise left
  alone.
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
