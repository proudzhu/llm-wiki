---
type: concept
created: 2026-08-16
updated: 2026-09-13
sources:
  - raw/papers/souden-2011-online-noise-tracking/full-text.md
  - raw/papers/taseska-2018-informed-spatial-filters/full-text.md
  - raw/papers/bagheri-2019-pmwf-spp/full-text.md
tags:
  - noise-estimation
  - speech-enhancement
  - statistical-model
  - spp
  - recursive-averaging
  - mcra
---

# Multichannel MCRA

**Multichannel MCRA** (Minima-Controlled Recursive Averaging) extends single-channel MCRA to estimate the noise Power Spectral Density (PSD) *matrix* $\boldsymbol{\Phi}_{\mathbf{v}}(t,k)$ from multi-microphone signals using a Speech Presence Probability (SPP)-controlled recursive averager. The noise PSD matrix is updated only at TF bins where speech is likely absent, with the averaging controlled by the a posteriori SPP. Taseska & Habets (IEEE/ACM TASLP 2017) showed that an **ML formulation** of the multichannel noise-PSD/SPP estimation problem yields the same structure as multichannel MCRA, with a specific a priori Speech Absence Probability (SAP) and a specific recursive averaging parameter.

## Origin: SPP-Controlled Matrix Tracking (Souden et al. 2011)

[[sources/souden-2011-online-noise-tracking|Souden, Chen, Benesty & Affes 2011]] gave the first generalization of single-channel MCRA to the noise PSD *matrix*: under $H_0$ the matrix updates by recursive averaging, under $H_1$ it is frozen, and both cases combine into a single recursion with SPP-controlled smoothing

$$\tilde{\alpha}_v(k,l) = \alpha_v + (1-\alpha_v)\,p(k,l)$$

driven by the [[concepts/multi-channel-speech-presence-probability|MC-SPP]] (whose a priori SAP is estimated multivariately from Hotelling's $T^2$ / $F$-distributed SNR measures). Because the SPP itself requires a current noise PSD matrix, a **two-iteration procedure** refines both per frame; tracking halts during speech activity and resumes as speech energy decays, following nonstationary noise including the cross-PSD terms between microphones. This is the SNR/multivariate-statistics branch of multichannel a priori SAP control; the ML formulation below and the CDR-based SAP are alternative control signals.

## ML Formulation

The ML solution for the noise PSD matrix and SPP results in a recursive update structurally identical to MCRA:

$$
\hat{\boldsymbol{\Phi}}_{\mathbf{v}}(t,k) = \alpha_v(t,k)\,\hat{\boldsymbol{\Phi}}_{\mathbf{v}}(t-1,k) + (1-\alpha_v(t,k))\,\mathbf{y}(t,k)\mathbf{y}^{\mathrm{H}}(t,k),
$$

where the averaging parameter $\alpha_v$ and the a priori SAP are *given by the ML solution*. However, the pure-ML solution is **not adequate in non-stationary environments**: without additional control, changes in the noise properties are falsely detected as speech onsets, corrupting the noise PSD matrix estimate.

## CDR-Based a Priori SAP

The key contribution: a **CDR-based a priori SAP** estimator that exploits the spatial coherence difference between desired speech (coherent across the array) and background noise (approximately diffuse). The [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Ratio (CDR)]] is mapped to an a priori SAP via a sigmoid-like function, providing robust control that distinguishes noise-property changes from speech onsets. This is more robust than single-channel and multichannel SNR-based a priori SAPs (SC-Cohen, MC-Souden).

## Relation to ISFs

The estimated $\boldsymbol{\Phi}_{\mathbf{v}}$ and SPP drive [[concepts/informed-spatial-filter|informed MVDR and MWF filters]] for blind speech extraction. The SPP also serves as the PMWF trade-off parameter, balancing noise reduction against speech distortion.

## Practical Implementation (Bagheri & Giacobello 2019)

[[sources/bagheri-2019-pmwf-spp|Bagheri & Giacobello 2019]] implement exactly this structure — described as a multi-channel generalization of MCRA — with the [[concepts/multi-channel-speech-presence-probability|MC-SPP]] as the control signal: effective smoothing $\tilde{\alpha}_v(\ell,k) = \alpha_v + (1-\alpha_v)\,p(\ell,k)$ with fixed $q_0 = 0.5$, plus practical safeguards the ML derivation does not cover: SPP smoothing with clamping to $[p_{\min}, p_{\max}]$, a fallback $\widehat{\boldsymbol{\Phi}}_{vv}^{-1} = \widehat{\boldsymbol{\Phi}}_{yy}^{-1}$ when $\gamma$ or $\xi$ go negative, a noise-only initialization period, and — since each update is a rank-1 correction — a **direct Woodbury/Sherman–Morrison update of the inverse** $\widehat{\boldsymbol{\Phi}}_{vv}^{-1}$ that avoids per-frame matrix inversions. The same SPP drives the [[concepts/parametric-multi-channel-wiener-filter|PMWF]] trade-off parameter and an MMSE output estimate with a $G_{\min}$ suppression floor.

## Related Concepts

- [[concepts/informed-spatial-filter|Informed Spatial Filter (ISF)]]
- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio (CDR)]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/multi-channel-wiener-filter|Multichannel Wiener Filter]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/multi-channel-speech-presence-probability|Multi-Channel Speech Presence Probability]] — the SPP control signal in the multi-channel recursive averager
- [[concepts/parametric-multi-channel-wiener-filter|Parametric Multi-Channel Wiener Filter]] — downstream consumer of the noise PSD matrix estimate

## Related Sources

- [[sources/taseska-2018-informed-spatial-filters|Taseska 2018: Informed Spatial Filters for Speech Enhancement]] (Chapter 3)
- [[sources/bagheri-2019-pmwf-spp|Bagheri & Giacobello 2019: Exploiting MC-SPP in Parametric Multi-Channel Wiener Filter]] — practical MC-SPP-driven implementation with Woodbury inverse updates
- [[sources/souden-2011-online-noise-tracking|Souden, Chen, Benesty & Affes 2011: An Integrated Solution for Online Multichannel Noise Tracking and Reduction]] — origin of the SPP-controlled noise PSD matrix tracking recursion
