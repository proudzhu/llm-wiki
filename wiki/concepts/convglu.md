---
type: concept
created: 2026-11-01
updated: 2026-11-01
sources:
  - raw/papers/yan-2025-lisennet/full-text.md
tags:
  - neural-network-architecture
  - gated-network
  - channel-mixing
  - speech-enhancement
---

# ConvGLU

**ConvGLU** (convolutional gated linear unit) is a channel-mixing module introduced in [[concepts/lisennet|LiSenNet]] (Yan et al., ICASSP 2025), modified from the Aggregated Attention design of TransNeXt (Shi 2023). It compensates for the modeling capacity lost when RNN hidden sizes are shrunk to meet real-time computational budgets.

## Structure

ConvGLU is composed of:

1. a **linear layer** (channel mixing),
2. a **depthwise convolution** ([[concepts/depthwise-separable-convolution|depthwise convolution]]) — aggregates information from the nearest channels,
3. a **Mish activation** (Misra 2019).

Operating as a channel mixer inside the dual-path recurrent bottleneck, the depthwise convolution provides local aggregation across channels, while the gate mechanism yields **fine-grained channel attention** — each channel's contribution is gated individually rather than uniformly weighted.

## Purpose and Effect

LiSenNet's dual-path recurrent module uses small GRUs (hidden 24 temporal / 12 frequency) so the model fits a 56M MACs/s budget; the RNN shrinkage would otherwise decay modeling capacity. ConvGLU restores inter-channel information fusion at low cost:

- Full LiSenNet: PESQ 3.07 / STOI 0.939 (37k params, 56M MACs/s)
- w/o ConvGLU: PESQ 2.98 / STOI 0.937 (31k params, 48M MACs/s)

Removing ConvGLU saves ~16% parameters and ~14% MACs but costs 0.09 PESQ — a favorable trade in favor of keeping it.

## Relation to Other Channel-Mixing Gates

- **GLU** (gated linear unit, Dauphin et al. 2017): $G(\mathbf{x}) = (\mathbf{x}\mathbf{W} + \mathbf{b}) \odot \sigma(\mathbf{x}\mathbf{V} + \mathbf{c})$ — ConvGLU replaces the second linear transform's global channel mixing with a depthwise convolution, making the gate locally aware.
- **[[concepts/gated-recurrent-unit|GRU]] gates** — recurrent, sequence-dependent gates; ConvGLU operates per frame independently.
- **[[concepts/adaptive-convolution|Adaptive convolution]]** — dynamic per-frame kernels; ConvGLU's kernels are static but spatially (channel-) local.

## Related Concepts

- [[concepts/lisennet|LiSenNet]]
- [[concepts/dprnn|Dual-Path RNN (DPRNN)]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit (GRU)]]
- [[concepts/adaptive-convolution|Adaptive Convolution]]

## Related Sources

- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]]
