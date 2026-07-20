---
name: "paper-reader"
description: "Full paper ingestion workflow from Zotero to wiki: search, extract, analyze, and create wiki pages. Invoke when user asks to ingest, re-ingest, or read a paper from Zotero."
---

# Paper Reader

End-to-end workflow for ingesting academic papers from Zotero into the LLM Wiki knowledge base.

## When to Invoke

- "ingest paper X from Zotero"
- "re-ingest paper X from Zotero"
- "read paper X from Zotero"
- Add a paper from the user's Zotero library to the wiki

## When NOT to Invoke

- **Paper is already in the wiki and up-to-date** — Check `wiki/sources/` and `wiki/log.md` first. Quick check:
  ```bash
  Select-String -Path wiki\log.md -Pattern "author|short title"
  Select-String -Path wiki\sources\*.md -Pattern "Author Year" -List
  ```
- **User just wants a quick summary** — Read the existing source page or use the abstract directly. Full ingestion is only for deep analysis.
- **Zotero is not running or unreachable** — Verify first: `curl -s http://localhost:23119/connector/ping`.
- **Paper is not in Zotero** — This skill only ingests from Zotero. For external papers (e.g., direct arXiv URL), skip Zotero steps and use extraction scripts directly.
- **Source is not a PDF/academic paper** — Web pages, blog posts, and informal documents use the standard raw article workflow instead.
- **Re-ingestion of an identical version** — Only re-ingest if the source PDF was updated (e.g., camera-ready replaces preprint) or the existing wiki page is significantly incomplete.

## Checking Existing Pages (Windows Glob Caveat)

Several steps require checking whether a page already exists. **On Windows, Glob brace expansion (`{a,b,c}.md`) does not work** and returns "No file found" even when files exist. Use one of these patterns instead:

- **Grep with alternation** (preferred for batch checks): `Grep` with pattern `seidel|fingscheidt|mowlaee`, path `wiki/entities`, `-i true` — returns all matching files in one call.
- **Multiple parallel Glob calls**: one Glob per slug (no braces), e.g. `wiki/entities/ernst-seidel.md`.
- **LS the directory**: `LS wiki/entities` returns the full file list; scan visually for the target slugs.

Always use **forward slashes** in Glob patterns and prefer **relative paths from project root** over absolute Windows paths.

## Prerequisites

- Zotero running with "Allow other applications" enabled
- `mineru-open-api` CLI (`npm install -g mineru-open-api`) — verify token: `mineru-open-api auth --show`
- `defuddle` CLI (`npm install -g defuddle`) for arXiv HTML extraction
- All scripts run from the **project root**

## Available Scripts

Mechanical steps are automated as Python scripts in `scripts/`. Run them from the project root.

| Script | Step | Purpose |
|--------|------|---------|
| `scripts/zotero_fetch.py` | 1-2 | Search Zotero + fetch metadata + find PDF attachment key |
| `scripts/prepare_paper.py` | 3a | Create `raw/papers/{slug}/`, copy PDF (handles Unicode), verify `%PDF-` header |
| `scripts/extract_arxiv_html.py` | 3b | arXiv HTML extraction via Defuddle + download figures + fix links + delete PDF |
| `scripts/extract_mineru.py` | 3c | MinerU extraction + rename `images/`→`figures/` + update refs + delete PDF |
| `scripts/extract_pdftotext.py` | 3d | pdftotext fallback (plain text, no images) + delete PDF |
| `scripts/update_indexes.py` | 10 | Add rows (`add`), batch-add from YAML manifest (`batch --manifest`), or recount statistics (`stats`) |
| `scripts/append_log.py` | 11 | Append formatted entry to `wiki/log.md` |
| `scripts/build_check.py` | 12 | Run `mkdocs build --strict` (tries `uv run` then `python -m`) |
| `scripts/commit_ingest.py` | 13 | Stage ingest files + verify no `paper.pdf` + commit |

