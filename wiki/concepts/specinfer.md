---
type: concept
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/articles/dspark-speculative-decoding.md
tags:
  - llm-inference
  - speculative-decoding
  - tree-verification
  - restorative-verification
---

# SpecInfer

**SpecInfer** (*Speculative Inference with Token Tree Verification*, UC Berkeley et al., 2023) is the work that introduced **tree attention** to speculative decoding. Before SpecInfer, draft models proposed a single linear candidate sequence and the target verified it position-by-position. SpecInfer's contribution: let the draft model propose a *tree* of candidate sequences, and verify the entire tree in one target forward pass using a custom attention mask.

## Two Core Innovations

### 1. Token-tree verification

The draft model (which can be one or more small LLMs, or even heuristic generators like n-gram models) proposes multiple candidate tokens at each position, forming a tree of possible continuations. The tree is flattened into a 1-D sequence and verified by the target model with a **tree-shaped attention mask**: each node attends only to its ancestors in the tree (plus the prompt). See [[concepts/tree-attention|tree attention]] for the mask construction.

This converts speculative decoding from a linear-search problem to a tree-search problem: $O(b^d)$ candidate paths are verified in $O(b \cdot d)$ attention operations, where $b$ is the branching factor and $d$ is the depth.

### 2. Restorative verification (generalized rejection sampling)

SpecInfer generalizes standard speculative sampling to the tree setting. At each node, the target model produces a distribution $p(\cdot | \text{ancestors})$; the draft's distribution is $q(\cdot | \text{ancestors})$. The acceptance rule is the same min-ratio as in standard speculative decoding, but applied at every tree node independently. A rejected node's subtree is pruned; an accepted node's children remain candidates.

The "restorative" part: when a node is rejected, SpecInfer samples a correction from the residual $\max(0, p - q)$, just as in standard speculative sampling. This preserves distribution equivalence — SpecInfer is lossless.

## Why It Matters

- **First tree-based speculative decoding.** SpecInfer established the paradigm that every subsequent tree-based method ([[concepts/medusa|Medusa]], [[concepts/eagle-speculative-decoding|EAGLE-2]], [[concepts/ddtree|DDTree]], [[concepts/dspark|DSpark]]) builds on.
- **Pluggable draft sources.** SpecInfer can combine multiple draft models — including n-gram heuristics — into a single tree, making it robust to cases where no single draft model is good enough.
- **Lossless.** Unlike Medusa's later "Typical Acceptance" heuristic, SpecInfer's restorative verification strictly preserves the target distribution.

## Limitations

- **Still serial drafting.** SpecInfer's draft models are autoregressive; the tree is built by running them serially. The $O(\gamma)$ drafting latency bottleneck that [[concepts/dflash|DFlash]] and [[concepts/dspark|DSpark]] later address is still present.
- **Tree topology is static.** The tree shape is fixed before verification; it does not adapt to the draft's per-position confidence the way EAGLE-2's dynamic trees do.

## References

- Miao, X. et al. *SpecInfer: Accelerating Generative Large Language Model Serving with Tree-based Speculative Inference*. [arXiv:2305.09781](https://arxiv.org/abs/2305.09781).
- [[sources/zartbot-2026-dspark-speculative-decoding|zartbot 2026]] §1.2.1.
- See also: [[concepts/tree-attention|tree attention]] (the mechanism SpecInfer introduced).
