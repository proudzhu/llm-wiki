---
type: concept
created: 2026-05-15
updated: 2026-05-15
sources:
  - raw/papers/zhan-2025-deeppem-afc/full-text.txt
tags:
  - hearing-aids
  - feedback-cancellation
  - adaptive-filtering
---

# Hearing Aid Feedback Cancellation

**Hearing aid feedback cancellation** addresses the acoustic feedback problem specific to hearing assistive devices, where the receiver-microphone coupling creates a closed-loop system prone to howling.

## The Problem

In hearing aids:
- Receiver amplifies sound for the hearing-impaired listener
- Some amplified sound radiates back to the microphone (acoustic feedback)
- This recirculation creates howling artifacts
- Limits the **Maximum Stable Gain (MSG)**, making devices inefficient for severe/profound hearing loss

## Key Methods

### 1. Phase Modulation (PM)
Introduces phase changes to break the feedback loop.

### 2. Gain Reduction
Reduces amplification when feedback is detected — simple but degrades audio quality.

### 3. Adaptive Feedback Cancellation (AFC)
Uses an adaptive filter to estimate and subtract the feedback component:
- Theoretically can eliminate feedback completely
- **Challenge**: High correlation between target and feedback signals causes estimation bias

### 4. De-correlation Methods for AFC

| Method | Principle | Limitation |
|--------|-----------|------------|
| **Probe Noise** | Adds known signal for unbiased estimation | Audible, degrades quality |
| **Frequency Shift (FS)** | Shifts frequency to break correlation | Limited for HA scenarios (direct + early reflections dominate) |
| **Prediction Error Method (PEM)** | Whitening pre-filters de-correlate signals | Increased computational complexity |

## Deep Learning Approaches

Recent work integrates deep learning for automatic step-size control:
- **Neural-AFC**: End-to-end neural network for AFC
- **DeepPEM-AFC**: GRU-based step-size prediction combined with PEM de-correlation

## Metrics

- **NESD** (Normalized Euclidean System Distance): Filter estimation accuracy
- **ASG** (Added Stable Gain): Additional gain before instability
- **Tracking Time**: Time to re-converge after path change
- **WB-PESQ, eSTOI, SI-SDR**: Speech quality metrics

## Related Concepts

- [[concepts/acoustic-feedback|Acoustic Feedback]]
- [[concepts/adaptive-feedback-control|Adaptive Feedback Control]]
- [[concepts/prediction-error-method|Prediction Error Method]]
- [[concepts/frequency-shift-feedback-cancellation|Frequency Shift Feedback Cancellation]]
- [[concepts/maximum-stable-gain|Maximum Stable Gain]]

## Related Sources

- [[sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]] — Deep learning-based PEM-AFC
- Waterschoot & Moonen 2011: Fifty years of acoustic feedback control
- Spriet et al. 2008: Feedback control in hearing aids
