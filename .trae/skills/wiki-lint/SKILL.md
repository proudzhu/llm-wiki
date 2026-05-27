---
name: "wiki-lint"
description: "Performs comprehensive health check of the LLM wiki knowledge base. Invoke when user asks to lint, health check, or verify wiki consistency."
---

# Wiki Lint Skill

This skill performs a comprehensive health check of the LLM wiki knowledge base, checking for index drift, broken links, orphan pages, and data gaps.

## When to Invoke

- User asks to "lint" the wiki
- User requests a health check or consistency verification
- After bulk operations (ingests, migrations) to verify integrity

## Lint Workflow

### Step 1: Understand Lint Requirements

Read `schema/AGENTS.md` to understand the lint workflow requirements (contradictions, stale claims, orphan pages, missing pages, cross-references, data gaps).

### Step 2: Count Actual Files

Use Python to count actual files in each directory:

```bash
python -c "
import os
dirs = {'entities':0,'concepts':0,'sources':0,'synthesis':0,'queries':0}
for d in dirs:
    count = len([f for f in os.listdir(f'wiki/{d}') if f.endswith('.md') and f != 'index.md'])
    dirs[d] = count
total = sum(dirs.values())
print(f'Actual: {dirs[\"entities\"]} entities, {dirs[\"concepts\"]} concepts, {dirs[\"sources\"]} sources, {dirs[\"synthesis\"]} synthesis, {dirs[\"queries\"]} queries = {total} total')
"
```

### Step 3: Count Index Rows

Count rows in each index file using Python (reliable regex across all platforms):

```bash
python -c "
import re
with open('wiki/index.md') as f:
    content = f.read()
for name in ('entities','concepts','sources','synthesis','queries'):
    count = len(re.findall(rf'^\\| \\[\\[{name}/', content, re.MULTILINE))
    print(f'Main index {name}: {count}')
"
```

Also check subdirectory indexes:

```bash
python -c "
import re
for name in ('entities','concepts','sources','synthesis','queries'):
    with open(f'wiki/{name}/index.md') as f:
        count = len(re.findall(r'^\\| \\[\\[' + name + r'/', f.read(), re.MULTILINE))
    print(f'Sub-index {name}: {count}')
"
```

### Step 4: Identify Missing & Phantom Entries

Compare actual files against index entries to find both **missing entries** (file exists but not in index) and **phantom entries** (index row with no file). Also check for **duplicate rows** (same slug multiple times):

```bash
python -c "
import os, re
from collections import Counter

for name in ('entities','concepts','sources','synthesis'):
    actual = set(os.path.splitext(f)[0] for f in os.listdir(f'wiki/{name}') if f.endswith('.md') and f != 'index.md')
    indexed = set()
    indexed_list = []
    with open('wiki/index.md') as f:
        for line in f:
            m = re.match(r'^\\| \\[\\[' + name + r'/([^|\\\\]+)', line)
            if m:
                indexed.add(m.group(1))
                indexed_list.append(m.group(1))
    
    missing = actual - indexed
    phantom = indexed - actual
    dupes = {k:v for k,v in Counter(indexed_list).items() if v > 1}
    
    print(f'{name}: {len(actual)} files, {len(indexed)} indexed')
    if missing:
        print(f'  MISSING from index ({len(missing)}):')
        for x in sorted(missing): print(f'    {x}')
    if phantom:
        print(f'  PHANTOM in index ({len(phantom)}):')
        for x in sorted(phantom): print(f'    {x}')
    if dupes:
        print(f'  DUPLICATE rows ({len(dupes)}):')
        for x, c in dupes.items(): print(f'    {x} appears {c}x')
"
```

Also check subdirectory indexes for consistency:

```bash
for name in entities concepts sources synthesis queries; do
  actual=$(ls wiki/$name/*.md 2>/dev/null | grep -v index.md | wc -l)
  indexed=$(grep -c '^| \[\[' wiki/$name/index.md 2>/dev/null || echo 0)
  echo "Sub-index $name: $indexed indexed vs $actual actual"
done
```

### Step 5: Check for Broken Wikilinks

Search for wikilinks that reference non-existent files. **Important:** use `os.path.normpath()` + `os.path.exists()` to correctly resolve `../` relative paths (which are convention violations but not actually broken):

```bash
python -c "
import glob, os, re

wikilinks = {}
for f in glob.glob('wiki/**/*.md', recursive=True):
    with open(f, encoding='utf-8') as fh:
        for m in re.finditer(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', fh.read()):
            link = m.group(1)
            if link.strip() == '...':  # skip placeholder in log.md
                continue
            if link not in wikilinks:
                wikilinks[link] = []
            wikilinks[link].append(os.path.relpath(f))

broken = []
for link in sorted(wikilinks):
    target = os.path.normpath(f'wiki/{link}.md')
    if not os.path.exists(target):
        broken.append(link)

print(f'Total wikilinks found: {len(wikilinks)}')
print(f'Broken wikilinks: {len(broken)}')
for b in broken[:20]:
    sources = wikilinks.get(b, [])
    print(f'  BROKEN: {b}')
    for s in sources[:2]:
        print(f'    from: {s}')
if len(broken) > 20:
    print(f'  ... and {len(broken)-20} more')
"
```

**Note:** Wikilinks using `../` prefixes (e.g., `[[../concepts/foo]]`) violate the vault-absolute convention but resolve correctly in MkDocs builds. They are not broken links — only links whose normalized path doesn't exist on disk are truly broken.

### Step 6: Check for Orphan Pages

