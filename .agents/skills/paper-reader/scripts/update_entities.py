#!/usr/bin/env python3
"""Step 6 helper: append-only updates to existing author entity pages.

For each listed entity, derives the paper's title/venue/year/authors from
the source page (wiki/sources/{slug}.md) and applies the append-only update
pattern from page-templates.md automatically:

  1. frontmatter `updated:` -> today
  2. new bullet under `## Key Contributions` (or `## Notable Contributions`):
     - Co-author of "Short Title" (Venue, Year) [-- note] — [[sources/{slug}|Authors Year]]
  3. new bullet under `## Related Sources`:
     - [[sources/{slug}|Authors Year: Full Title]]

This removes the most error-prone manual-edit batch of the ingest (4-6
entity pages x 2-3 edits each) while preserving the agent's role: run the
script for the guaranteed-consistent skeleton, then polish the Key
Contributions bullet wording (e.g., a paper-specific description via
--note, or "First author of" via --role) if desired.

New authors (no page yet) are NOT handled — those are created by hand per
the Step 6 template. This script only updates existing pages.

Usage:
  uv run python .agents/skills/paper-reader/scripts/update_entities.py \
      --slug paper-slug --entities author1 author2 \
      [--note "paper-specific contribution description"] \
      [--role "Co-author of"]

Idempotent: any entity page already referencing sources/{slug} is skipped.

Exit code 0 = all pages updated or skipped cleanly, 1 = any error.
"""
import argparse, datetime, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')

CONTRIB_HEADINGS = ('## Key Contributions', '## Notable Contributions')


def read_source_page(slug):
    """Extract (display, title, venue, year) from wiki/sources/{slug}.md."""
    path = os.path.join('wiki', 'sources', f'{slug}.md')
    if not os.path.isfile(path):
        print(f"ERROR: source page not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding='utf-8') as f:
        text = f.read()

    h1 = next((l for l in text.splitlines() if l.startswith('# ')), None)
    if h1 is None or ':' not in h1:
        print(f"ERROR: H1 in {path} missing or lacks ':' "
              f"(expected 'Authors Year: Title')", file=sys.stderr)
        sys.exit(1)
    display, title = (p.strip() for p in h1[2:].split(':', 1))

    vm = re.search(r'^\*\*Venue\*\*:\s*(.+)$', text, re.MULTILINE)
    venue = vm.group(1).strip() if vm else ''
    # Strip a trailing ", Sep. 2011"-style date (year is appended separately)
    venue = re.sub(r',\s*[A-Z][a-z]{2,8}\.?\s*\d{4}$', '', venue).rstrip(',')

    ym = re.search(r'(\d{4})', display)
    year = ym.group(1) if ym else ''

    return display, title, venue, year


def update_frontmatter_date(lines, today):
    """Set frontmatter `updated:` to today.

    Returns (lines, status) where status is 'updated', 'unchanged'
    (already today), or 'missing'.
    """
    in_fm = False
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if in_fm:
                break
            in_fm = True
            continue
        if in_fm and line.startswith('updated:'):
            if line.strip() == f'updated: {today}':
                return lines, 'unchanged'
            lines[i] = f'updated: {today}\n'
            return lines, 'updated'
    return lines, 'missing'


def find_heading_section(lines, headings):
    """Return (start, end) of the first matching heading's section.

    end is the index of the next '## ' heading (or len(lines)).
    """
    start = None
    for i, line in enumerate(lines):
        if any(line.strip() == h for h in headings):
            start = i
            break
    if start is None:
        return None, None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith('## '):
            end = i
            break
    return start, end


def append_bullet(lines, start, end, bullet):
    """Insert bullet at the end of the section [start, end), before trailing
    blank lines. Returns the new lines list."""
    insert_at = end
    while insert_at > start + 1 and lines[insert_at - 1].strip() == '':
        insert_at -= 1
    # Ensure exactly one blank line before the bullet if content precedes it
    prefix = [] if insert_at == start + 1 and lines[insert_at - 1].strip() == '' else []
    new_lines = lines[:insert_at] + prefix + [bullet + '\n', '\n'] + lines[insert_at:]
    # Avoid double blank line before the next heading
    if new_lines[insert_at + 1].strip() == '' and insert_at + 2 < len(new_lines) \
            and new_lines[insert_at + 2].startswith('## '):
        del new_lines[insert_at + 1]
    return new_lines


def update_entity(path, slug, display, title, venue, year, role, note, today):
    """Apply the append-only update pattern to one entity page."""
    if not os.path.isfile(path):
        print(f"WARN: {path} does not exist — new authors need a hand-created "
              f"page (Step 6 template); skipped", file=sys.stderr)
        return False

    with open(path, encoding='utf-8') as f:
        text = f.read()

    if f'sources/{slug}' in text:
        print(f"SKIP: {path} already references sources/{slug}")
        return True

    lines = text.splitlines(keepends=True)

    lines, fm_status = update_frontmatter_date(lines, today)
    if fm_status == 'missing':
        print(f"WARN: no 'updated:' field found in frontmatter of {path}",
              file=sys.stderr)

    # Key/Notable Contributions bullet
    venue_year = f'({venue}, {year})' if venue and year else \
                 (f'({venue})' if venue else (f'({year})' if year else ''))
    note_part = f' — {note}' if note else ''
    contrib_bullet = f'- {role} "{title}" {venue_year}{note_part} — [[sources/{slug}|{display}]]'

    start, end = find_heading_section(lines, CONTRIB_HEADINGS)
    if start is None:
        print(f"WARN: no {' or '.join(CONTRIB_HEADINGS)} section in {path}; "
              f"bullet not added", file=sys.stderr)
    else:
        lines = append_bullet(lines, start, end, contrib_bullet)

    # Related Sources bullet
    src_bullet = f'- [[sources/{slug}|{display}: {title}]]'
    start, end = find_heading_section(lines, ('## Related Sources',))
    if start is None:
        lines += ['\n', '## Related Sources\n', '\n', src_bullet + '\n']
    else:
        lines = append_bullet(lines, start, end, src_bullet)

    # Normalize EOF: collapse trailing blank lines to a single newline
    while lines and lines[-1].strip() == '':
        lines.pop()
    if lines and not lines[-1].endswith('\n'):
        lines[-1] += '\n'

    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"Updated: {path}")
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--slug', required=True, help='Source page slug (no .md)')
    p.add_argument('--entities', nargs='+', required=True,
                   help='Entity page slugs (no .md) — must already exist')
    p.add_argument('--note', default=None,
                   help='Paper-specific description inserted before the source wikilink')
    p.add_argument('--role', default='Co-author of',
                   help='Bullet verb phrase (default: "Co-author of"; '
                        'e.g. "First author of")')
    args = p.parse_args()

    display, title, venue, year = read_source_page(args.slug)
    today = datetime.date.today().isoformat()
    print(f"Source: {display}: {title}")
    print(f"Venue:  {venue} {year}\n")

    ok = True
    for eslug in args.entities:
        path = os.path.join('wiki', 'entities', f'{eslug}.md')
        if not update_entity(path, args.slug, display, title, venue, year,
                             args.role, args.note, today):
            ok = False

    if not ok:
        sys.exit(1)
    print("\nDone. Review the appended bullets and polish wording if needed "
          "(one Edit per file, sequential).")


if __name__ == '__main__':
    main()
