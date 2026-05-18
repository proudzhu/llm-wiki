---
type: concept
created: 2026-05-18
updated: 2026-05-18
sources:
aliases:
- Volterra Series
- Truncated Volterra Filter
tags:
- nonlinear-systems
- adaptive-filtering
- signal-processing
---

# Volterra Filter

## Overview

The **Volterra filter** is a polynomial expansion of the input signal that models discrete-time, fading-memory, time-invariant, continuous, finite-memory nonlinear systems. By the **Stone–Weierstrass approximation theorem**, a sufficiently high-order Volterra filter is a *universal approximator* of such systems.

The output of an order-$Q$, memory-$M$ Volterra filter is

$$ y(n) = \sum_{q=1}^{Q} \sum_{m_1=0}^{M-1}\cdots\sum_{m_q=0}^{M-1} h_q(m_1,\dots,m_q)\prod_{i=1}^{q} x(n-m_i), $$

where $h_q(\cdot)$ is the $q$-th order Volterra kernel.

## Linear-in-the-Parameters Form

Volterra filters belong to the **linear-in-the-parameters (LIP)** family. Defining the expanded input vector

$$ \mathbf{x}_e(n) = [\mathbf{x}_1^T(n), \mathbf{x}_2^T(n), \dots, \mathbf{x}_Q^T(n)]^T, \quad \mathbf{x}_j(n) = \mathbf{x}_1(n)\otimes \mathbf{x}_{j-1}(n), $$

the output is simply $y(n) = \mathbf{h}^T \mathbf{x}_e(n)$, so any LMS-style adaptive algorithm can train it.

## Coefficient Count

The number of distinct coefficients is

$$ N_c = \frac{(M+Q)!}{M!\,Q!} - 1, $$

which grows as $M^Q$ — an exponential dimension explosion with respect to nonlinearity order. In practice $Q \leq 3$:
- **Second-order Volterra (SOV)**: $N_c = \tfrac12 M(M+3)$
- **Third-order Volterra (TOV)**: rarely used directly.

## SOV Output Form

$$ y(n) = \sum_{m_1=0}^{M-1} h_1(m_1) x(n{-}m_1) + \sum_{m_1=0}^{M-1}\sum_{m_2=m_1}^{M-1} h_2(m_1, m_2)\,x(n{-}m_1)\,x(n{-}m_2). $$

## Application to NLANC

In [[nonlinear-active-noise-control|NLANC]], Volterra structures replace the linear adaptive filter in the FxLMS framework:

| Algorithm | Cost / criterion | Use case |
|:----------|:-----------------|:---------|
| **VFxLMS** (Tan & Jiang, 1997) | MSE | General nonlinear ANC |
| **VFxAP** (Sicuranza & Carini, 2004) | Affine projection | Multi-channel NLANC |
| **VFxLMP** | $\ell_p$-norm | [[impulsive-noise|Impulsive noise]] |
| **VFxlogLMP / VFxlogCLMP** | Logarithmic $\ell_p$ cost | Stable performance for highly impulsive ($\alpha\approx 1.1$) |
| **VFxRMC** | [[maximum-correntropy-criterion|MCC]] | Robust nonlinear ANC |

## Limitations

- Computational cost grows as $M^Q$.
- Selecting an appropriate truncation order is critical.
- For strong saturating nonlinearities, [[bilinear-filter|bilinear filters]] or [[flann-filter|FLANN]] structures may be more parsimonious.

## Related Concepts

- [[nonlinear-active-noise-control|Nonlinear ANC]]
- [[flann-filter|FLANN Filter]]
- [[bilinear-filter|Bilinear Filter]]
- [[adaptive-filtering|Adaptive Filtering]]
- [[filtered-x-lms-algorithm|Filtered-x LMS]]
- [[system-identification|System Identification]]

## Related Sources

- [[../sources/lu-2021-anc-survey-nonlinear|Lu et al. 2021: Survey on ANC — Part II (Nonlinear)]]
