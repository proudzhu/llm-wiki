---
type: concept
created: 2026-08-01
updated: 2026-08-01
sources:
  - raw/papers/liu-2021-igcrn/full-text.md
tags:
  - neural-network
  - speech-enhancement
  - convolution
  - multi-channel
  - inplace-model
---

# Inplace Convolution

**Inplace convolution** is a convolutional design choice introduced by [[concepts/igcrn|IGCRN]] (Liu & Zhang, Interspeech 2021) for multi-channel speech enhancement in the time-frequency domain. The defining property is that the **kernel stride on the frequency dimension is set to 1**, so the frequency axis is never downsampled — every output frequency bin is computed from the same input frequency bin (plus the kernel's local neighborhood in time). The encoder and decoder therefore keep the frequency resolution unchanged throughout the network.

## Motivation

The standard [[concepts/convolutional-recurrent-network|CRN]] uses strided convolutions (typically stride 2) on the frequency dimension to encode spectral patterns into the channel dimension, then symmetrically upsamples in the decoder. For single-channel SE this is effective — it captures the harmonic structure of speech that repeats across frequency bins.

For multi-channel SE, however, the spatial information that the array provides lives in the *per-frequency-bin* phase relationship between channels (this is exactly what a [[concepts/beamforming|beamformer]] exploits). Frequency downsampling **aliases spatial cues with spectral patterns** in the channel dimension, making it hard for the subsequent recurrent layer to recover the per-bin spatial information needed to act like a beamformer. Inplace convolution avoids this aliasing by keeping each frequency bin's spatial feature intact throughout the encoder and decoder.

## Mathematical Formulation

An inplace convolution is a standard convolution whose stride on the frequency dimension is 1 (the time stride is also 1 in IGCRN, so the kernel is $5 \times 1$ — frequency × time). The encoder uses inplace GLU:

$$Y = ELU(BN(iConv(X) \otimes Sigmoid(iConv(X))))\tag{2}$$

and the decoder uses the symmetric inplace transpose GLU:

$$Y = ELU(BN(iTConv(X) \otimes Sigmoid(iTConv(X))))\tag{3}$$

where $iConv$ and $iTConv$ are stride-1 inplace (transpose) convolutions and $\otimes$ is element-wise multiplication. As in the original GCRN, the GLU's gating mechanism lets the network learn frequency-selective gating patterns; the only difference from GCRN is the absence of frequency downsampling.

## Empirical Evidence

The IGCRN paper provides a striking ablation (Table 5) showing that **performance degrades monotonically as downsampling is added, even when model complexity grows by orders of magnitude**:

| Variant | Downsampling steps | Params (M) | MAC (G) | -3 dB Babble STOI / PESQ |
|---------|--------------------|------------|---------|----------------------------|
| **IGCRN64** (proposed) | 0 | 1.4 | 19.9 | **0.968 / 3.83** |
| IGCRN64-1DS | 1 | 3.5 | 32.1 | 0.982 / 3.94 |
| IGCRN64-2DS | 2 | 9.5 | 53.3 | 0.981 / 3.91 |
| IGCRN64-3DS | 3 | 24.1 | 85.3 | 0.974 / 3.73 |
| IGCRN64-4DS | 4 | 82.5 | 149.5 | 0.961 / 3.58 |
| IGCRN64-5DS | 5 | 316.3 | 277.8 | 0.954 / 3.52 |
| IGCRN64-6DS | 6 | 777.3 | 430.8 | 0.949 / 3.51 |

`IGCRN64-6DS` has 556× more parameters than `IGCRN64` but worse STOI/PESQ. The authors interpret this as direct evidence that the inplace characteristic is essential for multi-channel time-frequency-domain enhancement, and that downsampling aliases spatial information with spectral patterns in a way that more capacity cannot recover.

The `IGCRN80` variant (wider channels, no downsampling) matches `IGCRN64-1DS` in MAC count but beats it on both STOI and PESQ — confirming that widening the inplace model is more parameter-efficient than reintroducing downsampling.

## Use in the Inplace-CRN Family

- **[[concepts/igcrn|IGCRN]]** (Liu & Zhang 2021) — introduces inplace convolution as the encoder/decoder building block for dual-channel SE.
- **[[concepts/iccrn|ICCRN]]** (Liu & Zhang 2023) — inherits the inplace design (no frequency downsampling, $f = 160$ throughout) and replaces the GLU with the [[concepts/cepstral-frequency-block|Cepstral Frequency Block (CFB)]]. ICCRN's authors note that IGCRN's monaural performance was relatively weak because discarding frequency downsampling also discards full-band modeling capacity; ICCRN recovers that capacity by modeling speech in the cepstral space, where harmonic structure is sparsely represented, instead of relying on frequency downsampling to discover it.

## Related Concepts

- [[concepts/igcrn|IGCRN]] — the model that introduces inplace convolution
- [[concepts/channel-wise-lstm|Channel-wise LSTM with Model Reuse]] — the recurrent bottleneck that exploits the inplace design
- [[concepts/iccrn|ICCRN]] — successor that inherits the inplace design
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — the conventional CRN that uses frequency downsampling
- [[concepts/beamforming|Beamforming]] — the traditional per-frequency-bin processing that motivates inplace convolution
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — broader task

## Related Sources

- [[sources/liu-2021-igcrn|Liu & Zhang 2021: IGCRN — Inplace Gated Convolutional Recurrent Neural Network]]
- [[sources/liu-2023-iccrn|Liu & Zhang 2023: ICCRN — Inplace Cepstral Convolutional Recurrent Neural Network]]