## References

Load these on demand when the relevant situation arises. Do not read them up front.

| Reference | When to load |
|-----------|--------------|
| [`references/page-templates.md`](references/page-templates.md) | Step 5 (source pages), Step 6 (entity pages), Step 7 (concept pages) — full templates and the concept-page threshold rules |
| [`references/edge-cases.md`](references/edge-cases.md) | Step 4 — graphical-only results, citation discrepancies, loose classifications in review papers, cross-references to already-ingested papers |
| [`references/review-papers.md`](references/review-papers.md) | Step 4-7 — when the paper is a review/survey (different analysis targets and required sections) |
| [`references/pitfalls.md`](references/pitfalls.md) | When something unexpected happens, or skim before starting an ingest for known gotchas |

## Workflow

### Step 1-2: Search Zotero & Fetch Metadata

```bash
python .agents/skills/paper-reader/scripts/zotero_fetch.py search "SEARCH_TERMS"
python .agents/skills/paper-reader/scripts/zotero_fetch.py metadata ZOTERO_KEY
```

Note the **Zotero key** (e.g., `8ZWV2E4T`) and **PDF attachment key** (e.g., `5H7GWRF3`).

If the paper has an arXiv ID but is not in Zotero, note the arXiv ID and proceed to Step 3b directly (skip `prepare_paper.py`).

**Multiple attachments**: Zotero items often have both an HTML attachment and a PDF attachment (e.g., IEEE Xplore saves both). Always pick the **PDF attachment** (`application/pdf`) for `prepare_paper.py` — HTML attachments from publisher sites are typically cluttered with navigation/ads and not suitable for extraction. The `zotero_fetch.py metadata` output lists all attachments with their MIME types; choose the one whose type is `application/pdf`.

### Step 3: Extract Paper Content

#### 3a. Prepare Directory & Copy PDF

```bash
python .agents/skills/paper-reader/scripts/prepare_paper.py --slug SLUG --pdf-key PDF_KEY
```

Slug format: `author-year-short-title` (lowercase, hyphenated). The script handles non-ASCII filenames and verifies the `%PDF-` header.

#### 3b. arXiv HTML (Preferred for arXiv Papers)

If the paper has an arXiv ID, **always prefer the HTML version** — better text quality than PDF extraction:

```bash
python .agents/skills/paper-reader/scripts/extract_arxiv_html.py --arxiv-id ARXIV_ID --slug SLUG
```

The script auto-creates `raw/papers/{slug}/` (so arXiv-only papers can skip `prepare_paper.py`), checks if HTML exists (falls back to MinerU with exit code 2 if 404), verifies `defuddle` is on PATH (falls back to MinerU with exit code 2 if missing), runs Defuddle, downloads figures, and replaces remote image links with local embed wikilinks.

If the script exits with code 2 (HTML 404 or defuddle missing), proceed to 3c (MinerU) using the PDF you'll need to fetch first via `prepare_paper.py --slug SLUG --pdf-key PDF_KEY`.

#### 3c. MinerU (For Non-arXiv Papers or arXiv Fallback)

```bash
python .agents/skills/paper-reader/scripts/extract_mineru.py --slug SLUG [--language en --model vlm --timeout 600]
```

Parameters: `--model vlm` (VLM layout analysis, default), `--model pipeline` (zero-hallucination). Token required: `mineru-open-api auth`.

Post-processing (automatic): `images/` → `figures/`, references updated in `full-text.md`.

Verify extraction quality: Read first 200 lines and last 100 lines of `full-text.md`. MinerU VLM may produce mermaid code blocks for diagrams — these are normal.

#### 3d. Fallback: pdftotext (If MinerU Fails)

```bash
python .agents/skills/paper-reader/scripts/extract_pdftotext.py --slug SLUG
```

Produces `.txt` without images. Font mismatch warnings are normal.

