---
type: concept
created: 2026-10-03
updated: 2026-10-03
sources:
  - raw/papers/jin-2021-steering-study-ldma/full-text.txt
  - raw/papers/huang-2026-dual-mic-steerable-neural-beamformer/full-text.md
tags:
  - differential-microphone-array
  - beamforming
  - beam-steering
  - microphone-arrays
---

# Steerable LDMA

A steerable linear differential microphone array (SLDMA) is a linear DMA whose mainlobe can be pointed at an arbitrary look direction $\theta_s \in [0°, 180°]$ rather than only at endfire. The concept was established by [[entities/jilu-jin|Jin]] et al. ([[sources/jin-2021-steering-study-ldma|2021]]), who proved the steering limits of LDMAs and derived the design conditions below. With LDMAs, full steerability (a pure rotation of the endfire beampattern) is impossible; the achievable optimum is **partial steerability** — distortionless response at $\theta_s$ with pattern magnitude $\leq 1$ elsewhere.

## Ideal Function and Visible Zone

Every Nth-order DMA beampattern corresponds to a polynomial in $x = \cos\theta$ (the **ideal function**):

$$
P_N(x) = \sum_{n=0}^{N} a_{N,n} x^n = a_{N,N} \prod_{n=1}^{N} (x - x_n), \qquad P_N(x_s) = 1
$$

Because the beampattern is periodic in $x$ with period $c/(f\delta) \gg 1$ for small arrays, only the segment $-1 \leq x \leq 1$ (the **visible zone**) maps to physical directions. Nulls placed outside the visible zone (e.g., a subcardioid's null at $x = -1.5$) still shape the visible pattern and are legitimate design degrees of freedom.

## Steering Conditions

- **First order: not steerable.** The derivative $dP_1/d\theta = -a_{1,1}\sqrt{1-x^2}$ vanishes only at $x = \pm 1$ (endfire). No first-order LDMA beamformer — whatever the method — can place its mainlobe off endfire.
- **Second order:** $x_1 + x_2 = 2x_s$ — the two nulls must sit symmetrically about the steering direction.
- **Nth order ($N \geq 2$), general condition:**

$$
\sum_{n=1}^{N} n(-1)^{N-n}\,\zeta_{N,n}\, x_s^{\,n-1} = 0
$$

with $\zeta_{N,n}$ the elementary symmetric polynomials in the nulls $x_1, \ldots, x_N$.

## Design Procedure (Null-Constrained SLDMA)

1. Fix the look direction $x_s = \cos\theta_s$.
2. Choose the first $N-1$ nulls per application needs (nulls may repeat, with multiplicity handled by derivative constraints).
3. Solve for the last null from the steering condition — via the linear system $\mathbf{Q}(\mathbf{x})\mathbf{a}_N = \mathbf{i}_1$ (steering row $\mathbf{q}_N^T(x_s)$, derivative row $\mathbf{q}_N^T(x_s)\boldsymbol{\Sigma}_N$, null rows) and $x_N = -a_{N,N-1}/a_{N,N} - \sum_{n=1}^{N-1} x_n$.
4. Compute the beamforming filter from the null-constrained system $\mathbf{D}(\omega, \mathbf{x}_N)\mathbf{h}(\omega) = \mathbf{i}_1$, exactly with $M = N+1$ microphones or by the **minimum-norm solution** with $M > N+1$ to improve [[concepts/white-noise-gain|WNG]].

## Properties

- Designed beampatterns remain **frequency invariant** across the band (the defining DMA property is preserved under steering).
- DF and WNG vary with $\theta_s$; DF is maximized at endfire, which is why most LDMA literature fixes $\theta_s = 0°$.
- Minimum-norm solutions with extra microphones raise WNG but can introduce extra high-frequency nulls, so the effective order may exceed the specified order at high frequencies.
- Validated experimentally with an 8-microphone (1.1 cm spacing) prototype in an anechoic chamber: measured steered patterns match the designs.

## Neural Counterpart

The steerability limits above apply to **any classical beamforming method** — but not to learned beamformers: the [[concepts/neural-differential-beamformer|neural differential beamformer (NDBF)]] (Huang & Habets 2026) realizes steerable 1st- and 3rd-order patterns with a dual-omni linear array over the full 0°–180° semicircle, a geometry in which classical designs are first-order-only and provably non-steerable. NDBF replaces the null-position conditions with training-data supervision and a steering-direction conditioning input.

## Related Concepts

- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/frequency-invariant-beamforming|Frequency-Invariant Beamforming]]
- [[concepts/beamforming|Beamforming]]

## Related Sources

- [[sources/jin-2021-steering-study-ldma|Jin, Huang, Wang, Chen, Benesty & Cohen 2021: Steering Study of Linear Differential Microphone Arrays]] — the introducing paper (proofs, conditions, design method, experiments)
- [[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020: Microphone Array Beamforming Methods for Speech Communication and Interaction]] — surveys the endfire limitation that this paper resolves
- [[sources/huang-2025-steerable-neural-directional-filtering|Huang et al. 2025: Steerable Neural Directional Filtering]] — neural counterpart: steering a learned directivity pattern by conditioning rather than null constraints
- [[sources/huang-2026-dual-mic-steerable-neural-beamformer|Huang & Habets 2026: Dual-Microphone Steerable High-Order Neural Differential Beamformer]] — neural steerability attained in the geometry where classical steerability is provably impossible (two omni mics)
