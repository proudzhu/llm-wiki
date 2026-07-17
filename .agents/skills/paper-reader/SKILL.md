---
name: "paper-reader"
description: "Full paper ingestion workflow from Zotero to wiki: search, extract, analyze, and create wiki pages. Invoke when user asks to ingest, re-ingest, or read a paper from Zotero."
---

# Paper Reader

End-to-end workflow for ingesting academic papers from Zotero into the LLM Wiki knowledge base.

## When to Invoke

Invoke this skill when the user asks to:
- "ingest paper X from Zotero"
- "re-ingest paper X from Zotero"
- "read paper X from Zotero"
- Add a paper from their Zotero library to the wiki

## When NOT to Invoke

- **Paper is already in the wiki and up-to-date** — Check `wiki/sources/` and `wiki/log.md` first. If the paper was recently ingested and nothing changed, skip.
- **User just wants a quick summary** — For a skim or TL;DR, read the existing wiki source page or use the abstract directly. Full ingestion is only warranted for deep analysis.
- **Zotero is not running or unreachable** — The workflow depends on Zotero's local API. Verify first: `curl -s http://localhost:23119/connector/ping`.
- **Paper is not in the user's Zotero library** — This skill only ingests from Zotero. For external papers (e.g. direct arXiv URL), skip Zotero steps and use extraction scripts directly.
- **Source is not a PDF/academic paper** — Web pages, blog posts, and informal documents should use the standard raw article workflow instead.
- **Re-ingestion of an identical version** — Only re-ingest if the source PDF was updated (e.g., camera-ready replaces preprint) or the existing wiki page is significantly incomplete.

## Checking Existing Pages (Windows Glob Caveat)

Several steps require checking whether an entity/concept/source page already exists. **On Windows, Glob brace expansion (`{a,b,c}.md`) does not work** and returns "No file found" even when files exist. Use one of these patterns instead:

- **Grep with alternation** (preferred for batch checks): `Grep` with pattern `seidel|fingscheidt|mowlaee`, path `wiki/entities`, `-i true` — returns all matching files in one call.
- **Multiple parallel Glob calls**: one Glob per slug, e.g. `wiki/entities/ernst-seidel.md`, `wiki/entities/tim-fingscheidt.md` (no braces).
- **LS the directory**: `LS wiki/entities` returns the full file list; scan visually for the target slugs.

Always use **forward slashes** in Glob patterns (e.g. `wiki/concepts/*bark*.md`), and prefer **relative paths from project root** over absolute Windows paths (`d:\...`) — the latter sometimes fail with backslash escaping.

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
| `scripts/update_indexes.py` | 10 | Add rows to `wiki/index.md` + subdirectory indexes; recount statistics |
| `scripts/append_log.py` | 11 | Append formatted entry to `wiki/log.md` |
| `scripts/build_check.py` | 12 | Run `mkdocs build --strict` (tries `uv run` then `python -m`) |
| `scripts/commit_ingest.py` | 13 | Stage ingest files + verify no `paper.pdf` + commit |

## Workflow

### Step 1-2: Search Zotero & Fetch Metadata

```bash
# Search by title/author/year
python .agents/skills/paper-reader/scripts/zotero_fetch.py search "SEARCH_TERMS"

# Fetch full metadata + PDF attachment key for the chosen item
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

The script checks if HTML exists (falls back to MinerU with exit code 2 if 404), runs Defuddle, downloads figures, and replaces remote image links with local embed wikilinks.

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

**Note**: MinerU figures are hash-named JPEGs (e.g., `8b539670…583.jpg`). When referencing them, list the `figures/` directory to discover actual filenames — the filenames are deterministic from the PDF content.

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

#### Handling Graphical-Only Results

Some papers report key metrics **only in figures** (bar charts, curves) without a numeric table. When this happens:

- Do **not** fabricate numbers from the figure — transcription from rendered charts is error-prone.
- In the source page's `## Results` section, state explicitly: *"AECMOS / DNSMOS scores are reported graphically in Figure N (not as a numeric table). Key qualitative findings from the figure:"* and then list the findings as labeled bullet points matching the paper's own discussion (e.g., "(a) LEC scores highest on DT Other").
- Always include the numeric tables that **are** present (e.g., ERLE tables, complexity tables) — these are transcription-safe.
- When a later paper cites this paper's numeric scores, prefer the later paper's cited values **only if** they are explicitly attributed; otherwise flag the discrepancy (see "Citation discrepancies" below).

#### Handling Citation Discrepancies

Later papers often cite earlier work with **different numbers** than the original paper self-reports (e.g., different param counts, MACs/s, or band counts due to different counting methodologies, inclusion/exclusion of the linear stage, or simply typos). When you ingest a paper and notice its self-reported numbers differ from how a later, already-ingested paper cites it:

1. **Use the original paper's self-reported numbers** in the new source page.
2. **Add a discrepancy note** in the new source page (under `## Results` or a dedicated note) explaining the mismatch with the later citation.
3. **Update the already-ingested later paper's concept/entity pages** that reference the old numbers — correct the numbers and add a note pointing to the original paper as the authoritative source.
4. **Do not** modify the later paper's `wiki/sources/*.md` page (immutability of interpretation aside, the later paper *did* cite those numbers — note the discrepancy but leave the citation as-is in the source page; fix only the concept/synthesis pages that treat the cited numbers as ground truth).

