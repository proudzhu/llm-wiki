#!/usr/bin/env python3
"""Step 2: Apply wikilink convention fixes in-place.

Fixable categories:
  - missing_prefix: [[beamforming]] -> [[concepts/beamforming]]
  - wiki_prefix:    [[wiki/concepts/foo]] -> [[concepts/foo]]
  - dotdot_prefix:  [[../concepts/foo]] -> [[concepts/foo]]
  - log_informal:   [[Beamforming]] in log.md -> [[concepts/beamforming|Beamforming]]

Truly broken links are NEVER touched (manual review required).

The fixer is idempotent: running it on already-canonical links is a no-op.
Display text (after | or \\|) is preserved; only the link target is rewritten.
Section anchors (#Section) are preserved.

Usage:
  python fix_links.py --dry-run               # preview all fixes
  python fix_links.py                         # apply all fixes
  python fix_links.py --category missing_prefix
  python fix_links.py --file wiki/log.md
"""
import sys
import os
import re
import glob
import argparse
import tempfile

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

CATEGORIES = ['entities', 'concepts', 'sources', 'synthesis', 'queries']

ALL_CATEGORIES = {'missing_prefix', 'wiki_prefix', 'dotdot_prefix', 'log_informal'}


def extract_target(raw_link: str) -> tuple[str, str | None, str | None]:
    """Split a wikilink interior into (target, separator, rest).

    Returns:
        target: the link target (before any | or \\|)
        separator: None, '|', or '\\|' (the delimiter that introduced display text)
        rest: the display text after the separator, or None

    Section anchors are kept on the target side: e.g., for 'foo#Section|Display',
    target='foo#Section', separator='|', rest='Display'.
    """
    # Find the first separator (escaped pipe takes precedence over plain pipe)
    # In markdown tables, \\\n could exist but we don't expect it inside [[]].
    if '\\|' in raw_link:
        idx = raw_link.index('\\|')
        target = raw_link[:idx].strip()
        rest = raw_link[idx + 2:]
        return target, '\\|', rest
    if '|' in raw_link:
        idx = raw_link.index('|')
        target = raw_link[:idx].strip()
        rest = raw_link[idx + 1:]
        return target, '|', rest
    return raw_link.strip(), None, None


def split_anchor(target: str) -> tuple[str, str]:
    """Split 'foo#Section' -> ('foo', '#Section'). Returns (slug, anchor_or_empty)."""
    if '#' in target:
        idx = target.index('#')
        return target[:idx], target[idx:]
    return target, ''


def find_category_for_slug(slug: str, case_insensitive: bool = False) -> str | None:
    """Find which category contains a slug. Returns 'category/slug' or None."""
    if case_insensitive:
        slug_lower = slug.lower()
        for cat in CATEGORIES:
            d = f'wiki/{cat}'
            if not os.path.isdir(d):
                continue
            for entry in os.listdir(d):
                if entry.lower() == f'{slug_lower}.md':
                    return f'{cat}/{entry[:-3]}'
        return None

    for cat in CATEGORIES:
        if os.path.exists(f'wiki/{cat}/{slug}.md'):
            return f'{cat}/{slug}'
    return None


def compute_fix(raw_link: str, is_log: bool, categories: set[str]) -> tuple[str, str] | None:
    """Given the interior of a [[...]] wikilink, return (new_interior, fix_category) or None.

    Returns None if no fix applies (link is already canonical, or is truly broken,
    or the violation category is not in `categories`).
    """
    target, sep, rest = extract_target(raw_link)
    if not target:
        return None

    # raw/ embeds — already canonical
    if target.startswith('raw/'):
        return None

    slug, anchor = split_anchor(target)

    # ../ prefix -> strip
    if slug.startswith('../'):
        if 'dotdot_prefix' not in categories:
            return None
        new_slug = slug.lstrip('./')
        # Verify the fix target actually exists
        fixed_path = os.path.normpath(f'wiki/{new_slug}.md')
        if not os.path.exists(fixed_path):
            return None  # would be truly broken, skip
        new_target = new_slug + anchor
        new_interior = _reassemble(new_target, sep, rest)
        return new_interior, 'dotdot_prefix'

    # wiki/ prefix -> strip leading 'wiki/'
    if slug.startswith('wiki/'):
        if 'wiki_prefix' not in categories:
            return None
        new_slug = slug[5:]
        fixed_path = os.path.normpath(f'wiki/{new_slug}.md')
        if not os.path.exists(fixed_path):
            return None
        new_target = new_slug + anchor
        new_interior = _reassemble(new_target, sep, rest)
        return new_interior, 'wiki_prefix'

    # Already category-prefixed (has /)
    if '/' in slug:
        # Verify exists; if not, it's truly broken (not our problem)
        return None

    # Bare slug — try to find category
    target_path = os.path.normpath(f'wiki/{slug}.md')
    if os.path.exists(target_path):
        # Top-level page, already canonical
        return None

    # Try exact-match category lookup
    found = find_category_for_slug(slug)
    if found:
        if is_log and 'log_informal' in categories:
            # Log informal: preserve original text as display
            new_target = found + anchor
            # If no display text was set, add the original target as display
            if sep is None:
                new_interior = f'{new_target}|{slug}'
            else:
                new_interior = _reassemble(new_target, sep, rest)
            return new_interior, 'log_informal'
        if not is_log and 'missing_prefix' in categories:
            new_target = found + anchor
            new_interior = _reassemble(new_target, sep, rest)
            return new_interior, 'missing_prefix'
        return None

    # Case-insensitive match (log_informal only)
    if is_log and 'log_informal' in categories:
        found_ci = find_category_for_slug(slug, case_insensitive=True)
        if found_ci:
            new_target = found_ci + anchor
            if sep is None:
                new_interior = f'{new_target}|{slug}'
            else:
                new_interior = _reassemble(new_target, sep, rest)
            return new_interior, 'log_informal'

    # Truly broken — never touch
    return None


