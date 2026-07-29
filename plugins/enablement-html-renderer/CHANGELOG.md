# Changelog

All notable changes to the enablement-html-renderer plugin.

## [1.5.4] - 2026-07-29

### Added
- `templates/renderer-structure-contract.json` - a versioned "expected structure" manifest
  naming the 5 structural features a rendered artifact should have (format selector, interleaved
  images, dark-mode toggle + `normalizeSvg`, URL auto-linking, theme-variable accent palette) with
  a detection rule per feature. Feeds the KTLO B-01 drift checker being built in `ai-os-personal`
  (`toast-plugin-validator`, tracked in `ai-os-personal-ktlo--2026-07-28`) so already-shipped
  enablement artifacts can be checked against the current template without hand-auditing each one.
- `scripts/tests/test_structure_contract.py` - self-consistency test proving every detection rule
  in the new manifest actually matches the current template (pytest, stdlib-only).

### Fixed
- **VERSION regression (1.5.1 -> 1.3.1 -> 1.3.2), now corrected.** PR #41 (2026-07-21) bundled an
  unrelated fix from a branch that had diverged before the 1.4.0/1.5.0/1.5.1 work landed; merging
  it silently reset `VERSION` from `1.5.1` to `1.3.1` and deleted the CHANGELOG entries for those
  three releases (manual light/dark toggle, section images, spacing). PR #45 (2026-07-27)
  continued forward from the wrong number to `1.3.2`, compounding it. Both PRs' real content was
  valid and is kept below, renumbered `1.5.2` and `1.5.3` in correct chronological order. The three
  deleted CHANGELOG entries (`1.4.0`, `1.5.0`, `1.5.1`) are restored verbatim from their original
  commits (`2be6cac`, `2de8422`, `deb332d`). Found while grounding the new structure-contract
  manifest in this file's real feature/version history (`git log --follow` disagreed with the
  `VERSION` file); fixed here since it directly blocked writing an honest `introduced_in` field
  for every feature in the manifest above.

## [1.5.3] - 2026-07-27

### Fixed
- Document DOMAIN URL tenant-path requirement: DOMAIN-access GAS web apps require `/a/macros/<workspace-domain>/s/.../exec`; plain `/macros/s/...` form redirects Workspace users to a login wall.
- (Originally mislabeled `1.3.2` - see the `1.5.4` entry above for why.)

## [1.5.2] - 2026-07-21

### Changed
- Add sharing note: warn users that managed corporate devices may block GAS exec URLs from personal accounts; recommend offline .html as fallback.
- Improve access-level gate description to surface managed-device risk.
- (Originally mislabeled `1.3.1` - see the `1.5.4` entry above for why.)

## [1.5.1] - 2026-07-18

### Changed
- **More generous vertical spacing throughout the rendered file.** The default rhythm was tight,
  so sections, headings, callouts, command blocks, cards, figures and the footer now sit with more
  breathing room. Specifics: body line-height 1.65 to 1.7; page padding and header padding opened
  up; per-section padding 24px to 40px; selector bar padding increased; callout and command-block
  margins 0.5em to 0.85em; meta/cheat-sheet card padding 16px to 22px/24px and grid gap 20px to
  24px; comic panel gap 14px to 18px; more space above the footer. Purely presentational: the
  content bundle contract, every format, and all hard gates (AI-ism, diagram contrast) are
  unchanged, so existing bundles render identically apart from the looser spacing.

## [1.5.0] - 2026-07-13

### Added
- **Images, any number, placed anywhere.** No cap and no fixed slot. Three placements, mix freely:
  attach to a section (`section.images: [...]`), interleave with bullets (a `bullets` entry may be
  `"text"`, `{img}`, or `{text, img}`, so an image can sit before/after/between any bullets), or
  inline in `prose` (drop an `<img>` anywhere in the paragraph flow, down to one per sentence).
  `src` accepts an `http(s)` URL (already-online, kept as-is) or a `data:image/*;base64` URI (local
  files, inlined so the file stays offline). Sanitised to those two schemes; `alt`/`caption` escaped.
- `scripts/img_to_datauri.py` - converts local images into a ready-to-paste `images` JSON array
  of base64 data URIs. Dependency-free.

### Why
- A genuine screenshot of the actual screen beats any amount of prose or a drawn diagram, and
  many callers already have images to hand (a published blog, a workshop deck, a UI capture).
  The renderer previously had no way to carry them, so that quality was lost at packaging time.

## [1.4.0] - 2026-07-08

### Added
- Manual light/dark toggle button in the toolbar. Theme previously only followed the OS via
  `prefers-color-scheme`. The toggle sets `data-theme` on `<html>` (wins over the OS preference
  in either direction) and persists the choice in `localStorage`, applied before first paint via
  a head script so there is no flash back to the OS default.

## [1.3.0] - 2026-07-03

### Added
- GAS template assets: `templates/gas/Code.gs`, `templates/gas/appsscript.json`, `scripts/gas-deploy.sh`
- AskUserQuestion access-level gate before generating the Apps Script bundle (required, explicit error if skipped)

### Changed
- Default `webapp.access` changed from `DOMAIN` to `ANYONE` for public/cross-domain sharing
- AskUserQuestion option order: ANYONE first (recommended), DOMAIN second
- Added note about Google Workspace domain policy blocking ANYONE - clasp error message is misleading; check `clasp deployments` for actual result

Port-back from `toast-ai-os-standalone-skills` v1.1.0. Standalone-skills retains `DOMAIN` default for internal Toast use.

## [1.2.3] - 2026-06-19

### Changed
- Reworded the remaining tracker-specific public docs so the shipped plugin stays generic and does
  not imply one internal issue tracker.

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
- Kept URL auto-linking, but removed the tracker-specific issue-key auto-linking so the shipped
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
