---
type: source
created: 2026-04-18
updated: 2026-04-28
sources:
  - raw/papers/holzmueller-2026-obs-tasnet-virtual-sensing/full-text.txt
  - https://doi.org/10.1051/aacus/2026027
  - zotero://select/items/0_WY4S7C6Z
tags:
  - active-noise-control
  - conv-tasnet
  - deep-learning
  - tcn
  - virtual-sensing
aliases:
  - 'Holzmüller 2026: Obs-TasNet for Virtual Sensing ANC'
---

# Holzmüller 2026: Obs-TasNet: Online Estimation of Virtual Sensing Observation Filters for Active Noise Control

**Authors**: Felix Holzmüller, Alois Sontacchi
**Institution**: University of Music and Performing Arts Graz, Austria
**Published**: Acta Acustica (Accepted version), 2026
**DOI**: [10.1051/aacus/2026027](https://doi.org/10.1051/aacus/2026027)
**📎 Zotero**: [zotero://select/items/0_WY4S7C6Z](zotero://select/items/0_WY4S7C6Z)
**Code**: [GitHub](https://github.com/fholzm/Obs-TasNet)

## Summary

This paper introduces **Obs-TasNet**, an asynchronous neural network architecture designed to estimate the observation filters of the **Remote Microphone Technique (RMT)** online. It solves the critical challenge of **time-variant environments** (e.g., a moving listener) in local ANC without requiring offline pre-optimization, scene detection, or manual interpolation.

## Problem Formulation

### Handling Time-Variance in Local ANC

In local ANC, the **Zone of Quiet (ZoQ)** is small (~1/10th wavelength). Traditional virtual sensing (like fixed RMT) assumes a static relationship between remote and virtual microphones. When a listener moves (time-variant PoC), fixed filters diverge, causing system instability.

**Previous Solutions**:
- **Switching**: Optimize for a grid of points and switch based on detection. (High memory, switching artifacts)
- **Interpolation**: Parallel computation for multiple states. (High computational load)

**Obs-TasNet Goal**: End-to-end neural estimation of observation filters ($o$) that adapt to any position and scene without manual interpolation.

## Methodology

### 1. Architecture: Modified Inter-Channel Conv-TasNet

The network maps $N_m$ raw waveform signals and 3D coordinates ($x, y, z$) to $K$ observation filter coefficients.

#### 1.1 Learnable Encoding (Encoder)
- **Input**: Signal blocks of size $W=512$
- **Mechanism**: Learnable 1D convolution mappings rather than fixed STFT
- **Joint Embedding**: The virtual microphone coordinates are concatenated with the latent signal features

#### 1.2 Temporal Bottleneck (Key Contribution)
The authors introduced an additional bottleneck layer between the encoder and the TCN.
- **Impact**: Reduces parameters by 40% and GMACs (complexity) by 4x
- **Benefit**: Achieves lower NMSE than the baseline by focusing on the most relevant feature dependencies

#### 1.3 Temporal Convolutional Network (TCN)
- Consists of $S$ stacks of $D$ dilated depthwise separable convolution blocks
- Captures long-range temporal dependencies without the latency of RNNs or block STFT

#### 1.4 Output Transform
- Pointwise convolution and a linear layer map the TCN features back to the required $K$ (e.g., 257 taps) filter coefficients

### 2. Operational Strategy: Asynchronous Estimation

Obs-TasNet operates **asynchronously**:
1. **Slow Loop (Neural)**: Infers every 512ms. Updates the observation filter coefficients $\hat{o}$ based on environmental shifts
2. **Fast Loop (Audio DSP)**: Performs the real-time FxLMS control at the sampling rate (e.g., 16 kHz) using the latest $\hat{o}$

This offloads heavy AI computation to a co-processor (NPU) while maintaining the low-latency guarantees required for ANC stability.

### 3. Remote Microphone Technique (RMT) Background

The RMT estimates the error signal at a virtual microphone using signals from nearby remote microphones:

```
ê[n] = ŷ_e[n] + d̂_e[n]
     = ĝ_e^T u[n] + Σ_r ô_r^T d̂_m,r[n]
```

where:
- $u[n]$ = control signal vector
- $d̂_m,r[n]$ = estimated primary disturbance at remote microphone $r$
- $ô_r$ = observation filter for remote microphone $r$

To ensure causality, the delayed RMT estimates $ê[n-Δ]$ instead of $ê[n]$, shifting substantial parts of the observation filter into a causal range.

## Key Experimental Results

### Ablation Study

| Model | Params | Complexity | NMSE (Static) | NMSE (Moving) |
|-------|--------|------------|---------------|---------------|
| Baseline IC Conv-TasNet | 2.3 M | 4.1 GMACs | -14.8 dB | -14.6 dB |
| **Obs-TasNet (w/ Bottleneck)** | **1.39 M** | **1.03 GMACs** | **-15.32 dB** | **-15.0 dB** |

### ANC Performance
- In simulation, the Obs-TasNet-based RMT system achieved superior noise reduction across a wider frequency range compared to standard multi-point ANC
- Effectively tracks head movements without audible artifacts or re-training

## Critical Review and Insights

- **Practicality**: The asynchronous model is perfect for modern **Mobile SoCs** with integrated NPUs
- **Efficiency**: The temporal bottleneck is a significant architectural improvement for low-power hearables
- **Open Science**: A PyTorch implementation is provided by the authors

## Related Concepts

- [[../concepts/virtual-sensing|Virtual Sensing]]
- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]

## Related Synthesis

- [[../synthesis/virtual-sensing-evolution|Evolution of Virtual Sensing in ANC]]
- [[../synthesis/ai-driven-anc|AI-Driven ANC]]

## Related Entities

- [[../entities/felix-holzmueller|Felix Holzmüller]]
- [[../entities/alois-sontacchi|Alois Sontacchi]]
