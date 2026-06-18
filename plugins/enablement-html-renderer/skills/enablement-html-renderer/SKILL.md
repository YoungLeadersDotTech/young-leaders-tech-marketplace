---
name: enablement-html-renderer
description: Packages finished enablement material (meeting summaries, workshop notes, training guides) into one self-contained HTML file where the reader toggles format: bullets, prose, visual diagram, or comic. Invoke to distribute knowledge. Skip for drafting.
---

# enablement-html-renderer

A handoff target, not a starting point. Other skills (meeting, content-pipeline,
diy-build-companion) produce the substance; this skill packages it into a single
HTML file a person opens anywhere and reads in the format that suits how *they*
absorb information.

The core idea: people absorb the same knowledge differently. Some want terse
bullets, some want prose, some want a diagram, some want it as a comic. Instead of
producing four artifacts, this produces one file with a format selector built in.
All four representations of the same content ship inside the file. No server, no
build step, no dependency: it is one `.html` you email, drop in a channel, or
attach to a meeting summary.

---

## When to use

- The end of a meeting, workshop, or training session, packaging the outputs for attendees.
- Distributing a "gotcha" guide, a Claude Code help guide, or a how-to across a team.
- Repackaging any already-written knowledge so recipients pick their own format.
- Another skill calls this on finish to produce the shareable artifact.

## Skip when

- The content does not exist yet. This skill renders; it does not draft. Run the
  drafting skill first (meeting, content-pipeline, learning-content-enabler), then hand here.
- A plain document is genuinely all that is wanted (a single-format `.docx`/`.md`).
- The deliverable is interactive software, not a read-to-absorb artifact.

---

## The handoff contract (how other skills call this)

A calling skill passes a **content bundle**: a small JSON or markdown object with
the source material already written. This skill never invents the substance; it
only transforms and packages what it receives. Minimum fields:

```json
{
  "title": "Claude Code gotchas, week of 16 Jun",
  "kind": "training | meeting | workshop | guide",
  "core_idea": "The one thing the reader must leave with.",
  "sections": [
    {
      "heading": "...",
      "body": "the prose source of truth for this section",
      "estMinutes": 5,
      "videoUrl": "https://loom.com/share/...?t=52",
      "callouts": [
        { "level": "critical | warn | tip | never", "text": "the one thing not to get wrong" }
      ],
      "commands": ["colima stop", "colima start"]
    }
  ],
  "agenda": ["optional list of items covered"],
  "tasks": [{ "who": "[NAME]", "what": "action", "due": "date or blank" }],
  "links": [{ "label": "Loom walkthrough", "url": "..." }]
}
```

`sections[].body` is the **source of truth**. The four prose formats are all
*derived* from it during the Shape phase, so they never contradict each other.
Optional per-section fields make the artifact match how real enablement material
reads: `estMinutes` shows a time badge, `videoUrl` adds a deep-link to the exact
moment in a recording, `callouts` carry severity (critical/warn/tip/never) that
renders consistently across every format, and `commands` are copy-paste-ready code
lines. `agenda`, `tasks`, and `links` are optional and render as their own panels.
Recordings (Loom, Zoom) belong in `links` or per-section `videoUrl` so the file
complements video rather than replacing it.

**Trusted vs escaped fields.** Two fields are authored by this skill and pass
through as HTML: `prose` (you write the paragraph markup) and each section's
`visualSvg` (you write the inline SVG). Everything else (headings, bullets, comic
scene/say text, agenda items, task text, link labels) is treated as untrusted
plain text and HTML-escaped at render time, so a code snippet like `Skill<X>` or an
ampersand shows literally instead of breaking the page or injecting markup. Link
URLs are sanitised to http/https/mailto only. Put code and angle brackets in the
escaped fields freely; reserve `prose`/`visualSvg` for markup you intend.

**Auto-linking (URLs only in the public build).** At render time the page turns any `http(s)` URL
into a real link. This runs across every plain-text field (headings, bullets, comic text,
callouts, captions, agenda, tasks) and inside `prose` HTML - in prose it only touches text nodes,
never re-escaping and never re-linking content already inside an `<a>`. Net effect: never paste a
dead URL; write the full URL in any field and it resolves itself. Link-panel `labels` are left
un-linkified to avoid nested anchors (the row already links to its `url`), and code in `commands`
is never linkified. Issue-key auto-linking is intentionally not the default in the public build,
because a shared plugin should not assume one private tracker.

**Theming `visualSvg` (so diagrams survive dark mode).** Do not hardcode near-black
or brand colours for diagram strokes and text; they vanish on a dark background.
Use `currentColor` for lines and labels (it inherits the reader's theme ink and
flips automatically) and `var(--accent)` / `var(--accent2)` for highlights. The
renderer runs a `normalizeSvg` pass that remaps the legacy palette
(`#1a1a1a` to `currentColor`, `#2f5d50` to `var(--accent)`, `#c4622d` to
`var(--accent2)`) so older diagrams flip too, but author new SVGs with
`currentColor` from the start rather than relying on the safety net. Leave
`fill='none'` alone and keep any genuinely light fills explicit.

---

## How it works (the phase model)

Every run follows the toolkit's gated phase model. Do not start a phase until the
prior gate passes.

