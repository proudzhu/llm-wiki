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

## Prerequisites

- Zotero must be running with "Allow other applications" enabled
- Verify with: `curl -s http://localhost:23119/connector/ping`
- `mineru-open-api` CLI available for MinerU extraction (`npm install -g mineru-open-api`)
- `defuddle` CLI available for arXiv HTML extraction (`npm install -g defuddle`)
- Micromamba env activation: `$env:PATH = "D:\micromamba-envs\llm-wiki;" + $env:PATH`

## Workflow Steps

### Step 1: Search Zotero for the Paper

```bash
curl -s "http://localhost:23119/api/users/0/items?q=SEARCH_TERMS&qmode=titleCreatorYear&limit=5"
```

Parse the JSON response to identify the correct paper. Note the **Zotero key** (e.g., `6EW3W6U6`).

### Step 2: Fetch Paper Details and Find PDF Attachment

```bash
# Full metadata
curl -s "http://localhost:23119/api/users/0/items/KEY"

# Find PDF attachment (search children or look in the item's links)
curl -s "http://localhost:23119/api/users/0/items/KEY/children"
```

Extract: title, authors, year, type, abstract, DOI, URL, tags, and **PDF attachment key**.

### Step 3: Extract Paper Content from PDF

#### 3a. Copy PDF and Create Directory

```bash
mkdir -p raw/papers/{slug}/
# Zotero storage path varies by user — check the PDF attachment key from Step 2
# Common paths: C:\Users\{username}\Zotero\storage\{PDF_KEY}\
# IMPORTANT: Do NOT use wildcard (*.pdf) to copy — Zotero filenames may contain
# Chinese characters (e.g., "Sharma 等 - 1998 - ...pdf") which cause silent copy failures.
# Instead, list the directory first and copy using the exact filename:
Get-ChildItem "C:\Users\{username}\Zotero\storage\{PDF_KEY}\" -Filter "*.pdf" | Copy-Item -Destination "raw/papers/{slug}/paper.pdf"
```

**Verify the PDF copy** is valid by checking the file header starts with `%` (PDF magic bytes):
```powershell
$bytes = [System.IO.File]::ReadAllBytes("raw/papers/{slug}/paper.pdf"); [System.Text.Encoding]::ASCII.GetString($bytes[0..4])
# Should output something like: %PDF-
```

If the header is empty or the file size is 0, the copy failed — re-copy using the exact filename from `Get-ChildItem`.

Slug format: `author-year-short-title` (lowercase, hyphenated, meaningful abbreviation).

#### 3b. arXiv HTML (Preferred for arXiv Papers)

If the paper has an arXiv ID, **always prefer the HTML version** — it provides better text quality than PDF extraction (preserves equations, tables, and figure links natively).

1. **Extract markdown with Defuddle**:
```bash
$env:PATH = "D:\micromamba-envs\llm-wiki;" + $env:PATH
defuddle parse "https://arxiv.org/html/ARXIV_ID" --md -o "raw/papers/{slug}/full-text.md"
```

2. **Download figures from arXiv HTML**:
```bash
mkdir -p raw/papers/{slug}/figures
# Download each figure referenced in the HTML (check the extracted markdown for URLs)
curl -s -L "https://arxiv.org/html/ARXIV_IDv1/figure1.png" -o "raw/papers/{slug}/figures/fig1.png"
# Repeat for all figures
```

3. **Replace remote image links with local paths** in `full-text.md`:
```
![caption](https://arxiv.org/html/ARXIV_IDv1/figure.png)  →  ![caption](figures/fig1.png)
```

4. **Delete the PDF** after extraction — only keep `full-text.md` and `figures/`:
```powershell
Remove-Item "raw/papers/{slug}/paper.pdf"
```

#### 3c. MinerU (For Non-arXiv Papers or arXiv Fallback)

For papers without an arXiv HTML version, or if Defuddle extraction fails, use MinerU `extract` with VLM model for high accuracy on formulas, tables, and complex layouts.

```bash
$env:PATH = "D:\micromamba-envs\llm-wiki;" + $env:PATH
mineru-open-api extract "raw/papers/{slug}/paper.pdf" -o "raw/papers/{slug}/full-text.md" --language en --model vlm --formula --table --timeout 600
```

**Parameters:**
- `--language en`: Set to paper's language (en, zh, etc.). Default is `ch` (Chinese+English)
- `--model vlm`: VLM-based layout analysis, higher accuracy (default choice)
- `--model pipeline`: Pipeline model, zero hallucination — use when exact text fidelity is critical
- `--formula`: Enable formula recognition
- `--table`: Enable table recognition
- `--timeout 600`: Extended timeout for large documents

**Token required**: MinerU `extract` requires authentication. Run `mineru-open-api auth` to configure, or set `MINERU_TOKEN` environment variable. Verify with `mineru-open-api auth --show`.

**Output**: Single `full-text.md` file with embedded LaTeX math and inline image references.

**Post-processing**: MinerU saves images in an `images/` subdirectory. Rename it to `figures/` and update the markdown references:
```powershell
Rename-Item "raw/papers/{slug}/images" "figures"
(Get-Content "raw/papers/{slug}/full-text.md") -replace 'images/', 'figures/' | Set-Content "raw/papers/{slug}/full-text.md"
```

**Note**: After renaming, image paths in the markdown reference `figures/...` relative to the `full-text.md` file location.

**Verify extraction quality**: Read the first 200 lines and last 100 lines of `full-text.md` to check for completeness.

