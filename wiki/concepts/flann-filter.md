---
type: concept
created: 2026-05-18
updated: 2026-05-18
sources:
aliases:
- FLANN
- Functional Link Artificial Neural Network
- FsLMS
tags:
- nonlinear-systems
- adaptive-filtering
- neural-networks
---

# FLANN Filter

## Overview

The **Functional Link Artificial Neural Network (FLANN)** is a single-layer expansion of the input signal through a fixed set of nonlinear basis functions (most commonly trigonometric). It is a [[volterra-filter|linear-in-the-parameters (LIP)]] structure, so any linear adaptive algorithm — including [[filtered-x-lms-algorithm|FxLMS]] — extends naturally to it. FLANN delivers a favourable accuracy/complexity trade-off compared with Volterra filters and is one of the dominant tools in [[nonlinear-active-noise-control|NLANC]].

## Trigonometric Expansion

For input $x(n)$ with memory $M$ and expansion order $b$:

$$
\mathbf{x}_e(n) = \big\{x(n),\ \sin[\pi x(n)],\ \cos[\pi x(n)],\ \dots,\ \sin[b\pi x(n)],\ \cos[b\pi x(n)],\ \dots,\ x(n{-}M{+}1),\ \sin[b\pi x(n{-}M{+}1)],\ \cos[b\pi x(n{-}M{+}1)]\big\}^T
$$

Coefficient count $N_c = M(2b+1)$ — far below the $M^Q$ growth of Volterra filters.

## FsLMS Algorithm

The **filtered-s LMS (FsLMS)** algorithm (Das & Panda, 2004) is the canonical FLANN-based adaptive filter for ANC. Variants developed in the past decade:

| Variant | Distinguishing feature |
|:--------|:-----------------------|
| **Fast FsLMS** | FFT-based block processing |
| **RFsLMS** | Logarithmic cost — robust to Gaussian and impulsive noise |
| **$q$-gradient FsLMS** | Time-varying $q$ for Gaussian noise; impulsive variant for AINC |
| **FsuLMS** | Convex combination of FsLMS and FuLMS |

## Generalisations

- **GFLANN**: Adds cross-terms between $x(n)$ and $\sin/\cos(b\pi x(n))$ at different time shifts.
- **EFLANN (Exponential FLANN)**: Multiplies trigonometric terms by an exponential factor inspired by Taylor series; faster convergence.
- **RFLANN (Recursive FLANN)**: Uses past output as part of the input — analogous to FuLMS for IIR adaptation.

## Orthogonal-Basis FLANN Variants

Replacing the trigonometric basis with orthogonal polynomials improves convergence by reducing input correlation:

| Filter | Basis | Notes |
|:-------|:------|:------|
| **CN** (Chebyshev) | Chebyshev polynomials | Two recursive properties; fastest convergence among polynomial expansions |
| **FN** (Fourier) | Multidimensional Fourier basis | Not a true universal approximator (boundary discontinuities) |
| **EMFN** (Even-Mirror Fourier) | Symmetric Fourier expansion | Universal approximator; suited for strong nonlinearity |
| **LN** (Legendre) | Legendre polynomials | Mild–medium nonlinearity |

The Chebyshev recursion is

$$ T_{q+1}(x) = 2xT_q(x) - T_{q-1}(x), \quad T_0(x)=1. $$

## Limitations

- Standard trigonometric FLANN/GFLANN do **not** satisfy the Stone–Weierstrass conditions and so cannot universally approximate arbitrary systems.
- Performance depends on choice of basis order $b$.
- Cross-terms in GFLANN/RFLANN can slow convergence if poorly tuned.

## Related Concepts

- [[nonlinear-active-noise-control|Nonlinear ANC]]
- [[volterra-filter|Volterra Filter]]
- [[bilinear-filter|Bilinear Filter]]
- [[adaptive-filtering|Adaptive Filtering]]
- [[filtered-x-lms-algorithm|Filtered-x LMS]]
- [[neural-networks|Neural Networks]]

## Related Sources

- [[../sources/lu-2021-anc-survey-nonlinear|Lu et al. 2021: Survey on ANC — Part II (Nonlinear)]]
