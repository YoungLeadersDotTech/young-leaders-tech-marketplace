---
name: enablement-html-renderer
description: Packages finished enablement material into a multi-format HTML handoff. Always writes one offline .html file and can also emit a generic Apps Script web app bundle. Use for distribution, not drafting.
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion]
version: 1.0.0
---

# enablement-html-renderer

A handoff target, not a starting point. Other drafting workflows produce the
substance; this skill packages it into a single
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
- You want a hosted share path as well as the offline file, using a generic Apps Script web app.

## Skip when

- The content does not exist yet. This skill renders; it does not draft. Run the
  drafting workflow first, then hand here.
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
      "commands": ["colima stop", "colima start"],
      "images": [
        { "src": "data:image/png;base64,iVBORw0KGgo...", "alt": "the login screen", "caption": "Where the SSO button lives" }
      ]
    }
  ],
  "agenda": ["optional list of items covered"],
  "tasks": [{ "who": "[NAME]", "what": "action", "due": "date or blank" }],
  "links": [{ "label": "Loom walkthrough", "url": "..." }],
  "siteBar": {
    "name": "Young Leaders in Tech",
    "homeUrl": "https://www.youngleaders.tech/",
    "logo": "data:image/png;base64,... (or an https URL)",
    "brandColor": "#990101",
    "nav": [{ "label": "Blog", "url": "https://www.youngleaders.tech/" }],
    "subscribe": { "label": "Subscribe", "url": "https://..." }
  }
}
```

### Branded site bar (opt-out) and attribution

`siteBar` is **optional**. When present, the renderer draws a top bar - logo linking home, an
optional centred wordmark, `nav` links, and a Subscribe button - above the content. When it is
**absent, no bar renders**, so third-party content is never force-branded. `brandColor` styles the
button and active nav (defaults to `#990101`); the logo and URLs pass through the same image/URL
sanitisers as every other field.

Behaviour when this skill runs: **ask the operator each render whether to include the branded bar**
(AskUserQuestion, default *include* - it is opt-out). On include, inject the operator's preset -
for John that is `references/site-bar-youngleaders.json` - into `siteBar`. On decline, omit it.

Separately, every render carries a permanent footer credit - "Created using enablement-html-renderer
from youngleaders.tech" - which is **always present and not configurable**.

`sections[].body` is the **source of truth**. The four prose formats are all
*derived* from it during the Shape phase, so they never contradict each other.
Optional per-section fields make the artifact match how real enablement material
reads: `estMinutes` shows a time badge, `videoUrl` adds a deep-link to the exact
moment in a recording, `callouts` carry severity (critical/warn/tip/never) that
renders consistently across every format, and `commands` are copy-paste-ready code
lines. `agenda`, `tasks`, and `links` are optional and render as their own panels.
Recordings (Loom, Zoom) belong in `links` or per-section `videoUrl` so the file
complements video rather than replacing it.

**Images (real screenshots or supplied art).** Images are the big lever on content quality - a
real screenshot of the actual screen next to the words that explain it beats any amount of text,
and many callers already have images to hand (a published blog with inline shots, a workshop deck,
a product UI capture). There is **no cap on how many** and **no fixed slot**: put as many images as
the content needs, wherever they belong. You decide placement from what you are asked to illustrate.
Each image is `{ src, alt, caption }`. Three ways to place them, mix freely:

- **Attach to a section** - `section.images: [ {src,alt,caption}, ... ]`. A convenience for "here
  are the shots for this section". Renders together near the top of the section. Any number.
- **Interleave with bullets** - a `bullets` entry can be a string (text) or an object: `{text}` is a
  text bullet, `{img}` (or `{image}`) is a standalone image, `{text, img}` is a bullet followed by
  its image. Order is preserved, so an image can sit before, after or between any bullets - e.g. one
  screenshot per point.
- **Inline in prose** - `prose` is authored HTML, so drop an `<img src="...">` (or a `<figure>` with
  a `<figcaption>`) anywhere in the paragraph flow, including between two sentences. If the prose is
  five or six sentences, that can be one image per sentence. The renderer styles `.prose img`.

