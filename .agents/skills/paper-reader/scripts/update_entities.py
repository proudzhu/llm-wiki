#!/usr/bin/env python3
"""Step 6 helper: append-only updates to existing author entity pages.

For each listed entity, derives the paper's title/venue/year/authors from
the source page (wiki/sources/{slug}.md) and applies the append-only update
pattern from page-templates.md automatically:

  1. frontmatter `updated:` -> today
  2. new bullet under `## Key Contributions` (or `## Notable Contributions`).
     Pages using a bold inline label instead of a heading —
     `**Key Contributions**:` followed by bullets (e.g. israel-cohen.md) —
     are also supported; the bullet is appended after the last bullet of the
     label's block.
     - Co-author of "Short Title" (Venue, Year) [--note] — [[sources/{slug}|Authors Year]]
     Known conference venues are abbreviated automatically, e.g.
     "IEEE International Conference on Acoustics, Speech and Signal
     Processing (ICASSP), 2020" -> "(ICASSP 2020)" (pitfalls.md #62);
     journals, preprints, and unrecognized venues pass through verbatim.
  3. new bullet under `## Related Sources`:
     - [[sources/{slug}|Authors Year: Full Title]]

This removes the most error-prone manual-edit batch of the ingest (4-6
entity pages x 2-3 edits each) while preserving the agent's role: run the
script for the guaranteed-consistent skeleton, then polish the Key
Contributions bullet wording (e.g., a paper-specific description via
--note) if desired.

Role semantics (pitfalls.md #61): --role applies ONLY to the FIRST listed
entity (conventionally the paper's first author); every subsequent entity
gets "Co-author of". This prevents the Yamaoka 2021 failure mode where
--role "First author of" relabeled co-authors Ono and Makino as first
authors, each needing a hand-fix Edit.

New authors (no page yet) are NOT handled — those are created by hand per
the Step 6 template. This script only updates existing pages.

Usage:
  uv run python .agents/skills/paper-reader/scripts/update_entities.py \
      --slug paper-slug --entities first-author co-author-1 co-author-2 \
      [--note "paper-specific contribution description"] \
      [--role "First author of"]  # first entity only; rest get "Co-author of"

Idempotent: any entity page already referencing sources/{slug} is skipped.

Exit code 0 = all pages updated or skipped cleanly, 1 = any error.
"""
import argparse, datetime, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')

CONTRIB_HEADINGS = ('## Key Contributions', '## Notable Contributions')

# Some entity pages use a bold inline label followed by bullets instead of a
# level-2 heading, e.g. israel-cohen.md: `**Key Contributions**:` then `- ...`
# bullets. The Wang 2021 ingest silently skipped such a page (bullet never
# added) because find_heading_section only matched `##` headings.
BOLD_LABEL_RE = re.compile(r'^\*\*(Key Contributions|Notable Contributions)\*\*:?\s*$')

# --- Venue abbreviation (pitfalls.md #62) ---
# Zotero stores proceedings under verbose titles like "IEEE International
# Conference on Acoustics, Speech and Signal Processing (ICASSP), 2020";
# written verbatim into entity bullets this bloats the pages. Known
# conferences are abbreviated to their standard acronym + year ("ICASSP
# 2020"); journals, arXiv preprints, and unrecognized venues pass through
# unchanged (whitelist-keyed, so a journal parenthetical like "(IMWUT)" or
# "(article number)" is never mistaken for a conference acronym).
#
# Keys are UPPERCASED candidate tokens; values are the canonical display form.
KNOWN_CONFERENCE_ABBRS = {
    'ICASSP': 'ICASSP',
    'WASPAA': 'WASPAA',
    'EUSIPCO': 'EUSIPCO',
    'IWAENC': 'IWAENC',
    'INTERSPEECH': 'Interspeech',
    'NORSIG': 'NORSIG',
    'APSIPA': 'APSIPA ASC',
    'APSIPA ASC': 'APSIPA ASC',
    'HSCMA': 'HSCMA',
    'ICCE-ASIA': 'ICCE-Asia',
    'AICIT': 'AICIT',
    'EURONOISE': 'Euronoise',
    'ISMIR': 'ISMIR',
    'NEURIPS': 'NeurIPS',
}

# "(ICASSP)", "(WASPAA)", "(EUSIPCO 2022)", "(APSIPA ASC 2022)", "(NORSIG 2004)"
ABBR_PAREN_RE = re.compile(
    r'\(([A-Za-z][A-Za-z0-9-]{1,11})((?:\sASC)?(?:\s20\d\d)?)\)')
# "ICASSP 2024 - ...", "Proc. IEEE ICASSP 2025", "Interspeech 2019"
ABBR_PREFIX_RE = re.compile(
    r'^(?:proc\.?\s+)?(?:ieee\s+|acm\s+)?'
    r'([A-Za-z][A-Za-z0-9-]{1,11})(?:\s+(20\d\d))?', re.IGNORECASE)


