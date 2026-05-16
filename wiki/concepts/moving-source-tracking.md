---
type: concept
created: 2026-04-30
updated: 2026-04-30
sources:
  - raw/papers/wang-2026-predictive-dsfanc-crnn/full-text.md
tags:
  - signal-processing
  - array-processing
  - sound-source-localization
  - active-noise-control
---

# Moving Source Tracking

**Moving Source Tracking** is the problem of continuously estimating the time-varying position or Direction-of-Arrival (DoA) of a sound source as it moves through space. In ANC, this is critical for maintaining effective noise cancellation when the noise source is non-stationary.

## Overview

Traditional ANC systems assume a stationary noise source. In practice, sources such as vehicles, drones, and vacuum cleaners move, causing the acoustic paths to change over time. This creates two challenges:

1. **Path variation**: The primary and secondary paths change as the source moves
2. **Tracking delay**: Estimation and adaptation algorithms lag behind the actual source position

## Motion Models

Common motion patterns for moving sources:

| Mode | Description | Parameters |
|------|-------------|------------|
| **Static** | Constant DoA | Fixed angle |
| **Constant-rate** | Uniform angular velocity | Angular velocity (°/s) |
| **Time-varying-rate** | Non-uniform motion | Periodic modulation with amplitude, phase, cycle count |

## Approaches for ANC with Moving Sources

### Adaptive ANC (FxLMS)
Updates control filter coefficients online to track changing conditions. Suffers from slow convergence and divergence risk.

### Directional SFANC (D-SFANC)
Selects pre-trained filters based on current DoA. Has a one-frame lag — the filter corresponds to the previous frame's DoA, not the current one.

### Predictive Directional SFANC (PD-SFANC)
Wang et al. (2026) use a CRNN to predict the next-frame DoA from multi-frame temporal context, enabling proactive filter selection. The CRNN captures the hidden temporal dynamics of source trajectory evolution.

### Dynamic Factor Graph SFANC (DFG-SFANC)
Su et al. (2025) use a factor graph for filter pre-selection. Requires manual parameter tuning and struggles with rapidly accelerating sources.

## Key Insights from Wang et al. (2026)

- Multi-frame context ($K=4$ frames, 2 s) balances historical context for static sources with rapid detection of directional shifts
- CRNN-based prediction is more robust than traditional signal processing methods for time-varying-rate motion
- Proactive filter selection eliminates the reactive lag that degrades D-SFANC performance
- The Doppler effect can be omitted when source speed ≪ speed of sound

## Related Concepts

- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]] — spatial information for tracking
- [[concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]] — filter selection strategies for moving sources
- [[concepts/active-noise-control|Active Noise Control]] — application domain
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — neural architecture for trajectory prediction

## Related Sources

- [[sources/wang-2026-predictive-dsfanc-crnn|Wang 2026: Predictive Directional SFANC via CRNN]] — CRNN-based predictive tracking for ANC
