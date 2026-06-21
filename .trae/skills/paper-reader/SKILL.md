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
- **Zotero is not running or unreachable** — The workflow depends on Zotero's local API. Verify first with `curl -s http://localhost:23119/connector/ping`.
- **Paper is not in the user's Zotero library** — This skill only ingests from Zotero. For external papers, manually download the PDF and use a different workflow.
- **Source is not a PDF/academic paper** — This skill is designed for scholarly articles. Web pages, blog posts, and informal documents should use the standard raw article workflow instead.
- **Re-ingestion of an identical version** — Only re-ingest if the source PDF was updated (e.g., camera-ready replaces preprint) or the existing wiki page is significantly incomplete.

## Prerequisites

- Zotero must be running with "Allow other applications" enabled
- Verify with: `curl -s http://localhost:23119/connector/ping`
- `mineru-open-api` CLI available for MinerU extraction (`npm install -g mineru-open-api`)
- **Verify MinerU token is configured** before attempting extraction (avoids 600s timeout on auth failure):
  ```bash
  mineru-open-api auth --show
  ```
  If no token shown, run `mineru-open-api auth` to configure.
- `defuddle` CLI available for arXiv HTML extraction (`npm install -g defuddle`)

## Workflow Steps

### Step 1: Search Zotero for the Paper

```bash
curl -s "http://localhost:23119/api/users/0/items?q=SEARCH_TERMS&qmode=titleCreatorYear&limit=5"
```

Parse the JSON response to identify the correct paper. Note the **Zotero key** (e.g., `6EW3W6U6`).

### Step 2: Fetch Paper Details and Find PDF Attachment

```bash
# Save full metadata to temp file (avoids PowerShell encoding issues with JSON)
curl -s "http://localhost:23119/api/users/0/items/KEY" > .tmp_zotero.json

# Read the temp file with the Read tool to extract metadata fields

# Find PDF attachment (search children)
curl -s "http://localhost:23119/api/users/0/items/KEY/children" > .tmp_children.json
# Read the temp file to find the PDF attachment key (contentType: "application/pdf")
```

Extract: title, authors, year, type, abstract, DOI, URL, tags, and **PDF attachment key**.

**Clean up** temp files:
```bash
rm -f .tmp_zotero.json .tmp_children.json
```
```powershell
Remove-Item .tmp_zotero.json, .tmp_children.json -ErrorAction SilentlyContinue
```

### Step 3: Extract Paper Content from PDF

#### 3a. Copy PDF and Create Directory

Create directory:
```bash
mkdir -p "raw/papers/{slug}"
```
```powershell
New-Item -ItemType Directory -Force -Path "raw/papers/{slug}" | Out-Null
```

