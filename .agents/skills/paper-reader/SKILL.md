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

- **Paper already in wiki and up-to-date** — Grep `wiki/log.md` and `wiki/sources/*.md` for author/title first
- **User wants a quick summary** — read the existing source page or abstract; full ingest is only for deep analysis
- **Zotero not running** — verify: `curl -s http://localhost:23119/connector/ping`
- **Paper not in Zotero** — skip Zotero steps, use extraction scripts directly with an arXiv ID or local PDF
- **Source is a web page/blog/informal HTML** — use the standard raw article workflow. **Exception**: substantive non-academic PDFs (transcripts, slides, presentations) DO qualify — adapt the source page template with themed sections (Vision & Strategy / Q&A / Key Quotes); slug follows thought-piece convention without a year (e.g., `liang-wenfeng-investor-exchange-meeting`)
- **Re-ingesting an identical version** — only if PDF was updated (camera-ready replaces preprint) or the wiki page is significantly incomplete

## Checking Existing Pages (Windows Glob Caveat)

Several steps require checking whether a page already exists. **On Windows, Glob brace expansion (`{a,b,c}.md`) does not work** and returns "No file found" even when files exist. Use one of these patterns instead:

- **Grep with alternation** (preferred for batch checks): `Grep` with pattern `seidel|fingscheidt|mowlaee`, path `wiki/entities`, `-i true` — returns all matching files in one call.
- **Multiple parallel Glob calls**: one Glob per slug (no braces), e.g. `wiki/entities/ernst-seidel.md`.
- **LS the directory**: `LS wiki/entities` returns the full file list; scan visually for the target slugs.

Always use **forward slashes** in Glob patterns and prefer **relative paths from project root** over absolute Windows paths.

