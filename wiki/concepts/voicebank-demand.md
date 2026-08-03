---
type: concept
created: 2026-06-19
updated: 2026-08-03
sources:
  - raw/papers/chao-2024-mamba-speech-enhancement/full-text.md
tags:
  - dataset
  - speech-enhancement
---

# VoiceBank+DEMAND (VBD)

VoiceBank+DEMAND is a standard benchmark dataset for speech enhancement. It combines clean speech from the VoiceBank corpus with noise from the DEMAND database. The training set contains 28 speakers, and the test set contains 2 unseen speakers. Noisy utterances are mixed at various SNRs with diverse noise types.

## Standard Configuration

The configuration used by [[concepts/semamba|SEMamba]] (Chao et al. 2024) and most modern SE benchmarks:

- **Speakers**: 30 total — 28 for training, 2 for testing (unseen)
- **Train SNRs**: 0, 5, 10, 15 dB
- **Test SNRs**: 2.5, 7.5, 12.5, 17.5 dB
- **Train utterances**: 11,572
- **Test utterances**: 824
- **Sample rate**: 16 kHz (downsampled from 48 kHz)
- **Metrics**: WB-PESQ, CSIG, CBAK, COVL, STOI

The noisy baseline scores PESQ = 1.97, CSIG = 3.35, CBAK = 2.44, COVL = 2.63, STOI = 0.92.

## SOTA Results on VBD

| System | PESQ | Year | Notes |
|--------|------|------|-------|
| SEGAN | 2.16 | 2017 | GAN-based |
| MetricGAN+ | 3.15 | 2021 | metric-oriented loss |
| CMGAN | 3.41 | 2022 | conformal metric GAN |
| MP-SENet | 3.50 | 2023 | Conformer TF backbone |
| [[concepts/semamba|SEMamba]] | 3.55 | 2024 | [[concepts/mamba|Mamba]] replaces Conformer |
| **[[concepts/semamba|SEMamba]] (+PCS)** | **3.69** | 2024 | + [[concepts/perceptual-contrast-stretching|PCS]] post-processing — SOTA |

## Related Concepts

- [[concepts/dns-challenge|DNS Challenge (Deep Noise Suppression)]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/pesq|PESQ]] — primary evaluation metric
- [[concepts/semamba|SEMamba]] — current SOTA (PESQ 3.69)

## Related Sources

- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]
- [[sources/chao-2024-mamba-speech-enhancement|Chao et al. 2024: An Investigation of Incorporating Mamba for Speech Enhancement]] — SOTA PESQ 3.69 on VBD with SEMamba + PCS