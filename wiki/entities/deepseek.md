---
type: entity
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/articles/dspark-speculative-decoding.md
tags:
  - organization
  - ai-lab
  - llm
  - inference
  - speculative-decoding
  - china
---

# DeepSeek

**DeepSeek** (深度求索) is a Chinese AI research lab and LLM developer, known for open-weight large language models and open-source inference infrastructure. In the context of this wiki, DeepSeek is the developer of [[concepts/dspark|DSpark]] and the organization that deployed it in production on DeepSeek-V4.

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

## References

- DeepSpec repository: [github.com/deepseek-ai/DeepSpec](https://github.com/deepseek-ai/DeepSpec).
- DSpark paper: *Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation* (2026).
- DeepSeek-V3 Technical Report (2024) — describes the MTP module.
- [[sources/zartbot-2026-dspark-speculative-decoding|zartbot 2026]] — primary source for this page.
