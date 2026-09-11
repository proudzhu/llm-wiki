---
type: concept
created: 2026-07-15
updated: 2026-09-11
sources:
  - raw/papers/ma-2027-robust-ffanc-online-path-modeling/full-text.md
  - raw/papers/zhang-2026-feedback-path-mitigation-mcanc/full-text.md
tags:
  - active-noise-control
  - online-modeling
  - acoustic-feedback
  - adaptive-filtering
  - relative-transfer-matrix
---

# Online Feedback-Path Modeling

## Overview

**Online feedback-path modeling (OFBPM)** — also called *online feedback-path cancellation* — adaptively estimates and compensates the [[acoustic-feedback|Acoustic Feedback]] path $F(z)$ from the secondary source back to the reference microphone *while the ANC system is operating*. This contrasts with **offline feedback-path estimation**, where $F(z)$ is measured during an idle phase and held fixed during ANC operation. OFBPM is essential in real applications where $F(z)$ drifts due to temperature, airflow, headset positioning, or component aging — drifts that, if uncompensated, degrade FFANC performance or destabilize the closed loop.

## Why Online?

The original FFANC of [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999]] uses a fixed FIR estimate $\hat{F}(z)$ obtained offline. This estimate becomes stale when:

- A headset is repositioned on the head
- Duct airflow speed changes
- The acoustic environment near the secondary source changes
- Loudspeaker characteristics drift with temperature

In such cases, the uncompensated $F(z)$ residual corrupts the reference signal $r(n)$, leading to slower convergence, lower NRP, or instability.

## Standard Approach: Auxiliary Noise Injection

Following Eriksson's original 1987 patent, OFBPM is typically driven by the **same auxiliary white Gaussian noise (AWGN)** $v(n)$ injected for [[online-secondary-path-modeling|Online Secondary-Path Modeling]]:

$$
v(n) = G_s(n)\, v_o(n),
$$

where $v_o(n)$ is zero-mean AWGN and $G_s(n)$ is a scheduling gain. An adaptive filter $\hat{F}_n(z)$ models the FBP:

$$
\hat{s}_{f,m}(n+1) = \hat{s}_{f,m}(n) + \mu_f\, e_1(n)\, v(n-m),
$$

with $e_1(n)$ a suitable error signal (e.g., the first supporting-filter error in [[sources/ma-2027-robust-ffanc-online-path-modeling|Ma 2027]]). The FBP-compensated reference is then

$$
x(n) = r(n) - \sum_{m=0}^{\hat{M}_f-1} \hat{s}_{f,m}(n)\, y(n-m).
$$

## Coupling with OSPM

Because OFBPM and [[online-secondary-path-modeling|OSPM]] share the same injected AWGN, a coupling — small or large — exists between them. Simultaneous OSPM + OFBPM is technically demanding: only a handful of FFANC architectures have been published with both (Kuo–Ill 1999; Ahmed–Akhtar 2013; Xiao et al. 2019; Bai et al. 2019; Ma 2027). The coupling is one of the central challenges tackled by [[sources/ma-2027-robust-ffanc-online-path-modeling|Ma 2027]] via the second supporting filter $H_2(z)$.

## AWGN Scheduling Strategies

Two families of AWGN scaling strategies have been developed to reduce the injected-AWGN contribution to the residual error:

1. **Local scheduling** (Ahmed–Akhtar 2013, Eq. 22) — driven by OSPM and OFBPM error powers $P_{e_1}, P_{e_s}$; minimizes modeling error but not the global residual.
2. **Global scheduling** (Bai 2019, Eq. 37; Ma 2027, Eq. 43) — driven by a nonlinear function of the residual error (Bai) or of the second SF output $y_2(n)$ (Ma); directly targets the global residual noise. Ma 2027 shows that driving the scaling by $y_2(n)$ — which excludes the additive noise $v_p(n)$ — yields a lower steady-state $G_s(\infty)$ and better NRP.

See [[auxiliary-noise-scaling|Auxiliary Noise Scaling]] for a detailed comparison.

## Initialization Considerations

The OFBPM filter $\hat{F}_n(z)$ initialization is delicate in some architectures:

