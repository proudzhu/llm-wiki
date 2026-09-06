---
type: concept
created: 2026-06-19
updated: 2026-09-06
sources:
  - raw/papers/chao-2024-mamba-speech-enhancement/full-text.md
  - raw/papers/wang-2021-magnitude-phase-compensation/full-text.md
tags:
  - evaluation-metric
  - speech-quality
---

# Perceptual Evaluation of Speech Quality (PESQ)

PESQ (Perceptual Evaluation of Speech Quality) is an ITU-T P.862 standard objective metric for evaluating speech quality. It compares a degraded speech signal against the original clean reference and returns a score between -0.5 and 4.5. Wide-band PESQ (WB-PESQ) is commonly used in speech enhancement evaluation.

## Notable PESQ Results on VoiceBank-DEMAND

The VoiceBank-DEMAND benchmark has become a de facto standard for reporting PESQ in monaural speech enhancement. The progression of SOTA:

| System | Year | PESQ | Method |
|--------|------|------|--------|
| SEGAN | 2017 | 2.16 | GAN |
| MetricGAN+ | 2021 | 3.15 | metric-oriented loss |
| CMGAN | 2022 | 3.41 | conformal metric GAN |
| MP-SENet | 2023 | 3.50 | Conformer TF backbone |
| [[concepts/semamba|SEMamba]] | 2024 | 3.55 | [[concepts/mamba|Mamba]] replaces Conformer |
| **[[concepts/semamba|SEMamba]] (+PCS)** | 2024 | **3.69** | + [[concepts/perceptual-contrast-stretching|PCS]] — current SOTA |

## Why PESQ Rewards Magnitude over Phase

PESQ first time-aligns the predicted signal with the reference segment-wise (forgiving segmental time delays), then compares short-time Bark-scale power spectra. It therefore favours an accurate **magnitude** and is largely insensitive to phase errors and small signal shifts. [[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021]] provide the strongest evidence: a time-domain model trained with a magnitude-only loss ($\mathcal{L}_{\text{Wav}\times 0+\text{Mag}}$) reaches PESQ 2.67 on WHAMR! despite SI-SDR −9.09 dB and near-random phase (pSNR −3.64 dB) — PESQ stays good as long as the magnitude is good. This is also why adding a magnitude-domain training loss improves PESQ while slightly hurting SI-SDR (see [[concepts/magnitude-phase-compensation-effect|magnitude-phase compensation effect]]).

## Related Concepts

- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/voicebank-demand|VoiceBank-DEMAND]] — the benchmark where PESQ is most reported
- [[concepts/semamba|SEMamba]] — current SOTA PESQ 3.69
- [[concepts/perceptual-contrast-stretching|Perceptual Contrast Stretching (PCS)]] — post-processing that boosts PESQ
- [[concepts/magnitude-phase-compensation-effect|Magnitude-Phase Compensation Effect]] — why PESQ and SI-SDR respond oppositely to magnitude losses

## Related Sources

- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]
- [[sources/chao-2024-mamba-speech-enhancement|Chao et al. 2024: An Investigation of Incorporating Mamba for Speech Enhancement]] — SOTA PESQ 3.69 with SEMamba + PCS
- [[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021: On the Compensation Between Magnitude and Phase in Speech Separation]] — analyzes PESQ's magnitude-dominant behavior