`src` takes an `http(s)` URL (already-online content, kept as-is) or a `data:image/*;base64` URI
(local files, inlined so the file stays one offline artifact). Run `scripts/img_to_datauri.py --json
shot.png ...` to convert local images into paste-ready entries. `src` is sanitised at render time to
`data:image/*` or `http(s)` only; `alt`/`caption` are escaped plain text (in bullets/section images).

Keep embedded weight sane: base64 inflates by ~34%, so many multi-MB images in one file adds up -
size them for the web first if you are inlining a lot. During Shape, look for images the caller
already has before drawing a `visualSvg` from scratch; a genuine screenshot usually beats a diagram,
and the two can coexist (screenshot for the real thing, SVG for the abstract flow).

**Trusted vs escaped fields.** Two fields are authored by this skill and pass
through as HTML: `prose` (you write the paragraph markup) and each section's
`visualSvg` (you write the inline SVG). Everything else (headings, bullets, comic
scene/say text, agenda items, task text, link labels) is treated as untrusted
plain text and HTML-escaped at render time, so a code snippet like `Skill<X>` or an
ampersand shows literally instead of breaking the page or injecting markup. Link
URLs are sanitised to http/https/mailto only. Put code and angle brackets in the
escaped fields freely; reserve `prose`/`visualSvg` for markup you intend.

**Auto-linking (URLs only in the shared build).** At render time the page turns any `http(s)` URL
into a real link. This runs across every plain-text field (headings, bullets, comic text,
callouts, captions, agenda, tasks) and inside `prose` HTML - in prose it only touches text nodes,
never re-escaping and never re-linking content already inside an `<a>`. Net effect: never paste a
dead URL; write the full URL in any field and it resolves itself. Link-panel `labels` are left
un-linkified to avoid nested anchors (the row already links to its `url`), and code in `commands`
is never linkified. Issue-key auto-linking is intentionally not the default in the shared build,
because a shared plugin should not assume one tracker.

**Theming `visualSvg` (so diagrams survive dark mode).** Do not hardcode near-black
or brand colours for diagram strokes and text; they vanish on a dark background.
Use `currentColor` for lines and labels (it inherits the reader's theme ink and
flips automatically) and `var(--accent)` / `var(--accent2)` for highlights. The
renderer runs a `normalizeSvg` pass that remaps the legacy palette
(`#1a1a1a` to `currentColor`, `#2f5d50` to `var(--accent)`, `#c4622d` to
`var(--accent2)`) so older diagrams flip too, but author new SVGs with
`currentColor` from the start rather than relying on the safety net. Leave
`fill='none'` alone and keep any genuinely light fills explicit.

**Sizing `visualSvg` (avoid text clipping).** Every text x-coordinate and string
length must fit within the SVG's own declared `viewBox` width - text that runs
past the right edge of the `viewBox` gets clipped in the Visual tab. Example
failure: `viewBox="0 0 320 160"` with a `<text x="280">Automate & Optimize
Immediately</text>` - the label is far wider than the 40px of `viewBox` left
after `x="280"`, so most of it is cut off. Fix by widening the `viewBox` to fit
the longest label, or by wrapping/shortening the text so it fits the declared
width. The renderer's `.visual svg` rule sets `overflow:visible` as a safety
net (ported from `toast-ai-os-standalone-skills` Phase 3) so out-of-bounds
content is not hard-clipped by the browser, but a correctly-sized `viewBox` is
still the right fix - `overflow:visible` only prevents the worst case, it does
not make mis-sized text look intentional.

---

## How it works

Use the following working order and self-check each step before you move on.

