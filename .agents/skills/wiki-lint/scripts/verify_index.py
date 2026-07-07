#!/usr/bin/env python3
"""Post-rebuild verification: confirm all index diffs are 0."""
import sys, os, re

sys.stdout.reconfigure(encoding='utf-8')

all_ok = True
for name in ('entities', 'concepts', 'sources', 'synthesis', 'queries'):
    idx_path = f'wiki/{name}/index.md'
    actual = len([
        f for f in os.listdir(f'wiki/{name}')
        if f.endswith('.md') and f != 'index.md'
    ])

    indexed = 0
    with open(idx_path, encoding='utf-8') as f:
        for line in f:
            if re.match(r'^\| \[\[', line):
                indexed += 1

    diff = indexed - actual
    if diff != 0:
        all_ok = False
    status = 'OK' if diff == 0 else 'MISMATCH'
    print(f'[{status}] {name}: {indexed} indexed, {actual} actual (diff={diff})')

total_actual = sum(
    len([
        f for f in os.listdir(f'wiki/{d}')
        if f.endswith('.md') and f != 'index.md'
    ])
    for d in ('entities', 'concepts', 'sources', 'synthesis', 'queries')
)
print(f'\nTotal actual files: {total_actual}')
sys.exit(0 if all_ok else 1)
