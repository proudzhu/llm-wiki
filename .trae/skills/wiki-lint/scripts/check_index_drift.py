#!/usr/bin/env python3
"""Step 4: Check for missing entries, phantom entries, and duplicates in indexes.

Compares actual files on disk against index entries in both the main index
and subdirectory indexes. Reports:
  - MISSING: files that exist but have no index row
  - PHANTOM: index rows pointing to non-existent files
  - DUPLICATE: slugs appearing multiple times
"""
import sys, os, re
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

print('=== Main index vs actual files ===')
for name in ('entities', 'concepts', 'sources', 'synthesis'):
    actual = set(
        os.path.splitext(f)[0]
        for f in os.listdir(f'wiki/{name}')
        if f.endswith('.md') and f != 'index.md'
    )
    indexed = set()
    indexed_list = []
    with open('wiki/index.md', encoding='utf-8') as f:
        for line in f:
            # Matches: | [[category/slug|display]] or | [[category/slug\\|display]]
            # [^|\\\]]+ captures slug chars that are not |, \, or ]
            m = re.match(r'^\| \[\[' + name + r'/([^|\\\]]+)', line)
            if m:
                indexed.add(m.group(1))
                indexed_list.append(m.group(1))

    missing = actual - indexed
    phantom = indexed - actual
    dupes = {k: v for k, v in Counter(indexed_list).items() if v > 1}

    print(f'{name}: {len(actual)} files, {len(indexed)} indexed')
    if missing:
        print(f'  MISSING from index ({len(missing)}):')
        for x in sorted(missing):
            print(f'    {x}')
    if phantom:
        print(f'  PHANTOM in index ({len(phantom)}):')
        for x in sorted(phantom):
            print(f'    {x}')
    if dupes:
        print(f'  DUPLICATE rows ({len(dupes)}):')
        for x, c in dupes.items():
            print(f'    {x} appears {c}x')
    if not missing and not phantom and not dupes:
        print(f'  OK All consistent')

print()
print('=== Subdirectory indexes vs actual files ===')
for name in ('entities', 'concepts', 'sources', 'synthesis', 'queries'):
    actual = len([f for f in os.listdir(f'wiki/{name}')
                  if f.endswith('.md') and f != 'index.md'])
    with open(f'wiki/{name}/index.md', encoding='utf-8') as f:
        indexed = len(re.findall(r'^\| \[\[', f.read(), re.MULTILINE))
    diff = indexed - actual
    status = 'OK' if diff == 0 else 'MISMATCH'
    print(f'[{status}] {name}: {indexed} indexed vs {actual} actual (diff={diff})')