Copy PDF from Zotero storage (`C:\Users\proud\Zotero\storage\{PDF_KEY}\`). **Zotero filenames often contain non-ASCII characters (umlauts, CJK, etc.) that break bash `cp`. Use Python for reliable cross-platform copying:**
```bash
python -c "
import shutil, glob
files = glob.glob('C:/Users/proud/Zotero/storage/{PDF_KEY}/*.pdf')
if files:
    shutil.copy2(files[0], 'raw/papers/{slug}/paper.pdf')
    print('Copied:', files[0])
else:
    print('No PDF found')
"
```
```powershell
$pdf = Get-ChildItem "C:\Users\proud\Zotero\storage\{PDF_KEY}\" -Filter "*.pdf" | Select-Object -First 1
Copy-Item $pdf.FullName "raw/papers/{slug}/paper.pdf"
```

**Verify** the PDF header:
```bash
head -c 5 "raw/papers/{slug}/paper.pdf"
# Should output: %PDF-
```
```powershell
$bytes = [System.IO.File]::ReadAllBytes("raw/papers/{slug}/paper.pdf"); [System.Text.Encoding]::ASCII.GetString($bytes[0..4])
# Should output: %PDF-
```

If the header is empty or file size is 0, re-copy with the exact filename.

Slug format: `author-year-short-title` (lowercase, hyphenated).

#### 3b. arXiv HTML (Preferred for arXiv Papers)

If the paper has an arXiv ID, **always prefer the HTML version** — better text quality than PDF extraction. **But first verify it exists** — many older papers (pre-2022) don't have HTML versions:
```bash
curl -s -o /dev/null -w "%{http_code}" "https://arxiv.org/html/ARXIV_ID"
# If 200, proceed with HTML extraction below.
# If 404, fall back to MinerU (Step 3c).
```

1. **Extract markdown with Defuddle**:
```bash
defuddle parse "https://arxiv.org/html/ARXIV_ID" --md -o "raw/papers/{slug}/full-text.md"
```

2. **Download figures from arXiv HTML**:
```bash
mkdir -p raw/papers/{slug}/figures
curl -s -L "https://arxiv.org/html/ARXIV_IDv1/figure1.png" -o "raw/papers/{slug}/figures/fig1.png"
# Repeat for all figures
```

3. **Replace remote image links with local paths** in `full-text.md`.

4. **Delete the PDF**:
```bash
rm -f "raw/papers/{slug}/paper.pdf"
```
```powershell
Remove-Item "raw/papers/{slug}/paper.pdf"
```

#### 3c. MinerU (For Non-arXiv Papers or arXiv Fallback)

```bash
mineru-open-api extract "raw/papers/{slug}/paper.pdf" -o "raw/papers/{slug}/full-text.md" --language en --model vlm --formula --table --timeout 600
```

**Parameters**: `--language en` (paper language), `--model vlm` (VLM layout analysis, default), `--model pipeline` (zero-hallucination), `--formula`, `--table`, `--timeout 600`.

**Token required**: Run `mineru-open-api auth` to configure, or set `MINERU_TOKEN`. Verify with `mineru-open-api auth --show`.

**Post-processing**: MinerU saves images in an `images/` subdirectory. Rename and update references:
```bash
mv "raw/papers/{slug}/images" "raw/papers/{slug}/figures"
sed -i 's|images/|figures/|g' "raw/papers/{slug}/full-text.md"
```
```powershell
Move-Item "raw/papers/{slug}/images" "raw/papers/{slug}/figures" -Force
(Get-Content "raw/papers/{slug}/full-text.md") -replace 'images/', 'figures/' | Set-Content "raw/papers/{slug}/full-text.md"
```

**Verify extraction quality**: Read first 200 lines and last 100 lines of `full-text.md`.

**Note**: MinerU VLM may produce mermaid code blocks for diagrams — these are normal and can be left as-is.

**Delete the PDF** after successful extraction:
```bash
rm -f "raw/papers/{slug}/paper.pdf"
```
```powershell
Remove-Item "raw/papers/{slug}/paper.pdf"
```

**Troubleshooting**:
- If extract returns `parsing failed`, verify PDF is valid (Step 3a header check)
- If server errors persist, fall back to pdftotext (3d)
- If MinerU is not installed: `npm install -g mineru-open-api`

#### 3d. Fallback: pdftotext (If MinerU Fails)

```bash
pdftotext -layout "raw/papers/{slug}/paper.pdf" "raw/papers/{slug}/full-text.txt"
```

Font mismatch warnings are normal. Note: pdftotext produces `.txt` without images.

**Delete the PDF**:
```bash
rm -f "raw/papers/{slug}/paper.pdf"
```
```powershell
Remove-Item "raw/papers/{slug}/paper.pdf"
```

#### 3e. Extract Images (Optional — before deleting PDF)

If the user explicitly requests it, extract images **before the PDF is deleted** (add this step before the deletion command in whichever extraction path was taken):
```bash
pdfimages -all "raw/papers/{slug}/paper.pdf" "raw/papers/{slug}/img"
```
Requires `poppler-utils`.

**Note**: MinerU figures are hash-named JPEGs (e.g., `8b539670…583.jpg`). When referencing them in a source page, list the `figures/` directory to discover actual filenames rather than guessing — the filenames are deterministic from the PDF content.

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
| ✅ Include | Visual is essential to understand the core problem or method | System block diagram, network architecture, problem illustration |
| ❌ Skip | Data is already well-summarized in text or tables | Performance curves, spectrogram plots, convergence plots |

Guidelines:
- Place figures immediately after the section they illustrate
- Use vault-absolute wikilink paths: `![[raw/papers/{slug}/figures/ACTUAL_FILENAME.ext|caption]]`
- **List the `figures/` directory first** to discover actual filenames — MinerU produces hash-named `.jpg` files, arXiv HTML figures are named `fig1.png`
- Add an italicized caption below each figure: `*Figure N: description.*`
- Maximum 3 figures per source page — prefer the most informative ones
- If figures are available in `raw/papers/{slug}/figures/`, reference them (do not embed or duplicate)
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

**Main index** (`wiki/index.md`):
- Add new entity rows to the Entities table
- Add new concept rows to the Concepts table
- Add new source row to the Sources table
- Update Statistics section (increment counts)

**Subdirectory indexes** (append new rows to each):
- `wiki/sources/index.md` — add new source row
- `wiki/entities/index.md` — add new entity rows
- `wiki/concepts/index.md` — add new concept rows

### Step 11: Update Log

Append to the **end** of `wiki/log.md` (entries sorted by date ascending, newest at bottom):

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
  - `wiki/concepts/concept1.md`
  - `wiki/concepts/concept2.md`
- **Pages updated**:
  - `wiki/entities/existing-author.md` — added this paper
  - `wiki/concepts/existing-concept.md` — added cross-refs and source link
  - `wiki/synthesis/synthesis-page.md` — added paper to relevant synthesis
  - `wiki/index.md` — added N entities, N concepts, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added N entity rows
  - `wiki/concepts/index.md` — added N concept rows
```

For re-ingestion, use `ingest (re)` as the operation.

### Step 12: Build Verification (MkDocs)

```bash
uv run mkdocs build --strict
```

If `uv run` is unavailable:
```bash
python -m mkdocs build --strict
```

If the command fails or exits with warnings (broken links, missing pages), resolve them before proceeding.

### Step 13: Commit Changes

```bash
git add raw/papers/{slug}/ wiki/sources/{slug}.md wiki/index.md wiki/log.md wiki/sources/index.md
# Add new/modified entity, concept, and synthesis files explicitly (avoid broad dir adds):
git add wiki/entities/{author1}.md wiki/entities/{author2}.md wiki/concepts/{concept1}.md wiki/concepts/{concept2}.md
# Then update subdirectory indexes:
git add wiki/entities/index.md wiki/concepts/index.md
git status --short   # verify no PDF or unrelated files staged
git commit -m "ingest: Short Title (Author Year)"
```

If a pre-commit hook fails (e.g., `uv run` not found), bypass it:
```bash
git commit --no-verify -m "ingest: Short Title (Author Year)"
```

**Never commit `paper.pdf`** — if it appears staged, remove it:
```bash
git rm --cached "raw/papers/{slug}/paper.pdf" && rm -f "raw/papers/{slug}/paper.pdf" && git commit --no-verify --amend --no-edit
```

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Source slug | `author-year-short-title` | `tan-2018-convolutional-recurrent-network-speech-enhancement` |
| Entity slug | `firstname-lastname` | `ke-tan` |
| Concept slug | `descriptive-hyphenated` | `convolutional-recurrent-network` |

## Important Notes

- **Skill self-update**: The canonical, git-tracked copy of this skill is `.trae/skills/paper-reader/SKILL.md` in the main project repo (`proudzhu/llm-wiki`). The `.claude/skills`, `.reasonix/skills`, and `.agents/skills` directories are **symbolic links** to `.trae/skills` — they are the same file, not separate copies, so editing any path edits the canonical file. Only `.trae/` is git-tracked; commit normally: `git add .trae/skills/paper-reader/SKILL.md && git commit -m "..."`.
- **Never modify** files in `raw/` after creation (immutability rule) — **exception**: replacing remote image URLs with local paths in `full-text.md` is allowed
- **Always check** if a page already exists before creating (use Glob/Read)
- **Always read** existing pages before updating them
- **Wikilinks** use vault-absolute paths: `[[entities/name|Display Name]]` from any page
- **Never use `../` prefixes inside wikilinks**
- **Never link to a page that does not exist** — if you reference `[[concepts/some-new-concept]]`, create that page or leave as plain text
- **Cross-references** are bidirectional — when adding a link from A to B, also add from B to A
- **Frontmatter dates**: Use today's date for `created`, update `updated` on modified pages
- **Prefer curl over Python** for Zotero API calls
- **Create missing concept pages** during ingest to maintain wiki integrity
- **Log entries**: Always append at the end (newest last)
- **Avoid `\bm{}` in LaTeX math**: MathJax does not load the `bm` package. Use `\mathbf{x}` (bold upright) or `\boldsymbol{x}` (bold italic) instead
- **Delete the PDF** after extraction — never commit `paper.pdf`
- **Commit after build verification** — use `--no-verify` only if the pre-commit hook has environment issues unrelated to your changes
