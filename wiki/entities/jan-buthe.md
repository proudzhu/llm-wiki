---
type: entity
created: 2026-08-14
updated: 2026-08-30
sources:
  - raw/papers/valin-2024-fargan/full-text.md
tags:
  - researcher
  - speech-coding
  - bandwidth-extension
  - audio-signal-processing
  - low-complexity
---

# Jan Büthe

**Affiliation**: Amazon Web Services
**Role**: Researcher
**Research Focus**: Low-complexity speech coding and enhancement, neural codec post-processing, bandwidth extension, hybrid DSP/DNN architectures for real-time audio.

## Key Contributions

- Lead author of **BBWENet** (WASPAA 2025) — a lightweight blind wideband-to-fullband bandwidth extension model (~370 K params, ~140 MFLOPS) combining classical time-domain BWE signal processing with a small DNN; paired with Opus 1.5 it matches EVS 9.6 kb/s quality at 9 kb/s — [[sources/buthe-2025-blind-wideband-to-fullband-extension|Büthe & Valin 2025]]
- Co-author of **LACE** (WASPAA 2023) — a light-weight causal model for enhancing coded speech through adaptive convolutions (AdaConv); its STFT envelope-matching and spectral fine-structure losses are reused in BBWENet
- Co-author of **NoLACE** (ICASSP 2024) — improving low-complexity speech codec enhancement through adaptive temporal shaping (AdaShape); its frequency-domain discriminator design is adapted in BBWENet
- Co-author of noise-robust DSP-assisted neural pitch estimation (ICASSP 2024, with Subramani, Valin, Smaragdis & Goodwin) — complex phase-difference features that proved sufficient for high-accuracy pitch estimation, reused as BBWENet input features
- Co-authored "Very Low Complexity Speech Synthesis Using Framewise Autoregressive GAN (FARGAN) with Pitch Prediction" (IEEE Signal Processing Letters 2024) — 600-MFLOPS pitch-predictive GAN vocoder; its STFT discriminator bank reuses the frequency-stride and positional-embedding modifications he introduced with NoLACE — [[sources/valin-2024-fargan|Valin et al. 2024]]
