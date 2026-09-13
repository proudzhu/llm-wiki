---
type: concept
created: 2026-09-13
updated: 2026-09-13
sources:
  - raw/papers/pandey-2025-ultra-low-compute/full-text.md
tags:
  - multi-channel
  - deep-learning
  - spatial-filtering
  - low-compute
---

# Spatial Convolution

**Spatial convolution** is a trainable MIMO (multiple-input-multiple-output) convolution technique for multichannel audio in the time-frequency domain, introduced by Pandey & Xu ("Decoupled spatial and temporal processing for resource efficient multichannel speech enhancement", ICASSP 2024) and used as the spatial processing block of [[concepts/tinygru|TinyGRU]] in [[sources/pandey-2025-ultra-low-compute|Pandey & Azcarreta 2025]]. It brings the filter-and-sum beamforming operation of classical array processing into a learned, real-valued network layer.

## Formulation

Inspired by frequency-domain filter-and-sum beamforming, each spatial convolution layer $l$ comprises $F$ distinct trainable matrices, each of size $C_{out}^l \times C_{in}^l$ — one matrix per frequency bin. The matrix is multiplied by the input tensor of $C_{in}^l$ channels at each frequency bin, producing an output tensor with $C_{out}^l$ spatial dimensions and $F$ frequency bins:

- **Input**: the multichannel STFT with real and imaginary parts concatenated along the channel axis, forming a real-valued signal with $2 \cdot C$ channels (e.g., 16 real channels for an 8-microphone array).
- **Nonlinearity**: each convolution is followed by a parametric ReLU.
- **Stacking**: layers progressively reduce channel count (e.g., 16 → 8 → 4 → 2 → 1), ending in a single monaural representation.

Because the per-frequency matrices act only across channels (not across time), the operation is frame-local and fully causal; the temporal context is left to a separate recurrent block (e.g., [[concepts/splitgru|SplitGRU]]). This decoupling of spatial and temporal processing is the core efficiency trick: expensive joint time-frequency processing is replaced by a cheap per-bin linear spatial map plus a low-width recurrent sequence model.

## Role in TinyGRU

In [[concepts/tinygru|TinyGRU]], the spatial convolution block's final layer outputs a single-channel signal that is combined with linear-transformed ERB features of the reference microphone. Normalizing the first layer's output frame-wise (mean/variance over channel and frequency) renders the model scale-invariant in combination with masking.

## Related Concepts

- [[concepts/beamforming|Beamforming]] — the classical operation the layer mimics
- [[concepts/tinygru|TinyGRU]] — the model that uses it as its spatial front-end
- [[concepts/splitgru|SplitGRU]] — the complementary temporal processing block
- [[concepts/relative-transfer-function|Relative Transfer Function]] — the array-domain quantity implicitly modeled by per-bin spatial maps

## Related Sources

- [[sources/pandey-2025-ultra-low-compute|Pandey & Azcarreta 2025: Ultra Low-Compute Complex Spectral Masking for Multichannel Speech Enhancement]]
