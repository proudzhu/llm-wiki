---
type: concept
created: 2026-11-01
updated: 2026-11-01
sources:
  - raw/papers/yan-2025-lisennet/full-text.md
tags:
  - neural-network-architecture
  - convolution
  - speech-enhancement
  - frequency-resolution
---

# Sub-band Convolution

**Sub-band convolution** (sub-band DS-Conv / sub-band US-Conv) is an asymmetric frequency-axis compression scheme for convolutional encoder–decoders, introduced by [[concepts/lisennet|LiSenNet]] (Yan et al., ICASSP 2025). It encodes the perceptual prior that **low-frequency bands matter more for human hearing than high-frequency bands** (the PLP-analysis argument of Hermansky 1990) directly into the network's striding pattern: low frequencies keep full resolution while high frequencies are aggressively downsampled.

## Mechanism

In the encoder's downsampling convolution (DS-Conv) blocks:

- **Low-frequency bands**: Conv2d with **stride 1** — resolution preserved.
- **High-frequency bands**: Conv2d with **stride 3**.

In the decoder's upsampling (US-Conv) blocks the mirror operation recovers the frequency resolution:

- **Low-frequency bands**: stride-1 convolution (nothing to restore).
- **High-frequency bands**: [[concepts/sub-pixel-convolution|sub-pixel convolution]] (SP-Conv2d) with **factor 3**.

Combined with the frequency-axis halving the DS-Conv blocks apply across the whole spectrum, the **net frequency downsampling factor is 2**, but the *effective* resolution loss is concentrated entirely in the high frequencies.

This contrasts with uniform downsampling (e.g., GTCRN's ERB-based band merging compresses only above 2 kHz by learned averaging; [[concepts/cofi-lite|CoFi-Lite]]'s BM inherits that) — sub-band convolution achieves the asymmetry inside ordinary convolution striding rather than via a separate merging module.

## Effect

In LiSenNet's ablation, replacing sub-band convolution with a normal convolution layer ("w/o sub-band Conv") drops PESQ from 3.07 to 3.01 while *saving* parameters (30k vs. 37k) — i.e., the low-frequency resolution preservation is worth the extra cost.

The same principle recurs across the lightweight-SE line with different mechanisms — allocate resolution where hearing needs it:

| Model | Mechanism | Low-freq treatment |
|-------|-----------|---------------------|
| [[concepts/lisennet|LiSenNet]] | Sub-band strided conv (stride 1 vs. 3) | Full resolution via stride 1 |
| [[concepts/gtcrn|GTCRN]] | ERB Band Merging | First 65 bands (< 2 kHz) unaltered |
| [[concepts/cofi-lite|CoFi-Lite]] | Dual coarse/fine paths | Dedicated high-resolution fine path below 2 kHz |
| lightS4 ([[concepts/auditory-inspired-spectral-compressor|AISC]]) | 1.5 kHz perceptual split | Full-resolution low band |

## Related Concepts

- [[concepts/lisennet|LiSenNet]]
- [[concepts/sub-pixel-convolution|Sub-Pixel Convolution]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network (CRN)]]
- [[concepts/erb-scale|ERB Scale]]
- [[concepts/cofi-lite|CoFi-Lite]]

## Related Sources

- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]]
