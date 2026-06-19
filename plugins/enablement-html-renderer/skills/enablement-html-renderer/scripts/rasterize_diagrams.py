#!/usr/bin/env python3
"""
rasterize_diagrams.py - catch Visual-format colour regressions that headless DOM tests miss.

jsdom verifies structure and escaping but does not compute rendered colour, so it cannot
see a diagram that renders dark-on-dark (the exact bug that shipped twice). This script
extracts every Visual diagram from a rendered enablement HTML file, resolves both the
light and dark themes the way the browser would (substituting currentColor and the CSS
vars), and runs a coarse legibility check: the diagram ink, and any colour the author
hardcoded, must contrast with the theme background.

The pass/fail decision is pure-Python arithmetic (luminance + saturation) with NO third-party
dependency, so it runs the same in Cowork and in Claude Code. For optional human inspection it
also writes one preview per diagram per theme: a PNG if cairosvg happens to be installed,
otherwise a standalone, self-contained SVG (opens in any browser, no install). Preview
generation never affects the gate result - a missing library or a failed render is reported,
not counted as a contrast failure.

It is a safety net, not a substitute for a real on-device open, but it turns a silent visual
regression into a loud failure during Validate.

Usage:
    python3 rasterize_diagrams.py <rendered-output.html> [--out /tmp/diag]
Exit codes:
    0 = every diagram legible in both themes
    1 = a diagram failed the contrast check in at least one theme
    2 = could not run (file not found, or no diagrams to check)
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

# Theme colour maps, mirroring the template :root and the dark media query.
LIGHT = {"ink": "#1a1a1a", "accent": "#2f5d50", "accent2": "#c4622d", "bg": "#fafaf8", "panel": "#ffffff"}
DARK = {"ink": "#ececec", "accent": "#7fb3a3", "accent2": "#e0915f", "bg": "#16161a", "panel": "#1e1e24"}

# Contrast gap (difference in relative luminance, 0..1) below which ink is treated as
# illegible against the background. A near-greyscale hardcoded colour under this gap is the
# dark-on-dark (or light-on-light) risk; saturated semantic marks are exempt (see saturation).
CONTRAST_MIN = 0.25
SATURATION_MAX = 0.25


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def saturation(hex_colour: str) -> float:
    # HSL saturation proxy: how chromatic the colour is. Saturated colours (a red mark,
    # a green tick) stay legible on both light and dark backgrounds, so they are not the
    # dark-on-dark risk; only near-greyscale dark inks are. This keeps the gate from
    # false-flagging deliberate semantic colours.
    h = hex_colour.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    mx, mn = max(r, g, b), min(r, g, b)
    if mx == mn:
        return 0.0
    l = (mx + mn) / 2
    return (mx - mn) / (1 - abs(2 * l - 1)) if (1 - abs(2 * l - 1)) else 0.0


def normalize_svg(svg: str) -> str:
    # Mirror the template's normalizeSvg: remap the legacy palette to currentColor / vars
    # so we validate what actually renders, not the pre-normalised author string.
    s = re.sub(r"#1a1a1a", "currentColor", svg, flags=re.I)
    s = re.sub(r"#2f5d50", "var(--accent)", s, flags=re.I)
    s = re.sub(r"#c4622d", "var(--accent2)", s, flags=re.I)
    return s


def extract_svgs(html: str) -> list[str]:
    # Pull the visualSvg string literals out of the injected DATA block.
    data = re.search(r"/\*__DATA_START__\*/(.*?)/\*__DATA_END__\*/", html, re.S)
    scope = data.group(1) if data else html
    return [normalize_svg(s) for s in re.findall(r"<svg\b.*?</svg>", scope, re.S)]


def themed(svg: str, theme: dict) -> str:
    # Substitute the same way the browser resolves currentColor and the CSS vars.
    s = svg
    s = s.replace("currentColor", theme["ink"])
    s = s.replace("var(--accent2)", theme["accent2"]).replace("var(--accent)", theme["accent"])
    # Any text without an explicit fill inherits the theme ink (the .visual svg text rule).
    s = re.sub(r"<text(?![^>]*\bfill=)", f"<text fill='{theme['ink']}' ", s)
    return s


def with_background(svg: str, bg: str) -> str:
    # Prepend a full-bleed background rect so a saved preview shows on the theme background,
    # the same way the .visual svg{background:var(--panel)} rule frames it in the browser.
    return re.sub(r"(<svg\b[^>]*>)", r"\1" + f"<rect width='100%' height='100%' fill='{bg}'/>",
                  svg, count=1)


def write_preview(svg_themed: str, theme: dict, outdir: pathlib.Path, stem: str) -> tuple[str, str]:
    # Best-effort preview, never part of the gate. PNG if cairosvg is importable, else a
    # standalone SVG that opens anywhere with no dependency. Returns (path, note).
    framed = with_background(svg_themed, theme["bg"])
    try:
        import cairosvg  # optional; present in some Claude Code envs, absent in Cowork
        png = outdir / f"{stem}.png"
        cairosvg.svg2png(bytestring=svg_themed.encode(), write_to=str(png),
                         output_width=1280, background_color=theme["bg"])
        return str(png), ""
    except ImportError:
        out = outdir / f"{stem}.svg"
        out.write_text(framed, encoding="utf-8")
        return str(out), " (SVG preview; install cairosvg for PNG)"
    except Exception as e:  # noqa: BLE001  - a render hiccup must not fail the gate
        out = outdir / f"{stem}.svg"
        out.write_text(framed, encoding="utf-8")
        return str(out), f" (SVG preview; PNG render skipped: {e})"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--out", default="/tmp/diag")
    args = ap.parse_args(argv)

    path = pathlib.Path(args.html)
    if not path.exists():
        print(f"Not found: {path}", file=sys.stderr)
        return 2
    svgs = extract_svgs(path.read_text())
    if not svgs:
        print("No Visual diagrams found to check.", file=sys.stderr)
        return 2

    outdir = pathlib.Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    failed = 0
    for i, svg in enumerate(svgs):
        # Find any FIXED colours the author hardcoded (not currentColor, not a CSS var).
        # These do not flip with the theme, so they are the real dark-on-dark risk.
        fixed = re.findall(r"(?:stroke|fill)=['\"](#[0-9a-fA-F]{3,6})['\"]", svg)
        for theme_name, theme in (("light", LIGHT), ("dark", DARK)):
            s = themed(svg, theme)
            # The diagram's main ink is currentColor -> theme ink. It must contrast with bg.
            bg_lum = luminance(theme["bg"])
            contrast = abs(luminance(theme["ink"]) - bg_lum)
            # A hardcoded colour is a dark-on-dark (or light-on-light) risk only when it is
            # both low-contrast against the background AND near-greyscale. Saturated semantic
            # colours (red/amber/green marks) read on either theme, so they are exempt.
            low_fixed = [c for c in fixed
                         if abs(luminance(c) - bg_lum) < CONTRAST_MIN and saturation(c) < SATURATION_MAX]
            preview, note = write_preview(s, theme, outdir, f"diagram-{i}-{theme_name}")
            if contrast < CONTRAST_MIN:
                print(f"[FAIL] diagram {i} ({theme_name}): theme ink barely contrasts with "
                      f"background (gap {contrast:.2f}).", file=sys.stderr)
                failed += 1
            elif low_fixed:
                print(f"[FAIL] diagram {i} ({theme_name}): hardcoded colour(s) "
                      f"{sorted(set(low_fixed))} barely contrast with the {theme_name} background. "
                      f"Use currentColor / var(--accent) so they flip with the theme.",
                      file=sys.stderr)
                failed += 1
            else:
                print(f"[ok]   diagram {i} ({theme_name}): legible (contrast {contrast:.2f}) -> {preview}{note}")

    if failed:
        print(f"\n{failed} diagram/theme combination(s) failed. Open the previews in {outdir} and "
              f"check the diagram is legible, then fix the visualSvg theming.", file=sys.stderr)
        return 1
    print(f"\nAll {len(svgs)} diagram(s) legible in light and dark. Previews in {outdir}. "
          f"This is a safety net: still open the file on a real device before raising the score.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
