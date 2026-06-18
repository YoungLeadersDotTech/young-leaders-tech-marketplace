#!/usr/bin/env python3
"""measure_frontmatter_weight.py - check SKILL.md / agent description length.

Flattens block scalars, strips whitespace, counts characters, and flags any
description over the 250-char Claude Code cap. Works on a single file or a dir.

Usage:
  measure_frontmatter_weight.py <file-or-dir> [--cap 250]
Exit codes: 0 all within cap | 1 one or more over cap
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

CAP = 250


def iter_files(target: pathlib.Path):
    if target.is_file():
        yield target
        return
    for path in target.rglob("*.md"):
        rel = str(path)
        if path.name == "SKILL.md" or "/agents/" in rel or "/commands/" in rel:
            yield path


def extract_description(text: str) -> str | None:
    m = re.match(r"---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    fm = m.group(1)
    block = re.search(
        r"description:\s*(?:[|>][+\-]?\s*\n((?:  .*\n?)+)|([^\n]+))", fm, re.DOTALL
    )
    if not block:
        return None
    desc = (block.group(1) or block.group(2) or "").strip()
    # Flatten: collapse newlines + repeated whitespace to single spaces.
    return re.sub(r"\s+", " ", desc).strip()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--cap", type=int, default=CAP)
    args = ap.parse_args(argv)

    target = pathlib.Path(args.target).expanduser()
    if not target.exists():
        print(f"Not found: {target}", file=sys.stderr)
        return 1

    over = 0
    for path in iter_files(target):
        try:
            desc = extract_description(path.read_text().replace("\r\n", "\n"))
        except OSError:
            continue
        if desc is None:
            continue
        n = len(desc)
        flag = "OVER" if n > args.cap else "ok"
        if n > args.cap:
            over += 1
        print(f"[{flag}] {n:4d}/{args.cap}  {path}")
    if over:
        print(f"\n{over} description(s) over the {args.cap}-char cap. "
              f"Gradient-rewrite (never trim) before shipping.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
