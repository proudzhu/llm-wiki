---
type: concept
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/articles/dspark-speculative-decoding.md
tags:
  - llm-inference
  - speculative-decoding
  - deepseek
  - semi-autoregressive
  - confidence-scheduling
  - parallel-decoding
---

# DSpark

**DSpark** is [[entities/deepseek|DeepSeek]]'s open-source speculative decoding framework (released 2026 via the [DeepSpec](https://github.com/deepseek-ai/DeepSpec) repository), designed to overcome two bottlenecks of prior draft-model methods:

1. **Draft-quality decay** — parallel drafters like [[concepts/dflash\|DFlash]] generate all $\gamma$ tokens in one pass but cannot condition later positions on earlier sampled tokens, so acceptance rate collapses along the block.
2. **Verification inefficiency** — verifying every draft token regardless of confidence wastes target-model compute, especially under high concurrency where every verification slot has an opportunity cost.

DSpark addresses both with **semi-autoregressive generation** and **confidence-scheduled verification**, deployed in production on DeepSeek-V4.

## Speedup Decomposition

Average per-token latency is

$$
\bar{T} = \frac{T_d + T_v}{1 + \mathbb{E}[\text{accepted}]}
$$

so the three levers are: lower $T_d$ (faster drafting), raise acceptance $\alpha$ (better drafting), lower effective $T_v$ (smarter verification). DSpark pushes all three.

## Semi-Autoregressive Generation

The architecture splits drafting into two stages that run in sequence but share a single backbone forward pass.

### Parallel stage (backbone)

A DFlash-style bidirectional backbone (e.g., a 5-layer Qwen3-style decoder with `is_causal=False`) takes input $[\text{anchor}, \text{MASK}, \ldots, \text{MASK}]$ and produces base logits $b_k$ and hidden states $h_k$ for every position in one forward pass. Drafting latency is $O(1)$ in $\gamma$.

A small but important change from vanilla DFlash: the anchor itself is treated as the first prediction position, so $\gamma$ input tokens produce $\gamma$ draft logits (rather than $\gamma - 1$).

### Sequential stage (Markov or RNN head)

A *tiny* module adds a transition bias so each position can condition on the previously *sampled* token:

- **Markov head** — first-order transition, low-rank factorized:
  $$
  B(x_{k-1}) = W_2\, W_1[x_{k-1}], \qquad W_1 \in \mathbb{R}^{|V| \times r},\; W_2 \in \mathbb{R}^{r \times |V|}.
  $$
  This is just an embedding lookup + linear projection; the rank $r$ keeps both storage and per-step compute small.
- **RNN head** — GRU-like state $s_k$ accumulates the full prefix:
  $$
  s_k = g \odot s_{k-1} + (1 - g) \odot \tilde{s}, \quad B(x_{k-1}, h_k, s_{k-1}) = W_2\, \tanh(o_{\text{out}}).
  $$

Inference samples left-to-right:

$$
x_1 \sim \mathrm{softmax}(b_1), \quad x_k \sim \mathrm{softmax}(b_k + B(x_{k-1}, h_k)) \text{ for } k \geq 2.
$$

