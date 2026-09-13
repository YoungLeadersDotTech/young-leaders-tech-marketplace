# diy-build-companion

**Version**: 2.0.0

A companion for planning and running real DIY builds. It works in assembly-line order, sizes work
to the energy you actually have, enforces breaks, and will not let a child-safety concern through
on a promise to fix it later.

## What it does

- **Energy-aware work blocks.** It asks your energy level and the time you have, then picks work
  that fits. Low energy gets sanding and sorting, not a cut list.
- **Enforced breaks.** "Just one more thing" is treated as the signal that a break is overdue.
- **A resume that actually resumes.** State is written as an ultra-specific next action ("attach
  left side panel with 4x 2.5in screws, top holes first"), not "continue assembly".
- **A child-safety veto gate.** Runs inline against fall heights, entrapment gaps, a 4x structural
  safety factor, material hazards, and tolerances. A FAIL is a hard veto and cannot be overridden.
- **To-scale visuals only.** Design sketches are drawn to a real mm-to-px scale or labelled as
  not-to-scale. Never presented as representative when they are not.

## Modes

The skill infers one of five modes from what you ask:

| Mode | Triggered by |
|---|---|
| Start a build | "start a build for...", "new DIY project..." |
| Resume a build | "where was I", "resume", "pick up the mud kitchen" |
| Check progress | "how's it going", "progress", "am I due a break" |
| Save state before a break | stopping, fatigue, "just one more thing" |
| Child-safety veto gate | about to cut or assemble, a design changed, or an explicit safety check |

## Where state lives

The single source of truth is the project folder in your build repo:

```
projects/
  active/<project-slug>/      overview.md, state.md, progress-log.md, safety.md
  completed/<project-slug>/   same shape, moved here when the build is done
```

`state.md` is read first on every resume and leads with a READ FIRST band for blockers and
irreversible decisions. The skill pulls before reading and commits after writing, and it will
never claim a write it did not make: with no file-write ability it hands you the updated file and
the exact path instead.

## Install

Published in the young-leaders-tech-marketplace. Add that marketplace and install the
`diy-build-companion` plugin (see the marketplace README for the exact add and install commands).
In Cowork, install from Customize then Plugins.

## Design principle

Self-contained. The skill has no cross-skill or external plugin dependencies, and its reference
files (`safety-standards.md`, `field-notes.md`) live inside its own folder, so it runs the same
way standalone or bundled.