Find pages with no inbound wikilinks. Use Python for robust file scanning:

```bash
python -c "
import glob, os, re
# Get all page names
entity_pages = [os.path.splitext(os.path.basename(f))[0] for f in glob.glob('wiki/entities/*.md') if 'index.md' not in f]

# Collect all wikilink targets from ALL wiki content
all_links = set()
for f in glob.glob('wiki/**/*.md', recursive=True):
    with open(f, encoding='utf-8') as fh:
        for m in re.finditer(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', fh.read()):
            all_links.add(m.group(1))

# Find orphans (pages never linked to)
orphans = [p for p in entity_pages if p not in all_links]
print(f'Orphan pages: {len(orphans)}')
for o in sorted(orphans): print(f'  {o}')
```

Note: Many pages are expected to be linked only from index files, not from other content pages.

### Step 7: Check Statistics Consistency

Read the Statistics section in `wiki/index.md` and verify counts match actual files from Step 2:

```bash
python -c "
import re
with open('wiki/index.md') as f:
    content = f.read()
# Extract stats from the Statistics section
stats = re.findall(r'- \*\*(Entities|Concepts|Sources|Synthesis|Queries|Total pages)\*\*: (\d+)', content)
for name, val in stats:
    print(f'  {name}: {val}')
"
```

### Step 8: Rebuild Indexes (if drift detected)

If index drift is found, use the bundled `rebuild_index.py` script:

```bash
python .trae/skills/wiki-lint/rebuild_index.py
```

The script:
1. Reads existing index entries from `wiki/index.md` using regex (handles escaped `\|` in wikilinks)
2. Compares against actual files in `wiki/entities/`, `wiki/concepts/`, `wiki/sources/`
3. Outputs missing entries in markdown table format with auto-generated summaries (stdout only, not stderr)
4. Preserves existing high-quality summaries (only generates new ones for truly missing entries)

> ⚠️ **For Python in `pwsh -Command`**: When passing multi-line Python scripts inside `"..."`, escape `$` as `` `$ ``. Better yet, write the script to a temp `.py` file and run it with `python tmp_lint_script.py`.

After running the script, use the output to:
1. Add missing entries to `wiki/index.md` (entities, concepts, sources tables)
2. Add missing entries to `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md`
3. Remove any duplicate entries found
4. Update statistics section in `wiki/index.md`

**Manual rebuild approach** (if script is unavailable):

1. Read existing index entries to preserve high-quality summaries
2. Identify missing entries
3. Generate summaries from page content (skip tag lines, frontmatter, find first meaningful paragraph)
4. Add missing entries to all index files:
   - `wiki/index.md` (main index)
   - `wiki/entities/index.md`
   - `wiki/concepts/index.md`
   - `wiki/sources/index.md`
5. Remove any duplicates found
6. Update statistics section

### Step 9: Log Results

Append lint results to `wiki/log.md`. Include the `---` separator before the entry (consistent with existing log format):

```markdown
---

## [YYYY-MM-DD] lint | Health check

- **Index consistency**: [summary of findings — which categories match and which don't]
- **Broken links**: [count of truly broken links; note convention-violating `../` links separately]
- **Duplicate entries**: [count and which slugs]
- **Orphan pages**: [count per category]
- **Statistics**: [stated vs actual, whether Total pages is correct]
- **Actions taken**: [rebuild details, entries added/removed, stats corrected]
```

## Common Issues

### Index Drift
Accumulates over multiple ingest operations where subdirectory indexes were updated but main index wasn't fully synchronized. Fix by rebuilding all indexes.

### Duplicate Entries
Same entity/concept/source appears multiple times in index with different summaries. Fix by keeping the better summary and removing the duplicate.

### Escaped Pipes in Wikilinks
Markdown tables use `\|` for display text containing pipes. Regex patterns must handle both escaped and unescaped pipes: `r'\[\[entities/([^\|\\]+)(?:\\?\|[^\]]+)?\]\]'`

### Unicode Encoding on Windows
Python's default 'gbk' codec can't handle special characters. Use `sys.stdout.reconfigure(encoding='utf-8')` or redirect output to file.

## Verification Commands

After any index rebuild, verify all diffs are 0:

```python
# Run this as: python verification_script.py
import os, re

for name in ('entities','concepts','sources','synthesis'):
    idx_path = f'wiki/{name}/index.md'
    actual = len([f for f in os.listdir(f'wiki/{name}') if f.endswith('.md') and f != 'index.md'])
    
    indexed = 0
    with open(idx_path) as f:
        for line in f:
            if re.match(r'^\| \[\[', line):
                indexed += 1
    
    diff = indexed - actual
    status = '✅' if diff == 0 else '❌'
    print(f'{status} {name}: {indexed} indexed, {actual} actual (diff={diff})')

# Also check main index
total_actual = sum(
    len([f for f in os.listdir(f'wiki/{d}') if f.endswith('.md') and f != 'index.md'])
    for d in ('entities','concepts','sources','synthesis','queries')
)
print(f'\nTotal actual files: {total_actual}')
```

```powershell
# Quick PowerShell check (forward slashes, ${} for variables)
$eidx = (Select-String -Path "wiki/entities/index.md" -Pattern '^\| \[\[entities/' | Measure-Object).Count
$eact = (Get-ChildItem "wiki/entities/*.md" -Exclude "index.md").Count
$diff = $eidx - $eact
if ($diff -eq 0) { Write-Output "✅ Entities: ${eidx} = ${eact}" }
else { Write-Output "❌ Entities: ${eidx} indexed vs ${eact} actual (diff=${diff})" }
```
