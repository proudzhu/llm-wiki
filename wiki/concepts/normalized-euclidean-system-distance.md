---
type: concept
created: 2026-06-10
updated: 2026-06-10
sources:
  - raw/papers/lydaki-2026-deep-feedback-cancellation-hearing-aids/full-text.md
  - raw/papers/zhan-2025-deeppem-afc/full-text.txt
tags:
  - metrics
  - system-identification
  - adaptive-filtering
  - hearing-aids
---

# Normalized Euclidean System Distance

**Normalized Euclidean System Distance (NESD)** is a metric for evaluating the accuracy of feedback-path filter estimates in [[concepts/hearing-aid-feedback-cancellation|hearing aid feedback cancellation]]. It measures the normalized squared Euclidean distance between the true and estimated feedback-path impulse responses.

## Definition

```
NESD(n) = ||f(n) - f̂(n)||² / ||f(n)||²
```

where f(n) is the true feedback-path IR and f̂(n) is the estimated IR at time frame n. Lower values indicate better estimation accuracy.

## As a Loss Function

NESD is used as a training loss for deep learning-based feedback cancellation methods:

- **[[concepts/deep-feedback-cancellation|DFC]]**: NESD loss with temporal smoothing (average pooling N=50, exponential smoothing α=0.5) to resolve the convergence/steady-state trade-off
- **DeepPEM-AFC**: NESD loss for training the GRU-based step-size predictor

## Temporal Smoothing

When used as a loss, temporal smoothing via average pooling is critical:

```
L_NESD = (1/N) · Σ_{i=0}^{N-1} NESD(n-i)
```

Without smoothing: the model achieves lower steady-state NESD but much slower convergence after path changes. With smoothing (N=50): the model learns to produce temporally consistent estimates, enabling both fast convergence and low steady-state error.

## Related Concepts

- [[concepts/deep-feedback-cancellation|Deep Feedback Cancellation]]
- [[concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]]
- [[concepts/adaptive-feedback-control|Adaptive Feedback Control]]

## Related Sources

- [[sources/lydaki-2026-deep-feedback-cancellation-hearing-aids|Lydaki 2026: Deep Feedback Cancellation]] — NESD as loss and evaluation metric
- [[sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]] — NESD for step-size prediction training