1. **Intake** - read the content bundle (or the upstream skill's working doc) in
   full. Gate: you can state the title, kind, and core idea in one line each.
2. **Shape** - for each section, derive all four prose representations from the
   same `body`:
   - **Bullets** - 3 to 6 scannable points, business tone, no filler.
   - **Prose** - 1 to 3 short paragraphs, the same facts in connected sentences.
   - **Visual** - an inline SVG or Mermaid-style flow/relationship diagram plus a
     one-line caption (a real diagram, not a screenshot reference).
   - **Comic** - 3 to 5 panels narrating the concept as a small story using a
     recurring hand-drawn SVG character whose expression and prop change per panel
     to carry a setup-tension-payoff arc (give each panel a `mood` of
     calm/stressed/alarmed/relieved and an optional `prop` of coffee/warning/check).
     Speech bubbles, numbered tabs, comic linework; no external image dependency.
   The fifth format, **Cheat sheet**, is assembled automatically from the section
   headings, the highest-severity callouts, and the `commands` arrays into one
   copy-all reference card, mirroring how your real guides end with a copyable
   quick-reference block. Gate: every section has all four prose forms, they agree
   on the facts, and any callouts/commands are attached.

   **Voice gate (AI-isms).** Enablement docs are often built from a published blog,
   so the prose must stay in that voice, not drift into generic AI phrasing. Before
   rendering, scrub the `body`/`bullets`/`prose` of AI-isms and corporate filler:
   no "in today's rapidly evolving", "it's worth noting that", "let's dive in", "at
   the end of the day", "delve", "revolutionary", "game-changing", "seamless",
   "leverage", marketing fluff, false expertise, or excessive hedging. This mirrors
    the AI-ism removal pass in a content-cleanup workflow. Run
   `scripts/check_ai_isms.py` on the rendered file as part of Validate.
3. **Render** - emit one self-contained HTML file from the template. Gate: file
   opens standalone (no network needed), selector switches formats, prints cleanly.
4. **Validate** - run the hard gates (below) and self-check the file.
5. **Complete** - record the score in the ledger and present the file.

---

## The selector (what the recipient sees)

A single sticky control at the top: **Bullets / Prose / Visual / Comic**. Picking
one re-renders every section in that format in place. Defaults to Bullets. The
choice is reflected in the URL hash (for example `recap.html#prose`), so a sender
can share a link that opens straight into a chosen format, and the choice survives
a reload. No localStorage or sessionStorage, which break in sandboxed viewers. A
"Print / Save as PDF" button prints whatever format is showing. A small "Show all
formats" option stacks them for people who want to compare.

Accessibility floor: semantic headings, keyboard-operable selector, prefers-color
scheme respected, body text at least 16px, diagrams have text captions so the
visual format is not the only carrier of meaning.

---

## Producing the file

Read `templates/renderer-template.html` and inject the shaped content as a JS data
object. The template already contains the selector logic, the four render
functions, print styling, and the panels for agenda/tasks/links. Keep everything
inline (CSS in `<style>`, JS in `<script>`); the output must be a single file.
Write the result to `/mnt/user-data/outputs/<slug>.html` and present it.

If a format genuinely cannot be derived for a section (for example, a legal
disclaimer has no sensible comic), render that section in its best format and add a
visible note rather than faking a panel. Never claim a format that is not really there.

**Validation limits (be honest about these).** Headless DOM checks (jsdom) verify
structure, escaping, link sanitising, format switching, and the copy handler, but
they do not compute layout or rendered colour, so on their own they cannot catch
viewport problems or a diagram that renders dark-on-dark (the exact bug that shipped
twice). Two mitigations, neither a full substitute for a real open:

- For colour, run `scripts/rasterize_diagrams.py` on the rendered file (a hard gate
  below). It resolves every Visual diagram in both light and dark themes (the same
  currentColor / accent-var substitution the browser does) and fails when a diagram's
  ink would not contrast with the theme background, so a dark-on-dark regression becomes
  a loud failure instead of a silent one. The check is pure-Python with no third-party
  dependency, so it runs identically in Cowork and Claude Code.
- For layout, the format selector is the part most likely to break on a narrow phone
  screen, and nothing headless catches that. The current design keeps format pills on
  a single horizontally scrollable row (they never wrap into a thicket) with the label
  and utilities on a separate row.

Whenever the control strip or the diagram theming changes, treat a real on-device
open (phone width, dark mode toggled) as the validating signal before raising the
score. The diagram-contrast gate protects against colour regressions between those opens;
it does not replace them.

---

## Hard gates (run in Validate, all must pass)

```bash
python3 scripts/measure_frontmatter_weight.py SKILL.md     # description <= 250 chars
bash   scripts/check_em_dash.sh SKILL.md                   # no em dashes
python3 scripts/pii_scan.py SKILL.md                       # PII zero-tolerance; use [NAME] etc.
python3 scripts/check_ai_isms.py <rendered-output.html>    # voice gate: no AI-isms/corporate filler
python3 scripts/rasterize_diagrams.py <rendered-output.html>  # diagrams legible in light AND dark
```

The scripts are vendored into this plugin's own `scripts/` folder, so the skill
validates self-contained without depending on the skills-toolkit plugin.
`rasterize_diagrams.py` is dependency-free: it computes light/dark contrast in pure Python
and fails on a hardcoded near-greyscale colour that would not flip with the theme. It also
writes one preview per diagram per theme for eyeballing - a PNG if `cairosvg` happens to be
installed, otherwise a standalone SVG - but the pass/fail never depends on that optional
library, so it runs the same in Cowork and Claude Code.

Plus the two non-script gates: name-collision (this name is not a single verb and
does not collide) and artefact-type triage (this is a skill that runs on demand,
not a hook that fires on an event). Tasks carrying real attendee names must use
placeholders in any committed example; real names only in the generated output the
user keeps.

## Scoring

Record in the ledger after Validate:

```bash
python3 scripts/quality_ledger.py record --artifact SKILL.md --score <N> \
    --components "desc=..,body=..,safety=.." --findings "..."
```

Fix the lowest axis first on any rerun. Improving real behaviour (a missing format,
a print bug, a degraded-content fallback) is what should move the score, not
description padding.
