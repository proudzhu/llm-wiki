---
type: concept
created: 2026-05-07
updated: 2026-05-07
tags:
  - beamforming
  - adaptive-filtering
  - microphone-arrays
  - speech-enhancement
---

# MPDR Beamformer

**Category**: Adaptive Beamforming

## Definition

The Minimum Power Distortionless Response (MPDR) beamformer seeks a weight vector $\mathbf{w} \in \mathbb{C}^{M \times 1}$ that minimizes the total output power while maintaining a distortionless response in the target direction:

$$\min_{\mathbf{w}} \mathbf{w}^H \mathbf{R}_y \mathbf{w} \quad \text{s.t.} \quad \mathbf{w}^H \mathbf{d} = 1$$

where $\mathbf{R}_y = \mathbb{E}[\mathbf{y}\mathbf{y}^H]$ is the theoretical spatial correlation matrix and $\mathbf{d}$ is the steering vector (RTF) normalized such that $\mathbf{d}^H \mathbf{d} = M$.

## Optimal Solution

The closed-form optimal weight vector is:

$$\mathbf{w}_{opt} = \frac{\mathbf{R}_y^{-1} \mathbf{d}}{\mathbf{d}^H \mathbf{R}_y^{-1} \mathbf{d}}$$

## MPDR vs. MVDR

- **MPDR**: Minimizes total output power (target + interference + noise). More sensitive to steering vector mismatch and SCM estimation errors.
- **MVDR**: Minimizes interference-plus-noise power only. Requires knowledge of the noise-only SCM.

In practice, MPDR is more commonly used because estimating the noise-only SCM is difficult in dynamic environments.

## Robustness Challenges

1. **Snapshot deficiency**: When $L < M$, the sample SCM is rank-deficient, causing WNG collapse
2. **Array imperfections**: Sensor positioning errors, gain mismatches, phase perturbations
3. **Steering vector mismatch**: Errors in the assumed target direction

## Robust MPDR via Adaptive Diagonal Loading

Mittal et al. (2026) propose a WNG-constrained MPDR using adaptive diagonal loading:

$$\mathbf{Q}[i] = \hat{\mathbf{R}}_y[i] + \mu[i]\mathbf{I}$$

where $\mu[i]$ is computed at each frame to guarantee $W \geq W_{\min}$.

## Related Concepts

- [[mvdr-beamformer|MVDR Beamformer]]
- [[gsc-beamformer|Generalized Sidelobe Canceller]]
- [[diagonal-loading|Diagonal Loading]]
- [[white-noise-gain|White Noise Gain]]
- [[beamforming|Beamforming]]
- [[spatial-covariance-matrix|Spatial Covariance Matrix]]

## Related Sources

- [[../sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal et al. 2026: Adaptive Diagonal Loading for Norm Constrained Beamforming]]
