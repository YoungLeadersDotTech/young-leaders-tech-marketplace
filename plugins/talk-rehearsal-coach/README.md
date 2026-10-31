# talk-rehearsal-coach

**Version**: 1.0.0

Learn a talk off without notes in a day or two. Give it the talk you already have (a deck, a
script or slide notes) and the seconds per slide, and it gives you back a rehearsal pack and a
single offline HTML page to drill with.

The method is tailored for ADHD and useful for everyone. The four techniques that matter most when
focus is the bottleneck, and the timed drill, carry a small superscript **ADHD** tag, with a line
on why each one helps. The rest is good memory practice for anyone and is left untagged.

Try it without installing anything: the same page runs on
[tools.youngleaders.tech](https://tools.youngleaders.tech/), loaded with a real 20-slide example.
Paste your own script into its Your talk tab.

## What you get

- **A chapter map**: three or four chapters, each with a job, a tone and a running time, plus a
  recall chain (the first cue word of each chapter) to picture before you walk on.
- **One cue word per slide**: the single word that pulls the whole slide back.
- **The script**: your own words, by chapter, with stage anchors, pauses and a timing check that
  flags slides with more words than their seconds allow.
- **A drill**: a timer that moves the slides on like the real thing, at real, fast or slow pace, and
  a self-quiz (in order or shuffled) that remembers the slides you missed, even after you close the
  page, so you can re-drill just those.
- **A plan, as the front page**: tonight and tomorrow by default, or spread over more days. The next
  step is highlighted and each step has a button that opens the right tab.
- **Free-paced talks too**: give each slide its own time and a total limit, and the timing check
  works against the limit instead of flagging every dense slide.

## How it works

The skill runs in five phases:

| Phase | What happens |
|---|---|
| 1. Intake | Reads your deck or script, and asks for timing and the talk date if missing |
| 2. Shape | Chapters, cue words, anchors, pauses and a words-per-second timing check |
| 3. Rehearsal pack | The map and cue words in chat; the full pack as a markdown file if you want it |
| 4. HTML coach | `build_coach.py` writes one self-contained page with seven tabs |
| 5. Drill (optional) | A quick in-chat quiz: a cue word, you say the slide, it tells you what you missed |

It keeps your words. It organises and times the talk but does not rewrite it, and only suggests a
trim when a slide is over time.

## Usage

Ask in plain words, for example:

- "Help me learn my talk off, it's 20 slides at 15 seconds each" (attach the deck)
- "I'm speaking on Thursday, here's my script, can you make cue words and a drill"

To build a page yourself from a talk JSON file:

```bash
python3 skills/talk-rehearsal-coach/scripts/build_coach.py --data talk.json --out coach.html
```

Options: `--no-em-dashes` replaces em dashes with " - "; `--site-bar <preset.json>` adds a branded
header (off by default, so a coach built for someone else gets no site bar; the footer always has
a one-line credit). The JSON shape is in
`SKILL.md`, Phase 4.

## Contents

| Path | What it is |
|---|---|
| `skills/talk-rehearsal-coach/SKILL.md` | The skill |
| `skills/talk-rehearsal-coach/templates/rehearsal-coach.html` | The HTML coach template |
| `skills/talk-rehearsal-coach/scripts/build_coach.py` | Validates talk JSON and builds the page |
| `skills/talk-rehearsal-coach/scripts/tests/` | 44 pytest cases for the build script |
| `skills/talk-rehearsal-coach/reference/method.md` | The six techniques, recall chain, plan and pacing |
| `skills/talk-rehearsal-coach/reference/site-bar-youngleaders.json` | Opt-in branded header preset |

Self-contained: no dependencies on other plugins. The build script needs only Python 3 (stdlib).
In a session without Python, the skill gives you the JSON and the two-step manual paste instead.

## Testing

```bash
cd plugins/talk-rehearsal-coach && python3 -m pytest -q
```
