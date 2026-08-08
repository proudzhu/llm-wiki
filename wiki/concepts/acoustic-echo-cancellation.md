---
type: concept
created: 2026-06-06
updated: 2026-08-08
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

A complementary line of work targets ultra-low-complexity AEC for edge devices. These systems share the [[concepts/percepnet-style-neural-post-filter|PercepNet-style pattern]] (Valin et al. ICASSP 2020/2021): a linear adaptive filter removes the bulk of the linear echo, then a small neural network operating on perceptually-spaced features (ERB or Bark) predicts a gain mask for residual echo suppression.

| System | Params | MACs/s | ST FE EchoMOS | DT EchoMOS | Notes |
|--------|-------:|-------:|--------------:|-----------:|-------|
| [[concepts/percepnet\|PercepNet]] (Valin 2021) | 8M | 800M | 4.19 (P.831 DMOS) | 4.34 (P.831 DMOS) | 32 ERB bands; 2 conv + 5 GRU; pitch coherence + comb filter; 1st place ICASSP 2021 AEC Challenge |
| ULCNet-AER (Shetu 2024) | 1.12M | 173M | 2.89 | 2.68 | Sub-band interleaved DNN |
| Bark-AEC (Seidel 2024) | 1.58M | 235M | — (graphical) | — (graphical) | NSNet2-style FC+GRU on 86 Bark bands; CCMSE + STFT consistency loss |
| DeepVQE-S (Indenbom 2023) | 0.82M | 315M | 4.13 | 3.96 | Residual CNN + CCM |
| **EchoFree** (Li 2025) | **0.28M** | **30M** | **4.20** | **3.88** | U-Net on Bark + two-stage SSL training |

> **Note on PercepNet's scale**: The original PercepNet uses the [[concepts/erb-scale|ERB scale]] (32 bands), **not** the [[concepts/bark-scale-spectral-features|Bark scale]] used by Bark-AEC and EchoFree. The "PercepNet-style" pattern name refers to the hybrid AEC + perceptual-band neural post filter architecture, not strictly to the Bark scale. PercepNet's MOS values are P.831 DMOS (not directly comparable to AECMOS used by later works), and it won 1st place out of 17 submissions in the ICASSP 2021 AEC Challenge.

> **Note on Bark-AEC numbers**: The original [[sources/seidel-2024-bark-scale-nn-residual-suppression|Seidel et al. 2024]] paper reports **1.58M params / 235 MMACs/s / 86 Bark bands** and presents AECMOS results graphically (no numeric table). The numeric values "1.62M / 107M / 3.16 / 2.96" cited in [[sources/li-2025-echofree-neural-aec|EchoFree (Li 2025)]] appear to differ from the original paper's self-reported numbers — possibly due to different counting methodologies or a different model variant.

EchoFree achieves DeepVQE-S-comparable single-talk performance at ~10× lower compute via three combined techniques: [[concepts/bark-scale-spectral-features|Bark-scale]] input compression (257 → 100), a [[concepts/u-net-post-filter|U-Net post filter]] with [[concepts/depthwise-separable-convolution|depthwise separable convolutions]] and [[concepts/sub-pixel-convolution|sub-pixel upsampling]], and a two-stage training strategy using frozen [[concepts/self-supervised-speech-representation|WavLM-Large SSL embeddings]] for coarse-to-fine spectral learning.

## Historical Context

[[sources/richard-2023-audio-signal-processing-21st-century|Richard et al. 2023]] trace AEC from its 1960s origins through the adaptive-filter generation already surveyed at the SPS 50th anniversary (RLS, affine projection, subband, and frequency-domain adaptive filters, plus double-talk detectors) that made hands-free telephony and modern videoconferencing possible. Subsequent advances tackled loudspeaker/microphone nonlinearities (including DNN-based nonlinear AEC), combined AEC + dereverberation + noise-reduction postfiltering, multichannel and MIMO/wave-domain AEC, and step-size control evolving from double-talk detection through Kalman-filter-based schemes to Kalman + deep-learning step-size optimization. The International Workshop on Acoustic Echo and Noise Control (IWAENC, 1989→, later renamed International Workshop on Acoustic Signal Enhancement) tracks the field.

## Related Concepts

- [[concepts/cross-attention-alignment|Cross-Attention Alignment]]
- [[concepts/complex-convolving-mask|Complex Convolving Mask]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]]
- [[concepts/u-net-post-filter|U-Net Post Filter]]
- [[concepts/percepnet-style-neural-post-filter|PercepNet-Style Neural Post Filter]]
- [[concepts/nsnet2|NSNet2]]
- [[concepts/oversampled-filterbank|Oversampled Filterbank]]
- [[concepts/complex-compressed-mse|Complex Compressed MSE (CCMSE)]]
- [[concepts/stft-consistency|STFT Consistency]]
- [[concepts/dtln|DTLN]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]
- [[concepts/sub-pixel-convolution|Sub-Pixel Convolution]]
- [[concepts/frequency-domain-kalman-filter|Frequency-Domain Kalman Filter]]
- [[concepts/pi-nlms|Physics-Informed NLMS (PI-NLMS)]]
- [[concepts/residual-echo-suppression|Residual Echo Suppression]]
- [[concepts/psychoacoustic-postfilter|Psychoacoustic Postfilter]]
- [[concepts/error-recovery-nonlinearity|Error Recovery Nonlinearity (ERN)]]

## Related Sources

- [[sources/indenbom-2023-deepvqe|Indenbom et al. 2023: DeepVQE]]
- [[sources/shetu-2024-hybrid-low-complexity-aenr|Shetu et al. 2024: Hybrid Low-Complexity AENR]]
- [[sources/seidel-2024-bark-scale-nn-residual-suppression|Seidel, Mowlaee & Fingscheidt 2024: Bark-Scale NN for RES+NS]]
- [[sources/li-2025-echofree-neural-aec|Li et al. 2025: EchoFree]]
- [[sources/castelli-2025-embedded-joint-aec-ns|Castelli 2024: Embedded Joint AEC and NS]]
- [[sources/scarpiniti-2027-physics-informed-adaptive-filtering-aec|Scarpiniti, Comminiello & Uncini 2027: Physics-informed adaptive filtering for AEC]]
- [[sources/richard-2023-audio-signal-processing-21st-century|Richard et al. 2023: Audio Signal Processing in the 21st Century]] — 25-year retrospective of the AEC field and the IWAENC workshop series
- [[sources/wung-2011-residual-echo-suppression-system|Wung et al. 2011: A System Approach to RES]] — robust AEC with ERN + batch adaptation (DTD-free) feeding a system-level residual echo estimate and psychoacoustic postfilter