#### 3e. Extract Images (Optional — before deleting PDF)

If the user explicitly requests standalone image extraction (beyond what MinerU/arXiv HTML provides), and the PDF still exists:

```bash
pdfimages -all "raw/papers/{slug}/paper.pdf" "raw/papers/{slug}/img"
```

Requires `poppler-utils`. Run this **before** any extraction script that deletes the PDF.

**Note**: MinerU figures are hash-named JPEGs. When referencing them, list the `figures/` directory to discover actual filenames — the filenames are deterministic from the PDF content.

### Step 4: Read and Analyze the Full Paper Content

Read the extracted text in chunks (head 200 + tail 100 + targeted range reads for methodology/experiments/results). Extract:

- **Core problem and motivation**
- **Key technical contributions** (numbered)
- **Methodology** (architecture, algorithms, loss functions, equations)
- **Experimental setup** (datasets, metrics, hyperparameters)
- **Results** (quantitative tables, key findings)
- **Important distinctions** (e.g., how this differs from related work)
- **Future work directions**
- **Key concepts** that warrant their own wiki pages
- **Authors** who warrant entity pages

**If the paper is a review/survey**, load [`references/review-papers.md`](references/review-papers.md) for different analysis targets and required source-page sections.

**If you encounter any of these situations**, load [`references/edge-cases.md`](references/edge-cases.md):
- Results reported only in figures (do not transcribe numbers from charts)
- Self-reported numbers differ from how a later, already-ingested paper cites them
- A review paper groups cited methods under labels that don't fit
- The paper cites or discusses a paper already in the wiki (add bidirectional links)

### Step 5: Create/Update Source Page

Create `wiki/sources/{slug}.md`. Load [`references/page-templates.md`](references/page-templates.md) for the full frontmatter, required sections, and figure-usage criteria. Key points: H1 is `Author1, Author2 & Author3 Year: Short Title`; required sections are Summary / Problem Formulation / Methodology / Experimental Setup / Results / Key Contributions / Related Concepts / Related Synthesis; max 3 figures, placed immediately after the section they illustrate, with `LS figures/` first to discover actual filenames.

For re-ingestion: overwrite the existing source page with updated comprehensive content.

### Step 6: Create or Update Entity Pages

For each author not already in `wiki/entities/`, create a new page. For existing authors, make **append-only** edits (update `updated:`, append a bullet to `## Key Contributions`, do not touch `created:` or rewrite existing bullets). Load [`references/page-templates.md`](references/page-templates.md) for the full template and the append-only update rules.

**Check first**: use Glob/Grep (see "Checking Existing Pages" above) to see if an entity already exists.

### Step 7: Create Missing Concept Pages

For each key technical concept referenced via wikilinks in the source page but lacking a dedicated page, create `wiki/concepts/{concept-name}.md`. Load [`references/page-templates.md`](references/page-templates.md) for the template and the **concept-page threshold** — only create a page if the paper introduces, formulates distinctly, or centrally relies on the concept. Do **not** create pages for generic ML/DL primitives (Adam, ReLU, dropout, gradient clipping) — link them as plain text instead.

**Check first**: use Glob/Grep to see if a concept already exists. If so, update it.

### Step 8: Update Existing Concept Pages

For concepts that already have pages:

- Add the paper to `sources:` in frontmatter (if applicable)
- Update `updated:` date
- Add new sections or expand existing ones with findings from this paper
- Add cross-references (wikilinks) to new concepts/entities
- Add the paper to `## Related Sources` section

### Step 9: Update Synthesis Pages

Check if any existing synthesis pages should reference this paper. Update (or create) a synthesis page if **any** of these triggers fire:

