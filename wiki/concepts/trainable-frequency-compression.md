---
type: concept
created: 2026-07-20
updated: 2026-07-20
sources:
  - raw/papers/chen-2023-ultra-dual-path-compression/full-text.md
tags:
  - speech-enhancement
  - model-compression
  - frequency-domain
  - learnable-filterbank
---

# Trainable Frequency Compression

**Trainable Frequency Compression** is a frequency-axis dimensionality-reduction technique introduced by [[sources/chen-2023-ultra-dual-path-compression\|Chen et al. 2023]] in which the filter bank used to compress the STFT frequency axis is **learned jointly with the rest of the network** rather than being a hand-designed triangle filter (ERB or Mel). The trainable variant (called **TrainMel**) follows the Mel scale for band splitting but replaces fixed triangle weights with a learnable linear transformation per band.

## Formulation

For a band $b$ spanning frequency bins $\text{low}[b] : \text{high}[b]$, the compressed feature is computed as:

$$Z[:, t, b] = \text{Flatten}\big(X[0:C, t, \text{low}[b]:\text{high}[b]]\big) \times W, \quad W \in \mathbb{R}^{(\triangle B[b] \times C) \times E}$$

where $\triangle B[b] = \text{high}[b] - \text{low}[b]$, $C$ is the number of stacked signals (real + imaginary), and $E$ is the feature dimension per T-F bin. The transformation outputs a feature of shape $E \times T \times B$, where $B$ is the compressed band count.

Decompression uses a separate learnable linear transform back to $4C \times \triangle B[b]$ — note that the decompressed dimension is $4C \times \triangle B[b]$ rather than $E \times \triangle B[b]$ to save model size.

## Comparison with Fixed Filters

| Method | Filter Shape | Params (at 8×) | WB-PESQ (DT, 8×) | Notes |
|--------|-------------|---------------:|------------------:|-------|
| FixedERB | Triangle (ERB scale) | 109K | 2.30 | ERB scale; SI-SNR higher at large ratios |
| FixedMel | Triangle (Mel scale) | 109K | 2.42 | Mel scale emphasises low frequencies |
| TrainMel | Learnable linear (Mel split) | 398K | 2.56 | >0.1 WB-PESQ gain at 8× and 16× |

Trainable filters add ~300K parameters but yield substantial WB-PESQ improvement at high compression ratios. The authors also note that the $1 \times 1$ convolution in the input layer becomes redundant when using trainable compression and is removed.

## Why Trainable Wins

- Fixed triangle filters cannot adapt to the spectral statistics of the input; trainable filters learn the optimal projection per band.
- The trainable transform operates on the **complex spectrum** (real + imaginary parts stacked), whereas fixed filters operate on the magnitude only — this preserves phase information.
- The Mel band splitting is retained, providing a perceptually motivated initialization structure, while the linear transform within each band is free to learn.

## Relationship to Other Filterbank Techniques

- [[concepts/erb-scale\|ERB Scale]] — fixed filter bank used by DeepFilterNet and RT-Tango
- [[concepts/bark-scale-spectral-features\|Bark-Scale Spectral Features]] — alternative perceptual scale used by later PercepNet-style AEC works
- [[concepts/deep-filtering\|Deep Filtering]] — another learned complex filter, but applied along the **time** axis (per-band temporal filter) rather than along the **frequency** axis

## Related Concepts

- [[concepts/erb-scale\|ERB Scale]]
- [[concepts/dpt-fsnet\|DPT-FSNet]]
- [[concepts/dual-path-compression\|Dual-Path Compression]]
- [[concepts/bark-scale-spectral-features\|Bark-Scale Spectral Features]]
- [[concepts/deep-filtering\|Deep Filtering]]

## Related Sources

- [[sources/chen-2023-ultra-dual-path-compression\|Chen et al. 2023: Ultra Dual-Path Compression]] — introduces TrainMel as the trainable variant of frequency compression
