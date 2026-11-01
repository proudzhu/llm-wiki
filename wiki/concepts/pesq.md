---
type: concept
created: 2026-06-19
updated: 2026-11-01
sources:
  - raw/papers/chao-2024-mamba-speech-enhancement/full-text.md
  - raw/papers/wang-2021-magnitude-phase-compensation/full-text.md
  - raw/papers/lee-2016-dnn-plc/full-text.md
  - raw/papers/yan-2025-lisennet/full-text.md
  - raw/papers/ahn-2026-fastenhancer/full-text.md
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

FastEnhancer (Ahn et al. 2026) — uses a differentiable PESQ loss (torch-pesq) with a deliberately tiny weight ($\lambda_5 = 0.001$) inside its five-term composite loss, citing the PESQetarian / Goodhart's-law concern (de Oliveira et al. 2024); the tiny weight improved not only PESQ but also other objective metrics. The paper also observes a metric-disagreement caution: FastEnhancer-M slightly degrades DNSMOS despite improving every other metric vs S.

## Related Concepts

- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/voicebank-demand|VoiceBank-DEMAND]] — the benchmark where PESQ is most reported
- [[concepts/semamba|SEMamba]] — current SOTA PESQ 3.69
- [[concepts/perceptual-contrast-stretching|Perceptual Contrast Stretching (PCS)]] — post-processing that boosts PESQ
- [[concepts/magnitude-phase-compensation-effect|Magnitude-Phase Compensation Effect]] — why PESQ and SI-SDR respond oppositely to magnitude losses
- [[concepts/lisennet|LiSenNet]] — uses PESQ not only as a metric but as a *training loss* (MetricGAN-style discriminator, λ₃ = 0.05)

## Related Sources

- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]
- [[sources/chao-2024-mamba-speech-enhancement|Chao et al. 2024: An Investigation of Incorporating Mamba for Speech Enhancement]] — SOTA PESQ 3.69 with SEMamba + PCS
- [[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021: On the Compensation Between Magnitude and Phase in Speech Separation]] — analyzes PESQ's magnitude-dominant behavior
- [[sources/lee-2016-dnn-plc|Lee & Chang 2016: PLC Based on DNNs for Digital Speech Transmission]] — PESQ (with LSD and MOS) as the objective metric for DNN-regression PLC on AMR-WB at 5–30% packet loss
- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]] — includes a PESQ *loss* in the MetricGAN+ tradition (discriminator predicts PESQ scaled to (0,1); λ₃ = 0.05): worth +0.12 PESQ in ablation, the single largest contributor among LiSenNet's loss terms
- [[sources/ahn-2026-fastenhancer|Ahn, Han, Woo & Kim 2026: FastEnhancer]] — differentiable torch-pesq loss with tiny weight λ₅ = 0.001 (Goodhart's-law guard); improved PESQ *and* other metrics; also documents a DNSMOS-vs-other-metrics disagreement case (FastEnhancer-M)