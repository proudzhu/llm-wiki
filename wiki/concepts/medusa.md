---
type: concept
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/articles/dspark-speculative-decoding.md
tags:
  - llm-inference
  - speculative-decoding
  - multi-head-prediction
  - self-speculation
  - typical-acceptance
---

# Medusa

**Medusa** (*Simple LLM Inference Acceleration Framework with Multiple Decoding Heads*, Princeton/CMU, 2024) is the work that opened the **self-speculation** line of speculative decoding research. Instead of training a separate draft model, Medusa attaches $K$ lightweight prediction heads directly to the target LLM's final hidden state, each head forecasting a different future position in parallel.

Medusa is historically important because it **proved that the target model itself contains enough predictive signal to substitute for an external draft model** — a result that shaped everything that followed, including [[concepts/eagle-speculative-decoding|EAGLE]]'s feature-layer approach and [[concepts/multi-token-prediction|MTP]]-style training integration.

## Architecture

The target LLM is unmodified. After its final hidden state $h_t$, $K$ extra **Medusa heads** are appended in parallel. Each head is a single-layer FFN with residual connection that outputs a distribution over the vocabulary for position $t + k$ (for $k = 1, \ldots, K$). The heads are trained on the same corpus as the LLM, with the LLM frozen; only the heads are updated.

Parameters added: ~6% of the LLM's parameter count — Medusa is genuinely lightweight.

## Tree-Attention Verification

Each head emits its top-$k$ candidate tokens at every position. The Cartesian product across heads would be exponential, so Medusa builds a **draft tree** by combining the top-$k$ predictions level by level (with optional pruning), then verifies the entire tree in a single target-LLM forward pass using [[concepts/tree-attention\|tree attention]] — the same trick later used by [[concepts/eagle-speculative-decoding|EAGLE]] and [[concepts/dspark|DSpark]].

## Typical Acceptance

Standard speculative decoding's rejection sampling is conservative: it strictly preserves the target distribution but rejects many tokens that *would* have been acceptable. Medusa replaces it with **Typical Acceptance**, an entropy-adaptive rule:

- **Low-entropy position** (model is confident): apply a strict threshold — accept only high-probability tokens (greedy-like).
- **High-entropy position** (model is uncertain): apply a loose threshold — accept more tokens (more permissive).

The threshold adapts to the entropy of the target's distribution at each position, giving an elegant per-position knob. The trade-off: Typical Acceptance is no longer strictly lossless in the rejection-sampling sense, but in practice it produces output statistically indistinguishable from the target.

## Why It Matters

- **No external draft model.** This was the first demonstration that self-speculation — using the target model's own intermediate representations to predict future tokens — could deliver competitive speedups (2.2–2.8×) without a separate trained draft.
- **Tree attention as a first-class primitive.** Medusa's combination of multi-head prediction + tree verification became the template for nearly all subsequent feature-layer and parallel drafters.
- **Spawned a research line.** EAGLE, EAGLE-2, EAGLE-3 all build on the "predict from the target's own features" idea, but move the prediction into the feature space rather than the token space.

## Limitations

- **Batch scaling.** When the serving batch size grows, the system shifts from memory-bound to compute-bound, and the savings from parallel verification shrink. Medusa's speedup can vanish under high concurrency — exactly the regime that [[concepts/dspark|DSpark]]'s confidence-scheduled verification is designed to fix.
- **Independent-head predictions.** Each Medusa head predicts its position independently of the others' predictions, so the heads can produce mutually inconsistent token combinations (the same multimodal-collision problem that later plagues [[concepts/dflash|DFlash]]). EAGLE-1's contribution is essentially to fix this by making the prediction autoregressive in feature space.

## References

- Cai, T. et al. *Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads*. [arXiv:2401.10774](https://arxiv.org/abs/2401.10774).
- [[sources/zartbot-2026-dspark-speculative-decoding|zartbot 2026]] §1.3.1.
- Successor framing: [[concepts/eagle-speculative-decoding|EAGLE]] (feature-space autoregression); [[concepts/multi-token-prediction|MTP]] (training integration).
