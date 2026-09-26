---
type: concept
created: 2026-05-27
updated: 2026-09-26
sources:
  - raw/papers/xiang-2025-wiener-gain-reverberant/full-text.md
  - raw/papers/xiang-2024-multichannel-cdr-estimation/full-text.md
  - raw/papers/haeb-umbach-2024-microphone-array-deep-learning/full-text.md
tags:
  - signal-processing
  - speech-enhancement
  - reverberation
  - multichannel
---

# Dereverberation

**Dereverberation** refers to the processing of reverberant speech signals to reduce or remove the effects of late reverberation, thereby improving speech quality and intelligibility. Dereverberation methods can be broadly categorized into spectral enhancement approaches (masking-based), linear prediction approaches (MCLP), and deep learning approaches.

## Problem

Reverberation arises from acoustic reflections off room surfaces, causing temporal smearing of the speech signal. The reverberant signal can be decomposed into:
- **Direct path**: The direct line-of-sight propagation
- **Early reflections**: Reflections within ~50 ms of the direct path (beneficial for speech perception)
- **Late reverberation**: Later reflections that degrade intelligibility

The early-to-late power ratio (ELR) measures the ratio between desired (early) and undesired (late) components.

## CDR-based Dereverberation

A widely-used approach estimates the coherent-to-diffuse power ratio (CDR) from spatial coherence between two or more microphones, then applies a spectral postfilter:

$$G(l,f) = \max\left\{G_{\min}, 1 - \sqrt{\frac{\mu}{\widehat{CDR}(l,f) + 1}}\right\}$$

Key advantages: can operate blindly without DOA knowledge, requires only two microphones, computationally efficient.

Classical CDR estimators, however, ignore additive noise and are therefore biased in noisy reverberant fields. [[sources/xiang-2025-wiener-gain-reverberant|Xiang et al. 2025]] address this with a **noise-aware, DOA-independent pairwise estimator** — folding the noise coherence and the (decision-directed) SNR into the Schwarz & Kellermann pairwise formulation — and drive a [[concepts/snr-cdr-wiener-gain|joint SNR–CDR Wiener gain]] after a robust superdirective beamformer, with hyperparameters separating the reverberation-suppression and noise-reduction axes. The approach outperforms AWPE (the WPE-style baseline) precisely in jointly noisy and reverberant environments, where AWPE's SRMR degrades rapidly as input SNR drops.

## Other Approaches

| Method | Description | Key Property |
|--------|-------------|-------------|
| **Spectral subtraction (Lebart)** | Exponential decay model of late reverberation energy | Requires $T_{60}$ estimate |
| **MCLP (Multi-Channel Linear Prediction)** | Linear prediction models reverberation as delayed/weighted copies | Effective for WPE-style dereverberation |
| **Deep learning** | DNN-based spectral mapping or masking | Data-driven, can operate single-channel |
| **PHM quadrilateral (TRU-Net)** | Two pairs of phase-aware β-sigmoid masks form a quadrilateral in the complex STFT domain; the reverberation mask is uniquely determined by the other three sides | Single-stage joint denoising + dereverberation, 0.38 M params, 0 ms lookahead |
| **Joint AEC+NS+DR (DeepVQE)** | Unified model with CCM for simultaneous echo/noise/reverb removal | Over 10 dB SRR improvement, real-time |
| **Beamforming + postfilter** | Spatial filtering combined with postfiltering | Multi-channel required |

## Historical Context

[[sources/richard-2023-audio-signal-processing-21st-century|Richard et al. 2023]] position dereverberation as a blind estimation problem (no anechoic reference) that matured from a sparse late-1990s literature into a flourishing field, marked by Naylor's dedicated dereverberation book (2010) and the community-wide REVERB Challenge. In their 25-year TC-AASP retrospective, the **weighted prediction error (WPE)** method is highlighted as the dominant blind multichannel-linear-prediction approach — it introduced a nonstationary Gaussian source model and delayed prediction that protects inherent source correlations from being whitened — with subsequent work shifting toward DNN-based spectral mapping and an expected continuation toward model-based + data-driven hybrids.

## WPE and the Hybrid Perspective (Haeb-Umbach et al. 2024)

[[sources/haeb-umbach-2024-microphone-array-deep-learning|Haeb-Umbach et al. 2024]] present the two model-based pillars alongside their hybrid extensions: (i) a **state-space view** of the convolutive transfer function model, dereverberated by an EM algorithm whose E-step is a Kalman filter (Schwartz, Gannot & Habets 2014); and (ii) [[concepts/weighted-prediction-error|WPE]], which models late reverberation as an auto-regressive process over past frames with prediction lag $\Delta$ (protecting speech's own AR structure from whitening) and a zero-mean complex-Gaussian early component with time-varying variance $\lambda_{t,f}$. On the hybrid side, the iterative alternation of AR parameters and $\lambda_{t,f}$ can be short-circuited by a **neural PSD estimator** for $\lambda_{t,f}$ (Kinoshita et al. 2017) — a canonical Class-2 (combined parameter estimation) hybrid — and neural source models similarly couple to IVA/IVE for joint dereverberation and separation. The article cites WPE + the spatial mixture model as the CHiME-6/7 baseline choices, evidencing model-based robustness under extreme acoustics.

## Related Concepts

- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio (CDR)]]
- [[concepts/spatial-coherence|Spatial Coherence]]
- [[concepts/diffuse-sound-extraction|Diffuse Sound Extraction]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/complex-convolving-mask|Complex Convolving Mask]]
- [[concepts/trunet|Tiny Recurrent U-Net (TRU-Net)]]
- [[concepts/phase-aware-beta-sigmoid-mask|Phase-aware β-sigmoid Mask (PHM)]]
- [[concepts/snr-cdr-wiener-gain|SNR–CDR Wiener Gain]] — noise-aware CDR-driven dereverberation gain

## Key Sources

- [[sources/schwarz-2015-coherent-to-diffuse-power-ratio|Schwarz & Kellermann 2015: CDR Estimation for Dereverberation]]
- [[sources/schwarz-2019-dereverberation-spatial-coherence|Schwarz 2019: Dereverberation and Robust Speech Recognition]]
- [[sources/indenbom-2023-deepvqe|Indenbom et al. 2023: DeepVQE]]
- [[sources/choi-2021-trunet-real-time-speech-enhancement|Choi et al. 2021: TRU-Net — Real-Time Denoising and Dereverberation with Tiny Recurrent U-Net]]
- [[sources/richard-2023-audio-signal-processing-21st-century|Richard et al. 2023: Audio Signal Processing in the 21st Century]] — 25-year retrospective positioning WPE and the dereverberation field
- [[sources/xiang-2025-wiener-gain-reverberant|Xiang, Chen, Benesty, Lei & Pan 2025: Design of the Wiener Gain in Noisy and Reverberant Environments]] — noise-aware CDR estimation + joint SNR–CDR Wiener gain; outperforms AWPE in noise + reverberation
- [[sources/haeb-umbach-2024-microphone-array-deep-learning|Haeb-Umbach et al. 2024: Microphone Array Signal Processing and Deep Learning for Speech Enhancement]] — WPE in the hybrid taxonomy: neural PSD estimation for model-based dereverberation (see [[concepts/weighted-prediction-error|WPE]])
