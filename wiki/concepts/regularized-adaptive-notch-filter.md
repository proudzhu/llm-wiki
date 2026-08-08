---
type: concept
created: 2026-08-08
updated: 2026-08-08
sources:
  - raw/papers/gil-cacho-2009-regularized-adaptive-notch-filters/full-text.md
tags:
  - acoustic-howling
  - notch-filter
  - adaptive-notch-filter
  - regularization
  - leaky-lms
  - howling-detection
  - signal-processing
---

# Regularized Adaptive Notch Filter (RANF)

The **Regularized Adaptive Notch Filter (RANF)** is an [[concepts/notch-filter-based-howling-suppression|NHS]] method for [[concepts/acoustic-howling-suppression|acoustic howling suppression]] in which a bank of adaptive notch filters (ANFs) is regularized with signed coefficients so that their frequency estimates converge during howling and diverge otherwise, turning coefficient convergence itself into a [[concepts/howling-detection|howling detection]] criterion. It was introduced by Gil-Cacho, van Waterschoot, Moonen & Jensen (EUSIPCO 2009) to give ANF-based NHS a detection capability comparable to frame-based FFT methods while preserving the ANF's low processing delay and low complexity.

## Motivation: The ANF Detection Gap

Classical [[concepts/notch-filter-based-howling-suppression|NHS]] comes in two families:

- **Frame-based (FFT)** methods — two-stage (detect then suppress); accurate frequency estimates and good howling detection from power-spectrum amplitude, but large processing delay and high complexity from long FFT frames.
- **ANF-based** methods — one-stage (simultaneous detect and suppress), sample-based so minimum delay and low complexity, and able to track howling sample-by-sample; but historically *weak howling detection* because no power-spectrum information is available.

RANF closes this gap: it keeps the ANF's sample-based operation but replaces the missing power-spectrum cue with a *convergence cue* derived from regularization.

## Notch Filter and Direct-Form ANF

RANF uses a second-order IIR notch filter with constrained poles and zeros (Nehorai 1985): zeros on the unit circle, poles at radius $0 < r < 1$ on the same radial direction,

$$H(z) = \frac{1 - 2 \cos(\omega_0) z^{-1} + z^{-2}}{1 - 2 r \cos(\omega_0) z^{-1} + r^2 z^{-2}}.$$

A pole radius close to unity gives a very narrow notch (minimal surrounding distortion) but then demands very accurate frequency estimates. For coefficient updating the transfer function is rewritten in terms of a single parameter $a(n) \in (-2, 2)$:

$$H(q) = \frac{1 - a(n) q^{-1} + q^{-2}}{1 - a(n) r q^{-1} + r^2 q^{-2}}, \qquad \omega_0(n) = \arccos(a(n)/2).$$

$a(n)$ is estimated by minimizing the mean square error of the notch-filter output, $\min_{a(n)} E[y(n)^2]$, via a gradient-descent update (Regalia 1995). A gradient-descent (rather than Gauss-Newton) implementation is chosen for minimal complexity — only $n$ parameters are estimated, where $n$ is the number of sinusoids.

## Signed Regularization as a Detection Signal

The proposed method runs **three RANFs in parallel**, each regularized with a different signed term $\lambda_i$:

$$\min_{a_i(n)} E[y_i(n)^2] + \lambda_i a_i(n)^2, \quad i = 1, 2, 3,$$

giving a modified update equivalent to a **Leaky LMS** update:

$$a_i(n+1) = a_i(n) - \mu \left\{ y_i(n) \nabla_{a_i}(n) + \lambda_i a_i(n) \right\}.$$

The regularization term is **negligible when howling is present** (the gradient term $y_i(n)\nabla_{a_i}(n)$ dominates) but **dominates when howling is absent** (the gradient tends to zero), where the update reduces to $a_i(n+1) \approx (1 - \mu \lambda_i) a_i(n)$. The sign of $\lambda_i$ therefore determines the no-howling behaviour:

| $\lambda_i$ | No-howling behaviour | Howling behaviour |
|-------------|----------------------|-------------------|
| $+\lambda$ | coefficient leaked **towards 0** | converges to howling frequency |
| $0$ | neutral | converges to howling frequency |
| $-\lambda$ | coefficient accumulated **towards its bound** | converges to howling frequency |

The three RANFs are set with $\lambda_1 = +\lambda$, $\lambda_2 = 0$, $\lambda_3 = -\lambda$. Consequently the three estimates **converge to a common value during howling** and **diverge away from each other when howling is absent**. This convergence/divergence pattern is the detection signal — it does not rely on power-spectrum information, so a desired tonal source component (which does not drive three independently-regularized estimates to a common frequency the way a loop-sustained howling tone does) is not mistaken for howling.

