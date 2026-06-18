#!/usr/bin/env python3
"""Step 3: Count index rows in main index and subdirectory indexes."""
import sys, re

sys.stdout.reconfigure(encoding='utf-8')

# Main index
with open('wiki/index.md', encoding='utf-8') as f:
    content = f.read()
for name in ('entities', 'concepts', 'sources', 'synthesis', 'queries'):
    count = len(re.findall(rf'^\| \[\[{name}/', content, re.MULTILINE))
    print(f'Main index {name}: {count}')

print()

# Subdirectory indexes
for name in ('entities', 'concepts', 'sources', 'synthesis', 'queries'):
    with open(f'wiki/{name}/index.md', encoding='utf-8') as f:
        count = len(re.findall(r'^\| \[\[', f.read(), re.MULTILINE))
    print(f'Sub-index {name}: {count}')
