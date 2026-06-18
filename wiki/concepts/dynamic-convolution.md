---
type: concept
created: 2026-06-18
updated: 2026-06-18
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

## Applications

- **Efficient model scaling**: More parameters without proportional FLOPs increase
- **Adaptive processing**: Content-aware filtering for non-stationary signals
- **Frame-rate conversion**: Used in [[sources/zhao-2026-halo-half-frame-rate-adaptive-operator|HALO]] for adaptive frame-rate reduction and restoration in STFT-based speech enhancement

## Related Concepts

- [[concepts/attention-gate|Attention Gate / Gating Mechanisms]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]

## Related Sources

- [[sources/zhao-2026-halo-half-frame-rate-adaptive-operator|Zhao et al. 2026: HALO — Half-frame-rate Adaptive Learnable Operator]]
