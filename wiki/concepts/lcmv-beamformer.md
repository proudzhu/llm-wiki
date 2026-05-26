---
type: concept
created: 2026-05-26
updated: 2026-05-26
tags:
  - beamforming
  - spatial-filtering
  - constrained-optimization
---

# Linearly Constrained Minimum Variance (LCMV) Beamformer

The **Linearly Constrained Minimum Variance (LCMV)** beamformer is a general spatial filtering framework that minimizes output power subject to multiple linear constraints on the beamformer weights. It extends the [[concepts/mvdr-beamformer|MVDR beamformer]] (which enforces a single distortionless constraint) to simultaneously control the spatial response at multiple directions, enabling explicit null steering and multiple-target preservation.

## Formulation

Given $M$ microphones and $C$ linear constraints, the LCMV problem is:

$$
\min_{\mathbf{w}(k)} \mathbf{w}^{\mathrm{H}}(k) \hat{\mathbf{\Phi}}_{\mathbf{nn}}(k) \mathbf{w}(k) \quad \text{subject to} \quad \mathbf{C}^{\mathrm{H}}(k) \mathbf{w}(k) = \mathbf{g}
$$

where $\mathbf{C}(k) \in \mathbb{C}^{M \times C}$ is the constraint matrix whose columns are the spatial signatures (RTFs or steering vectors) of the controlled directions, $\hat{\mathbf{\Phi}}_{\mathbf{nn}}(k)$ is the noise covariance matrix, and $\mathbf{g} \in \mathbb{C}^{C}$ is the desired response vector (typically 1 for target, 0 for null directions).

## Optimal Solution

The closed-form solution is:

$$
\mathbf{w}_{\mathrm{LCMV}}(k) = \hat{\mathbf{\Phi}}_{\mathbf{nn}}^{-1}(k) \mathbf{C}(k) \left( \mathbf{C}^{\mathrm{H}}(k) \hat{\mathbf{\Phi}}_{\mathbf{nn}}^{-1}(k) \mathbf{C}(k) \right)^{-1} \mathbf{g}
$$

This formulation achieves:
- **Distortionless response**: Enforces $\mathbf{w}^{\mathrm{H}}(k)\mathbf{a}_{\mathrm{target}}(k)=1$ for the target speaker
- **Null steering**: Enforces $\mathbf{w}^{\mathrm{H}}(k)\mathbf{a}_{\mathrm{interf}}(k)=0$ for interfering speakers
- **Noise minimization**: Minimizes residual noise power subject to these constraints

## Relationship to MVDR

The MVDR beamformer is a special case of LCMV with a single constraint ($C=1$): preserving the target direction while minimizing total output power. LCMV generalizes this to multiple simultaneous constraints.

## Relationship to GSC

The [[concepts/gsc-beamformer|Generalized Sidelobe Canceller (GSC)]] is an efficient implementation of the LCMV beamformer that decomposes the weight vector into:
1. A **fixed quiescent beamformer** satisfying the constraints
2. An **adaptive interference-cancellation path** operating in the null space of the constraints

## Modern Extensions

The LCMV framework has been extended in several directions:
- **DNN-based LCMV**: Learning beamforming weights that satisfy linear constraints through penalty-based loss functions (Zaidel et al. 2026)
- **Combined LCMV-TRINICON**: Separating multiple speech sources in noisy and reverberant environments
- **Multi-speaker LCMV with postfilter**: Source separation and noise reduction

## Related Concepts

- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/gsc-beamformer|Generalized Sidelobe Canceller]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/relative-transfer-function|Relative Transfer Function (RTF)]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[sources/zaidel-2026-linearly-constrained-deep-beamformer|Zaidel et al. 2026: Linearly Constrained Deep Beamformer]]
