---
type: concept
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/articles/dspark-speculative-decoding.md
tags:
  - llm-inference
  - speculative-decoding
  - feature-layer-prediction
  - autoregressive-drafting
  - draft-tree
---

# EAGLE (Speculative Decoding)

**EAGLE** (*Extrapolation Algorithm for Greater Language-model Efficiency*) is a family of autoregressive draft-model methods — EAGLE-1 (2024), EAGLE-2 (2024), EAGLE-3 (2025) — that established feature-layer prediction as the state-of-the-art paradigm for autoregressive drafting before parallel drafters ([[concepts/dflash|DFlash]], [[concepts/dspark|DSpark]]) overtook it. It is the principal baseline against which DSpark is evaluated.

The central insight across all three versions: **token-level uncertainty comes from feature-level uncertainty**, so it is better to autoregress in the target model's hidden-feature space than in token-id space.

## EAGLE-1 (2024)

### Two key insights

1. **Feature-layer autoregression.** The target model's penultimate hidden state is a high-dimensional continuous vector that is far more regular and predictable than discrete token ids. Predicting the next *feature* and then projecting through the (frozen, shared) LM head yields a better draft than predicting tokens directly. This change alone lifts speedup from 1.5× to 1.9×.
2. **Feed the sampled token back in.** Sampling introduces stochasticity: the same feature $h_t$ could be followed by "am" or "always," and the *next* feature depends on which one was chosen. EAGLE tells the draft model what the target actually sampled by feeding the previous token's embedding as an additional input. This lifts speedup from 1.9× to 2.8×.

### Architecture

The draft model has three components:

- **Embedding layer** (frozen, shared with target).
- **LM head** (frozen, shared with target).
- **Autoregression head** — the only trained part: an FC layer + a single Transformer decoder layer.

One drafting step: input is the feature sequence $[h_1, \ldots, h_t]$ plus the shifted token sequence $[x_2, \ldots, x_{t+1}]$ (one-step-ahead); concatenate, project down (2·hidden → hidden), pass through the decoder layer to predict $h_{t+1}$, and apply the LM head to get the draft distribution. Sample $x_{t+1}$ and append both $h_{t+1}$ and $x_{t+2} = x_{t+1}$'s embedding to the input for the next step.

Verification uses [[concepts/tree-attention\|tree attention]]: at each drafting step the model produces top-$k$ candidates, organized as a tree, and the target model verifies the entire tree in one forward pass with a modified attention mask. Speculative sampling at each tree node preserves distribution equivalence.

## EAGLE-2 (2024): Dynamic draft trees

EAGLE-1 uses a **static** draft tree — the same shape regardless of context. This wastes candidate budget on easy prefixes and is too small for hard ones. EAGLE-2 makes the tree **context-dependent** via two phases:

- **Expand.** Each node has a value $V(n) = \prod P(\text{accept on path to } n)$, approximated by the draft's confidence. Pick the top-$k$ highest-value leaf nodes and expand them one more level.
- **Rerank.** After expansion, sort *all* nodes by value and keep the top-$m$ — but break ties toward shallower nodes, which guarantees the kept set still forms a connected tree.

The resulting tree is flattened into a 1-D sequence with a custom attention mask (each node sees only its ancestors) and verified in a single target forward pass.

For the query "10+2", EAGLE-1 and EAGLE-2 behave identically. But after the prefix "10+2=" is locked in, EAGLE-1 still splits into top-$k$ branches uniformly, while EAGLE-2 concentrates almost the entire budget on the high-confidence continuation "1".

## EAGLE-3 (2025): Training-Time Test + scaling law

EAGLE-3's drafting input can come from either the target model's features *or* the draft model's own previously-generated features. Training only on target features would leave the draft unprepared for the distribution shift at inference time, when it must consume its own outputs.

The fix is **Training-Time Test**: the draft is trained on multi-step rollouts where step $k$'s input includes features produced by the draft itself at step $k-1$. The only change required is to the self-attention mask — instead of a lower-triangular causal mask, it becomes a block-structured mask that respects the tree-shaped dependency between the original training prefix and the rolled-out draft tokens. For efficiency, this can be implemented as vector dot products over only the relevant positions.

EAGLE-3 also reports a **scaling law**: more draft-training data yields continuously improving inference speedup, with no sign of saturation in the tested regime. This makes draft-model training a predictable investment.

## Why EAGLE Is the Right Baseline for DSpark

EAGLE-3 is the strongest autoregressive drafter and the natural point of comparison for [[concepts/dspark|DSpark]]:

- Both share the feature-layer-prediction philosophy.
- Both use tree attention for verification.
- EAGLE-3 is bottlenecked by $O(\gamma)$ serial drafting; DSpark is $O(1)$ parallel + tiny serial head.

The empirical finding (zartbot 2026, §2.4.1): DSpark's deeper parallel backbone wins at position 1 (math: 0.93 vs. 0.81), and the leverage of position-1 correctness outweighs EAGLE-3's advantage in deeper positions. EAGLE-3's conditional acceptance actually *climbs* along the block (chat: 0.53 → 0.74) because autoregression exploits the locked-in prefix, but the head-start from depth wins globally.

## Limitations

- **$O(\gamma)$ drafting latency.** Even with a 1-layer model, generating $\gamma = 8$ tokens needs 8 serial forward passes. This forces the architecture to stay extremely shallow, capping per-position quality.
- **Static tree (EAGLE-1) wastes budget; dynamic tree (EAGLE-2) helps but still searches within an autoregressive paradigm.**

These limitations are exactly what [[concepts/dflash|DFlash]] and [[concepts/dspark|DSpark]] address by moving to parallel drafting.

## References

- EAGLE-1: Li et al. *EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty*. [arXiv:2401.15077](https://arxiv.org/abs/2401.15077).
- EAGLE-2: Li et al. *EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees*. [arXiv:2406.16858](https://arxiv.org/abs/2406.16858).
- EAGLE-3: Li et al. *EAGLE-3: Scaling up Inference Acceleration ... via Training-Time Test*. [arXiv:2503.01840](https://arxiv.org/abs/2503.01840).
- [[sources/zartbot-2026-dspark-speculative-decoding|zartbot 2026]] §1.3.3 — survey of all three versions, with the comparison framing used here.
