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
  - diffusion
  - block-decoding
  - kv-injection
---

# DFlash

**DFlash** (*Block Diffusion for Flash Speculative Decoding*, UC San Diego, 2025 / ICML 2026) is the work that broke speculative decoding's serial-drafting bottleneck. Its core move: recast the draft model as a **parallel diffusion adapter** that fills all $\gamma$ draft positions in a single forward pass, dropping drafting latency from $O(\gamma)$ to $O(1)$.

DFlash is the direct predecessor and backbone of [[concepts/dspark|DSpark]], which adds a serial head and confidence scheduling on top.

## The Problem It Solves

Every prior draft-model family — independent small models, [[concepts/eagle-speculative-decoding|EAGLE]], even [[concepts/medusa|Medusa]]'s multi-head approach — generates drafts **autoregressively**: token $k$ cannot be produced until token $k-1$ is sampled and fed back in. Even with a 1-layer draft model, generating $\gamma = 8$ tokens requires 8 serial forward passes, and $T_d$ grows linearly with $\gamma$. This forces a painful trade-off: keep $\gamma$ small (limits potential speedup) or keep the draft model extremely shallow (limits per-token quality).

DFlash observes that the actual bottleneck on modern GPUs is **weight loading (memory bandwidth)**, not compute. A single forward pass over $\gamma$ positions barely costs more than over 1, because the weights only need to be loaded once.

## Two Key Innovations

### 1. Parallel diffusion drafting

Input to the draft model is:

$$
[\,\text{anchor},\, \text{MASK},\, \text{MASK},\, \ldots,\, \text{MASK}\,]
$$

with **bidirectional attention** within the block (`is_causal = False`). Every position sees every other position — the natural mode of a diffusion / masked-prediction model. After a single forward pass, all $\gamma$ positions produce logits simultaneously.

Key property: **drafting latency is independent of $\gamma$.** Generating 16 tokens takes essentially the same time as generating 4.

### 2. KV-injection conditioning

A purely standalone diffusion model has no access to the target model's knowledge — like a student taking an exam without reading the question. DFlash fixes this by injecting the target model's hidden state into **every layer** of the draft model's attention.

**Feature extraction.** Sample $L$ layers from the target model (e.g., 5 layers out of 32 for Qwen3-8B), skipping layer 0 (too close to embedding) and the last 3 layers (too specialized for next-token prediction). Concatenate them along the channel axis and project down:

$$
\tilde{H} = \mathrm{RMSNorm}\!\Big(\,W_{\text{proj}}\, \big[\,h_{\ell_1};\, h_{\ell_2};\, \ldots;\, h_{\ell_L}\,\big]\Big).
$$

**Injection.** In every draft layer, the Key and Value tensors are the concatenation of the target-feature KV and the draft's own KV:

$$
K = [\,K_{\text{ctx}};\, K_{\text{draft}}\,] = K\text{-proj}\!\big([\,\tilde{H};\, H_{\text{draft}}\,]\big),
$$

and similarly for $V$. Each draft position thus attends over both its block siblings and a rich, multi-granularity summary of what the target model "thinks" about the context. Geometrically, this pulls the draft distribution $q$ toward the target distribution $p$ on the statistical manifold, reducing $\mathrm{TV}(p, q)$ and raising the acceptance rate.

## Inference Flow

1. **Target prefill** — standard autoregressive prefill, producing the first token and per-layer hidden states.
2. **Feature extraction** — gather hidden states at the preselected layers, project, and normalize once per round.
3. **Parallel draft** — one forward pass through the draft model produces $\gamma$ draft logits.
4. **Sample-and-compare verification** — the target model runs one forward pass over $[\text{anchor}, x_1, \ldots, x_\gamma]$; each position's argmax/sample is compared to the draft token. Acceptance length = length of the matching prefix.

### Why sample-and-compare instead of standard speculative sampling?

Standard speculative sampling needs $q(x_k | x_{<k})$ — a per-position conditional probability. But DFlash's draft is a **block-diffusion** model that emits a joint distribution over all positions, which doesn't decompose cleanly into conditionals. So DFlash verifies by independent sampling + comparison:

```python
draft_tokens   = sample(draft_logits)
posterior      = sample(target_logits, temperature)
acceptance_len = cumprod(draft_tokens == posterior[:, :-1]).sum()
```

At $T > 0$ this is theoretically slightly less efficient than standard speculative sampling (an inner product of distributions vs. their min), but the gap closes as KV injection drives $q \to p$.

## Training Tricks

- **Random anchor sampling** — instead of fixed chunk boundaries, sample random anchor positions per epoch. This matches the inference-time distribution (where anchors depend on the previous round's acceptance length) and acts as data augmentation.
- **Sparse block-wise attention** — multiple training blocks packed into one sequence, with block-internal bidirectional attention and block-external isolation. KV-injected features are visible to every block.
- **Position-weighted loss** — exponential decay $e^{-k/\gamma}$ on the loss weight, because prefix rejections are catastrophic. This optimizes the *expected acceptance length* directly.
- **Shared/frozen embedding and LM head** — only the Transformer layers and projection are trained; the draft model is genuinely a lightweight "adapter."

## Performance

On Qwen3-8B: **4.86× speedup**, roughly 2.5× over [[concepts/eagle-speculative-decoding|EAGLE-3]] (2.02×). The gain comes from being able to simultaneously use a *deeper* draft model (5 layers vs. 1) and a *longer* draft block, because $T_d$ no longer scales with $\gamma$ or model depth.

## The New Problem It Exposes

Parallel generation breaks the **causality** that autoregressive drafting gets for free. Each position is marginalized over all possible earlier tokens rather than conditioned on the actually-sampled one, so when the context permits multiple continuations (e.g., "of course" vs. "no problem"), the draft may produce inconsistent combinations like "of problem." Acceptance rate decays rapidly along the block.

Two successor works tackle this:

- [[concepts/ddtree|DDTree]] — builds a draft *tree* from DFlash's marginal logits, using best-first heap search to pick the highest-survival-probability prefix set.
- [[concepts/dspark|DSpark]] — keeps DFlash's parallel backbone but adds a lightweight serial (Markov or RNN) head that injects prefix conditioning without giving up $O(1)$ latency.
- JetSpec — uses a tree-shaped causal attention mask so each node attends only to its ancestors, achieving parallel + causal in a single pass.

## References

- DFlash paper: *Block Diffusion for Flash Speculative Decoding*. [arXiv:2602.06036](https://arxiv.org/abs/2602.06036).
- [[sources/zartbot-2026-dspark-speculative-decoding|zartbot 2026]] §1.5 — walkthrough with code from `dflash.py`.
- Successors: [[concepts/dspark|DSpark]] (this page's main context), [[concepts/ddtree|DDTree]], JetSpec.
