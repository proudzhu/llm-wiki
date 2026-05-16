---
type: concept
created: 2026-05-16
updated: 2026-05-16
sources:
  - wiki/sources/kuang-2024-lightweight-speech-enhancement-bone-air.md
tags:
  - feature-fusion
  - multi-modal
  - attention
  - deep-learning
---

# Iterative Attentional Feature Fusion (iAFF)

**Iterative Attentional Feature Fusion (iAFF)** is a multi-modal fusion technique that performs coarse-then-refined feature integration using channel attention modules. Originally proposed by Dai et al. (2021) for visual tasks, it was adapted by Kuang, Yang & Yang (2024) for fusing bone-conducted (BC) and air-conducted (AC) speech spectrograms.

## Mechanism

iAFF operates in two stages:

### 1. Coarse Fusion
The two input signals are summed and fed through a channel attention module to obtain initial attention coefficients $\alpha'$:

$$
\alpha' = \mathcal{F}_{a1}\{\mathbf{y}_{AC} + \mathbf{y}_{BC}\}
$$
$$
\mathbf{y}_{AF}' = \alpha' \otimes \mathbf{y}_{AC} + (1 - \alpha') \otimes \mathbf{y}_{BC}
$$

### 2. Refined Fusion
The coarsely fused signal is passed through a second channel attention module to obtain refined coefficients $\alpha$:

$$
\alpha = \mathcal{F}_{a2}\{\mathbf{y}_{AF}'\}
$$
$$
\mathbf{y}_{AF} = \alpha \otimes \mathbf{y}_{AC} + (1 - \alpha) \otimes \mathbf{y}_{BC}
$$

### Channel Attention Module

The attention module computes both local and global context:
1. Average pooling over features within a frame (local context)
2. Global context averaging
3. Each passes through two PWConv layers with BN and PReLU
4. Local and global features are aggregated and passed through sigmoid for the attention coefficient

## Advantages

iAFF alleviates the "bottleneck of low-quality initial fusion" that can occur in single-stage attention fusion. By first fusing coarsely and then refining, it produces more robust attention weights. In the Kuang et al. (2024) ablation study, removing iAFF caused noticeable wb-PESQ degradation particularly at low SNRs.

## Applications

- Multi-modal speech enhancement (BC + AC fusion)
- Audio-visual fusion
- Any application requiring robust cross-modal attention weighting

## Related Concepts

- [[concepts/densely-gated-convolutional-attention-network|DenGCAN]]
- [[concepts/attention-gate|Attention Gate (AG)]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cRM)]]

## Related Sources

- [[sources/kuang-2024-lightweight-speech-enhancement-bone-air|Kuang, Yang & Yang 2024: A Lightweight Speech Enhancement Network Fusing Bone- and Air-Conducted Speech]]