def abbreviate_venue(venue):
    """Return (abbr, year) for a known conference venue, else (None, None).

    Two tiers, both whitelist-keyed against KNOWN_CONFERENCE_ABBRS so that
    journals and preprints can never be caught:

      1. Parenthesized acronym, optionally followed by "ASC" and/or a year:
         "...Signal Processing (ICASSP), 2020", "(EUSIPCO 2022)",
         "(APSIPA ASC 2022)", "(NORSIG 2004)".
      2. Acronym prefix with optional year:
         "ICASSP 2024 - ...", "Proc. IEEE ICASSP 2025", "Interspeech 2019".

    The returned year is the one embedded in the acronym's parenthetical
    (tier 1) or prefix (tier 2), or None if the venue string puts the year
    elsewhere (the caller then falls back to the H1-derived year).
    """
    if not venue:
        return None, None
    m = ABBR_PAREN_RE.search(venue)
    if m:
        token, rest = m.group(1), m.group(2)
        ym = re.search(r'(20\d\d)', rest)
        key = (token + re.sub(r'\s20\d\d', '', rest)).upper()
        if key in KNOWN_CONFERENCE_ABBRS:
            return KNOWN_CONFERENCE_ABBRS[key], ym.group(1) if ym else None
        return None, None
    m = ABBR_PREFIX_RE.match(venue)
    if m and m.group(1).upper() in KNOWN_CONFERENCE_ABBRS:
        return KNOWN_CONFERENCE_ABBRS[m.group(1).upper()], m.group(2)
    return None, None


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


def find_bold_label_section(lines):
    """Return (start, end) for a `**Key Contributions**:`-style block.

    start = label line index; end = index just after the last bullet of the
    block. Bullets separated by blank lines still belong to the block; the
    block ends at the next `## ` heading or bold label. Returns (None, None)
    if no such label exists.
    """
    start = None
    for i, line in enumerate(lines):
        if BOLD_LABEL_RE.match(line.strip()):
            start = i
            break
    if start is None:
        return None, None
    last_bullet = None
    for i in range(start + 1, len(lines)):
        stripped = lines[i].strip()
        if stripped.startswith('## ') or BOLD_LABEL_RE.match(stripped):
            break
        if stripped.startswith('- '):
            last_bullet = i
    if last_bullet is None:
        return start, start + 1  # label present but no bullets yet
    return start, last_bullet + 1


def append_bullet(lines, start, end, bullet):
    """Insert bullet at the end of the section [start, end), before trailing
    blank lines. Returns the new lines list."""
    insert_at = end
    while insert_at > start + 1 and lines[insert_at - 1].strip() == '':
        insert_at -= 1
    new_lines = lines[:insert_at] + [bullet + '\n', '\n'] + lines[insert_at:]
    # Avoid double blank line: drop our inserted blank line if the original
    # text at the insertion point already starts with one.
    if insert_at + 2 < len(new_lines) and new_lines[insert_at + 2].strip() == '':
        del new_lines[insert_at + 1]
    return new_lines


def format_venue_year(venue, year):
    """Format the '(Venue, Year)' parenthetical for contribution bullets.

    Known conference venues are abbreviated first (pitfalls.md #62):
    'IEEE International Conference on Acoustics, Speech and Signal
    Processing (ICASSP), 2020' becomes '(ICASSP 2020)' — comma-free — using
    the year embedded in the venue when present, else the H1-derived year.

    Zotero venue strings for journals/preprints frequently already embed the
    publication year, either bare ('IEEE Transactions on Signal Processing,
    2021') or before a page range ('..., New Paltz, NY, 2011, pp. 189-192').
    Appending ', {year}' unconditionally produced '(..., 2021, 2021)' and
    '(..., NY, 2011, pp. 189-192, 2011)' in the Scheibler 2021 / Ono 2011 /
    Scheibler 2020 ingests, each requiring a hand-fix Edit (pitfalls.md #59).
    When the year already appears in the venue, keep the venue verbatim
    instead of appending it again.
    """
    abbr, venue_year = abbreviate_venue(venue)
    if abbr:
        y = venue_year or year
        return f'({abbr} {y})' if y else f'({abbr})'
    if venue and year:
        if re.search(rf'\b{re.escape(year)}\b', venue):
            return f'({venue})'
        return f'({venue}, {year})'
    if venue:
        return f'({venue})'
    if year:
        return f'({year})'
    return ''


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
    venue_year = format_venue_year(venue, year)
    note_part = f' — {note}' if note else ''
    contrib_bullet = f'- {role} "{title}" {venue_year}{note_part} — [[sources/{slug}|{display}]]'

    start, end = find_heading_section(lines, CONTRIB_HEADINGS)
    if start is None:
        # Fallback: bold inline label variant (`**Key Contributions**:`)
        start, end = find_bold_label_section(lines)
    if start is None:
        print(f"WARN: no {' or '.join(CONTRIB_HEADINGS)} section and no "
              f"'**Key Contributions**:' label in {path}; bullet not added",
              file=sys.stderr)
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
    print(f"Updated: {path} (role: {role})")
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
                   help='Bullet verb phrase applied to the FIRST listed '
                        'entity only (default: "Co-author of"; e.g. '
                        '"First author of"); all subsequent entities get '
                        '"Co-author of" (pitfalls.md #61)')
    args = p.parse_args()

    display, title, venue, year = read_source_page(args.slug)
    today = datetime.date.today().isoformat()
    print(f"Source: {display}: {title}")
    print(f"Venue:  {venue} {year}")
    print(f"        -> bullets will use: {format_venue_year(venue, year)}\n")

    ok = True
    for idx, eslug in enumerate(args.entities):
        path = os.path.join('wiki', 'entities', f'{eslug}.md')
        # --role applies to the first listed entity only (the paper's first
        # author by convention); every other entity is a co-author.
        role = args.role if idx == 0 else 'Co-author of'
        if not update_entity(path, args.slug, display, title, venue, year,
                             role, args.note, today):
            ok = False

    if not ok:
        sys.exit(1)
    print("\nDone. Review the appended bullets and polish wording if needed "
          "(one Edit per file, sequential).")


if __name__ == '__main__':
    main()
