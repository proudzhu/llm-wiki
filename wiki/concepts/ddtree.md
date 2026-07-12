---
type: concept
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/articles/dspark-speculative-decoding.md
tags:
  - llm-inference
  - speculative-decoding
  - parallel-decoding
  - tree-search
  - best-first-search
  - dflash
---

# DDTree

**DDTree** (2026) is a tree-structured extension of [[concepts/dflash|DFlash]] that addresses parallel drafting's **causality problem** without resorting to autoregressive serial heads (the route taken by [[concepts/dspark|DSpark]]). DDTree keeps DFlash's $O(1)$ parallel backbone but post-processes its marginal logits into a **best-first search tree**, so that the verified candidates respect prefix-dependency even though the draft itself does not.

## The Problem

DFlash's parallel backbone emits a marginal distribution $q_k(\cdot)$ at each position independently. These marginals are inconsistent: sampling from each independently can produce mutually-incompatible token combinations (e.g., "of problem" when "of course" and "no problem" are both plausible continuations). Acceptance rate decays sharply along the block.

DDTree's insight: **don't sample independently — search the joint space.**

## Algorithm

### Step 1: Build a candidate pool

Run DFlash's parallel backbone once to get marginal logits $b_1, \ldots, b_\gamma$ at all positions. At each position, keep the top-$k$ candidate tokens with their probabilities.

### Step 2: Best-first tree construction

Maintain a max-heap of partial tree paths, keyed by **cumulative survival probability** — the product of marginal probabilities along the path so far:

$$
V(\text{path}) = \prod_{j \in \text{path}} q_j(x_j).
$$

- Initialize the heap with the top-$k$ tokens at position 1.
- Repeatedly pop the highest-value partial path, extend it by one position (top-$k$ tokens at the next position), and push the extensions back.
- Stop when the tree contains $M$ leaves (a budget parameter) or reaches depth $\gamma$.

This is classic best-first search with cumulative probability as the priority. The result is a tree where the highest-probability paths are explored first, subject to a total-leaf budget.

### Step 3: Tree-attention verification

Flatten the tree and verify it in a single target-model forward pass using [[concepts/tree-attention|tree attention]]. Each node's acceptance is evaluated against the target's conditional distribution at that node.

## Why It Matters

- **Pure-parallel drafting + tree search = no serial head needed.** DDTree gets prefix-conditioned candidate selection *for free* from the tree structure, without adding any serial computation to the draft model. This is an alternative architectural response to the same causality problem that DSpark solves with a serial head.
- **Budget-adaptive.** The leaf budget $M$ directly controls the compute/quality trade-off: more leaves means more candidates verified but higher verification cost.
- **Best-first pruning is principled.** Cumulative survival probability is exactly the quantity that determines expected accepted tokens; prioritizing high-probability paths is the right objective.

## Limitations

- **Marginal probabilities are still inconsistent.** DDTree searches over paths using *marginal* probabilities $q_k(x_k)$ as edge weights, but the true conditional probability $q_k(x_k | x_{<k})$ is unavailable from a parallel drafter. The heuristic works well in practice but is not theoretically optimal.
- **Verification cost scales with $M$, not $\gamma$.** A large leaf budget can make verification expensive, partially undoing the $O(1)$ drafting advantage.

## Relationship to DSpark

DDTree and DSpark are sibling responses to DFlash's causality problem:

| Approach | How prefix-dependency is restored | Drafting latency |
|----------|-----------------------------------|-------------------|
| **DDTree** | Post-hoc tree search over marginal logits | $O(1)$ + search overhead |
| **DSpark** | Lightweight serial (Markov/RNN) head in the draft model | $O(1)$ + ~1% serial overhead |
| **JetSpec** | Tree causal attention mask — parallel + causal in one pass | $O(1)$ |

Each makes a different trade-off between draft-model complexity, search/verification overhead, and theoretical cleanliness.

## References

- DDTree paper (2026). Referenced in [[sources/zartbot-2026-dspark-speculative-decoding|zartbot 2026]] §1.6.
- Predecessor: [[concepts/dflash|DFlash]].
- Sibling approaches: [[concepts/dspark|DSpark]], JetSpec.
