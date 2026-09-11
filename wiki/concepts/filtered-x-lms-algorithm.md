---
type: concept
created: 2026-04-10
updated: 2026-09-11
sources:
  - raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/full-text.md
  - raw/papers/jiang-2025-ai-driven-avnc-review/full-text.md
  - raw/papers/zhang-2026-feedback-path-mitigation-mcanc/full-text.md
tags:
- adaptive-algorithms
- lms
- signal-processing
---

# Filtered-x LMS Algorithm

## Overview

The **Filtered-x Least Mean Square (FxLMS)** algorithm is the most widely used adaptive algorithm in [[active-noise-control|Active Noise Control]] systems. It is a variant of the standard LMS algorithm that accounts for the **secondary path** between the controller output and the error sensor.

## Why "Filtered-x"?

In standard LMS, the weight update is:

```
w(n+1) = w(n) + μ · e(n) · x(n)
```

In ANC, the error signal is affected by the secondary path S(z). The FxLMS algorithm accounts for this by filtering the reference signal x(n) through an **estimate of the secondary path** Ŝ(z) before using it in the weight update:

```
x_f(n) = Ŝ(z) * x(n)    (convolution)
w(n+1) = w(n) + μ · e(n) · x_f(n)
```

## Key Parameters

| Parameter | Description |
|-----------|-------------|
| **μ (step size)** | Controls convergence speed and stability; larger = faster but less stable |
| **Ŝ(z)** | Estimated secondary path response (typically an FIR filter with hundreds or thousands of coefficients) |
| **Filter length** | Number of taps in the adaptive filter; more taps = better performance but higher computation |

## Computational Burden

The FxLMS algorithm requires a **convolution operation** to filter the reference signal through Ŝ(z). When Ŝ(z) has hundreds or thousands of coefficients, this becomes a heavy burden for real-time controllers — especially in multi-channel ANC systems. This computational burden motivated the [[simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]] approach.

## Stability Condition

For stability, the phase difference between the true secondary path and its estimation must be within π/2 radians:

```
|∠S(e^jω) - ∠Ŝ(e^jω)| < π/2,  ∀ω
```

For MIMO systems, a sufficient stability criterion is:

$$\Re\left\{\text{eig}\left[\hat{\mathbf{G}}^H(\omega)\mathbf{G}(\omega)\right]\right\} > 0 \quad \forall\omega$$

where $\mathbf{G}(\omega)$ and $\hat{\mathbf{G}}(\omega)$ are the Fourier transforms of the actual and estimated secondary paths. This underlines the need for accurate secondary path estimates — approaches like [[secondary-path-interpolation|Secondary Path Interpolation]] via [[dynamic-time-warping|DTW]] can extend the stable frequency range by improving phase accuracy of interpolated paths.

## Variants

- [[leaky-fxlms-algorithm|Leaky FxLMS Algorithm]] — Adds a leakage coefficient to limit filter gain, improving stability
- Normalized FxLMS — Adapts step size based on reference signal power

## Statistics-Based Counterpart: FxMWF

When the control filter must adapt during *both* noise-only and speech-plus-noise periods (as in hearing-aid NR+ANC), gradient-based FxLMS updates become inconvenient. [[sources/serizel-2010-integrated-anc-nr-hearing-aids|Serizel et al. 2010]] instead compute the filtered-x controller in closed form from estimated second-order statistics — the [[concepts/filtered-x-mwf|Filtered-x MWF]] — a Wiener solution $\mathbf{w} = \mathbf{R}_{\hat{y}\hat{y}}^{-1}\mathbf{r}_{\hat{y}d}$ on secondary-path-filtered references that integrates noise reduction and ANC in one filter set.

## Feedback-Contaminated References in Multichannel FxLMS

FxLMS assumes the reference signal is a clean measurement of the primary noise. When the secondary loudspeaker radiates back into the reference microphone, the weight update is driven by a reference that contains the controller's own output, and the closed loop can destabilize. In multichannel arrays this is reached at moderate loudspeaker-to-microphone coupling: [[sources/zhang-2026-feedback-path-mitigation-mcanc|Zhang et al. 2026]] report their no-mitigation multichannel FxLMS baseline diverging at a secondary-source radius of 0.35 m for **every** tested step size, and at 0.3 m for $\mu = 0.01$.

The remedy can be applied *outside* the adaptation law: subtract an estimate of the loudspeaker leakage from the reference before it enters FxLMS. [[sources/zhang-2026-feedback-path-mitigation-mcanc|Zhang et al. 2026]] use a [[concepts/relative-transfer-matrix|Relative Transfer Matrix]] for this, replacing both the filtered reference $\mathbf{M}_{\mathrm{R}}^{\prime}$ in the weight update (Eq. 16) and the power estimate $\hat{\mathbf{P}}$ in the normalization (Eq. 18) with their feedback-subtracted versions — the normalized frequency-domain FxLMS of [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo & Morgan 1999]] then runs unmodified. Note that the quantity fed to the controller is not the clean primary reference but $\mathbf{P}_{\mathrm{R}} - \mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})}\mathbf{P}_{\mathrm{F}}$, so feedback neutralization alters the effective primary path as well as removing the leakage.

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]]
- [[concepts/simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]]
- [[concepts/online-secondary-path-estimation|Online Secondary Path Estimation]]
- [[concepts/subband-adaptive-filter|Subband Adaptive Filter]]
- [[concepts/distributed-anc|Distributed ANC]]
- [[concepts/sparse-anc|Sparse ANC]]
- [[concepts/convex-combination-anc|Convex Combination ANC]]
- [[concepts/filtered-x-mwf|Filtered-x MWF (FxMWF)]] — closed-form, statistics-based filtered-x controller
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the phenomenon that corrupts the reference signal driving the update
- [[concepts/relative-transfer-matrix|Relative Transfer Matrix (ReTM)]] — spatial-subtraction front end used to clean the reference

## Related Sources

- [[sources/lu-2021-survey-active-noise-control-linear|Lu et al. 2021: Survey on ANC — Part I: Linear Systems]]
- [[sources/serizel-2010-integrated-anc-nr-hearing-aids|Serizel, Moonen, Wouters & Jensen 2010: Integrated ANC and NR in Hearing Aids]] — replaces gradient FxLMS adaptation with a Wiener solution on filtered references
- [[sources/fujii-2006-simultaneous-equations-anc|Fujii et al. 2006: Verification of Simultaneous Equations Method — a method avoiding the secondary path filter requirement of FxLMS]]
- [[sources/jiang-2025-ai-driven-avnc-review|Jiang et al. 2025: AI-Driven AVNC Review]]
- [[sources/ma-2027-robust-ffanc-online-path-modeling|Ma 2027: Robust FFANC with Simultaneous OSPM and OFBPM]] — modifies the FXLMS update to use the second SF output $y_2(n)$ instead of the residual error $e(n)$, reducing the influence of additive noise and injected AWGN
- [[sources/guo-2024-anc-saturation-survey|Guo et al. 2024: ANC Algorithms Overcoming Output Saturation]] — uses FxLMS as the baseline for the output-saturation analysis and complexity comparison of saturation-mitigation algorithms
- [[sources/zhang-2026-feedback-path-mitigation-mcanc|Zhang, Abhayapala, Samarasinghe & Bastine 2026: Acoustic Feedback Path Mitigation for Multichannel ANC]] — keeps the normalized frequency-domain FxLMS update intact and makes the reference feedback-free upstream; documents the step-size/spacing region where unmitigated multichannel FxLMS diverges
