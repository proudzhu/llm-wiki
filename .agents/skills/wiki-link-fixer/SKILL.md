---
name: "wiki-link-fixer"
description: "Auto-fix wikilink convention violations in the LLM wiki. Invoke when check_broken_links.py reports missing-prefix, wiki/-prefix, ../-prefix, or log.md informal refs, or when the user asks to fix/clean up wikilinks."
---

# Wiki Link Fixer

Auto-repairs wikilink convention violations reported by `wiki-lint/scripts/check_broken_links.py`. Leaves truly broken links (target page does not exist) untouched — those need manual judgment (create page or rewrite text).

## When to Invoke

Invoke this skill when:
- `check_broken_links.py` reports **Missing category prefix**, **wiki/ prefix**, **Convention violations (../ prefix)**, or **Log.md informal refs**.
- The user says "fix wikilinks", "clean up link conventions", "repair bare slugs", or similar.
- After a bulk ingest/migration that may have introduced convention violations.

## When NOT to Invoke

- **Truly broken links** (target page genuinely doesn't exist) — the script explicitly skips these. Manually decide: create the missing page, or rewrite as plain text.
- **No violations detected** — run `check_broken_links.py` first to confirm there's work to do.
- **Conflicts in `raw/`** — never modify `raw/`.
- **`log.md` informal refs that reference non-existent pages** — these need human review (the original author may have referenced a concept that was never created).

## Categories Handled

| Category | Original | Fixed | Strategy |
|----------|----------|-------|----------|
| Missing category prefix | `[[beamforming]]` | `[[concepts/beamforming\|Beamforming]]` | Search all 6 categories for a matching slug; if found, prepend category |
| `wiki/` prefix | `[[wiki/concepts/foo]]` | `[[concepts/foo]]` | Strip leading `wiki/` |
| `../` prefix | `[[../concepts/foo]]` | `[[concepts/foo]]` | Strip leading `../` |
| Log.md informal refs | `[[Beamforming]]` | `[[concepts/beamforming\|Beamforming]]` | Try case-insensitive slug match across categories; if unique, convert to formal wikilink |

## Categories NOT Handled (Manual)

| Category | Why |
|----------|-----|
| Truly broken | No automatic way to know if page should be created or link rewritten |
| Section-only links (`[[#Section]]`) | These are intra-page refs, not convention violations |
| Embed links (`![[...]]`) | Treated identically to regular wikilinks — same fixer applies |

## Available Scripts

All scripts are in `scripts/`. Run from the project root.

| Script | Purpose |
|--------|---------|
| `scripts/classify_links.py` | Scan wiki/, categorize all violations, output JSON report (no writes) |
| `scripts/fix_links.py` | Apply fixes in-place; supports `--dry-run`, `--category`, `--file` |
| `scripts/verify_fix.py` | Post-fix verification: re-run classification + mkdocs build --strict |

## Workflow

### Step 1: Scan & Classify

```bash
python .agents/skills/wiki-link-fixer/scripts/classify_links.py
```

Outputs a JSON report to stdout (and a summary to stderr). Use `--output report.json` to save the full report. Categories in the report:

```json
{
  "missing_prefix": [{"target": "beamforming", "fix": "concepts/beamforming", "locations": ["wiki/sources/foo.md", ...]}],
  "wiki_prefix":    [{"target": "wiki/concepts/foo", "fix": "concepts/foo", "locations": [...]}],
  "dotdot_prefix":  [{"target": "../concepts/foo", "fix": "concepts/foo", "locations": [...]}],
  "log_informal":   [{"target": "Beamforming", "fix": "concepts/beamforming", "locations": ["wiki/log.md"]}],
  "truly_broken":   [{"target": "missing-page", "locations": [...]}]
}
```

### Step 2: Preview Fixes (Always Do This First)

```bash
python .agents/skills/wiki-link-fixer/scripts/fix_links.py --dry-run
```

Shows per-file diff of what would change, without writing. Output format:

```
=== wiki/sources/foo.md ===
- [[beamforming]] is great
+ [[concepts/beamforming|beamforming]] is great

- [[../concepts/feedback-anc|Feedback ANC]]
+ [[concepts/feedback-anc|Feedback ANC]]

Summary: 268 fixes across 84 files (dry-run)
```

### Step 3: Apply Fixes

```bash
# All categories, all files
python .agents/skills/wiki-link-fixer/scripts/fix_links.py

# Single category only
python .agents/skills/wiki-link-fixer/scripts/fix_links.py --category missing_prefix
python .agents/skills/wiki-link-fixer/scripts/fix_links.py --category wiki_prefix
python .agents/skills/wiki-link-fixer/scripts/fix_links.py --category dotdot_prefix
python .agents/skills/wiki-link-fixer/scripts/fix_links.py --category log_informal

# Single file (all categories)
python .agents/skills/wiki-link-fixer/scripts/fix_links.py --file wiki/log.md
```

The script:
1. Reads each file with `encoding='utf-8'`
2. For each `[[...]]` match, computes the fix (or skips if not in a fixable category)
3. Preserves the existing display text: `[[beamforming|BF]]` → `[[concepts/beamforming|BF]]` (display text unchanged)
4. If display text is absent, no display text is added (matches wiki-lint convention)
5. Writes the file back atomically (temp file + rename) to avoid partial writes
6. Reports per-file fix count and grand total

**Idempotent**: running twice is a no-op (already-canonical links are not matched).

### Step 4: Verify

```bash
# Re-classify — fixable categories should be empty
python .agents/skills/wiki-link-fixer/scripts/classify_links.py

# Confirm truly_broken count unchanged (script never touches these)
# Confirm mkdocs still builds
uv run mkdocs build --strict

# Or use the bundled verifier (does both)
python .agents/skills/wiki-link-fixer/scripts/verify_fix.py
```

### Step 5: Review & Commit

```bash
git diff --stat wiki/
git diff wiki/log.md  # spot-check the log_informal fixes
```

If `--dry-run` showed unexpected changes, `git checkout wiki/` to revert and re-run with `--category` to apply piecemeal.

Commit message convention:

```
lint: auto-fix N wikilink convention violations

- missing_prefix: X
- wiki_prefix: Y
- dotdot_prefix: Z
- log_informal: W

Applied via .agents/skills/wiki-link-fixer/scripts/fix_links.py
Truly broken links (N) left untouched for manual review.
```

## Design Notes

- **Atomic writes**: each file is written to a temp file in the same directory, then `os.replace()` renames it onto the target. No partial state on crash.
- **Encoding**: all reads/writes use `encoding='utf-8'`. On Windows, scripts also call `sys.stdout.reconfigure(encoding='utf-8')`.
- **Display text preservation**: the fixer never modifies what's after `|` or `\|`. Only the link target (before the first `|`/`\|`) is rewritten.
- **Section anchors preserved**: `[[beamforming#Architecture]]` → `[[concepts/beamforming#Architecture]]` (anchor kept).
- **Embed links**: `![[raw/papers/foo/figures/x.png|Figure 1]]` — the `raw/` prefix is already correct; the fixer skips anything starting with `raw/`.
- **Escaped pipes**: handled identically to `check_broken_links.py` — `\|` is the delimiter, not `|`.
- **No heuristics on truly broken**: if a missing-prefix lookup finds zero category matches, the link is left untouched (it would be a truly-broken case).

## Common Issues

### `--dry-run` shows fixes I don't want

Use `--category` to apply only some categories, or `--file` to limit scope. After applying, the next `--dry-run` will show only the remaining categories.

### Log.md informal ref can't be auto-resolved

The `log_informal` category only auto-fixes when the human-readable name (e.g., `Beamforming`) case-insensitively matches a unique slug across all 6 categories. If zero or multiple matches, the link is left as-is for manual review.

### MkDocs build still fails after fix

The fixer only repairs convention violations, not truly broken links. Run `check_broken_links.py` again — if `truly_broken` is non-empty, those need manual resolution (create missing page or rewrite as plain text).

### `fix_links.py` reports 0 fixes but `check_broken_links.py` still shows violations

This happens when violations are in categories the fixer doesn't handle (truly broken). Re-check the classification report — only `missing_prefix`, `wiki_prefix`, `dotdot_prefix`, and `log_informal` are fixable.

## Verification Commands

```bash
# Should report 0 for all fixable categories after a successful run
python .agents/skills/wiki-lint/scripts/check_broken_links.py

# Should exit 0
uv run mkdocs build --strict

# Statistics should be unchanged (link fixes don't add/remove pages)
python .agents/skills/wiki-lint/scripts/check_statistics.py
```

## Important Notes

- **Always run `--dry-run` first** — preview before writing.
- **Never run on `raw/`** — `raw/` is immutable; the script only scans `wiki/**/*.md`.
- **Truly broken links are skipped** — the fixer cannot decide whether to create a missing page or rewrite as text; that's a human call.
- **The fixer is idempotent** — running it on already-canonical links is a no-op.
- **Display text is preserved** — only the link target is rewritten.
- **Commit after verification** — only stage `wiki/` after `mkdocs build --strict` passes.
- **Log informal refs are conservative** — only auto-fixed when the case-insensitive match is unique across all categories.
