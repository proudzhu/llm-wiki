---
type: concept
created: 2026-04-29
updated: 2026-09-02
sources:
  - raw/papers/benslimane-2026-tango-quantized-distributed/full-text.md
  - raw/papers/jin-2017-multichannel-noise-reduction-mobile/full-text.md
  - raw/papers/bagheri-2019-pmwf-spp/full-text.md
  - raw/papers/yan-2014-dual-mic-bt-noise-reduction/full-text.md
  - raw/papers/braun-2015-residual-noise-control/full-text.md
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

## Speech-Distortion-Constrained Generalization

The SDW-MWF is itself a special case ($\beta = \mu = 1$) of the speech-distortion-constrained optimal filter $h = [\Phi_x + \beta \Phi_n]^{-1} \Phi_x i_1$ (Chen; Souden & Benesty), obtained by minimizing residual noise energy subject to a bound on speech-distortion energy. [[sources/yan-2014-dual-mic-bt-noise-reduction|Yan et al. 2014]] use this framework to unify the dual-microphone algorithm space: coherence-function filters and GSC variants occupy different points on the same $\beta$ trade-off curve, and GSC blocking-matrix mismatch is equivalent to operating at $\beta = 1$. See [[concepts/speech-distortion-constrained-noise-reduction|Speech-Distortion-Constrained Noise Reduction]].

## Residual Noise Control (RNC-MWF)

[[sources/braun-2015-residual-noise-control|Braun, Kowalczyk & Habets 2015]] redefine the MWF/PMWF target as *speech plus a fraction $c$ of the noise* and obtain $\mathbf{h}_Z = (1-c)\,\mathbf{h}_X + c\,\mathbf{e}_1$ — a weighted sum of the (standard parametric) MWF and the reference microphone that directly caps the maximum noise reduction at $c$ and bounds the speech distortion at $(1-c)^2$. Because no decomposition into spatial filter + gain-limited spectral gain is needed, the control remains valid for higher-rank speech PSD matrices (reverberant scenes). A noise-adaptive $c$ further keeps the output noise power constant in slowly time-varying noise fields. The mechanism survives today as the inference-time NAL knob of DNN suppressors ([[concepts/noise-attenuation-control|Noise Attenuation Control]]); see [[concepts/parametric-multi-channel-wiener-filter|PMWF]] for the full formulation.

## Differentiable SDW-MWF for End-to-End Training

The closed-form SDW-MWF $h = (\Phi_x + \mu \Phi_n)^{-1} \Phi_x i_1$ is differentiable (matrix inversion is smooth as long as $\Phi_x + \mu \Phi_n$ is well-conditioned), so it can be included in the training loop of a hybrid neural-spatial SE system. [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026]] use this property to train [[concepts/mn-tango|MN-TANGO]] end-to-end: gradients from an enhanced-STFT loss flow through the differentiable SDW-MWF back to the neural mask estimators. At inference, the [[concepts/gevd-spatial-filtering|GEVD-based]] rank-constrained SDW-MWF is used instead, which is non-differentiable but more robust to SCM estimation noise. The train-test mismatch is intentional: SDW-MWF acts as an optimization surrogate, while GEVD remains preferable at deployment.

## MVDR + Single-Channel Wiener Factorization

Simmer et al. [14] showed that the broadband MMSE-optimal multi-channel NR can be factored as a single-channel Wiener filter applied to the output of an [[concepts/mvdr-beamformer|MVDR beamformer]]. Jin et al. (2017) adopt this factorization for hands-free mobile-phone voice communication: the MVDR provides the distortionless spatial filter, and a single-channel Wiener post-filter (driven by the [[concepts/adaptive-coherence-noise-estimation|adaptive coherence noise estimator]]) applies the spectral gain. The contribution of Jin et al. lives entirely in the noise PSD estimate that feeds the Wiener gain — the MWF structure itself is the classical rank-1 case. This factorization is computationally lighter than a full MWF and decouples spatial filtering (MVDR) from noise PSD estimation (post-filter), which is attractive for real-time mobile-phone implementations.

## Parametric MWF (PMWF)

The MWF is one endpoint of a parameterized family: the [[concepts/parametric-multi-channel-wiener-filter|PMWF]] (Souden, Benesty & Affes 2010) derives from a constrained optimization (maximize noise reduction subject to a distortion bound) with trade-off parameter $\beta$, where $\beta = 1$ recovers the conventional MWF and $\beta = 0$ the MVDR. [[sources/bagheri-2019-pmwf-spp|Bagheri & Giacobello 2019]] show a practical implementation in which the [[concepts/multi-channel-speech-presence-probability|MC-SPP]] controls $\beta$ per time-frequency bin, updates the noise PSD matrix by SPP-weighted recursive averaging (with a Woodbury rank-1 update of its inverse), and blends the output with a $G_{\min}$-floored reference channel — improving ΔSINR, ΔSegSNR, and noise reduction over both MVDR and the fixed-$\beta$ MWF at nearly unchanged speech distortion.

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
- [[concepts/parametric-multi-channel-wiener-filter|Parametric Multi-Channel Wiener Filter (PMWF)]] — parameterized family with the MWF as the $\beta = 1$ endpoint
- [[concepts/multi-channel-speech-presence-probability|Multi-Channel Speech Presence Probability (MC-SPP)]]
- [[concepts/noise-attenuation-control|Noise Attenuation Control]]

## Related Sources

- [[sources/oviste-2026-neural-vslf-speech-enhancement|Oviste 2026: Neural VSLF for Speech Enhancement]]
- [[sources/liu-2026-scm-reconstruction-speech-enhancement|Liu 2026: SCM Reconstruction for Speech Enhancement]]
- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
- [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026: Quantized TANGO / MN-TANGO]]
- [[sources/jin-2017-multichannel-noise-reduction-mobile|Jin, Taghizadeh, Chen & Xiao 2017: Multi-channel Noise Reduction for Hands-free Voice Communication on Mobile Phones]] — adopts the MVDR + single-channel Wiener factorization (Simmer et al.) with an adaptive coherence noise PSD estimate driving the post-filter
- [[sources/bagheri-2019-pmwf-spp|Bagheri & Giacobello 2019: Exploiting MC-SPP in Parametric Multi-Channel Wiener Filter]] — MC-SPP-controlled PMWF with direct inverse noise PSD updates
- [[sources/braun-2015-residual-noise-control|Braun, Kowalczyk & Habets 2015: Residual Noise Control PMWF]] — target-signal redefinition yielding direct control of maximum noise reduction
