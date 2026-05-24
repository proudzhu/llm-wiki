---
type: concept
created: 2026-05-24
updated: 2026-05-24
tags:
  - beamforming
  - speech-recognition
  - microphone-array
---

# NLCMV Beamforming

**NLCMV** (Non-Linearly Constrained Minimum Variance) is a beamforming criterion proposed by Lin et al. (ICASSP 2024) that extends [[concepts/mvdr-beamformer|MVDR]] by incorporating white noise gain (WNG) control and explicit null direction constraints into the optimization.

## Formulation

The NLCMV beamformer minimizes the output power subject to a linear equality constraint (target-preserving) and a nonlinear inequality constraint (WNG):

$$\mathbf{h}^{H}(j\omega)\left[\mathbf{\Phi}_{dd}(j\omega) + \phi_{pp}(w)\sum_{n=1}^{N}\alpha_{p,n}\cdot\mathbf{g}_{n}(j\omega)\mathbf{g}_{n}^{H}(j\omega)\right]\mathbf{h}(j\omega)$$

subject to:
$$\mathbf{h}^{H}{(j\omega)}\mathbf{g}{(j\omega)} = 1$$
$$c(w) \triangleq \mathbf{h}^{H}({j\omega})\mathbf{\Psi}(j\omega)\mathbf{h}(j\omega) \leq 0$$

where $\mathbf{\Phi}_{dd}$ is the diffuse noise covariance, $\phi_{pp}(w)$ is the point noise PSD, $\alpha_{p,n}$ weights the $n$th point noise source, and $\mathbf{\Psi}(j\omega)$ encodes the WNG constraint:

$$\mathbf{\Psi}(j\omega) \triangleq \textbf{I} - \mathbf{g}(j\omega)\mathbf{g}^{H}(j\omega) \cdot M / [\sum_{m=1}^{M}|G_{m}(j\omega)|^2]$$

## Key Differences from MVDR

| Aspect | MVDR | NLCMV |
|--------|------|-------|
| WNG control | No explicit control | Non-linear inequality constraint |
| Null directions | Not specified | Soft control via weighted point noise terms |
| Formulation | Linear constraint | Linear equality + nonlinear inequality |

## Performance

NLCMV achieves ~10 dB gain at the designated look direction compared to super-directive beamforming, and ~0.7% absolute WER improvement in real ASR tests.

## Related Concepts

- [[concepts/beamforming|Beamforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/fixed-beamformer|Fixed Beamformer]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/white-noise-gain|White Noise Gain (WNG)]]

## Related Sources

- [[sources/lin-2024-agadir-array-geometry-agnostic-speech-recognition|Lin et al. 2024: AGADIR — Towards Array-Geometry Agnostic Directional Speech Recognition]]
