# Changelog

All notable changes to the enablement-html-renderer plugin.

## [1.2.2] - 2026-06-18

### Changed
- `scripts/rasterize_diagrams.py` is now dependency-free, so the diagram-contrast hard gate
  runs in Cowork (where `pip install` is blocked) as well as Claude Code. Previously the gate
  hard-required `cairosvg` and exited 2 ("could not run") whenever it was absent, blocking
  Validate. The pass/fail was already pure-Python (luminance + saturation); `cairosvg` was only
  writing PNG previews the decision never read back.
- Preview generation is now best-effort and never affects the result: a PNG when `cairosvg`
  happens to be installed, otherwise a standalone, self-contained SVG (a full-bleed theme
  background plus the resolved diagram, opens in any browser). A failed render is reported, not
  counted as a contrast failure.
- Exit codes: `0` legible in both themes, `1` a real contrast failure, `2` only for file-not-found
  or no diagrams. The missing-dependency exit-2 path is gone.
- Updated SKILL.md and README to describe the gate honestly (dependency-free static contrast
  check with optional previews) rather than claiming PNG rasterisation via `cairosvg`.

## [1.2.1] - 2026-06-18

### Changed
- First public marketplace release in `young-leaders-tech-marketplace`.
- Sanitised marketplace metadata and install docs for public distribution.
- Kept URL auto-linking, but removed the private issue-key auto-linking so the shipped
  default stays tracker-agnostic.

## [1.2.0] - 2026-06-18

### Added
- Auto-linking at render time for `http(s)` URLs. Applies across every plain-text field
  (headings, bullets, comic text, callouts, captions, agenda, tasks) via `linkifyPlain`, and
  inside `prose` HTML via `linkifyProse` (text nodes only - never re-escapes, never re-links
  inside an existing `<a>`). Link-panel labels and `commands` code are deliberately left
  un-linkified.
- Authors no longer need to pre-build anchors: write a full URL in any field and it resolves
  itself. Removes the need to prompt for "make the links clickable".

## [1.1.0] - 2026-06-17

### Changed
- Redesigned the comic character's faces so each mood reads as a distinct emotion. The
  faces were not respecting the moods: calm and relieved were near-identical, the eyes
  never changed across moods, alarmed had flat brows, stressed read as mildly sad, and the
  hair clipped across the brows. Now the eyes, brows, mouth, and a small per-mood accent
  vary together:
  - **calm** - neutral flat brows, open eyes, gentle smile.
  - **stressed** - worried (inner-raised) brows, smaller tense eyes, open downturned
    grimace, a sweat drop by the temple.
  - **alarmed** - high arched brows, wide white-ringed eyes with pupils, an open mouth, and
    shock ticks above the head.
  - **relieved** - relaxed brows, happy upward-curved closed eyes, a broad smile, cheek blush.
  The hair is redrawn as a skullcap that hugs the head instead of floating above it.
  Internally, `FACE` now holds the per-mood mouth, with new `EYES` and `ACCENT` maps; the
  `character()` function draws accent, ears, head, hair, brows, eyes, mouth, then prop. The
  panel `mood`/`prop` contract and the comic data shape are unchanged, so existing content
  bundles render with the new faces and no migration. The character linework stays
  `#1a1a1a` on the fixed cream comic panel (dark-mode-safe by design, unchanged).

## [1.0.0] - 2026-06-17

### Added
- Initial standalone plugin. Split out from the skills-toolkit plugin into its own
  top-level plugin so it can be installed and versioned independently.
- enablement-html-renderer skill: packages finished enablement material into one
  self-contained HTML file with a reader-chosen format selector (bullets, prose,
  visual diagram, comic, copy-all cheat sheet). Severity callouts, copy-paste command
  blocks, per-section time badges, and video deep-links persist across every format.
  URL-hash deep-linking, print/PDF, offline, single file.
- Theme-aware diagrams: a `normalizeSvg` render-time pass remaps the legacy palette
  (`#1a1a1a` to `currentColor`, `#2f5d50` to `var(--accent)`, `#c4622d` to
  `var(--accent2)`) so diagrams stay legible in light and dark.
- AI-ism voice gate (`scripts/check_ai_isms.py`) so docs built from published source material keep
  that voice.
- Comic format uses a recurring hand-drawn SVG character whose expression and prop
  carry a setup-tension-payoff arc.

### Note
- History before 1.0.0 lived in the skills-toolkit plugin CHANGELOG (the dark-mode
  fix and AI-ism gate were introduced there at skills-toolkit 3.2.0 before this split).
