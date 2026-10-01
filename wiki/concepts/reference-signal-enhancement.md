---
type: concept
created: 2026-10-01
updated: 2026-10-01
sources:
  - raw/papers/rao-2026-keep-speech-anc/full-text.txt
tags:
  - active-noise-control
  - speech-enhancement
  - deep-learning
  - causality
  - speech-preserving-anc
---

# Reference Signal Enhancement

**Reference Signal Enhancement (RSE)** is a placement strategy for neural networks in feedforward [[active-noise-control|Active Noise Control]]: instead of replacing the control filter with a DNN (as DeepANC does), a neural network is placed **on the reference path** to transform the raw reference signal into a better one — e.g., suppressing its speech components so the downstream conventional FIR control filter cancels only noise. Because the enhancement network is fully causal (stride-1 convolution with causal padding) and the control filter remains a standard FIR, the approach introduces **no additional algorithmic delay** and preserves a large [[causality|causality margin]] — in contrast to frame-based CRN controllers, whose latency violates the causality constraints of headphone ANC.

## Key Formulations

Introduced by [[sources/rao-2026-keep-speech-anc|Rao et al. 2026]] for keep-speech ANC: the reference microphone captures noise plus speech, $x_v(n) = x(n) + v_r(n)$, and the RSE network $g_\phi$ produces a noise-only enhanced reference

$$\hat{x} = g_\phi(x_v, \hat{d}_v),$$

taking the original reference and the secondary-path-compensated error signal $\hat{d}_v(n) = e(n) - \hat{s} \ast u(n)$ as inputs. The enhanced reference then drives the (RLS-adapted) FIR control filter exactly as in conventional feedforward ANC.

Two training strategies, with opposite alignment properties:

- **Error-domain loss** $\mathcal{L}_{\mathrm{enh}} = E[d(n) + s \ast w \ast g_\phi(x + v_r, d + v_e)]^2$ — the Wiener-optimal control filter is substituted during training, so the network is optimized against the closed-loop error; jointly encodes noise suppression and speech preservation.
- **Reference-domain loss** $\mathcal{L}_{\mathrm{refsep}} = E[x(n) - g_\phi(x + v_r, d + v_e)]^2$ — plain noise-extraction MSE at the reference microphone.

Empirically (Rao et al. 2026), the reference-domain loss yields *higher* coherence between the enhanced reference and the primary noise, but the error-domain loss delivers better STOI/DNSMOS — reference-side fidelity does not automatically translate to perceptual gains, because the downstream ANC objective is joint noise attenuation + speech preservation.

## Significance

- **Causality by construction**: the NN never sits inside the cancellation loop's critical delay path; the FIR filter's delay budget is unchanged.
- **Division of labor**: the DNN does what linear filters cannot (distinguish speech from noise in the reference), while the FIR filter does what it does best (stable, adaptive cancellation).
- Related placements of neural networks in ANC include selective fixed-filter control ([[sources/bai-2026-feedback-guided-anc|SFANC/GFANC family]]) and neural control-filter generation (DeepANC, DP-ANC); RSE keeps the conventional controller untouched.

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/causality|Causality in ANC]]
- [[concepts/speech-preserving-anc|Speech-Preserving ANC]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — the frame-based alternative whose latency motivates RSE

## Related Sources

- [[sources/rao-2026-keep-speech-anc|Rao, Rong, Sun, He, Chen, Zou & Lu 2026: Causal Reference-Enhanced Keep-Speech Active Noise Control]] — introduces the method
