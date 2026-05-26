---
type: concept
created: 2026-05-26
updated: 2026-05-26
tags:
  - spatial-filtering
  - beamforming
  - acoustic-modeling
  - transfer-function
---

# Relative Transfer Function (RTF)

The **Relative Transfer Function (RTF)** describes the acoustic propagation from a source to each microphone relative to a reference microphone. Unlike the absolute transfer function (ATF), the RTF captures only the relative differences between channels, eliminating the common source excitation and making it directly useful for spatial filtering.

## Definition

For a source at direction $\theta$ with ATF $\mathbf{h}(k,\theta) \in \mathbb{C}^{M}$ across $M$ microphones, the RTF with respect to the reference microphone $r$ is:

$$
\mathbf{a}(k,\theta) = \frac{\mathbf{h}(k,\theta)}{h_r(k,\theta)}
$$

where $h_r(k,\theta)$ is the ATF at the reference microphone. The RTF is normalized so that the $r$-th entry equals 1.

## Estimation via Covariance Whitening

The covariance whitening (CW) method is a popular approach for RTF estimation. Given noise-only frames $\mathcal{V}_n$:

$$
\hat{\mathbf{\Phi}}_{\mathbf{nn}}(k) = \frac{1}{|\mathcal{V}_n|} \sum_{l \in \mathcal{V}_n} \mathbf{y}(l,k) \mathbf{y}^{\mathrm{H}}(l,k)
$$

The whitened signal is:

$$
\mathbf{y_w}(l,k) = \hat{\mathbf{\Phi}}_{\mathbf{nn}}^{-1/2}(k) \mathbf{y}(l,k)
$$

For a set of target-only frames $\mathcal{V}_t$, the whitened covariance is:

$$
\hat{\mathbf{\Phi}}_{\mathbf{y_w y_w}}^{(\mathcal{V}_t)}(k) = \hat{\mathbf{\Phi}}_{\mathbf{nn}}^{-1/2}(k) \hat{\mathbf{\Phi}}_{\mathbf{yy}}^{(\mathcal{V}_t)}(k) (\hat{\mathbf{\Phi}}_{\mathbf{nn}}^{-1/2})^{\mathrm{H}}(k)
$$

The RTF is obtained from the dominant eigenvector $\hat{\bm{\psi}}^{(t)}$ of this whitened covariance:

$$
\hat{\mathbf{a}}^{(t)}(k) = \frac{ \hat{\mathbf{\Phi}}^{\mathrm{H}/2}_{\mathbf{nn}}(k) \hat{\bm{\psi}}^{(t)} }{ \mathbf{e}^{\top}_{\mathrm{ref}} \hat{\mathbf{\Phi}}^{\mathrm{H}/2}_{\mathbf{nn}}(k) \hat{\bm{\psi}}^{(t)} }
$$

where $\mathbf{e}_{\mathrm{ref}}$ is the selection vector for the reference microphone.

## Importance in Beamforming

The RTF captures both direct-path and reverberant propagation effects. RTF-based beamforming yields improved speech quality compared with approaches relying solely on direct-path (steering vector) models, particularly in reverberant environments.

## Related Concepts

- [[concepts/lcmv-beamformer|LCMV Beamformer]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/room-transfer-function|Room Transfer Function]]
- [[concepts/room-impulse-response|Room Impulse Response]]
- [[concepts/generalized-eigenvalue-decomposition|Generalized Eigenvalue Decomposition]]

## Related Sources

- [[sources/zaidel-2026-linearly-constrained-deep-beamformer|Zaidel et al. 2026: Linearly Constrained Deep Beamformer]]
