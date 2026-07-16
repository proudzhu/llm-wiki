---
type: concept
created: 2026-04-29
updated: 2026-07-16
sources:
  - raw/papers/benslimane-2026-tango-quantized-distributed/full-text.md
tags:
  - speech-enhancement
  - wiener-filter
  - multi-channel
---

# Multi-Channel Wiener Filter

The **Multi-Channel Wiener Filter (MWF)** is the optimal linear filter that minimizes the mean square error between the estimated and desired speech signal across multiple microphone channels.

## Formulation

Given noisy observation $y = x + n$, the MWF weights are:

$$h_{\text{MWF}} = \Phi_y^{-1} \Phi_x i_1 = (\Phi_x + \Phi_n)^{-1} \Phi_x i_1$$

where $\Phi_x$ is the clean-speech spatial covariance matrix and $\Phi_n$ is the noise spatial covariance matrix.

## Relationship to VSLF

The MWF is a special case of the [[concepts/variable-span-linear-filter|Variable Span Linear Filter]] with $\mu=1$ and $Q=M$ (full span).

## SCM Reconstruction-Based MWF (R-MWF)

Liu et al. (2026) propose using reconstructed SCMs in the MWF:

$$h_{W,1}(n) = \psi_1(n) \Gamma_y^{-1}(n) \Gamma_1(n) u$$

where $\Gamma_y(n)$ is the normalized observation SCM reconstructed from variance ratios and predefined coherence matrices. This approach avoids direct SCM estimation and instead estimates the variance ratios via a lightweight multiplicative update, enabling online operation with $\mathcal{O}(M^2(I+2))$ complexity.

## Speech Distortion Weighted MWF (SDW-MWF)

The **Speech Distortion Weighted Multichannel Wiener Filter (SDW-MWF)** is an MWF variant that introduces a parameter $\mu$ controlling the trade-off between noise reduction and speech distortion. It is widely used in binaural hearing aids and distributed [[concepts/distributed-binaural-speech-enhancement|distributed binaural speech enhancement]] frameworks (e.g., the [[concepts/tango-framework|Tango]] / [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|RT-Tango]] two-stage architecture), where it produces the ear-specific compressed signal exchanged between ear-nodes. The SDW-MWF requires [[concepts/spatial-covariance-matrix|spatial covariance matrices (SCM)]] for both speech and noise, which in real-time streaming variants (RT-Tango-OS) are estimated online via a recursive exponential moving average with forgetting factor $\alpha$.

## Differentiable SDW-MWF for End-to-End Training

The closed-form SDW-MWF $h = (\Phi_x + \mu \Phi_n)^{-1} \Phi_x i_1$ is differentiable (matrix inversion is smooth as long as $\Phi_x + \mu \Phi_n$ is well-conditioned), so it can be included in the training loop of a hybrid neural-spatial SE system. [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026]] use this property to train [[concepts/mn-tango|MN-TANGO]] end-to-end: gradients from an enhanced-STFT loss flow through the differentiable SDW-MWF back to the neural mask estimators. At inference, the [[concepts/gevd-spatial-filtering|GEVD-based]] rank-constrained SDW-MWF is used instead, which is non-differentiable but more robust to SCM estimation noise. The train-test mismatch is intentional: SDW-MWF acts as an optimization surrogate, while GEVD remains preferable at deployment.

## Related Concepts

- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/variable-span-linear-filter|Variable Span Linear Filter]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/tango-framework|Tango Framework]]
- [[concepts/gevd-spatial-filtering|GEVD-Based Spatial Filtering]]
- [[concepts/mn-tango|MN-TANGO]]

## Related Sources

- [[sources/oviste-2026-neural-vslf-speech-enhancement|Oviste 2026: Neural VSLF for Speech Enhancement]]
- [[sources/liu-2026-scm-reconstruction-speech-enhancement|Liu 2026: SCM Reconstruction for Speech Enhancement]]
- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
- [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026: Quantized TANGO / MN-TANGO]]
