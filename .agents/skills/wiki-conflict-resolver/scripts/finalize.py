#!/usr/bin/env python3
"""Post-conflict finalization: update statistics and verify no markers remain.

Steps:
  1. Scan all wiki/ markdown files for residual conflict markers.
  2. Recount pages in each category and rewrite the `## Statistics` section
     in wiki/index.md.
  3. Print a summary of what was updated.

Usage:
  python .agents/skills/wiki-conflict-resolver/scripts/finalize.py
  python .agents/skills/wiki-conflict-resolver/scripts/finalize.py --dry-run
"""
import argparse
import datetime
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

CATEGORIES = ('entities', 'concepts', 'sources', 'synthesis', 'queries')
MARKER_START = '<<<<<<<'
MARKER_MID = '======='
MARKER_END = '>>>>>>>'


def scan_residual_markers(root='wiki'):
    """Return list of (file, line_num, marker_type) for any residual markers."""
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ('.git', 'node_modules', 'site')]
        for fn in filenames:
            if not fn.endswith('.md'):
                continue
            path = os.path.join(dirpath, fn)
            with open(path, encoding='utf-8') as f:
                for i, line in enumerate(f, start=1):
                    s = line.rstrip()
                    if s.startswith(MARKER_START):
                        found.append((path, i, 'start'))
                    elif s == MARKER_MID:
                        found.append((path, i, 'mid'))
                    elif s.startswith(MARKER_END):
                        found.append((path, i, 'end'))
    return found


def recount_statistics():
    """Recount pages per category and return dict of counts."""
    counts = {}
    for cat in CATEGORIES:
        d = f'wiki/{cat}'
        if os.path.isdir(d):
            counts[cat] = len([
                f for f in os.listdir(d)
                if f.endswith('.md') and f != 'index.md'
            ])
        else:
            counts[cat] = 0
    counts['total'] = sum(counts.values())
    return counts


def update_statistics_section(counts, today):
    """Rewrite the ## Statistics section in wiki/index.md."""
    with open('wiki/index.md', encoding='utf-8') as f:
        content = f.read()

    stats_block = (
        f"## Statistics\n\n"
        f"- **Total pages**: {counts['total']}\n"
        f"- **Entities**: {counts['entities']}\n"
        f"- **Concepts**: {counts['concepts']}\n"
        f"- **Sources**: {counts['sources']}\n"
        f"- **Synthesis**: {counts['synthesis']}\n"
        f"- **Queries**: {counts['queries']}\n"
        f"- **Last updated**: {today}\n"
    )

    new_content = re.sub(
        r'## Statistics\n.*?(?=\n---|\Z)',
        stats_block.rstrip(),
        content,
        count=1,
        flags=re.DOTALL,
    )
    if not new_content.endswith('\n'):
        new_content += '\n'
    return new_content


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--dry-run', action='store_true',
                   help='Print changes without writing files')
    args = p.parse_args()

    # Step 1: scan for residual markers
    residuals = scan_residual_markers()
    if residuals:
        print(f"WARNING: {len(residuals)} residual conflict marker(s) found:")
        for path, line, kind in residuals[:20]:
            print(f"  {path}:{line} [{kind}]")
        if len(residuals) > 20:
            print(f"  ... and {len(residuals) - 20} more")
        print()
        print("Fix these before finalizing. Aborting.")
        sys.exit(1)
    print("OK: no residual conflict markers in wiki/.")

    # Step 2: recount statistics
    counts = recount_statistics()
    today = datetime.date.today().isoformat()
    print(f"Counts: total={counts['total']}, "
          f"entities={counts['entities']}, concepts={counts['concepts']}, "
          f"sources={counts['sources']}, synthesis={counts['synthesis']}, "
          f"queries={counts['queries']}")

    if args.dry_run:
        print('--- DRY RUN: new ## Statistics section ---')
        print(update_statistics_section(counts, today))
        return

    new_content = update_statistics_section(counts, today)
    with open('wiki/index.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated ## Statistics in wiki/index.md (last_updated={today})")
    print()
    print("Finalization complete. Next steps:")
    print("  - Review changes with `git diff`")
    print("  - Run `git add` on resolved files")
    print("  - Run `git rebase --continue` (set GIT_EDITOR=true to skip editor)")
    print("  - Run `uv run mkdocs build --strict` for build verification")


if __name__ == '__main__':
    main()
