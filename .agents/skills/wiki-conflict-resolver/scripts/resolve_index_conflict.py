#!/usr/bin/env python3
"""Resolve Git rebase conflicts in wiki index files.

Targets:
  - wiki/index.md              (main index with ## Entities/Concepts/Sources/... sections)
  - wiki/entities/index.md     (subdirectory index — table only)
  - wiki/concepts/index.md
  - wiki/sources/index.md
  - wiki/synthesis/index.md
  - wiki/queries/index.md

Conflict resolution strategy:
  1. For each conflict block, extract all markdown table rows
     (lines starting with `| [[category/slug...`) from both sides.
  2. Merge rows: deduplicate by (category, slug), preserving first-seen order
     (ours side first, then theirs-only rows appended).
  3. Replace the conflict block with the merged rows.
  4. Leave non-conflicted regions untouched.

Usage:
  python .agents/skills/wiki-conflict-resolver/scripts/resolve_index_conflict.py
  python .agents/skills/wiki-conflict-resolver/scripts/resolve_index_conflict.py --dry-run
  python .agents/skills/wiki-conflict-resolver/scripts/resolve_index_conflict.py --path wiki/index.md
  python .agents/skills/wiki-conflict-resolver/scripts/resolve_index_conflict.py --all
"""
import argparse
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DEFAULT_TARGETS = [
    'wiki/index.md',
    'wiki/entities/index.md',
    'wiki/concepts/index.md',
    'wiki/sources/index.md',
    'wiki/synthesis/index.md',
    'wiki/queries/index.md',
]

MARKER_START = '<<<<<<<'
MARKER_MID = '======='
MARKER_END = '>>>>>>>'

# Matches a table row like: | [[entities/foo\|Foo]] | summary | 2026-01-01 |
# Captures (category, slug). Handles escaped pipes `\|` in display text.
ROW_RE = re.compile(r'^\|\s*\[\[([a-z]+)/([^|\\\]]+)')


def extract_rows(text):
    """Return list of (category, slug, raw_line) for table rows in text."""
    rows = []
    for line in text.split('\n'):
        m = ROW_RE.match(line)
        if m:
            rows.append((m.group(1), m.group(2), line))
    return rows


def merge_rows(ours_rows, theirs_rows):
    """Merge two row lists, deduping by (category, slug).

    Preserves first-seen order: ours first, then theirs-only rows appended.
    """
    seen = set()
    merged = []
    for cat, slug, line in ours_rows + theirs_rows:
        key = (cat, slug)
        if key in seen:
            continue
        seen.add(key)
        merged.append((cat, slug, line))
    return merged


def resolve_conflict_block(block_text):
    """Given the inner content of a conflict block (without markers),
    this is a no-op placeholder — actual merging happens at the file level.
    """
    return block_text


def resolve_file(path, dry_run=False):
    """Resolve all conflict blocks in a single file.

    For each conflict block:
      - Extract rows from the 'ours' section (between <<<<<<< and =======)
      - Extract rows from the 'theirs' section (between ======= and >>>>>>>)
      - Merge rows (dedupe by slug)
      - Replace the entire conflict block with the merged rows

    Returns True if any conflicts were resolved, False if none found.
    """
    if not os.path.exists(path):
        print(f"SKIP: {path} does not exist")
        return False

    with open(path, encoding='utf-8') as f:
        content = f.read()

    if MARKER_START not in content:
        print(f"OK: no conflicts in {path}")
        return False

    lines = content.split('\n')
    out = []
    i = 0
    resolved_blocks = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith(MARKER_START):
            # Start of conflict block — collect ours/theirs
            ours_lines = []
            theirs_lines = []
            i += 1
            state = 'ours'
            while i < len(lines):
                cur = lines[i]
                if cur == MARKER_MID and state == 'ours':
                    state = 'theirs'
                    i += 1
                    continue
                if cur.startswith(MARKER_END) and state == 'theirs':
                    i += 1
                    break
                if state == 'ours':
                    ours_lines.append(cur)
                else:
                    theirs_lines.append(cur)
                i += 1

            ours_rows = extract_rows('\n'.join(ours_lines))
            theirs_rows = extract_rows('\n'.join(theirs_lines))

            # If no rows on either side, fall back to concatenating both
            # (preserves any non-row content like section headers)
            if not ours_rows and not theirs_rows:
                # Keep ours + theirs (no dedupe possible)
                out.extend(ours_lines)
                out.extend(theirs_lines)
            else:
                merged = merge_rows(ours_rows, theirs_rows)
                for cat, slug, raw_line in merged:
                    out.append(raw_line)
            resolved_blocks += 1
        else:
            out.append(line)
            i += 1

    new_content = '\n'.join(out)
    # Ensure file ends with newline
    if not new_content.endswith('\n'):
        new_content += '\n'

    print(f"{path}: resolved {resolved_blocks} conflict block(s)")

    if dry_run:
        print('--- DRY RUN: merged output (first 50 lines) ---')
        for line in new_content.split('\n')[:50]:
            print(line)
        return True

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--path', help='Resolve a single file (default: --all targets)')
    p.add_argument('--all', action='store_true',
                   help=f'Resolve all default targets: {", ".join(DEFAULT_TARGETS)}')
    p.add_argument('--dry-run', action='store_true',
                   help='Print merged result without writing files')
    args = p.parse_args()

    if args.path:
        targets = [args.path]
    elif args.all or not args.path:
        targets = DEFAULT_TARGETS
    else:
        targets = DEFAULT_TARGETS

    any_resolved = False
    for t in targets:
        if resolve_file(t, dry_run=args.dry_run):
            any_resolved = True

    if any_resolved:
        print()
        print("Done. Run `python .agents/skills/wiki-conflict-resolver/scripts/finalize.py` "
              "to update statistics and verify.")
    else:
        print("No conflicts found in any target file.")


if __name__ == '__main__':
    main()
