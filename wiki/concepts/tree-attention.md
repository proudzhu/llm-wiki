---
type: concept
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/articles/dspark-speculative-decoding.md
tags:
  - llm-inference
  - speculative-decoding
  - attention
  - tree-verification
  - parallel-verification
---

# Tree Attention

**Tree attention** is the attention-mask trick that lets a target LLM verify a *branched* set of draft candidates in a single forward pass. Without it, speculative decoding would be limited to verifying one linear draft sequence at a time, wasting most of the parallel capacity of modern GPUs. [[concepts/specinfer|SpecInfer]], [[concepts/medusa|Medusa]]'s multi-head trees, [[concepts/eagle-speculative-decoding|EAGLE-2]]'s dynamic draft trees, [[concepts/ddtree|DDTree]], [[concepts/dspark|DSpark]], and JetSpec all rely on it.

## The Problem

Standard causal attention uses a lower-triangular mask: token $i$ can attend to tokens $1, \ldots, i$. This is correct for verifying a single linear draft — each draft token conditions on the prefix before it.

But if the draft model proposes *multiple* candidate tokens at each position (e.g., top-$k$ from each of $K$ Medusa heads, or a heap-built tree from DFlash's marginals), the candidates form a **tree**, not a sequence. Siblings in the tree are mutually exclusive alternatives, so a candidate at position $k$ along branch $A$ must not attend to a candidate at position $k$ along branch $B$ — that would leak information from a counterfactual continuation.

## The Fix: Tree-Shaped Attention Mask

Flatten the tree into a 1-D sequence in any order that respects parent-before-child (e.g., BFS or DFS). Build a boolean visibility matrix $M \in \{0, 1\}^{N \times N}$ where $M[i, j] = 1$ iff node $j$ is an ancestor of (or equal to) node $i$ in the tree, or $j$ is a prompt token. Each row of $M$ defines the *causal prefix* for that node.

Construction is recursive:

```
for each node i in topological order:
    visibility[i] = visibility[parent(i)]
    visibility[i, i] = True
```

The mask is then applied to the standard scaled-dot-product attention pre-softmax:

```python
mask = torch.zeros((1, 1, N, N))
mask.masked_fill_(~visibility, torch.finfo(dtype).min)
attn = softmax(Q @ K^T / sqrt(d) + mask) @ V
```

Masked positions get $-\infty$ (in practice `finfo.min`), so they contribute nothing to the softmax. Each node's representation is then computed using exactly the information that would have been available had its branch been the "real" continuation.

## Verification Procedure

Once the tree-attention forward pass completes:

1. At each node, the target model produces a distribution $p(\cdot | \text{ancestors})$.
2. Compare with the draft model's distribution $q$ at that node (for rejection sampling) or with the draft's sampled token (for sample-and-compare, as in DFlash).
3. Walk the tree top-down; accept the longest prefix along each branch.
4. The final accepted token is the deepest accepted node along some branch; resume drafting from there.

A single target forward pass has thus verified exponentially many candidate paths in parallel.

## Why It Matters

- **Exponential candidate coverage at linear cost.** With branching factor $b$ and depth $d$, a tree contains $O(b^d)$ candidate sequences but verifies them in $O(b \cdot d)$ attention operations.
- **Foundation for adaptive drafting.** Without tree attention, [[concepts/eagle-speculative-decoding|EAGLE-2]]'s dynamic draft trees and [[concepts/ddtree|DDTree]]'s best-first heap construction would be impossible — there would be no cheap way to verify the branched candidates they generate.
- **Generalizes naturally to causal + parallel hybrids.** JetSpec (2026) extends tree attention into **tree causal attention**, where the mask is shaped so that each node attends to its ancestors *in causal order* — combining the parallel coverage of tree attention with the conditional-dependency property of autoregressive drafting in a single forward pass. This is the key enabler for parallel-causal hybrid drafters.

## Relationship to KV Cache

Tree attention's mask is applied only to the **draft tokens** being verified in the current round. The prompt and previously-generated tokens sit in the KV cache as usual; every draft node attends to all of them (they are common ancestors). This means tree attention adds essentially no KV-cache overhead relative to plain speculative decoding — the only cost is building the $N \times N$ mask, which is tiny.

## Limitations

- **Mask construction overhead.** For very large trees, building the visibility matrix and the corresponding position-ids can become non-trivial. Implementations typically cache the mask shape and only recompute when the tree topology changes.
- **Memory.** $O(N^2)$ attention is the same as for any Transformer, but $N$ now includes all candidate nodes, which can be 10–100× the number of tokens actually accepted. Memory-efficient attention (FlashAttention) handles this gracefully.

## References

- SpecInfer (Miao et al. 2023) introduced tree attention for speculative decoding. [arXiv:2305.09781](https://arxiv.org/abs/2305.09781).
- Medusa (Cai et al. 2024) made tree attention a first-class primitive combined with multi-head prediction. [arXiv:2401.10774](https://arxiv.org/abs/2401.10774).
- JetSpec (2026) extends to tree causal attention.
- [[sources/zartbot-2026-dspark-speculative-decoding|zartbot 2026]] §1.2.1, §1.7.
