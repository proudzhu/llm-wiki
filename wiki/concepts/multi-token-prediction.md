---
type: concept
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/articles/dspark-speculative-decoding.md
tags:
  - llm-training
  - llm-inference
  - speculative-decoding
  - multi-token-prediction
  - deepseek
  - meta
---

# Multi-Token Prediction (MTP)

**Multi-token prediction (MTP)** is a training-time technique that augments a large language model with auxiliary prediction heads for future tokens, so that the model learns to forecast multiple positions ahead — not just the next token — during pretraining. At inference time, these same heads serve as a free draft model for [[concepts/speculative-decoding|speculative decoding]], unifying training-time quality gains with inference-time acceleration.

Two influential realizations exist: **Meta MTP** (parallel independent heads) and **DeepSeek-V3 MTP** (sequential causal chain). The latter, in particular, marks the shift of speculative decoding from a "post-training add-on" to a "pretraining-builtin feature."

## Meta MTP (2024)

Meta FAIR's *Better & Faster Large Language Models via Multi-token Prediction* (2024) asks: **why not give the model speculative ability during pretraining itself?** The architecture adds $K$ independent output heads that predict tokens at positions $t+1, t+2, \ldots, t+K$ in parallel, all conditioned on the same hidden state at position $t$.

Training signal: each head incurs its own cross-entropy loss against the corresponding future token. The total loss is the sum.

Findings:

- **Usefulness only at scale.** Multi-token prediction helps for models above a certain size; small models can actually do slightly worse with MTP than without. This explains why the technique had been overlooked earlier.
- **Downstream quality gains** beyond inference speed — especially on code generation, where looking ahead naturally discourages locally-greedy token choices.
- **Inference reuse.** The trained heads plug directly into a speculative-decoding pipeline with no further training.

## DeepSeek-V3 MTP (2024)

DeepSeek-V3's MTP module changes two things relative to Meta MTP:

### Sequential causal chain

Instead of $K$ independent parallel heads, DeepSeek-V3 uses a **sequential** structure: the $k$-th MTP module takes the $(k-1)$-th module's output as part of its input. This creates a causal information flow — the prediction at depth $k$ depends on the prediction at depth $k-1$, mirroring how an autoregressive draft model conditions on its own previous outputs.

Each MTP module $k$ contains:

- A shared embedding layer $\mathrm{Emb}(\cdot)$ (frozen, shared with the main LLM).
- A shared output head $\mathrm{OutHead}(\cdot)$ (frozen, shared).
- A Transformer block $\mathrm{TRM}_k(\cdot)$ (the only trained part of module $k$).
- A projection matrix $\sigma_k$.

The forward computation chains: input at depth $k$ is a combination of the main model's hidden state and the previous depth's output, projected in, run through $\mathrm{TRM}_k$, and projected out via the shared head.

### Training objective

Weighted average of per-depth cross-entropy losses:

$$
\mathcal{L}_{\text{MTP}} = \sum_{k=1}^{K} \lambda_k \cdot \mathrm{CE}_k
$$

DeepSeek-V3 used $\lambda_k = 0.3$ for the first 10T tokens and $0.1$ for the last 4.8T — heavier weight early in training when the signal is most informative, lighter later to avoid over-regularizing the main LM head.

## Why It Matters

DeepSeek-V3's MTP is a **paradigm shift** in two senses:

1. **Training enhancement, not just inference acceleration.** The auxiliary heads densify the training signal — every training token contributes to $K + 1$ loss terms instead of 1 — which improves sample efficiency and downstream quality. The inference speedup is, in effect, a free byproduct.
2. **Pretraining-builtin drafting.** Prior draft models (EAGLE, Medusa, DFlash) are trained *after* the target LLM is frozen, then attached at inference time. MTP trains the draft *with* the LLM, guaranteeing perfect distribution alignment between draft and target — the most common failure mode of external draft models simply cannot occur.

## Limitations and Open Questions

- **Conservative depth.** DeepSeek-V3 uses $K = 1$ in production — a single extra prediction — to limit training cost. This caps single-round speedup. Extending to larger $K$ without proportional training-cost growth is an open problem.
- **Inference overhead.** Each extra MTP depth adds parameters and a forward-pass branch; the cost must be weighed against the speedup from longer drafts.

These tensions are exactly what later parallel drafters ([[concepts/dflash|DFlash]], [[concepts/dspark|DSpark]]) address by decoupling drafting latency from draft length.

## References

- Meta MTP: Gloeckle et al. *Better & Faster Large Language Models via Multi-token Prediction*. [arXiv:2404.19737](https://arxiv.org/abs/2404.19737).
- DeepSeek-V3 MTP: DeepSeek-AI. *DeepSeek-V3 Technical Report*. 2024. The MTP module is described in the inference section.
- [[sources/zartbot-2026-dspark-speculative-decoding|zartbot 2026]] §1.4.
- Successor context: [[concepts/dspark|DSpark]] — DeepSeek's 2026 follow-up that uses a parallel backbone instead of MTP for drafting.
