---
type: concept
created: 2026-06-19
updated: 2026-11-22
sources:
  - raw/papers/dang-2022-dpt-fsnet/full-text.md
  - raw/papers/braun-2021-loss-functions-speech-enhancement/full-text.md
  - raw/papers/chao-2024-mamba-speech-enhancement/full-text.md
  - raw/papers/pascual-2017-segan/full-text.md
  - raw/papers/fu-2019-metricgan/full-text.md
  - raw/papers/wang-2021-magnitude-phase-compensation/full-text.md
  - raw/papers/lee-2016-dnn-plc/full-text.md
  - raw/papers/yan-2025-lisennet/full-text.md
  - raw/papers/ahn-2026-fastenhancer/full-text.md
  - raw/papers/laroche-2026-lisenet-embedded/full-text.md
  - wiki/sources/wu-2026-dbmif-multimodal-fusion.md
  - raw/papers/li-2024-dbccrn/full-text.md
  - raw/papers/abdulatif-2024-cmgan/full-text.md
  - raw/papers/fu-2020-metricgan-post-processing/full-text.md
tags:
  - evaluation-metric
  - speech-quality
---

# Perceptual Evaluation of Speech Quality (PESQ)

PESQ (Perceptual Evaluation of Speech Quality) is an ITU-T P.862 standard objective metric for evaluating speech quality. It compares a degraded speech signal against the original clean reference and returns a score between -0.5 and 4.5. Wide-band PESQ (WB-PESQ) is commonly used in speech enhancement evaluation.

## PESQ as a Training Objective (the MetricGAN Line)

PESQ is not differentiable, so making it a *training signal* required a workaround. [[sources/fu-2019-metricgan|Fu et al. 2019 (MetricGAN, ICML)]] supply the origin of the family: a discriminator regressed onto PESQ values, with the generator pushed toward an assigned score $s$ — a black-box route needing no knowledge of PESQ's internals. It set PESQ 2.86 / CSIG 3.99 / CBAK 3.18 / COVL 3.42 on VoiceBank+DEMAND and is the reference point of this table's MetricGAN+ row.

The same experiments yield two cautionary findings about optimizing PESQ directly:

- **Every optimization is a bias purchase.** Driving an assigned PESQ score *down* makes MetricGAN add noise to the signal — not delete speech (which is what driving STOI down does). PESQ therefore rewards noise suppression over speech preservation, and a model optimized for it will trade accordingly.
- **The metric can be gamed.** PESQ-first training produced artifacts that PESQ itself ranks well but that are audible; the paper reports the adversarial term's optimum includes "unpleasant artifacts" at higher weight, and later work (FastEnhancer's $\lambda_5 = 10^{-3}$ PESQ term, the PESQetarian critique) treats this Goodhart risk explicitly.
- **The blind spot has a frequency address.** [[sources/fu-2020-metricgan-post-processing|Fu et al. (APSIPA ASC 2020)]] report that fine-tuning against a PESQ (or STOI) surrogate can generate *high-frequency noise*, because both metrics ignore signal differences in the high-frequency range — a concrete artifact mechanism behind the Goodhart concern, mitigated only by bounding the output (mask estimation rather than spectral mapping).

PESQ nonetheless remains the field's headline reporting metric — see the VoiceBank-DEMAND table below, where nearly every modern system optimizes it or a proxy for it.

## Notable PESQ Results on VoiceBank-DEMAND

The VoiceBank-DEMAND benchmark has become a de facto standard for reporting PESQ in monaural speech enhancement. The progression of SOTA:

