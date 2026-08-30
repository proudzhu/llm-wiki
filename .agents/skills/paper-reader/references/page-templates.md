# Page Templates and Thresholds

Templates for pages created during Step 5 (source), Step 6 (entities), and Step 7 (concepts). The main SKILL.md has the workflow; this file has the full templates and the concept-page threshold rules.

## Source Page (`wiki/sources/{slug}.md`)

### Frontmatter

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

### Required Sections

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

### Section Quality Examples

Concrete examples of what a good vs. thin section looks like (drawn from real ingests):

**`## Summary` (good — 2-3 sentences, captures the contribution):**
> This paper presents an in-depth overview of recent neural-based approaches to target speech/speaker extraction (TSE), the task of isolating a target speaker's speech from a mixture using auxiliary clues. The review unifies the field by introducing a single general neural TSE framework and showing how audio, visual, and spatial clue variants instantiate it.

**`## Methodology` (good — equations + prose, not just a list):**
> A neural TSE system consists of two main modules. The clue encoder converts the raw clue $\mathbf{C}_{s}$ into embeddings $\mathbf{E}_{s} = \mathrm{ClueEncoder}(\mathbf{C}_{s})$. The speech extraction module decomposes as $\mathbf{Z}_{y} = \mathrm{MixEncoder}(\mathbf{y})$, $\mathbf{Z}_{s} = \mathrm{Fusion}(\mathbf{Z}_{y}, \mathbf{E}_{s})$, $\hat{\mathbf{x}}_{s} = \mathrm{TgtExtractor}(\mathbf{Z}_{s}, \mathbf{y})$.

**`## Methodology` (thin — list only, no equations or reasoning):**
> The system uses a clue encoder, a mixture encoder, a fusion layer, and a target extractor. See Figure 3.

**`## Key Contributions` (good — numbered, specific, falsifiable):**
> 1. **Unified framework**: introduces the general neural TSE framework (clue encoder + mixture encoder + fusion layer + target extractor) that subsumes audio, visual, and spatial clue variants under a single description.
> 2. **Fusion layer survey**: tabulates five widely used fusion layers with equations and parameter counts, and reports empirically that the choice has "rather insignificant" impact.

**`## Key Contributions` (thin — vague, non-falsifiable):**
> 1. We propose a comprehensive review of TSE.
> 2. We compare various methods.

### Figure Usage

| Include figure? | Criteria | Examples |
|-----------------|----------|----------|
| Include | Visual is essential to understand the core problem, method, or results | System block diagram, network architecture, frequency response, listening-test curves, problem illustration |
| Skip | Data is already well-summarized in text or tables, or the figure is purely decorative | Performance curves with numbers already in a table, stock photos |

Guidelines:

- Place figures immediately after the section they illustrate.
- **Use embed wikilinks, NOT markdown image syntax.** Write `![[raw/papers/{slug}/figures/ACTUAL_FILENAME.ext|caption]]` — never `![alt](path)` — because markdown image paths resolve incorrectly in Obsidian and break the vault-absolute convention. A stray `![...](...)` figure line is a convention violation and will surface in `mkdocs build --strict`.
- **Run `scripts/map_figures.py --slug {slug}` FIRST** (Step 4a) to map hash-named crops to "Fig. N." captions in one call. MinerU splits multi-panel figures into several files and sometimes extracts axis/colorbar strips it never references; the script lists each caption's images with line numbers and dimensions, flags unreferenced strips, and errors (exit 2) on referenced-but-missing hashes. Copy filenames verbatim from its output.
- **Verify each filename exists** before writing the embed wikilink — a single-character typo in a hash filename will cause a build failure. Use Glob with a partial hash prefix (e.g., `raw/papers/{slug}/figures/3c0491873b*`) or `map_figures.py` output to confirm the exact filename.
- **Multi-panel figures**: MinerU extracts each panel as a separate file. When a figure has (a)/(b)/(c) sub-labels, embed each panel file separately with its own caption line (e.g., `(a) ...` / `(b) ...`) above the shared `*Figure N: ...*` caption — do not embed one cropped panel as a stand-in for the whole figure.
- Add an italicized caption below each figure: `*Figure N: description.*`
- **No hard cap on figure count** — include every figure that adds substantive value. Tutorial and survey papers may legitimately warrant 15–25 figures (one per surveyed concept/application); research papers typically warrant 3–8. Use judgment: include figures that aid comprehension, skip those that merely decorate.
- When adding figures, also update corresponding concept pages with the same figure if it illustrates a key concept.

