---
type: concept
created: 2026-05-15
updated: 2026-09-13
sources:
  - raw/papers/vanwaterschoot-2011-fifty-years-afc/full-text.md
  - raw/papers/zhan-2025-deeppem-afc/full-text.txt
  - raw/papers/schepker-2016-sdp-minmax-acoustic-feedback/full-text.md
  - raw/papers/zhan-2026-joint-afc-rfs/full-text.md
tags:
  - adaptive-filtering
  - system-identification
  - hearing-aids
  - de-correlation
---

# Prediction Error Method

The **Prediction Error Method (PEM)** is a de-correlation technique used in adaptive feedback cancellation (AFC) for hearing aids. It addresses the fundamental bias problem caused by high correlation between the target speech signal and the acoustic feedback signal.

## Core Idea

In closed-loop hearing aid systems, the adaptive filter estimating the feedback path receives a highly correlated input (speech + feedback), causing biased estimates. PEM introduces **whitening pre-filter operators** to de-correlate the signals before adaptive filtering.

## Mathematical Formulation

Given receiver signal u(n) and source signal s(n), the acoustic feedback path transfer function:

```
F(q,n) = f₀(n) + f₁(n)q⁻¹ + ... + f_{Lf-1}(n)q^{-(Lf-1)}
```

PEM applies whitening filters A(q) to both the receiver and microphone signals:

```
u_a(n) = A(q) · u(n)
y_a(n) = A(q) · y(n)
```

The prediction error is then:

```
e_a(n) = y_a(n) - F̂^T(n) · u_a(n)
```

where F̂(n) is the estimated feedback path filter.

## Frequency-Domain Implementation

Time-domain PEM filtering increases computational complexity. The frequency-domain implementation (PEMAF) uses FFT-based processing:

```
U_a(l) = FFT{Q · u_a(n)}
Y_a(l) = FFT{Q · y_a(n)}
E_a(l) = FFT{Q · e_a(n)}
```

where Q is the overlap-save matrix. This reduces complexity significantly, making it suitable for low-power hearing aid devices.

## Advantages

- Solves the high-correlation bias problem inherent in closed-loop AFC
- More effective than frequency shifting for hearing aid scenarios where direct and early reflections dominate the feedback path
- Can be combined with deep learning for step-size control

## Limitations

- Increased computational complexity in time-domain (mitigated by FD implementation)
- Requires careful design of whitening pre-filters
- Performance depends on accurate speech model for pre-whitening

## Integration with Common Part Decomposition

PEM-based AFC can be combined with [[concepts/common-part-decomposition|common part decomposition]] to reduce the number of adaptive parameters. Schepker & Doclo (2016) used PEM-AFC with a pre-estimated common part (pole-zero filter) and a shorter adaptive variable part (24 taps instead of 36), demonstrating increased initial convergence speed and faster reconvergence after feedback path changes, while maintaining similar steady-state performance. The common part was estimated offline using [[concepts/min-max-common-part-estimation|min-max SDP optimization]] from measured free-field impulse responses.

## PEM-AFC as a Stage in Joint Frameworks

[[concepts/jointdfc|JointDFC]] (Zhan et al. 2026) reuses the deep PEM-AFC ([[sources/zhan-2025-deeppem-afc|DeepPEM-AFC]]) as its first stage (LFCNet): PEM whitening plus GRU-predicted per-T-F-bin step sizes cancel the linear feedback, after which a neural suppression network (RFSNet) removes the residual feedback and noise. The PEM stage preserves the target signal while removing most feedback, letting the second stage specialize in residual components — and its steady-state accuracy and fast convergence are why it was chosen over direct suppression as the cancellation engine.

## Related Concepts

- [[concepts/acoustic-feedback|Acoustic Feedback]]
- [[concepts/adaptive-feedback-control|Adaptive Feedback Control]]
- [[concepts/adaptive-feedback-cancellation|Adaptive Feedback Cancellation (AFC)]] — PEM-AFROW realizes the AFC-PF variant (decorrelating prefilters in the adaptive filtering circuit)
- [[concepts/decorrelation-for-afc|Decorrelation for AFC]] — PEM-AFROW is the in-circuit decorrelation approach identified as superior by the 2011 survey
- [[concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]]
- [[concepts/frequency-shift-feedback-cancellation|Frequency Shift Feedback Cancellation]]
- [[concepts/variable-step-size-lms|Variable Step-Size LMS]]

## Related Sources

- [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] — formalizes PEM-AFROW as the decorrelating-prefilter realization (AFC-PF) for both speech (Rombouts et al.) and audio (van Waterschoot & Moonen) applications; identifies it as the practical state-of-the-art AFC variant
- [[sources/lydaki-2026-deep-feedback-cancellation-hearing-aids|Lydaki 2026: Deep Feedback Cancellation]] — DFC as alternative to PEM-based approaches
- [[sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]] — Deep learning-based PEM-AFC with GRU step-size prediction
- [[sources/schepker-2016-sdp-minmax-acoustic-feedback|Schepker & Doclo 2016]] — PEM-AFC integrated with common part decomposition, showing faster convergence with fewer adaptive parameters
- [[sources/zhan-2026-joint-afc-rfs|Zhan, Moore, Li & Zheng 2026: JointDFC]] — deep PEM-AFC (DeepPEM-AFC) as the first stage of a joint cancellation + suppression framework
- Spriet et al. 2005: Adaptive feedback cancellation in hearing aids with linear prediction of the desired signal
