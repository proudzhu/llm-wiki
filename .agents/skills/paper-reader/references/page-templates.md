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

### Figure Usage

| Include figure? | Criteria | Examples |
|-----------------|----------|----------|
| Include | Visual is essential to understand the core problem or method | System block diagram, network architecture, problem illustration |
| Skip | Data is already well-summarized in text or tables | Performance curves, spectrogram plots, convergence plots |

Guidelines:

- Place figures immediately after the section they illustrate.
- Use vault-absolute embed wikilink paths: `![[raw/papers/{slug}/figures/ACTUAL_FILENAME.ext|caption]]`.
- **List the `figures/` directory first** to discover actual filenames — MinerU produces hash-named `.jpg` files, arXiv HTML figures are named `fig1.png`.
- Add an italicized caption below each figure: `*Figure N: description.*`
- Maximum 3 figures per source page — prefer the most informative ones.
- When adding figures, also update corresponding concept pages with the same figure if it illustrates a key concept.

For re-ingestion: overwrite the existing source page with updated comprehensive content.

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
2. Append the new paper to `## Key Contributions` as a new bullet, with a wikilink to the new source page: `- Co-authored [short title] (Venue Year) — [[sources/{slug}|Author Year]]`
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

**Do NOT create concept pages for** generic prerequisites the paper merely *uses* without contribution — e.g., "Adam optimizer", "activation functions", "gradient clipping", "ReLU", "dropout", "batch normalization". Link these as **plain text** in the source page instead. Creating pages for generic ML/DL primitives leads to index bloat and dilutes the wiki's focus on the project's domain (acoustic echo cancellation, speech enhancement, sequence modeling).

**Stricter threshold for review papers**: see `review-papers.md`.

**When in doubt**: prefer plain text over a new page. It is much cheaper to promote a plain-text mention to a wikilink later (when another paper contributes to the concept) than to maintain a thin stub page that adds no value.
