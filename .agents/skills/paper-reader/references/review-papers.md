# Review Papers (Special Variant)

Review/survey papers (e.g., "a comprehensive review of X") follow a different structure than novel-research papers. Adapt Step 4 (analysis) and Step 5 (source page) accordingly.

## Analysis Targets

Instead of methodology/results, extract:

- **Taxonomy** of methods/variants the review proposes
- **Comparison tables** across methods (with the review's own criteria)
- **Application domains** surveyed and per-domain "best variant" recommendations
- **Open challenges and future directions** explicitly identified by the review
- **Coverage gaps** — what the review does *not* cover (e.g., recent efficient variants published after the review's literature cutoff)

## Source-Page Required Sections

Replace the standard Problem Formulation / Experimental Setup / Results with:

- `## Summary` — 2-3 sentence overview of scope
- `## Taxonomy` — the review's categorization of methods
- `## Methodology` — for a review, this is the *surveyed* methods (not the review's own method)
- `## Applications Survey` — per-domain findings and "best variant" recommendations, ideally as a table
- `## Key Contributions` — the review's own synthesis contributions (taxonomy, dataset catalog, open challenges)
- `## Limitations and Caveats` — what the review does *not* cover (recent variants, non-quantitative "best" claims, etc.)
- `## Related Concepts` / `## Related Sources` — bidirectional wikilinks

## Figure Selection

Prefer **taxonomy/comparison diagrams** over per-method architecture diagrams — the review's added value is the comparison, not re-illustrating individual methods.

## Stricter Concept-Page Threshold

A review paper surveys many concepts by name; resist the urge to create a page for each. Only create pages for concepts the review itself contributes a distinctive taxonomy or synthesis of — not for every term it mentions. For terms the review only *defines* (textbook-style) without adding a new perspective, link to existing pages or leave as plain text.

See `pitfalls.md` entry on "Concept-page threshold prevents index bloat" for concrete examples of borderline concepts that should *not* get pages.
