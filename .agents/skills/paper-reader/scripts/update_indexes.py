#!/usr/bin/env python3
"""Step 10: Add rows to index files and update statistics.

Subcommands:
  add     Insert a row into wiki/index.md (correct section) and wiki/{category}/index.md.
  batch   Insert multiple rows from a YAML manifest (entities/concepts/sources/synthesis/queries).
  stats   Recount all categories and rewrite the ## Statistics section in wiki/index.md.

Usage:
  uv run python .agents/skills/paper-reader/scripts/update_indexes.py add \
      --category entities --slug author-name --display "Author Name" \
      --summary "..." --date 2026-07-10
  uv run python .agents/skills/paper-reader/scripts/update_indexes.py add \
      --category sources --slug paper-slug --display "Title" --summary "..." --date 2026-07-10
  uv run python .agents/skills/paper-reader/scripts/update_indexes.py batch \
      --manifest .tmp_ingest_manifest.yaml
  uv run python .agents/skills/paper-reader/scripts/update_indexes.py stats

Batch manifest format (YAML):
  entries:
    - category: sources
      slug: mienye-2024-rnn-comprehensive-review
      display: "Mienye 2024: RNN Review"
      summary: "Comprehensive review of RNN architectures..."
      date: 2026-07-18
    - category: entities
      slug: ibomoiye-domor-mienye
      display: "Ibomoiye Domor Mienye"
      summary: "University of Johannesburg — lead author"
      date: 2026-07-18
    - category: concepts
      slug: recurrent-neural-network
      display: "Recurrent Neural Network"
      summary: "Sequential-data neural network..."
      date: 2026-07-18

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


def _insert_entry(category, slug, display, summary, date):
    """Insert a single entry into both wiki/index.md and wiki/{category}/index.md.

    Returns (added_to_main, added_to_subdir) booleans.
    """
    if category not in CATEGORIES:
        raise ValueError(f"category must be one of {CATEGORIES}")
    row = f"| [[{category}/{slug}\\|{display}]] | {summary} | {date} |"

    added_main = False
    added_sub = False

    # --- Update main index (wiki/index.md) ---
    main_path = 'wiki/index.md'
    with open(main_path, encoding='utf-8') as f:
        lines = f.readlines()

    if slug_exists_in_section(lines, category, slug):
        print(f"SKIP (main index): {category}/{slug} already exists")
    else:
        start, end = find_section_range(lines, category)
        if start is None:
            raise RuntimeError(
                f"Cannot find '## {category.capitalize()}' section in {main_path}"
            )
        lines.insert(end, row + '\n')
        with open(main_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        added_main = True

    # --- Update subdirectory index (wiki/{category}/index.md) ---
    sub_path = f'wiki/{category}/index.md'
    if not os.path.exists(sub_path):
        print(f"WARN: {sub_path} does not exist, skipping subdirectory index",
              file=sys.stderr)
        return added_main, False

    with open(sub_path, encoding='utf-8') as f:
        sub_lines = f.readlines()

    if slug_exists_in_section(sub_lines, category, slug):
        print(f"SKIP (subdir index): {category}/{slug} already exists")
    else:
        end = len(sub_lines)
        while end > 0 and sub_lines[end - 1].strip() == '':
            end -= 1
        sub_lines.insert(end, row + '\n')
        with open(sub_path, 'w', encoding='utf-8') as f:
            f.writelines(sub_lines)
        added_sub = True

    if added_main or added_sub:
        print(f"Added: {category}/{slug}")
    return added_main, added_sub


def cmd_add(args):
    try:
        _insert_entry(args.category, args.slug, args.display, args.summary, args.date)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_batch(args):
    """Insert multiple entries from a YAML manifest, then optionally run stats."""
    try:
        import yaml  # PyYAML
    except ImportError:
        print("ERROR: PyYAML is required for the batch subcommand. "
              "Install with `pip install pyyaml` or `uv add pyyaml`.",
              file=sys.stderr)
        sys.exit(2)

    with open(args.manifest, encoding='utf-8') as f:
        manifest = yaml.safe_load(f)

    if not isinstance(manifest, dict) or 'entries' not in manifest:
        print("ERROR: manifest must be a YAML object with an 'entries' list",
              file=sys.stderr)
        sys.exit(1)

    entries = manifest['entries']
    if not isinstance(entries, list):
        print("ERROR: 'entries' must be a list", file=sys.stderr)
        sys.exit(1)

    required_fields = ('category', 'slug', 'display', 'summary', 'date')
    counts = {'added': 0, 'skipped': 0, 'errors': 0}
    for i, entry in enumerate(entries):
        missing = [f for f in required_fields if f not in entry]
        if missing:
            print(f"ERROR: entry {i} missing fields: {missing}", file=sys.stderr)
            counts['errors'] += 1
            continue
        try:
            added_main, added_sub = _insert_entry(
                entry['category'], entry['slug'], entry['display'],
                entry['summary'], entry['date'],
            )
            if added_main or added_sub:
                counts['added'] += 1
            else:
                counts['skipped'] += 1
        except (ValueError, RuntimeError) as e:
            print(f"ERROR (entry {i}, {entry.get('slug', '?')}): {e}",
                  file=sys.stderr)
            counts['errors'] += 1

    print(f"\nBatch summary: {counts['added']} added, "
          f"{counts['skipped']} skipped, {counts['errors']} errors")

    # Optionally run stats if requested
    if args.stats:
        print("\nRunning stats...")
        cmd_stats(args)

    # Non-zero exit if any errors
    if counts['errors'] > 0:
        sys.exit(1)


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

    pb = sub.add_parser('batch',
                        help='Add multiple rows from a YAML manifest')
    pb.add_argument('--manifest', required=True,
                    help='Path to YAML manifest file with an "entries" list')
    pb.add_argument('--stats', action='store_true',
                    help='Run stats subcommand after batch insert')
    pb.set_defaults(func=cmd_batch)

    ps = sub.add_parser('stats', help='Recount and update statistics')
    ps.set_defaults(func=cmd_stats)

    args = p.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
