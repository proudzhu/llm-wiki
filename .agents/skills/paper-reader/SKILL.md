---
name: "paper-reader"
description: "Ingest one academic paper into the wiki end to end: locate it (Zotero, arXiv ID/URL, or a local PDF), extract full text and every figure, create the source page plus author and concept pages, update synthesis pages, indexes and log, then verify with mkdocs build --strict. Use when the user wants a paper added, processed, or re-ingested into the wiki regardless of source (Zotero library, arXiv link, PDF in Downloads). Trigger on \"ingest this paper\", \"add this arXiv paper to my wiki\", \"read this PDF into the wiki\", \"process this paper for the knowledge base\". Not for one-off summaries, questions answerable from existing pages, Zotero searching/listing, web articles, or non-academic PDFs."
---

# Paper Reader

Ingest one paper into the wiki: source page, entity pages, concept pages, synthesis updates, index rows,
log entry, build verification, commit. Scripts do the mechanical parts; Steps 4–9 carry the judgment.

## When to Run

Any phrasing that means "put this paper into the wiki":

- "ingest paper X from Zotero" / "re-ingest paper X" / "read paper X from Zotero"
- "add this arXiv paper to my wiki" — arXiv ID or URL, no Zotero (skip 1–2, go to 3b)
- "read this PDF into the wiki" — local PDF (3a then 3c)
- "process this paper for the knowledge base" / "update the wiki page for X's paper"

## When Not to Run

- **Page exists and is current** — Grep `wiki/log.md` and `wiki/sources/` for author/title first.
- **Quick summary only** — read the existing source page or abstract; an ingest is for analysis that creates pages.
- **Answerable from existing pages** — that is the Query Wiki workflow.
- **Web page / blog / informal HTML** — standard raw-article workflow. Exception: substantive non-academic PDFs
  (transcripts, slides) qualify — themed sections (Vision & Strategy / Q&A / Key Quotes), slug without a year
  (e.g. `liang-wenfeng-investor-exchange-meeting`).
- **Identical version already ingested** — re-ingest only when the PDF changed (camera-ready replaces preprint)
  or the page is materially incomplete.

The two cases below do **not** block an ingest — they only change the path:

- **Zotero down** (`curl -s http://localhost:23119/connector/ping`) — an arXiv ID goes to 3b, a local PDF to 3a + 3c.
- **Paper absent from Zotero** — skip 1–2; record the arXiv ID/DOI in frontmatter so the Zotero link is not invented.

## Hard Rules

