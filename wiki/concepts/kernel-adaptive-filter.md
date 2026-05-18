---
type: concept
created: 2026-05-18
updated: 2026-05-18
sources:
aliases:
- KAF
- KLMS
tags:
- nonlinear-systems
- adaptive-filtering
- kernel-methods
---

# Kernel Adaptive Filter

## Overview

A **Kernel Adaptive Filter (KAF)** uses the [[kernel-methods|kernel trick]] to recast input data from the input space $\mathcal{U}$ into a high-dimensional **Reproducing Kernel Hilbert Space (RKHS)** $\mathcal{F}$, allowing a linear adaptive algorithm in $\mathcal{F}$ to realise nonlinear filtering in $\mathcal{U}$. KAFs are well-suited to [[nonlinear-active-noise-control|NLANC]] when the nonlinearity is unknown or hard to parameterise, and were first applied to NLANC by Mahesh et al. in 2009.

## Mathematical Formulation

Let $\phi: \mathcal{U} \to \mathcal{F}$ be the nonlinear feature mapping. By **Mercer's theorem**, inner products in $\mathcal{F}$ are given by a kernel function:

$$ \langle \phi(\mathbf{X}), \phi(\mathbf{X}') \rangle = \kappa(\mathbf{X}, \mathbf{X}'). $$

Most commonly the **Gaussian kernel**

$$ \kappa(\mathbf{X}, \mathbf{X}') = \exp\!\left(-\sigma\,\|\mathbf{X}-\mathbf{X}'\|^2\right) $$

is used, where $\sigma$ is the kernel size. The KAF output is a weighted sum over a *dictionary* of past input samples:

$$ y(n) = \sum_{j=1}^{n} a_j\,\kappa(\mathbf{X}, \mathbf{X}_j). $$

## Application to NLANC

The first NLANC-KAF (2009) handled chaotic-noise scenarios with a nonlinear primary path only. Subsequent work extended KAF-ANC to:
- Nonlinear secondary paths.
- Multi-tonal and sinusoidal noise sources.
- Alternative kernels: **logistic**, **tan-sigmoid**, **inverse-tan** — improved performance over Gaussian in some scenarios.

## Limitations

The dictionary grows linearly with the number of samples processed, so computational and memory costs grow without bound. **Sparsification** schemes curb this:

| Scheme | Mechanism |
|:-------|:----------|
| **Quantised KAF** | Coarsen input space; dictionary entries with similar inputs are merged |
| **Set-membership KAF** | Update only when residual error exceeds a threshold |
| **Coherence-based** | Add a new dictionary entry only when sufficiently dissimilar from existing ones |

## Choice of Kernel

Gaussian is the default due to:
- Universal approximation property.
- Numerical stability.
- Smoothness and infinite differentiability.

The **kernel size $\sigma$** is the dominant tuning parameter; it controls the bias-variance trade-off in feature space.

## Related Concepts

- [[kernel-methods|Kernel Methods]]
- [[nonlinear-active-noise-control|Nonlinear ANC]]
- [[correntropy|Correntropy]] — also kernel-based
- [[maximum-correntropy-criterion|Maximum Correntropy Criterion]]
- [[adaptive-filtering|Adaptive Filtering]]
- [[filtered-x-lms-algorithm|Filtered-x LMS]]

## Related Sources

- [[../sources/lu-2021-anc-survey-nonlinear|Lu et al. 2021: Survey on ANC — Part II (Nonlinear)]]
