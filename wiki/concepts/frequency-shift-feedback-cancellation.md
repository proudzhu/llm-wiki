---
type: concept
created: 2026-05-15
updated: 2026-05-15
sources:
  - raw/papers/vanwaterschoot-2011-fifty-years-afc/full-text.md
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

## Two Roles: PFC and AFC Decorrelator

Van Waterschoot & Moonen (2011) show that FS plays two distinct roles in acoustic feedback control:

- **As a phase-modulating feedback control (PFC) method** — FS in the forward path smooths the loop gain so that the MSG is determined by the *average* rather than the *peak* magnitude response. Schroeder's optimal shift is ~5 Hz (half the ~10 Hz average spacing of room-response magnitude peaks), yielding up to 14 dB MSG increase theoretically but only ≤6 dB subjectively (to avoid audible beating). The PFC-FS variant is one of the three PFC realizations in the survey's comparative evaluation. See [[concepts/phase-modulating-feedback-control|Phase-Modulating Feedback Control (PFC)]].
- **As an AFC decorrelator** — FS in the forward path reduces the closed-loop identification bias of [[concepts/adaptive-feedback-cancellation|AFC]]. The AFC-FS variant uses $f_m = 5$ Hz. FS decorrelation is acceptable for speech but perceptually inadequate for audio. See [[concepts/decorrelation-for-afc|Decorrelation for AFC]].

The hearing-aid application below primarily uses FS in the second role.

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
- [[concepts/phase-modulating-feedback-control|Phase-Modulating Feedback Control (PFC)]] — FS as a PFC variant (loop-gain smoothing)
- [[concepts/adaptive-feedback-cancellation|Adaptive Feedback Cancellation (AFC)]] — FS as an AFC decorrelator (AFC-FS)
- [[concepts/decorrelation-for-afc|Decorrelation for AFC]] — FS as in-loop decorrelation

## Related Sources

- [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] — formalizes FS as both a PFC variant (Schroeder's optimal 5 Hz shift, ≤6 dB subjective MSG increase) and an AFC decorrelator (AFC-FS)
- [[sources/lydaki-2026-deep-feedback-cancellation-hearing-aids|Lydaki 2026: Deep Feedback Cancellation]] — DFC outperforms FD-AFC-FS without frequency shifting artifacts
- [[sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]] — FS+DeepPEM-AFC achieves optimal performance
- Schroeder 1964: Improvement of acoustic-feedback stability by frequency shifting
- Zheng et al. 2016: Analysis of additional stable gain by frequency shifting
