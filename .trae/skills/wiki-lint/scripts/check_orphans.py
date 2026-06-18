#!/usr/bin/env python3
"""Step 6: Check for orphan pages (no inbound references).

Searches both wikilinks [[target]] and markdown links [text](../target.md)
across all wiki content. The markdown link regex handles nested brackets
in link text (e.g., Sinh[ArcCosh[x]]).
"""
import sys, glob, os, re

sys.stdout.reconfigure(encoding='utf-8')

# Collect all page names per category
all_pages = {}
for cat in ('entities', 'concepts', 'sources', 'synthesis', 'queries'):
    pages = [
        os.path.splitext(os.path.basename(f))[0]
        for f in glob.glob(f'wiki/{cat}/*.md')
        if 'index.md' not in f
    ]
    all_pages[cat] = set(pages)


def extract_target(raw_link):
    """Extract page target from a [[...]] wikilink."""
    if '#' in raw_link:
        raw_link = raw_link.split('#')[0]
    if '\\|' in raw_link:
        target = raw_link.split('\\|')[0].strip()
    elif '|' in raw_link:
        target = raw_link.split('|')[0].strip()
    else:
        target = raw_link.strip()
    return target


# Collect ALL references
all_references = set()

for f in glob.glob('wiki/**/*.md', recursive=True):
    with open(f, encoding='utf-8') as fh:
        content = fh.read()

        # 1. Wikilinks [[...]]
        for m in re.finditer(r'\[\[([^\[\]]+?)\]\]', content):
            raw = m.group(1)
            if raw.strip() == '...':
                continue
            target = extract_target(raw)
            if not target:
                continue
            if target.startswith('../'):
                target = target.replace('../', '')
            if target.startswith('wiki/'):
                target = target[5:]
            all_references.add(target)
            if '/' in target:
                all_references.add(target.split('/')[1])

        # 2. Markdown links [text](path.md) with nested bracket support
        for m in re.finditer(
            r'\[([^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*)\]\(([^)]+)\)', content
        ):
            path = m.group(2)
            if path.endswith('.md'):
                path = path[:-3]
            if path.startswith('../'):
                path = path.replace('../', '')
            if path.startswith('wiki/'):
                path = path[5:]
            if '#' in path:
                path = path.split('#')[0]
            all_references.add(path)
            if '/' in path:
                all_references.add(path.split('/')[1])

# Report orphans
print('=== Orphan Pages ===')
total_orphans = 0
for cat in ('entities', 'concepts', 'sources', 'synthesis', 'queries'):
    orphans = []
    for page in sorted(all_pages[cat]):
        cat_target = f'{cat}/{page}'
        if cat_target not in all_references and page not in all_references:
            orphans.append(page)
    print(f'{cat}: {len(orphans)} orphans out of {len(all_pages[cat])} pages')
    for o in orphans:
        print(f'  {cat}/{o}')
    total_orphans += len(orphans)
print(f'\nTotal orphan pages: {total_orphans}')