def _reassemble(target: str, sep: str | None, rest: str | None) -> str:
    """Reassemble a wikilink interior from parts."""
    if sep is None:
        return target
    # Preserve original separator style
    return f'{target}{sep}{rest}'


def fix_file(path: str, categories: set[str], dry_run: bool) -> tuple[int, dict]:
    """Apply fixes to a single file. Returns (fix_count, per_category_counts)."""
    rel = os.path.relpath(path).replace('\\', '/')
    is_log = rel.endswith('log.md')

    with open(path, encoding='utf-8') as fh:
        content = fh.read()

    per_cat = {c: 0 for c in ALL_CATEGORIES}

    def replace_match(m: re.Match) -> str:
        raw = m.group(1)
        if raw.strip() == '...':
            return m.group(0)
        result = compute_fix(raw, is_log=is_log, categories=categories)
        if result is None:
            return m.group(0)
        new_interior, cat = result
        per_cat[cat] += 1
        return f'[[{new_interior}]]'

    new_content = re.sub(r'\[\[([^\[\]]+?)\]\]', replace_match, content)

    total = sum(per_cat.values())
    if total == 0:
        return 0, per_cat

    if not dry_run:
        # Atomic write: temp file in same dir, then rename
        d = os.path.dirname(path)
        fd, tmp = tempfile.mkstemp(dir=d, suffix='.tmp', text=True)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8', newline='') as fh:
                fh.write(new_content)
            os.replace(tmp, path)
        except Exception:
            if os.path.exists(tmp):
                os.unlink(tmp)
            raise

    return total, per_cat


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without writing')
    parser.add_argument('--category', choices=sorted(ALL_CATEGORIES),
                        help='Apply only one category of fixes')
    parser.add_argument('--file', default=None,
                        help='Fix only this file (relative path from project root)')
    args = parser.parse_args()

    if args.category:
        categories = {args.category}
    else:
        categories = ALL_CATEGORIES

    if args.file:
        if not os.path.exists(args.file):
            print(f'Error: {args.file} not found', file=sys.stderr)
            sys.exit(1)
        files = [args.file]
    else:
        files = sorted(glob.glob('wiki/**/*.md', recursive=True))

    grand_total = 0
    grand_per_cat = {c: 0 for c in ALL_CATEGORIES}
    files_changed = 0

    for f in files:
        count, per_cat = fix_file(f, categories, dry_run=args.dry_run)
        if count > 0:
            files_changed += 1
            grand_total += count
            for c in ALL_CATEGORIES:
                grand_per_cat[c] += per_cat[c]
            rel = os.path.relpath(f).replace('\\', '/')
            cat_summary = ', '.join(f'{c}={per_cat[c]}' for c in sorted(ALL_CATEGORIES) if per_cat[c] > 0)
            print(f'  {rel}: {count} fixes ({cat_summary})')

    print(file=sys.stderr)
    print(f'=== Summary ===', file=sys.stderr)
    print(f'  Files {"would change" if args.dry_run else "changed"}: {files_changed}',
          file=sys.stderr)
    print(f'  Total fixes: {grand_total}', file=sys.stderr)
    for c in sorted(ALL_CATEGORIES):
        if grand_per_cat[c] > 0:
            print(f'    {c}: {grand_per_cat[c]}', file=sys.stderr)
    if args.dry_run:
        print('  (dry-run, no files written)', file=sys.stderr)


if __name__ == '__main__':
    main()
