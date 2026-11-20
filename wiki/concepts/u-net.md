---
type: concept
created: 2026-11-15
updated: 2026-11-20
sources:
  - raw/papers/ronneberger-2015-u-net/full-text.md
  - raw/papers/pascual-2017-segan/full-text.md
tags:
  - u-net
  - semantic-segmentation
  - encoder-decoder
  - convolutional-neural-network
---

# U-Net

**U-Net** is a fully convolutional encoder–decoder for dense per-pixel prediction, introduced by Ronneberger, Fischer & Brox (MICCAI 2015) for biomedical image segmentation. Its defining property is the **U shape**: a contracting path that halves spatial resolution and doubles channels, a symmetric expansive path that restores resolution, and **skip connections that copy each contracting feature map into its matching expansion level**. It has no fully connected layers.

## Architecture

Let level $\ell = 1..L$ index resolution. The contracting path applies

$$\mathbf{H}^{c}_{\ell} = \mathrm{ReLU}\big(\mathrm{conv}_{3\times3}(\cdot)\big)\circ\mathrm{ReLU}\big(\mathrm{conv}_{3\times3}(\cdot)\big)(\mathrm{pool}_{2\times2}(\mathbf{H}^{c}_{\ell-1}))$$

and the expansive path applies

$$\mathbf{H}^{e}_{\ell} = \mathrm{ReLU}\big(\mathrm{conv}_{3\times3}\circ\mathrm{conv}_{3\times3}\big)\Big(\big[\mathrm{upconv}_{2\times2}(\mathbf{H}^{e}_{\ell-1});\ \mathrm{crop}(\mathbf{H}^{c}_{\ell})\big]\Big)$$

where $[\cdot;\cdot]$ is channel concatenation along the last axis and `crop` trims the contracting map to the spatial size left by the valid convolutions.

The original network: 23 convolutional layers, channels 64 → 128 → 256 → 512 → 1024 at the bottleneck → 512 → 256 → 128 → 64, 2×2 max-pool downsampling, 2×2 up-convolutions (stride-2 transposed convolution) upsampling, final 1×1 convolution to $K$ classes followed by pixel-wise softmax. All 3×3 convolutions are *valid* (unpadded), so the output is 388×388 for a 572×572 input — a 92-pixel border is lost per side.

Two design choices distinguish it from the FCN of Long et al.:
1. **Wide expansive path** — many channels in the upsampling branch let context propagate to high-resolution layers, instead of the decoder being a thin projection of the bottleneck.
2. **Concatenation, not addition**, at skips — the decoder sees the full contracting feature map, not a fused sum.

The output-size arithmetic that drives tiling: with $L$ pooling levels and valid convolutions, an input of side $S$ yields output side roughly $S - \sum\text{(border losses)}$; to tile seamlessly every max-pool must see an even side at every level.

## Why it works

Pooling is a lossy, non-invertible operation; the decoder cannot recover which of the pooled positions held the boundary. The skip tensor hands that high-frequency information back at exactly the resolution where it is needed. This is the mechanism that resolves the classical localization-vs-context trade-off of sliding-window segmentation, and it is why the same topology transfers to any dense-prediction problem — including spectrogram masking in speech enhancement, where "resolution" becomes the frequency axis.

## Descendants

Named variants in this wiki, all U-Net-shaped with domain-specific substitutions:

| Variant | Domain | Substitution |
|:---|:---|:---|
| [[concepts/u-net-post-filter|U-Net post filter]] | AEC / speech enhancement | Bark-band encoder, depthwise-separable convs, GRU bottleneck, sub-pixel upsampling, sigmoid gain mask output |
| [[concepts/trunet|TRU-Net]] | Real-time speech enhancement | 1D frequency-axis conv, FGRU + causal TGRU bottleneck, 1D transposed-conv decoder |
| [[concepts/tfc-tdf-unet|TFC-TDF U-Net]] | Music source separation | TFC and TDF blocks replace 2D convs; frequency-axis linear layers |
| [[concepts/segan|SEGAN]] | Waveform-level speech enhancement (1-D) | Strided conv1d encoder (k=31, stride 2), transposed-conv decoder, PReLU, latent vector concatenated at the bottleneck, adversarially trained |
| [[concepts/cdunet|CDUNet]] | Directional speech enhancement | Causal U-Net conditioned on three steered beams |

## Related Concepts

- [[concepts/overlap-tile-strategy|Overlap-Tile Strategy]]
- [[concepts/boundary-weighted-loss|Boundary-Weighted Loss]]
- [[concepts/elastic-deformation-augmentation|Elastic Deformation Augmentation]]
- [[concepts/sub-pixel-convolution|Sub-Pixel Convolution]] — the modern cheap replacement for up-convolution
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]] — what makes U-Net variants cheap enough for embedded use

## Related Sources

- [[sources/ronneberger-2015-u-net|Ronneberger, Fischer & Brox 2015: U-Net]]
- [[sources/pascual-2017-segan|Pascual, Bonafonte & Serrà 2017: SEGAN]] — the 1-D waveform instantiation: skip-connected encoder–decoder over raw 16 kHz samples, where "resolution" is time rather than the frequency axis
