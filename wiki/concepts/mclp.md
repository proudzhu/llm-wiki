---
type: concept
created: 2026-04-22
updated: 2026-04-22
sources:
  - wiki/sources/dietzen-2020-isclp-kalman.md
tags:
  - signal-processing
  - multichannel
  - prediction
---

# MCLP (Multi-Channel Linear Prediction)

**Multi-Channel Linear Prediction (MCLP)** is a technique used in speech processing for blind dereverberation and noise reduction.

## Core Mechanism
MCLP models the late reverberation as a linear combination of previous multi-channel observations. By subtracting this prediction from the current observation, the direct path and early reflections (the desired speech) can be recovered.

## Related Concepts
- [[signal-processing|Signal Processing]]
- [[kalman-filter|Kalman Filter]] (often used to track MCLP coefficients)
- [[beamforming|Beamforming]]

## Related Sources
- [[sources/dietzen-2020-isclp-kalman|Dietzen 2020: ISCLP Kalman Filter]]
