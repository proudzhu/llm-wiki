---
type: concept
created: 2026-06-19
updated: 2026-11-22
sources:
  - raw/papers/dang-2022-dpt-fsnet/full-text.md
  - raw/papers/chao-2024-mamba-speech-enhancement/full-text.md
  - raw/papers/pascual-2017-segan/full-text.md
  - raw/papers/fu-2019-metricgan/full-text.md
  - raw/papers/yan-2025-lisennet/full-text.md
  - raw/papers/ahn-2026-fastenhancer/full-text.md
  - raw/papers/kim-2026-faster-enhancer/full-text.md
  - raw/papers/laroche-2026-lisenet-embedded/full-text.md
  - raw/papers/zhao-2025-lightweight-transformer/full-text.md
  - raw/papers/fu-2026-one-model-many-latencies/full-text.md
  - raw/papers/li-2024-dbccrn/full-text.md
  - raw/papers/abdulatif-2024-cmgan/full-text.md
  - raw/papers/fu-2021-metricgan-plus/full-text.md
  - raw/papers/close-2022-metricgan-plus-minus/full-text.md
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
| [[concepts/segan\|SEGAN]] | 2.16 | 2017 | GAN-based; the benchmark's original configuration and first neural baseline |
| [[concepts/metricgan\|MetricGAN]] | 2.86 | 2019 | **Discriminator as learned metric surrogate** — first system trained directly against PESQ on this benchmark (CSIG 3.99 / CBAK 3.18 / COVL 3.42); distinct from the MetricGAN+ row below |
| [[sources/fu-2021-metricgan-plus\|MetricGAN+]] | 3.15 | 2021 | MetricGAN + three training techniques (noisy-speech $D$ targets, replay 0.2, learnable sigmoid $\beta = 1.2$); CSIG 4.14 / CBAK 3.16 / COVL 3.64 — CBAK trails rivals because the 0.05 mask floor leaves residual noise |
| [[concepts/dpt-fsnet\|DPT-FSNet]] | 3.33 | 2022 | Dual-path transformer full/sub-band fusion, 0.88 M params; CSIG 4.58 / CBAK 3.72 / COVL 4.00 / STOI 0.96 — [[sources/dang-2022-dpt-fsnet\|Dang et al. 2022]] |
| [[concepts/cmgan|CMGAN]] | 3.41 | 2022; extended 2024 | Conformer-based MetricGAN, 1.83 M params; CSIG 4.63 / CBAK 3.94 / COVL 4.12 / SSNR 11.10 / STOI 0.96 — [[sources/abdulatif-2024-cmgan|TASLP extension]] |
| MP-SENet | 3.50 | 2023 | Conformer TF backbone |
| [[concepts/dbccrn|DBCCRN]] + SA-SNR | 3.16 | 2024 | dual-branch complex CRN, 8.31 M params; ScaleError 0.014% |
| [[concepts/semamba|SEMamba]] | 3.55 | 2024 | [[concepts/mamba|Mamba]] replaces Conformer |
| [[concepts/semamba|SEMamba]] (+PCS) | **3.69** | 2024 | + [[concepts/perceptual-contrast-stretching|PCS]] post-processing — SOTA |
| Real-time RE-USE (Fu et al.) | 2.76 (LA 0) / 2.82 (LA 1) | 2026 | Cross-dataset (no VBD training); 2.9M params, 40/60 ms algorithmic latency, SI-SDR 18.6/18.8 dB |

FastEnhancer (Ahn et al. 2026) — the FastEnhancer family (22k–1.1M params, RTF 0.012–0.313 on Xeon) establishes a new performance-vs-speed Pareto frontier on this benchmark: FastEnhancer-B reaches PESQ 3.13 / STOI 0.945 at RTF 0.022, and FastEnhancer-T matches GTCRN-quality at RTF 0.012. Notably, FastEnhancer-B has *higher* MACs (262M) than GTCRN (40M) yet ~3× lower RTF — evidence that on this benchmark MACs are a poor proxy for real speed.

A 48 kHz variant of the benchmark appears in [[sources/kim-2026-faster-enhancer|Kim 2026]]: the faster-enhancer.c port evaluates FastEnhancer-Medium on the 824-utterance test set **at its native 48 kHz** (upstream trains/evaluates at 16 kHz), reporting fp32 PESQ 3.060 / STOI 0.9512 / SNR 19.43 and the int8 port tracking to −0.006 PESQ / −0.079 dB SNR. The paper also notes a metric-band caveat specific to fullband use: PESQ is defined only up to 16 kHz (blind above 8 kHz) and STOI observes 0–5 kHz, so fullband evaluation leans on SNR, LSD and SIGMOS — and fullband paired test sets remain scarce (DNS fullband tracks publish no clean references).

## Related Concepts

