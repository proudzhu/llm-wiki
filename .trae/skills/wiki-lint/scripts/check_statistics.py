#!/usr/bin/env python3
"""Step 7: Check statistics consistency between stated counts and actual files.

Reads the Statistics section from wiki/index.md and compares stated counts
against actual files on disk. Reports mismatches per category.
"""
import sys, os, re

sys.stdout.reconfigure(encoding='utf-8')

with open('wiki/index.md', encoding='utf-8') as f:
    content = f.read()

# Parse stated statistics
stats = {}
for m in re.finditer(
    r'- \*\*(Entities|Concepts|Sources|Synthesis|Queries|Total pages)\*\*: (\d+)',
    content,
):
    stats[m.group(1)] = int(m.group(2))

print('Stated statistics:')
for name in ('Entities', 'Concepts', 'Sources', 'Synthesis', 'Queries', 'Total pages'):
    print(f'  {name}: {stats.get(name, "?")}')

m = re.search(r'- \*\*Last updated\*\*: (\S+)', content)
if m:
    print(f'  Last updated: {m.group(1)}')

# Verify against actual files
print()
dirs_map = {
    'Entities': 'entities',
    'Concepts': 'concepts',
    'Sources': 'sources',
    'Synthesis': 'synthesis',
    'Queries': 'queries',
}
for display, d in dirs_map.items():
    actual = len([
        f for f in os.listdir(f'wiki/{d}')
        if f.endswith('.md') and f != 'index.md'
    ])
    stated = stats.get(display)
    if stated == actual:
        print(f'  OK {display}: stated={stated}, actual={actual}')
    else:
        print(f'  MISMATCH {display}: stated={stated}, actual={actual}')

total_actual = sum(
    len([
        f for f in os.listdir(f'wiki/{d}')
        if f.endswith('.md') and f != 'index.md'
    ])
    for d in ('entities', 'concepts', 'sources', 'synthesis', 'queries')
)
stated_total = stats.get('Total pages')
if stated_total == total_actual:
    print(f'  OK Total pages: stated={stated_total}, actual={total_actual}')
else:
    print(f'  MISMATCH Total pages: stated={stated_total}, actual={total_actual}')