For re-ingestion: overwrite the existing source page with updated comprehensive content.

## Neural-Network Model Documentation (mandatory for NN papers)

Applies whenever the paper's method includes a neural network (DNN/RNN/CNN/transformer/vocoder, hybrid DSP+DNN systems included). The source page must document **what the model is** (architecture), **what goes in and out** (features/samples at their actual rates), and **how it was trained** (losses) — not just cite the paper's figure. A reader should be able to re-implement the data flow from the source page alone.

### Required sections (inside `## Methodology`)

1. **`### Model Structure, Inputs, and Outputs`** — a mermaid block diagram of the full data flow, followed by one spec table per network, covering:
   - **Structure** — layer-by-layer (layer types, widths, activation/GRU/LSTM unit counts, sparsity/density if stated)
   - **Input** — exact feature representation (e.g., "18 BFCCs + pitch period + pitch correlation at 100 Hz"), frame rate, window/hop length, any conditioning or flags
   - **Output** — what the network produces and at what rate (e.g., "16 kHz samples — the middle 10 ms of each 20-ms window")
   - **Training data** — hours, corpora, speakers/languages
   - **Role** — one sentence on the network's function in the system (this is what disambiguates multi-network pipelines)
2. **`### Training Losses`** — the total objective and each loss term with equations and coefficient values; note which network(s) each loss trains and why the form was chosen (e.g., $L_{1}$ over $L_{2}$ for label-noise robustness). If the paper uses a single standard loss (plain cross-entropy), one sentence suffices — but state it explicitly.

For multi-network pipelines (e.g., predictive model + generative vocoder), also state whether the networks are trained **jointly or separately**, and in what order.

### Mermaid diagram rules

- Use `flowchart TB` (top-to-bottom) by default; one subgraph per network; label edges that carry non-obvious payloads (feature vectors, feedback loops).
- **Prerequisite**: `mkdocs.yml` must configure superfences `custom_fences` (already in place in this repo — verified in the Valin 2022 session):

  ```yaml
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  ```

  Without it, `mkdocs build --strict` **passes** but the diagram renders as a plain syntax-highlighted code block — a silent failure. Obsidian renders ```mermaid blocks natively with no configuration.
- **Syntax constraints** (both renderers, Obsidian uses mermaid v11):
  - Quote all node labels containing parentheses, `/`, `+`, `→`, or commas: `V2["Sample-rate network (GRU-A: 640 units)"]`.
  - Use `<br/>` for line breaks inside labels; `\n` is NOT rendered.
  - Self-loops (`V2 --> V2`) and edge labels (`A -->|"caption"| B`) are supported.
  - Subgraph titles with spaces are fine: `subgraph RNN["Feature prediction RNN"]`.
  - Do not use `%%` comments on the same line as a statement.
- The diagram should show **data flow at inference** (inputs → networks → outputs), including feedback loops and any bypass paths (e.g., known features bypassing a predictor). Keep it faithful to the paper — do not invent blocks the paper does not describe.
- Mermaid is a **supplement, not a substitute**: the spec tables carry the precise numbers; the diagram carries the topology. Include both.

### Worked example

See `wiki/sources/valin-2022-real-time-plc.md` (added 2026-08-30): a two-network pipeline (feature-prediction RNN + LPCNet vocoder) documented with a `flowchart TB` diagram showing input features → RNN subgraph → predicted-feature edge → LPCNet subgraph → autoregressive feedback self-loop → output samples, followed by per-network spec tables and the three perceptual losses ($\mathcal{L}_{s}+\mathcal{L}_{p}+\mathcal{L}_{c}$).

## Entity Page (`wiki/entities/{firstname-lastname}.md`)

### Template (new author)

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

### Updating an existing entity page

When the author already has a page, make these specific edits (do not rewrite the page):

1. Update `updated:` date in frontmatter to today.
2. Append the new paper to `## Key Contributions` as a new bullet, with a wikilink to the new source page. **Use quotes around the paper title** to avoid MkDocs interpreting `[title](venue)` as a broken markdown link:
   ```
   - Co-authored "Short Title" (Venue Year) — [[sources/{slug}|Author Year]]
   ```
   Do **not** write `- Co-authored [Short Title] (Venue Year)` — MkDocs parses `[text](parenthesized)` as a markdown link and the build will fail with "target not found".
