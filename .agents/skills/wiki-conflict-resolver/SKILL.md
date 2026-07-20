---
name: "wiki-conflict-resolver"
description: "Resolves Git rebase conflicts in the LLM wiki knowledge base. Invoke when a `git rebase` or `git merge` leaves conflict markers in wiki/index.md, wiki/{entities,concepts,sources,synthesis,queries}/index.md, or wiki/log.md."
---

# Wiki Conflict Resolver

Automates resolution of Git rebase conflicts in wiki index and log files. The canonical conventions (chronological log order, deduped index rows by slug, recalculation of statistics) are encoded in Python scripts so resolution is deterministic and reproducible.

## When to Invoke

Invoke this skill when:
- A `git rebase` or `git merge` has produced conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) in any wiki markdown file.
- The user says "fix rebase conflict", "resolve merge conflict", or similar.
- `git status` shows "Unmerged paths" under `wiki/index.md`, `wiki/*/index.md`, or `wiki/log.md`.

## When NOT to Invoke

- **Conflicts in non-wiki files** (source code under `.agents/skills/`, `scripts/`, `schema/`, etc.) — these need manual review, not this skill.
- **Conflicts in `raw/` source documents** — `raw/` is immutable and should never be touched.
- **No conflict markers present** — verify first with `detect_conflicts.py`.
- **Logic conflicts in wiki page bodies** (e.g., two sides rewrote a paragraph differently) — this skill only handles structured index/log conflicts.

## Conflict Resolution Strategy

The strategy follows the wiki conventions in `AGENTS.md`:

### 1. Log file (`wiki/log.md`)
- **Convention**: append-only, newest entries at the END, format `## [YYYY-MM-DD] op | Title`.
- **Resolution**: strip conflict markers, parse both sides into entries, dedupe by `(date, op, title)` (keeping the longer body on ties), sort chronologically (oldest first), re-emit with canonical header.

### 2. Index files (`wiki/index.md`, `wiki/*/index.md`)
- **Convention**: table rows like `| [[category/slug\|Display]] | summary | date |`, one row per page.
- **Resolution**: for each conflict block, extract all table rows from both sides, dedupe by `(category, slug)` keeping first-seen order (ours side first, theirs-only rows appended), replace conflict block with merged rows. Non-row content (headers, separators) is preserved.

### 3. Statistics (`## Statistics` in `wiki/index.md`)
- **Convention**: counts of pages in each category.
- **Resolution**: recount actual `.md` files per category directory (excluding `index.md`), rewrite the `## Statistics` section, set `Last updated` to today.

## Available Scripts

All Python scripts are in `scripts/`. Run from the project root.

| Script | Step | Purpose |
|--------|------|---------|
| `scripts/detect_conflicts.py` | 1 | Scan `wiki/` for conflict markers; list affected files and line ranges |
| `scripts/resolve_log_conflict.py` | 2 | Resolve conflicts in `wiki/log.md` (merge + dedupe + chronological sort) |
| `scripts/resolve_index_conflict.py` | 3 | Resolve conflicts in `wiki/index.md` and all subdirectory indexes (dedupe by slug) |
| `scripts/finalize.py` | 4 | Scan for residual markers; recount statistics; update `## Statistics` in `wiki/index.md` |
| `scripts/resolve_all.py` | all | End-to-end orchestration: detect → resolve log → resolve indexes → finalize |

## Workflow

### Quick Path: Resolve Everything

If you want the full pipeline to run automatically:

```bash
uv run python .agents/skills/wiki-conflict-resolver/scripts/resolve_all.py
```

This runs all four steps in sequence. To preview without writing, add `--dry-run`:

```bash
uv run python .agents/skills/wiki-conflict-resolver/scripts/resolve_all.py --dry-run
```

### Step-by-Step Path

Use this when you need fine-grained control or want to inspect intermediate state.

#### Step 1: Detect Conflicts

```bash
uv run python .agents/skills/wiki-conflict-resolver/scripts/detect_conflicts.py
```

Output lists each affected file with line ranges of conflict blocks. Use `--check-only` for scripting (exits 1 if any conflicts found):

```bash
uv run python .agents/skills/wiki-conflict-resolver/scripts/detect_conflicts.py --check-only
```

#### Step 2: Resolve `wiki/log.md`

```bash
uv run python .agents/skills/wiki-conflict-resolver/scripts/resolve_log_conflict.py
```

Strategy: strip markers → parse entries → dedupe by `(date, op, title)` → sort chronologically → rewrite file. Use `--dry-run` to preview:

```bash
uv run python .agents/skills/wiki-conflict-resolver/scripts/resolve_log_conflict.py --dry-run
```

If the log has no conflict markers, the script exits 0 without modifying anything.

#### Step 3: Resolve Index Files

```bash
# Resolve all default targets (wiki/index.md + all subdirectory indexes)
uv run python .agents/skills/wiki-conflict-resolver/scripts/resolve_index_conflict.py --all

# Or resolve a single file
uv run python .agents/skills/wiki-conflict-resolver/scripts/resolve_index_conflict.py --path wiki/index.md
```

