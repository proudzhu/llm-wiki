---
type: concept
created: 2026-05-18
updated: 2026-05-18
sources:
aliases:
- NLANC
- Nonlinear ANC
tags:
- active-noise-control
- nonlinear-systems
- adaptive-filtering
---

# Nonlinear Active Noise Control

## Overview

**Nonlinear Active Noise Control (NLANC)** extends conventional [[active-noise-control|ANC]] to scenarios where the primary path $P(z)$, the secondary path $S(z)$, or the noise source itself exhibits nonlinear behaviour. Linear algorithms such as [[filtered-x-lms-algorithm|FxLMS]] degrade in these conditions because they cannot exploit the full coherence in the noise.

## Sources of Nonlinearity (Lu 2021)

| Type | Examples |
|:-----|:---------|
| **Primary path** | Noise propagating in a duct with very high sound pressure |
| **Secondary path** | Overdriven amplifier, saturated speaker/transducer |
| **System components** | Actuator harmonics; chaotic noise from blowers, grinders, airfoils, fans |

## Algorithm Families

NLANC algorithms are organised by their underlying nonlinear structure:

### Volterra-based
Truncated Volterra series, a "universal approximator" by the Stone–Weierstrass theorem.
- SOV-ANC, TOV-ANC, VFxLMS, VFxLMP, VFxlogLMP, VFxlogCLMP, VFxRMC ([[maximum-correntropy-criterion|MCC]]-based), VFxAP.
- Coefficient count grows as $M^Q$ — only second/third order are practical.

### FLANN-based
[[flann-filter|Functional Link ANN]] expansions: trigonometric, Chebyshev (CN), Fourier (FN), Even-Mirror Fourier (EMFN), Legendre (LN). Linear-in-the-parameters → easy adaptation. Variants:
- FsLMS family: classical, fast, robust (RFsLMS), $q$-gradient
- GFLANN, EFLANN, RFLANN (recursive, FuLMS-style)

### Hammerstein / Wiener / Hammerstein–Wiener
Cascade of static nonlinearity and linear dynamics in different orderings (N–L, L–N, N–L–N, L–N–L).

### Bilinear ANC
Cross-products of past inputs and outputs; suited to strong saturation with shorter filters.

### Spline ANC
[[spline-adaptive-filter|Spline adaptive filter]] with adaptive look-up table interpolated by polynomial splines. Both FIR-spline and IIR-spline variants.

### Kernel Adaptive Filter ANC
[[kernel-adaptive-filter|KAF]] in an RKHS via Gaussian / logistic / tan-sigmoid / inverse-tan kernels.

### Heuristic-based
Global optimisers when secondary path is non-convex: [[heuristic-anc-algorithms|GA, PSO, BFO, BSA, FF, FWA]].

### Distributed NLANC
EFLANN/FLANN expansions inside diffusion or incremental algorithms for [[multi-channel-anc|wireless acoustic sensor networks]].

## Cost Functions

When noise is non-Gaussian or impulsive, NLANC uses robust costs:
- Logarithmic $\ell_p$ cost (VFxlogLMP)
- [[maximum-correntropy-criterion|Maximum Correntropy Criterion]] (VFxRMC)
- [[renyi-entropy|Rényi's entropy]] (GFx-IECGD)
- $\ell_p$-norm with $p<2$ for [[impulsive-noise|impulsive noise]]

## Coefficient Count Comparison

| Filter | $N_c$ |
|:-------|:------|
| SOV (second-order Volterra) | $\tfrac12 M(M+3)$ |
| FLANN (trigonometric) | $M(2b+1)$ |
| GFLANN | $M(2b+1)+1$ |
| Chebyshev (CN) | $2M+1$ |
| Legendre (LN) | $QM + 1$ |
| Bilinear | $N_1^2 + 3N_1 + 1$ |

FLANN-based filters carry roughly an order of magnitude less computation than equivalent Volterra structures.

## Open Challenges

1. Theoretical analysis under α-stable noise (infinite variance breaks MSE assumptions).
2. Sparsification of KAF dictionaries (quantised, set-membership schemes).
3. Practical, low-complexity implementations beyond laboratory setups.
4. ANC-IoT integration including impulsive noise, distributed nodes, Internet of Vehicles.
5. Cost-effective application scenarios for large-scale deployment.

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[volterra-filter|Volterra Filter]]
- [[flann-filter|FLANN Filter]]
- [[spline-adaptive-filter|Spline Adaptive Filter]]
- [[kernel-adaptive-filter|Kernel Adaptive Filter]]
- [[bilinear-filter|Bilinear Filter]]
- [[heuristic-anc-algorithms|Heuristic ANC Algorithms]]
- [[filtered-x-lms-algorithm|Filtered-x LMS]]
- [[impulsive-noise|Impulsive Noise]]
- [[maximum-correntropy-criterion|Maximum Correntropy Criterion]]

## Related Sources

- [[../sources/lu-2021-anc-survey-nonlinear|Lu et al. 2021: Survey on ANC — Part II (Nonlinear)]] — Comprehensive 2009–2020 review
- [[../sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: ANC Tutorial Review]] — Linear ANC foundations
