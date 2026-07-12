---
type: concept
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/articles/dspark-speculative-decoding.md
tags:
  - llm-inference
  - acceleration
  - draft-model
  - rejection-sampling
  - speculative-sampling
---

# Speculative Decoding

**Speculative decoding** (Leviathan et al. 2022; Chen et al. 2023) is an inference-acceleration technique for autoregressive large language models that uses a cheap **draft model** to propose candidate tokens and an expensive **target model** to verify them in a single parallel forward pass. The key result: a correctly-implemented verifier recovers *exactly* the target model's output distribution, so the speedup is **lossless**.

## The Draft-Then-Verify Framework

Two roles:

- **Target model** $p$ — the authoritative, slow LLM (e.g., GPT-4). Generating one token requires a full forward pass over a large model.
- **Draft model** $q$ — a much smaller, faster model (or some other cheap predictor). It autoregressively generates $\gamma$ candidate tokens $x_1, \ldots, x_\gamma$.

The target model then runs **one** forward pass over the prefix + all $\gamma$ candidates simultaneously, producing $p(x_{k} | x_{<k})$ at each position. Each draft token is accepted or rejected by **speculative sampling** (a form of rejection sampling). The first rejection truncates the suffix; one extra token is sampled from the residual to keep things moving.

The intuition: a single target forward pass costs roughly the same whether it processes 1 or $\gamma + 1$ positions, so if the draft is mostly right, $\gamma + 1$ tokens emerge for the price of one.

## Mathematical Foundation: Rejection Sampling

Suppose the draft model proposes $x_k \sim q(\cdot | x_{<k})$. The target model produces $p(\cdot | x_{<k})$ at the same position. The acceptance rule is

$$
P(\text{accept } x_k) = \min\!\left(1, \frac{p(x_k | x_{<k})}{q(x_k | x_{<k})}\right).
$$

If accepted, continue to $k+1$. If rejected, discard $x_k$ (and all later draft tokens) and resample a correction from the residual

$$
r(x) = \frac{\max(0,\, p(x|x_{<k}) - q(x|x_{<k}))}{\mathrm{TV}(p, q)},
\qquad
\mathrm{TV}(p, q) = \tfrac{1}{2}\sum_x |p(x) - q(x)|.
$$

**Distribution-equivalence proof sketch.** A token $y$ ends up in the output via exactly two mutually exclusive paths:

1. The draft proposes $y$ *and* it is accepted: contributes $q(y) \cdot \min(1, p(y)/q(y)) = \min(p(y), q(y))$.
2. The draft proposes some other token $z$ that is rejected, and $y$ is resampled from $r$: contributes $\sum_{z \neq y} q(z)(1 - \min(1, p(z)/q(z))) \cdot r(y)$.

Adding both paths and simplifying yields $p(y)$ exactly — the verifier's output distribution is the target's, *regardless* of how the draft model is built.

## Core Parameter Triple

The end-to-end speedup is governed by three quantities (Leviathan et al. 2022):

| Symbol | Meaning | Typical range |
|--------|---------|---------------|
| $\alpha$ | **Acceptance rate** per position; $\alpha = 1 - \mathrm{TV}(p, q)$ | $0.5$ – $0.9$ |
| $c$ | **Cost ratio** $T_d / T_v$ (draft step time / target step time) | $0.05$ – $0.2$ |
| $\gamma$ | **Draft length** (tokens proposed per round) | $4$ – $16$ |

The expected accepted tokens per round is a truncated geometric series $\sum_{k=1}^{\gamma} \alpha^k = \frac{\alpha(1-\alpha^\gamma)}{1-\alpha}$, and the round's wall-clock cost is $T_v + \gamma T_d = T_v (1 + c\gamma)$. So

$$
S = \frac{\text{tokens per round}}{\text{time per round}}
   = \frac{1 + c\gamma\alpha}{1 + c\gamma} \quad\text{(speedup over plain autoregression)}.
$$

All subsequent algorithmic work in speculative decoding can be read as attacking one of these three knobs — and the three are coupled: making the draft model bigger raises $\alpha$ but also $c$; making $\gamma$ larger amplifies both the numerator (more free tokens if accepted) and the denominator (more wasted drafting if rejected).

## Implementation Pattern

A minimal verifier (adapted from DSpark's `deepspec/eval/base_evaluator.py`):

```python
# Step 1: target model parallel forward over [current, t1, ..., tγ]
target_probs = softmax(target_model([current, *draft_tokens]).logits)

# Step 2: speculative sampling — accept prob per position
accept_prob = clamp(target_probs[:, :-1, draft_tokens] / draft_probs, max=1.0)
accept_mask = (rand < accept_prob).int()
accept_prefix_mask = accept_mask.cumprod(dim=1)   # prefix semantics

# Step 3: if rejected at position k, resample from residual = norm(max(0, p - q))
#         if all accepted, sample a "bonus" token from target_probs[:, -1, :]
```

The `cumprod` encodes the **prefix-acceptance** semantics: once a position is rejected, every later draft token is automatically rejected too.

## Common Draft-Model Families

Speculative decoding research is essentially a taxonomy of *what serves as the draft model*:

| Family | Examples | Drafting latency |
|--------|----------|-------------------|
| Independent small autoregressive model | Leviathan 2022; Speculative Sampling | $O(\gamma)$ serial |
| Tree of drafts | [[concepts/specinfer\|SpecInfer]]; [[concepts/ddtree\|DDTree]] | $O(\gamma)$ + tree verify |
| Multi-head self-prediction | [[concepts/medusa\|Medusa]] | $O(1)$ parallel |
| Feature-layer autoregression | [[concepts/eagle-speculative-decoding\|EAGLE-1/2/3]] | $O(\gamma)$ serial but high $\alpha$ |
| Training-integrated | [[concepts/multi-token-prediction\|Meta MTP; DeepSeek-V3 MTP]] | $O(1)$ parallel |
| Parallel block diffusion | [[concepts/dflash\|DFlash]] | $O(1)$ parallel |
| Semi-autoregressive | [[concepts/dspark\|DSpark]] | $O(1)$ parallel + light serial |

See [[sources/zartbot-2026-dspark-speculative-decoding|zartbot 2026]] §1 for a full six-stage timeline of this evolution.

## When It Helps and When It Doesn't

- **Compute-bound regime** (large batch, e.g., online serving under high QPS): the target's forward pass is already GPU-saturated, so a parallel verifier barely costs less than generating $\gamma$ tokens one at a time. The gain shrinks or vanishes. This is the regime where [[concepts/dspark|DSpark]]'s confidence-scheduled *verification trimming* is essential.
- **Memory-bound regime** (small batch, single user): the target's forward pass is dominated by weight loading, so verifying $\gamma + 1$ tokens costs almost the same as verifying 1. Speedups of $2$–$5\times$ are routine.
- **Open-ended generation** (chat): higher token entropy → lower $\alpha$ → smaller gain. Code and math, with more deterministic continuations, see the largest gains.

## References

- Leviathan, Y., Kalman, M., & Matias, Y. *Fast Inference from Transformers via Speculative Decoding*. ICML 2023. [arXiv:2211.17192](https://arxiv.org/abs/2211.17192)
- Chen, C. et al. *Accelerating Large Language Model Decoding with Speculative Sampling*. 2023. [arXiv:2302.01318](https://arxiv.org/abs/2302.01318)
- [[sources/zartbot-2026-dspark-speculative-decoding|zartbot 2026: DSpark投机解码的原理]] — the source of this page's content.