1. **Never parallelize edits to the same file.** N edits to one file in one message race; last write wins and the
   others vanish *silently* (every call reports success). Parallelize **across** files, never within one.
   Multiple changes to one file = sequential edits. Prefer the scripts (`update_indexes.py`, `append_log.py`,
   `commit_ingest.py`) — they are race-free by construction. Re-applying a "lost" edit can duplicate content, so
   re-read the region first (`pitfalls.md` #13, #46).
2. **Run scripts blocking, never background + poll.** One foreground call with the tool timeout set to cover it
   (MinerU `--timeout` ≤ ~550 s). Polling intermediate state cannot distinguish "running" from "done" and wastes
   turns (`pitfalls.md` #57).
3. **Always `uv run python`**, never bare `python` (on this machine `python` is a Store stub that exits 9009).
   If `uv run` hangs for minutes, a stale `uv` holds the lock: `tasklist /FI "IMAGENAME eq uv.exe"`,
   `Stop-Process -Id <PID> -Force`, retry (`pitfalls.md` #18, #53).
4. **Scripts over hand-edits** for `wiki/index.md` and `wiki/log.md` — hand-edited index tables are the known
   cause of lost rows (`pitfalls.md` #35), and raw git bypasses `commit_ingest.py`'s guards (#48).
5. **Verify by filesystem, not by narrated success.** After any edit batch or index/log write, Grep for the new
   slug. A tool call reporting success is not evidence that the content landed.
6. **Resumed sessions: re-verify claims.** When the conversation continues from a summary, treat every "done" as
   unverified — Grep each page the summary says was edited for the new slug before Step 10 (`pitfalls.md` #49).

## Existence Checks (pages, figures)

- **Use `glob` with braces** — `wiki/entities/{a,b,c}.md` returns every match in one call (brace expansion works;
  `pitfalls.md` #1 is historical). `read` on a directory lists its entries.
- **Grep is a content search, never an existence check.** A page rarely contains its own slug (H1 is the display
  name → false "missing"), and `index.md` contains every slug (false "exists"). Use Grep only for "does any page
  mention X?" (`pitfalls.md` #43 supersedes #34).
- **Figure filenames** are 64-char hashes: Glob a hash prefix and copy the exact result, never type hashes from
  memory (`pitfalls.md` #20).

## Prerequisites

- Zotero running with "Allow other applications" enabled (**serial API — one Zotero call at a time**, #60)
- `mineru-open-api` CLI (`npm install -g mineru-open-api`; token: `mineru-open-api auth --show`)
- `defuddle` CLI (`npm install -g defuddle`) for arXiv HTML
- Run every script from the project root: `uv run python .agents/skills/paper-reader/scripts/<script>.py`

## Script Quick Reference

Prefix every command with `uv run python .agents/skills/paper-reader/scripts/`. In sessions resumed from a
summary, consult this table before a script's first call — summaries keep step order and lose CLI signatures
(`pitfalls.md` #50, #51); `--help` is one cheap call.

| Step | Command |
|------|---------|
| 1-2 | `zotero_fetch.py search "3-5 WORDS"` → `zotero_fetch.py metadata KEY` |
| 3a | `prepare_paper.py --slug SLUG --pdf-key PDF_KEY` |
| 3b | `extract_arxiv_html.py --arxiv-id ID --slug SLUG` (`--harvest-only` to repair an earlier extraction) |
| 3c | `extract_mineru.py --slug SLUG [--language en --model vlm --timeout 600 --pending-timeout 120]` |
| 3d | `extract_pdftotext.py --slug SLUG` |
| 3e | `map_figures.py --slug SLUG [--json]` |
| 6 | `update_entities.py --slug SLUG --entities first-author co-author1 [...] [--note "..."] [--role "First author of"]` |
| 9 | `triage_synthesis.py --slug SLUG` |
| 10 | `update_indexes.py source --slug SLUG` · `update_indexes.py add --category CAT --slug SLUG --display "..." --summary "..." --date YYYY-MM-DD` then `stats` · `update_indexes.py batch --manifest .tmp_ingest_manifest.yaml --stats` |
| 11 | `append_log.py --op ingest --title "..." --file .tmp_log_entry.md` (or `--body "..."`) — flags only |
| 12 | `verify_all.py --slug SLUG` (runs 12a→12b→12c fail-fast; preferred) |
| 12a-c | `verify_wikilinks.py --slug SLUG` · `check_backlinks.py --slug SLUG` · `build_check.py` |
| 13 | `commit_ingest.py --slug SLUG --message "ingest: Short Title (Author Year)" --entities ... --concepts ... --synthesis ...` |

**Self-tests** (offline, no network; run after editing this skill):

```bash
uv run python .agents/skills/paper-reader/scripts/test_skill_docs.py    # doc/CLI drift: flags, refs, pitfall numbers, step refs
uv run python .agents/skills/paper-reader/scripts/test_vector_figures.py # SVG harvest, after touching extract_arxiv_html.py
```

## References (load on demand)

| Reference | When to load |
|-----------|--------------|
| [`references/review-papers.md`](references/review-papers.md) | **First** — if the paper is a review/survey/tutorial. Routes Steps 4–7. |
| [`references/page-templates.md`](references/page-templates.md) | Steps 5–7 — templates, figure criteria, NN documentation rules, concept threshold |
| [`references/edge-cases.md`](references/edge-cases.md) | Step 4 — graphical-only results, citation discrepancies, loose review classifications |
| [`references/pitfalls.md`](references/pitfalls.md) | When something unexpected happens (starts with a symptom index) |

## Review/Survey Routing

Detect on any strong signal (load `review-papers.md` on the first match): title contains survey / overview /
review / comprehensive / taxonomy / tutorial / primer; abstract says "we survey" / "this paper reviews"; venue is a
magazine (IEEE SPM, IEEE Comms. Surveys & Tutorials, ACM Comput. Surv.); the main contribution is a
taxonomy/comparison table rather than one method; 60+ references.

| Step | Research paper | Review/survey |
|:-----|:---------------|:--------------|
| 4 | problem, contributions, methodology, setup, results | taxonomy, comparison tables, application domains, open challenges, coverage gaps |
| 5 | Summary / Problem Formulation / Methodology / Experimental Setup / Results | Summary / Taxonomy / Methodology (surveyed) / Applications Survey / Key Contributions / Limitations and Caveats |
| 5 figures | block diagrams, architectures, result plots | taxonomy/comparison diagrams over per-method architectures |
| 7 concepts | pages for methods/losses/architectures the paper introduces | **stricter** — only concepts the review contributes a distinctive taxonomy or synthesis of |
| 8 concepts | add source, extend with findings | same, but the contribution is the taxonomy/comparison |
| 9 synthesis | new data point / gap-fill / refutation / new axis | same; reviews often *refine* an existing claim (trigger 3) |

**Tutorials**: review structure, research-paper figure inclusion — every figure that aids comprehension of a
surveyed method (7 application areas ⇒ 15–25 figures is legitimate).

## Workflow

### Step 1-2: Search Zotero & Fetch Metadata

```bash
uv run python .agents/skills/paper-reader/scripts/zotero_fetch.py search "SEARCH_TERMS"
uv run python .agents/skills/paper-reader/scripts/zotero_fetch.py metadata ZOTERO_KEY
```

Note the **Zotero item key** and the **PDF attachment key**. Keep queries to 3–5 distinctive words — a full title
times out (#45). Issue Zotero calls **one at a time**; the local API serves serially and concurrent calls all
time out (#60). Pick the `application/pdf` attachment, never the HTML one saved alongside it (#5). No Zotero entry
but an arXiv ID? Record the ID and go to 3b.

### Step 3: Extract Paper Content

Priority: **arXiv HTML > MinerU > pdftotext/pypdf**. Every script deletes `paper.pdf` after extraction.

#### 3a. Prepare directory & copy PDF (skip for arXiv HTML)

```bash
uv run python .agents/skills/paper-reader/scripts/prepare_paper.py --slug SLUG --pdf-key PDF_KEY
```

Slug format: `author-year-short-title` (lowercase, hyphenated).

#### 3b. arXiv HTML (preferred for arXiv papers)

```bash
uv run python .agents/skills/paper-reader/scripts/extract_arxiv_html.py --arxiv-id ARXIV_ID --slug SLUG
```

Auto-creates `raw/papers/{slug}/`; exits 2 (→ 3a + 3c) if the HTML 404s or `defuddle` is missing.
**Vector figures are recovered automatically** — arXiv serves plots as `<object type="image/svg+xml">` and
defuddle serializes only `<img>`, so every SVG would vanish silently. The script harvests them and inserts each
embed under its own `Fig. N` caption. Confirm `Recovered vector figure: …` lines plus `Figures: N in …`, then check
`map_figures.py` shows every caption with an image. A caption still lacking an image means the figure is text-only
or lives behind a `<table>` — inspect before assuming loss (#68).

Repair an extraction from before this existed with `--harvest-only`: keeps `full-text.md` byte-for-byte (only
inserts the missing embeds), so cited text is not swapped for a different arXiv version.

#### 3c. MinerU (non-arXiv or arXiv fallback)

```bash
uv run python .agents/skills/paper-reader/scripts/extract_mineru.py --slug SLUG [--language en --model vlm --timeout 550 --pending-timeout 120]
```

- `--model vlm` (default) or `pipeline` (zero-hallucination); token required.
- **Blocking foreground call**, with the tool timeout set comfortably above `--timeout` (default 600 s) — Hard Rule 2.
- **Built-in early abort**: streams `mineru-open-api extract -v` and a watchdog polls the batch API, killing the CLI
  on a fatal `Error:`, server state `failed`, a batch queued (`pending`/`waiting-file`) past `--pending-timeout`
  (the queue silently drops batches — one cost a 540 s blind wait), or the overall timeout (#58). On a
  stuck-`pending` abort, re-run once, then fall back to 3d.
- **Language codes are MinerU's, not ISO 639**: `ch` (Chinese), `en`, `chinese_cht`, `japan`, `korean`, `latin`,
  `arabic`, `cyrillic`, `east_slavic`, `devanagari`, `ta`/`te`/`ka`. `zh` is invalid (#23).
- Verify quality: read the first 200 and last 100 lines. Mermaid blocks for diagrams are normal.

#### 3d. pdftotext / pypdf fallback (plain text, no images)

```bash
uv run python .agents/skills/paper-reader/scripts/extract_pdftotext.py --slug SLUG
```

Uses poppler `pdftotext` when present, **automatically falls back to `pypdf`** (no poppler on this machine, #47).
Output is `full-text.txt` — no figures, no `map_figures.py` step, and the source page frontmatter cites the `.txt`
(43 papers in the vault were produced this way). A custom extraction script must still write the text into
`raw/papers/{slug}/` and **delete `paper.pdf`** — `commit_ingest.py` refuses to stage the PDF, but a manual
`git add` would (#48).

#### 3e. Map figures to captions (after 3b or 3c)

```bash
uv run python .agents/skills/paper-reader/scripts/map_figures.py --slug SLUG
```

Pairs each hash-named crop and recovered `.svg` with its `Fig. N` caption, prints dimensions, flags axis/colorbar
strips, exits 2 on referenced-but-missing hashes (#25). With no caption lines it falls back to the first in-text
"Fig. N" reference (heuristic — check multi-panel figures against the sub-labels it prints, #32). An empty image
list under a caption after arXiv extraction means a lost figure, not an absent one (#68).

### Step 4: Read and Analyze

Read in chunks (head 200 + tail 100 + targeted ranges). Extract: problem/motivation, numbered contributions,
methodology (architecture, algorithms, losses, equations), experimental setup (datasets, metrics,
hyperparameters), quantitative results, concepts warranting pages, authors warranting pages.

**Neural-network papers** (DNN/RNN/CNN/transformer/vocoder, hybrid DSP+DNN included): additionally the model
architecture (layer-by-layer with sizes), input features (representation, frame rate, window), outputs (what, at
what rate), and training losses (equations with coefficients). These feed the mandatory section in Step 5.

**Review/survey**: use the analysis targets in `review-papers.md` instead.

**MinerU numeric sign check**: MinerU silently drops minus signs on negatives (a −5…10 dB SNR sweep extracted as
"5 dB to 10 dB"). Suspicious: a dB sweep that appears to start positive, or a value list with a repeated entry
after a sign flip. Cross-check against the publisher page or PDF (#42).

**On** graphical-only results, citation discrepancies, loose review classifications, or cross-references to
already-ingested papers: load `references/edge-cases.md`.

### Step 5: Create/Update Source Page

Create `wiki/sources/{slug}.md`. Load `references/page-templates.md` for frontmatter, required sections
(Summary / Problem Formulation / Methodology / Experimental Setup / Results / Key Contributions / Related Concepts
/ Related Synthesis), figure criteria, and filename verification. H1 is `Author1, Author2 & Author3 Year: Short Title`.

**NN papers**: MUST add `### Model Structure, Inputs, and Outputs` (mermaid data-flow diagram + per-network spec
tables: structure / inputs / outputs / training data / role) and `### Training Losses` (total objective + per-term
equations with coefficients, and which network each trains) — citing "see Fig. 2" is not enough (#39). Mermaid
renders only because `mkdocs.yml` has superfences `custom_fences`; without it the build *passes* and shows code
(#38).

**Review/survey**: use the review template in `review-papers.md`.

**Figure embeds**: `![[raw/papers/{slug}/figures/HASH.jpg|caption]]` — never markdown `![alt](path)` (#27). One
embed per (a)/(b) crop above the shared `*Figure N: …*` caption (#26). Embed only files that are referenced in
`full-text.md` **and** paired with a caption or in-text reference — axis strips and stray crops are noise (#33).
**No hard cap on figure count** — include what aids comprehension; skip decoration.

Re-ingestion: overwrite the source page with updated comprehensive content.

**Immediately after writing the source page, collect every `[[concepts/...]]` link in it** (Related Concepts and
body) and union that set into the Step 8 update targets. Those links define the minimum backlink set; a concept
that never gains a reciprocal reference fails Step 12b and costs a full verify cycle (#64).

### Step 6: Create or Update Entity Pages

New authors: create `wiki/entities/{firstname-lastname}.md` from the template in `page-templates.md`.

Existing authors: **append-only** — update `updated:`, append a bullet to the contributions section, never touch
`created:` or rewrite existing bullets (#4). Quote paper titles in bullets: `- Co-authored "Short Title" (Venue
Year) — [[sources/{slug}|Author Year]]`; `[Text] (Parenthesized)` parses as a broken markdown link (#19).

**Use the script** for existing authors — it applies the append-only pattern idempotently across all listed pages:

```bash
uv run python .agents/skills/paper-reader/scripts/update_entities.py \
    --slug SLUG --entities first-author co-author1 co-author2 \
    [--note "contribution description"] [--role "First author of"]
```

- **List the first author first**: `--role` applies to the first listed entity only, the rest get "Co-author of"
  (#61); for co-first-author papers use the default role and hand-polish the wording.
- It derives title/venue/year from the source page's H1 and `**Venue**:` line and abbreviates known conferences via
  the `KNOWN_CONFERENCE_ABBRS` whitelist (#62) — check the printed `-> bullets will use:` line and add a missing
  acronym there. Journals and unknown venues pass through verbatim. Duplicate years are de-duplicated (#59).
- It handles all three contribution layouts: `## Key/Notable Contributions`, a `**Key Contributions**:` bold label
  (#56), and `## Research Contributions` with `### N.` subsections — the last gets a new numbered subsection titled
  after the paper, which you then polish into a short topical title (#65).
- Review the appended bullets and polish wording with one sequential edit per file (`--note` covers it at insert
  time). New-author pages are still hand-written.

### Step 7: Create Missing Concept Pages

For each key concept linked from the source page without a page, create `wiki/concepts/{concept-name}.md` from
`page-templates.md`, subject to the **concept threshold** (novelty / distinctive formulation / central to the
contribution). Generic primitives (Adam, ReLU, dropout, gradient clipping) and off-the-shelf named algorithms are
plain text. **Reviews**: stricter threshold — see `review-papers.md`. When in doubt, plain text; promoting a
mention later is cheaper than maintaining a stub (#11).

Existence check: one `glob` with braces over the candidate slugs (§ Existence Checks).

### Step 8: Update Existing Concept Pages

For each existing concept page touched by this paper: add the paper to frontmatter `sources:`, bump `updated:`, add
findings, extend `## Related Concepts` / `## Related Sources`. Targets = (Step 7 candidates that already exist) ∪
(every `[[concepts/...]]` link in the new source page, #64).

Batched pattern for >2 pages:

1. Read all targets — one Read per file, parallel (different files: safe).
2. Frontmatter round — one Edit per file, parallel. Build each `old_string` **verbatim from that file's own Read**:
   key order varies (`tags:` before `sources:` on some pages), so never reconstruct from the template (#63).
3. Content round — one Edit per file.
4. Related Concepts/Sources round — one Edit per file.

A page needing all three gets **sequential edits in separate messages** (Hard Rule 1). `commit_ingest.py` prints
`WARN: uncommitted changes remain after commit` when an edit was silently dropped — investigate it.

### Step 9: Update Synthesis Pages

Triage first; it needs the source page (Step 5) to exist:

```bash
uv run python .agents/skills/paper-reader/scripts/triage_synthesis.py --slug SLUG
```

- **No matches** → skip the step (common for single-method papers).
- **`Shared tags (1): <broad topic>`** (`speech-enhancement`, `beamforming`, `signal-processing`, …) → skip without
  reading; topical coincidence. Read only if N ≥ 2, or N = 1 with a contribution-specific tag (`lpcnet`,
  `packet-loss-concealment`) (#30).
- **Survivors** → read, then update only if a trigger fires: (1) new data point on an existing frontier,
  (2) fills a gap in a comparison, (3) refutes or refines a claim, (4) introduces a new axis.

| Trigger | Example |
|:--------|:--------|
| 1 new data point | CoFi-Lite (Yang 2026) added (0.78 M params, 0.6 GMACs, PESQ 2.92) to the efficiency frontier in `deep-speech-enhancement.md`. |
| 2 gap-fill | A PercepNet successor reporting ERB-scale complexity would fill the missing column in `multi-scale-speech-enhancement`. |
| 3 refine claim | Zmolikova 2023 sharpened Insight 8's framing of TSE as "identify + extract inside one model". |
| 4 new axis | A wave-RNN TSE paper would add "vocoder stage" as an axis to `multi-modal-speech-enhancement`. |

**When in doubt, skip.** If you cannot write one substantive sentence about what the paper contributes to the
cross-source analysis, there is nothing to add.

Applying an update is typically 4–6 edits to one file (frontmatter `sources:` + `updated:`, `tags:`, Sources
Synthesized row, insight paragraph, maybe a takeaway) — **sequential, one per message** (#13).

**Verify, mandatory**: after the last edit, Grep the file for the new slug and confirm it appears in both the
frontmatter `sources:` list and the Sources Synthesized row. The frontmatter edit is the one most often lost — it
is first and invisible in the rendered page (#49).

### Step 10: Update Indexes

Never hand-edit index tables for new rows (lost-row history, #35); hand-edits are fine only for *modifying* an
existing row's summary/date.

Source row — derives display from the H1, summary from the first sentence of `## Summary`, date from `created:`,
then runs `stats` (no `add`-then-forget-`stats` hazard, #7):

```bash
uv run python .agents/skills/paper-reader/scripts/update_indexes.py source --slug SLUG
```

Review the printed `Derived:` line; `--summary "..."` overrides a long or vague first sentence.

Entity/concept rows — `add` then `stats`, or one `batch` call with a YAML manifest (preferred for a typical ingest
creating 2–4 entities + 5–15 concepts):

```yaml
# .tmp_ingest_manifest.yaml
entries:
  - category: concepts
    slug: author-year-short-title
    display: "Author Year: Short Title"
    summary: "One-line summary"
    date: YYYY-MM-DD
```

```bash
uv run python .agents/skills/paper-reader/scripts/update_indexes.py batch --manifest .tmp_ingest_manifest.yaml --stats
```

**Verify (mandatory, one Grep)**: each new slug must appear in **two** files — `wiki/index.md` and
`wiki/{category}/index.md`. Correct statistics do not prove the rows exist (Guldenschuh 2014, #35).

```bash
uv run python .agents/skills/wiki-lint/scripts/check_statistics.py   # exit 0 = counts match files
```

### Step 11: Update Log

Write the body to a temp file, then append:

```bash
uv run python .agents/skills/paper-reader/scripts/append_log.py --op ingest \
    --title "Paper Title (Author Year)" --file .tmp_log_entry.md
```

Flags only — `--op`, `--title`, one of `--body`/`--file`/`--stdin`; positionals exit 2 (#50). Short entries can use
`--body "..."`. A re-ingest (camera-ready replacing a preprint) adds `--re`, which renders as `ingest (re)`.

Body format:

```markdown
- **Source**: `raw/papers/{slug}/full-text.md` (`.txt` when extracted via 3d) (Zotero: KEY)
- **Authors**: Author1, Author2, ...
- **Published**: Venue Year, pp. XXX–XXX
- **DOI**: 10.xxxx/xxxxx
- **Summary**: One-line summary
- **Pages created**: each new file path
- **Pages updated**: each modified file with a short note
```

**Link format**: vault-absolute wikilinks (`[[sources/slug|Title]]`) or backticked plain paths
(`wiki/sources/slug.md`). Never `[Title](../sources/slug.md)` — `../` escapes the docs root from `wiki/log.md` and
aborts the strict build; the script rejects such bodies (exit 2) (#40).

### Step 12: Build Verification

```bash
uv run python .agents/skills/paper-reader/scripts/verify_all.py --slug SLUG
```

Runs 12a → 12b → 12c fail-fast and reports once — one blocking call instead of three, and the build alone is
60–130 s. On failure, fix and re-run; the individual checks remain available for targeted re-checks.

**12a — Wikilinks** (`verify_wikilinks.py --slug SLUG`): resolves `[[category/slug]]` and `![[raw/...]]` embeds
against the filesystem for the source page plus every modified wiki file, and flags `$…$` in alias text, which
mangles the pipe-escaping and aborts the build (#44). Catches hash typos and broken link targets before the build
cycle. Fix by creating the page, correcting the slug, or dropping to plain text; for embeds, Glob the hash prefix.

Do not substitute wiki-lint's `check_broken_links.py`: vault-wide, it reports hundreds of pre-existing convention
violations and drowns the ingest's signal.

**12b — Backlinks** (`check_backlinks.py --slug SLUG`): every concept/synthesis page the source links must reference
it back (frontmatter `sources:`, body wikilink, or `## Related Sources`). Flagged only when the target already
reciprocates ≥50% of its in-linkers and shares a distinctive tag. Apply the Step 8 pattern, re-run until clean;
prevention is Step 5's link union (#64).

**12c — MkDocs strict** (`build_check.py`): wraps `mkdocs build --strict` and writes a freshness marker that
`commit_ingest.py` uses to skip a redundant pre-commit build. Never re-add `--quiet`: it raises the log level to
ERROR, filters WARNING records, and a strict build can then exit 0 despite violations (#41). INFO lines about
`log.md` links and the Material "MkDocs 2.0" banner are normal (#8, #28).

### Step 13: Commit

```bash
uv run python .agents/skills/paper-reader/scripts/commit_ingest.py \
    --slug SLUG --message "ingest: Short Title (Author Year)" \
    --entities author1 author2 --concepts concept1 concept2 --synthesis synth1
```

Stages `raw/papers/{slug}/`, the source page, all index files, `wiki/log.md`, and the listed pages; refuses to stage
`paper.pdf`; auto-stages any other modified `wiki/` file (catches Step 8 edits) unless `--strict`. `--no-verify`
only for pre-commit hook environment problems unrelated to the change.

If 12c passed within the last hour and no build input changed since, the script commits with `--no-verify` itself
and prints a `NOTE:`. That skip matters only when the strict-build hook is installed
(`git config core.hooksPath .githooks`, whose `pre-commit` runs `uv run mkdocs build --strict`); with no hook
configured the flag is inert. Post-commit `WARN: uncommitted changes remain` listing only `.obsidian/*` is expected;
investigate if a `wiki/` or `raw/` path appears.

## Important Notes

- **`raw/` immutability exception**: replacing remote image URLs with local paths in `full-text.md` is allowed.
- **No `\bm{}` in LaTeX** — MathJax lacks the package; use `\mathbf{x}` / `\boldsymbol{x}`.
- **No LaTeX in wikilink aliases** — `[[concepts/foo|$\mathcal{L}$]]` breaks pipe-escaping and aborts the strict
  build (#44); use a plain-text alias and keep math outside.
- **Never raw `git add`/`git commit` for an ingest** — it loses `commit_ingest.py`'s guards (PDF staging,
  auto-staged cross-references, `.obsidian/` scoping). If a manual commit is truly unavoidable: exclude
  `paper.pdf` and `.obsidian/`, and pass the message with `git commit -F <file>`.
- **New pages may be written with LF while the vault is mostly CRLF** — harmless for MkDocs and git; do not rewrite
  whole files to normalize it.
- **Todo list**: one item per workflow step (1–13) in order; 3a–3e collapse into "extract content" and 12a–12c into
  "build verification". When Step 9 triage finds nothing, complete that item with "none relevant — triage" rather
  than leaving it pending.
