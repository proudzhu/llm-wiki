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

- **LS the directory** (ground truth for existence — filenames cannot lie): `LS wiki/entities` returns the full file list; scan for the target slugs. One call checks any number of candidates.
- **Multiple parallel Glob calls**: one Glob per slug (no braces), e.g. `wiki/entities/ernst-seidel.md`.
- **Grep with alternation** — *content search only, not an existence check.* Grep matches file **contents**, not filenames: a page rarely contains its own slug (e.g. `mvdr-beamformer.md` has H1 "MVDR Beamformer", so grepping `mvdr-beamformer` misses it — false "missing"), while `index.md` contains *every* slug (false "exists"). Use Grep only to find pages that **mention** a name, e.g. pattern `seidel|fingscheidt|mowlaee` finds those authors' entity pages because the names appear in the body text. See `pitfalls.md` #43.

Always use **forward slashes** in Glob patterns and prefer **relative paths from project root** over absolute Windows paths.

**Do not use `RunCommand` with PowerShell `Where-Object { $_.Name -match '...' }`** for batch existence checks — the shell wrapper strips `$_` and other `$`-prefixed automatic variables, producing "item not recognized" errors (see `pitfalls.md` #31). Use the LS/Glob/Grep tools directly instead; they avoid PowerShell quoting entirely.

## Prerequisites

- Zotero running with "Allow other applications" enabled
- `mineru-open-api` CLI (`npm install -g mineru-open-api`) — verify token: `mineru-open-api auth --show`
- `defuddle` CLI (`npm install -g defuddle`) for arXiv HTML extraction
- All scripts run from the **project root** via `uv run python .agents/skills/paper-reader/scripts/<script>.py`

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

Pairs each hash-named crop with its "Fig. N." caption (line proximity), prints dimensions, flags axis/colorbar strips, exits 2 on referenced-but-missing hashes. One-call replacement for manual figure forensics (`pitfalls.md` #25). If no caption-style lines exist, it falls back automatically to the first in-text "Fig. N" reference of each figure (heuristic — verify multi-panel figures against the sub-labels it prints); only when it reports *neither* captions nor in-text references do you match manually (`pitfalls.md` #32).

### Step 4: Read and Analyze the Full Paper Content

Read the extracted text in chunks (head 200 + tail 100 + targeted range reads). Extract: core problem/motivation, key contributions (numbered), methodology (architecture/algorithms/losses/equations), experimental setup (datasets/metrics/hyperparameters), results (quantitative tables), key concepts warranting wiki pages, authors warranting entity pages.

**Neural-network papers** (any paper whose method includes a DNN/RNN/CNN/transformer/vocoder etc.): additionally extract the **model architecture** (layer-by-layer structure with sizes/densities), the **input features** (exact feature representation, frame rate, window length) and **output** (what the network produces, at what rate), and the **training losses** (equations with coefficient values). These feed the mandatory model-documentation section in Step 5 — see the **Neural-Network Model Documentation** rules in [`references/page-templates.md`](references/page-templates.md).

**Review/survey paper**: use the **Analysis Targets** in [`references/review-papers.md`](references/review-papers.md) — taxonomy, comparison tables, application domains, open challenges, coverage gaps — instead of the research-paper-shaped list above. See the **Review/Survey Paper Routing** section earlier in this file for the full routing table.

**Numeric sign check (MinerU)**: MinerU can silently drop minus signs on negative numbers — the Ke 2021 SNR range −5…10 dB extracted as "5 dB to 10 dB", and the test SNRs {−5, 0, 5, 10} as "5, 0, 5, 10". Suspicious patterns: a 1 dB-step SNR sweep that appears to start positive, or a value list with a repeated entry after a sign flip. Cross-check numeric signs against the publisher page / abstract / PDF before writing them into the source page.

**If you encounter** graphical-only results, citation discrepancies, loose review classifications, or cross-references to already-ingested papers: load [`references/edge-cases.md`](references/edge-cases.md).

### Step 5: Create/Update Source Page

Create `wiki/sources/{slug}.md`. Load [`references/page-templates.md`](references/page-templates.md) for frontmatter, required sections (Summary / Problem Formulation / Methodology / Experimental Setup / Results / Key Contributions / Related Concepts / Related Synthesis), figure-usage criteria, and figure-filename verification rules. H1 is `Author1, Author2 & Author3 Year: Short Title`.

**Neural-network papers**: the source page MUST include a **Model Structure, Inputs, and Outputs** section with a **mermaid architecture block diagram** and per-network spec tables (structure / inputs / outputs / training data / role), plus a **Training Losses** section with the loss equations — see the **Neural-Network Model Documentation** rules in [`references/page-templates.md`](references/page-templates.md) for the template and mermaid syntax constraints.

**Review/survey paper**: use the **review-paper source-page template** in [`references/review-papers.md`](references/review-papers.md) — sections are Summary / Taxonomy / Methodology (surveyed methods) / Applications Survey / Key Contributions / Limitations and Caveats / Related Concepts / Related Sources. The research-paper sections (Problem Formulation / Experimental Setup / Results) do not apply unless the review itself reports original experiments.

**Figure embeds**: use `map_figures.py` output (Step 3e) to write `![[raw/papers/{slug}/figures/HASH.jpg|caption]]` — never markdown `![alt](path)` (`pitfalls.md` #27). Multi-panel figures: one `![[...]]` per (a)/(b) crop above the shared `*Figure N: ...*` caption (`pitfalls.md` #26).

**Unreferenced figure files**: `map_figures.py` lists files in `figures/` that `full-text.md` never references — these are typically axis/colorbar strips split off by MinerU (flagged as `<-- likely axis/colorbar strip, skip`). **Do not embed unreferenced files.** Only embed figures that are (i) referenced in `full-text.md` AND (ii) paired with a caption or an in-text "Fig. N" reference by `map_figures.py` (the in-text fallback runs automatically when no caption lines exist), or manually matched. If `map_figures.py` reports *neither* captions nor in-text references, fall back to reading the text for "Fig. N" / "Figure N" mentions and matching by position (see `pitfalls.md` #32).

For re-ingestion: overwrite the existing source page with updated comprehensive content.

### Step 6: Create or Update Entity Pages

For each author not already in `wiki/entities/`, create a new page. For existing authors, make **append-only** edits (update `updated:`, append a bullet to `## Key Contributions`, do not touch `created:` or rewrite existing bullets). Load [`references/page-templates.md`](references/page-templates.md) for the full template and the append-only update rules. **Check first**: LS `wiki/entities` and scan the filenames for the author slug (entity pages don't contain their own slug, so a content Grep gives false "missing").

### Step 7: Create Missing Concept Pages

For each key concept referenced via wikilink in the source page but lacking a dedicated page, create `wiki/concepts/{concept-name}.md`. Load [`references/page-templates.md`](references/page-templates.md) for the template and **concept-page threshold** (novelty / distinctive formulation / central-to-contribution). Do **not** create pages for generic ML/DL primitives (Adam, ReLU, dropout, gradient clipping) — link them as plain text.

**Review/survey paper**: apply the **stricter concept-page threshold** described in [`references/review-papers.md`](references/review-papers.md). A review surveys many terms, but only warrants creating a concept page when the review itself contributes a **distinctive taxonomy or synthesis** of that concept — not merely because the concept is mentioned. Tutorials are an exception (a tutorial that introduces/formulates a concept distinctly warrants a page).

**Batch existence check** (one LS call, not N Globs): before creating any concept page, list all candidate concept slugs from the source page and check them against the directory listing:

```
LS wiki/concepts
```

Scan the returned filenames for each candidate. Candidates absent from the list are confirmed missing and should be created (if they pass the concept-page threshold). Do **not** use Grep for this — it matches file *contents*: a page like `mvdr-beamformer.md` doesn't contain its own slug (false "missing"), and any page *mentioning* a slug in a wikilink matches (false "exists"). See the "Checking Existing Pages" section above and `pitfalls.md` #43.

### Step 8: Update Existing Concept Pages

For each existing concept page touched by this paper: add the paper to `sources:` in frontmatter, update `updated:` date, add new sections with findings, extend `## Related Concepts` and `## Related Sources` with new wikilinks.

**Identify existing concept pages to update** from the same Step 7 LS listing — the candidates that *did* appear in `wiki/concepts` are the existing pages to update here. No separate existence check needed.

**Efficient batched-update pattern** (when updating >2 existing concept pages in one ingest):

1. **Read all target pages in parallel** — one Read per file in a single message (different files, safe). Typical ingest touches 4–8 existing concept pages.
2. **Round 1 — frontmatter edits in parallel** — one Edit per file (different files, safe).
3. **Round 2 — content additions in parallel** — one Edit per file.
4. **Round 3 — `## Related Concepts` / `## Related Sources` extensions in parallel** — one Edit per file.

**Parallel Edits to the *same* file race and silently drop each other** (`pitfalls.md` #13). Parallelize *across files*, never *within* a file. If a single page needs frontmatter + content + Related Sources changes, apply them as **sequential Edit calls in separate messages**. `commit_ingest.py` emits `WARN: uncommitted changes remain after commit` when an edit was silently dropped.

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

**Concrete trigger examples** (from real ingests):

| Trigger | Example |
|:--------|:--------|
| 1 (new data point) | CoFi-Lite (Yang 2026) ingest added a row to the efficiency-frontier table in `deep-speech-enhancement.md` — (0.78M params, 0.6 GMACs, PESQ 2.92) was a new point on the existing params-vs-quality frontier. |
| 2 (gap-fill) | A future ingest of a PercepNet successor that adds ERB-scale-complexity numbers would fill a gap in the `multi-scale-speech-enhancement` comparison, which currently lacks that column for PercepNet-style models. |
| 3 (refine claim) | Zmolikova 2023 ingest refined `deep-speech-enhancement.md` Insight 8 — the review's framing of TSE as "internally solving identify + extract" sharpened the existing PSE/OVC complementarity claim, giving it a cleaner conceptual handle. |
| 4 (new axis) | A future ingest of a wave-RNN-based TSE paper would introduce "vocoder stage" as a new comparison axis in `multi-modal-speech-enhancement.md`, which currently tracks only clue type and fusion method. |

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

**Verify after updating indexes** (mandatory, one Grep call): confirm every new slug actually landed in both the main index and its subdirectory index. Long ingests can lose track of which entries were added — statistics alone do not prove the table rows exist (the Guldenschuh 2014 ingest had correct statistics but missing table rows, caught only by this check):

```
Grep pattern: "new-slug-1|new-slug-2|new-slug-3"
      path: wiki
      output_mode: content, -n: true
```

Each new slug must appear in **two** files: `wiki/index.md` and `wiki/{category}/index.md`. If a slug is missing from either, add the row before proceeding.

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

If the build fails, resolve broken links/missing pages before proceeding. Pre-existing `INFO` messages about `log.md` links and the Material "MkDocs 2.0" banner do not fail the build (`pitfalls.md` #8, #28). The check intentionally runs **without `--quiet`**: mkdocs's `--quiet` sets the log level to ERROR, which filters WARNING records before strict-mode's counter sees them — a `--quiet` build can exit 0 despite strict violations (observed in the Ke 2021 ingest). INFO-level nav lines in the output are normal.

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
- **Never put LaTeX math in a wikilink alias** — `[[concepts/foo|$\mathcal{L}$]]` breaks the `fix_obsidian_escapes` pipe-escaping and aborts `mkdocs build --strict` (`pitfalls.md` #44). Use a plain-text alias (`[[concepts/foo|Spectrally Adaptive Loss]]`) and keep the math outside the wikilink.
- **Todo list structure**: one todo per workflow step (1–13), in numerical order. Treat Steps 3a–3e as a single "extract content" todo. Treat Step 12a–12b as a single "build verification" todo. If Step 9 triage finds no candidates, mark that todo `completed` with "none relevant — grep triage" rather than leaving it `pending`.
