---
type: concept
created: 2026-09-30
updated: 2026-09-30
sources:
  - raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/full-text.md
tags:
  - beamforming
  - microphone-arrays
  - robust-beamforming
---

# Steering-Vector Error

**Category**: Array-model mismatch

## Definition

A **steering vector** $\mathbf{d}(\theta_0, \omega)$ encodes the assumed array response to a source at look direction $\theta_0$ — in the free-field, far-field model it is a vector of phase delays determined by microphone positions and geometry. **Steering-vector error** (or *steering-vector mismatch*) is the discrepancy between that assumed response and the true transfer function $\mathbf{a}(\theta, \omega)$ relating the source to the microphones:

$$\mathbf{e} = \mathbf{a}(\theta, \omega) - \mathbf{d}(\theta_0, \omega) \neq \mathbf{0}$$

Beamformers that treat the steering vector as exact — MPDR/[[concepts/mvdr-beamformer|MVDR]] with a sample covariance, and the plain Griffiths–Jim [[concepts/gsc-beamformer|GSC]] — degrade sharply when $\mathbf{e}$ is non-negligible, because the "distortionless" constraint is then satisfied in the wrong direction and the target is suppressed as if it were interference: [[concepts/target-signal-cancellation|target-signal cancellation]].

## Sources of Error

| Source | Notes |
|:-------|:------|
| **Target-direction error** | The dominant factor in real microphone arrays, because the talker moves and the exact DOA is unknowable. Hoshuyama et al. treat it as *the* design variable, quantifying robustness as a permissible angular error (up to 20° in their system). |
| **Microphone position error** | Fabrication and mounting tolerances perturb the geometric delays, especially for small apertures. |
| **Microphone sensitivity (gain/phase) error** | Uncalibrated microphones break the assumed per-channel response. |
| **Reverberation** | Multipath propagation makes the true transfer function frequency-selective and position-dependent, so no free-field steering vector is ever correct indoors. This is why [[concepts/relative-transfer-function|relative transfer functions (RTFs)]] replace steering vectors as the standard remedy. |
| **Near-field / geometry mismatch** | Sources closer than the far-field distance invalidate the plane-wave model. |

## Consequences

1. **In an adaptive beamformer**: the target is incompletely blocked, leaks into the adaptive reference path, and is then cancelled — audible as high-frequency attenuation and distortion.
2. **In a fixed beamformer**: the main lobe points slightly off target, and the distortionless constraint degrades into a passband ripple / attenuation.
3. **In the covariance-domain beamformers**: the weight norm can grow without bound as the assumed steering direction moves away from any real signal, collapsing the [[concepts/white-noise-gain|white noise gain]] and amplifying noise.

## Remedies

- **Robust constraints**: bound the adaptive filter so it cannot cancel the target. The [[concepts/coefficient-constrained-adaptive-filter|coefficient-constrained adaptive filter (CCAF)]] is the most explicit instance — its box region is derived by requiring target minimization only over an explicitly chosen direction-error sector, so the permissible error is a design parameter (Hoshuyama et al. 1999).
- **[[concepts/norm-constrained-adaptive-filter|Norm constraint]] / [[concepts/diagonal-loading|diagonal loading]] / WNG constraint**: indirect scalar bounds that limit how far the solution may depart from the nominal design.
- **Uncertainty-set formulations**: model the error explicitly and optimize the worst case, e.g. the [[concepts/ellipsoidal-uncertainty-modeling|ellipsoidal]] and [[concepts/convex-hull-uncertainty-model|convex-hull]] uncertainty models in [[concepts/robust-minimum-variance-beamforming|robust minimum variance beamforming]].
- **RTF-based steering**: estimate the true transfer function instead of assuming it ([[concepts/relative-transfer-function|RTF]], [[concepts/informed-gsc|informed GSC]]).
- **Target tracking / calibration**: adapt the look direction online — effective for large errors but mistracks burst signals and needs matrix products.
- **Output-based selection**: search a dictionary of candidate steering directions rather than committing to one ([[concepts/output-based-speech-enhancement|output-based speech enhancement]]).

## Related Concepts

- [[concepts/beamforming|Beamforming]]
- [[concepts/target-signal-cancellation|Target-Signal Cancellation]]
- [[concepts/gsc-beamformer|Generalized Sidelobe Canceller (GSC)]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]
- [[concepts/relative-transfer-function|Relative Transfer Function (RTF)]]
- [[concepts/robust-minimum-variance-beamforming|Robust Minimum Variance Beamforming]]
- [[concepts/ellipsoidal-uncertainty-modeling|Ellipsoidal Uncertainty Modeling]]
- [[concepts/convex-hull-uncertainty-model|Convex Hull Uncertainty Model]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/coefficient-constrained-adaptive-filter|Coefficient-Constrained Adaptive Filter (CCAF)]]
- [[concepts/diagonal-loading|Diagonal Loading]]

## Related Sources

- [[sources/hoshuyama-1999-robust-adaptive-beamformer-ccaf|Hoshuyama, Sugiyama & Hirano 1999: A Robust Adaptive Beamformer with a Blocking Matrix Using Constrained Adaptive Filters]] — enumerates the causes, argues target-direction error dominates, and converts the permissible error into an explicit design parameter
- [[sources/lorenz-2005-robust-minimum-variance-beamforming|Lorenz & Boyd 2005: Robust Minimum Variance Beamforming]] — uncertainty-set treatment of steering-vector and covariance error
- [[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020: Microphone Array Beamforming Methods for Speech Communication and Interaction]] — steering-vector/RTF estimation as the practical bottleneck of adaptive beamforming
- [[sources/apostolidis-2026-listen-first-output-based-multi-microphone|Apostolidis et al. 2026: Listen-First Output-Based Multi-Microphone Speech Enhancement]] — steering search as a remedy for RTF mismatch
- [[sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal et al. 2026: Adaptive Diagonal Loading for Norm Constrained Beamforming]]
- [[sources/yan-2014-dual-mic-bt-noise-reduction|Yan, Qiu & Lu 2014: Dual-Mic Noise Suppression for Bluetooth Headsets]] — pre-modeled RTF robust to wearing-angle mismatch
