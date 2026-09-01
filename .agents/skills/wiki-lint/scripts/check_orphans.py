#!/usr/bin/env python3
"""Step 6: Check for orphan pages (no inbound references).

Searches both wikilinks [[target]] and markdown links [text](path.md)
across all wiki content. Link extraction is robust to nested brackets
in display text (e.g., [Why ... Sinh[ArcCosh[x]]](path)) and to links
inside code (fenced blocks / inline code spans are skipped).
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


# Collect ALL references
all_references = set()

for f in glob.glob('wiki/**/*.md', recursive=True):
    with open(f, encoding='utf-8') as fh:
        content = fh.read()

    # Links inside code (fenced blocks / inline spans) are examples, not links
    content = re.sub(r'```[\s\S]*?```', '', content)
    content = re.sub(r'`[^`\n]*`', '', content)

    # 1. Wikilinks [[...]] — capture the target portion only: chars after [[
    #    up to the first |, #, ] or newline. Handles escaped pipes (\|),
    #    section anchors, and nested brackets in display text.
    for m in re.finditer(r'\[\[([^\[\]|#\n]+)(?=[\]|#\n])', content):
        target = m.group(1).strip().rstrip('\\').strip()
        if not target or '...' in target:
            continue
        if target.startswith('../'):
            target = target.replace('../', '')
        if target.startswith('wiki/'):
            target = target[5:]
        all_references.add(target)
        if '/' in target:
            all_references.add(target.split('/')[1])

    # 2. Markdown link destinations ](path) — matching the destination only
    #    means any nesting in the link text is handled automatically.
    for m in re.finditer(r'\]\(([^)\n]+)\)', content):
        path = m.group(1).strip()
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