- **Ahmed–Akhtar 2013 (Sys-B)**: initial weights cannot be null; must be proportional to truth (initial modeling accuracy ≈ −5 dB) — impractical when abrupt path changes occur mid-run.
- **Ma 2027 (Sys-D)**: null-vector initialization is admissible thanks to the second supporting filter $H_2(z)$, which decouples the OFBPM/OSPM from the controller.

## Non-Adaptive Alternative: One-Shot Identification Under Persistent Noise

OFBPM is not the only way to handle a feedback path that conventional offline estimation cannot measure. A contrasting strategy keeps the *non-adaptive* structure of offline FBPM but removes its precondition: instead of requiring the primary noise to be silenced, it isolates the secondary field from **covariance differences**.

[[sources/zhang-2026-feedback-path-mitigation-mcanc|Zhang et al. 2026]] apply this to a multichannel ANC array. Two measurement stages — primary-only (loudspeakers off) and total (loudspeakers probing with the primary still running) — give $\boldsymbol{\Phi}^{(\mathrm{Sec})} = \boldsymbol{\Phi}^{(\mathrm{Tot})} - \boldsymbol{\Phi}^{(\mathrm{Pri})}$ by [[concepts/covariance-subtraction|covariance subtraction]], from which a [[concepts/relative-transfer-matrix|Relative Transfer Matrix]] between a reference microphone group and a feedback microphone group is estimated once and then held fixed.

Trade-offs against OFBPM:

| Aspect | OFBPM (auxiliary-noise adaptive) | One-shot ReTM + covariance subtraction |
|---|---|---|
| Tracks secondary-side drift | Yes, continuously | No — explicitly listed as future work |
| In-operation auxiliary noise | Required (raises the residual floor, mitigated by AWGN scaling) | None — probing confined to the identification stage |
| Model-order choice | Per-path FIR length $\hat{M}_f$ | Fixed $J_{\mathrm{R}} \times J_{\mathrm{F}}$ matrix, no per-path order |
| Identification signal | Secondary output $y(n)$ observed at a reference mic | Second-order statistics across two microphone *groups* (needs an extra array) |
| Bias under persistent primary noise | Unbiased by construction (auxiliary noise dominates locally) | Unbiased provided primary and probe components are mutually independent |

The two are complementary rather than competing: OFBPM buys drift tracking at the cost of an in-operation noise floor, while the covariance-subtracted ReTM buys identification under ongoing primary noise at the cost of a mapping that cannot adapt.

## Related Concepts

- [[acoustic-feedback|Acoustic Feedback]] — the physical phenomenon OFBPM compensates
- [[online-secondary-path-modeling|Online Secondary-Path Modeling]] — sibling online-modeling problem; the two are coupled when both are active
- [[auxiliary-noise-scaling|Auxiliary Noise Scaling]] — strategies to reduce the injected-AWGN contribution
- [[supporting-filter-anc|Supporting Filter in ANC]] — the $H_1(z)$/$H_2(z)$ mechanism used to decouple OFBPM/OSPM from the controller
- [[feedforward-anc|Feedforward ANC]] — host architecture
- [[hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]] — related but hearing-aid-specific AFC problem
- [[concepts/relative-transfer-matrix|Relative Transfer Matrix (ReTM)]] — group-to-group mapping used by the non-adaptive one-shot alternative
- [[concepts/covariance-subtraction|Covariance Subtraction]] — estimator that replaces the ANC-idle window for FBP/ReTM identification

## Related Sources

- [[sources/ma-2027-robust-ffanc-online-path-modeling|Ma 2027: Robust FFANC with Simultaneous OSPM and OFBPM]] — proposes the $H_2(z)$-driven global AWGN scaling for OFBPM
- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section II-D covers the original offline feedback neutralization
- [[sources/zhang-2026-feedback-path-mitigation-mcanc|Zhang, Abhayapala, Samarasinghe & Bastine 2026: Acoustic Feedback Path Mitigation for Multichannel ANC]] — non-adaptive alternative: a covariance-subtracted ReTM identified once, stable where a no-mitigation multichannel FxLMS baseline diverges
