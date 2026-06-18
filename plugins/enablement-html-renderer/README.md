# enablement-html-renderer

**Version 1.2.1**

Packages finished enablement material into one self-contained HTML file where the reader chooses
the format. A handoff target, not a starting point: other skills (meeting, content-pipeline,
diy-build-companion) produce the substance, this packages it.

## Skill

- **enablement-html-renderer** - one `.html` file with a built-in format selector: bullets, prose,
  visual diagram, comic, or a copy-all cheat sheet. Severity callouts (critical/warn/tip/never),
  copy-paste command blocks, per-section time badges, and video deep-links persist across every
  format. The choice is reflected in the URL hash so a sender can link straight into a format.
  No server, no build step, offline, single file.

## Notable behaviour

- **Auto-linked URLs.** At render time, `http(s)` URLs become real links across every field and
  inside prose. Write a full URL anywhere and it resolves itself; no pre-built anchors, no dead
  links. The public build stays tracker-agnostic, so issue keys remain plain text.
- **Theme-aware diagrams.** A `normalizeSvg` pass remaps the legacy hardcoded palette to
  `currentColor` and the accent vars at render time, so Visual-format diagrams stay legible in
  both light and dark mode rather than rendering dark-on-dark.
- **AI-ism voice gate.** `scripts/check_ai_isms.py` (sourced from the content-pipeline Phase 4
  avoid-patterns) keeps the prose in the source blog's voice rather than drifting into generic AI
  phrasing. It is wired into the SKILL Shape phase and hard gates.
- **Comic with a real character.** The comic format draws a recurring hand-drawn SVG developer
  whose expression and prop carry a setup-tension-payoff arc, not captioned CSS boxes. Each mood
  (calm, stressed, alarmed, relieved) is a genuinely distinct face: the eyes, brows, mouth, and a
  small per-mood accent (sweat drop, shock ticks, cheek blush) all change together.

## History

Split out of the skills-toolkit plugin at v1.0.0. Earlier history (the dark-mode fix and AI-ism
gate, introduced at skills-toolkit 3.2.0) lived in that plugin's CHANGELOG before the split.

## Install

Published in the young-leaders-tech-marketplace. Add that marketplace and install the plugin:

```bash
claude plugin marketplace add YoungLeadersDotTech/young-leaders-tech-marketplace
claude plugin install enablement-html-renderer@young-leaders-tech-marketplace
```

If you want to install the skill manually instead of using the plugin marketplace, clone this
repo, go to `plugins/enablement-html-renderer/skills/enablement-html-renderer/`, and zip that
folder so `SKILL.md` sits at the root of the zip.
