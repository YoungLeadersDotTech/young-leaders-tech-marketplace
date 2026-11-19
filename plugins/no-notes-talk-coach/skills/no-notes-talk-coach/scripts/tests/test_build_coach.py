"""Tests for build_coach.py: validation, safe JSON injection, site bar preset, CLI exit codes."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))

import build_coach as bc  # noqa: E402

TEMPLATE = SCRIPTS.parent / "templates" / "no-notes-coach.html"
PRESET = SCRIPTS.parent / "reference" / "site-bar-youngleaders.json"


def talk(**over):
    base = {"talkTitle": "T", "secondsPerSlide": 15,
            "slides": [{"title": "One", "cue": "A", "lines": "First."},
                       {"title": "Two", "lines": "Second."}]}
    base.update(over)
    return base


def embedded(html: str) -> dict:
    m = re.search(r"/\*__DATA_START__\*/(.*?)/\*__DATA_END__\*/", html, re.S)
    assert m, "bundle markers missing"
    return json.loads(m.group(1))


# ---- validate ----

def test_minimal_slides_only_is_valid():
    out = bc.validate({"slides": ["Just some words."]})
    assert out["slides"][0]["lines"] == "Just some words."
    assert out["secondsPerSlide"] == 15
    assert out["talkTitle"] == "Your talk"


@pytest.mark.parametrize("bad", [None, [], "x", {"slides": []}, {"slides": "x"}, {}])
def test_rejects_missing_or_empty_slides(bad):
    with pytest.raises(bc.CoachDataError):
        bc.validate(bad)


def test_rejects_slide_with_no_text():
    with pytest.raises(bc.CoachDataError, match="slide 2"):
        bc.validate(talk(slides=[{"lines": "ok"}, {"cue": "only a cue"}]))


@pytest.mark.parametrize("sps", [2, 601, "abc", None])
def test_rejects_bad_seconds(sps):
    with pytest.raises(bc.CoachDataError):
        bc.validate(talk(secondsPerSlide=sps))


def test_rejects_chapter_pointing_at_missing_slide():
    with pytest.raises(bc.CoachDataError, match="does not exist"):
        bc.validate(talk(chapters=[{"name": "c", "slides": [1, 3]}]))


def test_rejects_slide_in_two_chapters():
    with pytest.raises(bc.CoachDataError, match="more than one chapter"):
        bc.validate(talk(chapters=[{"slides": [1]}, {"slides": [1, 2]}]))


def test_rejects_bool_slide_number():
    with pytest.raises(bc.CoachDataError):
        bc.validate(talk(chapters=[{"slides": [True]}]))


def test_rejects_half_a_plan():
    with pytest.raises(bc.CoachDataError, match="plan"):
        bc.validate(talk(plan={"tonight": ["x"]}))


def test_legacy_plan_becomes_days():
    out = bc.validate(talk(plan={"tonight": ["a", ""], "tomorrow": ["b"]}))
    assert out["plan"] == {"days": [{"name": "Tonight", "steps": ["a"]},
                                    {"name": "Tomorrow", "steps": ["b"]}]}


def test_multi_day_plan():
    days = [{"name": f"Day {i}", "steps": ["x"]} for i in range(1, 6)]
    assert len(bc.validate(talk(plan={"days": days}))["plan"]["days"]) == 5


@pytest.mark.parametrize("plan", [
    {"days": []},
    {"days": [{"name": "Mon"}]},
    {"days": [{"name": "Mon", "steps": ["", " "]}]},
    {"days": [{"steps": ["x"]}] * 15},
])
def test_rejects_bad_days(plan):
    with pytest.raises(bc.CoachDataError):
        bc.validate(talk(plan=plan))


def test_per_slide_seconds_and_time_limit():
    out = bc.validate(talk(timeLimit=600, slides=[{"lines": "a", "seconds": 90}, {"lines": "b"}]))
    assert out["timeLimit"] == 600
    assert out["slides"][0]["seconds"] == 90
    assert "seconds" not in out["slides"][1]


@pytest.mark.parametrize("bad", [{"seconds": 1}, {"seconds": "x"}, {"seconds": True}])
def test_rejects_bad_slide_seconds(bad):
    with pytest.raises(bc.CoachDataError, match="seconds"):
        bc.validate(talk(slides=[{"lines": "a", **bad}]))


def test_too_many_slides():
    with pytest.raises(bc.CoachDataError, match="too many"):
        bc.validate({"slides": ["x"] * (bc.MAX_SLIDES + 1)})


def test_unknown_fields_are_dropped():
    out = bc.validate(talk(evil="<script>", slides=[{"lines": "a", "onclick": "x"}]))
    assert "evil" not in out
    assert set(out["slides"][0]) == set(bc.SLIDE_FIELDS)  # no "seconds" key unless given


# ---- build / injection safety ----

def test_build_replaces_bundle_and_round_trips():
    html = bc.build(TEMPLATE.read_text(encoding="utf-8"), bc.validate(talk()))
    data = embedded(html)
    assert data["talkTitle"] == "T"
    assert [s["title"] for s in data["slides"]] == ["One", "Two"]
    assert html.count("/*__DATA_START__*/") == 1


def test_script_breakout_is_neutralised():
    nasty = "</script><script>alert(1)</script><!--  "
    html = bc.build(TEMPLATE.read_text(encoding="utf-8"),
                    bc.validate(talk(talkTitle=nasty)))
    bundle = re.search(r"/\*__DATA_START__\*/(.*?)/\*__DATA_END__\*/", html, re.S).group(1)
    assert "<" not in bundle
    assert " " not in bundle
    assert embedded(html)["talkTitle"] == nasty.strip()


def test_template_without_markers_is_an_error():
    with pytest.raises(bc.CoachDataError, match="markers"):
        bc.build("<html></html>", bc.validate(talk()))


def test_template_default_bundle_is_strict_json_and_valid():
    data = embedded(TEMPLATE.read_text(encoding="utf-8"))
    bc.validate(data)
    assert "siteBar" not in data, "the shipped template must not be branded by default"


# ---- site bar preset + em dashes ----

def test_preset_unwraps_nested_sitebar(tmp_path):
    bar = bc.load_site_bar(PRESET)
    assert bar["nav"] and bar["subscribe"]["url"] and bar["logo"]
    flat = tmp_path / "flat.json"
    flat.write_text(json.dumps({"name": "X", "nav": []}))
    assert bc.load_site_bar(flat)["name"] == "X"


def test_strip_em_dashes_recurses():
    out = bc.strip_em_dashes({"a": "one " + chr(0x2014) + " two", "b": ["x" + chr(0x2014) + "y"], "c": 3})
    assert out == {"a": "one - two", "b": ["x - y"], "c": 3}


# ---- CLI ----

def run_cli(tmp_path, data, *extra):
    src = tmp_path / "talk.json"
    src.write_text(json.dumps(data) if not isinstance(data, str) else data)
    out = tmp_path / "out.html"
    code = bc.main(["--data", str(src), "--out", str(out), *extra])
    return code, out


def test_cli_writes_file(tmp_path):
    code, out = run_cli(tmp_path, talk(), "--no-em-dashes", "--site-bar", str(PRESET))
    assert code == 0 and out.exists()
    assert embedded(out.read_text(encoding="utf-8"))["siteBar"]["nav"]


def test_cli_invalid_data_exits_1(tmp_path):
    code, out = run_cli(tmp_path, {"slides": []})
    assert code == 1 and not out.exists()


def test_cli_unreadable_json_exits_2(tmp_path):
    code, out = run_cli(tmp_path, "{not json")
    assert code == 2 and not out.exists()


# ---- hardening from the security review ----

def test_end_marker_in_talk_text_cannot_break_a_rebuild():
    evil = "x/*__DATA_END__*/;alert(document.domain)//"
    first = bc.build(TEMPLATE.read_text(encoding="utf-8"),
                     bc.validate(talk(slides=[{"lines": evil}])))
    assert first.count("/*__DATA_END__*/") == 1
    # feed the built page back in as a template: the bundle must still be replaced whole
    second = bc.build(first, bc.validate(talk()))
    assert "alert(document.domain)" not in second
    assert embedded(second)["talkTitle"] == "T"


def test_separators_are_escaped_not_literal():
    out = bc.to_script_json({"a": "x" + chr(0x2028) + "y" + chr(0x2029)})
    assert chr(0x2028) not in out and chr(0x2029) not in out
    assert json.loads(out)["a"] == "x" + chr(0x2028) + "y" + chr(0x2029)


@pytest.mark.parametrize("bar", [
    {"nav": "Tools"},
    {"nav": [None]},
    {"nav": [{"label": "Tools"}]},
    {"subscribe": "https://example.com"},
    {"logo": 5},
])
def test_malformed_preset_is_rejected(tmp_path, bar):
    f = tmp_path / "bar.json"
    f.write_text(json.dumps(bar))
    with pytest.raises(bc.CoachDataError):
        bc.load_site_bar(f)


def test_example_flag_only_when_explicitly_true():
    assert bc.validate(talk(example=True))["example"] is True
    assert bc.validate(talk())["example"] is False
    assert bc.validate(talk(example="yes"))["example"] is False


def test_shipped_sample_is_marked_as_example():
    assert embedded(TEMPLATE.read_text(encoding="utf-8"))["example"] is True


def test_slide_image_kept_when_valid():
    out = bc.validate(talk(slides=[{"lines": "a", "image": "slides/01.webp"}, {"lines": "b", "image": ""}]))
    assert out["slides"][0]["image"] == "slides/01.webp"
    assert "image" not in out["slides"][1]


@pytest.mark.parametrize("bad", ["../x.webp", "slides/../x.png", "https://evil/x.png", "javascript:alert(1)",
                                 "data:image/png;base64,AAA", "slides/a.svg", "/slides/a.png", "slides/a b.png", 5])
def test_rejects_bad_slide_image(bad):
    with pytest.raises(bc.CoachDataError):
        bc.validate(talk(slides=[{"lines": "a", "image": bad}]))


def test_video_kept_when_valid():
    out = bc.validate(talk(video={"youtube": "neG5uoy84ls", "title": "  My talk  "}))
    assert out["video"] == {"youtube": "neG5uoy84ls", "title": "My talk"}
    assert "video" not in bc.validate(talk())


@pytest.mark.parametrize("bad", [{"youtube": "https://youtu.be/neG5uoy84ls"}, {"youtube": "short"},
                                 {"youtube": "neG5uoy84l\""}, {"youtube": 5}, "neG5uoy84ls", {"title": "x"}])
def test_rejects_bad_video(bad):
    with pytest.raises(bc.CoachDataError):
        bc.validate(talk(video=bad))


def build_page(**kw):
    return bc.build(TEMPLATE.read_text(encoding="utf-8"), bc.validate(talk()), **kw)


def test_default_build_stays_self_contained():
    """Without --brand the page carries its own palette and system fonts and needs no site files."""
    html = build_page()
    assert "/brand.css" not in html and "/fonts/" not in html
    assert "--accent:#2f5d50" in html and "-apple-system" in html
    assert "__BRAND_" not in html


def test_brand_build_takes_colours_and_fonts_from_the_site_files():
    html = build_page(brand=True)
    assert '<link rel="stylesheet" href="/brand.css">' in html
    assert '<link rel="preload" href="/fonts/league-spartan-latin-700.woff2"' in html
    assert '<link rel="preload" href="/fonts/inter-latin-400.woff2"' in html
    assert ":root{--soft:var(--accent-soft);--good:var(--ok);}" in html
    # the built-in green palette and the system font stack are gone
    assert "--accent:#2f5d50" not in html and "-apple-system" not in html
    assert "__BRAND_" not in html


def test_brand_build_uses_the_display_font_only_on_big_headings():
    """League Spartan 700 is for large type only; small bold labels use Inter 600."""
    html = build_page(brand=True)
    for sel in (".cuecard .cw{", ".stage .bigcue{"):
        rule = html[html.index(sel):html.index("}", html.index(sel))]
        assert "font-family:var(--font-display)" in rule and "font-weight:700" in rule
    for sel in (".adhd{", "h1 .example-tag{"):
        rule = html[html.index(sel):html.index("}", html.index(sel))]
        assert "font-family:var(--font-body)" in rule and "font-weight:600" in rule


def test_both_variants_keep_the_data_and_the_script():
    for brand in (False, True):
        html = build_page(brand=brand)
        assert embedded(html)["slides"]
        assert html.count("<style>") == 1 and html.count("</style>") == 1


def test_both_variants_have_balanced_css_and_no_leftover_markers():
    for brand in (False, True):
        html = build_page(brand=brand)
        style = html[html.index("<style>"):html.index("</style>")]
        assert style.count("{") == style.count("}")
        assert style.count("/*") == style.count("*/")
        assert "__BRAND_" not in html


def test_windows_line_endings_in_the_template_still_select_one_variant():
    crlf = TEMPLATE.read_text(encoding="utf-8").replace("\n", "\r\n")
    for brand in (False, True):
        html = bc.build(crlf, bc.validate(talk()), brand=brand)
        assert "__BRAND_" not in html
        assert ("/brand.css" in html) is brand


def test_talk_text_that_looks_like_a_marker_is_left_alone():
    marker = "/*__BRAND_OFF_START__*/"
    data = bc.validate(talk(talkTitle="x\n" + marker + "\ny"))
    html = bc.build(TEMPLATE.read_text(encoding="utf-8"), data, brand=True)
    assert embedded(html)["talkTitle"].count("__BRAND_OFF_START__") == 1


def test_brand_build_has_no_sitebar_rules_the_site_component_styles_the_bar():
    """The Young Leaders site bar is one component in /brand.css; a --brand page must not carry its own."""
    html = build_page(brand=True)
    assert ".sitebar" not in html and ".sb-" not in html and "--sb-brand" not in html
    assert 'setProperty("--sb' not in html
    assert 'class="sb-sub"' in html, "the script still renders the bar markup"


def test_self_contained_build_keeps_its_own_sitebar_rules():
    html = build_page(brand=False)
    assert ".sitebar .sb-sub{" in html and "--sb-brand" in html


# Point NO_NOTES_GALLERY_TILE at tool-gallery/public/prototypes/no-notes-talk-coach in an ai-os-personal checkout.
GALLERY_PAGE = Path(os.environ.get("NO_NOTES_GALLERY_TILE", "/nonexistent"))


@pytest.mark.skipif(not (GALLERY_PAGE / "index.html").exists(), reason="set NO_NOTES_GALLERY_TILE to the gallery tile folder to run this")
def test_generator_output_matches_the_gallery_page_byte_for_byte():
    """The gallery tile is generated; a hand edit that the generator does not make would be lost on the next rebuild."""
    data = json.loads((GALLERY_PAGE / "data.json").read_text(encoding="utf-8"))
    page = bc.build(TEMPLATE.read_text(encoding="utf-8"), bc.strip_em_dashes(bc.validate(data)) | {"siteBar": bc.load_site_bar(PRESET)}, brand=True)
    assert page == (GALLERY_PAGE / "index.html").read_text(encoding="utf-8")


def test_cli_brand_flag(tmp_path):
    code, out = run_cli(tmp_path, talk(), "--brand")
    assert code == 0 and "/brand.css" in out.read_text(encoding="utf-8")
    code, out = run_cli(tmp_path, talk())
    assert code == 0 and "/brand.css" not in out.read_text(encoding="utf-8")
