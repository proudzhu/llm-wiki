---
type: concept
created: 2026-06-06
updated: 2026-08-15
sources:
  - raw/papers/li-2025-echofree-neural-aec/full-text.md
  - raw/papers/lugo-2026-diffvqe/full-text.md
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

## Related Concepts

- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/complex-convolving-mask|Complex Convolving Mask]]

## Related Sources

- [[sources/indenbom-2023-deepvqe|Indenbom et al. 2023: DeepVQE]]
- [[sources/lugo-2026-diffvqe|Lugo et al. 2026: DiffVQE]] — anti-aliasing replacement for transposed convolutions in the Cond/Score U-Net
