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

Use PowerShell to count actual files in each directory:

```powershell
# Count actual files (excluding index.md)
$entities = (Get-ChildItem "wiki/entities/*.md" -Exclude "index.md").Count
$concepts = (Get-ChildItem "wiki/concepts/*.md" -Exclude "index.md").Count
$sources = (Get-ChildItem "wiki/sources/*.md" -Exclude "index.md").Count
$synthesis = (Get-ChildItem "wiki/synthesis/*.md" -Exclude "index.md").Count
$queries = (Get-ChildItem "wiki/queries/*.md" -Exclude "index.md").Count
$total = $entities + $concepts + $sources + $synthesis + $queries
Write-Output "Actual: ${entities} entities, ${concepts} concepts, ${sources} sources, ${synthesis} synthesis, ${queries} queries = ${total} total"
```

> ⚠️ **Windows/cmd compatibility**: All PowerShell commands below must be run via `pwsh -NoProfile -Command "..."` since the default shell is cmd. Use forward slashes in paths to avoid escaping issues.

### Step 3: Count Index Rows

Count rows in each index file:

```powershell
# Count index rows
$eidx = (Select-String -Path "wiki/index.md" -Pattern '^\| \[\[entities/' | Measure-Object).Count
$cidx = (Select-String -Path "wiki/index.md" -Pattern '^\| \[\[concepts/' | Measure-Object).Count
$sidx = (Select-String -Path "wiki/index.md" -Pattern '^\| \[\[sources/' | Measure-Object).Count
Write-Output "Index: ${eidx} entities, ${cidx} concepts, ${sidx} sources"

# Count subdirectory index rows
$eidx2 = (Select-String -Path "wiki/entities/index.md" -Pattern '^\| \[\[entities/' | Measure-Object).Count
$cidx2 = (Select-String -Path "wiki/concepts/index.md" -Pattern '^\| \[\[concepts/' | Measure-Object).Count
$sidx2 = (Select-String -Path "wiki/sources/index.md" -Pattern '^\| \[\[sources/' | Measure-Object).Count
Write-Output "Sub-index: ${eidx2} entities, ${cidx2} concepts, ${sidx2} sources"
```

### Step 4: Identify Missing Entries

Compare actual files against index entries to find missing ones. **Use Python for regex matching** (PowerShell's `Select-String` has trouble with `|` inside character classes like `[^\|\\]`):

```powershell
# Dump actual file names to temp files
Get-ChildItem "wiki/entities/*.md" -Exclude "index.md" | Select-Object -ExpandProperty BaseName | Sort-Object > tmp_actual_entities.txt
Get-ChildItem "wiki/concepts/*.md" -Exclude "index.md" | Select-Object -ExpandProperty BaseName | Sort-Object > tmp_actual_concepts.txt
Get-ChildItem "wiki/sources/*.md" -Exclude "index.md" | Select-Object -ExpandProperty BaseName | Sort-Object > tmp_actual_sources.txt
```

Then run the comparison in Python:

```bash
python -c "
import os, re
for name in ('entities','concepts','sources'):
    actual = set(open(f'tmp_actual_{name}.txt').read().splitlines())
    indexed = set()
    with open('wiki/index.md') as f:
        for line in f:
            m = re.match(r'^\| \[\[' + name + r'/([^|\\\\]+)', line)
            if m: indexed.add(m.group(1))
    missing = actual - indexed
    print(f'{name}: {len(actual)} files, {len(indexed)} indexed')
    if missing:
        for x in sorted(missing): print(f'  MISSING: {x}')
"
```

Clean up temp files afterward: `Remove-Item tmp_actual_*.txt`

### Step 5: Check for Broken Wikilinks

Search for wikilinks that reference non-existent files. Use Python for reliable regex:

```bash
python -c "
import glob, re
# Collect all wikilinks from wiki content
wikilinks = set()
for f in glob.glob('wiki/**/*.md', recursive=True):
    with open(f, encoding='utf-8') as fh:
        for m in re.finditer(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', fh.read()):
            wikilinks.add(m.group(1))

# Check each link target exists
broken = []
for link in sorted(wikilinks):
    target = f'wiki/{link}.md'
    if not glob.glob(target):
        broken.append(link)

if broken:
    for b in broken: print(f'BROKEN: {b}')
else:
    print('No broken wikilinks found')
"
```

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

Append lint results to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] lint | Health check

- **Index consistency**: [summary of findings]
- **Broken links**: [count and details]
- **Orphan pages**: [count]
- **Statistics**: [current vs actual]
- **Actions taken**: [rebuild details if applicable]
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
