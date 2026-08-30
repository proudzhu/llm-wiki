---
type: synthesis
created: 2026-08-30
updated: 2026-08-30
sources:
  - raw/papers/valin-2018-lpcnet/full-text.md
  - raw/papers/valin-2024-fargan/full-text.md
tags:
  - neural-vocoder
  - low-complexity
  - speech-synthesis
  - real-time
  - speech-coding
  - gan
  - autoregressive
---

# Low-Complexity Neural Vocoders

> Cross-source synthesis connecting: LPCNet (Valin & Skoglund, ICASSP 2019) and FARGAN (Valin, Mustafa & Büthe, IEEE SPL 2024), with FWGAN, CARGAN and HiFi-GAN as comparison points reported within those papers.

---

## The Problem

Since WaveNet, neural vocoders have been a core building block of TTS, low-bitrate speech coding, PLC, and codec enhancement — but the vocoder is often the *most complex component* of the system. Real-time speech communications demand algorithmic delay under 20 ms and complexity compatible with continuous operation on a mobile CPU. The history of this field is a sequence of roughly 5× complexity reductions, each achieved by moving a piece of speech structure **out of the neural network** and into cheap classical DSP.

## The Complexity-Quality Frontier

All numbers are for 16 kHz, speaker-independent synthesis; GFLOPS counts one multiply-add as two FLOPS. Quality columns are as evaluated in [[sources/valin-2024-fargan|Valin et al. 2024]] (all vocoders retrained on the same 205-hour data) unless noted.

| Vocoder | Year | Mechanism | Params | GFLOPS | CPU core | Quality evidence |
|---------|------|-----------|-------:|-------:|---------:|------------------|
| WaveRNN | 2018 | Sparse-GRU density estimation | – | ~10 (est.) | – | Speaker-dependent era baseline |
| **LPCNet** | 2019 | LPC envelope + excitation density model | – | 2.8 | 4.5% (i7-8565U) | MUSHRA beats equal-complexity WaveRNN+; PESQ 2.539, MPE 5.303 in the 2024 re-evaluation |
| HiFi-GAN v3 | 2020 | Non-AR GAN, CNN | – | 2.8 | – | PESQ 2.373, MPE 6.715 — *below* FARGAN at equal complexity |
| FWGAN | 2023 | Framewise GAN, 10-ms frames | – | 1.2 | – | PESQ 2.833, MPE 5.063 |
| **FARGAN** | 2024 | Pitch-predictive AR-GAN, 2.5-ms subframes | 820k | **0.6** | **0.8%** | P.808 statistically tied with CARGAN & HiFi-GAN v1; PESQ 3.298, MPE 4.108 (best of all) |
| FARGAN small | 2024 | Same, 500k weights | 500k | 0.35 | 0.5% | Tied with LPCNet & FWGAN |
| *References* | – | CARGAN: 65.9 GFLOPS; HiFi-GAN v1: 38.1 GFLOPS | – | 65.9 / 38.1 | – | Quality *matched* by 600-MFLOPS FARGAN (110× / 64× reductions) |

The frontier's shape: quality parity with the high-complexity references was reached at **0.6 GFLOPS** in 2024, roughly 17× below the first real-time-capable autoregressive vocoder (LPCNet) and two orders of magnitude below CARGAN.

## Insights

### 1. Every 5× reduction moved structure out of the network

- **WaveRNN → LPCNet (~3.5×)**: the spectral envelope moved to an all-pole LPC filter derived from the conditioning cepstrum; the network models only the spectrally flat excitation. ([[concepts/linear-prediction|Linear prediction]] as the classical workhorse.)
- **LPCNet → FWGAN → FARGAN (~5×)**: first the training paradigm (density estimation → adversarial), then *periodicity itself* moved out — FARGAN's [[concepts/pitch-prediction|pitch prediction]] hands the network the signal from one period back, so the generator only models the aperiodic residual, exactly as CELP's adaptive codebook offloads periodicity.

This is the same hybrid DSP/DNN philosophy as [[concepts/percepnet|PercepNet]] on the enhancement side: classical DSP carries what classical DSP models well (envelope, periodicity), and the network spends its capacity on what has no simple model (excitation detail).

