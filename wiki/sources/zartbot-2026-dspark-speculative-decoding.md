---
type: source
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/articles/dspark-speculative-decoding.md
  - https://mp.weixin.qq.com/s/RRHg9UCCInSc_zEcIgjNBQ
tags:
  - speculative-decoding
  - llm-inference
  - draft-model
  - rejection-sampling
  - tree-attention
  - deepseek
  - dspark
  - dflash
  - eagle
  - medusa
  - multi-token-prediction
  - parallel-decoding
---

# zartbot 2026: 详细谈谈DSpark投机解码的原理 (Detailed Discussion on DSpark Speculative Decoding)

**Author**: [[entities/zartbot|zartbot]]
**Published**: 2026-07-04 (WeChat article)
**Language**: Chinese
**URL**: [mp.weixin.qq.com/s/RRHg9UCCInSc_zEcIgjNBQ](https://mp.weixin.qq.com/s/RRHg9UCCInSc_zEcIgjNBQ)
**Type**: Technical blog post / survey with code walkthrough

## Summary

A long-form, code-level walkthrough of [[concepts/dspark|DSpark]] — [[entities/deepseek|DeepSeek]]'s open-source speculative decoding framework released in 2026 — set against the full arc of draft-model research from 2022 to 2026. The article has three layers: (1) a self-contained primer on speculative decoding and rejection sampling; (2) a survey of draft-model algorithms across six stages (autoregressive, tree-based, multi-head/feature-layer, training-integrated MTP, parallel diffusion, causal-tree); and (3) a deep dive into DSpark's two innovations — **semi-autoregressive generation** and **confidence-scheduled verification** — including code excerpts from the `deepspec` repository and a production-deployment report on DeepSeek-V4.

## Core Thesis

Speculative decoding's end-to-end speedup is governed by three levers — drafting latency $T_d$, acceptance rate $\alpha$, and verification cost $T_v$ — and DSpark improves on prior art on **all three axes** by:

1. **Semi-autoregressive generation**: Keep DFlash's $O(1)$ parallel drafting (a deep bidirectional backbone produces all $\gamma$ draft logits in one forward pass), then add a *lightweight* serial head (Markov or RNN) that injects block-internal token dependency left-to-right. This preserves parallel speed while arresting the suffix-quality decay that plagues pure parallel drafters.
2. **Confidence-scheduled verification**: A trained **confidence head** estimates per-position acceptance probability; a **hardware-aware prefix scheduler** then solves a global throughput-maximization problem to decide, per request and per batch, how many draft tokens to actually verify — pruning low-confidence suffixes under high load, extending them under low load.

## Structure

The article is organized as:

- **§0 — What is speculative decoding?** A layperson "professor + student" analogy, the rejection-sampling proof of distribution-equivalence, an implementation walkthrough of `verify_draft_tokens` from `deepspec/eval/base_evaluator.py`, and the **core parameter triple** $(\alpha, \gamma, c)$ with the exact speedup formula $S = \frac{1+c\gamma\alpha}{1+c\gamma}$ (per Leviathan et al. 2022).
- **§1 — Draft model algorithm survey**: 14 algorithms across 6 stages, with the evolution of drafting paradigms (autoregressive → tree → multi-head/feature → MTP → parallel diffusion → causal tree).
- **§2 — DSpark deep dive**: Architecture, training loss, experimental ablations, and online serving on DeepSeek-V4.
- **§3 — Conclusion**: Performance model, mathematical model, and scheduling-strategy design considerations.
- **Appendix A**: Six-stage timeline (2022.11 → 2026.06) of speculative decoding as a field.
- **Appendix B**: Line-by-line analysis of `Qwen3DSparkModel.forward` and `compute_dspark_loss`.

## Key Concepts Introduced

| Concept | Role in the article |
|---------|--------------------|
| [[concepts/speculative-decoding\|Speculative decoding]] | The draft-then-verify framework; rejection sampling guarantees distribution equivalence |
| [[concepts/dspark\|DSpark]] | The paper's subject — semi-autoregressive drafting + confidence-scheduled verification |
| [[concepts/dflash\|DFlash]] | Direct predecessor — parallel block-diffusion drafting with KV injection; DSpark's backbone |
| [[concepts/eagle-speculative-decoding\|EAGLE-1/2/3]] | The autoregressive-drafting benchmark DSpark is compared against |
| [[concepts/medusa\|Medusa]] | Multi-head speculative decoding — the original "self-speculation" work |
| [[concepts/multi-token-prediction\|Multi-token prediction]] | Meta MTP and DeepSeek-V3 MTP — training-integrated drafting |
| [[concepts/tree-attention\|Tree attention]] | The attention-mask trick enabling single-pass parallel verification of branched candidates |

## Algorithms Surveyed (§1)

| Stage | Algorithm | Key idea |
|-------|-----------|----------|
| 1.1.1 | Speculative Decoding (Leviathan 2022) | Independent small autoregressive draft model + reject sampling |
| 1.1.2 | Speculative Sampling (DeepMind 2023) | Wide-shallow draft co-deployed with Chinchilla (16-way TP) |
| 1.1.3 | BiLD (2023) | Fallback/Rollback by confidence; first dynamic draft length |
| 1.1.4 | Self-Speculative (2023) | Layer-skipping inside the target model itself |
| 1.2.1 | [[concepts/specinfer\|SpecInfer]] (2023) | Tree of draft sequences, tree-attention parallel verification |
| 1.3.1 | [[concepts/medusa\|Medusa]] (2024) | K extra heads on the target LLM; typical acceptance |
| 1.3.2 | Lookahead Decoding (2024) | Jacobi-iteration framing; n-gram trajectories as drafts |
| 1.3.3 | [[concepts/eagle-speculative-decoding\|EAGLE-1/2/3]] (2024–25) | Feature-layer autoregression; dynamic draft trees; training-time test |
| 1.4.1 | Meta MTP (2024) | K parallel output heads trained into the LLM |
| 1.4.2 | DeepSeek-V3 MTP (2024) | Sequential causal-chain MTP; pretraining-builtin drafting |
| 1.5 | [[concepts/dflash\|DFlash]] (2025) | Parallel block diffusion; $T_d = O(1)$; KV injection |
| 1.6 | DDTree (2026) | Best-first heap tree construction from DFlash's marginal logits |
| 1.7 | JetSpec (2026) | Tree causal attention mask — parallel + causal in one pass |

## DSpark Architecture (§2)

### 2.1 Semi-Autoregressive Generation

- **Parallel stage**: A DFlash-style backbone (e.g., 5-layer Qwen3 decoder, `is_causal=False`) runs one forward pass over $[anchor, MASK, \ldots, MASK]$ to produce base logits $b_k$ and hidden states $h_k$ for all $\gamma$ positions.
- **Sequential stage**: A tiny Markov or RNN head adds a transition bias $B(x_{k-1}, \cdot)$ so each position conditions on the previously sampled token. The head's compute is negligible (~1% of backbone), keeping $T_d \approx O(1)$.
  - **Markov head**: low-rank factorization $W_1 \in \mathbb{R}^{|V| \times r}, W_2 \in \mathbb{R}^{r \times |V|}$, $B(x_{k-1}) = W_2 W_1[x_{k-1}]$.
  - **RNN head**: GRU-like state $s_k = g \odot s_{k-1} + (1-g) \odot \tilde{s}$, accumulating full prefix history.
- **Inference**: Sample $x_1 \sim b_1$; then for $k \geq 2$ sample $x_k \sim \mathrm{softmax}(b_k + B(x_{k-1}))$.

### 2.2 Confidence-Scheduled Verification

- **Confidence head**: A linear layer + sigmoid predicts $c_k = P(\text{accept at } k \mid x_{<k} \text{ all accepted})$, supervised by the analytic acceptance rate $1 - \mathrm{TV}(p, q)$.
- **Sequential Temperature Scaling (STS)**: Post-hoc calibration from left to right — at each position, a 1-D grid search finds a temperature that minimizes ECE on the *cumulative* survival probability $\prod_{j \leq k} c_j$. STS is order-preserving, so the head's learned ranking is retained.
- **Hardware-aware prefix scheduler**: For a batch of $N$ active requests, choose verification lengths $\{l_i\}$ to maximize $\frac{\sum_i \mathbb{E}[\text{accepted}_i]}{T_{\text{forward}}(\sum_i l_i)}$. The scheduler maintains a pre-profiled cost table of throughput-vs-batch and greedily admits tokens by descending survival probability $c_k$, stopping early when throughput peaks (which also enforces causality — see Appendix A counter-example).

### 2.3 Training

Three losses, position-weighted by $e^{-k/\gamma}$ (front positions matter more because prefix rejection discards the whole block):

- $\mathcal{L}_{\text{CE}}$: next-token cross-entropy against ground truth.
- $\mathcal{L}_{\text{TV}}$: L1 distance between draft and target distributions — directly minimizes total variation, maximizing acceptance rate.
- $\mathcal{L}_{\text{conf}}$: BCE on the analytic acceptance-rate label.

Target model is frozen; embedding and LM head are shared and frozen; only the backbone, serial head, and confidence head are trained.

### 2.4 Experiments — Headline Findings

- **Parallel can beat autoregressive**: DFlash's deeper backbone wins at position 1 (e.g., math: 0.88 vs. EAGLE-3's 0.81); the leverage of position-1 correctness outweighs the suffix decay.
- **A little autoregression goes a long way**: Adding a 2-layer serial head to DSpark beats a 5-layer pure-parallel DFlash, at ~1% drafting-time overhead and ~30% draft-quality gain.
- **Confidence head**: Static-threshold sweep shows the head correctly identifies low-value suffix tokens (chat acceptance 45.7% → 95.7%); STS reduces ECE from 3–8% to ~1%.

