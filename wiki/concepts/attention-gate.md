---
type: concept
created: 2026-05-16
updated: 2026-05-16
sources:
  - wiki/sources/kuang-2024-lightweight-speech-enhancement-bone-air.md
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

## Related Concepts

- [[concepts/densely-gated-convolutional-attention-network|DenGCAN]]
- [[concepts/iterative-attentional-feature-fusion|Iterative Attentional Feature Fusion (iAFF)]]

## Related Sources

- [[sources/kuang-2024-lightweight-speech-enhancement-bone-air|Kuang, Yang & Yang 2024: A Lightweight Speech Enhancement Network Fusing Bone- and Air-Conducted Speech]]