**Delete the PDF** after successful extraction:
```powershell
Remove-Item "raw/papers/{slug}/paper.pdf"
```

**Troubleshooting**:
- If extract returns `parsing failed`, the PDF may be corrupted — verify with the PDF header check in 3a
- If server errors persist after retry, fall back to pdftotext (3d)
- If MinerU is not installed: `$env:PATH = "D:\micromamba-envs\llm-wiki;" + $env:PATH; npm install -g mineru-open-api`

#### 3d. Fallback: pdftotext (If MinerU Fails)

```bash
$env:PATH = "D:\micromamba-envs\llm-wiki;" + $env:PATH
pdftotext -layout "raw/papers/{slug}/paper.pdf" "raw/papers/{slug}/full-text.txt"
```

Font mismatch warnings from pdftotext are normal and can be ignored. Note: pdftotext produces `.txt` without images.

**Delete the PDF** after extraction:
```powershell
Remove-Item "raw/papers/{slug}/paper.pdf"
```

#### 3e. Extract Images (Optional)

Only extract images if the user explicitly requests it:

```bash
pdfimages -all "raw/papers/{slug}/paper.pdf" "raw/papers/{slug}/img"
```

### Step 4: Read and Analyze the Full Paper Content

Read the extracted text from `raw/papers/{slug}/full-text.md` (or `.txt` if from pdftotext fallback).

Extract:

- **Core problem and motivation**
- **Key technical contributions** (numbered)
- **Methodology** (architecture, algorithms, loss functions, equations)
- **Experimental setup** (datasets, metrics, hyperparameters)
- **Results** (quantitative tables, key findings)
- **Important distinctions** (e.g., how this differs from related work)
- **Future work directions**
- **Key concepts** that warrant their own wiki pages
- **Authors** who warrant entity pages

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

Figures should be included selectively — only when they convey information that text and tables cannot easily capture. Use the following criteria:

| Include figure? | Criteria | Examples |
|-----------------|----------|----------|
| ✅ Include | Visual is essential to understand the core problem or method | System block diagram, network architecture, problem illustration |
| ❌ Skip | Data is already well-summarized in text or tables | Performance curves, spectrogram plots, convergence plots |

Guidelines:
- Place figures immediately after the section they illustrate (not in a separate figures section)
- Use relative paths from the wiki root: `![caption](raw/papers/{slug}/figures/fig-name.png)`
- For arXiv papers extracted via Defuddle, figures are also in `figures/` subdirectory: `![caption](raw/papers/{slug}/figures/fig-name.png)`
- Add an italicized caption below each figure: `*Figure N: description.*`
- Maximum 3 figures per source page — prefer the most informative ones
- If figures are available in `raw/papers/{slug}/figures/`, reference them; do not embed or duplicate
- When adding figures, also update the corresponding concept pages with the same figure if it illustrates a key concept (e.g., network architecture on the concept page for that architecture)

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

### Step 7: Create Missing Concept Pages

For each key technical concept referenced via wikilinks in the source page but lacking a dedicated page in `wiki/concepts/`:

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

- [[../concepts/related|Related Concept]]

## Related Sources

- [[../sources/{slug}|Source Title]]
```

**Check first**: Use Glob to see if concept already exists. If so, update it with new information from this paper.

### Step 8: Update Existing Concept Pages

For concepts that already have pages:
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

### Step 10: Update Index

Update `wiki/index.md`:
- Add new entity rows to the Entities table
- Add new concept rows to the Concepts table
- Add new source row to the Sources table
- Update Statistics section (increment counts)

### Step 11: Update Log

Append to the **end** of `wiki/log.md` (entries are sorted by date ascending, newest at bottom):

```markdown
---

## [YYYY-MM-DD] ingest | Paper Title (Author Year)

- **Source**: `raw/papers/{slug}/full-text.md` (Zotero: KEY)
- **Authors**: Author1, Author2, Author3
- **Published**: Venue Year, pp. XXX–XXX
- **DOI**: 10.xxxx/xxxxx
- **Summary**: One-line summary
- **Pages created**:
  - `raw/papers/{slug}/full-text.md` — extracted text from Zotero PDF
  - `wiki/sources/{slug}.md`
  - `wiki/entities/author1.md`
  - `wiki/entities/author2.md`
- **Pages updated**:
  - `wiki/index.md` — added N entities, 1 source
```

For re-ingestion, use `ingest (re)` as the operation.

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Source slug | `author-year-short-title` | `farmani-2026-virtual-mic-beamforming-hearing-aid` |
| Entity slug | `firstname-lastname` | `mojtaba-farmani` |
| Concept slug | `descriptive-hyphenated` | `spatial-covariance-matrix` |

## Important Notes

- **Never modify** files in `raw/` after creation (immutability rule) — **exception**: replacing remote image URLs with local paths in `full-text.md` is allowed
- **Always check** if a page already exists before creating (use Glob)
- **Always read** existing pages before updating them (use Read)
- **Wikilinks** use relative paths: `[[../entities/name|Display Name]]` from sources
- **Cross-references** are bidirectional — when adding a link from A to B, also add a link from B to A
- **Frontmatter dates**: Use today's date for `created` on new pages, update `updated` on modified pages
- **No comments** in code/markdown unless explicitly requested
- **Prefer curl over Python** for Zotero API calls
- **Create missing concept pages** during ingest to maintain wiki integrity
- **Log entries**: Always append at the end (newest last)
