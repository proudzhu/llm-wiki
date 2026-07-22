---
type: concept
created: 2026-07-22
updated: 2026-07-22
tags:
  - adaptive-filtering
  - acoustic-echo-cancellation
  - physics-informed
  - room-impulse-response
  - regularization
---

# Physics-Informed NLMS (PI-NLMS)

**PI-NLMS (Physics-Informed Normalized Least-Mean-Squares)** is an adaptive filtering algorithm for [[concepts/acoustic-echo-cancellation|acoustic echo cancellation (AEC)]] that incorporates physically motivated priors about room impulse response structure into the NLMS update. It was introduced by Scarpiniti, Comminiello & Uncini (2027) as the core algorithm of the **Physics-Informed Adaptive Filtering (PIAF)** framework.

## Motivation

Conventional adaptive filters (NLMS, PNLMS) treat echo path identification as an unconstrained linear system identification problem. However, room impulse responses (RIRs) obey well-established physical laws: causality, exponential energy decay, sparse early reflections, spectral smoothness, and slow temporal variation. By incorporating these priors, PI-NLMS constrains the adaptation to a physically plausible echo-path manifold, improving conditioning and reducing variance without substantially increasing computational complexity.

## Composite Cost Function

PI-NLMS minimizes a composite objective that augments the instantaneous squared error with physically motivated regularization terms:

$$
J(n) = \frac{1}{2} e^2(n) + \sum_{i=1}^{M} \Phi_i(\mathbf{w}_n),
$$

where $\Phi_i(\mathbf{w}_n)$ encode the physical priors and $e(n) = d(n) - \mathbf{w}_n^\top \mathbf{x}_n$ is the error signal.

## Physical Priors

PI-NLMS incorporates five physically motivated priors:

| Prior | Type | Form | Physical Basis |
|-------|------|------|----------------|
| **Causality** | Hard (projection) | $w_k = 0,\ k < \tau_\text{min}$ | Finite sound propagation speed |
| **Exponential decay** | Soft ($\ell_2$ weight) | $\frac{1}{2}\sum e^{\alpha k} w_k^2$ | Sabine's reverberation theory |
| **Sparsity** | Soft ($\ell_1$-like) | $\sum \beta_k \|w_k\|$, $\beta_k = e^{-\eta k}$ | Sparse early reflections |
| **Temporal smoothness** | Soft (Laplacian) | $\frac{1}{2}\sum (w_k - w_{k-1})^2$ | Band-limited transducer response |
| **Spectral smoothness** | Soft (frequency Laplacian) | $\frac{1}{2}\sum (W_k - W_{k-1})^2$ | Smooth acoustic transfer function |
| **Slow temporal variation** | Soft ($\ell_2$ difference) | $\frac{1}{2}\|\mathbf{w}_n - \mathbf{w}_{n-1}\|^2$ | Slow environmental changes |

All soft priors are combined into a total regularization term:

$$
\Phi(\mathbf{w}_n) = \frac{1}{2} \mathbf{w}_n^\top \boldsymbol{\Lambda} \mathbf{w}_n - \mathbf{b}^\top \mathbf{w}_n + a,
$$

where $\boldsymbol{\Lambda} = \boldsymbol{\Lambda}_\text{decay} + \boldsymbol{\Lambda}_{\ell_1} + \boldsymbol{\Lambda}_\text{ts} + \boldsymbol{\Lambda}_\text{ss} + \boldsymbol{\Lambda}_t$.

## Algorithm

The PI-NLMS update rule is:

$$
\mathbf{w}_{n+1} = \mathbf{w}_n + \mu_n e(n) \mathbf{x}_n - \mu_n \underbrace{(\boldsymbol{\Lambda} \mathbf{w}_n - \mathbf{b})}_{\mathbf{g}_\text{phys}(n)},
$$

followed by causality projection: $w_k(n+1) = 0$ for all $k < \tau_\text{min}$.

The physics gradient $\mathbf{g}_\text{phys}(n)$ pulls the estimate toward the physically plausible subspace, counteracting noise-driven drift in weakly-excited modes.

## Convergence Properties

The regularization modifies the effective input correlation matrix:

$$
\mathbf{R}_\text{eff} = \mathbf{R}_x + \boldsymbol{\Lambda},
$$

improving conditioning and enabling stable adaptation with larger effective step-size bounds. The steady-state MSD under white input is:

$$
\text{MSD} = \frac{\mu_n L \sigma_v^2}{2} \cdot \frac{\sigma_x^2}{\sigma_x^2 + \lambda},
$$

showing variance reduction proportional to regularization strength $\lambda$, at the cost of a controlled bias.

## Complexity

PI-NLMS preserves NLMS-level computational efficiency:

- $\mathcal{O}(L)$ per iteration without spectral smoothness prior ($7L$ mults, $6L$ adds)
- $\mathcal{O}(L \log L)$ with spectral smoothness prior ($7L + \frac{L}{2}\log_2 L$ mults)
- Suitable for real-time AEC with filter lengths of hundreds to thousands of taps

## Related Concepts

- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/physics-informed-neural-network|Physics-Informed Neural Network]]
- [[concepts/frequency-domain-kalman-filter|Frequency-Domain Kalman Filter]]
- [[concepts/kalman-filter|Kalman Filter]]
- [[concepts/spline-adaptive-filter|Spline Adaptive Filter]]

## Related Sources

- [[sources/scarpiniti-2027-physics-informed-adaptive-filtering-aec|Scarpiniti, Comminiello & Uncini 2027: Physics-informed adaptive filtering for acoustic echo cancellation]]