## Decision Rule and Parameter Choice

The decision block monitors the three coefficient sequences. After buffering $L$ samples (small, for minimum decision delay; e.g. $L = 5$ samples = 0.312 ms at 16 kHz), it computes the mean and variance over the block for each RANF. If the difference between two mean values (in Hz) is below a fixed threshold, howling is declared; the output is taken as the RANF output with the smallest variance (the most reliable estimate). If all pairwise mean differences exceed the threshold, no howling is assumed and the input is passed through directly.

The regularization magnitude $\lambda$ is chosen so that, over a period of $M$ samples, two coefficients diverge by a prescribed frequency threshold $\Delta f$ (Hz). Under the small-angle approximation ($\Delta f \ll f_s$):

$$\lambda = \frac{1}{\mu} \left[ \sqrt[2M]{1 + \left(\frac{2\pi}{f_s} \Delta f\right)^2} - 1 \right].$$

This links the detection threshold directly to a tunable frequency separation, rather than to an ad-hoc regularization magnitude.

## Reported Performance and Limitation

On synthetic speech and music feedback paths (16 kHz, scenarios 'a'/'b' differing in howling frequency range and onset speed), with $\lambda_1 = +0.0001$, $\lambda_2 = 0$, $\lambda_3 = -0.0001$, $\mu = 0.023$, $r = 0.85$, threshold $5$ Hz, $L = 5$:

| Signal | $\mathrm{SD}_{\mathrm{mean}}$ | $\mathrm{SD}_{\max}$ | $\mathrm{Att}_{\max}$ (dB) | $\mathrm{Att}_{\min}$ (dB) |
|--------|------|------|------|------|
| $\mathrm{Speech}_a$ | 1.66 | 14.78 | 5 | 6 |
| $\mathrm{Speech}_b$ | 4.32 | 28.83 | 5 | 40 |
| $\mathrm{Music}_a$ | 1.05 | 13.24 | 3 | 6 |
| $\mathrm{Music}_b$ | 3.61 | 17.83 | 1 | 40 |

Suppression and sound quality are comparable to frame-based methods *for mid-range howling frequencies*. The method **fails for howling near $0$ or $f_s/2$** (below 1.5 kHz in scenario 'b'), because direct-form ANFs are not necessarily stable when the notch frequency approaches its extreme values (Regalia 1995). Lattice ANF implementations would address the stability issue but, as the authors note, their performance is acceptable only for sinusoids immersed in white noise — not for coloured inputs such as speech or music. This is an open limitation of the direct-form RANF variant.

## Position Among Howling-Detection Paradigms

RANF's convergence-based detection is distinct from the other [[concepts/howling-detection|howling detection]] paradigms in the wiki:

- **Spectral-feature HD** (PTPR/PAPR/PHPR/PNPR/IPMP/IMSD; van Waterschoot & Moonen 2010) — frame-based, candidate howling frequencies are peak-picked then discriminated by spectral features.
- **Sparsity-based HD** ([[concepts/ninosp2-transposed|NINOS²-T]]; Mounir et al. 2025) — full-grid transposed spectral sparsity, enables early-howling/ringing detection without candidate preselection.
- **Ballistics-based candidate selection** ([[concepts/ballistics-based-howling-detection|Williams 2014]]) — temporal-persistence asymmetric per-bin filter replaces peak-picking.
- **Closed-loop trial-and-verify** ([[concepts/trial-and-verify-notch-insertion|Williams 2014]]) — a trial notch is inserted and the post-notch response is checked, sidestepping the sustained-tone ambiguity.
- **RANF convergence** (this concept) — three signed-regularization ANFs must agree on a frequency for howling to be declared; no power spectrum or candidate preselection required, but inherits direct-form ANF instability at frequency extremes.

## Related Concepts

- [[concepts/notch-filter-based-howling-suppression|Notch-Filter-Based Howling Suppression (NHS)]] — the solution family RANF belongs to (ANF-based, one-stage variant)
- [[concepts/howling-detection|Howling Detection]] — RANF convergence is a detection paradigm
- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — broader AHS context
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the closed-loop instability RANF suppresses
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — NHS effectively raises the operable gain above the passive MSG

## Related Sources

- [[sources/gil-cacho-2009-regularized-adaptive-notch-filters|Gil-Cacho, van Waterschoot, Moonen & Jensen 2009]] — introduces the RANF method
