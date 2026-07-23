# Review Papers (Special Variant)

Review/survey papers (e.g., "a comprehensive review of X") follow a different structure than novel-research papers. Adapt Step 4 (analysis) and Step 5 (source page) accordingly.

**Tutorial papers** (e.g., Härmä 2000 "Frequency-Warped Signal Processing for Audio Applications") are a special case: they survey methods AND teach them. Treat tutorials as reviews for structure (Taxonomy / Applications Survey / Limitations), but treat them as research papers for figure inclusion — include every figure that aids comprehension of a surveyed method or concept.

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
- `## Applications Survey` — per-domain findings and "best variant" recommendations, ideally as a table. For tutorials covering many application areas (e.g., 7 applications in Härmä 2000), structure as: a summary table first, then a dedicated `###` subsection per application with quantitative results and figure(s).
- `## Key Contributions` — the review's own synthesis contributions (taxonomy, dataset catalog, open challenges)
- `## Limitations and Caveats` — what the review does *not* cover (recent variants, non-quantitative "best" claims, etc.)
- `## Related Concepts` / `## Related Sources` — bidirectional wikilinks

## Figure Selection

- **Pure reviews/surveys**: Prefer **taxonomy/comparison diagrams** over per-method architecture diagrams — the review's added value is the comparison, not re-illustrating individual methods.
- **Tutorial papers**: Include every figure that aids comprehension of a surveyed method or concept (filter structures, phase responses, listening-test curves, equalization curves, etc.). A tutorial with 7 application areas may legitimately warrant 15–25 figures. See `page-templates.md` "Figure Usage" for the general criteria.

## Stricter Concept-Page Threshold

A review paper surveys many concepts by name; resist the urge to create a page for each. Only create pages for concepts the review itself contributes a distinctive taxonomy or synthesis of — not for every term it mentions. For terms the review only *defines* (textbook-style) without adding a new perspective, link to existing pages or leave as plain text.

**Tutorials are an exception**: a tutorial that introduces and formulates a concept distinctly (e.g., Härmä 2000's presentation of WIIR delay-free loop elimination, or WLP's automatic noise masking) warrants a concept page, even if the concept was originally proposed elsewhere — the tutorial's distinctive formulation is the contribution.

See `pitfalls.md` entry on "Concept-page threshold prevents index bloat" for concrete examples of borderline concepts that should *not* get pages.
