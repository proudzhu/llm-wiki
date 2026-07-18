# Common Pitfalls

Concrete lessons from prior ingests. Skim this list before starting an ingest and consult it when something unexpected happens.

1. **Brace glob on Windows fails silently** — `wiki/entities/{a,b,c}.md` returns "No file found" even when files exist. Use Grep with alternation or multiple parallel Globs (see "Checking Existing Pages" in SKILL.md).

2. **Citation discrepancies propagate** — Later papers often cite earlier work with wrong numbers (e.g., EchoFree 2025 cited Seidel 2024 with 1.62M params / 107 MMACs/s / 100 Bark bands, but the original reports 1.58M / 235M / 86). When ingesting the original paper, use its self-reported numbers and add a discrepancy note; update concept/synthesis pages that treated the later citation as ground truth (see `edge-cases.md` "Citation Discrepancies").

3. **Graphical results are not tables** — Do not transcribe numbers from bar charts or curves. Use qualitative labeled bullet points matching the paper's own discussion (see `edge-cases.md` "Graphical-Only Results").

4. **Entity updates are append-only** — When an author already has a page, append the new paper to `## Key Contributions` with a wikilink; do not rewrite existing bullets or change `created:` (see `page-templates.md` "Updating an existing entity page").

5. **Pick the PDF attachment, not HTML** — Zotero items from IEEE/ACM often have both. HTML attachments are cluttered with publisher chrome; always extract from `application/pdf`.

6. **MinerU figure filenames are deterministic hashes** — Do not guess filenames. Always `LS` the `figures/` directory after extraction to discover actual names before writing embed wikilinks.

7. **`update_indexes.py stats` is mandatory after `add`** — The `add` subcommand inserts rows but does not recompute the `## Statistics` section. Always run `stats` after all `add` calls (or use `batch --stats` which does both in one call), or `wiki/index.md` will show stale totals.

8. **Build hook INFO messages are not errors** — `mkdocs build --strict` may emit `INFO - Doc file 'log.md' contains an unrecognized relative link` for pre-existing issues in `log.md`. These do not fail the build (exit 0) and are not caused by your ingest; do not block on them.

9. **Synthesis pages are optional but high-value** — Not every paper warrants a synthesis update, but when a new paper is a key data point on an existing efficiency/architecture frontier (e.g., a new point on the AEC complexity-vs-quality Pareto curve), add it to the synthesis's sources table and write 1–2 sentences on what it contributes to the cross-source analysis. See SKILL.md Step 9's trigger checklist for the explicit criteria.

10. **Review papers' classifications can be loose** — A review may group cited methods under labels that don't quite fit (e.g., Mienye 2024 lists PercepNet — which is GRU-based — under "Echo State Network applications"). When ingesting a review, flag any such loose classifications in both the source page and the affected concept page. Do *not* propagate the loose classification as if it were the original paper's own claim. See `edge-cases.md` "Loose Classifications in Review Papers".

11. **Concept-page threshold prevents index bloat** — Resist creating pages for every term a paper mentions. Generic ML/DL primitives (Adam, ReLU, gradient clipping, dropout) do not warrant pages unless the paper makes a *contribution* to them. The Mienye 2024 ingest initially created pages for `adam-optimizer`, `activation-functions`, `gradient-clipping`, `neural-architecture-search` — these are borderline and should be promoted to wikilinks only when a future paper contributes a distinctive formulation of them. See `page-templates.md` "Concept-Page Threshold" for the explicit criteria.

12. **Batch the index updates** — For an ingest creating >3 pages, write a YAML manifest and use `update_indexes.py batch --manifest ... --stats` instead of chaining 10+ `add` calls. The Mienye 2024 ingest required 17 separate `add` calls; the batch subcommand collapses this to one.
