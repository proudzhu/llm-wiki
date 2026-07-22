---
type: concept
created: 2026-04-25
updated: 2026-07-22
sources:
tags:
  - deep-learning
  - neural-network-architecture
  - audio-processing
  - active-noise-control
---

# Convolutional Recurrent Network

A **Convolutional Recurrent Network (CRN)** is a deep learning architecture that combines convolutional layers for spatial/spectral feature extraction with recurrent layers (typically LSTM) for temporal sequence modeling. Originally proposed by Tan and Wang for real-time speech enhancement, the CRN has become the dominant architecture for Deep ANC systems.

## Architecture

The CRN follows an **encoder-decoder** structure with a recurrent bottleneck:

1. **Convolutional Encoder**: Stacked 2D convolutional layers compress high-dimensional input (e.g., complex STFT) into compact feature representations. Frequency dimension is halved at each layer while channels double, learning translation-invariant spectral structures.

2. **Recurrent Bottleneck**: LSTM layers at the compressed bottleneck capture long-term temporal dependencies in the feature sequence. A linear projection layer often reduces dimensionality before the LSTM to limit parameter count.

3. **Transposed Convolutional Decoder**: Symmetric decoder restores the abstract features back to the original input dimensions via transposed convolutions (upsampling).

4. **Skip Connections**: Following U-Net design, encoder features are concatenated with decoder inputs at matching layers, preserving fine-grained details (especially phase information) that would otherwise be lost in the bottleneck.

## Key Design Principles for ANC

- **Causal convolution**: Asymmetric zero-padding (past-only) ensures the network never uses future information, making it suitable for real-time deployment
- **ELU activation**: Preferred over ReLU for audio spectra which contain negative values; ELU provides smoother gradients and faster convergence
- **Linear output**: Final decoder layer uses no activation function to directly output real/imaginary spectral components
- **Complex spectrum I/O**: Input and output are 2-channel (real + imaginary STFT), enabling [[complex-spectrum-mapping|Complex Spectrum Mapping]]

## Advantages for ANC

| Property | CNN Component | LSTM Component |
|----------|--------------|----------------|
| Feature extraction | Harmonic textures, spectral patterns | - |
| Temporal modeling | Local (via kernel) | Long-range dependencies |
| Nonlinear modeling | Implicit via deep layers | Implicit via gate mechanisms |
| Causality | Enforced via padding | Inherent (sequential processing) |

## Applications

- **Deep ANC**: End-to-end anti-noise generation (Zhang & Wang 2021, Dai 2026)
- **Speech Enhancement**: Real-time noise suppression (Tan & Wang 2018)
- **DCCRN**: Deep Complex CRN won 1st place in Interspeech 2020 Deep Noise Suppression Challenge
- **Attention Recurrent Network (ARN)**: CRN variant with attention for lower latency (Zhang et al. 2023)
- **GTCRN**: Grouped Temporal CRN with only 23.7 K parameters for edge-device speech enhancement (Rong et al. 2024, ICASSP)
- **[[concepts/cofi-lite|CoFi-Lite]]**: Dual coarse/fine-path CRN with [[concepts/cross-path-fusion|Cross-Path Fusion]], reaching 12.87M MACs/s while outperforming GTCRN (Yang et al. 2026, IEEE SPL)
- **[[concepts/adaptcrn|AdaptCRN]]**: Ultra-lightweight CRN pairing [[concepts/adaptive-convolution|adaptive convolution]] with a ConvNeXt/StarNet-inspired encoder-decoder, [[concepts/grouped-recurrent-neural-network|grouped]] [[concepts/dprnn|DPRNN]], and [[concepts/erb-scale|ERB]]-based spectral compression — 135K params, 41 MMACs/s, PESQ 2.98 on VCTK-DEMAND (Wang et al. 2025, IEEE TASLPRO). Same lab lineage as GTCRN and CoFi-Lite.
- **Audibility-estimation VAD**: Apostolidis et al. (2026) train a 2.9M-parameter CRN (5-layer causal conv encoder-decoder + 4 stacked LSTM layers, ELU + batchnorm, kernel $(3,2)$, frequency stride 2, sigmoid output) to estimate a per-T-F **audibility** map $\widehat{\mathrm{AUD}}(k,l) \in [0,1]$ inspired by the Speech Intelligibility Index. The CRN takes stacked real/imaginary STFT parts as input and is trained with MSE for 300 epochs (Adam, lr 0.016, batch size 32, Bayesian-optimized architecture). The audibility output drives both ideal-binary-mask construction for an [[concepts/mvdr-beamformer|MVDR]] baseline and [[concepts/glimpse-proportion|Glimpse Proportion]] computation for [[concepts/output-based-speech-enhancement|output-based]] [[concepts/mpdr-beamformer|MPDR]] candidate selection.

## Related Concepts

- [[deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[active-noise-control|Active Noise Control]]
- [[speech-preserving-anc|Speech-Preserving ANC]]
- [[selective-fixed-filter-anc|Selective Fixed-Filter ANC]]
- [[direction-of-arrival-estimation|Direction-of-Arrival Estimation]]

## Related Sources

- [[sources/dai-2026-speech-preserving-deep-anc|Dai 2026: Speech-Preserving Deep ANC]]
- [[sources/tan-2018-convolutional-recurrent-network-speech-enhancement|Tan & Wang 2018: CRN for Real-Time Speech Enhancement (original proposal)]]
- [[sources/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement|Yang et al. 2026: CoFi-Lite — Pushing the Limits of Ultra-Lightweight Speech Enhancement]] — dual coarse/fine-path CRN decoupling spectral modeling at 12.87M MACs/s
- [[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng et al. 2023: Sixty Years of Frequency-Domain Monaural Speech Enhancement]] — surveys CRN family evolution (CRN → DCCRN → DPCRN → GCRN) and decoupling-style successors
- [[sources/apostolidis-2026-listen-first-output-based-multi-microphone|Apostolidis et al. 2026: Listen first — output-based multi-microphone speech enhancement]] — CRN used as audibility-estimating neural VAD for output-based MPDR selection
- [[sources/wang-2025-adaptive-convolution-cnn-speech-enhancement|Wang et al. 2025: Adaptive Convolution for CNN-based Speech Enhancement Models]] — applies [[concepts/adaptive-convolution|adaptive convolution]] across the CRN family (DPCRN at 3 scales, DCCRN, GTCRN, LiSenNet); proposes [[concepts/adaptcrn|AdaptCRN]]
