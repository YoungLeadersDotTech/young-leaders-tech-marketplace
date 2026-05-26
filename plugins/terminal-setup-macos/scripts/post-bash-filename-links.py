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
    return f'{ESC}]8;;{uri}{ESC}\\{display}{ESC}]8;;{ESC}\\'

def resolve_filename(name: str, cwd: str) -> str | None:
    """Return absolute path for bare filename, or None if not found."""
    # Already absolute
    if os.path.isabs(name):
        return name if os.path.exists(name) else None

    # cwd first, then search roots
    roots = [cwd] + [r for r in SEARCH_ROOTS if r != cwd]
    for root in roots:
        if not root:
            continue
        candidate = os.path.join(root, name)
        if os.path.exists(candidate):
            return os.path.realpath(candidate)
        # Also try a one-level glob within the root
        # (e.g. file is in docs/workflows/ but we only know the basename)

    # Try rglob-style: walk up to 3 levels deep in cwd and work-registry
    for root in [cwd, os.path.expanduser('~/work-registry')]:
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
                    return os.path.realpath(os.path.join(dirpath, name))
        except PermissionError:
            continue

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
