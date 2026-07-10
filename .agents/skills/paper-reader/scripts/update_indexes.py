#!/usr/bin/env python3
"""Step 10: Add rows to index files and update statistics.

Subcommands:
  add     Insert a row into wiki/index.md (correct section) and wiki/{category}/index.md.
  stats   Recount all categories and rewrite the ## Statistics section in wiki/index.md.

Usage:
  python .agents/skills/paper-reader/scripts/update_indexes.py add \
      --category entities --slug author-name --display "Author Name" \
      --summary "..." --date 2026-07-10
  python .agents/skills/paper-reader/scripts/update_indexes.py add \
      --category sources --slug paper-slug --display "Title" --summary "..." --date 2026-07-10
  python .agents/skills/paper-reader/scripts/update_indexes.py stats

Categories: entities, concepts, sources, synthesis, queries.
Skips insertion if the slug already exists in the target index.
"""
import argparse, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')

CATEGORIES = ('entities', 'concepts', 'sources', 'synthesis', 'queries')
DATE_HEADER = {'entities': 'Created', 'concepts': 'Created', 'sources': 'Date',
               'synthesis': 'Date', 'queries': 'Date'}


def find_section_range(lines, category):
    """Find the line range of a ## {Category} section in wiki/index.md.

    Returns (start, end) where end is the line *after* the last table row
    (i.e., the blank line or --- before the next section).
    """
    section_cap = category.capitalize()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == f'## {section_cap}':
            start = i
            break
    if start is None:
        return None, None

    # Find the end: next '---' separator or '## ' heading after the table rows
    end = None
    for i in range(start + 1, len(lines)):
        s = lines[i].strip()
        if s == '---':
            end = i
            break
        if s.startswith('## ') and i > start + 1:
            end = i
            break
    if end is None:
        end = len(lines)
    # Walk back past trailing blank lines
    while end > start + 1 and lines[end - 1].strip() == '':
        end -= 1
    return start, end


def slug_exists_in_section(lines, category, slug):
    """Check if a wikilink row for this slug already exists in the section."""
    pattern = re.compile(r'\|\s*\[\[' + category + r'/' + re.escape(slug) + r'[\|\\]')
    for line in lines:
        if pattern.search(line):
            return True
    return False


def cmd_add(args):
    if args.category not in CATEGORIES:
        print(f"ERROR: category must be one of {CATEGORIES}", file=sys.stderr)
        sys.exit(1)

    row = f"| [[{args.category}/{args.slug}\\|{args.display}]] | {args.summary} | {args.date} |"

    # --- Update main index (wiki/index.md) ---
    main_path = 'wiki/index.md'
    with open(main_path, encoding='utf-8') as f:
        lines = f.readlines()

    if slug_exists_in_section(lines, args.category, args.slug):
        print(f"SKIP (main index): {args.category}/{args.slug} already exists")
    else:
        start, end = find_section_range(lines, args.category)
        if start is None:
            print(f"ERROR: Cannot find '## {args.category.capitalize()}' section in {main_path}",
                  file=sys.stderr)
            sys.exit(1)
        # Insert before the trailing separator/blank
        lines.insert(end, row + '\n')
        with open(main_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Added to main index: {args.category}/{args.slug}")

    # --- Update subdirectory index (wiki/{category}/index.md) ---
    sub_path = f'wiki/{args.category}/index.md'
    if not os.path.exists(sub_path):
        print(f"WARN: {sub_path} does not exist, skipping subdirectory index",
              file=sys.stderr)
        return

    with open(sub_path, encoding='utf-8') as f:
        sub_lines = f.readlines()

    if slug_exists_in_section(sub_lines, args.category, args.slug):
        print(f"SKIP (subdir index): {args.category}/{args.slug} already exists")
    else:
        # Subdirectory index: append before trailing blank lines
        end = len(sub_lines)
        while end > 0 and sub_lines[end - 1].strip() == '':
            end -= 1
        sub_lines.insert(end, row + '\n')
        with open(sub_path, 'w', encoding='utf-8') as f:
            f.writelines(sub_lines)
        print(f"Added to subdirectory index: {sub_path}")


def cmd_stats(args):
    """Recount all categories and rewrite the ## Statistics section."""
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
    total = sum(counts.values())

    import datetime
    today = datetime.date.today().isoformat()

    with open('wiki/index.md', encoding='utf-8') as f:
        content = f.read()

    # Replace the entire ## Statistics section
    stats_block = (
        f"## Statistics\n\n"
        f"- **Total pages**: {total}\n"
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
    # Preserve trailing newline at end of file
    if not new_content.endswith('\n'):
        new_content += '\n'
    with open('wiki/index.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated statistics: total={total}, "
          f"entities={counts['entities']}, concepts={counts['concepts']}, "
          f"sources={counts['sources']}, synthesis={counts['synthesis']}, "
          f"queries={counts['queries']}, last_updated={today}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='command', required=True)

    pa = sub.add_parser('add', help='Add a row to index files')
    pa.add_argument('--category', required=True, choices=CATEGORIES)
    pa.add_argument('--slug', required=True, help='Page slug (no .md)')
    pa.add_argument('--display', required=True, help='Display text for wikilink')
    pa.add_argument('--summary', required=True, help='One-line summary')
    pa.add_argument('--date', required=True, help='Date (YYYY-MM-DD or year)')
    pa.set_defaults(func=cmd_add)

    ps = sub.add_parser('stats', help='Recount and update statistics')
    ps.set_defaults(func=cmd_stats)

    args = p.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
