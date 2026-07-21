---
type: concept
created: 2026-07-21
updated: 2026-07-21
tags:
  - neural-network
  - speech-enhancement
  - lightweight-model
  - feature-fusion
  - attention
---

# Cross-Path Fusion (CPF)

**Cross-Path Fusion (CPF)** is a lightweight feature-fusion module introduced by Yang et al. (IEEE SPL 2026) in [[concepts/cofi-lite|CoFi-Lite]]. It bridges two parallel encoder-decoder paths (a coarse full-band path and a fine low-frequency path) at their bottlenecks, enabling **mutual** feature interaction — in contrast to cascaded coarse-to-fine designs, where information flows one way and errors accumulate.

## Formulation

Given the two paths' pre-bottleneck representations $\mathbf{E}_\mathrm{c}$ and $\mathbf{E}_\mathrm{f}$ (each of shape $C_i \times T \times F_i'$):

1. **Flatten & concatenate**: reshape each to $T \times (C_i \cdot F_i')$ and concatenate into a unified representation $\mathbf{E}_\text{in} \in \mathbb{R}^{T \times D}$, where $D = (C_1 \cdot F_1') + (C_2 \cdot F_2')$
2. **Bottleneck compression**: an FC layer compresses $D \rightarrow H$ to control complexity ($H = 76$ in the base model, 102 in the Large variant)
3. **Temporal modeling**: layer normalization + ELU, then a grouped GRU (2 groups) captures temporal patterns of the fused feature $\mathbf{Z}$
4. **Expansion & split**: a second FC restores dimension $D$; the output is split in two, reshaped back to $C_i \times T \times F_i'$, and combined with **skip connections** from the original $\mathbf{E}_\mathrm{c}, \mathbf{E}_\mathrm{f}$ to produce the fused features $\mathbf{D}_\mathrm{c}, \mathbf{D}_\mathrm{f}$

The design operates on the time axis only (features flattened over channel × frequency), so cost is dominated by the two FC layers; the $H$-dimensional bottleneck keeps this negligible.

## Efficacy

In CoFi-Lite's ablation (Table III, complexity-matched by Inter-RNN hidden size):

| Config | Params (k) | PESQ |
|--------|-----------|------|
| Dual paths, no CPF | 21.23 | 2.02 |
| No CPF, scaled to match CPF params | 90.80 | 2.06 |
| Dual paths + CPF | 83.12 | **2.16** |

CPF yields **+0.14 PESQ** over the unfused dual-path model, and +0.10 over a parameter-matched unfused model — evidence that the two paths' features are highly complementary and that their *interaction* (not merely added capacity) drives the improvement.

## Related Concepts

- [[concepts/cofi-lite|CoFi-Lite]]
- [[concepts/gtcrn|Grouped Temporal Convolutional Recurrent Network (GTCRN)]]
- [[concepts/dprnn|Dual-Path RNN (DPRNN)]]
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]]
- [[concepts/iterative-attentional-feature-fusion|Iterative Attentional Feature Fusion]]

## Related Sources

- [[sources/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement|Yang et al. 2026: CoFi-Lite — Pushing the Limits of Ultra-Lightweight Speech Enhancement]]
