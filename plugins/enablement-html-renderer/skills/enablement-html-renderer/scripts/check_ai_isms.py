#!/usr/bin/env python3
"""
check_ai_isms.py - flag AI-isms and corporate filler in rendered enablement content.

Sourced from a content-cleanup workflow (Phase 4 "AI-ism Removal") and the corpus
"Avoid" patterns (marketing fluff, false expertise, hedging, corporate speak).
This keeps enablement-html-renderer output in the same voice as the published blog
it is often built from, rather than drifting into generic AI phrasing.

Usage:
    python3 check_ai_isms.py <file.html|file.md|file.json>
Exit codes:
    0 = clean
    1 = AI-isms found (printed with the offending phrase + a suggested fix)
"""
import re, sys, pathlib

# Each entry: (regex, why it is an AI-ism, a plain-voice fix).
PATTERNS = [
    (r"in today'?s rapidly evolving", "scene-setting filler", "name the actual thing that changed"),
    (r"it'?s worth noting that", "throat-clearing hedge", "just state the point"),
    (r"let'?s dive in", "filler transition", "start with the point"),
    (r"at the end of the day", "empty summariser", "say what you actually mean"),
    (r"\bdelve\b", "AI-tell vocabulary", "use 'look at' or 'dig into'"),
    (r"\brevolutionary\b", "marketing fluff", "describe what it does"),
    (r"\bgame-?changing\b", "marketing fluff", "describe the concrete change"),
    (r"unlock(ing)? the (power|potential)", "marketing fluff", "say what becomes possible"),
    (r"\bever-?evolving\b", "scene-setting filler", "cut it"),
    (r"\bseamless(ly)?\b", "corporate speak", "say what works, and how"),
    (r"\bsynergy\b", "corporate speak", "name the actual benefit"),
    (r"in the (world|realm) of", "scene-setting filler", "cut it, start with the noun"),
    (r"navigating the (complex|landscape|world)", "corporate metaphor", "say the concrete task"),
    (r"it is important to (note|remember|understand) that", "throat-clearing hedge", "just say it"),
    (r"\bfurthermore\b", "stiff connector", "use 'and' or start a new sentence"),
    (r"\bmoreover\b", "stiff connector", "use 'also' or cut"),
    (r"that being said", "filler pivot", "use 'but' or 'still'"),
    (r"a testament to", "inflated phrasing", "say what it shows"),
    (r"\bplethora\b", "AI-tell vocabulary", "use 'lots' or a number"),
    (r"\bmyriad\b", "AI-tell vocabulary", "use 'many' or a number"),
    (r"when it comes to", "filler lead-in", "cut it, start with the noun"),
    (r"the fact that", "wordiness", "rephrase to drop it"),
    (r"in order to", "wordiness", "use 'to'"),
]

def scan(text):
    hits = []
    for pat, why, fix in PATTERNS:
        for m in re.finditer(pat, text, re.I):
            hits.append((m.group(0), why, fix))
    return hits

def main():
    if len(sys.argv) < 2:
        print("usage: check_ai_isms.py <file>"); sys.exit(2)
    text = pathlib.Path(sys.argv[1]).read_text(errors="ignore")
    hits = scan(text)
    if not hits:
        print("AI-ism scan clean."); sys.exit(0)
    print(f"{len(hits)} AI-ism(s) found:")
    for phrase, why, fix in hits:
        print(f"  - {phrase!r}: {why} -> {fix}")
    sys.exit(1)

if __name__ == "__main__":
    main()
