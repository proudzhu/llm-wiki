---
type: source
created: 2026-04-18
updated: 2026-04-28
sources:
  - raw/papers/toyooka-2026-hybrid-anc-virtual-sensing/full-text.txt
  - https://ssrn.com/abstract=5271898
  - zotero://select/items/0_AMKNDVMJ
tags:
  - active-noise-control
  - hybrid-anc
  - remote-microphone
  - virtual-sensing
  - dual-compensation-filter
  - signal-decomposition
aliases:
  - 'Toyooka 2026: Hybrid ANC with Dual Compensation Paper Reading Note'
---

# Toyooka 2026: Hybrid Active Noise Control System for Remote Microphone Based Virtual Sensing with Two Compensation Filters

**Authors**: Shota Toyooka, Yoshinobu Kajikawa
**Institution**: Kansai University, Japan
**Published**: Applied Acoustics (Preprint), 2026
**DOI**: [10.1051/aacus/2026027](https://ssrn.com/abstract=5271898)
**📎 Zotero**: [zotero://select/items/0_AMKNDVMJ](zotero://select/items/0_AMKNDVMJ)

## Summary

This paper proposes an advanced **Hybrid Active Noise Control (ANC)** system designed for **[[concepts/virtual-sensing|virtual sensing]]** using the remote microphone technique. The core innovation is the use of **two compensation filters** per noise source to improve the accuracy of the estimated error signal at the target (virtual) location.

## Problem Formulation

### The Multi-Source Bottleneck in Virtual Sensing

[[concepts/virtual-sensing|Virtual Sensing]] (RMVS) using the **Remote Microphone Technique (RMT)** typically relies on a fixed compensation filter ($C(z)$) derived from the transfer functions between the physical error microphone and the virtual target point.

In environments with **multiple independent noise sources**, a single fixed compensation filter fails because:
1. The error microphone captures a **mixed signal** from all sources
2. Each noise source has a **different primary path ratio** (Physical path / Virtual path)
3. Applying a single filter to a composite signal leads to large estimation errors at the virtual location

## Methodology

### 1. Dual Compensation and Signal Decomposition

The core innovation is the **signal decomposition** layer added to a [[concepts/hybrid-anc|Hybrid ANC]] structure.

#### 1.1 The Decomposition Filter $H(z)$

An additional adaptive filter $H(z)$ is introduced to separate the contributions of individual noise sources at the error microphone.
- $H(z)$ is updated based on the correlation with the reference signal $R(z)$
- It converges to $H(z) = P_{mx}(z) / R(z)$, where $P_{mx}$ is the primary path from source 1 to the error mic

#### 1.2 Dual Compensation Filters

The system maintains a set of compensation filters $\{C_{mx}(z), C_{mv}(z), \dots\}$ for each noise source.
- **Compensation Filter 1 ($C_{mx}$)**: Optimizes the estimation for Source 1
- **Compensation Filter 2 ($C_{mv}$)**: Optimizes the estimation for Source 2

#### 1.3 Signal Flow

1. **Separate**: The error mic signal $d_m(n)$ is decomposed into $d_{mx}(n)$ (Source 1 component) and $d_{mv}(n)$ (residual, representing Source 2)
2. **Compensate**: Each component is filtered by its respective $C(z)$
3. **Synthesize**: The estimated virtual error signal $e_v(n)$ is the sum of these compensated components
4. **Control**: The synthesized $e_v(n)$ drives both the Feedforward (FF) and Feedback (FB) controllers

### 2. Tuning Stages

The system requires a two-stage offline tuning process:
- **Stage 1**: Only Noise Source 1 is active. Estimate $C_{mx}(z) = P_{vx}(z) / P_{mx}(z)$
- **Stage 2**: Only Noise Source 2 is active. Estimate $C_{mv}(z) = P_{vv}(z) / P_{mv}(z)$

During the **Control Stage**, the adaptive filter $H(z)$ continuously tracks the decomposition path online.

### 3. FFANC with RMVS (Background)

In the tuning stage of RMVS, the virtual microphone is placed at the desired position and the transfer function of the ratio of $P_{mx}$ and $P_{vx}$ is estimated:

```
C_{mx}(z) = P_{vx}(z) / P_{mx}(z)
```

The compensation filter is updated using NLMS:

```
c_{mx}(n+1) = c_{mx}(n) + μ·e(n)·d_{mx}(n) / (δ + ||d_{mx}(n)||²)
```

## Performance Evaluation

### Simulation Setup
- **Environment**: Real acoustic impulse responses
- **Baseline**: Conventional Hybrid ANC with a single RMVS compensation filter
- **Noise Type**: Broadband and non-stationary

### Key Results
- **Noise Reduction**: The proposed system achieves **~20 dB better reduction** than conventional RMVS-HANC in multi-source scenarios
- **Spectrum**: Significant attenuation across the low-to-mid frequency range (up to 1 kHz)
- **Stability**: The decomposition filter $H(z)$ shows stable convergence, ensuring the virtual error estimate remains accurate even as noise intensities shift

## Critical Review and Insights

- **Practicality**: This approach is highly relevant for **TWS earbuds** and **Automotive Headrests** where internal (e.g., wind) and external (e.g., engine) noise sources have distinct spatial characteristics
- **Limitation**: The system complexity scales linearly with the number of independent noise sources. It requires a dedicated reference signal for each feedforward source
- **AI Potential**: Future work could replace the adaptive $H(z)$ with a neural observer (like [[holzmueller-2026-obs-tasnet-virtual-sensing|Obs-TasNet]]) to handle non-linearities and moving sources

## Related Concepts

- [[concepts/virtual-sensing|Virtual Sensing]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/hybrid-anc|Hybrid ANC]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]

## Related Synthesis

- [[synthesis/virtual-sensing-evolution|Evolution of Virtual Sensing in ANC]]
- [[synthesis/anc-architecture-evolution|ANC Architecture Evolution]]

## Related Entities

- [[entities/shota-toyooka|Shota Toyooka]]
- [[entities/yoshinobu-kajikawa|Yoshinobu Kajikawa]]
