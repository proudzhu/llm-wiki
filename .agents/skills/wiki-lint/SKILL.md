---
name: "wiki-lint"
description: "Performs comprehensive health check of the LLM wiki knowledge base. Invoke when user asks to lint, health check, or verify wiki consistency."
---

# Wiki Lint Skill

This skill performs a comprehensive health check of the LLM wiki knowledge base, checking for index drift, broken links, orphan pages, and data gaps.

## Available Scripts

All Python scripts are in the `scripts/` subdirectory. Run from the project root using `python .agents/skills/wiki-lint/scripts/<script>.py`.

| Script | Purpose |
|--------|---------|
| `scripts/count_files.py` | Count actual `.md` files per category directory |
| `scripts/count_index_rows.py` | Count rows in main index and subdirectory indexes |
| `scripts/check_index_drift.py` | Check missing, phantom, duplicate entries |
| `scripts/check_broken_links.py` | Categorized broken wikilink analysis |
| `scripts/check_orphans.py` | Find pages with zero inbound references |
| `scripts/check_statistics.py` | Verify stated stats vs actual file counts |
| `scripts/verify_index.py` | Post-rebuild diff=0 verification |
| `scripts/rebuild_index.py` | Auto-generate missing index rows |

## When to Invoke

- User asks to "lint" the wiki
- User requests a health check or consistency verification
- After bulk operations (ingests, migrations) to verify integrity

## Lint Workflow

### Step 1: Understand Lint Requirements

Read `AGENTS.md` (project root) to understand the lint workflow requirements (contradictions, stale claims, orphan pages, missing pages, cross-references, data gaps).

### Step 2: Count Actual Files

Count actual `.md` files in each category directory (excluding `index.md`):

```bash
python .agents/skills/wiki-lint/scripts/count_files.py
```

**Expected output:**
```
Actual: 258 entities, 224 concepts, 102 sources, 19 synthesis, 7 queries = 610 total
```

### Step 3: Count Index Rows

Count rows in the main index and each subdirectory index:

```bash
python .agents/skills/wiki-lint/scripts/count_index_rows.py
```

This counts lines like `| [[entities/some-page|...` in `wiki/index.md` and all `| [[` lines in subdirectory indexes. If counts match Step 2, there is no index drift.

**Expected output:**
```
Main index entities: 258
Main index concepts: 224
...
Sub-index entities: 258
Sub-index concepts: 224
...
```

### Step 4: Identify Missing & Phantom Entries

Compare actual files against index entries to find **missing** (file exists but not in index), **phantom** (index row with no file), and **duplicate** entries:

```bash
python .agents/skills/wiki-lint/scripts/check_index_drift.py
```

The script handles escaped pipes (`\|`) in markdown tables. The slug capture pattern `[^|\\\]]+` excludes pipe, backslash, and closing bracket so that `\|` doesn't append a trailing backslash to the slug name.

### Step 5: Check for Broken Wikilinks

Scans all wiki content for wikilinks and categorizes them. **Important considerations:**

1. **Escaped pipes** (`\|`) in markdown tables: the `\|` sequence separates the link target from display text inside `[[...]]`. Treat `\|` as a delimiter.
2. **Section anchors** (`#Heading`): stripped before existence checking.
3. **`../` prefixes**: violate the vault-absolute convention (per `AGENTS.md`) but resolve in MkDocs. Reported separately as convention violations.
4. **`wiki/` prefixes**: e.g., `[[wiki/concepts/beamforming]]` -- the target resolves to `wiki/wiki/concepts/beamforming.md` which doesn't exist. Correct form is `[[concepts/beamforming]]`.
5. **Missing category prefix**: e.g., `[[beamforming]]` instead of `[[concepts/beamforming]]`. The target `wiki/beamforming.md` doesn't exist, but `wiki/concepts/beamforming.md` does.

```bash
python .agents/skills/wiki-lint/scripts/check_broken_links.py
```

**Note:** Wikilinks using `../` prefixes are convention violations but not broken links. Links missing category prefix are the most common issue -- the script automatically detects the correct category. Links using `wiki/` prefix should be fixed by removing the `wiki/` prefix.

### Step 6: Check for Orphan Pages

Find pages with **zero inbound references** from any wiki content. Checks both wikilinks (`[[target]]`) and markdown links (`[text](../target.md)`), with nested-bracket support in link text:

```bash
python .agents/skills/wiki-lint/scripts/check_orphans.py
```

This covers wikilinks and markdown links, normalizes `../` and `wiki/` prefixes to avoid false positives. A page counted as "orphaned" genuinely has zero inbound references from any wiki page, index, or log entry.

### Step 7: Check Statistics Consistency

Read the Statistics section in `wiki/index.md` and verify stated counts match actual files:

```bash
python .agents/skills/wiki-lint/scripts/check_statistics.py
```

This parses the `## Statistics` section, extracts stated counts, and compares each category (including Total pages) against the actual file counts from disk.

### Step 8: Rebuild Indexes (if drift detected)

If index drift is found, use the bundled `rebuild_index.py` script:

```bash
python .agents/skills/wiki-lint/scripts/rebuild_index.py
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
4. Add missing entries to all index files: `wiki/index.md`, `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md`
5. Remove any duplicates found
6. Update statistics section

### Step 9: Log Results

Append lint results to `wiki/log.md`. Include the `---` separator before the entry:

```markdown
---

## [YYYY-MM-DD] lint | Health check

- **Index consistency**: [summary of findings -- which categories match and which don't]
- **Broken links**: [count per category: truly broken, missing-prefix, wiki/-prefix, ../ violations, log.md refs]
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
Markdown tables use `\|` for display text containing pipes. Regex patterns must handle both escaped and unescaped pipes. The `\|` sequence splits the target from display text. Use `[^|\\\]]+` to capture slug characters excluding pipe, backslash, and closing bracket.

### Unicode Encoding on Windows
Python's default 'gbk' codec can't handle special characters on Windows. All scripts use `sys.stdout.reconfigure(encoding='utf-8')` and `encoding='utf-8'` in `open()` calls.

### Missing Category Prefix in Wikilinks
Content pages frequently use bare slugs (e.g., `[[beamforming]]`) instead of category-qualified paths (e.g., `[[concepts/beamforming]]`). Fix by prepending the correct category.

### `wiki/` Prefix in Wikilinks
Some pages use `[[wiki/concepts/foo]]` instead of the correct `[[concepts/foo]]`. The `wiki/` prefix duplicates the root directory name. Fix by removing the `wiki/` prefix.

### `../` Relative Prefixes
Using `[[../concepts/foo]]` instead of `[[concepts/foo]]` violates the vault-absolute convention (per `AGENTS.md`). While these resolve in MkDocs builds, they should be fixed to use the standard `[[category/slug]]` form.

## Verification Commands

After any index rebuild, verify all diffs are 0:

```bash
python .agents/skills/wiki-lint/scripts/verify_index.py
```

Quick PowerShell check:

```powershell
$eidx = (Select-String -Path "wiki/entities/index.md" -Pattern '^\| \[\[entities/' | Measure-Object).Count
$eact = (Get-ChildItem "wiki/entities/*.md" -Exclude "index.md").Count
$diff = $eidx - $eact
if ($diff -eq 0) { Write-Output "OK Entities: ${eidx} = ${eact}" }
else { Write-Output "MISMATCH Entities: ${eidx} indexed vs ${eact} actual (diff=${diff})" }
```
