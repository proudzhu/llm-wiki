---
type: concept
created: 2026-04-11
updated: 2026-09-12
sources:
  - raw/papers/zhang-2026-feedback-path-mitigation-mcanc/full-text.md
  - raw/papers/holzmuller-2026-dtw-secondary-path-anc/full-text.md
tags:
- active-noise-control
- secondary-path
- system-identification
- acoustic-feedback
---

# Offline Secondary-Path Modeling

**Offline secondary-path modeling** identifies the secondary path $S(z)$ during a **training phase before ANC operation begins**. This contrasts with [[online-secondary-path-modeling|Online Secondary-Path Modeling]], which identifies $S(z)$ while the system is actively canceling noise.

## Method

The standard approach (Kuo 1999, Section VI):

1. **Inject white noise** $v(n)$ through the secondary path (loudspeaker)
2. **Record the error sensor** output $d(n) = S(z) * v(n)$
3. **Identify $\hat{S}(z)$** using the LMS algorithm:

$$\hat{s}(n+1) = \hat{s}(n) + \rho \cdot e_s(n) \cdot v(n)$$

where $e_s(n) = d(n) - \hat{s}(n) * v(n)$ is the modeling error.

## Advantages

- **No bias**: The injected noise is uncorrelated with primary noise, so convergence is unbiased
- **Fast convergence**: All processing power goes to identification — no interference from ANC operation
- **Simple implementation**: Standard LMS with white noise input converges quickly

## Disadvantages

- **Requires downtime**: System must be taken offline for training
- **Cannot track changes**: If $S(z)$ drifts (temperature, headphone fit, ear canal changes), the model becomes stale
- **Inconvenient for users**: Training noise is audible

## Accuracy Requirements

The [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] tolerates moderate modeling errors:
- Under slow adaptation, FXLMS can tolerate **~90° phase error** between $S(z)$ and $\hat{S}(z)$
- Within 40° phase error, convergence speed is nearly unaffected

## When to Use

| Scenario | Offline | Online |
|----------|---------|--------|
| Fixed, known hardware | ✅ | — |
| Lab / controlled environment | ✅ | — |
| Headphones (fit varies per user) | — | ✅ |
| Ear canal changes during use | — | ✅ |
| Long secondary paths (many coefficients) | — | ✅ (if adaptive) |

## Persistent Primary Noise: Why "Offline" Is Not Enough

"Offline" only guarantees an unbiased estimate when the excitation used for identification is uncorrelated with the interfering signal. In the classical secondary-path training phase the injected probe dominates the error sensor, so the recipe above holds. The **feedback-path** case is harder: measuring $F(z)$ requires probing the secondary loudspeaker, and the reference microphones simultaneously pick up **persistent primary noise** that cannot be silenced in a realistic deployment — a bias this page's noise-free recipe simply does not address. The naive fix (estimating the path from total-field statistics) fails badly rather than gracefully: in a multichannel ANC array, a mapping estimated from un-subtracted total-field covariances collapsed noise reduction to ≈ −2 dB, because the persistent primary field dominates the pseudo-inverse ([[sources/zhang-2026-feedback-path-mitigation-mcanc|Zhang et al. 2026]]).

Two families of remedies exist:

- **Adaptive online modeling** — [[concepts/online-feedback-path-modeling|OFBPM]], which tracks the path during operation using scheduled auxiliary noise.
- **Statistics-domain isolation** — [[concepts/covariance-subtraction|covariance subtraction]], which measures primary-only and total-field covariances in two stages and differences them, so the primary contribution cancels and identification proceeds *without* a noise-free window.

The distinction is worth keeping sharp: the first relaxes **when** identification happens, the second relaxes **the quiet precondition** while keeping identification essentially one-shot.

## Related

- [[online-secondary-path-modeling|Online Secondary-Path Modeling]] — Identifying $S(z)$ during active ANC operation
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — Requires $\hat{S}(z)$ for reference signal filtering
- [[multi-channel-anc|Multi-Channel ANC]] — Offline modeling is impractical when $O(M \times N)$ paths must be identified
- [[active-noise-control|Active Noise Control]] — Core system architecture

## Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section VI: Online Secondary-Path Modeling (describes offline as baseline)
- [[sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]] — Uses offline secondary path modeling

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[online-secondary-path-modeling|Online Secondary-Path Modeling]]
- [[system-identification|System Identification]]
- [[multi-channel-anc|Multi-Channel ANC]]
- [[concepts/covariance-subtraction|Covariance Subtraction]] — two-stage estimator that removes the persistent-noise bias without an ANC-idle window
- [[concepts/online-feedback-path-modeling|Online Feedback-Path Modeling]] — the adaptive alternative for the feedback-path case

## Related Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]]
- [[sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]]
- [[sources/zhang-2026-feedback-path-mitigation-mcanc|Zhang, Abhayapala, Samarasinghe & Bastine 2026: Acoustic Feedback Path Mitigation for Multichannel ANC]] — offline identification of a feedback-group-to-reference-group mapping under persistent primary noise, via covariance subtraction
- [[sources/holzmuller-2026-dtw-secondary-path-anc|Holzmüller & Sontacchi 2026: DTW for Secondary Path Interpolation in ANC]]

