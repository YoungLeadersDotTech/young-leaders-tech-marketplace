#!/usr/bin/env python3
"""Embed local images as base64 data: URIs for the renderer's section `images` field.

The offline HTML must be one self-contained file, so a screenshot on disk has to become an
inline `data:image/...;base64,...` URI before it goes into the DATA object. This helper does
that conversion. For content that already lives online, skip this and put the http(s) URL
straight into `src` (the renderer accepts http(s) as-is; only local files need embedding).

Usage:
  # Print a ready-to-paste JSON array for the section `images` field:
  python3 img_to_datauri.py --json shot1.png shot2.png

  # Print one data: URI per file (no JSON wrapper):
  python3 img_to_datauri.py shot1.png

  # Attach captions positionally (one --caption per image, in order):
  python3 img_to_datauri.py --json --caption "Single-select" --caption "Multi-select" a.png b.png

Notes:
  - Only image types are emitted (png, jpg/jpeg, gif, webp, svg). Anything else is refused.
  - base64 inflates size by ~34%. Keep the total embedded weight sane (a handful of
    screenshots is fine; do not embed a whole gallery of multi-MB images into one file).
  - No third-party dependencies, so it runs identically in Cowork and Claude Code.
"""
import sys, os, base64, json, mimetypes

MIME = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml",
}


def to_datauri(path):
    ext = os.path.splitext(path)[1].lower()
    mime = MIME.get(ext) or mimetypes.guess_type(path)[0]
    if not mime or not mime.startswith("image/"):
        raise SystemExit(f"refusing non-image file: {path} (type {mime!r})")
    with open(path, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def main(argv):
    as_json = False
    captions = []
    paths = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--json":
            as_json = True
        elif a == "--caption":
            i += 1
            captions.append(argv[i] if i < len(argv) else "")
        elif a in ("-h", "--help"):
            print(__doc__)
            return 0
        else:
            paths.append(a)
        i += 1
    if not paths:
        print(__doc__)
        return 2

    total = 0
    items = []
    for idx, p in enumerate(paths):
        uri = to_datauri(p)
        total += len(uri)
        items.append({
            "src": uri,
            "alt": os.path.splitext(os.path.basename(p))[0].replace("-", " "),
            "caption": captions[idx] if idx < len(captions) else "",
        })

    if as_json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
    else:
        for it in items:
            print(it["src"])
    sys.stderr.write(f"[img_to_datauri] {len(items)} image(s), ~{total // 1024} KB of base64 emitted\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
