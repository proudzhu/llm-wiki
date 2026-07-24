---
type: entity
created: 2026-07-12
updated: 2026-07-24
sources:
  - raw/articles/dspark-speculative-decoding.md
  - raw/papers/liang-wenfeng-investor-exchange-meeting/full-text.md
tags:
  - organization
  - ai-lab
  - llm
  - inference
  - speculative-decoding
  - china
  - open-weight
  - agi
---

# DeepSeek

**DeepSeek** (深度求索) is a Chinese AI research lab and LLM developer, known for open-weight large language models and open-source inference infrastructure. Founded by [[entities/wenfeng-liang|Liang Wenfeng]] around 2024, the company is notable for its vision-driven organization, "ten-month payback" API pricing benchmark, and the strategic decision to open-source its strongest models (see [[concepts/restraint-as-strategy|Restraint as Strategy]]). In the context of this wiki, DeepSeek is the developer of [[concepts/dspark|DSpark]] and the organization that deployed it in production on DeepSeek-V4.

## Relevance to Speculative Decoding

DeepSeek has contributed to speculative decoding across multiple layers of the stack:

- **DeepSeek-V3 MTP (2024)** — DeepSeek-V3's [[concepts/multi-token-prediction|multi-token prediction]] module, which builds a sequential causal chain of auxiliary heads directly into pretraining. This was a paradigm shift: drafting became a *pretraining-builtin* feature rather than a post-training add-on.
- **DSpark (2026)** — DeepSeek's open-source speculative decoding framework ([DeepSpec repository](https://github.com/deepseek-ai/DeepSpec)), combining semi-autoregressive generation with confidence-scheduled verification. DSpark is built on top of [[concepts/dflash|DFlash]]'s parallel diffusion backbone.
- **DeepSeek-V4 deployment** — DSpark is deployed in production on DeepSeek-V4-Flash and DeepSeek-V4-Pro preview, where it delivers 60–85% per-user generation speedup under matched throughput.

## Systems Contributions

Beyond algorithmic work, DeepSeek's DSpark deployment required two systems-level innovations that are described in [[sources/zartbot-2026-dspark-speculative-decoding|zartbot 2026]]:

- **Hidden-state communication** — workers exchange `hidden_size`-dim activations rather than full-vocabulary logits during distributed draft training, reducing communication from $O(|V|)$ to $O(d)$ per token.
- **Anchor-bounded sequence packing** — short anchor-bounded draft blocks are packed densely into training batches with token-level attention indices, preserving exact causality across packed blocks without padding waste.

These optimizations were implemented in DeepSeek's HAI-LLM training framework.

## Model Family

- **DeepSeek-V3** (2024) — open-weight LLM with integrated MTP module.
- **DeepSeek-V4-Flash / DeepSeek-V4-Pro** (2026) — production models on which DSpark is deployed.

## Strategic Vision (2026 Investor Meeting)

In a closed-door investor exchange meeting recorded 2026-05-20 (transcribed 2026-07-16), founder [[entities/wenfeng-liang|Liang Wenfeng]] publicly articulated DeepSeek's strategic posture. Key disclosures:

- **Open-source of frontier models is non-negotiable** — original intent, not forced; "I don't see what inevitable benefit closed-source brings"
- **Pricing benchmark**: API prices set so that hardware cost is recovered in 10 months (~6× profit margin); demand is price-inelastic at this point, so further cuts would not increase usage
- **Compute**: ~20k H-equivalent cards (mostly recently arrived); 16k Huawei 950 from Huawei (≈4k B-series equivalent); cannot currently train 800B-activation models
- **AGI roadmap**: staircase of language models → CoT → Agent → continuous learning → self-iterating singularity → embodied AI; explicit exclusion of world models and video generation from the main line
- **Organization**: no KPI, no formal structure; half formal cross-team work, half self-directed research; minimal overtime; the only non-negotiable is team stability
- **US–China gap**: framed as a resource gap, not a talent gap; target narrative "1–2 years behind, using 1/20 of US compute"

See [[sources/liang-wenfeng-investor-exchange-meeting|Liang Wenfeng 2026: Investor Exchange Meeting]] for the full transcript-derived source page, and [[concepts/agi-roadmap-staircase|AGI Roadmap Staircase]], [[concepts/restraint-as-strategy|Restraint as Strategy]], [[concepts/continuous-learning|Continuous Learning]] for the concepts derived from it.

## References

- DeepSpec repository: [github.com/deepseek-ai/DeepSpec](https://github.com/deepseek-ai/DeepSpec).
- DSpark paper: *Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation* (2026).
- DeepSeek-V3 Technical Report (2024) — describes the MTP module.
- [[sources/zartbot-2026-dspark-speculative-decoding|zartbot 2026]] — primary source for this page.
- [[sources/liang-wenfeng-investor-exchange-meeting|Liang Wenfeng 2026: Investor Exchange Meeting]] — primary source for the Strategic Vision section.