1. **New data point on an existing frontier** — a new (params, MACs/s, quality) tuple or row in an existing comparison table.
2. **Fills a gap in an existing comparison** — covers a configuration (latency, sample rate, model size) flagged as missing.
3. **Crosses multiple synthesis pages** — relevant to more than one existing synthesis; add to each.
4. **Refutes or refines an existing synthesis claim** — findings contradict or sharpen a claim; update the claim and cite the paper.
5. **Introduces a new axis of comparison** — proposes a new evaluation axis that should be added to an existing comparison table.

**When NOT to update**: the paper is a narrow incremental result on a single existing system, does not change any cross-source comparison, and does not introduce a new axis. Skip — synthesis pages are for *synthesis*, not for listing every paper.

**When in doubt**: prefer *not* updating. A thin synthesis addition adds clutter; a substantive one (1–2 sentences + a table row) is valuable. If you cannot write at least one substantive sentence about what the paper *contributes to the cross-source analysis*, skip.

### Step 10: Update Indexes

For each new page created, add a row to the indexes. For ingests creating **multiple pages** (typical: 1 source + 2–4 entities + 5–15 concepts), **prefer the `batch` subcommand** with a YAML manifest.

#### Option A: Batch (preferred for multi-page ingests)

Write a YAML manifest to a temp file (e.g., `.tmp_ingest_manifest.yaml`):

```yaml
entries:
  - category: sources
    slug: author-year-short-title
    display: "Author Year: Short Title"
    summary: "One-line summary"
    date: YYYY-MM-DD
  - category: entities
    slug: firstname-lastname
    display: "Author Name"
    summary: "Affiliation — role in paper"
    date: YYYY-MM-DD
  - category: concepts
    slug: concept-name
    display: "Concept Name"
    summary: "One-line summary"
    date: YYYY-MM-DD
```

Then run:

```bash
python .agents/skills/paper-reader/scripts/update_indexes.py batch \
    --manifest .tmp_ingest_manifest.yaml --stats
```

The `--stats` flag runs the statistics recount automatically. Delete the temp manifest afterward.

#### Option B: Single-entry `add` (one-off additions or re-ingests)

```bash
python .agents/skills/paper-reader/scripts/update_indexes.py add \
    --category sources --slug SLUG --display "Title" --summary "..." --date YYYY-MM-DD
```

If you used `add`, **always** run `stats` afterward:

```bash
python .agents/skills/paper-reader/scripts/update_indexes.py stats
```

### Step 11: Update Log

```bash
python .agents/skills/paper-reader/scripts/append_log.py --op ingest \
    --title "Paper Title (Author Year)" --file .tmp_log_entry.md
```

Entry body format (write to temp file):

```markdown
- **Source**: `raw/papers/{slug}/full-text.md` (Zotero: KEY)
- **Authors**: Author1, Author2, Author3
- **Published**: Venue Year, pp. XXX–XXX
- **DOI**: 10.xxxx/xxxxx
- **Summary**: One-line summary
- **Pages created**:
  - `raw/papers/{slug}/full-text.md` — extracted text from Zotero PDF
  - `wiki/sources/{slug}.md`
  - `wiki/entities/author1.md`
  - `wiki/concepts/concept1.md`
- **Pages updated**:
  - `wiki/entities/existing-author.md` — added this paper
  - `wiki/concepts/existing-concept.md` — added cross-refs and source link
  - `wiki/index.md` — added N entities, N concepts, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
```

For re-ingestion, use `ingest (re)` as the operation in `--title`.

### Step 12: Build Verification (MkDocs)

```bash
python .agents/skills/paper-reader/scripts/build_check.py
```

If the build fails or exits with warnings (broken links, missing pages), resolve them before proceeding. The page-creation rules in AGENTS.md *Link Conventions* are designed so this step should always pass; if it does not, the offending page violated a convention and must be fixed.

Note: `mkdocs build --strict` may emit `INFO - Doc file 'log.md' contains an unrecognized relative link` for pre-existing issues in `log.md`. These do not fail the build (exit 0) and are not caused by your ingest; do not block on them.

### Step 13: Commit Changes

