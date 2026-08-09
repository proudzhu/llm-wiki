---
type: concept
created: 2026-08-09
updated: 2026-08-09
sources:
  - raw/papers/lin-2023-tinyml-progress-futures/full-text.md
tags:
  - tinyml
  - on-device-training
  - efficient-deep-learning
  - microcontroller
  - memory-optimization
---

# Sparse Update

**Sparse Update** is the MCUNetV3 algorithm-side technique that enables on-device transfer learning on microcontrollers by selectively updating only a *subset* of layers (sparse layer update) and a *subset* of channels within an updated layer (sparse tensor update), plus bias updates on a separate sparsity axis. Combined with [[concepts/quantization-aware-scaling\|Quantization-Aware Scaling (QAS)]] on the algorithm side and compiled by the [[concepts/tiny-training-engine\|Tiny Training Engine (TTE)]] on the system side, sparse update achieves 4.5–7.5× smaller extra memory than updating the last $k$ layers *at equal or higher accuracy*, fitting on-device training within 256 kB SRAM. It is surveyed in [[sources/lin-2023-tinyml-progress-futures\|Lin et al. 2023: TinyML — Progress and Futures]].

## Motivation

Updating the whole model — or even the last several blocks — on a microcontroller is infeasible because every trainable weight needs a stored gradient and (on MCU) a Flash-resident copy in addition to the original read-only weights. Naive baselines:

- **Classifier-only update** — cheap but accuracy is low; the backbone cannot adapt to domain shift.
- **Bias-only update** (à la TinyTL) — better than classifier-only but accuracy plateaus quickly because biases alone have limited expressivity.
- **Last-$k$-layers update** — accuracy grows with $k$, but memory blows past 256 kB once $k$ exceeds ~2 blocks.

Sparse update fills the gap: more expressive than bias-only, far cheaper than last-$k$-layers.

## Three Sparsity Axes

For a linear layer $\mathbf{y} = \mathbf{W}\mathbf{x} + \mathbf{b}$ with gradient update $\mathbf{G_W} = f_1(\mathbf{G_y}, \mathbf{x})$ and $\mathbf{G_b} = f_2(\mathbf{G_y})$:

1. **Bias update** — biases are cheap (no input activation $\mathbf{x}$ needed for $\mathbf{G_b}$), so the number of layers $k$ that backpropagate and update biases is the *cheap* axis: update biases wherever the layer is backpropagated.
2. **Sparse layer update** — pick a subset $\mathbf{i}$ of layers whose *weights* are updated; layers not in $\mathbf{i}$ have their backward graph pruned entirely.
3. **Sparse tensor update** — within an updated layer, update only a fraction $r \in \{1/8, 1/4, 1/2, 1\}$ of weight channels, further reducing the gradient memory.

The combination $(k, \mathbf{i}, \mathbf{r})$ spans ~$10^{30}$ configurations for a 43-layer MCUNet — exhaustive search is intractable, so an automated selection procedure is required.

## Automated Selection via Contribution Analysis

Sparse update is derived by *contribution analysis*: for each candidate (layer, channel-ratio), measure its marginal accuracy improvement $\Delta\text{acc}$ relative to a baseline, then solve

$$
k^{*},\ \mathbf{i}^{*},\ \mathbf{r}^{*} = \arg\max_{k,\mathbf{i},\mathbf{r}} \left(\Delta\text{acc}_{\mathbf{b}[:k]} + \sum_{i \in \mathbf{i},\, r \in \mathbf{r}} \Delta\text{acc}_{\mathbf{W}_{i}, r}\right) \quad \text{s.t.} \quad \text{Memory}(k, \mathbf{i}, \mathbf{r}) \leq \text{constraint}.
$$

The optimization is solved efficiently with evolutionary search. Empirically, the per-tensor $\Delta\text{acc}$ contributions are *approximately additive* — the searched scheme matches or exceeds the accuracy of the best last-$k$-layers baseline ("upper bound") while consuming 4.5–7.5× less extra memory.

Two consistent findings from the contribution analysis (MCUNet on Cars):

- **Later layers contribute more** than earlier ones to downstream accuracy.
- **The first point-wise conv (`pw1`) of each inverted-bottleneck block** is the most important weight to update; more channels updated → larger gain.

## Empirical Impact

- Same accuracy as the last-$k$-layers upper bound at 4.5–7.5× smaller extra (analytic) memory.
- When compiled with [[concepts/tiny-training-engine\|TTE]] (which prunes the backward graph for frozen tensors and reorders operators for in-place gradient updates), sparse update yields **20–21× measured peak-memory reduction** and **23–25× faster training** vs. full-update + TF-Lite Micro kernels — fitting training of three different MCUNet models into 256 kB SRAM.

## Related Concepts

- [[concepts/quantization-aware-scaling\|Quantization-Aware Scaling (QAS)]] — companion algorithm fix for *how* to update the selected tensors on a quantized graph
- [[concepts/tiny-training-engine\|Tiny Training Engine (TTE)]] — system that compiles sparse update into measured memory savings via backward-graph pruning
- [[concepts/tinyml\|TinyML]] — problem domain
- [[concepts/online-learning\|Online Learning]]
- [[concepts/continuous-learning\|Continuous Learning]]

## Related Sources

- [[sources/lin-2023-tinyml-progress-futures\|Lin et al. 2023: TinyML — Progress and Futures]] — surveys sparse update as part of MCUNetV3