**Do not use `RunCommand` with PowerShell `Where-Object { $_.Name -match '...' }`** for batch existence checks — the shell wrapper strips `$_` and other `$`-prefixed automatic variables, producing "item not recognized" errors (see `pitfalls.md` #31). Prefer the Grep tool with alternation, which calls ripgrep directly and avoids PowerShell quoting entirely.

## Prerequisites

- Zotero running with "Allow other applications" enabled
- `mineru-open-api` CLI (`npm install -g mineru-open-api`) — verify token: `mineru-open-api auth --show`
- `defuddle` CLI (`npm install -g defuddle`) for arXiv HTML extraction
- All scripts run from the **project root** via `uv run python .agents/skills/paper-reader/scripts/<script>.py`

## References (load on demand)

| Reference | When to load |
|-----------|--------------|
| [`references/page-templates.md`](references/page-templates.md) | Step 5-7 — full templates and concept-page threshold |
| [`references/edge-cases.md`](references/edge-cases.md) | Step 4 — graphical-only results, citation discrepancies, loose review classifications |
| [`references/review-papers.md`](references/review-papers.md) | Step 4-7 — when the paper is a review/survey |
| [`references/pitfalls.md`](references/pitfalls.md) | When something unexpected happens, or skim before starting an ingest |

## Workflow

### Step 1-2: Search Zotero & Fetch Metadata

```bash
uv run python .agents/skills/paper-reader/scripts/zotero_fetch.py search "SEARCH_TERMS"
uv run python .agents/skills/paper-reader/scripts/zotero_fetch.py metadata ZOTERO_KEY
```

Note the **Zotero key** (e.g., `8ZWV2E4T`) and **PDF attachment key** (e.g., `5H7GWRF3`).

If the paper has an arXiv ID but is not in Zotero, note the arXiv ID and proceed to Step 3b directly (skip `prepare_paper.py`).

**Multiple attachments**: Zotero items often have both an HTML attachment and a PDF attachment (e.g., IEEE Xplore saves both). Always pick the **PDF attachment** (`application/pdf`) for `prepare_paper.py` — HTML attachments from publisher sites are typically cluttered with navigation/ads and not suitable for extraction. The `zotero_fetch.py metadata` output lists all attachments with their MIME types; choose the one whose type is `application/pdf`.

### Step 3: Extract Paper Content

**Extraction priority**: arXiv HTML > MinerU > pdftotext. All scripts delete the PDF after extraction (so run `pdfimages` first if you need standalone images).

#### 3a. Prepare directory & copy PDF (skip for arXiv-only papers with HTML)

```bash
uv run python .agents/skills/paper-reader/scripts/prepare_paper.py --slug SLUG --pdf-key PDF_KEY
```

Slug format: `author-year-short-title` (lowercase, hyphenated).

#### 3b. arXiv HTML (preferred for arXiv papers — better text quality than PDF)

```bash
uv run python .agents/skills/paper-reader/scripts/extract_arxiv_html.py --arxiv-id ARXIV_ID --slug SLUG
```

Auto-creates `raw/papers/{slug}/`. Falls back to MinerU (exit code 2) if HTML 404 or `defuddle` missing — then run 3a + 3c.

#### 3c. MinerU (non-arXiv papers or arXiv fallback)

```bash
uv run python .agents/skills/paper-reader/scripts/extract_mineru.py --slug SLUG [--language en --model vlm --timeout 600]
```

- `--model vlm` (default, layout analysis) or `--model pipeline` (zero-hallucination). Token required: `mineru-open-api auth`.
- **Language codes** (MinerU convention, NOT ISO 639 — `zh` is INVALID, use `ch`): `ch` (Chinese), `en` (English), `chinese_cht`, `japan`, `korean`, `latin`, `arabic`, `cyrillic`, `east_slavic`, `devanagari`, `ta`/`te`/`ka`. Script validates locally; invalid codes exit 2 with the valid list.
- Post-processing: `images/` → `figures/`, refs updated in `full-text.md`.
- Verify quality: Read first 200 + last 100 lines. Mermaid code blocks for diagrams are normal.

#### 3d. pdftotext fallback (plain text, no images)

```bash
uv run python .agents/skills/paper-reader/scripts/extract_pdftotext.py --slug SLUG
```

#### 3e. Map figures to captions (after 3b or 3c)

```bash
uv run python .agents/skills/paper-reader/scripts/map_figures.py --slug SLUG
```

Pairs each hash-named crop with its "Fig. N." caption (line proximity), prints dimensions, flags axis/colorbar strips, exits 2 on referenced-but-missing hashes. One-call replacement for manual figure forensics (`pitfalls.md` #25).

### Step 4: Read and Analyze the Full Paper Content

Read the extracted text in chunks (head 200 + tail 100 + targeted range reads). Extract: core problem/motivation, key contributions (numbered), methodology (architecture/algorithms/losses/equations), experimental setup (datasets/metrics/hyperparameters), results (quantitative tables), key concepts warranting wiki pages, authors warranting entity pages.

**If review/survey**: load [`references/review-papers.md`](references/review-papers.md). **If you encounter** graphical-only results, citation discrepancies, loose review classifications, or cross-references to already-ingested papers: load [`references/edge-cases.md`](references/edge-cases.md).

### Step 5: Create/Update Source Page

Create `wiki/sources/{slug}.md`. Load [`references/page-templates.md`](references/page-templates.md) for frontmatter, required sections (Summary / Problem Formulation / Methodology / Experimental Setup / Results / Key Contributions / Related Concepts / Related Synthesis), figure-usage criteria, and figure-filename verification rules. H1 is `Author1, Author2 & Author3 Year: Short Title`.

**Figure embeds**: use `map_figures.py` output (Step 3e) to write `![[raw/papers/{slug}/figures/HASH.jpg|caption]]` — never markdown `![alt](path)` (`pitfalls.md` #27). Multi-panel figures: one `![[...]]` per (a)/(b) crop above the shared `*Figure N: ...*` caption (`pitfalls.md` #26).

For re-ingestion: overwrite the existing source page with updated comprehensive content.

### Step 6: Create or Update Entity Pages

For each author not already in `wiki/entities/`, create a new page. For existing authors, make **append-only** edits (update `updated:`, append a bullet to `## Key Contributions`, do not touch `created:` or rewrite existing bullets). Load [`references/page-templates.md`](references/page-templates.md) for the full template and the append-only update rules. **Check first**: Grep `wiki/entities` for the author slug.

### Step 7: Create Missing Concept Pages

For each key concept referenced via wikilink in the source page but lacking a dedicated page, create `wiki/concepts/{concept-name}.md`. Load [`references/page-templates.md`](references/page-templates.md) for the template and **concept-page threshold** (novelty / distinctive formulation / central-to-contribution). Do **not** create pages for generic ML/DL primitives (Adam, ReLU, dropout, gradient clipping) — link them as plain text. **Check first**: Grep `wiki/concepts` for the concept slug.

### Step 8: Update Existing Concept Pages

For each existing concept page touched by this paper: add the paper to `sources:` in frontmatter, update `updated:` date, add new sections with findings, extend `## Related Concepts` and `## Related Sources` with new wikilinks.

**Efficient batched-update pattern** (when updating >2 existing concept pages in one ingest):

1. **Read all target pages in parallel** — one Read per file in a single message (different files, safe). Typical ingest touches 4–8 existing concept pages.
2. **Round 1 — frontmatter edits in parallel** — one Edit per file (different files, safe).
3. **Round 2 — content additions in parallel** — one Edit per file.
4. **Round 3 — `## Related Concepts` / `## Related Sources` extensions in parallel** — one Edit per file.

**Parallel Edits to the *same* file race and silently drop each other** (`pitfalls.md` #13). Parallelize *across files*, never *within* a file. If a single page needs frontmatter + content + Related Sources changes, apply them as **sequential Edit calls in separate messages**. `commit_ingest.py` emits `WARN: uncommitted changes remain after commit` when an edit was silently dropped.

### Step 9: Update Synthesis Pages

**Triage first** (cheap — avoids reading 200–400-line synthesis pages):

```bash
uv run python .agents/skills/paper-reader/scripts/triage_synthesis.py --slug SLUG
```

- **No matches** → skip Step 9 entirely (common for single-method papers).
- **Candidates** with `Shared tags (1): <broad-topic>` (e.g. `speech-enhancement`, `beamforming`, `audio-processing`, `signal-processing`, `machine-learning`) → **skip without reading** — topical coincidence. Read only if N ≥ 2, or N = 1 with a contribution-specific tag (e.g. `lpcnet`, `packet-loss-concealment`).
- **Surviving candidates** → read, then update if any trigger fires:
  1. New data point on an existing frontier (params/MACs/quality tuple)
  2. Fills a gap in an existing comparison
  3. Refutes or refines an existing synthesis claim
  4. Introduces a new axis of comparison

**When in doubt**: prefer *not* updating. A thin synthesis addition adds clutter; a substantive one (1–2 sentences + a table row) is valuable. If you cannot write at least one substantive sentence about what the paper *contributes to the cross-source analysis*, skip.

### Step 10: Update Indexes

For ingests creating **multiple pages** (typical: 1 source + 2–4 entities + 5–15 concepts), **prefer `batch`** with a YAML manifest:

```yaml
# .tmp_ingest_manifest.yaml
entries:
  - category: sources
    slug: author-year-short-title
    display: "Author Year: Short Title"
    summary: "One-line summary"
    date: YYYY-MM-DD
  # ... repeat for each entity and concept
```

```bash
uv run python .agents/skills/paper-reader/scripts/update_indexes.py batch \
    --manifest .tmp_ingest_manifest.yaml --stats
```

`--stats` recounts statistics automatically. Delete the temp manifest afterward.

For one-off additions or re-ingests, use `add --category <cat> --slug <slug> --display "..." --summary "..." --date YYYY-MM-DD`, then run `stats`.

### Step 11: Update Log

Write the entry body to a temp file, then call the script:

```bash
uv run python .agents/skills/paper-reader/scripts/append_log.py --op ingest \
    --title "Paper Title (Author Year)" --file .tmp_log_entry.md
```

Entry body format (temp file):

```markdown
- **Source**: `raw/papers/{slug}/full-text.md` (Zotero: KEY)
- **Authors**: Author1, Author2, ...
- **Published**: Venue Year, pp. XXX–XXX
- **DOI**: 10.xxxx/xxxxx
- **Summary**: One-line summary
- **Pages created**: list each new file path
- **Pages updated**: list each modified file with a short note (e.g., "added cross-refs")
```

For re-ingestion, use `ingest (re)` in `--title`.

### Step 12: Build Verification

```bash
uv run python .agents/skills/paper-reader/scripts/build_check.py
```

If the build fails, resolve broken links/missing pages before proceeding. Pre-existing `INFO` messages about `log.md` links and the Material "MkDocs 2.0" banner do not fail the build (`pitfalls.md` #8, #28).

### Step 13: Commit Changes

```bash
uv run python .agents/skills/paper-reader/scripts/commit_ingest.py \
    --slug SLUG --message "ingest: Short Title (Author Year)" \
    --entities author1 author2 --concepts concept1 concept2 --synthesis synth1
```

Stages `raw/papers/{slug}/`, `wiki/sources/{slug}.md`, all index files, `wiki/log.md`, and the specified entity/concept/synthesis pages. Verifies no `paper.pdf` is staged. **Auto-stages** any other modified/untracked file under `wiki/` (catches Step 8 edits to existing concept/entity pages that would otherwise be dropped) — pass `--strict` to disable. Use `--no-verify` only if the pre-commit hook has environment issues unrelated to your changes.

## Important Notes

- **`raw/` immutability exception**: replacing remote image URLs with local paths in `full-text.md` is allowed.
- **Avoid `\bm{}` in LaTeX math** — MathJax does not load the `bm` package. Use `\mathbf{x}` or `\boldsymbol{x}` instead.
- **Todo list structure**: one todo per workflow step (1–13), in numerical order. Treat Steps 3a–3e as a single "extract content" todo. If Step 9 triage finds no candidates, mark that todo `completed` with "none relevant — grep triage" rather than leaving it `pending`.
