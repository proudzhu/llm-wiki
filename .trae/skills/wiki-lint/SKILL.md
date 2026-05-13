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
$entities = (Get-ChildItem "wiki\entities\*.md" -Exclude "index.md").Count
$concepts = (Get-ChildItem "wiki\concepts\*.md" -Exclude "index.md").Count
$sources = (Get-ChildItem "wiki\sources\*.md" -Exclude "index.md").Count
$synthesis = (Get-ChildItem "wiki\synthesis\*.md" -Exclude "index.md").Count
$queries = (Get-ChildItem "wiki\queries\*.md" -Exclude "index.md").Count
$total = $entities + $concepts + $sources + $synthesis + $queries
Write-Output "Actual: $entities entities, $concepts concepts, $sources sources, $synthesis synthesis, $queries queries = $total total"
```

### Step 3: Count Index Rows

Count rows in each index file:

```powershell
# Count index rows
$eidx = (Select-String -Path "wiki\index.md" -Pattern '^\| \[\[entities/' | Measure-Object).Count
$cidx = (Select-String -Path "wiki\index.md" -Pattern '^\| \[\[concepts/' | Measure-Object).Count
$sidx = (Select-String -Path "wiki\index.md" -Pattern '^\| \[\[sources/' | Measure-Object).Count
Write-Output "Index: $eidx entities, $cidx concepts, $sidx sources"

# Count subdirectory index rows
$eidx2 = (Select-String -Path "wiki\entities\index.md" -Pattern '^\| \[\[entities/' | Measure-Object).Count
$cidx2 = (Select-String -Path "wiki\concepts\index.md" -Pattern '^\| \[\[concepts/' | Measure-Object).Count
$sidx2 = (Select-String -Path "wiki\sources\index.md" -Pattern '^\| \[\[sources/' | Measure-Object).Count
Write-Output "Sub-index: $eidx2 entities, $cidx2 concepts, $sidx2 sources"
```

### Step 4: Identify Missing Entries

Compare actual files against index entries to find missing ones:

```powershell
# Get actual file names (without .md extension)
$actual = Get-ChildItem "wiki\entities\*.md" -Exclude "index.md" | ForEach-Object { $_.BaseName }

# Get indexed names from wiki\entities\index.md
$indexed = Select-String -Path "wiki\entities\index.md" -Pattern '^\| \[\[entities/' | ForEach-Object {
    if ($_ -match '\[\[entities/([^\|\\]+)') { $matches[1] }
}

# Find missing
$missing = $actual | Where-Object { $_ -notin $indexed }
Write-Output "Missing from entities index: $($missing -join ', ')"
```

Repeat for concepts and sources.

### Step 5: Check for Broken Wikilinks

Search for wikilinks that reference non-existent files:

```powershell
# Extract all wikilinks from wiki content
$links = Select-String -Path "wiki\**\*.md" -Pattern '\[\[([^\]|]+)(?:\|[^\]]+)?\]\]' -AllMatches | ForEach-Object {
    $_.Matches | ForEach-Object { $_.Groups[1].Value }
} | Sort-Object -Unique

# Check each link target exists
foreach ($link in $links) {
    $target = "wiki\$link.md"
    if (-not (Test-Path $target)) {
        Write-Output "BROKEN: $link -> $target"
    }
}
```

### Step 6: Check for Orphan Pages

Find pages with no inbound wikilinks:

```powershell
# Get all page names
$pages = Get-ChildItem "wiki\entities\*.md" -Exclude "index.md" | ForEach-Object { $_.BaseName }

# Get all wikilink targets
$allLinks = Select-String -Path "wiki\**\*.md" -Pattern '\[\[([^\]|]+)(?:\|[^\]]+)?\]\]' -AllMatches | ForEach-Object {
    $_.Matches | ForEach-Object { $_.Groups[1].Value }
}

# Find orphans (pages never linked to)
$orphans = $pages | Where-Object { $_ -notin $allLinks }
Write-Output "Orphan pages: $($orphans.Count)"
```

Note: Many pages are expected to be linked only from index files, not from other content pages.

### Step 7: Check Statistics Consistency

Read the Statistics section in `wiki/index.md` and verify counts match actual files:

```powershell
# Read statistics from wiki/index.md
$stats = Select-String -Path "wiki\index.md" -Pattern '^\- \*\*(Entities|Concepts|Sources|Synthesis|Queries|Total pages)\*\*: (\d+)'
```

### Step 8: Rebuild Indexes (if drift detected)

If index drift is found, use the bundled `rebuild_index.py` script:

```bash
python .trae/skills/wiki-lint/rebuild_index.py > missing_entries.txt 2>&1
```

The script:
1. Reads existing index entries from `wiki/index.md` using regex (handles escaped `\|` in wikilinks)
2. Compares against actual files in `wiki/entities/`, `wiki/concepts/`, `wiki/sources/`
3. Outputs missing entries in markdown table format with auto-generated summaries
4. Preserves existing high-quality summaries (only generates new ones for truly missing entries)

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

After any index rebuild, verify counts match:

```powershell
$eidx = (Select-String -Path "wiki\entities\index.md" -Pattern '^\| \[\[entities/' | Measure-Object).Count
$eact = (Get-ChildItem "wiki\entities\*.md" -Exclude "index.md").Count
Write-Output "Entities index: $eidx rows, actual: $eact files, diff: $($eidx - $eact)"
```

All diffs should be 0.
