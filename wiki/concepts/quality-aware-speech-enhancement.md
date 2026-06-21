---
type: concept
created: 2026-06-21
updated: 2026-06-21
sources:
  - wiki/sources/han-2026-quality-aware-earable-se.md
tags:
  - speech-enhancement
  - quality-aware
  - multi-modal-fusion
  - self-supervised
  - earable
  - modality-imbalance
---

# Quality-Aware Speech Enhancement

**Quality-Aware Speech Enhancement** is a multi-modal fusion paradigm that dynamically adjusts the contribution of an auxiliary modality (e.g., in-ear speech) based on a self-assessed quality metric, mitigating the negative impact of quality-varying or degraded auxiliary signals on the primary modality (e.g., airborne speech).

## Overview

Traditional multi-modal speech enhancement assumes that auxiliary modalities provide stable, high-quality complementary information. In practice, auxiliary modality quality can fluctuate unpredictably due to physical phenomena such as [[concepts/ear-canal-deformation|Ear Canal Deformation (ECD)]], sensor failure, or environmental interference. Naively fusing a degraded auxiliary modality introduces **modality imbalance** and can degrade overall enhancement performance.

Quality-aware speech enhancement addresses this by:
1. **Assessing** auxiliary modality quality without reference signals (self-supervised)
2. **Embedding** the quality metric into a learnable representation
3. **Weighting** auxiliary features by quality before cross-modal fusion

## Key Components (QuaSE Framework)

### 1. Self-supervised Quality Assessment

An autoencoder is trained **only on high-quality** auxiliary spectrograms. At inference, the reconstruction error (mean absolute error between input and output) serves as the quality metric — low-quality inputs (with distorted spectral structure) produce large reconstruction errors. This avoids the need for clean reference speech, which is unavailable in real-world noisy environments.

### 2. Quality Embedding Generation

The quality matrix is transformed into a feature-map-compatible embedding via:
- **Frequency squeeze**: 1×1 convolution + global average pooling along frequency (valid because ECD-induced attenuation is frequency-independent at a given time)
- **Quality learning**: Fully-connected layers with ReLU + Sigmoid, producing weights in [0, 1]
- **Unsqueeze**: Expand back to match feature map dimensions ($C \times F \times T$)

### 3. Quality-aware Cross Fusion

The quality embedding multiplies the auxiliary feature map, then weighted auxiliary features are concatenated with primary features. A lightweight attention module (CBAM) refines the fused representation.

## Reference-free Quality Selection

To obtain high-quality training data for the quality assessor, a **spectral peak-to-valley matching** strategy exploits cross-channel correlation in the low-frequency band (100–1000 Hz):
- Extract FFT magnitude spectrum envelopes of both channels
- Detect peaks and valleys via local extrema
- **Greedy matching**: Compute peak/valley matching rate and location error
- **First-order difference DTW alignment**: Align interval sequences to capture rhythm similarity
- Combine into a similarity score; threshold classifies high vs. low quality

See [[concepts/dynamic-time-warping|Dynamic Time Warping]] for the alignment algorithm.

## Content-aware Data Augmentation

To improve robustness to low-quality auxiliary speech, **content-aware adaptive time masking** simulates ECD-induced distortion. Unlike random masking, mask probability per time bin is conditioned on the spectral energy distribution, producing realistic low-quality samples from synthesized high-quality data.

## Distinction from Sensor-Failure Robust Fusion

Quality-aware SE is related to but distinct from [[concepts/sensor-failure-robust-fusion|Sensor-Failure Robust Fusion]]:
- **Sensor-failure robust fusion** (e.g., Liu 2025 ATFA) handles *binary* sensor failure (present/absent) via random modality dropout during training
- **Quality-aware SE** handles *continuous* quality variations (partial degradation) via dynamic quality-weighted fusion, providing finer-grained adaptation

## Related Concepts

- [[concepts/ear-canal-deformation|Ear Canal Deformation]]
- [[concepts/ear-canal-occlusion-effect|Ear Canal Occlusion Effect]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/bone-conduction|Bone Conduction]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/dynamic-time-warping|Dynamic Time Warping]]
- [[concepts/sensor-failure-robust-fusion|Sensor-Failure Robust Fusion]]
- [[concepts/pesq|PESQ]]

## Related Sources

- [[sources/han-2026-quality-aware-earable-se|Han et al. 2026: QuaSE — Quality-Aware Earable Dual-Microphone SE]]