Because the serial head is shallow (default 2 layers vs. the backbone's 5), total drafting time grows by only ~1% relative to pure-parallel DFlash, while draft quality (measured by acceptance rate) improves by ~30%.

### Why "semi"-autoregressive matters

Pure parallel drafting marginalizes over all possible earlier tokens, producing inconsistent suffix combinations (e.g., "of problem" when "of course" and "no problem" are both plausible). The serial head, by conditioning on the actually-sampled prefix, suppresses these **multimodal collisions** and arrests the suffix-decay that limits DFlash's effective $\gamma$.

## Confidence-Scheduled Verification

### Confidence head

A linear layer + sigmoid predicts the conditional acceptance probability

$$
c_k = P\!\left(\text{draft}_k \text{ accepted} \;\middle|\; x_{<k} \text{ all accepted}\right).
$$

Inputs: backbone hidden state $h_k$ plus the previous token's Markov embedding $W_1[x_{k-1}]$. Supervision is the analytic per-step acceptance rate

$$
\alpha_k = 1 - \mathrm{TV}(p(\cdot|x_{<k}),\, q(\cdot|x_{<k})).
$$

### Sequential Temperature Scaling (STS)

Raw neural confidence is over-confident (ECE 3–8%). Because the scheduler (below) needs *absolute* survival probabilities — not just rankings — DSpark calibrates left-to-right: at each position $k$, do a 1-D grid search over a temperature $\tau_k$ that minimizes ECE on the cumulative product $\prod_{j \leq k} c_j^{(\tau)}$, holding earlier temperatures fixed. STS is monotonic, so it preserves the head's learned ordering while fixing the magnitudes. Post-STS ECE is ~1%.

### Hardware-aware prefix scheduler

For a batch of $N$ active requests with per-position survival probabilities $\{c_{i,k}\}$, choose verification lengths $\{l_i\}$ to maximize expected system throughput:

$$
\max_{\{l_i\}} \frac{\sum_{i=1}^{N} \sum_{k=1}^{l_i} \prod_{j \leq k} c_{i,j}}{\;T_{\text{forward}}\!\Big(\sum_i l_i\Big)\;}
$$

where $T_{\text{forward}}(B)$ is the engine's throughput-vs-batch profile, measured once at startup and stored as a cost table.

The objective is monotone in each $c_{i,k}$, so the optimal solution admits tokens in order of descending survival probability — a greedy queue. **Crucially, the scheduler stops as soon as the throughput curve peaks** (`break` in Algorithm 1). This is not just an optimization heuristic — it enforces **non-anticipation** (causality): without the early stop, the decision at position $k$ would implicitly depend on $c_{k+1}$, which is itself a function of the not-yet-sampled $x_k$. That leakage biases the sampling distribution and breaks the losslessness guarantee. (The article's Appendix A works through a concrete counter-example.)

## Training

Target model is frozen; embedding and LM head are shared and frozen. Only the backbone, serial head, and confidence head are trained.

Three losses, each position-weighted by $e^{-k/\gamma}$ (front positions dominate because a prefix rejection discards the entire block):

- $\mathcal{L}_{\text{CE}}$ — next-token cross-entropy against the ground truth.
- $\mathcal{L}_{\text{TV}}$ — L1 distance between draft and target distributions; directly minimizes $\mathrm{TV}(p, q)$ and hence maximizes acceptance rate.
- $\mathcal{L}_{\text{conf}}$ — BCE on the analytic acceptance-rate label $\alpha_k$.

Default weights: equal weighting of CE and TV, smaller weight on confidence.

Two system-level optimizations enable training at target-model scale (HAI-LLM framework):

- **Hidden-state communication**: workers exchange `hidden_size`-dim activations rather than $|V|$-dim full-vocabulary logits; the LM-head projection is applied locally on the draft-worker. Communication drops from $O(|V|)$ to $O(d)$ per token.
- **Anchor-bounded sequence packing**: many short anchor-bounded draft blocks are packed into a dense batch with token-level attention indices (not 2-D masks), keeping causality exact across packed blocks without padding waste.

## Experimental Findings

- **Parallel can beat autoregressive.** Despite parallel drafting's per-position independence, DSpark's deeper backbone wins at position 1 (e.g., math: 0.93 vs. EAGLE-3's 0.81). Position-1 correctness has the highest leverage — a rejection there discards the entire block — so the head start propagates.
- **A little autoregression is high-leverage.** A 2-layer serial head on DSpark beats a 5-layer pure-parallel DFlash, at ~1% drafting-time overhead and ~30% draft-quality gain.
- **Confidence head works.** Static-threshold sweep: chat acceptance rises 45.7% → 95.7% as the threshold filters low-confidence suffixes; STS reduces ECE from 3–8% to ~1%.

## Production Deployment

Deployed with DeepSeek-V4-Flash and DeepSeek-V4-Pro preview. With $\gamma$ set to a large block size and a Markov serial head:

- Under **matched throughput**, per-user generation speed improves **60–85%**.
- Under a **strict SLA**, DSpark sustains throughput levels the baseline cannot reach.

This is the first reported production deployment of parallel/semi-autoregressive speculative decoding at scale.

## Why It Matters

DSpark is the system that closes the loop on two threads the field had been pursuing separately:

- **Algorithmic** — combining parallel drafting's $O(1)$ latency with autoregressive drafting's conditional dependency.
- **Systems** — explicitly modeling verification as a throughput-maximization problem under hardware capacity constraints, not just a per-request speedup problem.

The confidence scheduler is the more consequential half: it makes speculative decoding's cost-benefit **adaptive to system load**, which is what high-concurrency serving actually requires.

## References

- DSpark paper: *Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation*. DeepSpec repository: [github.com/deepseek-ai/DeepSpec](https://github.com/deepseek-ai/DeepSpec).
- [[sources/zartbot-2026-dspark-speculative-decoding|zartbot 2026]] — line-by-line walkthrough of DSpark's architecture and code, the source of this page.
- Direct predecessor: [[concepts/dflash|DFlash]].
- Autoregressive baseline: [[concepts/eagle-speculative-decoding|EAGLE-3]].
