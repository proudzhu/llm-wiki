---
type: concept
created: 2026-09-24
updated: 2026-09-24
sources:
  - raw/papers/desena-2012-higher-order-differential/full-text.md
tags:
  - directivity-pattern
  - beamforming
  - differential-microphone-array
  - spatial-audio
---

# Sector-Based Directivity Design

**Sector-based directivity design** is the framework introduced by [[sources/desena-2012-higher-order-differential|De Sena, Hacihabiboglu & Cvetkovic 2012]] for designing the directivity pattern of an $N$-th order microphone (or any device whose pattern is a trigonometric polynomial) by minimizing a cost function controlled by two physically meaningful parameters: the angular width $\alpha$ of a frontal sector of interest and a convex combination factor $\lambda$.

## Key Formulations

Writing the frequency-independent $N$-th order pattern as $\Gamma_{\mathbf{a}}(\theta) = 1 - \sum_i a_i + \sum_i a_i \cos^i\theta$ (normalized to unit gain at $\theta = 0$), the optimal coefficients minimize

$$
\Phi_{\mathbf{a}} (\alpha, \lambda) = \lambda \underbrace{\frac{\int_{\alpha}^{\pi} |\Gamma_{\mathbf{a}} (\theta)|^2 d\theta}{\int_{0}^{\alpha} |\Gamma_{\mathbf{a}} (\theta)|^2 d\theta}}_{\text{out-of-sector / in-sector energy}} + (1 - \lambda) \underbrace{\int_{0}^{\alpha} |\Gamma_{\mathbf{a}}' (\theta)|^2 d\theta}_{\text{in-sector non-uniformity}}
$$

- $\alpha \in [0, \pi]$ sets where the sources of interest are (e.g., $\alpha = \pi/2$ for a frontal plane / orchestra);
- $\lambda \in [0, 1]$ trades rejection of out-of-sector sources against flat pickup within the sector.

A spherically isotropic variant inserts a $\sin(\theta)$ weight in every integral. An alternative cost (absolute leakage + deviation-from-unity) was rejected because its solutions exhibit undesirable ripples. Optimization is cheap (Nelder–Mead converges in <0.1 s up to fourth order), enabling real-time pattern adaptation.

## Standard Patterns as Special Cases

| Pattern | $(\lambda, \alpha)$ | Interpretation |
|---|---|---|
| Omnidirectional | $(0, \pi)$ | Pure uniformity term → constant pattern |
| Supercardioid | $(1, \pi/2)$ | Inverse front–back ratio → max-FBR pattern |
| Hypercardioid | $(1, \alpha \to 0)$ | Total energy → max directivity factor |
| Subcardioid | $\approx (0.5008,\ 2.247\ \mathrm{rad})$ | Near-exact fit (error $\ll -100$ dB) |
| Cardioid (1st order) | $\approx (1,\ \pi)$ | Rejects $\theta = \pi$ while keeping sensitivity elsewhere |

Higher-order cardioid-A/B patterns fit with errors from $-43$ dB to $\ll -100$ dB, so the classical cardioid family is unified with the optimality-driven hypercardioid/supercardioid as points in one $(\alpha, \lambda)$ design space.

## Why It Matters

- **User-facing interface**: a recording engineer sets two physical parameters instead of $N$ polynomial coefficients.
- **Design-space coverage**: $(\alpha, \lambda)$ pairs between the standard points yield practically useful patterns (e.g., hypercardioid-like but wider, for multi-instrument pickup; $\alpha = \pi/2$ with reduced $\lambda$ for uniform frontal recording).
- **Adaptive/zoom applications**: teleconferencing (widen the pattern as source-position estimates degrade) and "acoustical zoom" synchronized with a camera's optical zoom.
- **Complex-root region**: for many $(\alpha, \lambda)$ pairs the optimal polynomial has complex-conjugate roots, which conventional cascaded [[concepts/differential-microphone-array|differential microphone arrays]] cannot implement — the motivation for the [[concepts/complex-root-differential-array|complex-root differential array]] structure proposed in the same paper.

The framework applies to any microphone whose pattern is a trigonometric polynomial (equivalently, a weighted sum of spherical harmonics of degree 0), including differential-integral arrays and spherical arrays such as the Eigenmike.

## Related Concepts

- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/complex-root-differential-array|Complex-Root Differential Array]]
- [[concepts/superdirective-beamforming|Superdirective Beamforming]] — hypercardioid (max DF) as the $\lambda \to 1, \alpha \to 0$ corner
- [[concepts/frequency-invariant-beamforming|Frequency-Invariant Beamforming]]

## Related Sources

- [[sources/desena-2012-higher-order-differential|De Sena, Hacihabiboglu & Cvetkovic 2012: On the Design and Implementation of Higher Order Differential Microphones]] — introduces the framework
