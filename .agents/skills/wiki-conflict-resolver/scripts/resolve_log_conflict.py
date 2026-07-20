#!/usr/bin/env python3
"""Resolve Git rebase conflicts in wiki/log.md.

Log convention (per AGENTS.md):
  - Append-only, newest entries at the END of the file.
  - Format: `## [YYYY-MM-DD] op | Title` after a `---` separator.
  - Operations: ingest, query, lint, merge.

Conflict resolution strategy:
  1. Strip conflict markers and concatenate both sides' content.
  2. Parse the file into individual log entries (split on `---` separators).
  3. Deduplicate by (date, op, title) — keep the entry with the longer body
     (more informative) on ties.
  4. Sort entries chronologically (oldest first — newest at end).
  5. Re-emit the file with the standard header.

Usage:
  uv run python .agents/skills/wiki-conflict-resolver/scripts/resolve_log_conflict.py
  uv run python .agents/skills/wiki-conflict-resolver/scripts/resolve_log_conflict.py --dry-run
  uv run python .agents/skills/wiki-conflict-resolver/scripts/resolve_log_conflict.py --path wiki/log.md
"""
import argparse
import os
import re
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

LOG_PATH = 'wiki/log.md'
MARKER_START = '<<<<<<<'
MARKER_MID = '======='
MARKER_END = '>>>>>>>'

ENTRY_HEADER_RE = re.compile(
    r'^##\s*\[(\d{4}-\d{2}-\d{2})\]\s*(\w+)\s*\|\s*(.+?)\s*$',
    re.MULTILINE,
)


def strip_conflict_markers(text):
    """Remove conflict markers, keeping both sides' content concatenated."""
    out = []
    lines = text.split('\n')
    state = 'common'  # 'common' | 'ours' | 'theirs'
    for line in lines:
        s = line.rstrip()
        if s.startswith(MARKER_START):
            state = 'ours'
            continue
        if s == MARKER_MID and state == 'ours':
            state = 'theirs'
            continue
        if s.startswith(MARKER_END) and state == 'theirs':
            state = 'common'
            continue
        # Keep lines from both sides and common regions
        out.append(line)
    return '\n'.join(out)


def parse_entries(text):
    """Parse log content into list of entries using header regex.

    An entry is anything starting with `## [YYYY-MM-DD] op | Title` up to
    the next header (or end of text). `---` separators between entries are
    stripped from bodies. This handles conflicts where multiple headers were
    concatenated without intervening `---` separators.
    """
    matches = list(ENTRY_HEADER_RE.finditer(text))
    entries = []
    for i, m in enumerate(matches):
        date_str, op, title = m.group(1), m.group(2), m.group(3)
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[body_start:body_end]
        # Strip leading/trailing `---` separator lines and whitespace
        body = re.sub(r'(?m)^\s*---\s*$', '', body).strip('\n')
        entries.append({
            'date': date_str,
            'op': op,
            'title': title.strip(),
            'body': body,
        })
    return entries


def dedupe_entries(entries):
    """Deduplicate by (date, op, title); keep entry with longer body."""
    seen = {}
    for e in entries:
        key = (e['date'], e['op'], e['title'].lower())
        if key not in seen:
            seen[key] = e
        else:
            # Prefer the one with the longer body
            if len(e['body']) > len(seen[key]['body']):
                seen[key] = e
    return list(seen.values())


def sort_entries(entries):
    """Sort entries chronologically (oldest first — newest at end)."""
    def key(e):
        # Parse date for sorting; fall back to 9999-01-01 if unparseable
        try:
            return datetime.strptime(e['date'], '%Y-%m-%d')
        except ValueError:
            return datetime(9999, 1, 1)
    return sorted(entries, key=key)


def render_file(entries):
    """Render the canonical log.md with header and entries."""
    out = ['# Wiki Log\n']
    out.append('> **Purpose**: Chronological, append-only record of what happened and when.')
    out.append('> **Format**: `## [YYYY-MM-DD] operation | Description`')
    out.append('> **Operations**: `ingest`, `query`, `lint`\n')
    out.append('---\n')
    for e in entries:
        out.append(f"## [{e['date']}] {e['op']} | {e['title']}\n")
        if e['body']:
            out.append(e['body'].rstrip() + '\n')
        out.append('---\n')
    # Remove trailing newline from last `---` for cleaner file end
    text = '\n'.join(out)
    if text.endswith('---\n'):
        text = text[:-1]
    return text


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--path', default=LOG_PATH, help=f'Log file path (default: {LOG_PATH})')
    p.add_argument('--dry-run', action='store_true',
                   help='Print merged result without writing the file')
    args = p.parse_args()

    if not os.path.exists(args.path):
        print(f"ERROR: {args.path} not found", file=sys.stderr)
        sys.exit(1)

    with open(args.path, encoding='utf-8') as f:
        original = f.read()

    # Check if there are any conflict markers
    has_conflicts = (MARKER_START in original and
                     MARKER_MID in original and
                     MARKER_END in original)
    if not has_conflicts:
        print(f"OK: no conflict markers in {args.path}")
        # Still allow re-sort/dedupe if --force is given? For now, exit.
        sys.exit(0)

    # Strip markers and parse
    merged_text = strip_conflict_markers(original)
    entries = parse_entries(merged_text)
    before = len(entries)
    entries = dedupe_entries(entries)
    after_dedupe = len(entries)
    entries = sort_entries(entries)

    print(f"Parsed {before} entries; {before - after_dedupe} duplicate(s) removed; "
          f"{len(entries)} unique entries after merge.")

    rendered = render_file(entries)

    if args.dry_run:
        print('--- DRY RUN: merged output ---')
        print(rendered)
        return

    with open(args.path, 'w', encoding='utf-8') as f:
        f.write(rendered)
    print(f"Resolved conflicts in {args.path}")


if __name__ == '__main__':
    main()
