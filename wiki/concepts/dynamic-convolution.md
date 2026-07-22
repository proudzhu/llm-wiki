---
type: concept
created: 2026-06-18
updated: 2026-07-22
sources:
  - raw/papers/wang-2025-adaptive-convolution-cnn-speech-enhancement/full-text.md
tags:
  - neural-network
  - convolution
  - adaptive-processing
  - efficient-inference
---

# Dynamic Convolution

**Dynamic convolution** is a technique where the convolution kernel is conditioned on the input, rather than being fixed after training. By aggregating multiple parallel kernels with input-dependent mixture weights, dynamic convolution increases model expressiveness with modest additional FLOPs.

## Formulation

A dynamic convolution layer maintains a kernel bank $\{W_k\}_{k=1}^K$ and predicts mixture weights $\alpha_k(x)$ via a lightweight gating network:

$$y = \sum_{k=1}^K \alpha_k(x) \, (W_k * x)$$

where $\alpha_k(x) \geq 0$ and $\sum_k \alpha_k(x) = 1$. The gating network is typically a small MLP or pointwise convolution followed by softmax.

## Key Variants

| Variant | Weight Prediction | Key Innovation |
|---------|-------------------|----------------|
| CondConv (Yang et al. 2019) | Global pooling + FC + softmax | Kernel mixing conditioned on entire input |
| DynamicConv (Chen et al. 2020) | Global + per-position | Two-stage weight generation |
| Per-pixel convolution (Wang et al. 2021) | T-F-dependent weights | Position-wise conditioning for spectrograms |
| ODConv (Li et al. 2022) | Multi-dimensional attention (spatial, channel, filter, kernel) | Complementary attention across kernel-space dimensions |
| **Adaptive convolution** (Wang et al. 2025) | **Per-frame**, frequency-only power pooling + temporal (GRU) channel modeling | Frame-wise causal dynamic convolution for streaming SE — see [[concepts/adaptive-convolution\|Adaptive Convolution]] |

## Applications

- **Efficient model scaling**: More parameters without proportional FLOPs increase
- **Adaptive processing**: Content-aware filtering for non-stationary signals
- **Frame-rate conversion**: Used in [[sources/zhao-2026-halo-half-frame-rate-adaptive-operator|HALO]] for adaptive frame-rate reduction and restoration in STFT-based speech enhancement
- **Frame-wise causal SE**: [[concepts/adaptive-convolution|Adaptive convolution]] (Wang et al. 2025) specializes dynamic convolution for streaming speech enhancement by pooling along frequency only and using a GRU for temporal channel modeling. It yields large quality gains on lightweight CNN SE backbones (DPCRN, DCCRN, GTCRN, LiSenNet) and underpins the ultra-lightweight [[concepts/adaptcrn|AdaptCRN]] (41 MMACs/s, 135K params). Two CV-recommended techniques — temperature annealing and softmax normalization — are shown to provide **no benefit** in SE, an important negative result for CV→SE transfer.

## Related Concepts

- [[concepts/attention-gate|Attention Gate / Gating Mechanisms]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/adaptive-convolution|Adaptive Convolution]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]

## Related Sources

- [[sources/zhao-2026-halo-half-frame-rate-adaptive-operator|Zhao et al. 2026: HALO — Half-frame-rate Adaptive Learnable Operator]]
- [[sources/wang-2025-adaptive-convolution-cnn-speech-enhancement|Wang et al. 2025: Adaptive Convolution for CNN-based Speech Enhancement Models]]
