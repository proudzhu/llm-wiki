---
type: concept
created: 2026-08-03
updated: 2026-08-03
sources:
  - raw/papers/chao-2024-mamba-speech-enhancement/full-text.md
tags:
  - speech-enhancement
  - post-processing
  - psychoacoustics
  - spectral-processing
---

# Perceptual Contrast Stretching (PCS)

**Perceptual Contrast Stretching (PCS)** is a post-enhancement spectral processing technique that improves the perceptual quality of speech signals by stretching the magnitude spectrum according to the **perceptual importance of each frequency band**, exploiting the varying sensitivity of the human auditory system. It is an auxiliary step applied **after** the speech enhancement (SE) model has produced its output, rather than a change to the model architecture itself. PCS was introduced to SE by Scalias et al. (2021) and was combined with [[concepts/semamba|SEMamba]] by Chao et al. (IEEE SLT 2024) to set a new state-of-the-art [[concepts/pesq|PESQ]] of 3.69 on the [[concepts/voicebank-demand|VoiceBank-DEMAND]] benchmark.

## Mechanism

PCS works by applying a **non-linear stretching** to the enhanced magnitude spectrum: frequency bands that are perceptually more important (where the human auditory system is more sensitive) are amplified relative to less important bands. This is grounded in the empirical observation that the human auditory system exhibits frequency-dependent sensitivity — for example, the 1–4 kHz range critical for speech intelligibility is weighted more heavily than very low or very high frequencies.

The key property is that PCS:

- **Does not change the SE model** — it is applied to the model's output as a post-processing step.
- **No runtime cost increase** — the stretching is a cheap spectral operation applied once to the enhanced spectrogram, so the model's computational footprint is unchanged.
- **Trades background intrusiveness for perceptual quality** — on VoiceBank-DEMAND, adding PCS to SEMamba raises PESQ from 3.55 to 3.69 but lowers CBAK (background-intrusiveness prediction) from 3.95 to 3.63, reflecting a deliberate emphasis on speech over background.

## Effect on SEMamba

| Variant | PESQ | CSIG | CBAK | COVL | STOI |
|---------|------|------|------|------|------|
| SEMamba (no PCS) | 3.55 | 4.77 | 3.95 | 4.29 | 0.96 |
| **SEMamba (+PCS)** | **3.69** | 4.79 | 3.63 | 4.37 | 0.96 |

PCS adds **+0.14 PESQ** and +0.08 COVL at the cost of −0.32 CBAK. STOI is unchanged.

## Related Concepts

- [[concepts/semamba|SEMamba]] — the SE system that PCS lifts to SOTA PESQ
- [[concepts/speech-enhancement|Speech Enhancement]] — the task
- [[concepts/pesq|PESQ]] — the metric that PCS optimizes for
- [[concepts/voicebank-demand|VoiceBank-DEMAND]] — the benchmark where the SOTA result is set

## Related Sources

- [[sources/chao-2024-mamba-speech-enhancement|Chao et al. 2024: An Investigation of Incorporating Mamba for Speech Enhancement]]
