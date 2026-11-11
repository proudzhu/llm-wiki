---
type: concept
created: 2026-06-19
updated: 2026-11-11
sources:
  - raw/papers/chao-2024-mamba-speech-enhancement/full-text.md
  - raw/papers/yan-2025-lisennet/full-text.md
  - raw/papers/ahn-2026-fastenhancer/full-text.md
  - raw/papers/kim-2026-faster-enhancer/full-text.md
  - raw/papers/laroche-2026-lisenet-embedded/full-text.md
  - raw/papers/zhao-2025-lightweight-transformer/full-text.md
  - raw/papers/fu-2026-one-model-many-latencies/full-text.md
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

- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]
- [[sources/chao-2024-mamba-speech-enhancement|Chao et al. 2024: An Investigation of Incorporating Mamba for Speech Enhancement]] — SOTA PESQ 3.69 on VBD with SEMamba + PCS
- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]] — PESQ 3.07 / STOI 0.939 at 37k params and 56M MACs/s: the lightweight-SE operating point on this benchmark; also introduces the WSJ0+ESC50 instantaneous-noise dataset
- [[sources/ahn-2026-fastenhancer|Ahn, Han, Woo & Kim 2026: FastEnhancer]] — new performance-vs-speed Pareto frontier: FastEnhancer-B at PESQ 3.13 / STOI 0.945 / RTF 0.022, FastEnhancer-T at RTF 0.012; shows MACs are a poor proxy for real speed on this benchmark
- [[sources/kim-2026-faster-enhancer|Kim 2026: faster-enhancer.c]] — 48 kHz evaluation of FastEnhancer-Medium on the 824-utterance test set (fp32 PESQ 3.060); quantization-delta reference point (−0.006 PESQ) and metric-band caveats for fullband scoring
- [[sources/laroche-2026-lisenet-embedded|Laroche & Olsson 2026: Beyond Model Size]] — retrained LiSenNet baseline + 11 NPU variants evaluated on the full 824-utterance test set (16 kHz, CMGAN recipe), with PESQ reported both FP32 and int8
- [[sources/zhao-2025-lightweight-transformer|Zhao & Madhu 2025: LCT-GAN]] — smallest reported operating point that reaches DeepFilterNet2 quality: 0.14 M params / 0.35 G MAC/s → PESQ 3.06 (3.20 with PCS), CSIG 4.41, CBAK 3.66, COVL 3.80, STOI 0.95; the parameter-count floor among causal models on this benchmark
- [[sources/fu-2026-one-model-many-latencies|Fu et al. 2026: One Model, Many Latencies]] — cross-dataset (URGENT-trained) point: PESQ 2.76 / 2.82 at 40 / 60 ms algorithmic latency and 2.9M params, ahead of DeepFilterNet3 and Stream.FM at comparable latency