- [[concepts/dns-challenge|DNS Challenge (Deep Noise Suppression)]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/pesq|PESQ]] — primary evaluation metric
- [[concepts/semamba|SEMamba]] — current SOTA (PESQ 3.69)
- [[concepts/lisennet|LiSenNet]] — lightweight-SE reference point on this benchmark: PESQ 3.07 / STOI 0.939 at 37k params, 56M MACs/s

## Related Sources

- [[sources/pascual-2017-segan|Pascual, Bonafonte & Serrà 2017: SEGAN]] — the paper that *defined* this benchmark's canonical configuration (30 Voice Bank speakers split 28/2, 40 train conditions = 10 noise types × 4 SNR, 20 test conditions = 5 DEMAND noises × 4 SNR, 824 test files, 16 kHz) and supplied its first neural baseline: PESQ 2.16 / CSIG 3.48 / CBAK 2.94 / COVL 2.80 / SSNR 7.73, plus MOS 3.18 vs. Wiener 2.70
- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]
- [[sources/chao-2024-mamba-speech-enhancement|Chao et al. 2024: An Investigation of Incorporating Mamba for Speech Enhancement]] — SOTA PESQ 3.69 on VBD with SEMamba + PCS
- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]] — PESQ 3.07 / STOI 0.939 at 37k params and 56M MACs/s: the lightweight-SE operating point on this benchmark; also introduces the WSJ0+ESC50 instantaneous-noise dataset
- [[sources/ahn-2026-fastenhancer|Ahn, Han, Woo & Kim 2026: FastEnhancer]] — new performance-vs-speed Pareto frontier: FastEnhancer-B at PESQ 3.13 / STOI 0.945 / RTF 0.022, FastEnhancer-T at RTF 0.012; shows MACs are a poor proxy for real speed on this benchmark
- [[sources/kim-2026-faster-enhancer|Kim 2026: faster-enhancer.c]] — 48 kHz evaluation of FastEnhancer-Medium on the 824-utterance test set (fp32 PESQ 3.060); quantization-delta reference point (−0.006 PESQ) and metric-band caveats for fullband scoring
- [[sources/laroche-2026-lisenet-embedded|Laroche & Olsson 2026: Beyond Model Size]] — retrained LiSenNet baseline + 11 NPU variants evaluated on the full 824-utterance test set (16 kHz, CMGAN recipe), with PESQ reported both FP32 and int8
- [[sources/zhao-2025-lightweight-transformer|Zhao & Madhu 2025: LCT-GAN]] — smallest reported operating point that reaches DeepFilterNet2 quality: 0.14 M params / 0.35 G MAC/s → PESQ 3.06 (3.20 with PCS), CSIG 4.41, CBAK 3.66, COVL 3.80, STOI 0.95; the parameter-count floor among causal models on this benchmark
- [[sources/fu-2026-one-model-many-latencies|Fu et al. 2026: One Model, Many Latencies]] — cross-dataset (URGENT-trained) point: PESQ 2.76 / 2.82 at 40 / 60 ms algorithmic latency and 2.9M params, ahead of DeepFilterNet3 and Stream.FM at comparable latency
- [[sources/fu-2019-metricgan|Fu, Liao, Tsao & Lin 2019: MetricGAN]] — PESQ 2.86 / CSIG 3.99 / CBAK 3.18 / COVL 3.42, best of six compared systems: the first entry on this benchmark trained against a metric rather than a target signal, and the origin of the MetricGAN+ line (whose 3.15 row must not be conflated with it)
- [[sources/li-2024-dbccrn|Li, Sun, Zhang & Van hamme 2024: DBCCRN]] — PESQ 3.16 / STOI 0.940 / SSNR 10.98 at 8.31 M params; introduces the peak-normalized **scaled test set** variant of this benchmark to expose scale-sensitive losses ([[concepts/scale-error|ScaleError]])
- [[sources/dang-2022-dpt-fsnet|Dang, Chen & Zhang 2022: DPT-FSNet]] — PESQ 3.33 / STOI 0.96 at 0.88 M params (fewest among its compared systems); the paper states 872 test utterances where the canonical release has 824 — an apparent typo, scores unaffected
- [[sources/fu-2021-metricgan-plus|Fu et al. 2021: MetricGAN+]] — PESQ 3.15 / CSIG 4.14 / CBAK 3.16 / COVL 3.64 at an unchanged BLSTM backbone; the cumulative ablation (2.86 → 2.95 → 3.02 → 3.05 → 3.15) and replay-portion study are the benchmark's cleanest loss-technique isolation
- [[sources/close-2022-metricgan-plus-minus|Close, Hain & Goetze 2022: MetricGAN+/-]] — SpeechBrain MetricGAN+ re-run scores 3.05 (not the reported 3.15), de-generator extension reaches 3.22; also evaluates VBD-trained models on CHiME-3 real/simulated — a cross-dataset generalization protocol for this benchmark's models