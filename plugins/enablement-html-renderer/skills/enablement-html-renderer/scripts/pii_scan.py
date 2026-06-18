#!/usr/bin/env python3
"""pii_scan.py - zero-tolerance PII gate for authored artifacts.

Scans a file or directory for emails, phone numbers, SSNs, and API-key-shaped
strings. Whitelists documentation-safe example values (example.com, 555-01xx,
etc.). Mirrors the skills-toolkit pii-detection-patterns reference.

Usage: pii_scan.py <file-or-dir>
Exit codes: 0 clean | 1 CRITICAL PII found
"""
from __future__ import annotations

import pathlib
import re
import sys

SAFE_DOMAINS = ("example.com", "example.org", "example.net", "test.com", "localhost")
SAFE_PHONES = re.compile(r"555-?01\d\d")  # reserved test range 555-0100..0199

PATTERNS = {
    "email": (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "CRITICAL"),
    "ssn": (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "CRITICAL"),
    "phone_us": (re.compile(r"\b\d{3}[-.]\d{3}[-.]\d{4}\b"), "CRITICAL"),
    "api_key": (re.compile(r"\b(sk|pk|ghp|xox[baprs])[-_][A-Za-z0-9]{16,}\b"), "CRITICAL"),
}


def is_safe(kind: str, value: str) -> bool:
    if kind == "email":
        return any(value.lower().endswith("@" + d) or value.lower().endswith("." + d)
                   for d in SAFE_DOMAINS)
    if kind in ("phone_us",):
        return bool(SAFE_PHONES.search(value))
    if kind == "ssn":
        return value in ("123-45-6789", "000-00-0000")  # common doc placeholders
    return False


def scan_text(text: str):
    hits = []
    for kind, (rx, sev) in PATTERNS.items():
        for m in rx.finditer(text):
            val = m.group(0)
            if is_safe(kind, val):
                continue
            hits.append((sev, kind, val))
    return hits


def iter_files(target: pathlib.Path):
    if target.is_file():
        yield target
    else:
        for p in target.rglob("*"):
            if p.is_file() and p.suffix in (".md", ".json", ".yaml", ".yml", ".txt", ".py", ".sh"):
                yield p


def main(argv: list[str]) -> int:
    if not argv:
        print("Usage: pii_scan.py <file-or-dir>", file=sys.stderr)
        return 1
    target = pathlib.Path(argv[0]).expanduser()
    if not target.exists():
        print(f"Not found: {target}", file=sys.stderr)
        return 1

    found = 0
    for path in iter_files(target):
        try:
            for sev, kind, val in scan_text(path.read_text(errors="ignore")):
                found += 1
                print(f"[{sev}] {kind}: {val}  ->  {path}")
        except OSError:
            continue
    if found:
        print(f"\n{found} PII hit(s). Replace with placeholders like [EMAIL], "
              f"[PHONE], [NAME] before shipping. Zero tolerance.", file=sys.stderr)
        return 1
    print("PII scan clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