| System | Year | PESQ | Method |
|--------|------|------|--------|
| [[concepts/segan\|SEGAN]] | 2017 | 2.16 | GAN |
| [[concepts/metricgan\|MetricGAN]] | 2019 | 2.86 | PESQ-optimized via learned surrogate |
| MetricGAN+ | 2021 | 3.15 | metric-oriented loss |
| [[concepts/dpt-fsnet\|DPT-FSNet]] | 2022 | 3.33 | Dual-path transformer full/sub-band fusion; 0.88 M params, discriminative dual-domain loss (no metric surrogate) |
| [[concepts/cmgan|CMGAN]] | 2022; extended 2024 | 3.41 | Conformer-based MetricGAN; PESQ-surrogate loss weighted 0.01 alongside reconstruction losses — [[sources/abdulatif-2024-cmgan|TASLP extension]] |
| MP-SENet | 2023 | 3.50 | Conformer TF backbone |
| [[concepts/semamba|SEMamba]] | 2024 | 3.55 | [[concepts/mamba|Mamba]] replaces Conformer |
| **[[concepts/semamba|SEMamba]] (+PCS)** | 2024 | **3.69** | + [[concepts/perceptual-contrast-stretching|PCS]] — current SOTA |

## Why PESQ Rewards Magnitude over Phase

PESQ first time-aligns the predicted signal with the reference segment-wise (forgiving segmental time delays), then compares short-time Bark-scale power spectra. It therefore favours an accurate **magnitude** and is largely insensitive to phase errors and small signal shifts. [[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021]] provide the strongest evidence: a time-domain model trained with a magnitude-only loss ($\mathcal{L}_{\text{Wav}\times 0+\text{Mag}}$) reaches PESQ 2.67 on WHAMR! despite SI-SDR −9.09 dB and near-random phase (pSNR −3.64 dB) — PESQ stays good as long as the magnitude is good. This is also why adding a magnitude-domain training loss improves PESQ while slightly hurting SI-SDR (see [[concepts/magnitude-phase-compensation-effect|magnitude-phase compensation effect]]).

FastEnhancer (Ahn et al. 2026) — uses a differentiable PESQ loss (torch-pesq) with a deliberately tiny weight ($\lambda_5 = 0.001$) inside its five-term composite loss, citing the PESQetarian / Goodhart's-law concern (de Oliveira et al. 2024); the tiny weight improved not only PESQ but also other objective metrics. The paper also observes a metric-disagreement caution: FastEnhancer-M slightly degrades DNSMOS despite improving every other metric vs S.

## PESQ as a Model-Selection and Hyperparameter Objective

PESQ does not have to be differentiable to steer training: it can select. [[sources/braun-2021-loss-functions-speech-enhancement|Braun & Tashev 2021]] chose the best checkpoint by validation PESQ (every 10 epochs) **and** grid-searched every loss weight ($\beta$, $\lambda$, compression and weighting constants) against validation PESQ, so all 19 compared losses were tuned to the same metric.

The consequence is visible in their own table: the PESQ-optimal mixture weight gave PESQ 3.31 while its SI-SDR fell to 9.42 dB, below the MAE mixture's 9.75 dB — i.e. tuning to PESQ systematically selects the configuration that trades waveform accuracy for spectral magnitude accuracy. Any "loss X beats loss Y" claim measured under PESQ-guided selection is therefore a claim about PESQ's preference as much as about the loss.

## PESQ Misses Scale Errors (Li et al. 2024)

[[sources/li-2024-dbccrn|Li et al. 2024]] document a blind spot complementary to the magnitude bias above: PESQ (and STOI/COVL) barely notice **output amplitude drift**. DCCRN trained with SI-SNR scores PESQ 2.89 on VoiceBank+DEMAND while its output peaks overshoot the target by ScaleError 18.653% — clipping in any $[-1,1]$ playback pipeline. On a peak-normalized test set the same model drops to PESQ 2.50, while [[concepts/scale-aware-snr|SA-SNR]] training holds 3.16 → 3.15. Their [[concepts/scale-error|ScaleError]] metric and scaled-test-set recipe make this failure mode measurable alongside PESQ.

## Related Concepts

- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/voicebank-demand|VoiceBank-DEMAND]] — the benchmark where PESQ is most reported
- [[concepts/semamba|SEMamba]] — current SOTA PESQ 3.69
- [[concepts/perceptual-contrast-stretching|Perceptual Contrast Stretching (PCS)]] — post-processing that boosts PESQ
- [[concepts/magnitude-phase-compensation-effect|Magnitude-Phase Compensation Effect]] — why PESQ and SI-SDR respond oppositely to magnitude losses
- [[concepts/lisennet|LiSenNet]] — uses PESQ not only as a metric but as a *training loss* (MetricGAN-style discriminator, λ₃ = 0.05)

