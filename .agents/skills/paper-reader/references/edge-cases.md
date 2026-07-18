# Edge Cases During Paper Analysis

Load this reference when Step 4 (Read and Analyze) encounters one of these situations. The main SKILL.md workflow covers the common path; this file handles infrequent but important complications.

## Graphical-Only Results

Some papers report key metrics **only in figures** (bar charts, curves) without a numeric table. When this happens:

- Do **not** fabricate numbers from the figure — transcription from rendered charts is error-prone.
- In the source page's `## Results` section, state explicitly: *"AECMOS / DNSMOS scores are reported graphically in Figure N (not as a numeric table). Key qualitative findings from the figure:"* and then list the findings as labeled bullet points matching the paper's own discussion (e.g., "(a) LEC scores highest on DT Other").
- Always include the numeric tables that **are** present (e.g., ERLE tables, complexity tables) — these are transcription-safe.
- When a later paper cites this paper's numeric scores, prefer the later paper's cited values **only if** they are explicitly attributed; otherwise flag the discrepancy (see below).

## Citation Discrepancies

Later papers often cite earlier work with **different numbers** than the original paper self-reports (e.g., different param counts, MACs/s, or band counts due to different counting methodologies, inclusion/exclusion of the linear stage, or simply typos). When you ingest a paper and notice its self-reported numbers differ from how a later, already-ingested paper cites it:

1. **Use the original paper's self-reported numbers** in the new source page.
2. **Add a discrepancy note** in the new source page (under `## Results` or a dedicated note) explaining the mismatch with the later citation.
3. **Update the already-ingested later paper's concept/entity pages** that reference the old numbers — correct the numbers and add a note pointing to the original paper as the authoritative source.
4. **Do not** modify the later paper's `wiki/sources/*.md` page — the later paper *did* cite those numbers; note the discrepancy but leave the citation as-is in the source page. Fix only the concept/synthesis pages that treated the cited numbers as ground truth.

## Loose Classifications in Review Papers

Review papers sometimes **categorize cited methods under labels that don't quite fit** the actual architecture of those methods. For example, Mienye et al. 2024 lists PercepNet (Valin et al. 2021, which is GRU-based) under "Echo State Network applications" — a loose grouping, since PercepNet is not a reservoir-computing model. When ingesting a review paper and you notice such a loose classification:

1. **Note the classification in the source page** under the relevant application section, with a brief caveat: e.g., *"The review cites Valin 2021 under ESN applications; this is a loose grouping — PercepNet uses a GRU-based post filter, not a reservoir."*
2. **Add the same caveat to the affected concept page** (e.g., in `echo-state-network.md` under Applications, note that the review's classification of PercepNet as an ESN application is loose).
3. **Do not** modify the cited paper's own source page — the misclassification is in the review, not the original work.

## Cross-references to Already-Ingested Papers

When the paper being ingested cites or discusses a paper that is **already in the wiki** (no discrepancy required), add bidirectional `[[sources/...]]` links:

1. In the new source page, add the existing paper to `## Related Sources` with a one-line note on how the new paper uses it (e.g., *"cited as a representative ESN application"* or *"baseline in our experiments"*).
2. In the existing paper's source page, append a one-line note to `## Related Sources` (or create the section if absent) pointing back to the new paper with the relationship.
3. If the new paper's framing of the cited work differs from the wiki's current framing (without being a numeric discrepancy or loose classification), note the difference briefly in both pages — this helps future readers understand how the field's view of the work has evolved.
