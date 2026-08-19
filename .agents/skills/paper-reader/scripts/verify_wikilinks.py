#!/usr/bin/env python3
"""Step 12 pre-check: Verify wikilinks in new/modified wiki pages point to existing files.

Catches broken `[[concepts/foo|Foo]]`, `[[entities/bar|Bar]]`, etc. BEFORE
running `mkdocs build --strict`, so the model can fix typos or create missing
pages without a build-fail-fix cycle.

Usage:
  # Check the source page for a slug + all new/modified wiki/*.md files
  uv run python .agents/skills/paper-reader/scripts/verify_wikilinks.py --slug SLUG

  # Check specific files
  uv run python .agents/skills/paper-reader/scripts/verify_wikilinks.py --files wiki/sources/foo.md wiki/concepts/bar.md

  # Check all wiki/*.md files modified since HEAD (no slug/files)
  uv run python .agents/skills/paper-reader/scripts/verify_wikilinks.py

Exit code 0 = all wikilinks resolve, 1 = broken links found.
"""
import argparse
import os
import re
import subprocess
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass

# Matches [[category/slug|text]], [[category/slug#section|text]],
# [[category/slug]] (no display text), and [[category/slug#section]].
# Categories: entities, concepts, sources, synthesis, queries.
# Does NOT match [[raw/...]] (image embeds — handled by map_figures.py)
# or bare [[slug]] (no slash — these are convention violations, not
# broken-link candidates for this script).
#
# Slug capture excludes backslash so that `\|` (the MkDocs/Obsidian
# pipe-escape used in table cells, e.g. `[[concepts/foo\|Foo]]`) is
# not treated as part of the slug. Without this exclusion, the regex
# would capture slug='foo\' and look for wiki/concepts/foo\.md, which
# never exists — producing false-positive NOT FOUND reports on every
# wikilink written inside a markdown table.
WIKILINK_RE = re.compile(
    r'\[\['
    r'(entities|concepts|sources|synthesis|queries)/([^\]|#\\]+)'
    r'(?:#[^\]|\\]*)?'
    r'(?:\\?\|[^\]]*)?'
    r'\]\]'
)


def get_modified_wiki_files():
    """Return list of wiki/*.md files modified or untracked since HEAD."""
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain', '--', 'wiki/'],
            capture_output=True, text=True, encoding='utf-8', errors='replace'
        )
        files = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            # Format: XY <path>  (X=staged, Y=worktree status)
            status = line[:2]
            path = line[3:].split(' -> ')[-1].strip().replace('/', os.sep)
            if path.endswith('.md') and os.path.exists(path):
                files.append(path)
        return files
    except (subprocess.SubprocessError, FileNotFoundError):
        return []


def extract_wikilinks(file_path):
    """Yield (line_no, full_match, category, slug) for each wikilink in file."""
    try:
        with open(file_path, encoding='utf-8') as f:
            for idx, line in enumerate(f, start=1):
                for m in WIKILINK_RE.finditer(line):
                    yield (idx, m.group(0), m.group(1), m.group(2).strip())
    except (IOError, OSError):
        return


def check_wikilink(category, slug, project_root):
    """Return True if wiki/{category}/{slug}.md exists."""
    target = os.path.join(project_root, 'wiki', category, f'{slug}.md')
    return os.path.exists(target)


def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--slug', help='Paper slug — checks wiki/sources/{slug}.md plus modified wiki files')
    p.add_argument('--files', nargs='+', help='Specific files to check')
    args = p.parse_args()

    project_root = os.getcwd()
    files_to_check = []

    if args.files:
        files_to_check = [f.replace('/', os.sep) for f in args.files]
    elif args.slug:
        source_page = os.path.join('wiki', 'sources', f'{args.slug}.md')
        if os.path.exists(source_page):
            files_to_check.append(source_page)
        files_to_check.extend(get_modified_wiki_files())
    else:
        files_to_check = get_modified_wiki_files()

    # Deduplicate while preserving order
    seen = set()
    files_to_check = [f for f in files_to_check if not (f in seen or seen.add(f))]

    if not files_to_check:
        print("No wiki files to check.")
        return 0

    # Filter to existing .md files under wiki/
    files_to_check = [f for f in files_to_check
                      if f.endswith('.md') and f.startswith('wiki' + os.sep)
                      and os.path.exists(f)]

    if not files_to_check:
        print("No wiki/*.md files to check.")
        return 0

    print(f"Checking {len(files_to_check)} file(s) for broken wikilinks...\n")

    broken = []
    total_links = 0

    for fpath in files_to_check:
        for line_no, full_match, category, slug in extract_wikilinks(fpath):
            total_links += 1
            if not check_wikilink(category, slug, project_root):
                broken.append({
                    'file': fpath,
                    'line': line_no,
                    'link': full_match,
                    'target': f'wiki/{category}/{slug}.md',
                })

    print(f"Scanned {total_links} wikilink(s) across {len(files_to_check)} file(s).")

    if not broken:
        print("OK: all wikilinks resolve to existing pages.")
        return 0

    print(f"\nBROKEN: {len(broken)} wikilink(s) point to non-existent pages:\n")
    for b in broken:
        print(f"  {b['file']}:{b['line']}")
        print(f"    {b['link']}")
        print(f"    -> {b['target']} (NOT FOUND)\n")

    print("Fix: create the missing page, correct the slug, or use plain text.")
    return 1


if __name__ == '__main__':
    sys.exit(main())
