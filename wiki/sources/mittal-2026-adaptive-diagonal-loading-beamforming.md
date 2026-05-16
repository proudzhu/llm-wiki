---
type: source
created: 2026-05-07
updated: 2026-05-07
sources:
  - raw/papers/mittal-2026-adaptive-diagonal-loading-beamforming/full-text.md
  - https://arxiv.org/abs/2605.04342
  - zotero://select/items/0_KQQNX9WS
tags:
  - beamforming
  - diagonal-loading
  - robustness
  - microphone-arrays
  - adaptive-filtering
---

# Mittal, Corey, Buck & Singer 2026: Adaptive Diagonal Loading for Norm Constrained Beamforming

**Authors**: [[entities/manan-mittal|Manan Mittal]], [[entities/ryan-corey|Ryan M. Corey]], [[entities/john-buck|John R. Buck]], [[entities/andrew-singer|Andrew C. Singer]]
**Type**: arXiv Preprint (5 pages, 5 figures)
**arXiv**: [2605.04342](https://arxiv.org/abs/2605.04342)
**DOI**: [10.48550/arXiv.2605.04342](https://doi.org/10.48550/arXiv.2605.04342)
**Date**: 2026-05-05
**Zotero**: [KQQNX9WS](zotero://select/items/0_KQQNX9WS)

## Summary

Proposes a novel adaptive [[concepts/diagonal-loading|diagonal loading]] method for [[concepts/mpdr-beamformer|MPDR]]/[[concepts/mvdr-beamformer|MVDR]] beamformers that deterministically guarantees the [[concepts/white-noise-gain|White Noise Gain]] (WNG) stays within specified bounds. By leveraging the [[concepts/kantorovich-inequality|Kantorovich inequality]], the authors map the desired WNG to a strict upper bound on the [[concepts/condition-number|condition number]] of the [[concepts/spatial-covariance-matrix|spatial correlation matrix]]. Three scalable estimation modes (Trace, Gershgorin, Exact EVD) provide O(M) to O(M³) complexity trade-offs.

## Problem Formulation

Adaptive beamformers (MPDR/MVDR) fail under snapshot deficiency — when the number of available frames L is less than or comparable to the number of microphones M, the sample SCM $\hat{\mathbf{R}}_y[i]$ becomes ill-conditioned. This causes the weight vector norm $\|\mathbf{w}\|^2$ to spike, collapsing the WNG and causing severe target signal cancellation.

The MPDR beamformer solves:

$$\min_{\mathbf{w}} \mathbf{w}^H \mathbf{R}_y \mathbf{w} \quad \text{s.t.} \quad \mathbf{w}^H \mathbf{d} = 1$$

with optimal solution $\mathbf{w}_{opt} = \frac{\mathbf{R}_y^{-1}\mathbf{d}}{\mathbf{d}^H \mathbf{R}_y^{-1}\mathbf{d}}$.

The sample SCM is estimated via a short sliding window:

$$\hat{\mathbf{R}}_y[i] = \frac{1}{L}\sum_{l=0}^{L-1} \mathbf{y}[i-l]\mathbf{y}^H[i-l]$$

When $L < M$, $\hat{\mathbf{R}}_y[i]$ is rank-deficient and its inverse amplifies estimation errors.

## Methodology

### Kantorovich-Bounded WNG

The WNG is defined as $W = \frac{1}{\|\mathbf{w}\|^2}$. Using the Kantorovich inequality, the authors derive a relationship between WNG and the SCM condition number $\kappa = \lambda_{\max}/\lambda_{\min}$:

$$\frac{W}{M} \geq \frac{4\kappa}{(\kappa+1)^2}$$

Setting $A_G = M/W_{\min}$ (the maximum allowable array gain degradation), the maximum allowable condition number is:

$$\kappa_{\max} = (2A_G - 1) + 2\sqrt{A_G(A_G - 1)}$$

### Adaptive Diagonal Loading

At each frame, a dynamic loading factor $\mu[i]$ is applied:

$$\mathbf{Q}[i] = \hat{\mathbf{R}}_y[i] + \mu[i]\mathbf{I}$$

The exact required loading to satisfy $\kappa_{loaded} \leq \kappa_{\max}$ is:

$$\mu[i] = \max\left(0, \frac{\lambda_{\max} - \kappa_{\max}\lambda_{\min}}{\kappa_{\max} - 1}\right)$$

### Three Scalable Estimation Modes

| Mode | Complexity | Method | Characteristics |
|------|-----------|--------|-----------------|
| **Trace** | $\mathcal{O}(M)$ | $\lambda_{\max} \leq \text{Tr}(\hat{\mathbf{R}}_y)$, $\lambda_{\min} \approx 0$ | Fastest; conservative (over-loads slightly) |
| **Gershgorin** | $\mathcal{O}(M^2)$ | Gershgorin disc bounds on eigenvalues | Best trade-off; near-EVD performance |
| **Exact EVD** | $\mathcal{O}(M^3)$ | Full eigenvalue decomposition | Optimal loading; highest SINR |

### GSC Formulation

The method is also applicable within the [[concepts/gsc-beamformer|Generalized Sidelobe Canceller]] (GSC) framework. The transformed matrix $\tilde{\mathbf{R}} = \mathbf{T}^H \hat{\mathbf{R}}_y \mathbf{T}$ (where $\mathbf{T} = [\sqrt{M}\mathbf{w}_q, \mathbf{B}]$) shares the same eigenvalues as $\hat{\mathbf{R}}_y$. The loading is applied to the noise correlation matrix:

$$\mathbf{w}_a = (\mathbf{R}_n + \mu[i]\mathbf{I})^{-1}\mathbf{r}_{qn}$$

EVD and Trace modes are invariant under this transformation; Gershgorin is basis-dependent and yields slightly different loading estimates.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Array | ULA, $M = 15$, half-wavelength spacing |
| Center frequency | $f_0 = 1000$ Hz |
| Snapshots | $T = 20000$ |
| Window length | $L = 37$ ($\approx 2.5M$) |
| Target | Broadside ($90^\circ$), SNR = $-5$ dB |
| Interferers | Up to 2, birth-death, INR = $7$ dB |
| WNG bound | $W_{\min} = 10\log_{10}(M) - 3 \approx 8.76$ dB |
| Baselines | Cox et al. (1987) post-hoc scaling, Omniscient Capon |

## Results

- **WNG guarantee**: All three modes strictly maintain WNG $\geq 8.76$ dB at every frame
- **Performance hierarchy**: Exact EVD > Gershgorin > Trace > Cox
- **Gershgorin near-optimal**: Achieves nearly identical SINR to Exact EVD at $\mathcal{O}(M^2)$
- **Trace mode**: Conservative but provides absolute WNG stability at $\mathcal{O}(M)$
- **Cox method**: Post-hoc null-space scaling disrupts spatial filter optimality, yielding worse MSE and slower convergence
- **GSC equivalence**: EVD and Trace modes are invariant between MPDR and GSC; Gershgorin is basis-dependent

![Ground truth spatial spectrum over time](raw/papers/mittal-2026-adaptive-diagonal-loading-beamforming/figures/ground_truth_trial_1.png)

*Figure 1: Ground truth spatial spectrum showing dynamic birth-death interferers and broadside target.*

![Ensemble WNG over time](raw/papers/mittal-2026-adaptive-diagonal-loading-beamforming/figures/wng.png)

*Figure 2: Ensemble White Noise Gain. All proposed methods actively bound WNG above the 8.76 dB threshold.*

## Key Contributions

1. **Analytical WNG-condition number relationship** via the Kantorovich inequality — maps desired WNG to a deterministic $\kappa_{\max}$ bound
2. **Closed-form adaptive diagonal loading** — computes the exact minimal $\mu[i]$ needed to satisfy the WNG constraint at every frame
3. **Three scalable complexity modes** — Trace $\mathcal{O}(M)$, Gershgorin $\mathcal{O}(M^2)$, Exact EVD $\mathcal{O}(M^3)$
4. **Architecture-agnostic formulation** — works in both direct MPDR and partitioned GSC frameworks
5. **Principled alternative to ad-hoc loading** — replaces heuristic fixed-$\mu$ selection with a mathematically guaranteed approach

## Related Concepts

- [[concepts/diagonal-loading|Diagonal Loading]]
- [[concepts/kantorovich-inequality|Kantorovich Inequality]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]
- [[concepts/gsc-beamformer|Generalized Sidelobe Canceller]]
- [[concepts/gershgorin-circle-theorem|Gershgorin Circle Theorem]]
- [[concepts/condition-number|Condition Number]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]

## Related Synthesis

- [[synthesis/adaptive-algorithm-tradeoffs|Adaptive Algorithm Trade-offs]]
