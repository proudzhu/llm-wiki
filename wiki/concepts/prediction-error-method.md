---
type: concept
created: 2026-05-15
updated: 2026-05-15
sources:
  - raw/papers/zhan-2025-deeppem-afc/full-text.txt
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

## Related Concepts

- [[../concepts/acoustic-feedback|Acoustic Feedback]]
- [[../concepts/adaptive-feedback-control|Adaptive Feedback Control]]
- [[../concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]]
- [[../concepts/frequency-shift-feedback-cancellation|Frequency Shift Feedback Cancellation]]
- [[../concepts/variable-step-size-lms|Variable Step-Size LMS]]

## Related Sources

- [[../sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]] — Deep learning-based PEM-AFC with GRU step-size prediction
- Spriet et al. 2005: Adaptive feedback cancellation in hearing aids with linear prediction of the desired signal
