---
type: concept
created: 2026-04-29
updated: 2026-04-29
tags:
  - speech-enhancement
  - linear-filtering
  - optimal-filtering
---

# Variable Span Linear Filter

The **Variable Span Linear Filter (VSLF)** is a generalized linear filtering framework for multi-channel speech enhancement that provides controllable tradeoff between speech distortion and noise reduction.

## Formulation

Given clean-speech SCM $\Phi_x$ and overall-noise SCM $\Phi_n$, the VSLF performs joint diagonalization:

$$B^H \Phi_x B = \Lambda, \quad B^H \Phi_n B = I_M$$

The optimal VSLF weights are:

$$h_Q^{(\mu)} = B_{:Q} (\Lambda_{:Q} + \mu I_Q)^{-1} B_{:Q}^H \Phi_x i_1$$

where:
- $Q \in \{1, \ldots, M\}$ is the span dimension
- $\mu \geq 0$ controls speech distortion vs noise reduction tradeoff

## Special Cases

| Parameters | Result |
|:-----------|:-------|
| $\mu=1, Q=M$ | Multi-Channel Wiener Filter (MWF) |
| $\mu=0, Q=P$ (rank of $\Phi_x$) | MVDR beamformer |

## Hybrid VSLF (HVSF)

The HVSF architecture uses a DNN to estimate $\Phi_x$, $\Phi_n$, and $\mu$ from noisy spectrogram, then computes VSLF weights via GEVD. This provides:
- Interpretability of estimated rank
- Explicit control over distortion-noise tradeoff
- Generalization beyond MWF/MVDR

## Related Concepts

- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/generalized-eigenvalue-decomposition|Generalized Eigenvalue Decomposition]]

## Related Sources

- [[sources/oviste-2026-neural-vslf-speech-enhancement|Oviste 2026: Neural VSLF for Speech Enhancement]]