### 2. The training-paradigm shift was the enabler, not the FLOP count

Autoregressive density estimation structurally requires [[concepts/exposure-bias|teacher forcing]] and precludes adversarial losses. FARGAN's framewise generation (one pass per 2.5-ms subframe, model unrolled during training) is what let an *autoregressive* model be trained as a GAN — combining CARGAN's pitch/phase inductive bias with GAN losses. Notably, the FARGAN authors report that direct pitch prediction could not be added to LPCNet under teacher forcing: the mechanism is only viable once training-time feedback comes from the synthesized signal.

### 3. The feature representation outlived the architectures

The 20-dimensional conditioning vector — 18 [[concepts/bark-scale-spectral-features|Bark-scale cepstral coefficients]] + pitch period (+ correlation in LPCNet, voicing indicator in FARGAN) — is unchanged from LPCNet (2019) through the 2022 PLC system to FARGAN (2024), across a complete change of synthesizer architecture and training objective. It is the stable interface of this vocoder family, and the natural "feature space" in which predictive models (e.g., the PLC feature-prediction RNN) can be built around the vocoder.

### 4. Model size and quantization are first-class constraints

FARGAN treats FLOPS as only half the story: 8-bit weights *and* activations (bounded tanh/sigmoid, gain normalization, pre-emphasized domain) give 4× more ops per SIMD vector length, and sub-1 MB weight storage fits the L2 cache — cache residency, not arithmetic, is the binding constraint on mobile CPUs. This axis is invisible in GFLOPS tables and matters for any embedded neural-audio deployment (compare BBWENet's ~140 MFLOPS / 370k params on the enhancement side).

### 5. Objective metrics disagree at the frontier

PESQ and WARP-Q rank FARGAN, HiFi-GAN v1 and CARGAN in *opposite* orders — comparing very different algorithm families objectively "is a notoriously difficult task" (Valin et al. 2024). Subjective P.808 testing remains the arbiter at the quality ceiling; MPE (mean pitch error) is the most discriminating objective proxy for vocoder quality in this comparison set.

### 6. The frontier is deployed

LPCNet shipped in Opus (2022 PLC / DRED redundancy); FARGAN replaced it in **Opus 1.5**, cutting DRED synthesis complexity 5×. The complexity-quality frontier of this table is not academic — it is live codec infrastructure.

## Gaps and Open Questions

- **FWGAN, CARGAN, HiFi-GAN not yet ingested as sources** — their numbers above come from the FARGAN paper's re-evaluation. Ingesting Mustafa et al. 2023 (FWGAN) would add the framewise-GAN origin story and its 10-ms design point.
- **Generalization ceiling**: pitch prediction presumes a single periodic source — FARGAN cannot synthesize music. A universal low-complexity vocoder remains open.
- **Wideband/full-band extension**: all frontier entries are 16 kHz; extending to 48 kHz (as BBWENet does for enhancement) is unexplored here.
- **Quality ceiling**: FARGAN ties HiFi-GAN v1 but does not beat it; whether sub-GFLOPS vocoders can *exceed* high-complexity quality is untested.

## Related Concepts

- [[concepts/lpcnet|LPCNet]] — envelope-offloading vocoder (2019 frontier point)
- [[concepts/fargan|FARGAN]] — pitch-predictive AR-GAN vocoder (2024 frontier point)
- [[concepts/pitch-prediction|Pitch Prediction]] — the mechanism behind the latest reduction
- [[concepts/exposure-bias|Teacher Forcing and Exposure Bias]] — the training-paradigm constraint that shaped the lineage
- [[concepts/wavernn|WaveRNN]] — the density-estimation starting point
- [[concepts/linear-prediction|Linear Prediction]] — the classical structure reused by LPCNet
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]] — the stable conditioning interface

## Related Sources

- [[sources/valin-2018-lpcnet|Valin & Skoglund 2018: LPCNet]]
- [[sources/valin-2024-fargan|Valin, Mustafa & Büthe 2024: FARGAN]]
