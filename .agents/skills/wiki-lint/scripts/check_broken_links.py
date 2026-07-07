#!/usr/bin/env python3
"""Step 5: Check for broken wikilinks with categorization.

Categories:
  - Truly broken: target genuinely doesn't exist anywhere
  - Missing category prefix: bare slug without category (e.g., [[beamforming]])
  - wiki/ prefix: redundant wiki/ in path (e.g., [[wiki/concepts/foo]])
  - Convention violations: ../ relative prefixes
  - Log.md informal refs: human-readable names in log entries

Handles escaped pipes (\\|) in markdown tables and section anchors (#Heading).
"""
import sys, glob, os, re

sys.stdout.reconfigure(encoding='utf-8')


def extract_target(raw_link):
    """Extract the page target from a [[...]] wikilink.

    Handles: [[target]], [[target|display]], [[target#Section|display]],
             [[target\\|display]] (escaped pipe in markdown tables)
    """
    if '#' in raw_link:
        raw_link = raw_link.split('#')[0]
    if '\\|' in raw_link:
        target = raw_link.split('\\|')[0].strip()
    elif '|' in raw_link:
        target = raw_link.split('|')[0].strip()
    else:
        target = raw_link.strip()
    return target


categories = ['entities', 'concepts', 'sources', 'synthesis', 'queries']

truly_broken = {}
missing_prefix = {}
wiki_prefix = {}
convention_violations = {}
log_refs = {}

for f in glob.glob('wiki/**/*.md', recursive=True):
    rel = os.path.relpath(f)
    is_log = 'log.md' in rel

    with open(f, encoding='utf-8') as fh:
        for m in re.finditer(r'\[\[([^\[\]]+?)\]\]', fh.read()):
            raw = m.group(1)
            if raw.strip() == '...':
                continue

            target = extract_target(raw)
            if not target:
                continue

            if target.startswith('../'):
                convention_violations.setdefault(target, []).append(rel)
                continue

            if target.startswith('wiki/'):
                fixed = target[5:]
                fixed_path = os.path.normpath(f'wiki/{fixed}.md')
                if os.path.exists(fixed_path):
                    wiki_prefix.setdefault(target, []).append((rel, fixed))
                else:
                    truly_broken.setdefault(target, []).append(rel)
                continue

            target_path = os.path.normpath(f'wiki/{target}.md')
            if not os.path.exists(target_path):
                found_cat = None
                if '/' not in target:
                    for cat in categories:
                        if os.path.exists(f'wiki/{cat}/{target}.md'):
                            found_cat = cat
                            break

                if found_cat and not is_log:
                    missing_prefix.setdefault(target, []).append(
                        (rel, f'{found_cat}/{target}'))
                elif is_log:
                    log_refs.setdefault(target, []).append(rel)
                else:
                    truly_broken.setdefault(target, []).append(rel)

# Print report
print('=== Broken Wikilinks Report ===')
print()

print(f'Truly broken: {len(truly_broken)}')
for t in sorted(truly_broken)[:15]:
    print(f'  [[{t}]]')
    for s in truly_broken[t][:2]:
        print(f'    from: {s}')
if len(truly_broken) > 15:
    print(f'    ... and {len(truly_broken) - 15} more')
print()

print(f'Missing category prefix: {len(missing_prefix)}')
for t in sorted(missing_prefix)[:10]:
    for s, fix in missing_prefix[t][:2]:
        print(f'  [[{t}]]  ->  [[{fix}]]  (from {s})')
if len(missing_prefix) > 10:
    print(f'  ... and {len(missing_prefix) - 10} more')
print()

print(f'wiki/ prefix: {len(wiki_prefix)}')
for t in sorted(wiki_prefix)[:10]:
    for s, fix in wiki_prefix[t][:2]:
        print(f'  [[{t}]]  ->  [[{fix}]]  (from {s})')
if len(wiki_prefix) > 10:
    print(f'  ... and {len(wiki_prefix) - 10} more')
print()

print(f'Convention violations (../ prefix): {len(convention_violations)}')
for t in sorted(convention_violations)[:5]:
    for s in convention_violations[t][:2]:
        print(f'  [[{t}]]  (from {s})')
if len(convention_violations) > 5:
    print(f'  ... and {len(convention_violations) - 5} more')
print()

print(f'Log.md informal refs: {len(log_refs)}')
for t in sorted(log_refs)[:5]:
    print(f'  [[{t}]]')
if len(log_refs) > 5:
    print(f'  ... and {len(log_refs) - 5} more')
