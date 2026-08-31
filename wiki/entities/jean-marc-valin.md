---
type: entity
created: 2026-07-17
updated: 2026-08-31
sources:
  - raw/papers/mustafa-2023-framewise-wavegan/full-text.md
  - raw/papers/valin-2021-percepnet-joint-echo-control/full-text.md
  - raw/papers/valin-2022-real-time-plc/full-text.md
  - raw/papers/valin-2018-lpcnet/full-text.md
  - raw/papers/valin-2024-fargan/full-text.md
tags:
  - researcher
  - speech-enhancement
  - acoustic-echo-cancellation
  - audio-signal-processing
---

# Jean-Marc Valin

**Affiliation**: Amazon Web Services, Palo Alto, CA, USA (at the time of LPCNet, 2018: Mozilla, Mountain View, CA, USA; at the time of FARGAN, 2024: Xiph.Org Foundation)
**Role**: Researcher / Principal Scientist
**Research Focus**: Real-time speech enhancement, acoustic echo cancellation, low-complexity neural audio processing, perceptually-motivated DSP/DNN hybrid architectures.

## Key Contributions

- Lead author of **PercepNet** — the perceptually-motivated low-complexity speech enhancement model (ICASSP 2020) and its extension to joint echo control (arXiv 2021, 1st place ICASSP 2021 AEC Challenge) — [[sources/valin-2021-percepnet-joint-echo-control|Valin et al. 2021]]
- Author of **LPCNet** (ICASSP 2019) — neural speech synthesis through linear prediction; the WaveRNN + linear-prediction hybrid reaches speaker-independent synthesis at ≈2.8 GFLOPS, real-time on a single Apple A8 (iPhone 6) core — [[sources/valin-2018-lpcnet|Valin & Skoglund 2018]]
- Author of **SpeexDSP** — open-source acoustic echo cancellation library implementing the multidelay block frequency-domain (MDF) adaptive filter used in the PercepNet AEC system
- Contributor to **Opus audio codec** (Xiph.Org / IETF RFC 6716)
- Co-authored "A Lightweight and Robust Method for Blind Wideband-to-Fullband Extension of Speech" (WASPAA 2025) — a hybrid DSP/DNN blind BWE model (~370 K params, ~140 MFLOPS) that, paired with Opus 1.5 at 9 kb/s, statistically matches EVS at 9.6 kb/s and Opus 1.4 at 18 kb/s — [[sources/buthe-2025-blind-wideband-to-fullband-extension|Büthe & Valin 2025]]
- Lead author of "Real-Time Packet Loss Concealment With Mixed Generative and Predictive Model" (INTERSPEECH 2022, pp. 570–574) — hybrid LPCNet + predictive RNN PLC, 2nd place Interspeech 2022 Audio Deep PLC Challenge (1st in WAcc); first neural PLC integrated into the Opus speech codec (replacing SILK PLC) — [[sources/valin-2022-real-time-plc|Valin et al. 2022]]
- Lead author of "Very Low Complexity Speech Synthesis Using Framewise Autoregressive GAN (FARGAN) with Pitch Prediction" (IEEE Signal Processing Letters 2024) — 600-MFLOPS GAN vocoder with pitch-prediction autoregression, statistically tied with CARGAN and HiFi-GAN v1 at 64–110× lower complexity; replaced LPCNet as the DRED vocoder in Opus 1.5 — [[sources/valin-2024-fargan|Valin et al. 2024]]
- Co-authored "Framewise WaveGAN: High Speed Adversarial Vocoder in Time Domain with Very Low Computational Complexity" (ICASSP 2023) — the 1.2-GFLOPS framewise GAN vocoder whose framewise generation and two-stage spectral pre-training/adversarial recipe FARGAN builds on — [[sources/mustafa-2023-framewise-wavegan|Mustafa et al. 2023]]
