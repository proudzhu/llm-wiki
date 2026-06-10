---
type: concept
created: 2026-06-10
updated: 2026-06-10
sources:
  - raw/papers/lydaki-2026-deep-feedback-cancellation-hearing-aids/full-text.md
tags:
  - hearing-aids
  - feedback-cancellation
  - deep-learning
  - system-identification
  - impulse-response-estimation
---

# Deep Feedback Cancellation

**Deep Feedback Cancellation (DFC)** is a deep learning approach to [[concepts/hearing-aid-feedback-cancellation|hearing aid feedback cancellation]] that directly estimates the feedback-path impulse response using a compact DNN. Unlike prior methods that predict the clean output signal, DFC exploits the constrained solution space of plausible IRs to achieve superior performance with a small model.

## Core Idea

Instead of predicting the clean signal (which can be any real-world sound), DFC predicts the feedback-path IR — a much more constrained target determined by the physical positions of the microphone and receiver. This allows a small DNN (856K parameters) to outperform larger models (8.7M parameters for DeepMFC).

## Architecture

1. **STFT** → log magnitude + phase features from loudspeaker and microphone signals
2. **Causal convolution** (2 layers, kernels (4,5), dilations (2,1)) with skip connection
3. **FC1** (LeakyReLU) → **LSTM** (128 hidden) → **FC2+FC3** (tanh)
4. **AveragePooling** (N=50) + **exponential smoothing** (α=0.5)
5. Output: estimated feedback-path IR f̂(n)

The estimated IR is subtracted from the microphone signal in the time domain, canceling the feedback component.

## NESD Loss with Temporal Smoothing

The [[concepts/normalized-euclidean-system-distance|NESD]] loss with average pooling encourages consistent IR estimates across frames:

```
L_NESD = (1/N) · Σ ||f(n-i) - f̂(n-i)||² / ||f(n-i)||²
```

Without smoothing: lower steady-state error but much slower convergence. With smoothing: resolves the convergence speed vs steady-state error trade-off.

## Key Properties

| Property | Value |
|----------|-------|
| Parameters | 856K (10x smaller than DeepMFC) |
| RTF | 0.10 |
| Convergence after path change | ~0.5s (30x faster than FD-AFC) |
| PESQ (speech) | 4.54 (vs 4.34 FD-AFC, 4.35 DeepMFC) |
| PEAQ (music) | -0.53 (vs -2.31 FD-AFC, -0.92 DeepMFC) |
| MUSHRA (speech) | 86.13 (vs 57.48 FD-AFC, 37.45 DeepMFC) |

## Why IR Prediction Beats Signal Prediction

1. **Constrained solution space**: Plausible hearing aid IRs are limited by physical microphone/receiver geometry
2. **Error tolerance**: Inaccuracies in less important IR coefficients have minimal impact on the transfer function
3. **Signal independence**: The IR estimation task is independent of the input signal type, enabling cross-domain generalization (speech model works on music and vice versa)
4. **Smaller model suffices**: The constrained target space requires less representational capacity

## Comparison with Other Methods

| Method | Approach | Adaptation | Biased Estimation |
|--------|----------|------------|-------------------|
| FD-AFC | Adaptive filter (NLMS/KF) | Explicit | Yes (correlated signals) |
| DeepMFC | DNN predicts clean output | None (open-loop) | No, but fails on path changes |
| Neural-AFC | DNN controls AF step-size | Via AF | Partially |
| **DFC** | **DNN predicts feedback IR** | **Implicit (temporal)** | **No** |

## Related Concepts

- [[concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]]
- [[concepts/normalized-euclidean-system-distance|Normalized Euclidean System Distance]]
- [[concepts/maximum-stable-gain|Maximum Stable Gain]]
- [[concepts/acoustic-feedback|Acoustic Feedback]]
- [[concepts/adaptive-feedback-control|Adaptive Feedback Control]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]

## Related Sources

- [[sources/lydaki-2026-deep-feedback-cancellation-hearing-aids|Lydaki 2026: Deep Feedback Cancellation in Hearing Aids]] — Full analysis and evaluation
- [[sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]] — Deep learning step-size control for traditional AFC
