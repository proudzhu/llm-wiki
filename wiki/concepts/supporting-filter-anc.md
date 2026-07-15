---
type: concept
created: 2026-07-15
updated: 2026-07-15
sources:
  - raw/papers/ma-2027-robust-ffanc-online-path-modeling/full-text.md
tags:
  - active-noise-control
  - adaptive-filtering
  - online-modeling
---

# Supporting Filter in ANC

## Overview

A **supporting filter (SF)** in active noise control is an auxiliary adaptive filter included in the ANC architecture to *separate* or *isolate* signal components for different sub-tasks (e.g., [[online-secondary-path-modeling|OSPM]], [[online-feedback-path-modeling|OFBPM]], controller update, [[auxiliary-noise-scaling|AWGN scaling]]). SFs have been used in ANC for three decades; the pioneer trial was Kuo and Vijayan (1997), who introduced a linear prediction filter (LPF) as an SF on the residual error to reduce the interference (coupling) between the OSPM and the controller.

## Purpose

Without an SF, the residual error $e(n)$ in an FFANC with OSPM contains *both*:

- the remaining target noise (controller's responsibility), and
- the injected AWGN (OSPM's excitation).

This mixture couples the OSPM and the controller: the controller's residual acts as additive noise for the OSPM, and the OSPM's AWGN leaks into the controller's update — undermining both convergence and steady-state NRP. An SF breaks this coupling by extracting a cleaner component from $e(n)$ or related signals.

## Two-SF Architecture (Ma 2027)

[[sources/ma-2027-robust-ffanc-online-path-modeling|Ma 2027]] introduces a **second** SF $H_2(z)$ alongside the existing first SF $H_1(z)$ of Ahmed–Akhtar 2013:

| SF | Input | Output | Used for |
|----|-------|--------|----------|
| $H_1(z)$ | FBP-compensated reference $x(n)$ and controller output $y_0(n)$ | $y_1(n)$ — estimate of controller-output contribution to $x(n)$; error $e_1(n)$ ≈ residual AWGN in $x(n)$ | Drives OFBPM update; isolates AWGN component |
| $H_2(z)$ *(new)* | FBP-compensated reference $x(n)$ | $y_2(n)$ — less noisy estimate of remaining target noise; error $e_2(n) = e(n) - y_2(n)$ | (i) Controller FXLMS update, (ii) OSPM desired signal via $e_2(n)$, (iii) AWGN scaling driver |

### $H_2(z)$ update (uses OSPM error to reduce mutual interference)

$$
y_2(n) = \sum_{j=0}^{L_2-1} h_{2,j}(n)\, x(n-j),
$$

$$
h_{2,j}(n+1) = h_{2,j}(n) + \mu_2\, e_s(n)\, x(n-j), \qquad e_s(n) = e_2(n) + y_s(n).
$$

### Length and step-size selection

- If the noise source is **narrowband**, $L_2 \approx L_c$ (controller length).
- If **broadband**, $L_2 \geq L_c$.
- $\mu_2$ must be moderately larger than the controller step size $\mu_c$ so that $H_2(z)$ converges faster than $W(z)$.

## Benefits Quantified (Ma 2027)

- **Decoupling (F1)**: $y_2(n)$ is much less noisy than $e_s(n)$ or $e(n)$, so the controller converges faster and to a lower residual.
- **Lower AWGN scaling (F2)**: because the additive noise $v_p(n)$ is *not* directly in $y_2(n)$, the steady-state scaling factor $G_s(\infty) \propto \mu_2 \sigma_p^2 L_2 P_{x_r}$ can be made much smaller than in prior schemes.
- **Null-vector initialization (F4)**: OSPM and OFBPM filters can start from null vectors — unlike Ahmed–Akhtar 2013, which requires proportional-to-truth initialization.

## Prior SF Variants

The SF concept has appeared in many forms across the ANC literature:

- Linear prediction filter (Kuo–Vijayan 1997)
- FIR filter on residual error (Akhtar 2006)
- Adaptive notch filter bank (Ma–Xiao 2017)
- Bandpass filter bank
- Sinusoidal noise canceller
- CANFB (cascade adaptive notch filter bank) in Bai 2019

These have been applied to broadband ANC with OFBPM or OSPM, feedback ANC with OSPM, hybrid ANC with OSPM, etc. Ma 2027's contribution is the **first** to introduce a second SF (applied to the FBP-compensated reference, not the residual error) in an FFANC with *simultaneous* OSPM + OFBPM, and the first to drive the AWGN scaling by the SF output alone.

## Related Concepts

- [[online-secondary-path-modeling|Online Secondary-Path Modeling]] — OSPM, whose decoupling from the controller is the primary SF role
- [[online-feedback-path-modeling|Online Feedback-Path Modeling]] — OFBPM, the sibling online-modeling problem
- [[auxiliary-noise-scaling|Auxiliary Noise Scaling]] — the AWGN scaling strategy, increasingly driven by SF outputs
- [[feedforward-anc|Feedforward ANC]] — host architecture
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — controller update rule, modified in Ma 2027 to use $y_2(n)$
- [[variable-step-size-lms|Variable Step Size LMS]] — alternative decoupling approach via step-size scheduling

## Related Sources

- [[sources/ma-2027-robust-ffanc-online-path-modeling|Ma 2027: Robust FFANC with Simultaneous OSPM and OFBPM]] — introduces the second SF $H_2(z)$ and analyzes its steady-state statistics
- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — sets the FFANC framework within which SFs are deployed
