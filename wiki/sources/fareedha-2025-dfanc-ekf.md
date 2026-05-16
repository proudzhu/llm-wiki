---
type: source
created: 2026-04-22
updated: 2026-04-22
sources:
  - zotero://select/items/0_M77TYZR5
tags:
  - active-noise-control
  - extended-kalman-filter
  - convolutional-neural-networks
  - dynamic-fixed-filter
---

# Fareedha et al. (2025): DFANC-EKF - Next-Generation ANC

> **Paper**: [Next-Generation ANC: Integrating Dynamic Fixed-Filter Strategies With Extended Kalman Filtering for Enhanced Noise Suppression](https://doi.org/10.1109/ICASSP49660.2025.10888794) ([M77TYZR5](zotero://select/items/0_M77TYZR5))

## Overview
This paper introduces the **Dynamic Fixed-filter Active Noise Control with Extended Kalman Filter (DFANC-EKF)**, which addresses the limitations of static hybrid filters in rapidly changing noise environments.

## Key Innovations
1.  **EKF-CNN Integration**: Combines an Extended Kalman Filter (EKF) for parameter adaptation with a 2D Convolutional Neural Network (CNN) for advanced feature extraction from the noise spectrum.
2.  **Advanced Feature Extraction**: The 2D-CNN allows the system to better capture and recognize intricate noise patterns (e.g., Doppler-shifted sirens) compared to standard spectral heuristics.
3.  **Enhanced Adaptability**: Overcomes the tracking lag of SFANC-FxNLMS and the complexity limits of GFANC-Kalman by using the EKF to linearize and track non-linear control dynamics.

## Performance
- Validated using real-world dynamic noise data.
- Demonstrates superior noise reduction and convergence speed in non-stationary scenarios where traditional hybrid filters underperform.
- Achieved **22% faster convergence** during fast-moving noise tests (as cited in [Jiang 2025](jiang-2025-ai-driven-avnc-review.md)).

## Related Concepts
- [[wiki/concepts/active-noise-control|Active Noise Control]]
- [[wiki/concepts/kalman-filter|Kalman Filter]]
- [[wiki/concepts/neural-networks|Neural Networks]]
- [[wiki/concepts/robust-adaptive-filtering|Robust Adaptive Filtering]]

## Related Synthesis

## Related Entities

- [[entities/fareedha|Fareedha]]
- [[entities/asutosh-kar|Asutosh Kar]]
- [[entities/mads-graesboell-christensen|Mads Græsbøll Christensen]]

## Later Work

- [[sources/fareedha-2026-joint-deep-spe-anc|Fareedha 2026: Joint Deep SPE and Adaptive Control for ANC]] — Extended to end-to-end joint SPE + control with DeepSPE + ANC-Net
