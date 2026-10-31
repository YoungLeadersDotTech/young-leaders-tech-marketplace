# Changelog

All notable changes to the talk-rehearsal-coach plugin.

## [1.0.0] - 2026-10-31

### Added
- **`talk-rehearsal-coach` skill**: five phases (intake, shape, rehearsal pack, HTML coach, optional
  in-chat drill) with per-phase task tracking chained by `addBlockedBy`.
- **`templates/rehearsal-coach.html`**: one self-contained, offline page with seven tabs (Start
  here, Method, Map, Cue cards, Script, Drill, Your talk), light and dark themes, print styles, and
  a paste box that rebuilds the whole page from any script in the browser. Opens on the plan with
  the next step highlighted and a button per step to the right tab. The drill runs at real, fast or
  slow pace, the quiz can shuffle and remembers misses between visits, and the cue cards warn when
  two cues start with the same word. The ADHD tag sits on the four ADHD-specific techniques only and is
  explained once, in the Method intro. Keyboard shortcuts can be switched off, focus is kept on every
  re-render, and the slide is announced once in a single live region.
- **`scripts/build_coach.py`**: validates talk JSON and injects it into the template as strict JSON
  that is safe inside a script element. Optional `--site-bar` preset (off by default) and
  `--no-em-dashes`. Optional per-slide `seconds`, a `timeLimit` for free-paced talks, and
  `plan.days` for plans longer than two days. 44 tests in `scripts/tests/test_build_coach.py`.
- **`reference/method.md`**: the six techniques (the four that are tailored for ADHD carry the tag),
  the recall chain, the default two-day plan and pacing guidance.
- **`reference/site-bar-youngleaders.json`**: opt-in Young Leaders in Tech site-bar preset.
