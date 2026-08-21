---
type: concept
created: 2026-05-24
updated: 2026-08-22
sources:
  - raw/papers/lin-2024-agadir-array-geometry-agnostic-speech-recognition/full-text.md
  - raw/papers/yang-2025-mc-differential-asr-smart-glasses/full-text.md
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

## WSR vs. Conversational Directional ASR

Yang et al. (2025) compared NLCMV (multi-direction, for conversational ASR where both wearer and bystander must be transcribed) with an internal adjusted MVDR steered solely at the wearer's mouth for [[concepts/wearer-speech-recognition|WSR]]. For pure WSR, the single-direction MVDR is more suitable than NLCMV because NLCMV's null-direction control and multiple steering directions add complexity without benefit when only the wearer is being transcribed. The paper's [[concepts/differential-asr|differential ASR]] framework then layers additional frontends (microphone selection, side-talk detection embedding) on top of the MVDR output to recover the side-talk robustness that NLCMV's spatial filtering alone cannot provide. This suggests NLCMV and MVDR+differential-frontends occupy different niches: NLCMV for multi-talker conversational ASR, MVDR+differential for single-talker WSR.

## Related Concepts

- [[concepts/beamforming|Beamforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/fixed-beamformer|Fixed Beamformer]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/white-noise-gain|White Noise Gain (WNG)]]
- [[concepts/differential-asr|Differential ASR]]
- [[concepts/wearer-speech-recognition|Wearer Speech Recognition (WSR)]]

## Related Sources

- [[sources/lin-2024-agadir-array-geometry-agnostic-speech-recognition|Lin et al. 2024: AGADIR — Towards Array-Geometry Agnostic Directional Speech Recognition]]
- [[sources/yang-2025-mc-differential-asr-smart-glasses|Yang et al. 2025: Multi-Channel Differential ASR for Smart Glasses]] — contrasts NLCMV (multi-direction) with adjusted MVDR (wearer-only) for WSR