## Related Sources

- [[sources/braun-2021-loss-functions-speech-enhancement|Braun & Tashev 2021: A Consolidated View of Loss Functions]] — PESQ used as *both* checkpoint-selection criterion and hyperparameter grid-search objective for 17 losses, which biases the comparison toward magnitude-accurate configurations (PESQ-best 3.31 at SI-SDR 9.42 vs. MAE mixture 9.75 dB)
- [[sources/fu-2019-metricgan|Fu, Liao, Tsao & Lin 2019: MetricGAN]] — the origin of PESQ-as-training-objective: a discriminator regressed onto PESQ values steers the generator, and the score-assignment experiment shows the metric-optimal direction adds noise rather than preserving speech (PESQ measures quality, not intelligibility — contrast [[concepts/stoi|STOI]])
- [[sources/pascual-2017-segan|Pascual, Bonafonte & Serrà 2017: SEGAN]] — the benchmark's origin point and its illustrative case for PESQ's phase/magnitude bias: SEGAN scores **below** the Wiener baseline on PESQ (2.16 vs 2.22) yet above it on CSIG/CBAK/COVL/SSNR and on subjective MOS (3.18 vs 2.70), i.e. PESQ penalizes the adversarial objective's high-frequency artifacts more than listeners do
- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]
- [[sources/chao-2024-mamba-speech-enhancement|Chao et al. 2024: An Investigation of Incorporating Mamba for Speech Enhancement]] — SOTA PESQ 3.69 with SEMamba + PCS
- [[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021: On the Compensation Between Magnitude and Phase in Speech Separation]] — analyzes PESQ's magnitude-dominant behavior
- [[sources/lee-2016-dnn-plc|Lee & Chang 2016: PLC Based on DNNs for Digital Speech Transmission]] — PESQ (with LSD and MOS) as the objective metric for DNN-regression PLC on AMR-WB at 5–30% packet loss
- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]] — includes a PESQ *loss* in the MetricGAN+ tradition (discriminator predicts PESQ scaled to (0,1); λ₃ = 0.05): worth +0.12 PESQ in ablation, the single largest contributor among LiSenNet's loss terms
- [[sources/ahn-2026-fastenhancer|Ahn, Han, Woo & Kim 2026: FastEnhancer]] — differentiable torch-pesq loss with tiny weight λ₅ = 0.001 (Goodhart's-law guard); improved PESQ *and* other metrics; also documents a DNSMOS-vs-other-metrics disagreement case (FastEnhancer-M)
- [[sources/laroche-2026-lisenet-embedded|Laroche & Olsson 2026: Beyond Model Size]] — on-device int8 PESQ 3.01 on VoiceBank-DEMAND (STM32N6 NPU): the deployment-domain PESQ comparison (quality after static quantization, measured against the FP32 graph)
- [[sources/wu-2026-dbmif-multimodal-fusion|Wu et al. 2026: DBMIF]] — PESQ 2.70 for AC/BC fusion (best of nine), contrasted with DNSMOS 3.35 as the GAN-training effect
- [[sources/li-2024-dbccrn|Li, Sun, Zhang & Van hamme 2024: DBCCRN]] — PESQ's blindness to output-scale drift; ScaleError + peak-normalized scaled test set as companion evaluation
- [[sources/dang-2022-dpt-fsnet|Dang, Chen & Zhang 2022: DPT-FSNet]] — discriminative counterpoint on VoiceBank+DEMAND: waveform MSE + RI-magnitude L1 (no PESQ surrogate) reaches PESQ 3.33 at 0.88 M params
- [[sources/fu-2020-metricgan-post-processing|Fu et al. 2020: MetricGAN Post-Processing]] — PESQ-surrogate fine-tuning of a converged Transformer (+0.138 PESQ on DNS 2020 at unchanged complexity); documents the high-frequency-noise artifact PESQ cannot penalize