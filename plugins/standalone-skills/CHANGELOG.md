# Changelog

All notable changes to the standalone-skills plugin.

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
