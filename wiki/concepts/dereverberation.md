---
type: concept
created: 2026-05-27
updated: 2026-08-08
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

## Key Sources

- [[sources/schwarz-2015-coherent-to-diffuse-power-ratio|Schwarz & Kellermann 2015: CDR Estimation for Dereverberation]]
- [[sources/schwarz-2019-dereverberation-spatial-coherence|Schwarz 2019: Dereverberation and Robust Speech Recognition]]
- [[sources/indenbom-2023-deepvqe|Indenbom et al. 2023: DeepVQE]]
- [[sources/choi-2021-trunet-real-time-speech-enhancement|Choi et al. 2021: TRU-Net — Real-Time Denoising and Dereverberation with Tiny Recurrent U-Net]]
- [[sources/richard-2023-audio-signal-processing-21st-century|Richard et al. 2023: Audio Signal Processing in the 21st Century]] — 25-year retrospective positioning WPE and the dereverberation field