3. If the new paper reveals a new affiliation, research focus area, or tag not already on the page, add it (do not replace existing content).
4. If the new paper is the author's primary contribution (more important than prior listed work), consider moving it to the top of the list — but otherwise preserve chronological/listed order.
5. Do **not** touch the `created:` date or rewrite existing bullets.

## Concept Page (`wiki/concepts/{concept-name}.md`)

### Template

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

### Concept-Page Threshold (avoid index bloat)

**Only create a concept page if at least one of these holds:**

1. **Novelty** — the concept is introduced or named by this paper (e.g., "PercepNet", "Bark-AEC", "Grouped RNN" as a named architecture).
2. **Distinctive formulation** — the paper provides a distinctive formulation, extension, or survey of the concept that adds value beyond a textbook definition (e.g., a paper that proposes a new loss function warrants a page for that loss; a paper that *uses* cross-entropy does not).
3. **Central to the contribution** — the concept is a core building block of the paper's contribution and is referenced repeatedly (e.g., "ERB scale" for PercepNet, "complex compressed MSE" for Bark-AEC).

**Do NOT create concept pages for** generic prerequisites the paper merely *uses* without contribution — e.g., "Adam optimizer", "activation functions", "gradient clipping", "ReLU", "dropout", "batch normalization". The same applies to **named-but-generic signal-processing algorithms** the paper adopts off-the-shelf — e.g., "Leaky LMS", "gradient descent", "FxLMS", "Gauss-Newton", "RLS", "Welch's method". A named algorithm is not by itself a contribution; promote it to a wikilink only when a paper *modifies, extends, or surveys* it distinctively. Concrete example from the Gil-Cacho 2009 ingest: the [[concepts/regularized-adaptive-notch-filter|RANF]] method gets a page because it *introduces* signed regularization as a howling-detection mechanism; "Leaky LMS", which RANF merely *borrows* as its update rule, stays plain text. Link these as **plain text** in the source page instead. Creating pages for generic ML/DSP primitives leads to index bloat and dilutes the wiki's focus on the project's domain (acoustic echo cancellation, speech enhancement, sequence modeling).

**Stricter threshold for review papers**: see `review-papers.md`.

**Concrete examples** (from real ingests):

| Concept | Decision | Reason |
|:--------|:---------|:------|
| [[concepts/ranf\|RANF]] (Gil-Cacho 2009) | **Create** | Novelty — introduces signed regularization as a howling-detection mechanism. |
| "Leaky LMS" (Gil-Cacho 2009) | **Skip** (plain text) | Generic — RANF borrows it as its update rule; no distinctive formulation. |
| [[concepts/cocktail-party-problem\|Cocktail-Party Problem]] (Zmolikova 2023) | **Create** | Distinctive formulation — review contributes the engineering framing (TSE as the response that mirrors human selective hearing); not just a mention. |
| [[concepts/angle-feature\|Angle Feature]] (Zmolikova 2023) | **Create** | Central + distinctive — review surveys the TPD-vs-IPD cosine formulation with equations; central to spatial-clue TSE. |
| "i-vector" (Zmolikova 2023) | **Skip** (plain text) | Mentioned as one of three audio-clue encoder families, but the review does not contribute a distinctive formulation of i-vectors — it cites the standard speaker-verification formulation. |
| "d-vector" / "x-vector" (Zmolikova 2023) | **Skip** (plain text) | Same as i-vector — surveyed but not distinctively formulated by the review. [[concepts/speaker-embedding\|Speaker Embedding]] already exists as the umbrella page. |
| [[concepts/target-speaker-vad\|TS-VAD]] (Zmolikova 2023) | **Create** | Distinctive + central — review contributes the framing of TS-VAD as the activity-detection analog of TSE, plus the multi-target diarization extension. |
| [[concepts/film-layer\|FiLM Layer]] (existing, updated) | **Update, not create** | Page already exists from earlier ingest; review adds the fusion-layer survey table, so update rather than create. |

**When in doubt**: prefer plain text over a new page. It is much cheaper to promote a plain-text mention to a wikilink later (when another paper contributes to the concept) than to maintain a thin stub page that adds no value.
