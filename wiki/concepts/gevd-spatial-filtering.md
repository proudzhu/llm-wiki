---
type: concept
created: 2026-07-16
updated: 2026-07-16
sources:
  - raw/papers/benslimane-2026-tango-quantized-distributed/full-text.md
tags:
  - speech-enhancement
  - spatial-filtering
  - multi-channel
  - beamforming
  - wiener-filter
  - gevd
---

# GEVD-Based Spatial Filtering

**GEVD-based spatial filtering** is a rank-constrained formulation of the [[concepts/multi-channel-wiener-filter|Speech Distortion Weighted Multichannel Wiener Filter (SDW-MWF)]] in which the speech and noise [[concepts/spatial-covariance-matrix|spatial covariance matrices (SCMs)]] are decomposed via a Generalized EigenValue Decomposition (GEVD). It is the inference-time spatial filter used in the [[concepts/tango-framework|Tango]] family of distributed binaural speech enhancement frameworks.

## Formulation

Given noisy multichannel observations $y = x + n$, the SDW-MWF computes the optimal linear filter that minimizes a weighted combination of residual noise and speech distortion:

$$h_{\mathrm{SDW\text{-}MWF}} = \left( \Phi_x + \mu \Phi_n \right)^{-1} \Phi_x \, i_1$$

where $\Phi_x$ and $\Phi_n$ are the speech and noise SCMs, $\mu$ is a trade-off parameter ($\mu = 1$ in Tango), and $i_1$ is a selection vector picking the reference microphone.

The **GEVD-based** implementation computes the joint diagonalization of $(\Phi_x, \Phi_n)$:

$$\Phi_x = U \Lambda_x U^{\mathsf{H}}, \qquad \Phi_n = U \Lambda_n U^{\mathsf{H}}$$

where $U$ is the matrix of generalized eigenvectors and $\Lambda_x$, $\Lambda_n$ are diagonal matrices of generalized eigenvalues. The relative speech-to-noise power per eigenvector is $\rho_k = \lambda_{x,k} / \lambda_{n,k}$. Truncating the eigenvector basis to the $r$ dominant components (where $\rho_k$ is largest) yields a **low-rank** approximation of the speech SCM, which:

- Improves robustness against SCM estimation noise (fewer parameters to estimate).
- Reduces computational cost of the matrix inversion.
- Is especially useful when the speech SCM is rank-deficient (e.g., a single directional source).

The rank-constrained SDW-MWF is the formulation used in Serizel et al. (2014) and is the **inference-time spatial filter in TANGO, RT-Tango, and MN-TANGO**.

## Use in TANGO-Family Frameworks

In the [[concepts/tango-framework|Tango]] two-stage architecture and its variants, the GEVD-based SDW-MWF appears twice:

1. After the SN-DNN stage, producing the ear-specific compressed signal exchanged between ear-nodes.
2. After the MN-DNN stage, producing the final enhanced binaural output.

In [[concepts/mn-tango|MN-TANGO]], only the second occurrence is retained. The masks estimated by the neural mask estimators are used to compute the speech and noise SCMs via time-frequency-averaged outer products of the observed STFT bins, from which the GEVD-based filter is derived.

## Differentiable Surrogate for Training

GEVD is non-differentiable (eigendecomposition has unstable gradients at repeated eigenvalues), so end-to-end training of TANGO-family models cannot propagate gradients through the GEVD filter directly. [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026]] address this by training with a **differentiable SDW-MWF** (the unconstrained closed-form $(\Phi_x + \mu \Phi_n)^{-1} \Phi_x i_1$) and switching to the GEVD-based implementation at inference. The train-test mismatch is intentional: the differentiable SDW-MWF acts as an optimization surrogate, while GEVD remains preferable at deployment for its robustness and low-rank noise rejection.

Empirically, SDW-MWF inference yields higher SI-SDR/SI-SAR but lower SI-SIR/STOI/PESQ than GEVD inference — validating the choice of GEVD for deployment.

## Robustness to Mask Errors

A central finding of [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026]] is that the GEVD-based spatial filter is **highly robust to errors in the neural mask estimates**, including those introduced by INT8 [[concepts/quantization-aware-training|quantization]]. Although W8A8 quantization noticeably degrades the intermediate MN-DNN mask output, the final GEVD-filtered output is within 0.1–0.6 dB of the FP32 baseline. This robustness is what enables aggressive compression of the neural component without sacrificing final enhancement quality.

## Related Concepts

- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/tango-framework|Tango Framework]]
- [[concepts/mn-tango|MN-TANGO]]
- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026: Quantized TANGO / MN-TANGO]]
- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
