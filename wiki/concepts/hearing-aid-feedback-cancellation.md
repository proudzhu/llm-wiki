---
type: concept
created: 2026-05-15
updated: 2026-08-20
sources:
  - raw/papers/zhan-2025-deeppem-afc/full-text.txt
  - raw/papers/lydaki-2026-deep-feedback-cancellation-hearing-aids/full-text.md
  - raw/papers/schepker-2016-sdp-minmax-acoustic-feedback/full-text.md
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

### AFC-Based Methods
Recent work integrates deep learning for automatic step-size control or direct IR estimation:
- **Neural-AFC**: End-to-end neural network for AFC
- **DeepPEM-AFC**: GRU-based step-size prediction combined with PEM de-correlation
- **[[concepts/deep-feedback-cancellation|DFC]]**: Compact DNN (856K params) that directly estimates the feedback-path IR, outperforming both adaptive filtering and signal-prediction approaches with 30x faster convergence after path changes

### Direct Feedback Suppression (DeepMFC)
[[concepts/deep-marginal-feedback-cancellation|Deep Marginal Feedback Cancellation (DeepMFC)]] treats feedback cancellation as interference suppression rather than path estimation:
- **DeepMFC** (Zheng et al. 2022): Complex spectrum mapping to estimate feedback-free speech directly; trained open-loop, applied closed-loop
- **L3C-DeepMFC** (Hao et al. 2025): Low-latency (4 ms) low-complexity (0.31M params) variant with full- and sub-band recurrent modeling and closed-loop fine tuning
- Maintains stability at high gains where AFC methods struggle
- Can be integrated with AFC for further improvement

## Metrics

- **NESD** (Normalized Euclidean System Distance): Filter estimation accuracy
- **ASG** (Added Stable Gain): Additional gain before instability
- **Tracking Time**: Time to re-converge after path change
- **WB-PESQ, eSTOI, SI-SDR**: Speech quality metrics

## Common Part Decomposition

A parameter-reduction approach specific to multi-microphone or multi-condition hearing aids is [[concepts/common-part-decomposition|common part decomposition]], which separates each feedback path into a time-invariant common part (shared transducer/ear characteristics, modeled as a pole-zero filter) and a time-varying variable part (modeled as an all-zero filter). Only the variable part is adapted online, reducing convergence time. Schepker & Doclo (2016) proposed a [[concepts/min-max-common-part-estimation|min-max SDP optimization]] that directly maximizes the [[concepts/maximum-stable-gain|MSG]] rather than minimizing misalignment, yielding 2–5 dB MSG improvement and faster [[concepts/prediction-error-method|PEM]]-AFC convergence. The approach is robust to unseen feedback path conditions (telephone, repositioning).

## Related Concepts

- [[concepts/acoustic-feedback|Acoustic Feedback]]
- [[concepts/adaptive-feedback-control|Adaptive Feedback Control]]
- [[concepts/prediction-error-method|Prediction Error Method]]
- [[concepts/frequency-shift-feedback-cancellation|Frequency Shift Feedback Cancellation]]
- [[concepts/maximum-stable-gain|Maximum Stable Gain]]
- [[concepts/deep-marginal-feedback-cancellation|Deep Marginal Feedback Cancellation]]
- [[concepts/closed-loop-fine-tuning|Closed-Loop Fine Tuning]]

## Related Sources

- [[sources/lydaki-2026-deep-feedback-cancellation-hearing-aids|Lydaki 2026: Deep Feedback Cancellation]] — DFC with direct IR estimation
- [[sources/hao-2025-l3c-deepmfc|Hao et al. 2025: L3C-DeepMFC]] — Low-latency low-complexity deep marginal feedback cancellation
- [[sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]] — Deep learning-based PEM-AFC
- [[sources/schepker-2016-sdp-minmax-acoustic-feedback|Schepker & Doclo 2016]] — common part decomposition with min-max SDP optimization for MSG maximization and faster AFC convergence
- Waterschoot & Moonen 2011: Fifty years of acoustic feedback control
- Spriet et al. 2008: Feedback control in hearing aids
