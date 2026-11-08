---
type: concept
created: 2026-05-16
updated: 2026-11-08
sources:
  - wiki/sources/kuang-2024-lightweight-speech-enhancement-bone-air.md
  - wiki/sources/kuang-2025-low-complexity-bc-speech-enhancement.md
  - wiki/sources/wu-2026-dbmif-multimodal-fusion.md
tags:
  - attention
  - deep-learning
  - skip-connection
  - speech-enhancement
---

# Attention Gate (AG)

An **Attention Gate (AG)** is a mechanism for selectively propagating relevant features through skip-connections in encoder-decoder architectures. Originally proposed by Oktay et al. (2018) for medical image segmentation (Attention U-Net), it was adapted and improved by Kuang, Yang & Yang (2024) for speech enhancement.

## Standard AG (Oktay et al. 2018)

The AG takes two inputs: the encoder feature map $\mathbf{X}_l$ (low-level features) and the decoder feature map $\mathbf{G}_{l+1}$ (higher-level semantic features). The decoder features provide "gating" signal that determines which spatial/spectral regions of the encoder features are relevant.

## Improved AG (Kuang, Yang & Yang 2024)

The improved AG considers both **local and global features** to compute attention coefficients:

1. **Feature fusion**: Input features $\mathbf{x}_d$ (from encoder) and $\mathbf{g}_d$ (from decoder) at position $d$ are summed
2. **Local information extraction**: PWConv with projection $\mathbf{W}_l$ on each feature pair
3. **Global information extraction**: Average pooling $\bar{\mathbf{x}}$ across all features, then PWConv with projection $\mathbf{W}_g$
4. **Attention coefficient**: Sigmoid of the combined local + global features:

$$
\bar{\mathbf{x}} = \frac{1}{D_l}\sum_{k=1}^{D_l}(\mathbf{x}_k + \mathbf{g}_k)
$$
$$
a_d = \sigma\{\mathbf{W}_l^T(\mathbf{x}_d + \mathbf{g}_d) + \mathbf{W}_g^T \bar{\mathbf{x}}\}
$$

5. **Feature scaling**: The scaled feature passes through a third PWConv:

$$
\hat{\mathbf{x}}_d = \mathbf{W}^T(a_d \mathbf{x}_d)
$$

## Types of Skip-Connections

| Type | Description | Performance (wb-PESQ) |
|------|------------|----------------------|
| Concatenation-based | Direct concat of encoder and decoder features | Baseline |
| PWConv-based | PWConv layer on skip features before fusion | +0.030 |
| **AG-based** | Attention-gated skip connections (local + global) | **+0.053** |

## Applications

- Speech enhancement encoder-decoder networks (DenGCAN)
- Medical image segmentation (Attention U-Net)
- Any U-Net style architecture where selective feature propagation improves efficiency

## Reuse in the Sub-Band/Full-Band Successor (Kuang et al. 2025)

[[sources/kuang-2025-low-complexity-bc-speech-enhancement|Kuang, Yang, Wang & Yang 2025]] retain the AG skip-connections in the small ERB encoder-decoder set of their [[concepts/sub-band-full-band-architecture|sub-band + full-band architecture]] (gain-estimation branch), while the large spectral encoder-decoder set (deep-filtering branch) uses cheaper pointwise-convolution skip-connections — a granularity-matched skip strategy: attention-gated skips where only 36 frequency features are reconstructed, PWConv skips for the 257-bin full-band path.

## Related Concepts

- [[concepts/densely-gated-convolutional-attention-network|DenGCAN]]
- [[concepts/iterative-attentional-feature-fusion|Iterative Attentional Feature Fusion (iAFF)]]
- [[concepts/dynamic-convolution|Dynamic Convolution]]
- [[concepts/cross-branch-gated-interaction|Cross-Branch Gated Interaction (CBGI)]] — bidirectional gating between parallel branches rather than within skip connections
- [[concepts/deep-iterative-attention-fusion|Deep Iterative Attention Fusion (DIAF)]] — channel attention iterated over a fusion estimate

## Related Sources

- [[sources/wu-2026-dbmif-multimodal-fusion|Wu et al. 2026: DBMIF]] — sigmoid gating applied bidirectionally between AC, BC and fusion streams (CBGI), the largest ablation contributor
- [[sources/kuang-2024-lightweight-speech-enhancement-bone-air|Kuang, Yang & Yang 2024: A Lightweight Speech Enhancement Network Fusing Bone- and Air-Conducted Speech]]
- [[sources/kuang-2025-low-complexity-bc-speech-enhancement|Kuang, Yang, Wang & Yang 2025: Low-Complexity BC-Aided Speech Enhancement]] — AG skips retained in the ERB branch; PWConv skips in the full-band branch
- [[sources/zhao-2026-halo-half-frame-rate-adaptive-operator|Zhao et al. 2026: HALO — Gated dynamic convolution for adaptive frame-rate reduction]]
