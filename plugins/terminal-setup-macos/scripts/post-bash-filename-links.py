#!/usr/bin/env python3
"""
post-bash-filename-links.py - PostToolUse hook for Bash

Scans Bash stdout for bare filenames (no directory component, known extensions)
and rewrites them as OSC 8 hyperlinks with the short name as display text.

This makes filenames like `btt-ai-ways-of-working-faq.md` clickable in Ghostty
without requiring Claude to print the full absolute path.

Resolution strategy: for each bare filename, check:
  1. Absolute if it already is one (passthrough)
  2. cwd-relative
  3. Known project roots (work-registry, Projects)
  4. Home-relative
"""

import hashlib
import json
import os
import re
import sys
from pathlib import Path

# File extensions to linkify (must have at least one dir separator to be
# an absolute path already; bare names get resolved)
LINKABLE_EXTENSIONS = {
    '.md', '.yaml', '.yml', '.json', '.py', '.ts', '.tsx', '.js', '.jsx',
    '.sh', '.bash', '.zsh', '.toml', '.cfg', '.conf', '.txt', '.csv',
    '.html', '.css', '.scss', '.sql', '.graphql', '.proto',
}

# Directories to search when resolving a bare filename (in priority order)
SEARCH_ROOTS = [
    os.environ.get('CWD', os.getcwd()),
    os.path.expanduser('~/work-registry'),
    os.path.expanduser('~/Projects'),
    os.path.expanduser('~/.claude'),
]

# OSC 8 hyperlink: ESC ] 8 ; ; URI ESC \\ display_text ESC ] 8 ; ; ESC \\
ESC = '\x1b'

def osc8_link(abs_path: str, display: str) -> str:
    uri = 'file://' + abs_path
    # id= groups this link's display text as one logical hyperlink even if the
    # terminal wraps it across a line break (ghostty-terminal-improvements--2026-08-28,
    # T-01/T-07). Derived from the URI so repeated mentions of the same file share an id.
    link_id = hashlib.sha1(uri.encode()).hexdigest()[:12]
    return f'{ESC}]8;id={link_id};{uri}{ESC}\\{display}{ESC}]8;;{ESC}\\'

def resolve_filename(name: str, cwd: str) -> str | None:
    """Return absolute path for bare filename, or None if not found or ambiguous.

    A generic basename like `index.md` or `state.json` commonly exists under many
    unrelated directories in the same repo (e.g. one per builder-plans/* folder).
    Returning the first match found by `os.walk` silently links to an arbitrary
    one of them - wrong more often than not for a repo with several such folders,
    and worse than no link at all since a wrong link looks confidently correct.
    So this collects every candidate across all search locations and only
    resolves when exactly one distinct file matches; two or more real matches is
    treated as ambiguous and returns None rather than guessing (T-16 follow-up,
    ghostty-terminal-improvements--2026-08-28 - caught live: `index.md` for one
    plan folder resolved to an unrelated plan folder's `index.md`).
    """
    # Already absolute
    if os.path.isabs(name):
        return name if os.path.exists(name) else None

    candidates: set[str] = set()

    # Direct join under each search root (cwd first, then the fixed roots)
    roots = [cwd] + [r for r in SEARCH_ROOTS if r != cwd]
    for root in roots:
        if not root:
            continue
        candidate = os.path.join(root, name)
        if os.path.exists(candidate):
            candidates.add(os.path.realpath(candidate))

    # Recursive search in cwd and work-registry, depth-limited to 5 levels.
    # Stops walking as soon as ambiguity is confirmed (2+ distinct matches) -
    # the answer is already "None" at that point, no need to keep scanning.
    for root in [cwd, os.path.expanduser('~/work-registry')]:
        if len(candidates) > 1:
            break
        if not root:
            continue
        try:
            for dirpath, dirnames, filenames in os.walk(root):
                # Don't descend into hidden dirs or node_modules
                dirnames[:] = [d for d in dirnames
                               if not d.startswith('.') and d != 'node_modules'
                               and d != '__pycache__']
                # Limit depth to 5 levels
                depth = dirpath.replace(root, '').count(os.sep)
                if depth > 5:
                    dirnames.clear()
                    continue
                if name in filenames:
                    candidates.add(os.path.realpath(os.path.join(dirpath, name)))
                    if len(candidates) > 1:
                        break
        except PermissionError:
            continue

    if len(candidates) == 1:
        return candidates.pop()
    return None

def linkify_stdout(text: str, cwd: str) -> str:
    """Replace bare filenames with OSC 8 links in text."""
    if not text:
        return text

    # Pattern: a word boundary, then a filename (no slashes), with known extension
    # We capture the full token including any surrounding punctuation carefully
    # Match: optional quote/backtick, then the filename, then optional quote/backtick
    pattern = re.compile(
        r'(?<![/\w])([A-Za-z0-9_\-\.]+(' + '|'.join(re.escape(e) for e in LINKABLE_EXTENSIONS) + r'))(?![/\w])',
        re.IGNORECASE
    )

    # Track already-resolved names to avoid redundant filesystem walks
    cache: dict[str, str | None] = {}

    def replace_match(m: re.Match) -> str:
        name = m.group(1)
        # Skip if it looks like it already has a path component
        if '/' in name:
            return name
        # Skip very short names (avoid false positives on things like "a.py")
        if len(name) < 5:
            return name
        if name not in cache:
            cache[name] = resolve_filename(name, cwd)
        abs_path = cache[name]
        if abs_path:
            return osc8_link(abs_path, name)
        return name

    return pattern.sub(replace_match, text)

def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Only act on Bash PostToolUse
    if payload.get('tool_name') != 'Bash':
        sys.exit(0)
    if payload.get('hook_event_name') != 'PostToolUse':
        sys.exit(0)

    tool_response = payload.get('tool_response', {})
    stdout = tool_response.get('stdout', '')
    stderr = tool_response.get('stderr', '')

    if not stdout:
        sys.exit(0)

    cwd = payload.get('cwd') or os.getcwd()

    new_stdout = linkify_stdout(stdout, cwd)

    # Only emit output if we actually changed something (avoid overhead)
    if new_stdout == stdout:
        sys.exit(0)

    out = {
        'hookSpecificOutput': {
            'hookEventName': 'PostToolUse',
            'updatedToolOutput': {
                'stdout': new_stdout,
                'stderr': stderr,
                'interrupted': tool_response.get('interrupted', False),
                'isImage': tool_response.get('isImage', False),
            }
        }
    }
    print(json.dumps(out))

if __name__ == '__main__':
    main()
