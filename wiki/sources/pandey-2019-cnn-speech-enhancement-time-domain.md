---
type: source
created: 2026-05-23
updated: 2026-05-23
sources:
  - raw/papers/pandey-2019-cnn-speech-enhancement-time-domain/full-text.txt
  - https://doi.org/10.1109/TASLP.2019.2913512
  - zotero://select/items/0_35DQRHLV
tags:
  - speech-enhancement
  - time-domain
  - convolutional-neural-network
  - frequency-domain-loss
  - deep-learning
---

# Pandey & Wang 2019: A New Framework for CNN-Based Speech Enhancement in the Time Domain

| Field | Value |
|:------|:------|
| **Authors** | [[entities/ashutosh-pandey\|Ashutosh Pandey]], [[entities/deliang-wang\|DeLiang Wang]] |
| **Institution** | Ohio State University |
| **Venue** | IEEE/ACM Trans. Audio, Speech, and Language Processing |
| **Year** | 2019 |
| **Volume/Pages** | Vol. 27, No. 7, pp. 1179-1188 |
| **Type** | Journal article |
| **DOI** | [10.1109/TASLP.2019.2913512](https://doi.org/10.1109/TASLP.2019.2913512) |
| **Zotero** | [35DQRHLV](zotero://select/items/0_35DQRHLV) |

## Summary

Proposes a fully convolutional autoencoder network (AECNN) that operates in the **time domain** but is trained with a **frequency domain loss** — specifically the MAE between estimated and clean STFT magnitudes. This framework avoids the [[concepts/invalid-stft-problem|invalid STFT problem]] inherent to frequency-domain methods that combine enhanced magnitude with noisy phase. The time-to-frequency conversion is a simple differentiable DFT matrix multiplication, enabling end-to-end training. Results show substantial improvements over SEGAN and GRN baselines across TIMIT, IEEE, and WSJ0 SI-84 datasets.

## Problem Statement

Conventional DNN-based speech enhancement operates in the frequency domain via T-F masking or spectral mapping, then reconstructs time-domain signals using the noisy phase. This suffers from two issues:

1. **Invalid STFT problem**: Combining enhanced magnitude with noisy phase may not correspond to a valid STFT, causing signal distortions
2. **Phase information loss**: The noisy phase is suboptimal but not improved by the learning process

The proposed framework resolves both by working in the time domain (always producing valid signals) while training with a frequency-domain loss (leveraging spectral structure for better optimisation).

## Methodology

### Frequency Domain Loss

Given time-domain output $\mathbf{x}_t$ of size $N$, the DFT is computed via matrix multiplication:

$$\mathbf{x}_f = \mathbf{D}\mathbf{x}_t = (\mathbf{D}_r + i\mathbf{D}_i)\mathbf{x}_t$$

The proposed loss is the MAE on STFT magnitudes (L1 norm):

$$\mathcal{L} = \frac{1}{N}\sum_{n=1}^{N} \left| \left(|x_{fr}(n)| + |x_{fi}(n)|\right) - \left(|\hat{x}_{fr}(n)| + |\hat{x}_{fi}(n)|\right) \right|$$

This is differentiable and propagates gradients back through the time-domain network.

### Model Architecture (AECNN)

A U-Net-style fully convolutional network adopted from SEGAN:

- **Encoder**: 9 convolutional layers with stride-2 downsampling (1 → 64 → 256 channels, 2048 → 8 samples)
- **Decoder**: 8 deconvolutional layers mirroring the encoder with skip connections
- **Activation**: Parametric ReLU (except Tanh at output)
- **Dropout**: 0.2 at every 3 layers
- **Parameters**: ~6.4M (vs. SEGAN's ~58M)
- **Frame size**: 2048 samples (128 ms) for TIMIT/IEEE; 16384 samples (1024 ms) for WSJ0

### Loss Function Variants

| Name | Loss domain | Phase used | Performance |
|:-----|:------------|:-----------|:------------|
| AECNN-T | Time (MAE/MSE on samples) | Implicit | Low PESQ |
| AECNN-RI | Frequency (real + imaginary) | Explicit | Best SI-SDR |
| **AECNN-SM1** | **Frequency (STFT magnitude, L1)** | **None** | **Best STOI + PESQ** |
| AECNN-SM2 | Frequency (STFT magnitude, L2) | None | Similar to SM1 |

## Experimental Setup

| Parameter | Value |
|:----------|:------|
| Datasets | TIMIT, IEEE, WSJ0 SI-84 |
| Sampling rate | 16 kHz |
| Frame size | 2048 (TIMIT/IEEE), 16384 (WSJ0) |
| Frame shift | 256 samples (OLA) |
| STFT analysis window | 512 samples, Hamming |
| Filter size | 11 |
| Optimiser | Adam, lr=0.0002, batch=4 |
| Training SNRs | -5, 0 dB (TIMIT); -2 dB (IEEE); -5 to -1 dB (WSJ0) |
| Evaluation SNRs | -5, 0, 5 dB |
| Metrics | STOI, PESQ, SI-SDR |

## Results

### TIMIT (noise-dependent, average over 5 noises)

| Model | STOI (-5 dB) | PESQ (-5 dB) | SI-SDR (-5 dB) |
|:------|:-------------|:-------------|:---------------|
| DNN-IRM | 0.71 | 1.53 | 3.0 |
| SEGAN | 0.70 | 1.37 | 1.2 |
| AECNN-T (MSE) | 0.75 | 1.59 | 4.5 |
| AECNN-RI (MSE) | 0.75 | 1.57 | **5.8** |
| **AECNN-SM1 (MAE)** | **0.78** | **1.74** | 5.1 |

### WSJ0 SI-84 (speaker- and noise-independent)

| Model | STOI (-5 dB) | PESQ (-5 dB) |
|:------|:-------------|:-------------|
| GRN (62-layer) | 0.76 | 1.60 |
| **AECNN-SM1** | **0.78** | **1.72** |

### Phase Analysis

- Learned phase consistently outperforms noisy phase
- Clean phase still superior → room for future improvement
- STFT magnitude loss does not explicitly train phase, yet the network implicitly learns phase structure

## Key Contributions

1. **Time-domain CNN with frequency-domain loss**: Novel training framework that operates in time domain but optimises spectral magnitude, avoiding invalid STFT
2. **STFT magnitude MAE (AECNN-SM1)**: Best loss function for joint STOI/PESQ improvement; magnitude has clearer structure than real/imaginary parts
3. **Implicit phase learning**: Network learns phase structure superior to noisy phase without explicit phase supervision
4. **Efficient architecture**: 6.4M parameters (vs. 58M for SEGAN) with superior performance

## Important Distinctions

- **vs. [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]**: CSM operates in frequency domain predicting both real and imaginary components; AECNN operates in time domain and uses frequency loss only for training
- **vs. SEGAN**: Same U-Net architecture but much smaller (6.4M vs. 58M params), uses frequency loss instead of adversarial loss
- **vs. TasNet/Conv-TasNet**: TasNet uses SI-SNR loss in time domain; AECNN uses frequency-domain magnitude loss for better perceptual quality

## Influence

This paper established the paradigm of **time-domain processing with frequency-domain loss** that became widely adopted in subsequent speech enhancement research. The key insight — that spectral structure provides better training signal than raw waveform loss — influenced many later architectures.

## Related Concepts

- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]]
- [[concepts/frequency-domain-loss|Frequency Domain Loss for Time-Domain Networks]]
- [[concepts/invalid-stft-problem|Invalid STFT Problem]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]

## Related Sources

- [[sources/tan-2018-convolutional-recurrent-network-speech-enhancement|Tan & Wang 2018: CRN for Real-Time Speech Enhancement]]
