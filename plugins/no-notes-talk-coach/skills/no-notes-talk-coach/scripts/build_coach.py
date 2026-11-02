#!/usr/bin/env python3
"""Build a self-contained No-Notes Talk Coach HTML page from a talk JSON file.

Reads templates/no-notes-coach.html, validates the talk data, and replaces the
bundle between /*__DATA_START__*/ and /*__DATA_END__*/ with the new data as
strict JSON. Stdlib only.

Usage:
    python3 build_coach.py --data talk.json --out coach.html
        [--site-bar reference/site-bar-youngleaders.json]
        [--no-em-dashes]

Talk JSON shape (only "slides" is required):
    {
      "talkTitle": "When Things Go Wrong",
      "secondsPerSlide": 15,
      "intro": "One line shown under the title.",
      "chapters": [{"name": "The problem", "tone": "calm", "slides": [1, 2, 3]}],
      "timeLimit": 300,
      "slides": [{"title": "True story", "cue": "Fax", "lines": "...",
                  "anchor": "Left of stage", "pause": "After 'faxed it in'",
                  "seconds": 20}],
      "plan": {"days": [{"name": "Tonight", "steps": ["..."]},
                        {"name": "Tomorrow", "steps": ["..."]}]}
    }

"seconds" on a slide overrides secondsPerSlide for that slide (free-paced talks).
"image" on a slide (optional) is a picture of the slide, shipped next to the page as
slides/<name>.webp (or .jpg/.png): it shows as a thumbnail on the Map and on the
back of the cue card. Only set it when the user supplies slide images.
"video" (optional) is {"youtube": "<11-character id>", "title": "..."}: a recording of
the talk, shown click-to-load on the Script tab of an example talk only.
"timeLimit" is the total allowed, in seconds. "example": true marks a demo talk
(the page then says so up front, with a button to start your own); never set it
for a user's own talk. "plan" also accepts the older
{"tonight": [...], "tomorrow": [...]} shape.

Exit codes: 0 written, 1 invalid data, 2 bad arguments or unreadable files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "templates" / "no-notes-coach.html"
DATA_RE = re.compile(r"/\*__DATA_START__\*/.*?/\*__DATA_END__\*/", re.S)
SLIDE_FIELDS = ("title", "cue", "lines", "anchor", "pause")
# A slide image is a file shipped next to the page: slides/<name>.webp|jpg|jpeg|png, nothing else.
YOUTUBE_ID_RE = re.compile(r"[A-Za-z0-9_-]{11}")
IMAGE_RE = re.compile(r"slides/[A-Za-z0-9_-]{1,64}\.(?:webp|jpe?g|png)")
MAX_SLIDES = 200
MAX_PLAN_DAYS = 14
EM_DASH = chr(0x2014)


class CoachDataError(ValueError):
    """Raised when the talk data cannot produce a usable coach page."""


def _text(value: object) -> str:
    return "" if value is None else str(value).strip()


def _seconds(value: object, label: str, lo: int, hi: int) -> int:
    if isinstance(value, bool):
        raise CoachDataError(f"{label} must be a whole number")
    try:
        n = int(value)
    except (TypeError, ValueError):
        raise CoachDataError(f"{label} must be a whole number") from None
    if not lo <= n <= hi:
        raise CoachDataError(f"{label} must be between {lo} and {hi}")
    return n


def _plan(plan: object) -> dict:
    """Normalise a plan to {"days": [{"name", "steps"}]}, accepting the older tonight/tomorrow shape."""
    if isinstance(plan, dict) and isinstance(plan.get("tonight"), list) and isinstance(plan.get("tomorrow"), list):
        plan = {"days": [{"name": "Tonight", "steps": plan["tonight"]},
                         {"name": "Tomorrow", "steps": plan["tomorrow"]}]}
    if not (isinstance(plan, dict) and isinstance(plan.get("days"), list) and plan["days"]):
        raise CoachDataError("'plan' needs a non-empty 'days' list (or 'tonight' and 'tomorrow' lists)")
    if len(plan["days"]) > MAX_PLAN_DAYS:
        raise CoachDataError(f"'plan' has more than {MAX_PLAN_DAYS} days")
    days = []
    for i, day in enumerate(plan["days"], start=1):
        if not (isinstance(day, dict) and isinstance(day.get("steps"), list)):
            raise CoachDataError(f"plan day {i} needs a 'steps' list")
        steps = [_text(x) for x in day["steps"] if _text(x)]
        if not steps:
            raise CoachDataError(f"plan day {i} has no steps")
        days.append({"name": _text(day.get("name")) or f"Day {i}", "steps": steps})
    return {"days": days}


def validate(data: object) -> dict:
    """Return a cleaned copy of the talk data, or raise CoachDataError."""
    if not isinstance(data, dict):
        raise CoachDataError("talk data must be a JSON object")
    slides = data.get("slides")
    if not isinstance(slides, list) or not slides:
        raise CoachDataError("'slides' must be a non-empty list")
    if len(slides) > MAX_SLIDES:
        raise CoachDataError(f"too many slides ({len(slides)}), the limit is {MAX_SLIDES}")

    clean_slides = []
    for i, slide in enumerate(slides, start=1):
        if isinstance(slide, str):
            slide = {"lines": slide}
        if not isinstance(slide, dict):
            raise CoachDataError(f"slide {i} must be an object or a string")
        cleaned = {k: _text(slide.get(k)) for k in SLIDE_FIELDS}
        if not (cleaned["lines"] or cleaned["title"]):
            raise CoachDataError(f"slide {i} has neither 'lines' nor 'title'")
        if slide.get("seconds") is not None:
            cleaned["seconds"] = _seconds(slide["seconds"], f"slide {i} 'seconds'", 3, 600)
        if slide.get("image") not in (None, ""):
            image = slide["image"]
            if not (isinstance(image, str) and IMAGE_RE.fullmatch(image)):
                raise CoachDataError(f"slide {i} 'image' must look like slides/01.webp (webp, jpg or png in a slides/ folder next to the page)")
            cleaned["image"] = image
        clean_slides.append(cleaned)

    out: dict = {
        "title": _text(data.get("title")) or "No-Notes Talk Coach",
        "talkTitle": _text(data.get("talkTitle")) or "Your talk",
        "intro": _text(data.get("intro")),
        # Only the shipped demo talks set this: it shows the "This is an example" banner.
        "example": data.get("example") is True,
        "slides": clean_slides,
    }

    video = data.get("video")
    if video is not None:
        if not isinstance(video, dict) or not isinstance(video.get("youtube"), str) or not YOUTUBE_ID_RE.fullmatch(video["youtube"]):
            raise CoachDataError("'video' must be {\"youtube\": \"<11-character video id>\", \"title\": \"...\"}: the id only, never a URL")
        out["video"] = {"youtube": video["youtube"], "title": _text(video.get("title"))[:120]}

    out["secondsPerSlide"] = _seconds(data.get("secondsPerSlide", 15), "'secondsPerSlide'", 3, 600)
    if data.get("timeLimit") is not None:
        out["timeLimit"] = _seconds(data["timeLimit"], "'timeLimit'", 10, 36000)

    chapters = data.get("chapters")
    if chapters is not None:
        if not isinstance(chapters, list):
            raise CoachDataError("'chapters' must be a list")
        n = len(clean_slides)
        seen: set[int] = set()
        clean_ch = []
        for j, ch in enumerate(chapters, start=1):
            if not isinstance(ch, dict):
                raise CoachDataError(f"chapter {j} must be an object")
            nums = ch.get("slides")
            if not isinstance(nums, list) or not nums:
                raise CoachDataError(f"chapter {j} needs a non-empty 'slides' list")
            for x in nums:
                if not isinstance(x, int) or isinstance(x, bool) or not 1 <= x <= n:
                    raise CoachDataError(f"chapter {j} refers to slide {x!r}, which does not exist")
                if x in seen:
                    raise CoachDataError(f"slide {x} is in more than one chapter")
                seen.add(x)
            clean_ch.append({"name": _text(ch.get("name")) or f"Chapter {j}",
                             "tone": _text(ch.get("tone")), "slides": nums})
        out["chapters"] = clean_ch

    plan = data.get("plan")
    if plan is not None:
        out["plan"] = _plan(plan)

    return out


def load_site_bar(path: Path) -> dict:
    """Load a site-bar preset. Accepts the bare bar object or {"siteBar": {...}}.

    The shape is checked here because the page builds the bar at load time, and a
    malformed preset (a non-list nav, a null entry) would stop the whole page rendering.
    """
    bar = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(bar, dict) and isinstance(bar.get("siteBar"), dict):
        bar = bar["siteBar"]
    if not isinstance(bar, dict):
        raise CoachDataError("site-bar preset must be a JSON object")
    for key in ("name", "homeUrl", "logo", "brandColor"):
        if key in bar and not isinstance(bar[key], str):
            raise CoachDataError(f"site-bar '{key}' must be a string")
    nav = bar.get("nav", [])
    if not isinstance(nav, list) or not all(
            isinstance(n, dict) and isinstance(n.get("label"), str) and isinstance(n.get("url"), str)
            for n in nav):
        raise CoachDataError("site-bar 'nav' must be a list of {label, url} objects")
    sub = bar.get("subscribe")
    if sub is not None and not (isinstance(sub, dict) and isinstance(sub.get("url"), str)):
        raise CoachDataError("site-bar 'subscribe' must be an object with a 'url' string")
    return bar


def strip_em_dashes(obj):
    """Recursively replace em dashes with ' - ' in every string."""
    if isinstance(obj, str):
        return re.sub(r"\s*\u2014\s*", " - ", obj)
    if isinstance(obj, list):
        return [strip_em_dashes(x) for x in obj]
    if isinstance(obj, dict):
        return {k: strip_em_dashes(v) for k, v in obj.items()}
    return obj


def to_script_json(data: dict) -> str:
    """Serialise as strict JSON that is also safe inside a <script> element.

    Every '<' becomes \\u003c, so no value can close the script tag or open a
    comment. Every '/' becomes \\/, so no value can contain the end-of-bundle
    marker and break a later rebuild. Line and paragraph separators are escaped
    for older JS engines.
    """
    text = json.dumps(data, ensure_ascii=False)
    return (text.replace("<", "\\u003c")
                .replace("/", "\\/")
                .replace(chr(0x2028), "\\u2028")
                .replace(chr(0x2029), "\\u2029"))


def build(template_html: str, data: dict) -> str:
    if not DATA_RE.search(template_html):
        raise CoachDataError("template has no /*__DATA_START__*/ ... /*__DATA_END__*/ markers")
    bundle = "/*__DATA_START__*/" + to_script_json(data) + "/*__DATA_END__*/"
    return DATA_RE.sub(lambda _m: bundle, template_html, count=1)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", required=True, type=Path, help="talk JSON file")
    ap.add_argument("--out", required=True, type=Path, help="where to write the HTML page")
    ap.add_argument("--template", type=Path, default=TEMPLATE)
    ap.add_argument("--site-bar", type=Path, help="optional branded site-bar preset JSON")
    ap.add_argument("--no-em-dashes", action="store_true",
                    help="replace em dashes with ' - ' in every text field")
    args = ap.parse_args(argv)

    try:
        raw = json.loads(args.data.read_text(encoding="utf-8"))
        template_html = args.template.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    try:
        data = validate(raw)
        if args.site_bar:
            data["siteBar"] = load_site_bar(args.site_bar)
        if args.no_em_dashes:
            data = strip_em_dashes(data)
        html = build(template_html, data)
    except (CoachDataError, OSError, ValueError) as exc:
        print(f"invalid: {exc}", file=sys.stderr)
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8")
    dashes = json.dumps(data, ensure_ascii=False).count(EM_DASH)
    print(f"wrote {args.out} ({len(data['slides'])} slides, {data['secondsPerSlide']}s each)")
    if dashes:
        print(f"note: {dashes} em dash(es) in the talk text; pass --no-em-dashes to replace them")
    return 0


if __name__ == "__main__":
    sys.exit(main())
