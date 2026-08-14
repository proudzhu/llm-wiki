---
type: concept
created: 2026-08-14
updated: 2026-08-14
tags:
  - neural-network
  - convolution
  - adaptive-processing
  - speech-coding
  - hybrid-dsp-dnn
---

# AdaConv

**AdaConv (Adaptive Convolution)** is a convolution layer whose weights are **adapted at a fixed rate from a latent feature vector**, rather than being fixed after training. It was proposed by Büthe, Valin & Mustafa in **LACE** (WASPAA 2023) for enhancing coded speech, and extended to multiple input/output channels in **NoLACE** (ICASSP 2024). In [[sources/buthe-2025-blind-wideband-to-fullband-extension|BBWENet (Büthe & Valin 2025)]], AdaConv implements the adaptive **pre- and post-filtering** of the classical time-domain bandwidth-extension signal path.

## Formulation

AdaConv behaves like a regular Conv1d layer, except its kernel weights $\mathbf{W}(t)$ are recomputed at a fixed rate (200 Hz in BBWENet) based on a latent feature vector $\phi(\cdot)$ produced by a small feature encoder:

$$
\mathbf{W}(t) = g(\phi(t))
$$

where $g$ is a small learned mapping from the latent feature sequence to kernel weights. The convolution itself remains a standard linear operation — only the weights are time-varying. This keeps the signal path cheap and interpretable (classical filtering) while letting a compact DNN steer the filter response to the signal's characteristics.

## Role in the Hybrid DSP/DNN Pipeline

In BBWENet's bandwidth-extension pipeline (pre-filtering → upsampling → extension → post-filtering), AdaConv modules provide the **time-varying linear filtering**:

- A **pre-filter** shapes the wideband signal before extension (e.g., spectral flattening to make folding more effective);
- A **post-filter** shapes the extended signal to match the target spectral envelope.

Both are steered by the latent features derived from the 72-dimensional ERB-spectrogram + phase-difference input. This is the key hybrid design move: the expensive adaptive computation lives in the small DNN feature encoder, while the audio path itself stays classical DSP.

## Distinction from Frame-Wise Adaptive Convolution (Wang et al. 2025)

The wiki also documents a different mechanism under [[concepts/adaptive-convolution|Adaptive Convolution]] (Wang et al., IEEE TASLPRO 2025): a frame-wise causal variant of dynamic convolution for speech *enhancement* that aggregates multiple candidate kernels with per-frame attention weights. The two are related in spirit (per-frame/rate-limited kernel adaptation for streaming audio) but differ in mechanism:

| Aspect | AdaConv (LACE/NoLACE/BBWENet) | Adaptive convolution (Wang et al. 2025) |
|---|---|---|
| Kernel generation | Weights mapped from a latent feature vector at a fixed rate (200 Hz) | Attention-weighted sum of $K$ learned candidate kernels per STFT frame |
| Adaptation rate | Fixed (200 Hz), decoupled from frame rate | Per STFT frame |
| Primary use | Time-varying filtering in hybrid DSP/DNN (codec enhancement, BWE) | Drop-in replacement for convolutions in CRN-based SE models |
| Origin | Büthe et al. WASPAA 2023 (LACE) | Wang et al. TASLPRO 2025 |

## Related Concepts

- [[concepts/adaptive-convolution|Adaptive Convolution (Wang et al. 2025)]] — a different, frame-wise dynamic-convolution mechanism for SE
- [[concepts/adashape|AdaShape]] — sibling adaptive module from NoLACE (sample-wise weighting instead of filter weights)
- [[concepts/blind-bandwidth-extension|Blind Bandwidth Extension]] — the task where AdaConv provides pre/post-filtering
- [[concepts/adaptive-filtering|Adaptive Filtering]] — classical counterpart: filter coefficients adjusted in real time from signal statistics

## Related Sources

- [[sources/buthe-2025-blind-wideband-to-fullband-extension|Büthe & Valin 2025: A Lightweight and Robust Method for Blind Wideband-to-Fullband Extension of Speech]] — uses AdaConv for adaptive pre/post-filtering in blind BWE
- [[sources/wang-2025-adaptive-convolution-cnn-speech-enhancement|Wang et al. 2025: Adaptive Convolution for CNN-based Speech Enhancement Models]] — the distinct frame-wise mechanism documented under [[concepts/adaptive-convolution|Adaptive Convolution]]
