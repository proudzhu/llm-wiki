---
type: concept
created: 2026-06-06
updated: 2026-07-16
tags:
  - speech-enhancement
  - echo-cancellation
  - signal-processing
---

# Acoustic Echo Cancellation (AEC)

**Acoustic Echo Cancellation (AEC)** removes acoustic echo from microphone signals in communication systems. Echo occurs when the far-end signal played through a loudspeaker is picked up by the microphone via room reflections, degrading call quality.

## Problem Formulation

The microphone signal contains:
- Near-end speech (desired)
- Acoustic echo from far-end signal (undesired)
- Background noise
- Reverberation

The goal is to estimate and subtract the echo component, or equivalently learn a filter that suppresses echo while preserving near-end speech.

## Traditional Approaches

| Method | Description | Key Property |
|--------|-------------|--------------|
| **Adaptive filtering (NLMS, RLS)** | Estimates echo path impulse response | Requires double-talk detection |
| **Linear echo canceller (LAEC)** | DSP-based adaptive filter | Foundation for hybrid systems |
| **Delay compensation** | Aligns mic and far-end signals | Critical for AEC performance |

## Deep Learning Approaches

| Method | Description | Key Property |
|--------|-------------|--------------|
| **Hybrid DL+AEC** | DL post-processor after LAEC | Combines interpretability with learning |
| **End-to-end DL** | Pure neural network AEC | No explicit echo path estimation |
| **Cross-attention alignment** | Soft alignment in feature space | Replaces DSP delay compensator |

## Key Challenges

- **Double-talk scenarios**: Near-end and far-end speech overlap
- **Time-varying echo paths**: Room acoustics change with movement
- **Long delays**: Echo delays up to 1 second in large rooms
- **Nonlinear distortion**: Loudspeaker and microphone nonlinearities

## Evaluation Metrics

- **ERLE** (Echo Return Loss Enhancement): Measures echo suppression in far-end single-talk
- **AECMOS**: MOS-based echo quality score for both single-talk and double-talk
- **WER** (Word Error Rate): ASR-based intelligibility metric

## Lightweight / PercepNet-Style Hybrid AEC

A complementary line of work targets ultra-low-complexity AEC for edge devices. These systems share the PercepNet pattern (Valin et al. ICASSP 2021): a linear adaptive filter removes the bulk of the linear echo, then a small neural network operating on [[concepts/bark-scale-spectral-features|Bark-scale perceptual features]] predicts a gain mask for residual echo suppression.

| System | Params | MACs/s | ST FE EchoMOS | DT EchoMOS | Notes |
|--------|-------:|-------:|--------------:|-----------:|-------|
| ULCNet-AER (Shetu 2024) | 1.12M | 173M | 2.89 | 2.68 | Sub-band interleaved DNN |
| Bark-AEC (Seidel 2024) | 1.62M | 107M | 3.16 | 2.96 | FC + GRU on Bark features |
| DeepVQE-S (Indenbom 2023) | 0.82M | 315M | 4.13 | 3.96 | Residual CNN + CCM |
| **EchoFree** (Li 2025) | **0.28M** | **30M** | **4.20** | **3.88** | U-Net on Bark + two-stage SSL training |

EchoFree achieves DeepVQE-S-comparable single-talk performance at ~10× lower compute via three combined techniques: [[concepts/bark-scale-spectral-features|Bark-scale]] input compression (257 → 100), a [[concepts/u-net-post-filter|U-Net post filter]] with [[concepts/depthwise-separable-convolution|depthwise separable convolutions]] and [[concepts/sub-pixel-convolution|sub-pixel upsampling]], and a two-stage training strategy using frozen [[concepts/self-supervised-speech-representation|WavLM-Large SSL embeddings]] for coarse-to-fine spectral learning.

## Related Concepts

- [[concepts/cross-attention-alignment|Cross-Attention Alignment]]
- [[concepts/complex-convolving-mask|Complex Convolving Mask]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]]
- [[concepts/u-net-post-filter|U-Net Post Filter]]
- [[concepts/percepnet-style-neural-post-filter|PercepNet-Style Neural Post Filter]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]
- [[concepts/sub-pixel-convolution|Sub-Pixel Convolution]]
- [[concepts/frequency-domain-kalman-filter|Frequency-Domain Kalman Filter]]

## Related Sources

- [[sources/indenbom-2023-deepvqe|Indenbom et al. 2023: DeepVQE]]
- [[sources/shetu-2024-hybrid-low-complexity-aenr|Shetu et al. 2024: Hybrid Low-Complexity AENR]]
- [[sources/li-2025-echofree-neural-aec|Li et al. 2025: EchoFree]]