### 2.5 Online Serving (DeepSeek-V4)

Deployed with DeepSeek-V4-Flash and DeepSeek-V4-Pro preview. Under matched throughput, per-user generation speed improves **60–85%**; under strict SLA, DSpark sustains throughput levels the baseline cannot reach. Two training-system optimizations:

- **Hidden-state communication**: ship `hidden_size`-dim activations (not $|V|$-dim logits) across workers; apply LM head locally where the draft lives.
- **Anchor-bounded sequence packing**: pack many short anchor-bounded blocks into a dense batch; use token-level attention indices (not 2-D masks) to keep causality exact across packed blocks.

## Critical Commentary

The article (signed "渣注" — "Slacker's note") interleaves the author's own analysis with the paper's content. Notable opinions:

- The JetSpec framing of "tree causal attention = restoring causality" is recast as **"position-aware restricted attention"** — its real value is preventing cross-branch contamination and providing an ordered positional inductive bias, *not* implementing true causal conditioning.
- The confidence scheduler is identified as the article's most consequential contribution, because it is the only part that explicitly models **system-level throughput** rather than single-request latency.
- The author draws an **optimal-transport interpretation** of draft training: minimizing $W_1(p, q)$ (or its TV special case) is the first-principles objective, not next-token accuracy.

## References Cited

The article cites 13 primary sources; the full reference list (with arXiv links) is at the end of `raw/articles/dspark-speculative-decoding.md`. Key ones:

- Leviathan et al. 2022 — *Fast Inference from Transformers via Speculative Decoding* (foundational).
- DFlash 2025 — direct predecessor; DSpark reuses its backbone.
- DSpark paper — *Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation* (DeepSpec repo).

## Why This Source Matters

This is one of the few long-form treatments that:

1. Unifies the **algorithmic** view (draft-model taxonomy) with the **systems** view (hardware-aware scheduling, batch capacity, throughput curves).
2. Provides **line-by-line code** from the actual `deepspec` repository rather than paraphrasing the paper.
3. Reports **production-scale** results (DeepSeek-V4), not just offline benchmarks.

It is the natural anchor page for any wiki work on speculative decoding, and the concept pages cross-referenced above extract its key technical content.
