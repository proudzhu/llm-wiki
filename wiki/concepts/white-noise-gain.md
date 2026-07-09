---
type: concept
created: 2026-05-07
updated: 2026-07-09
tags:
  - beamforming
  - robustness
  - microphone-arrays
sources:
  - raw/papers/deng-2026-joint-covariance-wng-mvdr/full-text.md
---

# White Noise Gain (WNG)

**Category**: Beamforming Robustness Metric

## Definition

The White Noise Gain (WNG) quantifies a beamformer's robustness to spatially uncorrelated (white) noise. It is defined as the ratio of output SNR to input SNR in a spatially white noise field:

$$W = \frac{|\mathbf{w}^H \mathbf{d}|^2}{\|\mathbf{w}\|^2} = \frac{1}{\|\mathbf{w}\|^2}$$

where the second equality holds under the distortionless constraint $\mathbf{w}^H \mathbf{d} = 1$.

## Interpretation

- **High WNG**: The beamformer is robust to uncorrelated sensor noise and array imperfections
- **Low WNG**: The weight vector norm $\|\mathbf{w}\|^2$ is large, indicating sensitivity to noise and potential target cancellation
- **Maximum WNG**: For an $M$-element array, the theoretical maximum is $10\log_{10}(M)$ dB (achieved by the delay-and-sum beamformer)

## WNG Collapse in Snapshot Deficiency

When the sample SCM is estimated from insufficient snapshots ($L < M$ or $L \approx M$):
1. The SCM becomes ill-conditioned
2. The weight vector norm $\|\mathbf{w}\|^2$ spikes
3. WNG plummets, causing severe target signal cancellation

## WNG-Constrained Beamforming (Mittal et al. 2026)

Mittal et al. (2026) propose enforcing a strict lower bound $W \geq W_{\min}$ via adaptive diagonal loading. Using the Kantorovich inequality, they derive:

$$\frac{W}{M} \geq \frac{4\kappa}{(\kappa+1)^2}$$

This maps the desired WNG bound to a maximum allowable condition number $\kappa_{\max}$, enabling principled loading parameter selection.

### Practical WNG Bound

A typical choice is $W_{\min} = 10\log_{10}(M) - 3$ dB, allowing 3 dB of WNG degradation from the delay-and-sum maximum in exchange for adaptive interference nulling.

## Data-Driven WNG Estimation

Conventionally, the WNG lower bound $W_{\min}$ is a fixed hyperparameter tuned manually (e.g., $10\log_{10}(M) - 3$ dB for all frequencies). Deng et al. (2026) introduce a **frequency-adaptive learnable WNG** scheme where a neural network predicts a per-frequency-bin WNG threshold $\mathcal{W}_0(k)$ jointly with T-F masks for [[concepts/spatial-covariance-matrix|SCM]] estimation. The WNG prediction is implicitly supervised via the beamforming reconstruction loss rather than requiring explicit WNG labels, enabling the network to discover optimal frequency-dependent robustness tradeoffs automatically. This approach outperforms fixed-threshold baselines by +1.4–1.8 dB SNR gain under both matched and mismatched array conditions.

## Related Concepts

- [[concepts/diagonal-loading|Diagonal Loading]]
- [[concepts/kantorovich-inequality|Kantorovich Inequality]]
- [[concepts/condition-number|Condition Number]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/robust-minimum-variance-beamforming|Robust Minimum Variance Beamforming]]
- [[concepts/neural-beamforming|Neural Beamforming]]

## Related Sources

- [[sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal et al. 2026: Adaptive Diagonal Loading for Norm Constrained Beamforming]]
- [[sources/deng-2026-joint-covariance-wng-mvdr|Deng et al. 2026: Joint Covariance and WNG Learning for Robust MVDR]]
