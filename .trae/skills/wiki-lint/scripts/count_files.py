#!/usr/bin/env python3
"""Step 2: Count actual wiki page files in each category directory."""
import sys, os

sys.stdout.reconfigure(encoding='utf-8')

dirs = {'entities': 0, 'concepts': 0, 'sources': 0, 'synthesis': 0, 'queries': 0}
for d in dirs:
    count = len([f for f in os.listdir(f'wiki/{d}') if f.endswith('.md') and f != 'index.md'])
    dirs[d] = count
total = sum(dirs.values())
print(f'Actual: {dirs["entities"]} entities, {dirs["concepts"]} concepts, '
      f'{dirs["sources"]} sources, {dirs["synthesis"]} synthesis, '
      f'{dirs["queries"]} queries = {total} total')
