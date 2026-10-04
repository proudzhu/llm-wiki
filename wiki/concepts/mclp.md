---
type: concept
created: 2026-04-22
updated: 2026-10-04
sources:
  - wiki/sources/dietzen-2020-isclp-kalman.md
  - raw/papers/nakatani-2022-switching-iva/full-text.md
tags:
  - signal-processing
  - multichannel
  - prediction
---

# MCLP (Multi-Channel Linear Prediction)

**Multi-Channel Linear Prediction (MCLP)** is a technique used in speech processing for blind dereverberation and noise reduction.

## Core Mechanism
MCLP models the late reverberation as a linear combination of previous multi-channel observations. By subtracting this prediction from the current observation, the direct path and early reflections (the desired speech) can be recovered.

## Switching MCLP Filters

In switching convolutional beamforming ([[concepts/switching-civa|swCIVA]]), a bank of $I$ time-invariant MCLP filters $\mathbf{G}_f^{(i)}$ replaces the single filter, with a switch selecting one dereverberated output $\mathbf{z}_{t,f}^{(i)}$ per time-frequency point. Because the noise influence on the past observed signal (and hence the optimal prediction) is highly time-varying, different filters can specialize in different frame clusters, each with reduced model mismatch ([[sources/nakatani-2022-switching-iva|Nakatani et al. 2022]]).

## Related Concepts
- [[concepts/kalman-filter|Kalman Filter]] (often used to track MCLP coefficients)
- [[concepts/beamforming|Beamforming]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/weighted-prediction-error|Weighted Prediction Error (WPE)]]
- [[concepts/switching-civa|Switching CIVA (swCIVA)]]

## Related Sources
- [[sources/dietzen-2020-isclp-kalman|Dietzen 2020: ISCLP Kalman Filter]]
- [[sources/nakatani-2022-switching-iva|Nakatani et al. 2022: Switching IVA and Its Extension to Blind and Spatially Guided Convolutional Beamforming]]