### Step 5: Create/Update Source Page

Create `wiki/sources/{slug}.md` with comprehensive content:

**Frontmatter:**
```yaml
---
type: source
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - raw/papers/{slug}/full-text.md
  - https://doi.org/...
  - zotero://select/items/0_KEY
tags:
  - relevant-tags
---
```

**Required sections:**
- `# Author1, Author2 & Author3 Year: Short Title` — H1 with author-year short title
- Bibliographic metadata (author wikilinks, institution, venue, year, type, DOI, Zotero link)
- `## Summary` — 2-3 sentence overview
- `## Problem Formulation` — key equations and problem setup
- `## Methodology` — core methods and algorithms
- `## Experimental Setup` — table format
- `## Results` — quantitative findings
- `## Key Contributions` — numbered list
- `## Related Concepts` — wikilinks to concept pages
- `## Related Synthesis` — wikilinks to synthesis pages

**Figure usage in source pages:**

| Include figure? | Criteria | Examples |
|-----------------|----------|----------|
| Include | Visual is essential to understand the core problem or method | System block diagram, network architecture, problem illustration |
| Skip | Data is already well-summarized in text or tables | Performance curves, spectrogram plots, convergence plots |

Guidelines:
- Place figures immediately after the section they illustrate
- Use vault-absolute embed wikilink paths: `![[raw/papers/{slug}/figures/ACTUAL_FILENAME.ext|caption]]`
- **List the `figures/` directory first** to discover actual filenames — MinerU produces hash-named `.jpg` files, arXiv HTML figures are named `fig1.png`
- Add an italicized caption below each figure: `*Figure N: description.*`
- Maximum 3 figures per source page — prefer the most informative ones
- When adding figures, also update corresponding concept pages with the same figure if it illustrates a key concept

**For re-ingestion**: Overwrite the existing source page with updated comprehensive content.

### Step 6: Create Entity Pages

For each author not already in `wiki/entities/`:

```yaml
---
type: entity
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - researcher
  - relevant-field-tags
---

# Author Name

**Affiliation**: Institution, Location
**Role**: Researcher
**Research Focus**: Research areas.

## Key Contributions

- Paper contribution (Venue Year)
```

**Check first**: Use Glob to see if entity already exists. If so, update it instead.

#### Updating an existing entity page

When the author already has a page, make these specific edits (do not rewrite the page):

1. Update `updated:` date in frontmatter to today.
2. Append the new paper to `## Key Contributions` as a new bullet, with a wikilink to the new source page: `- Co-authored [short title] (Venue Year) — [[sources/{slug}|Author Year]]`
3. If the new paper reveals a new affiliation, research focus area, or tag not already on the page, add it (do not replace existing content).
4. If the new paper is the author's primary contribution (more important than prior listed work), consider moving it to the top of the list — but otherwise preserve chronological/listed order.
5. Do **not** touch the `created:` date or rewrite existing bullets.

### Step 7: Create Missing Concept Pages

For each key technical concept referenced via wikilinks in the source page but lacking a dedicated page:

```yaml
---
type: concept
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - relevant-tags
---

# Concept Name

Definition and overview.

## Key Formulations

Math and equations.

## Related Concepts

- [[concepts/related|Related Concept]]

## Related Sources

- [[sources/{slug}|Source Title]]
```

**Check first**: Use Glob to see if concept already exists. If so, update it.

### Step 8: Update Existing Concept Pages

- Add the paper to `sources:` in frontmatter (if applicable)
- Update `updated:` date
- Add new sections or expand existing ones with findings from this paper
- Add cross-references (wikilinks) to new concepts/entities
- Add the paper to `## Related Sources` section

### Step 9: Update Synthesis Pages

Check if any existing synthesis pages should reference this paper:
- Add findings that contribute to cross-source analysis
- Update `updated:` date
- Add to `## Related Sources`

### Step 10: Update Indexes

For each new page created, add a row to the indexes:

```bash
# Add source row
python .agents/skills/paper-reader/scripts/update_indexes.py add \
    --category sources --slug SLUG --display "Title" --summary "..." --date YYYY-MM-DD

# Add entity rows
python .agents/skills/paper-reader/scripts/update_indexes.py add \
    --category entities --slug author-name --display "Author Name" --summary "..." --date YYYY-MM-DD

# Add concept rows
python .agents/skills/paper-reader/scripts/update_indexes.py add \
    --category concepts --slug concept-name --display "Concept Name" --summary "..." --date YYYY-MM-DD
```

The script inserts into both `wiki/index.md` (correct section) and the subdirectory index, skipping duplicates. Then update statistics:

```bash
python .agents/skills/paper-reader/scripts/update_indexes.py stats
```

This recounts all categories and rewrites the `## Statistics` section.

### Step 11: Update Log

Write the log entry body to a temp file (or use `--stdin`/`--body`), then append:

