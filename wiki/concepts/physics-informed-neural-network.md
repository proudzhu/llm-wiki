---
type: concept
created: 2026-06-25
updated: 2026-09-12
sources:
  - raw/papers/zhang-2024-active-noise-control-soundfield-interpolation-pinn/full-text.md
  - raw/papers/jiang-2025-ai-driven-avnc-review/full-text.md
  - raw/papers/scarpiniti-2027-physics-informed-adaptive-filtering-aec/full-text.md
tags:
  - neural-networks
  - physics-informed
  - pde
  - acoustics
---

# Physics-Informed Neural Network

## Overview

A **Physics-Informed Neural Network (PINN)** is a neural network trained to approximate solutions to partial differential equations (PDEs) by incorporating the governing physical laws into the loss function as a regularization term. PINNs leverage automatic differentiation to compute the PDE residuals at arbitrary collocation points, enabling data-efficient learning that respects known physics.

## Formulation

A PINN minimizes a composite loss function with two terms:

$$
\mathcal{L} = \mathcal{L}_\text{data} + \lambda \, \mathcal{L}_\text{PDE}
$$

- **$\mathcal{L}_\text{data}$**: Supervised loss (MSE) at measurement points where ground-truth values are known.
- **$\mathcal{L}_\text{PDE}$**: PDE residual loss enforcing the governing physical equations at collocation points throughout the domain.
- **$\lambda$**: Weighting factor balancing data fidelity against physical consistency.

The PDE residuals are computed via automatic differentiation of the network output with respect to its inputs, avoiding the need for numerical discretization of the PDE.

## Applications in Acoustics

### Soundfield Interpolation (Zhang et al. 2024)

In [[active-noise-control|Active Noise Control]], a PINN with 1 hidden layer and 16 neurons is used to interpolate the soundfield from 8 monitoring microphones placed outside the region of interest. The PDE loss enforces the acoustic wave equation:

$$
\nabla^2 p - \frac{1}{c^2} \frac{\partial^2 p}{\partial t^2} = 0,
$$

where $c$ is the speed of sound. See [[sources/zhang-2024-active-noise-control-soundfield-interpolation-pinn|Zhang et al. 2024: ANC with PINN-based Soundfield Interpolation]].

## Advantages

- **Data efficiency**: Fewer measurements needed, as the PDE constraint regularizes the solution.
- **Continuous representation**: No grid discretization required.
- **Incorporation of boundary conditions**: Hard or soft constraints can be encoded directly.

## Limitations

- **Training cost**: Requires many epochs and careful tuning.
- **Stiff PDEs**: Problems with high-frequency content are difficult.
- **Generalization**: Performance degrades for domains not seen during training.

## Beyond PDE Residuals: Physics-Informed Adaptive Filtering

The physics-informed idea extends beyond PDE-residual losses. [[sources/scarpiniti-2027-physics-informed-adaptive-filtering-aec|Scarpiniti et al. 2027]]'s Physics-Informed NLMS (PI-NLMS) for acoustic echo cancellation embeds physically motivated priors on the room impulse response — causality, exponential energy decay (Sabine), time-weighted sparsity of early reflections, spectral smoothness, and slow temporal variation — as regularization terms in the adaptive-filter cost function. Compared with PINNs, the physics enters as structured penalties on an interpretable filter estimate rather than autodifferentiated PDE residuals, yielding convergence guarantees at only $\mathcal{O}(L \log L)$ additional cost. See [[concepts/pi-nlms|PI-NLMS]].

## Related Concepts

- [[neural-networks|Neural Networks]]
- [[soundfield-interpolation|Soundfield Interpolation]]
- [[active-noise-control|Active Noise Control]]
- [[active-vibration-control|Active Vibration Control]]
- [[input-shaping|Input Shaping]]
- [[spherical-harmonic-transform|Spherical Harmonic Transform]]
- [[concepts/pi-nlms|Physics-Informed NLMS (PI-NLMS)]]

## Related Sources

- [[sources/zhang-2024-active-noise-control-soundfield-interpolation-pinn|Zhang et al. 2024: ANC with PINN-based Soundfield Interpolation]]
- [[sources/jiang-2025-ai-driven-avnc-review|Jiang et al. 2025: AI-Driven AVNC Review]]
- [[sources/scarpiniti-2027-physics-informed-adaptive-filtering-aec|Scarpiniti, Comminiello & Uncini 2027: Physics-informed adaptive filtering for AEC]] — RIR physical priors as regularization in adaptive filtering (PI-NLMS), a non-PDE branch of the physics-informed family
