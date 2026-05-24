---
type: source
created: 2026-05-20
updated: 2026-05-20
sources:
  - raw/papers/feng-2025-directional-source-separation-smart-glasses/full-text.md
  - https://arxiv.org/abs/2309.10993
  - https://doi.org/10.1109/ICASSP49660.2025.10888256
  - zotero://select/items/0_3DZ5NNH3
tags:
  - source-separation
  - beamforming
  - smart-glasses
  - neural-beamforming
  - asr
  - nlcvm
tags:
  - source-separation
  - beamforming
  - smart-glasses
  - neural-beamforming
  - asr
  - nlcvm
aliases:
  - Feng et al. 2025: Directional Source Separation for Smart Glasses
---

# Feng et al. 2025: Directional Source Separation for Robust Speech Recognition on Smart Glasses

**Authors**: Tiantian Feng, Ju Lin, Yiteng Huang, Weipeng He, Kaustubh Kalgaonkar, Niko Moritz, Li Wan, Xin Lei, Ming Sun, Frank Seide
**Institutions**: University of Southern California (Feng); Meta Platforms, Inc. (all others)
**Published**: ICASSP 2025, pp. 1–5
**DOI**: [10.1109/ICASSP49660.2025.10888256](https://doi.org/10.1109/ICASSP49660.2025.10888256)
**arXiv**: [2309.10993](https://arxiv.org/abs/2309.10993)
**📎 Zotero**: [zotero://select/items/0_3DZ5NNH3](zotero://select/items/0_3DZ5NNH3)

## Summary

Investigates **directional source separation** on the multi-microphone Project Aria smart glasses for robust ASR. The system combines a **beamforming front-end** (NLCMV with $K$ steering directions) with a **source separation back-end** (encoder-decoder with GLU + LSTM). Shows that:
- Neural beamforming (learned via backprop) significantly outperforms predetermined beamforming (+2.27 dB SI-SDR for wearer)
- Source separation benefits wearer ASR (6.51% WER) but degrades partner ASR
- **Joint training** of separation + ASR achieves best overall WER (13.25%), balancing both speakers

## Methodology

![[raw/papers/feng-2025-directional-source-separation-smart-glasses/figures/fig2.png|System architecture: beamforming front-end + source separation back-end]]
*Figure 1: Proposed directional source separation architecture. 7-ch audio → NLCMV beamformers (K steering directions + mouth direction) → encoder-decoder separation network.*

### Beamforming Front-end

Uses **NLCMV** (Non-Linearly Constrained Minimum Variance) as the predetermined beamformer. Multiple beamformers preprocess raw 7-channel audio into $K$ horizontal steering directions plus one mouth direction:

- **BF-5**: $K=4$ + mouth → 5 beamformed channels
- **BF-13**: $K=12$ + mouth → 13 beamformed channels
- **Neural BF-13**: Same structure but beamformer weights are fine-tuned via backprop during training

NLCMV minimizes output power subject to:
- **Linear equalities**: $\mathbf{h}^H(j\omega) \cdot \mathbf{g}_n(j\omega) = 1$ (target-preserving)
- **Nonlinear inequality**: $c(\omega) = \mathbf{h}^H(j\omega) \boldsymbol{\Psi}(j\omega) \mathbf{h}(j\omega) \leq 0$ (WNG constraint)

### Source Separation Back-end

Encoder-decoder architecture:
1. STFT features extracted from $K+1$ beamformed channels
2. **Encoder**: Multiple convolutional blocks with GLU activation + Dropout
3. **3-layer LSTM** for sequence modeling
4. **Decoder**: Convolutional decoding layers
5. **Gating**: Computes STFT masks for wearer (SELF) and partner (PARTNER) from reference audio
6. Loss: L1 + STFT + Log SI-SDR

### ASR Modeling

Two configurations:
- **Two-stage ASR**: Pre-trained separation → log-mel → Neural Transducer (RNN-T with SOT)
- **Two-stage Fusion**: Combines separation outputs with beamformed channels ($K+3$ input)
- **Joint Training**: Pre-trained separation + ASR fine-tuned together with combined loss (equal weights)

## Experimental Setup

**Dataset**: LibriSpeech (960h), simulated with 100k RIRs using Project Aria 7-channel geometry via image-source method

**Test Scenarios**: Varying bystanders (1–3), SNR (−8 to 40 dB), overlap ratios (5%–50%)

**Separation Training**: 60 epochs, Adam, lr=4e-4, 10k warmup, tri-stage scheduler

**ASR Training**: 120 epochs (separate); 30 epochs (joint), lr=1e-4, equal loss weights

## Key Results

### Source Separation Quality

| System | PESQ (Wearer / Partner) | SI-SDR (Wearer / Partner) |
|--------|------------------------|---------------------------|
| Without BF (7-ch raw) | 2.89 / 1.80 | 18.17 / 8.50 |
| BF-5 | 2.88 / 1.82 | 18.09 / 8.55 |
| BF-13 | 2.95 / 1.86 | 18.33 / 8.83 |
| **Neural BF-13** | **3.11 / 1.89** | **20.44 / 9.51** |

Neural BF-13 provides **+2.27 dB** SI-SDR gain for wearer and **+1.01 dB** for partner over the no-BF baseline.

### ASR Performance (1 bystander)

| System | Overall WER | Wearer WER | Partner WER |
|--------|------------|-----------|------------|
| Directional ASR (BF-13) | 14.14% | 8.28% | 20.12% |
| Two-stage (Neural BF-13) | 16.04% | **6.51%** | 25.46% |
| Two-stage Fusion (Neural BF-13) | 13.70% | 6.65% | 20.66% |
| **Joint Training Fusion (Neural BF-13)** | **13.25%** | 8.06% | **18.89%** |

Key findings:
- Source separation alone **benefits wearer** (6.51% vs 8.28%) but **hurts partner** (25.46% vs 20.12%)
- **Fusion** (combining separation + beamformed outputs) recovers partner performance
- **Joint training** achieves best overall (13.25%) and partner (18.89%) WER — striking a balance between speakers
- Neural BF-13 is more robust to increasing bystanders than predetermined beamformers

## Key Contributions

1. First comprehensive study of **directional source separation** on smart glasses with 7-channel microphone array
2. Demonstrates **neural beamforming** in source separation — learning beamformer weights via backprop yields +2.27 dB SI-SDR improvement
3. Quantifies the **wearer vs. partner ASR trade-off**: separation helps wearer but hurts far-field partner
4. **Joint training** of separation + ASR achieves best overall WER (13.25%), balancing both speakers
5. Beam pattern analysis reveals neural beamforming learns strong lateral suppression (~10 dB gain in side directions)

## Related Concepts

- [[concepts/beamforming|Beamforming]]
- [[concepts/nlcmv-beamforming|NLCMV Beamforming]]
- [[concepts/neural-beamforming|Neural Beamforming]]
- [[concepts/auditory-augmented-reality|Auditory Augmented Reality]]
- [[concepts/roi-beamforming|Region-of-Interest Beamforming]]

## Related Entities

- [[entities/tiantian-feng|Tiantian Feng]]
- [[entities/ju-lin|Ju Lin]]
- [[entities/yiteng-huang|Yiteng Huang]]
- [[entities/weipeng-he|Weipeng He]]
- [[entities/kaustubh-kalgaonkar|Kaustubh Kalgaonkar]]
- [[entities/niko-moritz|Niko Moritz]]
- [[entities/li-wan|Li Wan]]
- [[entities/xin-lei|Xin Lei]]
- [[entities/ming-sun|Ming Sun]]
- [[entities/frank-seide|Frank Seide]]
