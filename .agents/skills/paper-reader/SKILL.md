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

## Checking Existing Pages (existence checks on this host)

Several steps require checking whether a page already exists. Three constraints shape how to do it:

- **There is no `LS` / directory-listing tool in this harness.** Use Glob, Grep, and Read.
- **Glob caps at 100 paths.** `wiki/concepts/*.md` returns `(Showing 100 of 502 paths)` — the 100 most recently modified, in modification-time order — so a directory-wide Glob is **not** an existence check: a page that exists may simply fall outside the window, producing a false "missing" and a duplicate page (`pitfalls.md` #56). When the cap is hit the tool reports where it spilled the complete sorted list; that spill file can be Grepped if you genuinely need the whole listing.
- **Glob brace expansion (`{a,b,c}.md`) does not work** and returns "No file found" even when the files exist.

**Preferred batch check — Grep the subdirectory index.** `wiki/{category}/index.md` carries a row for every page in that category, so a single alternation Grep answers any number of candidates at once:

```
Grep pattern: "temporal-cepstrum-smoothing|mmse-based-noise-psd-estimation|decision-directed-a-priori-snr"
      path: wiki/concepts/index.md
```

This resolved 5 candidates in 2 calls during the Gerkmann 2012 ingest. Caveat: it is only as current as the index — a page created but not yet indexed reads as "missing", and a deleted page can linger as a phantom row. Those are precisely the drifts `check_index_drift.py` exists to catch, and this workflow's Step 10 keeps the indexes honest for every page it creates.

**For a single candidate**, an exact-path Glob is precise and never capped: `wiki/concepts/temporal-cepstrum-smoothing.md` returns the file or nothing.

**Do not use Grep for existence on the directory itself** — Grep matches file *contents*: a page like `mvdr-beamformer.md` has H1 "MVDR Beamformer" and never contains its own slug (false "missing"), while `index.md` sits in that directory and contains *every* slug (false "exists"). Reserve Grep for finding pages that **mention** a name, e.g. pattern `seidel|fingscheidt|mowlaee` finds those authors' entity pages because the names appear in the body text (`pitfalls.md` #43).

Always use **forward slashes** in Glob patterns and prefer **relative paths from project root** over absolute Windows paths.

## Same-File Edit Discipline (applies to EVERY step)

**Never issue parallel Edit/Write calls to the same file.** A batch of N parallel edits to one file races: each call reads the file as it was when the batch started, and last-write-wins discards the others — *silently* (every call reports success). Which edit survives is nondeterministic; sometimes a *later* batch member persists on top of an earlier write, producing duplicated content on re-apply (see `pitfalls.md` #46).

This has bitten **three** ingests — Apostolidis 2026 (Step 8 concept pages), Xiao 2023 and Sun 2024 (Step 9 synthesis page and Step 10 `wiki/index.md`, where four parallel row-edits were lost and only the Statistics edit survived). Hence this top-level rule.

Rules:

1. **Parallelize across files, never within a file.** Reads, Globs, Greps, and Edits to *different* files are safe and encouraged in one message.
2. **Multiple changes to one file: pick one of two safe methods.** The `edit` tool takes a single `old_string`/`new_string` pair — **there is no `edits[]` array**, so "all of this file's changes in one atomic call" is not available (`pitfalls.md` #59). Either apply **sequential `edit` calls, one per message**, or **rewrite the file wholesale** (table below). What races is several `edit` calls against the same file in one message.
3. **Verify after a suspected race**: Grep the file for the expected new content (e.g. the new slug). If missing, re-read the target region before re-applying — a *prefix-matching* `old_string` can match text that already contains your addition and duplicate it.
4. Prefer scripts over hand-edits wherever one exists (`update_indexes.py`, `append_log.py`, `commit_ingest.py`) — they are immune to the race by construction.

**Choosing between sequential edits and a full rewrite:**

| Situation | Method |
|:----------|:-------|
| ≥2 changes to one file, and a single Read captured the **whole** file (typical concept/entity page) | **Rewrite**: `write` the complete updated content to the project root, then `Move-Item -Force` it over the target. One write per file ⇒ race-free by construction, and it parallelizes across files. |
| ≥2 changes to one file, page too large to reproduce safely (200–400-line synthesis pages) | **Sequential `edit` calls, one per message**, each anchored on unique surrounding text. |
| Exactly one change | A single `edit` call. |

A rewrite is only safe if the Read was **complete** — if its output carried a `(Showing lines X–Y of N)` trailer, you do not have the whole file and must not rewrite it. The Gerkmann 2012 ingest used the rewrite path for four existing pages in one parallel batch with zero lost writes; all three earlier races came from several `edit` *calls* against one file, never from a rewrite.

## Creating Pages Under `wiki/` (Write-Tool Caveat)

**The `write` tool fails for new files inside pre-existing directories.** In the Zhang 2026 ingest, creating `wiki/sources/{slug}.md` failed four times with `EEXIST: file already exists, mkdir 'D:\Projects\llm-wiki\wiki\sources'` — for a directory that plainly exists. Probing showed the failure is **path-dependent, not content-dependent**: writes into pre-existing directories (`wiki/`, `wiki/sources/`, `wiki/concepts/`, `wiki/queries/`, `raw/`, `schema/`, `scripts/`, `plugins/`, `.obsidian/`, `.githooks/`, `site/`) all fail, while writes to the **project root**, to **`.agents/**`**, and to **newly created** directories succeed. Retrying the same path never helps. See `pitfalls.md` #50.

Use one of these instead:

| Need | Method |
|------|--------|
| **Create a new page** (Steps 5, 7) | `write` to the project root (e.g. `zz_page.tmp.md`), then `Move-Item -Force zz_page.tmp.md wiki/sources/{slug}.md` |
| **Overwrite or update any existing page** (Steps 5, 6, 8, 9) | Same pattern — **`Move-Item -Force` overwrites**, so it covers camera-ready re-ingests and the multi-region-update path |
| **Single targeted change to an existing page** | `edit` is unaffected — it works normally on files under `wiki/`, so no workaround is needed |
| **Large or bulk content** | Same pattern again — `write` to the project root, then `Move-Item -Force`. There is **no working shell heredoc** on this host: `<<'ZEOF'` is a PowerShell parse error (`pitfalls.md` #60) |

> **`mv` does NOT overwrite here.** `mv` is a PowerShell **alias for `Move-Item`**, which refuses an existing destination with `Move-Item: 当文件已存在时，无法创建该文件。` The Gerkmann 2012 ingest lost all four Step 8 updates this way, because the create-only `mv` calls earlier in the same ingest had succeeded and the failure looked intermittent. Always `Move-Item -Force` when the target may exist (`pitfalls.md` #54).

Give temp files a distinctive name (e.g. `zz_<purpose>.tmp.md`) and delete stragglers before committing — `commit_ingest.py` stages only `wiki/` and `raw/`, so a leftover root-level temp file stays silently untracked.

## Prerequisites

- Zotero running with "Allow other applications" enabled
- `mineru-open-api` CLI (`npm install -g mineru-open-api`) — verify token: `mineru-open-api auth --show`
- `defuddle` CLI (`npm install -g defuddle`) for arXiv HTML extraction
- All scripts run from the **project root** via `uv run python .agents/skills/paper-reader/scripts/<script>.py`

### Environment — set `UV_CACHE_DIR` on every shell call

`uv`'s default cache lives outside the workspace (`D:\Scoop\persist\uv\cache`), which the file sandbox denies, so **every** `uv run` fails before doing any work:

```
error: Failed to initialize cache at `D:\Scoop\persist\uv\cache`
  Caused by: failed to open file `…\sdists-v9\.git`: 拒绝访问。 (os error 5)
```

Each shell call is a fresh process, so an exported variable does **not** persist between calls — prefix every invocation:

```powershell
$env:UV_CACHE_DIR = "D:\Projects\llm-wiki\.uv-cache"; uv run python .agents/skills/paper-reader/scripts/<script>.py --args
```

The error text resembles a broken Python environment or a missing dependency; it is purely the cache location (`pitfalls.md` #55). Every script in this skill — including the wiki-lint scripts and `build_check.py` — is affected equally.

The cache directory needs no `.gitignore` entry: `uv` writes its own `.uv-cache/.gitignore` containing `*`, so the whole cache self-ignores and never appears in `git status`.

## References (load on demand)

| Reference | When to load |
|-----------|--------------|
| [`references/review-papers.md`](references/review-papers.md) | **First** — if the paper is a review/survey/tutorial. Determines the routing for Steps 4–7. |
| [`references/page-templates.md`](references/page-templates.md) | Step 5-7 — full templates and concept-page threshold |
| [`references/edge-cases.md`](references/edge-cases.md) | Step 4 — graphical-only results, citation discrepancies, loose review classifications |
| [`references/pitfalls.md`](references/pitfalls.md) | When something unexpected happens, or skim before starting an ingest |

## Review/Survey Paper Routing

The default workflow (Steps 4–9) is shaped around **research papers** — Problem Formulation / Methodology / Experimental Setup / Results. **Review/survey/tutorial papers** need different analysis targets, source-page sections, concept-page thresholds, and figure selection. Detect them early and route accordingly.

### How to detect a review/survey paper

Any of the following is a strong signal (load [`references/review-papers.md`](references/review-papers.md) on the first match):

- **Title** contains: survey, overview, review, comprehensive, taxonomy, tutorial, primer, introduction to
- **Abstract** phrases: "we survey", "we review", "we present an overview", "this paper reviews", "a comprehensive review"
- **Zotero metadata**: `paperType` is `journalArticle` and the venue is a magazine (IEEE SPM, IEEE Comms. Surveys & Tutorials, ACM Comput. Surv.) rather than conference proceedings
- **Structure**: the paper's primary contribution is a taxonomy/comparison table, not a single proposed method; "Section II: Background" appears before any "Proposed Method"
- **Reference count**: 60+ references (reviews typically cite 50–200+; research papers usually 20–40)

### Step-by-step routing differences

Once you've identified a review/survey, these steps change:

| Step | Research-paper default | Review/survey variant |
|:-----|:-----------------------|:---------------------|
| **4 (Analyze)** | Extract: problem, contributions, methodology, experimental setup, results | Extract: **taxonomy**, comparison tables, application domains, open challenges, coverage gaps |
| **5 (Source page)** | Sections: Summary / Problem Formulation / Methodology / Experimental Setup / Results | Sections: Summary / Taxonomy / Methodology (surveyed methods) / Applications Survey / Key Contributions / Limitations and Caveats |
| **5 (Figures)** | Include system block diagrams, architecture diagrams, results plots | Prefer **taxonomy/comparison diagrams** over per-method architecture diagrams |
| **7 (New concepts)** | Create pages for novel methods/losses/architectures introduced by the paper | **Stricter threshold** — only create pages for concepts the review itself contributes a distinctive taxonomy or synthesis of; **do not** create a page for every surveyed term. Tutorials are an exception (a tutorial that introduces/formulates a concept distinctly warrants a page). |
| **8 (Update concepts)** | Add the paper as a source; extend sections with findings | Same, but the synthesis contribution is the taxonomy/comparison, not a new data point |
| **9 (Synthesis)** | Triage by tag overlap; update if new data point / gap-fill / refutation / new axis | Same triage, but reviews often **refine** existing synthesis claims (e.g., a review's framing of TSE vs. BSS sharpens the field's terminology) — this counts as trigger 3 (refines a claim). |

### Tutorials are a special case

Tutorial papers survey methods AND teach them. Treat tutorials as reviews for **structure** (Taxonomy / Applications Survey / Limitations), but treat them as research papers for **figure inclusion** — include every figure that aids comprehension of a surveyed method or concept (a tutorial with 7 application areas may legitimately warrant 15–25 figures).

## Workflow

### Step 1-2: Search Zotero & Fetch Metadata

```bash
uv run python .agents/skills/paper-reader/scripts/zotero_fetch.py search "SEARCH_TERMS"
uv run python .agents/skills/paper-reader/scripts/zotero_fetch.py metadata ZOTERO_KEY
```

Note the **Zotero key** (e.g., `8ZWV2E4T`) and **PDF attachment key** (e.g., `5H7GWRF3`).

**Keep search terms short (3–5 distinctive words)** — searching with the full paper title times out (Sun 2024 ingest: the complete title timed out; `"directional voice activity detection"` found it instantly, `pitfalls.md` #45).

If the paper has an arXiv ID but is not in Zotero, note the arXiv ID and proceed to Step 3b directly (skip `prepare_paper.py`).

**Multiple attachments**: Zotero items often have both an HTML attachment and a PDF attachment (e.g., IEEE Xplore saves both). Always pick the **PDF attachment** (`application/pdf`) for `prepare_paper.py` — HTML attachments from publisher sites are typically cluttered with navigation/ads and not suitable for extraction. The `zotero_fetch.py metadata` output lists all attachments with their MIME types; choose the one whose type is `application/pdf`.

**Verify authors, year, and venue before naming anything** (`pitfalls.md` #49). The Zotero record is a *lead*, not ground truth:

- **Creators can be incomplete.** The EUSIPCO 2026 ingest (`LVZPGG2Q`) returned only 3 of the paper's 4 authors — the **first author was missing entirely**. Since the slug's author segment, the H1, and the Step 6 entity set all derive from the author list, a bad Zotero list yields a wrong slug, a wrong H1, and a missing entity page.
- **`date`, `conferenceName`, and `publicationTitle` are often blank.** Resolve the year/venue from the paper itself or from an external listing (the conference's accepted-papers page, the publisher page, arXiv) — never default the year to "today".
- **`abstract` is often truncated mid-sentence** (Gerkmann 2012 returned the abstract cut off at "The MMSE-based approach em…", with no warning). Take the abstract from `full-text.md`, never from the Zotero field.
- **Page ranges are frequently absent.** The Step 11 log template shows `pp. XXX–XXX`, but if the range cannot be verified, **omit it** rather than inventing one, and note the omission on the source page (`pitfalls.md` #57).
- **The PDF is authoritative.** `full-text.md` exists by Step 4, so check its title page for the author list *and order*. Do this before Step 5 — the slug is baked into `raw/papers/{slug}/` by then, and renaming afterwards means updating every cross-reference.
- **Record the discrepancy** on the source page when Zotero and the paper disagree (author list, year, venue, truncated abstract), so the next reader knows the wiki page is deliberate.

### Step 3: Extract Paper Content

**Extraction priority**: arXiv HTML > MinerU > pdftotext. All scripts delete the PDF after extraction (so run `pdfimages` first if you need standalone images).

#### 3a. Prepare directory & copy PDF (skip for arXiv-only papers with HTML)

```bash
uv run python .agents/skills/paper-reader/scripts/prepare_paper.py --slug SLUG --pdf-key PDF_KEY
```

Slug format: `author-year-short-title` (lowercase, hyphenated), where **author = the paper's first author as printed on the title page** — not the first creator Zotero happens to list (see the verification block at the end of Step 1-2 and `pitfalls.md` #49).

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
- MinerU succeeds on short non-arXiv conference PDFs (the 4-page Gerkmann 2012 ICASSP paper extracted cleanly with `--model vlm`). The Xiao 2023 / Sun 2024 `parsing failed` runs were the exception, not the rule — do **not** pre-emptively skip MinerU (`pitfalls.md` #47).

#### 3d. pdftotext/pypdf fallback (plain text, no images)

```bash
uv run python .agents/skills/paper-reader/scripts/extract_pdftotext.py --slug SLUG
```

Uses `pdftotext` (poppler) if on PATH; **automatically falls back to `pypdf`** when poppler is not installed — common on Windows (both the Xiao 2023 and Sun 2024 ingests hit MinerU failures *and* had no poppler, forcing ad-hoc Python extraction; `pypdf` is now a project dependency so this path always works, `pitfalls.md` #47). If you resort to a custom extraction script anyway, it must still (i) write `full-text.txt`/`full-text.md` into `raw/papers/{slug}/` and (ii) **delete `paper.pdf` afterward** — every standard script enforces this, and `commit_ingest.py` refuses to stage `paper.pdf`; a manual `git add raw/papers/{slug}/` bypasses that guard (Sun 2024 committed its PDF this way, `pitfalls.md` #48).

#### 3e. Map figures to captions (after 3b or 3c)

```bash
uv run python .agents/skills/paper-reader/scripts/map_figures.py --slug SLUG
```

Pairs each hash-named crop with its "Fig. N." caption (line proximity), prints dimensions, flags axis/colorbar strips, exits 2 on referenced-but-missing hashes. One-call replacement for manual figure forensics (`pitfalls.md` #25). If no caption-style lines exist, it falls back automatically to the first in-text "Fig. N" reference of each figure (heuristic — verify multi-panel figures against the sub-labels it prints); only when it reports *neither* captions nor in-text references do you match manually (`pitfalls.md` #32).

### Step 4: Read and Analyze the Full Paper Content

Read the extracted text in chunks (head 200 + tail 100 + targeted range reads). Extract: core problem/motivation, key contributions (numbered), methodology (architecture/algorithms/losses/equations), experimental setup (datasets/metrics/hyperparameters), results (quantitative tables), key concepts warranting wiki pages, authors warranting entity pages.

**Neural-network papers** (any paper whose method includes a DNN/RNN/CNN/transformer/vocoder etc.): additionally extract the **model architecture** (layer-by-layer structure with sizes/densities), the **input features** (exact feature representation, frame rate, window length) and **output** (what the network produces, at what rate), and the **training losses** (equations with coefficient values). These feed the mandatory model-documentation section in Step 5 — see the **Neural-Network Model Documentation** rules in [`references/page-templates.md`](references/page-templates.md).

Classical/DSP papers have no such requirement, but a **mermaid data-flow diagram** of the algorithm is often the single most useful addition when the paper ships no block diagram of its own (the Gerkmann 2012 ingest added one showing preliminary speech PSD → cepstrum → selective smoothing → pitch detection → bias correction → MMSE noise estimate). See the mermaid rules in `page-templates.md` and the render check in Step 12.

**Review/survey paper**: use the **Analysis Targets** in [`references/review-papers.md`](references/review-papers.md) — taxonomy, comparison tables, application domains, open challenges, coverage gaps — instead of the research-paper-shaped list above. See the **Review/Survey Paper Routing** section earlier in this file for the full routing table.

**Numeric sign check (MinerU)**: MinerU can silently drop minus signs on negative numbers — the Ke 2021 SNR range −5…10 dB extracted as "5 dB to 10 dB", and the test SNRs {−5, 0, 5, 10} as "5, 0, 5, 10". Suspicious patterns: a 1 dB-step SNR sweep that appears to start positive, or a value list with a repeated entry after a sign flip. Cross-check numeric signs against the publisher page / abstract / PDF before writing them into the source page. (The Gerkmann 2012 extraction preserved its `−10` correctly, so the fault is intermittent — always eyeball any signed range.)

**If you encounter** graphical-only results, citation discrepancies, loose review classifications, or cross-references to already-ingested papers: load [`references/edge-cases.md`](references/edge-cases.md).

### Step 5: Create/Update Source Page

Create `wiki/sources/{slug}.md` (root-temp-then-`Move-Item -Force`, see *Creating Pages Under `wiki/`*). Load [`references/page-templates.md`](references/page-templates.md) for frontmatter, required sections (Summary / Problem Formulation / Methodology / Experimental Setup / Results / Key Contributions / Related Concepts / Related Synthesis), figure-usage criteria, and figure-filename verification rules. H1 is `Author1, Author2 & Author3 Year: Short Title`.

**Neural-network papers**: the source page MUST include a **Model Structure, Inputs, and Outputs** section with a **mermaid architecture block diagram** and per-network spec tables (structure / inputs / outputs / training data / role), plus a **Training Losses** section with the loss equations — see the **Neural-Network Model Documentation** rules in [`references/page-templates.md`](references/page-templates.md) for the template and mermaid syntax constraints.

**Review/survey paper**: use the **review-paper source-page template** in [`references/review-papers.md`](references/review-papers.md) — sections are Summary / Taxonomy / Methodology (surveyed methods) / Applications Survey / Key Contributions / Limitations and Caveats / Related Concepts / Related Sources. The research-paper sections (Problem Formulation / Experimental Setup / Results) do not apply unless the review itself reports original experiments.

**Figure embeds**: use `map_figures.py` output (Step 3e) to write `![[raw/papers/{slug}/figures/HASH.jpg|caption]]` — never markdown `![alt](path)` (`pitfalls.md` #27). Multi-panel figures: one `![[...]]` per (a)/(b) crop above the shared `*Figure N: ...*` caption (`pitfalls.md` #26).

**Unreferenced figure files**: `map_figures.py` lists files in `figures/` that `full-text.md` never references — these are typically axis/colorbar strips split off by MinerU (flagged as `<-- likely axis/colorbar strip, skip`). **Do not embed unreferenced files.** Only embed figures that are (i) referenced in `full-text.md` AND (ii) paired with a caption or an in-text "Fig. N" reference by `map_figures.py` (the in-text fallback runs automatically when no caption lines exist), or manually matched. If `map_figures.py` reports *neither* captions nor in-text references, fall back to reading the text for "Fig. N" / "Figure N" mentions and matching by position (see `pitfalls.md` #32).

For re-ingestion: overwrite the existing source page with updated comprehensive content — `write` to the project root, then `Move-Item -Force` (a direct `write` into a pre-existing `wiki/sources/` fails, and a bare `mv` will not clobber; see *Creating Pages Under `wiki/`* above).

### Step 6: Create or Update Entity Pages

For each author not already in `wiki/entities/`, create a new page (root-temp-then-`Move-Item -Force`). For existing authors, make **append-only** edits (update `updated:`, append a bullet to `## Key Contributions`, do not touch `created:` or rewrite existing bullets) — an append plus a frontmatter date is two regions, so use a whole-file rewrite or two sequential `edit` calls. Load [`references/page-templates.md`](references/page-templates.md) for the full template and the append-only update rules. **Check first**: Grep `wiki/entities/index.md` for the author slug (already-present authors are exactly the rows that Grep returns; do not Grep `wiki/entities/` itself, `pitfalls.md` #43).

### Step 7: Create Missing Concept Pages

For each key concept referenced via wikilink in the source page but lacking a dedicated page, create `wiki/concepts/{concept-name}.md` (root-temp-then-`Move-Item -Force`). Load [`references/page-templates.md`](references/page-templates.md) for the template and **concept-page threshold** (novelty / distinctive formulation / central-to-contribution). Do **not** create pages for generic ML/DL primitives (Adam, ReLU, dropout, gradient clipping) — link them as plain text.

**Review/survey paper**: apply the **stricter concept-page threshold** described in [`references/review-papers.md`](references/review-papers.md). A review surveys many terms, but only warrants creating a concept page when the review itself contributes a **distinctive taxonomy or synthesis** of that concept — not merely because the concept is mentioned. Tutorials are an exception (a tutorial that introduces/formulates a concept distinctly warrants a page).

**Batch existence check** (one Grep, not N Globs): collect all candidate concept slugs first, then check them in a single call against the subdirectory index:

```
Grep pattern: "slug-1|slug-2|slug-3|slug-4"
      path: wiki/concepts/index.md
```

Candidates with no match are confirmed missing and should be created (if they pass the concept-page threshold); candidates that *do* match already have pages and become the Step 8 update targets. Note two traps: a **directory-wide Glob is not a substitute** (it caps at 100 of 502 paths — `pitfalls.md` #56), and Grepping the *directory* rather than its index gives false positives via `index.md` and false negatives for every page whose slug is not in its own body (`pitfalls.md` #43).

### Step 8: Update Existing Concept Pages

For each existing concept page touched by this paper: add the paper to `sources:` in frontmatter, update `updated:` date, add new sections with findings, extend `## Related Concepts` and `## Related Sources` with new wikilinks.

**Identify existing concept pages to update** from the Step 7 index Grep — the candidates that *did* match are the existing pages. No separate existence check needed.

**Efficient batched-update pattern** (when updating >2 existing concept pages in one ingest):

1. **Read all target pages in parallel** — one Read per file in a single message (different files, safe). Check each read is complete: if the output ends with a `(Showing lines X–Y of N)` trailer you do not have the whole file. Typical ingest touches 4–8 existing concept pages.
2. **Make exactly one write per file, then parallelize across files.** Each page needs frontmatter (`sources:`, `updated:`, `tags:`) + a new body section + `## Related Concepts` / `## Related Sources` extensions. Since `edit` handles only one `old_string`/`new_string` pair (`pitfalls.md` #59):
   - **Small/medium page** → rewrite: `write` the complete updated content to the project root, then `Move-Item -Force` it over the target. One write per file, so issuing all of them in a single parallel batch cannot race — the Gerkmann 2012 ingest updated 4 pages this way with zero lost writes.
   - **Large page** (200–400-line synthesis-style pages) → sequential `edit` calls, one per message.
3. **Verify every file afterwards** — Grep each edited page for one intended addition (e.g. the new slug under `## Related Sources`). A failed `edit` anchor applies **nothing** (`pitfalls.md` #51); a rewrite that silently did not land shows up as the file missing from `git status`.

**Never issue several parallel `edit` calls against the *same* file** (`pitfalls.md` #13; see the top-level "Same-File Edit Discipline" section). Parallelize *across files*, never *within* a file. `commit_ingest.py` emits `WARN: uncommitted changes remain after commit` when an edit was silently dropped — in the normal case that list contains only `.obsidian/` churn, so read the file list before assuming a drop (`pitfalls.md` #58).

### Step 9: Update Synthesis Pages

**Triage first** (cheap — avoids reading 200–400-line synthesis pages). **Precondition**: the source page `wiki/sources/{slug}.md` must already exist (Step 5) — the script reads its frontmatter tags and exits with an error if the page is missing:

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

**Record which triage outcome actually occurred.** "No matches" and "6 candidates, all sharing a single broad-topic tag" are different results, and the source page's `## Related Synthesis` section must state the true one. Standard wording for the thin-match case:

> _None. Triage (`triage_synthesis.py`, YYYY-MM-DD) returned 6 candidates (`a`, `b`, …), but each shared only a single broad-topic tag (`speech-enhancement`), so all were skipped without reading._

Never write "no matches" when triage did return candidates — the distinction tells a later reader the triage was run rather than skipped.

**Concrete trigger examples** (from real ingests):

| Trigger | Example |
|:--------|:--------|
| 1 (new data point) | CoFi-Lite (Yang 2026) ingest added a row to the efficiency-frontier table in `deep-speech-enhancement.md` — (0.78M params, 0.6 GMACs, PESQ 2.92) was a new point on the existing params-vs-quality frontier. |
| 2 (gap-fill) | A future ingest of a PercepNet successor that adds ERB-scale-complexity numbers would fill a gap in the `multi-scale-speech-enhancement` comparison, which currently lacks that column for PercepNet-style models. |
| 3 (refine claim) | Zmolikova 2023 ingest refined `deep-speech-enhancement.md` Insight 8 — the review's framing of TSE as "internally solving identify + extract" sharpened the existing PSE/OVC complementarity claim, giving it a cleaner conceptual handle. |
| 4 (new axis) | A future ingest of a wave-RNN-based TSE paper would introduce "vocoder stage" as a new comparison axis in `multi-modal-speech-enhancement.md`, which currently tracks only clue type and fusion method. |

**When in doubt**: prefer *not* updating. A thin synthesis addition adds clutter; a substantive one (1–2 sentences + a table row) is valuable. If you cannot write at least one substantive sentence about what the paper *contributes to the cross-source analysis*, skip.

**Earn your `## Related Synthesis` links.** List a synthesis page under `## Related Synthesis` only if triage actually surfaced it (tag overlap) and you either updated it or can justify why not. A link the triage never returned is usually *conceptual adjacency* rather than a relation the synthesis supports — the Zhang 2026 ingest initially linked `secondary-path-modeling-evolution` because both concern "path identification", but that synthesis covers the **secondary** path, while the paper identifies the **feedback** path; triage had already reported zero tag overlap, which was the correct signal (`pitfalls.md` #53).

**Applying a synthesis update** typically means 4–6 changes to the *same* file: frontmatter `sources:` + `updated:`, frontmatter `tags:`, a row in the Sources Synthesized table, a paragraph in the matching insight, possibly a takeaway and an open question. These sit in several far-apart regions, so **sequential `edit` calls, one per message** (large file — do not rewrite it wholesale), or one rewrite if the file was fully read and is small. Afterwards, Grep the file for the new slug to confirm every change landed (the Sun 2024 ingest lost 3 of 5 parallel synthesis edits).

### Step 10: Update Indexes

**Do not hand-edit index tables for new entries** — use the scripts below. Hand-editing is the known cause of lost rows: in the Sun 2024 ingest, four parallel manual edits to `wiki/index.md` all reported success but only the Statistics edit survived, leaving the three new slugs unindexed (caught by the mandatory Grep check below and `check_index_drift.py`). The scripts write rows atomically and recompute statistics; hand-edits are acceptable only for *modifying* an existing row's summary/date.

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

**Manifest hygiene**:

- **Write `display` and `summary` as prose, not math.** Each row is a pipe-delimited markdown table; `update_indexes.py` now escapes bare pipes, but `E[|N|^2 | y]` becomes `E[\|N\|^2 \| y]` in two index files — write `E[|N|^2 given y]` instead.
- **Use the ingest date (`YYYY-MM-DD`)** for `date`. Recent rows all do; older rows in `wiki/sources/index.md` carry the paper's publication year. Do not mix the two styles within one batch.

For one-off additions or re-ingests, use `add --category <cat> --slug <slug> --display "..." --summary "..." --date YYYY-MM-DD`, then run `stats`.

**Verify after updating indexes** (mandatory, one Grep call): confirm every new slug actually landed in both the main index and its subdirectory index. Long ingests can lose track of which entries were added — statistics alone do not prove the table rows exist (the Guldenschuh 2014 ingest had correct statistics but missing table rows, caught only by this check):

```
Grep pattern: "new-slug-1|new-slug-2|new-slug-3"   include: index.md
      path: wiki
```

Each new slug must appear in **two** files: `wiki/index.md` and `wiki/{category}/index.md`. If a slug is missing from either, add the row before proceeding. Note that each category directory contains its own `index.md`, so `ls wiki/sources | wc -l` overcounts by one — for page counts use `check_statistics.py` (or `update_indexes.py`'s own `stats` output), never a directory listing (`pitfalls.md` #52).

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

**Link format in log bodies** (`pitfalls.md` #40): reference wiki pages with vault-absolute wikilinks (`[[sources/slug|Title]]`) or backticked plain paths (`wiki/sources/slug.md`) — **never** `../`-relative markdown links like `[Title](../sources/slug.md)`, which do not resolve from `wiki/log.md` and abort `mkdocs build --strict`. `append_log.py` validates the body and rejects such links (exit 2) before appending.

### Step 12: Build Verification

**Step 12a — Wikilink verification** (fast pre-check, catches broken links before the build):

```bash
uv run python .agents/skills/paper-reader/scripts/verify_wikilinks.py --slug SLUG
```

Checks both `[[category/slug]]` wikilinks and `![[raw/...]]` figure embeds against the filesystem, and flags LaTeX math (`$...$`) in wikilink/embed display text — math aliases mangle the pipe-escaping and abort the build (`pitfalls.md` #44). A single-character hash typo in a MinerU figure filename (`...151105...` vs `...158105...`) aborts the mkdocs build — this check catches it here, before the 60+ second build cycle. Scans the source page + all new/modified `wiki/*.md` files; exits 0 if all links resolve, 1 if broken links found. Fix any broken links (create the missing page, correct the slug, or use plain text; for embeds, Glob the `figures/` dir with a hash prefix and copy the exact filename) before proceeding to 12b.

**Step 12b — MkDocs strict build**:

```bash
uv run python .agents/skills/paper-reader/scripts/build_check.py
```

If the build fails, resolve broken links/missing pages before proceeding. Pre-existing `INFO` messages about `log.md` links and the Material "MkDocs 2.0" banner do not fail the build (`pitfalls.md` #8, #28). The check intentionally runs **without `--quiet`**: mkdocs's `--quiet` sets the log level to ERROR, which filters WARNING records before strict-mode's counter sees them — a `--quiet` build can exit 0 despite strict violations (observed in the Ke 2021 ingest). INFO-level nav lines in the output are normal. A clean run takes ~45 s.

**Step 12c — Statistics check** (required by `AGENTS.md`; independent of Step 10's own recount):

```bash
uv run python .agents/skills/wiki-lint/scripts/check_statistics.py
```

`update_indexes.py batch --stats` writes the counts; this verifies them against the actual files (`OK` per category, or a stated-vs-actual mismatch to fix).

**Step 12d — Mermaid render check** (only if a page added a mermaid fenced code block). `mkdocs build --strict` **passes** even when mermaid is unconfigured, silently emitting a syntax-highlighted code block instead of a diagram (`pitfalls.md` #38). Confirm the built page really contains the diagram:

```
Grep pattern: class="mermaid"    path: site/sources/{slug}.html
```

A match on `<pre class="mermaid">` means it renders; none means fix `mkdocs.yml`'s superfences `custom_fences`.

### Step 13: Commit Changes

```bash
uv run python .agents/skills/paper-reader/scripts/commit_ingest.py \
    --slug SLUG --message "ingest: Short Title (Author Year)" \
    --entities author1 author2 --concepts concept1 concept2 --synthesis synth1
```

Stages `raw/papers/{slug}/`, `wiki/sources/{slug}.md`, all index files, `wiki/log.md`, and the specified entity/concept/synthesis pages. Verifies no `paper.pdf` is staged. **Auto-stages** any other modified/untracked file under `wiki/` (catches Step 8 edits to existing concept/entity pages that would otherwise be dropped) — pass `--strict` to disable.

**`--no-verify` when the hook cannot run under the sandbox.** On this host the pre-commit hook fails for a purely environmental reason, with this exact signature:

```
Commit failed:
  0 [main] sh (…): *** fatal error - couldn't create signal pipe, Win32 error 5
```

The hook runs `sh.exe` (MSYS), which needs a named pipe the file sandbox forbids — it is unrelated to the staged content, so retrying, re-staging, or trimming the file list will not help. Re-run the identical command with `--no-verify`. This loses no verification **only because Step 12b already ran the same strict build the hook runs** — never skip the hook without a clean 12b (`pitfalls.md` #58).

Afterwards, `WARN: uncommitted changes remain after commit` listing **only** `.obsidian/*.json` is the expected steady state (Obsidian config churn, deliberately excluded — `pitfalls.md` #37). It signals a dropped edit only when `wiki/` paths appear in that list.

## Important Notes

- **`raw/` immutability exception**: replacing remote image URLs with local paths in `full-text.md` is allowed.
- **Avoid `\bm{}` in LaTeX math** — MathJax does not load the `bm` package. Use `\mathbf{x}` or `\boldsymbol{x}` instead.
- **Never put LaTeX math in a wikilink alias** — `[[concepts/foo|$\mathcal{L}$]]` breaks the `fix_obsidian_escapes` pipe-escaping and aborts `mkdocs build --strict` (`pitfalls.md` #44). Use a plain-text alias (`[[concepts/foo|Spectrally Adaptive Loss]]`) and keep the math outside the wikilink.
- **Always commit via `commit_ingest.py`** — manual `git add`/`git commit` bypasses its guards: it refuses to stage `paper.pdf`, auto-stages all `wiki/` modifications, and avoids PowerShell quoting entirely. If a manual commit is unavoidable: exclude `paper.pdf` and `.obsidian/`, and pass multi-paragraph messages as multiple `-m` flags.
- **Shell facts for this host (verified 2026-09-11)**: PowerShell **7.6.6**; `&&` works; bash heredocs (`<<'EOF'`) are a **parse error** — never propose one; `$_` automatic variables are **not** stripped. Older notes in `pitfalls.md` claiming otherwise were stale and are corrected in #60. Re-verify with a one-line command before adding any *new* environment claim to these docs.
- **Todo list structure**: one todo per workflow step (1–13), in numerical order. Treat Steps 3a–3e as a single "extract content" todo. Treat Step 12a–12d as a single "build verification" todo. If Step 9 triage finds no candidates, mark that todo `completed` with "none relevant — grep triage" rather than leaving it `pending`.