```bash
python .agents/skills/paper-reader/scripts/append_log.py --op ingest --title "Paper Title (Author Year)" --file .tmp_log_entry.md
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

### Step 13: Commit Changes

```bash
python .agents/skills/paper-reader/scripts/commit_ingest.py \
    --slug SLUG \
    --message "ingest: Short Title (Author Year)" \
    --entities author1 author2 \
    --concepts concept1 concept2 \
    --synthesis synth1
```

The script stages `raw/papers/{slug}/`, `wiki/sources/{slug}.md`, all index files, `wiki/log.md`, and the specified entity/concept/synthesis pages. It verifies no `paper.pdf` is staged and commits. Use `--no-verify` if the pre-commit hook has environment issues unrelated to your changes.

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Source slug | `author-year-short-title` | `tan-2018-convolutional-recurrent-network-speech-enhancement` |
| Entity slug | `firstname-lastname` | `ke-tan` |
| Concept slug | `descriptive-hyphenated` | `convolutional-recurrent-network` |

## Important Notes

- **Skill self-update**: The canonical, git-tracked copy of this skill is `.agents/skills/paper-reader/SKILL.md` in the main project repo (`proudzhu/llm-wiki`). Other IDE skill directories may mirror it via filesystem links:
  - `.claude/skills` → symbolic link to `..\.agents\skills` ✅
  - `.reasonix/skills` → symbolic link to `..\.agents\skills` ✅
  - `.gemini/skills` → plain text file containing `../.agents/skills/` (Windows symlink creation failed; not a real link) ⚠️

  Edit the canonical `.agents/skills/paper-reader/SKILL.md` directly. Commit normally: `git add .agents/skills/paper-reader/SKILL.md && git commit -m "..."`.
- **Never modify** files in `raw/` after creation (immutability rule) — **exception**: replacing remote image URLs with local paths in `full-text.md` is allowed
- **Always check** if a page already exists before creating (use Glob/Read)
- **Always read** existing pages before updating them
- **Wikilinks** use vault-absolute paths: `[[entities/name|Display Name]]` from any page
- **Never use `../` prefixes inside wikilinks**
- **Never link to a page that does not exist** — if you reference `[[concepts/some-new-concept]]`, create that page or leave as plain text
- **Cross-references** are bidirectional — when adding a link from A to B, also add from B to A
- **Frontmatter dates**: Use today's date for `created`, update `updated` on modified pages
- **Create missing concept pages** during ingest to maintain wiki integrity
- **Avoid `\bm{}` in LaTeX math**: MathJax does not load the `bm` package. Use `\mathbf{x}` (bold upright) or `\boldsymbol{x}` (bold italic) instead
- **Delete the PDF** after extraction — extraction scripts handle this automatically; never commit `paper.pdf`
- **Commit after build verification** — use `--no-verify` only if the pre-commit hook has environment issues unrelated to your changes

## Common Pitfalls

Concrete lessons from prior ingests:

1. **Brace glob on Windows fails silently** — `wiki/entities/{a,b,c}.md` returns "No file found" even when files exist. Use Grep with alternation or multiple parallel Globs (see "Checking Existing Pages" above).
2. **Citation discrepancies propagate** — Later papers often cite earlier work with wrong numbers (e.g., EchoFree 2025 cited Seidel 2024 with 1.62M params / 107 MMACs/s / 100 Bark bands, but the original reports 1.58M / 235M / 86). When ingesting the original paper, use its self-reported numbers and add a discrepancy note; update concept/synthesis pages that treated the later citation as ground truth (see "Handling Citation Discrepancies" in Step 4).
3. **Graphical results are not tables** — Do not transcribe numbers from bar charts or curves. Use qualitative labeled bullet points matching the paper's own discussion (see "Handling Graphical-Only Results" in Step 4).
4. **Entity updates are append-only** — When an author already has a page, append the new paper to `## Key Contributions` with a wikilink; do not rewrite existing bullets or change `created:` (see Step 6 "Updating an existing entity page").
5. **Pick the PDF attachment, not HTML** — Zotero items from IEEE/ACM often have both. HTML attachments are cluttered with publisher chrome; always extract from `application/pdf`.
6. **MinerU figure filenames are deterministic hashes** — Do not guess filenames. Always `LS` the `figures/` directory after extraction to discover actual names before writing embed wikilinks.
7. **`update_indexes.py stats` is mandatory after `add`** — The `add` subcommand inserts rows but does not recompute the `## Statistics` section. Always run `stats` after all `add` calls, or `wiki/index.md` will show stale totals.
8. **Build hook INFO messages are not errors** — `mkdocs build --strict` may emit `INFO - Doc file 'log.md' contains an unrecognized relative link` for pre-existing issues in `log.md`. These do not fail the build (exit 0) and are not caused by your ingest; do not block on them.
9. **Synthesis pages are optional but high-value** — Not every paper warrants a synthesis update, but when a new paper is a key data point on an existing efficiency/architecture frontier (e.g., a new point on the AEC complexity-vs-quality Pareto curve), add it to the synthesis's sources table and write 1–2 sentences on what it contributes to the cross-source analysis.
