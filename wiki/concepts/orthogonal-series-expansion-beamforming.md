---
type: concept
created: 2026-09-19
updated: 2026-09-19
sources:
  - raw/papers/pan-2020-microphone-array-beamforming/full-text.txt
tags:
  - beamforming
  - microphone-arrays
  - frequency-invariance
  - approximation
---

# Orthogonal Series Expansion Beamforming

**Orthogonal series expansion beamforming** (正交级数展开波束形成) is a [[concepts/frequency-invariant-beamforming|frequency-invariant beamforming]] design approach for small-aperture arrays: the desired beampattern is represented as a truncated orthogonal series, and the beamforming filter is solved so that the actual array beampattern approximates this target in a minimum-mean-square-error sense, with a loading parameter trading approximation accuracy against [[concepts/white-noise-gain|white noise gain]] (robustness).

## Formulation

The target beampattern is expanded as

$$\mathcal{B}_N(\theta) = \sum_{n=0}^{N} a_n \mathcal{P}_n(\theta)$$

where the basis functions $\mathcal{P}_n(\theta)$ are orthogonal with respect to a non-negative weight function $w(\theta)$:

$$\int \mathcal{P}_m(\theta)\, \mathcal{P}_n(\theta)\, w(\theta)\, d\theta = \begin{cases} \beta_n \ne 0, & m = n \\ 0, & \text{otherwise} \end{cases}$$

Typical choices: **Chebyshev** and **Legendre** series (linear arrays, where $\mathcal{P}_n$ is an $n$th-order polynomial in $\cos\theta$ and $N$ equals the beampattern order), **Jacobi** series (circular arrays), and **spherical harmonics** (spherical arrays). For general array shapes the series can be more complex and $N$ no longer equals the pattern order.

The array's steering vector is expanded in the same basis, $\mathbf{d}(\theta,\omega) = \sum_{n=0}^{N-1} \mathbf{D}_n(\omega) \mathcal{P}_n(\theta)$, and the filter is obtained from the linear system $\boldsymbol{\Psi}(\omega)\mathbf{h}(\omega) = \boldsymbol{\varrho}$ built from the expansion coefficients. Theory shows that minimizing $\mathbf{h}^H \boldsymbol{\Psi} \mathbf{h}$ controls the error between the array beampattern and the target, yielding a frequency-consistent response. A loading parameter $\delta \geq 0$ is embedded in $\boldsymbol{\Psi}(\delta) = \boldsymbol{\Psi} + \delta\mathbf{I}$:

- $\delta = 0$: MMSE-optimal beampattern approximation, but typically poor robustness;
- larger $\delta$: better WNG, but worse frequency consistency.

## Key Results (per Pan, Huang & Chen 2020)

- **Jacobi-series circular arrays**: the frequency-invariant design is minimum-mean-square-error optimal among such expansions, and there are **analytic relations** between the beampattern, directivity factor, WNG, and the number of microphones and array radius — giving theoretical guidance for optimizing circular frequency-invariant beamforming.
- **Bessel-zero singularity**: circular-array filter coefficients involve Bessel functions $J_n(kr)$; as $J_n(kr)$ approaches a zero (typically at high frequencies), the coefficients diverge and array performance collapses. Lower orders suffer worse. Remedies: concentric circular arrays (which also improve high-frequency frequency invariance, robustness, and directivity) and adding a center microphone (fixes the zeroth-order singularity). The concentric structure is flexible — outer rings carry more microphones for high-order pattern components, inner rings fewer for low-order ones; rings need not be aligned, reducing manufacturing constraints and improving robustness.
- **Versus spherical-harmonic-decomposition beamforming** (e.g., Eigenmike): spherical harmonic decomposition requires strict sensor placement to satisfy sampling orthogonality, whereas series-expansion designs impose no strict placement requirements and can achieve frequency-invariant designs with flexible arrays.

## Position in the Field

Within the review's taxonomy, this family is the "beampattern approximation" design philosophy — complementary to the differential-field measurement philosophy of [[concepts/differential-microphone-array|DMAs]] (which the Jacobi circular designs generalize) and the task-decomposition philosophy of [[concepts/kronecker-product-beamforming|Kronecker product beamforming]]. Its distinctive strength is turning frequency-invariant design into a **linear system + loading parameter** procedure with closed-form performance relations.

## Related Concepts

- [[concepts/frequency-invariant-beamforming|Frequency-Invariant Beamforming]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/fixed-beamformer|Fixed Beamformer]]

## Related Sources

- [[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020: Microphone Array Beamforming Methods for Speech Communication and Interaction]] — review section giving the unified formulation and the Jacobi/circular/spherical survey
