---
type: concept
created: 2026-05-27
updated: 2026-05-27
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
| **Beamforming + postfilter** | Spatial filtering combined with postfiltering | Multi-channel required |

## Related Concepts

- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio (CDR)]]
- [[concepts/spatial-coherence|Spatial Coherence]]
- [[concepts/diffuse-sound-extraction|Diffuse Sound Extraction]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/wiener-filter|Wiener Filter]]

## Key Sources

- [[sources/schwarz-2015-coherent-to-diffuse-power-ratio|Schwarz & Kellermann 2015: CDR Estimation for Dereverberation]]
- [[sources/schwarz-2019-dereverberation-spatial-coherence|Schwarz 2019: Dereverberation and Robust Speech Recognition]]
