#!/usr/bin/env python3
"""Detect Git conflict markers in wiki markdown files.

Scans files under wiki/ (or a given path) for the standard Git conflict
markers (`<<<<<<<`, `=======`, `>>>>>>`) and reports which files contain
unresolved conflicts, along with the line ranges and counts.

Usage:
  uv run python .agents/skills/wiki-conflict-resolver/scripts/detect_conflicts.py
  uv run python .agents/skills/wiki-conflict-resolver/scripts/detect_conflicts.py --path wiki
  uv run python .agents/skills/wiki-conflict-resolver/scripts/detect_conflicts.py --path wiki/index.md
  uv run python .agents/skills/wiki-conflict-resolver/scripts/detect_conflicts.py --check-only  # exit 1 if any conflicts
"""
import argparse
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

MARKER_START = '<<<<<<<'
MARKER_MID = '======='
MARKER_END = '>>>>>>>'
ALL_MARKERS = (MARKER_START, MARKER_MID, MARKER_END)


def find_conflicts_in_file(path):
    """Return list of (start_line, mid_line, end_line) tuples (1-indexed)."""
    blocks = []
    in_block = False
    start = mid = None
    with open(path, encoding='utf-8') as f:
        for i, line in enumerate(f, start=1):
            s = line.rstrip('\n')
            if s.startswith(MARKER_START):
                if in_block:
                    # Nested/unexpected start — report as anomaly
                    blocks.append((start, mid, i, 'nested-start'))
                in_block = True
                start = i
                mid = None
            elif s == MARKER_MID and in_block and mid is None:
                mid = i
            elif s.startswith(MARKER_END) and in_block:
                blocks.append((start, mid, i, 'ok'))
                in_block = False
                start = mid = None
    if in_block:
        blocks.append((start, mid, None, 'unterminated'))
    return blocks


def iter_md_files(root):
    """Yield all .md files under root (excluding .git, raw/, .agents/)."""
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip irrelevant directories
        dirnames[:] = [d for d in dirnames if d not in ('.git', 'raw', '.agents',
                                                         'node_modules', 'site')]
        for fn in filenames:
            if fn.endswith('.md'):
                yield os.path.join(dirpath, fn)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--path', default='wiki',
                   help='File or directory to scan (default: wiki)')
    p.add_argument('--check-only', action='store_true',
                   help='Exit 1 if any conflicts found (for scripting)')
    args = p.parse_args()

    if os.path.isfile(args.path):
        files = [args.path]
    else:
        files = sorted(iter_md_files(args.path))

    total_conflicts = 0
    affected_files = 0
    for path in files:
        blocks = find_conflicts_in_file(path.path if hasattr(path, 'path') else path) \
            if False else find_conflicts_in_file(path)
        if not blocks:
            continue
        affected_files += 1
        n = len(blocks)
        total_conflicts += n
        print(f"{path}: {n} conflict block(s)")
        for (s, m, e, status) in blocks:
            if status == 'ok':
                print(f"  lines {s}-{e} (separator at {m})")
            else:
                print(f"  lines {s}-{e if e else '?'} [{status}]")

    print()
    if total_conflicts == 0:
        print("OK: no conflict markers found.")
        sys.exit(0)
    print(f"Total: {total_conflicts} conflict block(s) across {affected_files} file(s).")
    if args.check_only:
        sys.exit(1)


if __name__ == '__main__':
    main()
