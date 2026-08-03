---
type: source
created: 2026-08-03
updated: 2026-08-03
sources:
  - raw/papers/chao-2024-mamba-speech-enhancement/full-text.md
  - https://doi.org/10.1109/SLT61566.2024.10832332
  - zotero://select/items/0_KTXM4766
tags:
  - speech-enhancement
  - state-space-model
  - mamba
  - selective-ssm
  - spectral-mapping
  - benchmark
---

# Chao, Cheng, La Quatra, Siniscalchi, Yang, Fu & Tsao 2024: An Investigation of Incorporating Mamba for Speech Enhancement

- **Authors**: [[entities/rong-chao|Rong Chao]], [[entities/wen-huang-cheng|Wen-Huang Cheng]], [[entities/moreno-la-quatra|Moreno La Quatra]], [[entities/sabato-marco-siniscalchi|Sabato Marco Siniscalchi]], [[entities/chao-han-huck-yang|Chao-Han Huck Yang]], [[entities/szu-wei-fu|Szu-Wei Fu]], [[entities/yu-tsao|Yu Tsao]]
- **Venue**: IEEE Spoken Language Technology Workshop (SLT) 2024
- **Year**: 2024
- **Type**: Conference paper
- **DOI**: [10.1109/SLT61566.2024.10832332](https://doi.org/10.1109/SLT61566.2024.10832332)
- **arXiv**: [2405.06573](https://arxiv.org/abs/2405.06573)
- **Zotero**: [KTXM4766](zotero://select/items/0_KTXM4766)

## Summary

This is the **first work to apply Mamba** — a selective state-space model (SSM) with input-dependent gating and linear-time scaling — to speech enhancement (SE). The authors propose **SEMamba**, a regression-based SE family deployed in both a basic (magnitude-mapping) and an advanced (magnitude-phase, MP-SENet-style) configuration, with causal/non-causal and uni-/bi-directional variants. On the VoiceBank-DEMAND benchmark, the advanced non-causal SEMamba reaches **PESQ 3.55**, competitive with the Conformer-based MP-SENet at ~12% lower FLOPs; combined with Perceptual Contrast Stretching (PCS), SEMamba sets a **new state-of-the-art PESQ of 3.69**. As a Whisper ASR front-end, SEMamba yields 12.22% / 12.90% relative WER reductions on Whisper-Base / Whisper-LargeV3.

## Problem Formulation

Speech enhancement is framed as a **regression task**: a neural-network mapping function $f_\theta$ converts a noisy waveform $y$ into an enhanced waveform $\hat{x} \approx x$ (the clean reference). The paper investigates whether the recently proposed [[concepts/mamba|Mamba]] selective SSM — which scales linearly in sequence length and has an input-dependent selection mechanism — can replace the Transformer/Conformer block inside this mapping function while matching or exceeding quality at lower computational cost.

Two configurations are studied:

1. **Basic** — magnitude-only mapping: input noisy waveform $\xrightarrow{\text{STFT}}$ magnitude $\xrightarrow{\log1p}$ compressed magnitude $\xrightarrow{\text{SE module}}$ enhanced magnitude $\xrightarrow{\log1p^{-1}}$ de-compressed $\xrightarrow{\text{iSTFT with noisy phase}}$ enhanced waveform.
2. **Advanced** — magnitude-and-phase mapping built on the [[concepts/mp-senet|MP-SENet]] backbone, predicting both magnitude and phase spectra.

## Methodology

### SEMamba-basic

A causal magnitude-mapping architecture:

- **Encoder**: 4 convolutional layers
- **Sequence model**: two **uni-directional Mamba blocks** (replacing the Transformer blocks of the baseline in [36])
- **Decoder**: a fully connected layer
- **Loss**: mean absolute error of the magnitude (L1)

The noisy phase is reused at the iSTFT stage to reconstruct the waveform.

![[raw/papers/chao-2024-mamba-speech-enhancement/figures/fig1.png|SEMamba-basic architecture]]

*Figure 1: Architecture of the basic Mamba-based Speech Enhancement (SE) model, SEMamba-basic.*

### SEMamba-advanced

A non-causal magnitude-and-phase architecture built on [[concepts/mp-senet|MP-SENet]]:

- **Feature encoder**: dilated DenseNet flanked by two conv layers; input is the stacked compressed magnitude + phase
- **TF-Mamba block**: a Time-Frequency Mamba block, repeated $N=4$ times, replacing MP-SENet's Conformer/attention-based TF block
- **Two decoders**: separate magnitude and phase decoders, each = dilated DenseNet + deconvolution + 2D-conv output layer
- **Loss**: linear combination of PESQ-based GAN discriminator loss + time loss + magnitude loss + complex loss + phase loss (as in MP-SENet)

![[raw/papers/chao-2024-mamba-speech-enhancement/figures/fig2.png|SEMamba-advanced architecture]]

*Figure 2: Architecture of the proposed SEMamba-advanced with Time-Frequency (TF) and Selective-SSM mechanism.*

### Additional design choices

**Bi-directional Mamba.** The Mamba module is run on both the original and the time-reversed sequence in parallel; outputs are concatenated and fused by a `Conv1D`:

$$\mathbf{y} = Conv1D\big(M_{uni}(\mathbf{x}) \oplus flip(M_{uni}(flip(\mathbf{x})))\big)$$

This bidirectional variant is the default for the advanced configuration.

**Consistency loss (CL).** Minimizes the gap between the complex spectrum predicted directly by the model and the spectrum obtained by re-applying STFT after iSTFT of the model output — pulling the predicted spectrum back into the valid STFT domain. (Adapted from [37].)

**Perceptual Contrast Stretching (PCS).** An auxiliary post-enhancement spectral step that stretches the magnitude spectrum according to the perceptual importance of each frequency band, exploiting the human auditory system's varying sensitivity. PCS alone turns a PESQ of 3.55 into the SOTA **3.69**.

### The Mamba block

The structured state-space recurrence used by each Mamba block maps an input $x_n$ to an output $y_n$ through a latent state $h_n$:

$$h_n = \bar{\mathbf{A}}\, h_{n-1} + \bar{\mathbf{B}}\, x_n, \qquad y_n = \mathbf{C}\, h_n$$

where $(\bar{\mathbf{A}}, \bar{\mathbf{B}})$ are the discretized counterparts of the continuous parameters $(\Delta, \mathbf{A}, \mathbf{B})$. Mamba's two key advances over prior structured SSMs are: (i) an **input-dependent selection mechanism** that parameterizes the SSM from the input, enabling content-based filtering; and (ii) a **hardware-aware scan algorithm** that scales linearly in sequence length. See [[concepts/mamba|Mamba]] for the full architecture.

## Experimental Setup

| Item | Value |
|------|-------|
| **Dataset** | [[concepts/voicebank-demand|VoiceBank-DEMAND]] — 11,572 train / 824 test utterances, 30 speakers (28 train / 2 test) |
| **Sample rate** | 16 kHz (downsampled from 48 kHz) |
| **Train SNRs** | 0, 5, 10, 15 dB |
| **Test SNRs** | 2.5, 7.5, 12.5, 17.5 dB |
| **Metrics** | WB-PESQ, CSIG, CBAK, COVL, [[concepts/pesq|STOI]] |
| **Basic backbone** | 4-layer conv encoder + 2 Mamba blocks + FC decoder |
| **Advanced backbone** | MP-SENet with TF-Mamba block ($N=4$) replacing Conformer |
| **Basic loss** | L1 on magnitude |
| **Advanced loss** | PESQ-GAN + time + magnitude + complex + phase |
| **ASR front-end test** | Whisper-Base, Whisper-LargeV3 |

## Results

### Table 1 — Basic SE architecture: Mamba vs. Transformer

| Config | Causal | PESQ | STOI | FLOPs | Params |
|--------|--------|------|------|-------|--------|
| noisy | – | 1.97 | 0.92 | – | – |
| Transformer [36] | Yes | 2.76 | 0.94 | 2.26 G | 9.05 M |
| **Mamba** | Yes | 2.76 | 0.94 | **0.76 G** | **3.60 M** |
| Transformer [36] | No | 2.84 | 0.94 | 2.26 G | 9.05 M |
| **Mamba** | No | 2.85 | 0.94 | **1.06 G** | **6.49 M** |

Mamba matches Transformer quality while cutting FLOPs by **66.4%** (causal) / **53.1%** (non-causal) and parameters by **60.2%** / **28.3%**.

### Table 2 — Advanced SE architecture: Mamba vs. Conformer (no CL, no PCS)

| Core | PESQ | STOI | FLOPs | Params |
|------|------|------|-------|--------|
| noisy | 1.97 | 0.92 | – | – |
| Conformer | 3.50 | 0.96 | 74.29 G | 2.05 M |
| Mamba (Uni) | 3.29 | 0.95 | 53.09 G | 1.41 M |
| **Mamba (Bi)** | **3.52** | 0.96 | **65.46 G** | 2.26 M |

Bidirectional Mamba slightly exceeds Conformer PESQ at **11.9% fewer FLOPs** (65.46 G vs. 74.29 G).

### Table 3 — VoiceBank-DEMAND benchmark vs. prior SE systems

| Model | PESQ | CSIG | CBAK | COVL | STOI |
|-------|------|------|------|------|------|
| noisy | 1.97 | 3.35 | 2.44 | 2.63 | 0.92 |
| SEGAN | 2.16 | 3.48 | 2.94 | 2.80 | – |
| MetricGAN+ | 3.15 | 4.14 | 3.16 | 3.64 | 0.93 |
| DPT | 3.33 | 4.58 | 3.72 | 4.00 | 0.96 |
| CMGAN | 3.41 | 4.63 | 3.94 | 4.12 | 0.96 |
| MP-SENet | 3.50 | 4.73 | 3.95 | 4.22 | 0.96 |
| S4DSE | 2.55 | 3.94 | 3.00 | 3.23 | 0.93 |
| S4ND-UNet | 3.15 | 4.52 | 3.62 | 3.85 | – |
| Spiking-S4 | 3.39 | 4.92 | 2.64 | 4.31 | – |
| SEMamba (-CL) | 3.52 | 4.75 | 3.98 | 4.26 | 0.96 |
| **SEMamba** | **3.55** | 4.77 | 3.95 | 4.29 | 0.96 |
| **SEMamba (+PCS)** | **3.69** | 4.79 | 3.63 | 4.37 | 0.96 |

SEMamba(+PCS) sets a **new SOTA PESQ of 3.69** on VoiceBank-DEMAND. Note the CBAK drop with PCS (3.95 → 3.63) — PCS trades background-intrusiveness for perceptual quality.

### ASR front-end results

![[raw/papers/chao-2024-mamba-speech-enhancement/figures/fig3.png|WER comparison]]

*Figure 3: Comparative WERs for SEMamba and related models on VoiceBank-DEMAND with Whisper ASR.*

| ASR model | Noisy | MetricGAN+ | MP-SENet | **SEMamba** |
|-----------|-------|------------|----------|-------------|
| Whisper-Base | 9.0% | – | higher | **7.9%** (−12.22% rel.) |
| Whisper-LargeV3 | 3.1% | – | higher | **2.7%** (−12.90% rel.) |

## Key Contributions

1. **First application of Mamba to speech enhancement** — proposes SEMamba, a regression-based SE family that uses the selective SSM as the core sequence model in place of Transformer/Conformer.
2. **Basic + advanced configurations** — demonstrates Mamba in both a simple magnitude-mapping setup (4-layer conv encoder + 2 Mamba blocks) and an advanced MP-SENet-style magnitude-phase setup with a Time-Frequency Mamba block.
3. **Causal/non-causal and uni-/bi-directional variants** — systematically evaluates all four combinations and shows the bi-directional non-causal variant is best for offline SE.
4. **FLOPs reduction at parity quality** — in the basic architecture Mamba cuts FLOPs by 53–66% and parameters by 28–60% vs. Transformer at the same PESQ; in the advanced architecture Mamba cuts FLOPs by ~12% vs. Conformer while slightly exceeding PESQ.
5. **New SOTA PESQ 3.69 on VoiceBank-DEMAND** — by combining SEMamba with Perceptual Contrast Stretching (PCS), establishing the best reported PESQ on this benchmark at the time.
6. **Effective ASR front-end** — SEMamba-advanced as a pre-processor for Whisper-Base / Whisper-LargeV3 yields 12.22% / 12.90% relative WER reductions.

## Related Concepts

- [[concepts/mamba|Mamba]] — the selective state-space model used as the core block
- [[concepts/semamba|SEMamba]] — the proposed SE system (this paper)
- [[concepts/state-space-model|State-Space Model]] — broader SSM family, including the deep-learning subfamily
- [[concepts/s4nd|S4ND]] — earlier structured SSM applied to SE (S4ND-UNet baseline)
- [[concepts/mamba-mingru|Mamba-MinGRU]] — later hybrid Mamba + linear-RNN architecture for own-voice cancellation
- [[concepts/mp-senet|MP-SENet]] — the advanced backbone that SEMamba-advanced adapts
- [[concepts/perceptual-contrast-stretching|Perceptual Contrast Stretching (PCS)]] — auxiliary post-processing that lifts PESQ to 3.69
- [[concepts/voicebank-demand|VoiceBank-DEMAND]] — the SE benchmark
- [[concepts/pesq|PESQ]] — the primary evaluation metric
- [[concepts/speech-enhancement|Speech Enhancement]] — the task

## Related Synthesis

- [[synthesis/computational-efficiency-evolution|Computational Efficiency in ANC and SE]] — Mamba/SSM as the linear-time sequence-modeling axis replacing quadratic-attention Transformers
