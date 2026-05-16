---
type: concept
created: 2026-04-17
updated: 2026-05-06
sources:
  - raw/papers/fareedha-2026-joint-deep-spe-anc/full-text.txt
  - raw/papers/akhtar-2006-vss-lms-online-spm/full-text.txt
  - raw/papers/holzmuller-2026-dtw-secondary-path-anc/full-text.md
tags:
- active-noise-control
- signal-processing
- system-identification
---

# Secondary Path Modeling

**Secondary Path Modeling** is the process of identifying the transfer function of the **secondary path** $S(z)$ in an [[active-noise-control|Active Noise Control]] system.

## Overview

The secondary path includes all components between the digital control signal and the residual error measurement:
- Digital-to-Analog Converter (DAC)
- Reconstruction filter
- Power amplifier
- Secondary source (loudspeaker)
- Acoustic path from loudspeaker to error microphone
- Error microphone
- Preamplifier
- Anti-aliasing filter
- Analog-to-Digital Converter (ADC)

Accurate knowledge of $S(z)$ is essential for the stability and convergence of adaptive algorithms like the [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]].

## Modeling Approaches

### 1. [[offline-secondary-path-modeling|Offline Secondary-Path Modeling]]
Conducted before the ANC system starts operating. A training signal (typically white noise) is played through the secondary source, and an adaptive filter (e.g., LMS) is used to identify the impulse response.

### 2. [[online-secondary-path-modeling|Online Secondary-Path Modeling]]
Conducted during ANC operation. This is necessary when the secondary path is time-varying (e.g., movement of the user's head in headphones).
- **Additive Noise Method**: Injecting a low-level auxiliary noise signal into the secondary source and using it to identify $S(z)$ simultaneously with noise cancellation. Key methods include:
  - **Eriksson (1989)**: Basic two-filter structure with auxiliary noise injection
  - **Zhang (2001)**: Three-filter cross-updated method, best among classical approaches
  - **Akhtar (2006)**: Two-filter method with [[variable-step-size-lms|VSS LMS]] (inverse step-size strategy) and MFxLMS, achieving −12.35 dB NMSE
- **Overall Modeling**: Identifying $S(z)$ without auxiliary noise by exploiting the relationship between existing signals (more complex, less stable).

### 3. [[deep-secondary-path-estimation|Deep Secondary Path Estimation]]
Uses deep neural networks (Conv1D + BiLSTM + Attention) to predict $S(z)$ from ANC input-output pairs in a single forward pass, replacing iterative adaptation with frame-level inference. Achieves −16.27 dB NMSE, outperforming the best classical method (Akhtar's VSS-LMS) by 3.92 dB (Fareedha et al. 2026).

## Impact of Modeling Errors

The [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] can tolerate a phase error of up to **$\pm 90^\circ$** between the true secondary path and its estimate $\hat{S}(z)$. If the error exceeds this limit, the algorithm will diverge.

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[offline-secondary-path-modeling|Offline Secondary-Path Modeling]]
- [[online-secondary-path-modeling|Online Secondary-Path Modeling]]
- [[system-identification|System Identification]]
- [[deep-secondary-path-estimation|Deep Secondary Path Estimation]]

## Related Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]]
- [[sources/fareedha-2026-joint-deep-spe-anc|Fareedha 2026: Joint Deep SPE and Adaptive Control for ANC]]
- [[sources/akhtar-2006-vss-lms-online-spm|Akhtar 2006: VSS LMS for Online Secondary Path Modeling]]
