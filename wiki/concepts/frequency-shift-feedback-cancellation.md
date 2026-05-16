---
type: concept
created: 2026-05-15
updated: 2026-05-15
sources:
  - raw/papers/zhan-2025-deeppem-afc/full-text.txt
tags:
  - hearing-aids
  - feedback-cancellation
  - frequency-shift
  - de-correlation
---

# Frequency Shift Feedback Cancellation

**Frequency Shift (FS)** is a de-correlation method for acoustic feedback cancellation that introduces a small frequency offset in the signal path to break the correlation between the target and feedback signals.

## Principle

By shifting the frequency of the processed signal by a small amount (typically 5-10 Hz), the feedback path estimation becomes unbiased because the feedback signal no longer aligns spectrally with the original target signal.

## Application in Hearing Aids

FS is placed in the feed-forward path of the hearing aid system:
- Typical shift: 10 Hz
- Effective for breaking feedback correlation
- **Limitation**: Performance is limited in HA scenarios where direct and early reflections dominate the acoustic feedback path

## Combination with Other Methods

FS can be combined with other AFC methods for improved performance:
- **FS+NLMS**: Frequency shift with normalized LMS
- **FS+KF**: Frequency shift with Kalman filter
- **FS+DeepPEM-AFC**: Frequency shift combined with deep learning-based PEM-AFC, achieving optimal performance across all speech quality metrics

## Comparison with PEM

| Aspect | Frequency Shift | PEM |
|--------|----------------|-----|
| Mechanism | Frequency offset | Whitening pre-filters |
| Effectiveness in HA | Limited (direct/early reflections) | Strong |
| Computational cost | Low | Higher (mitigated by FD implementation) |
| Combined performance | Best when combined with PEM | Best when combined with FS |

## Related Concepts

- [[concepts/acoustic-feedback|Acoustic Feedback]]
- [[concepts/prediction-error-method|Prediction Error Method]]
- [[concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]]
- [[concepts/adaptive-feedback-control|Adaptive Feedback Control]]

## Related Sources

- [[sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]] — FS+DeepPEM-AFC achieves optimal performance
- Schroeder 1964: Improvement of acoustic-feedback stability by frequency shifting
- Zheng et al. 2016: Analysis of additional stable gain by frequency shifting