Strategy: for each conflict block, extract `| [[category/slug\|...]] |` rows from both sides, dedupe by `(category, slug)`, preserve first-seen order, replace conflict block with merged rows. Non-row lines (headers, separators, statistics) are left untouched.

Use `--dry-run` to preview the first 50 lines of each resolved file.

#### Step 4: Finalize (Statistics + Verification)

```bash
uv run python .agents/skills/wiki-conflict-resolver/scripts/finalize.py
```

This script:
1. Scans all `wiki/` markdown files for residual conflict markers (aborts if any are found).
2. Recounts `.md` files per category directory (excluding `index.md`).
3. Rewrites the `## Statistics` section in `wiki/index.md` with current counts and today's date.

Use `--dry-run` to preview the new `## Statistics` block without writing.

### Manual Review (Optional)

After running the scripts, review changes before staging:

```bash
git diff wiki/index.md wiki/log.md wiki/entities/index.md wiki/concepts/index.md wiki/sources/index.md
```

If the merge introduced genuinely conflicting content in a page body (e.g., two sides rewrote a paragraph differently), resolve that manually — the scripts only handle structured index/log conflicts.

### Complete the Rebase

Once all conflicts are resolved and finalized:

```powershell
# PowerShell syntax (user's environment)
git add wiki/
$env:GIT_EDITOR='true'; git rebase --continue
```

Setting `GIT_EDITOR='true'` bypasses the commit-message editor — the existing commit message is reused. Use `git rebase --skip` only if the commit's changes were entirely superseded by the merge.

### Build Verification

After the rebase completes, verify the wiki still builds:

```bash
uv run mkdocs build --strict
```

A clean build exits 0 with `INFO - Documentation built in N seconds`. If warnings appear (broken links, missing pages), they indicate convention violations that need manual fixing — see the `wiki-lint` skill for health-check tooling.

## Common Issues

### Conflict in a Wiki Page Body (Not Index/Log)

The scripts do **not** resolve conflicts in regular wiki page bodies (`wiki/sources/*.md`, `wiki/concepts/*.md`, etc.). These require manual review — open the file, read both sides, and choose the better content (or merge manually). Run `detect_conflicts.py` to find them:

```bash
uv run python .agents/skills/wiki-conflict-resolver/scripts/detect_conflicts.py
```

Any file listed that is **not** `wiki/index.md`, `wiki/*/index.md`, or `wiki/log.md` needs manual resolution.

### Nested Conflict Markers

If `detect_conflicts.py` reports `[nested-start]` or `[unterminated]` status, the conflict markers are malformed (often due to a previous botched merge). Resolve manually by inspecting the file and ensuring markers are properly paired.

### Rebase Editor Blocks Progress

On Windows PowerShell, set `GIT_EDITOR` inline to skip the editor prompt:

```powershell
$env:GIT_EDITOR='true'; git rebase --continue
```

### Unmerged Paths Error

If `git rebase --continue` fails with "you need to resolve your current index first", there are still unmerged paths. Check with `git status` and re-run the detection script:

```bash
uv run python .agents/skills/wiki-conflict-resolver/scripts/detect_conflicts.py
```

### Statistics Section Not Updated

If `finalize.py` reports updated statistics but `git diff` doesn't show changes, the file may have been staged before the script ran. Re-run finalize after `git reset` (unstage) or run `update_indexes.py stats` from the `paper-reader` skill as a fallback.

## Verification Commands

After resolution, verify the wiki is consistent:

```bash
# No residual conflict markers anywhere in wiki/
uv run python .agents/skills/wiki-conflict-resolver/scripts/detect_conflicts.py --check-only

# Index drift check (no missing/phantom/duplicate entries)
uv run python .agents/skills/wiki-lint/scripts/check_index_drift.py

# Statistics consistency
uv run python .agents/skills/wiki-lint/scripts/check_statistics.py

# MkDocs build (must exit 0)
uv run mkdocs build --strict
```

## Important Notes

- **Never run on `raw/`** — `raw/` is immutable; conflicts there indicate a process error and require manual investigation.
- **Always run `detect_conflicts.py` first** — confirms which files actually have conflicts before running resolvers.
- **Use `--dry-run` liberally** — preview changes before writing, especially for the log file where order matters.
- **The scripts are idempotent** — running them on a file without conflict markers is a no-op.
- **Commit after verification** — only stage and commit after `detect_conflicts.py` reports no conflicts and `mkdocs build --strict` passes.
- **Subdirectory indexes are updated too** — `resolve_index_conflict.py --all` covers `wiki/{entities,concepts,sources,synthesis,queries}/index.md` as well as the main index.
- **Log entries are deduped conservatively** — by `(date, op, title)`; if both sides added the same paper's ingest entry, only one survives (the longer-bodied one).
- **Index rows are deduped by slug** — if both sides added the same entity, only one row survives (first-seen order preserved).
