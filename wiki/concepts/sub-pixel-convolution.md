---
type: concept
created: 2026-06-06
updated: 2026-11-07
sources:
  - raw/papers/li-2025-echofree-neural-aec/full-text.md
  - raw/papers/lugo-2026-diffvqe/full-text.md
  - raw/papers/yan-2025-lisennet/full-text.md
  - raw/papers/laroche-2026-lisenet-embedded/full-text.md
tags:
  - deep-learning
  - upsampling
  - convolution
---

# Sub-Pixel Convolution

**Sub-pixel convolution** is an upsampling method that learns an array of filters to transform low-resolution feature maps into high-resolution output. It replaces transposed convolution and enables higher feature diversity with small computational cost.

## Mechanism

Given input $\mathbf{X} \in \mathbb{R}^{c_i \times t \times f}$ with $c_i$ channels:

1. **Convolution**: Regular convolution with $2c$ filters produces $\mathbf{X}' \in \mathbb{R}^{2c \times t \times f}$

2. **Pixel shuffle**: Transpose and reshape into output $\mathbf{Y} \in \mathbb{R}^{c \times t \times 2f}$

Each upscaling is by factor 2 on the frequency axis.

## Advantages over Transposed Convolution

- Learns upsampling filters rather than fixed interpolation
- Higher feature diversity
- Smaller performance cost
- Avoids checkerboard artifacts common in transposed convolution

## Applications

- Speech enhancement decoders (frequency-axis upsampling)
- Image super-resolution (original application)
- Any encoder-decoder architecture requiring upsampling
- Diffusion-based AEC ([[sources/lugo-2026-diffvqe|DiffVQE]]): sub-pixel convolution replaces transposed convolution in the Cond/Score U-Net decoder to alleviate aliasing phenomena
- High-frequency sub-band upsampling in [[concepts/lisennet|LiSenNet]] ([[concepts/sub-band-convolution|sub-band US-Conv]]): SP-Conv2d with factor 3 restores the high-frequency resolution that the encoder's stride-3 DS-Conv compressed, mirroring the downsampling asymmetry

## When Sub-Pixel Convolution Is *Not* Deployable

[[sources/laroche-2026-lisenet-embedded|Laroche & Olsson 2026]] replace LiSenNet's reshape-based sub-pixel upsampling with a 1×3 transposed convolution (stride 3, frequency axis) when porting to the STM32N6 NPU: the rank-5 intermediate tensors produced by the reshape-based variant are unsupported by the accelerator's static-graph operator set. The transposed-convolution substitute also cuts decoder arithmetic by ~3× — a reminder that the "avoids checkerboard artifacts" advantage of sub-pixel convolution ([[concepts/lisennet-npu|LiSenNet-NPU]] table) is moot when the target hardware cannot execute the reshape at all.

## Related Concepts

- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/complex-convolving-mask|Complex Convolving Mask]]
- [[concepts/sub-band-convolution|Sub-band Convolution]]

## Related Sources

- [[sources/indenbom-2023-deepvqe|Indenbom et al. 2023: DeepVQE]]
- [[sources/lugo-2026-diffvqe|Lugo et al. 2026: DiffVQE]] — anti-aliasing replacement for transposed convolutions in the Cond/Score U-Net
- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]] — sub-band US-Conv applies SP-Conv2d with factor 3 to the high-frequency bands only
- [[sources/laroche-2026-lisenet-embedded|Laroche & Olsson 2026: Beyond Model Size]] — reshape-based SP-Conv replaced by 1×3 transposed conv for NPU compatibility (rank-5 tensors unsupported)
