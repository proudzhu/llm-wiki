---
type: concept
created: 2026-08-03
updated: 2026-08-03
sources:
  - raw/papers/chao-2024-mamba-speech-enhancement/full-text.md
tags:
  - neural-network
  - speech-enhancement
  - state-space-model
  - mamba
  - spectral-mapping
  - benchmark
---

# SEMamba

**SEMamba** is a regression-based speech enhancement (SE) system proposed by Chao et al. (IEEE SLT 2024) that uses [[concepts/mamba|Mamba]] — a selective state-space model — as the core sequence-modeling block in place of Transformer/Conformer. It is the **first application of Mamba to speech enhancement**. SEMamba is deployed in two configurations — *basic* (magnitude-mapping, causal) and *advanced* (magnitude-and-phase, non-causal, built on [[concepts/mp-senet|MP-SENet]]) — and combines uni-/bi-directional Mamba variants with optional consistency loss and [[concepts/perceptual-contrast-stretching|Perceptual Contrast Stretching (PCS)]]. On the [[concepts/voicebank-demand|VoiceBank-DEMAND]] benchmark, SEMamba with PCS achieves a **state-of-the-art PESQ of 3.69**.

## Architecture

### SEMamba-basic (causal, magnitude-only)

A simple magnitude-mapping pipeline:

- **STFT** on the noisy waveform
- **Magnitude compression** with $log1p(z) = \log(1+z)$
- **Encoder**: 4-layer convolutional encoder
- **Mamba blocks**: 2 uni-directional [[concepts/mamba|Mamba]] blocks (replacing the Transformer blocks of the baseline)
- **Decoder**: a fully connected layer
- **Decompression**: $\exp(\cdot) - 1$
- **iSTFT** with the **noisy phase** reused to reconstruct the waveform
- **Loss**: L1 (mean absolute error) on the magnitude

### SEMamba-advanced (non-causal, magnitude-and-phase)

Built on the [[concepts/mp-senet|MP-SENet]] backbone:

- **STFT** on the noisy waveform; the compressed magnitude is **stacked with the phase**
- **Feature encoder**: a dilated DenseNet flanked by two convolutional layers
- **Time-Frequency (TF) Mamba block**: replaces MP-SENet's Conformer-based TF block; repeated $N=4$ times
- **Two decoders** (one for magnitude, one for phase): each = dilated DenseNet + deconvolution + 2D-conv output layer
- **Loss**: linear combination of PESQ-based GAN discriminator loss + time loss + magnitude loss + complex loss + phase loss (as in MP-SENet)

### Bi-directional Mamba

The advanced configuration runs the Mamba module on both the original and the time-reversed sequence in parallel, then concatenates and fuses with `Conv1D`:

$$\mathbf{y} = Conv1D\big(M_{uni}(\mathbf{x}) \oplus flip(M_{uni}(flip(\mathbf{x})))\big)$$

This bidirectional variant is the default for SEMamba-advanced and is the best-performing configuration.

### Optional add-ons

- **Consistency loss (CL)** — minimizes the gap between the model's direct complex-spectrum output and the spectrum obtained by re-applying STFT after iSTFT, pulling the prediction back into the valid STFT domain.
- **[[concepts/perceptual-contrast-stretching|Perceptual Contrast Stretching (PCS)]]** — a post-enhancement step that stretches the magnitude spectrum according to the perceptual importance of each frequency band. PCS alone lifts PESQ from 3.55 to the SOTA **3.69**.

## Results

### Basic architecture — Mamba vs. Transformer

| Config | Causal | PESQ | STOI | FLOPs | Params |
|--------|--------|------|------|-------|--------|
| Transformer | Yes | 2.76 | 0.94 | 2.26 G | 9.05 M |
| Mamba | Yes | 2.76 | 0.94 | 0.76 G | 3.60 M |
| Transformer | No | 2.84 | 0.94 | 2.26 G | 9.05 M |
| Mamba | No | 2.85 | 0.94 | 1.06 G | 6.49 M |

Mamba matches Transformer quality while cutting FLOPs by 53–66% and parameters by 28–60%.

### Advanced architecture — Mamba vs. Conformer

| Core | PESQ | STOI | FLOPs | Params |
|------|------|------|-------|--------|
| Conformer | 3.50 | 0.96 | 74.29 G | 2.05 M |
| Mamba (Uni) | 3.29 | 0.95 | 53.09 G | 1.41 M |
| Mamba (Bi) | 3.52 | 0.96 | 65.46 G | 2.26 M |

Bidirectional Mamba slightly exceeds Conformer PESQ at 11.9% fewer FLOPs.

### VoiceBank-DEMAND benchmark

| Model | PESQ | CSIG | CBAK | COVL | STOI |
|-------|------|------|------|------|------|
| MP-SENet | 3.50 | 4.73 | 3.95 | 4.22 | 0.96 |
| SEMamba (no CL) | 3.52 | 4.75 | 3.98 | 4.26 | 0.96 |
| SEMamba | 3.55 | 4.77 | 3.95 | 4.29 | 0.96 |
| **SEMamba (+PCS)** | **3.69** | 4.79 | 3.63 | 4.37 | 0.96 |

### ASR front-end

When used as a pre-processor for Whisper ASR on the VoiceBank-DEMAND test set:

| ASR model | Noisy WER | SEMamba WER | Relative reduction |
|-----------|-----------|-------------|--------------------|
| Whisper-Base | 9.0% | 7.9% | 12.22% |
| Whisper-LargeV3 | 3.1% | 2.7% | 12.90% |

## Key Properties

| Property | Value |
|----------|-------|
| Sequence model | [[concepts/mamba|Mamba]] (selective SSM) |
| Domain | STFT (magnitude-only / magnitude-and-phase) |
| Causality | Basic: causal; Advanced: non-causal |
| Directionality | Uni or Bi (Bi is default for advanced) |
| SOTA result | PESQ 3.69 on VoiceBank-DEMAND (with PCS) |
| FLOPs reduction | 53–66% vs. Transformer (basic); ~12% vs. Conformer (advanced) |

## Related Concepts

- [[concepts/mamba|Mamba]] — the core selective SSM block
- [[concepts/mp-senet|MP-SENet]] — the advanced backbone that SEMamba-advanced adapts
- [[concepts/perceptual-contrast-stretching|Perceptual Contrast Stretching (PCS)]] — post-processing that lifts PESQ to 3.69
- [[concepts/state-space-model|State-Space Model]] — broader SSM family
- [[concepts/s4nd|S4ND]] — earlier structured SSM applied to SE (S4ND-UNet baseline)
- [[concepts/mamba-mingru|Mamba-MinGRU]] — later hybrid Mamba architecture for own-voice cancellation
- [[concepts/voicebank-demand|VoiceBank-DEMAND]] — the SE benchmark
- [[concepts/pesq|PESQ]] — the primary evaluation metric
- [[concepts/speech-enhancement|Speech Enhancement]] — the task

## Related Sources

- [[sources/chao-2024-mamba-speech-enhancement|Chao et al. 2024: An Investigation of Incorporating Mamba for Speech Enhancement]]