```bash
python .agents/skills/paper-reader/scripts/commit_ingest.py \
    --slug SLUG \
    --message "ingest: Short Title (Author Year)" \
    --entities author1 author2 \
    --concepts concept1 concept2 \
    --synthesis synth1
```

The script stages `raw/papers/{slug}/`, `wiki/sources/{slug}.md`, all index files, `wiki/log.md`, and the specified entity/concept/synthesis pages. It verifies no `paper.pdf` is staged and commits.

**Auto-staging of unlisted `wiki/` modifications**: the script also auto-stages any other modified or untracked file under `wiki/` that you did not list explicitly. This catches Step 8 edits to **existing** concept/entity pages (bidirectional cross-references) that would otherwise be silently dropped from the commit. The auto-staged files are printed before the commit so you can verify them. Pass `--strict` to disable this behavior (e.g., for a partial ingest under review).

Use `--no-verify` only if the pre-commit hook has environment issues unrelated to your changes.

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Source slug | `author-year-short-title` | `tan-2018-convolutional-recurrent-network-speech-enhancement` |
| Entity slug | `firstname-lastname` | `ke-tan` |
| Concept slug | `descriptive-hyphenated` | `convolutional-recurrent-network` |

## Important Notes

- **Never modify** files in `raw/` after creation (immutability rule) — **exception**: replacing remote image URLs with local paths in `full-text.md` is allowed.
- **Always check** if a page already exists before creating (use Glob/Grep).
- **Always read** existing pages before updating them.
- **Wikilinks** use vault-absolute paths: `[[entities/name|Display Name]]` from any page. Never use `../` prefixes inside wikilinks. Never link to a page that does not exist — if you reference `[[concepts/some-new-concept]]`, create that page or leave as plain text.
- **Cross-references** are bidirectional — when adding a link from A to B, also add from B to A.
- **Frontmatter dates**: Use today's date for `created`, update `updated` on modified pages.
- **Avoid `\bm{}` in LaTeX math**: MathJax does not load the `bm` package. Use `\mathbf{x}` (bold upright) or `\boldsymbol{x}` (bold italic) instead.
- **Delete the PDF** after extraction — extraction scripts handle this automatically; never commit `paper.pdf`.
- **Commit after build verification** — use `--no-verify` only if the pre-commit hook has environment issues unrelated to your changes.
- **Sequence edits to the same file** — when updating an existing page with multiple changes (e.g., frontmatter date + new section + Related Concepts/Sources extension), issue the Edit calls **sequentially, one tool call per message**, not in parallel. Parallel Edits to the same file silently race against each other and only one of them persists, leading to missing sections and follow-up "complete pending edits" commits. Parallel Edits to **different** files are fine and encouraged.
- **Verify each Edit actually persisted** — after editing an existing page (especially in a multi-edit batch), re-Read the relevant section of the file before assuming the edit landed. If an edit was silently dropped, re-apply it before committing. The `commit_ingest.py` script now warns if uncommitted changes remain after commit; treat that warning as a signal to inspect.
- **Commit hygiene** — if you do discover missing edits after a commit, stage the affected files explicitly and create a follow-up commit (e.g., `ingest(slug): complete pending concept cross-refs missed by first commit`) rather than amending or force-pushing.

## Skill Self-Update

The canonical, git-tracked copy of this skill is `.agents/skills/paper-reader/SKILL.md` in the main project repo (`proudzhu/llm-wiki`). Other IDE skill directories mirror it via filesystem links (`.claude/skills` and `.reasonix/skills` symlink to `..\.agents\skills`; `.gemini/skills` is a plain text file pointing at the same path — Windows symlink creation failed there). Edit the canonical `.agents/skills/paper-reader/SKILL.md` directly and commit normally.

If something unexpected happens during an ingest, consult [`references/pitfalls.md`](references/pitfalls.md) for concrete lessons from prior ingests.
