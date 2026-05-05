---
type: concept
created: 2026-04-30
updated: 2026-04-30
sources:
  - raw/papers/liu-2026-scm-reconstruction-speech-enhancement/paper.pdf
tags:
  - spatial-covariance-matrix
  - adaptive-algorithm
  - speech-enhancement
  - constrained-optimization
---

# Variance Ratio Estimation

**Variance Ratio Estimation** is a technique for decomposing the normalized spatial covariance matrix (SCM) of microphone array observations into a linear combination of predefined coherence matrices, where the combination weights (variance ratios) reflect the relative contribution of each acoustic component.

## Definition

Given the normalized observation SCM $\Gamma_y(n)$, it is decomposed as:

$$\Gamma_y(n) = \sum_{i=1}^{I} \psi_i(n) \Gamma_i(n) + \psi_R(n) \Gamma_d + \psi_V(n) I_M$$

The **variance ratios** are defined as:

$$\psi_i(n) = \frac{\phi_i(n)}{\phi_Y(n)}, \quad \psi_R(n) = \frac{\phi_R(n)}{\phi_Y(n)}, \quad \psi_V(n) = \frac{\phi_V(n)}{\phi_Y(n)}$$

where $\phi_i, \phi_R, \phi_V$ are the variances of source $i$, late reverberation, and noise at the reference microphone, and $\phi_Y$ is the total observation variance.

## Constraints

- **Non-negativity**: $\psi_i \geq 0, \psi_R \geq 0, \psi_V \geq 0$
- **Unity sum**: $\sum_{i=1}^{I}\psi_i + \psi_R + \psi_V = 1$

These constraints arise naturally from the normalization by trace.

## Estimation via Constrained Optimization

The variance ratios are estimated by minimizing the Frobenius norm between the modeled and observed normalized SCMs:

$$\min_{\psi} \left\| \Gamma_y - \sum_{i=1}^{I}\psi_i \Gamma_i - \psi_R \Gamma_d - \psi_V I_M \right\|_F^2 \quad \text{s.t.} \quad \psi \geq 0, \|\psi\|_1 = 1$$

## Multiplicative Update Algorithm

Liu et al. (2026) introduce a KL-divergence-regularized adaptive algorithm with multiplicative update:

$$h(n) = \frac{h(n-1) \circ r(n)}{h^T(n-1) r(n)}$$

where $r(n) = \exp\{\eta \Re[\Upsilon^H(n)\varepsilon(n)]\}$ is the multiplicative vector, $\eta$ is the step size, and $\varepsilon(n)$ is the posterior error.

### Properties

- **Non-negativity guaranteed**: Multiplicative update with positive $r(n)$ ensures $h(n) \geq 0$
- **Unity sum enforced**: Normalization by $h^T(n-1)r(n)$ ensures $\|h(n)\|_1 = 1$
- **KL divergence regularization**: Controls update step size for smooth tracking
- **Low complexity**: $\mathcal{O}(M^2(I+2))$ per time-frequency bin

## Relationship to Other Approaches

| Approach | Method | Complexity | Online? |
|----------|--------|------------|---------|
| DNN-based SCM prediction | Neural network predicts SCM directly | High (model-dependent) | Typically offline |
| Mask-based SCM estimation | T-F masks weighted averaging | Medium | Semi-online |
| Directional-gain methods | Fixed beamformer outputs | Low | Online |
| **Variance ratio estimation** | Constrained optimization + multiplicative update | **Low** $\mathcal{O}(M^2(I+2))$ | **Online** |

## Related Concepts

- [[../concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[../concepts/spatial-coherence|Spatial Coherence]]
- [[../concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[../concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[../concepts/adaptive-filtering|Adaptive Filtering]]

## Related Sources

- [[../sources/liu-2026-scm-reconstruction-speech-enhancement|Liu 2026: SCM Reconstruction for Speech Enhancement]]