1. **Intake** - read the content bundle (or the upstream skill's working doc) in
   full. You should be able to restate the title, kind, and core idea in one line each.
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
    quick-reference block. Every section should have all four prose forms, or an
    explicit visible fallback note for any format that genuinely does not fit, they
    should agree on the facts, and any callouts/commands should be attached.

    **Voice gate (AI-isms).** Enablement docs are often built from a published blog,
    so the displayed prose must stay in that voice, not drift into generic AI
    phrasing. Treat `body` as source input, not something to rewrite in place.
    Before rendering, scrub the derived `bullets`/`prose` of AI-isms and corporate filler:
   no "in today's rapidly evolving", "it's worth noting that", "let's dive in", "at
   the end of the day", "delve", "revolutionary", "game-changing", "seamless",
   "leverage", marketing fluff, false expertise, or excessive hedging. This mirrors
    the AI-ism removal pass in a content-cleanup workflow. Run
     `scripts/check_ai_isms.py`
     on the rendered file as part of Validate.
3. **Render** - emit one self-contained HTML file from the template, and optionally
   a generic Apps Script web app bundle from the same rendered source. The
   offline file should open standalone (no network needed), the selector should switch
   formats, it should print cleanly, and the hosted bundle should be structurally
   ready to deploy.
4. **Validate** - run the hard gates (below) and self-check the file.
5. **Complete** - present the offline file, the hosted bundle if requested, and any
   live `/exec` URL only when you actually deployed it.

---

## The selector (what the recipient sees)

A single sticky control at the top: **Bullets / Prose / Visual / Comic / Cheat
sheet**. Picking one re-renders every section in that format in place. Defaults to
Bullets. The
offline file reflects the choice in the URL hash (for example `recap.html#prose`).
The hosted Apps Script path should honour top-level `#prose` and `?fmt=prose`
links by using the Apps Script browser APIs (`google.script.url` and
`google.script.history`) rather than trusting the iframe's own `window.location`.
No localStorage or sessionStorage, which break in sandboxed viewers. A
"Print / Save as PDF" button prints whatever format is showing. A small "Show all
formats" option stacks them for people who want to compare.

Accessibility floor: semantic headings, keyboard-operable selector, prefers-color
scheme respected, body text at least 16px, diagrams have text captions so the
visual format is not the only carrier of meaning.

---

## Producing the file

All `templates/...` and `scripts/...` paths below are relative to **this skill
directory**. In a downloaded standalone zip, that means the folder containing
`SKILL.md`. In a plugin checkout, resolve them from
`plugins/enablement-html-renderer/skills/enablement-html-renderer/`.

Read `templates/renderer-template.html`
and inject the shaped content as a JS data object. The template already contains the selector logic, the four render
functions, print styling, and the panels for agenda/tasks/links. Keep everything
inline (CSS in `<style>`, JS in `<script>`); the offline output must remain a
single file.

**Replace the `__TITLE__` placeholder in BOTH locations** - the static `<title>__TITLE__</title>`
tag near the top of `<head>` AND the `<h1 id="title">__TITLE__</h1>` body heading. The template's
JS `document.title = DATA.title || document.title` assignment corrects the browser tab after
script execution, but never touches the static `<title>` tag - anything that reads the raw HTML
without executing JS (curl/view-source, some social-preview scrapers, or a brief flash of the
placeholder before JS runs in a real browser) still sees the literal `__TITLE__` string if it
isn't substituted at generation time.

In Cowork-style sandboxes, write the offline fallback to
`/mnt/user-data/outputs/<slug>.html`. Outside that environment, write to the
caller's requested output directory or another explicit local path and report the
exact location.

When the caller wants the hosted path too, also write a bundle directory at
`/mnt/user-data/outputs/<slug>-gas/` in Cowork-style sandboxes, or the matching
local output directory elsewhere, containing:

- `Index.html` - the same rendered HTML artifact, adapted for HtmlService hosting.
- `Code.gs` - copied from `templates/gas/Code.gs`.
- `appsscript.json` - copied from `templates/gas/appsscript.json`. Default access is `ANYONE` for public sharing; override to `DOMAIN` if deploying within a Google Workspace.
- `gas-deploy.sh` - copied from `scripts/gas-deploy.sh` so the bundle can be
  deployed in place.

**Access level gate (required before writing appsscript.json).** When the caller requests a hosted bundle, always ask which audience should access the deployed web app before writing `appsscript.json`:

```
AskUserQuestion:
  header: "Who should be able to open the hosted web app?"
  options:
    A) Anyone with the link (ANYONE) - for personal or fully public sharing
       description: "Any Google account can open the URL. Note: managed corporate devices may block exec URLs from personal accounts even with ANYONE access."
    B) My Google Workspace domain (DOMAIN) - for mixed or managed-device audiences
       description: "Anyone in your Google Workspace can open the URL. Also works from managed/corporate devices."
```

If the user skips or dismisses without answering, stop and surface an error:
`"webapp.access must be set before generating the bundle. Please choose ANYONE or DOMAIN."`
Never silently default - the choice must be explicit.

**Important - managed device constraint**: Google Workspace MDM policies can block `script.google.com` exec URLs deployed from personal (non-Workspace) accounts, even when `access: ANYONE` is set. If any viewer may be on a managed corporate device, deploy from a Google Workspace account with `DOMAIN` access instead.

Write the chosen value into `appsscript.json` before copying it into the bundle.
If `GAS_WEBAPP_ACCESS` is already set in the environment, use that value and skip the question (non-interactive context).

**Note for Google Workspace deployers**: clasp may print "ANYONE access has been disabled" even when deployment succeeds - this is a CLI quirk. Check `clasp deployments` for the actual result.

Do not add Toast, AWS, region, CMA, agent, secret, or external-request logic. The
bundle is only the static-hosting layer around the same renderer.

**Claude Code deploy path.** If `clasp` is available and authenticated, you may run
the bundled deploy helper or the equivalent explicit `clasp` commands for real.
Return a live `/exec` URL only after the deploy actually succeeded.

**Cowork sandbox path.** Always write the bundle, plus print the exact `clasp`
commands the user should run later. Never imply a live deployment exists when you
did not perform one.

**DOMAIN deployments use a different URL format.** When a web app is deployed with
`DOMAIN` access from a Google Workspace account, the working URL includes the tenant
path segment and looks like:
`https://script.google.com/a/macros/<workspace-domain>/s/<deployment-id>/exec`
The plain `/macros/s/.../exec` form redirects Workspace users to a login wall.
Always use the `/a/macros/<domain>/` form when sharing DOMAIN-access apps.
The deployment ID is the same; only the URL prefix changes.

**Sharing note (include every time you present an exec URL to the user):**

> **Before sharing this link**, note that some recipients may see an error page
> ("unable to open file" or similar) if their organisation's IT policy blocks
> Google Apps Script web apps. This is a Google Workspace MDM restriction, not a
> problem with the link itself. If a recipient can't open it:
> - Ask them to try on a personal (non-work) device or browser profile
> - Or redeploy with `DOMAIN` access from a shared Google Workspace account they have access to
> - The offline `.html` file always works as a fallback - attach it directly

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
open (phone width, dark mode toggled) as the validating signal before raising
confidence. The diagram-contrast gate protects against colour regressions between
those opens; it does not replace them.

For the hosted Apps Script path, do one real deploy before shipping the feature and
open the `/exec` URL. Specifically confirm whether the format selector still works
through direct links and whether the Print button behaves usefully inside
HtmlService. In the validated path, direct links work when the hosted page reads the
outer `/exec` URL through the Apps Script browser APIs, and the Print button still
calls `window.print()` from inside the iframe. If a tenant policy blocks broader
access levels like `ANYONE` or `ANYONE_ANONYMOUS`, keep the default `DOMAIN` flow or
fall back to `MYSELF` and say so plainly.

---

## Hard gates (run in Validate, all must pass)

Run these from the skill directory, or resolve the same relative paths from the
skill root explicitly.

```bash
python3 scripts/measure_frontmatter_weight.py SKILL.md
bash   scripts/check_em_dash.sh SKILL.md
python3 scripts/pii_scan.py SKILL.md
python3 scripts/check_ai_isms.py <rendered-output.html>
python3 scripts/rasterize_diagrams.py <rendered-output.html>
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

## Final honesty check

Do not claim the hosted path is live unless you actually ran the deploy and opened
the resulting `/exec` URL. If `clasp` is unavailable, unauthenticated, or blocked,
say so plainly and leave the user with the offline file plus the exact bundle path
and commands.
