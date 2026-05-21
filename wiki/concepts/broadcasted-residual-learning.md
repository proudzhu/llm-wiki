---
type: concept
created: 2026-05-21
updated: 2026-05-21
sources:
  - raw/papers/kim-2021-broadcasted-residual-learning/full-text.md
tags:
  - neural-networks
  - keyword-spotting
  - efficient-neural-networks
---

# Broadcasted Residual Learning

**Broadcasted residual learning** is a residual neural-network design that computes most residual information on compressed temporal features and broadcasts that residual back over the full frequency-time representation. It was introduced by Kim et al. for efficient [[concepts/keyword-spotting|keyword spotting]] and is the central mechanism behind [[concepts/bc-resnet|BC-ResNet]].

## Key Formulation

For a conventional residual block:

$$y = x + f(x)$$

broadcasted residual learning decomposes the residual function into a frequency-aware 2D operation $f_2$, frequency pooling, and a temporal operation $f_1$:

$$y = x + BC(f_1(avgpool(f_2(x))))$$

where $BC$ expands the temporal residual back along the frequency dimension.

BC-ResNet uses an augmented block:

$$y = x + f_2(x) + BC(f_1(avgpool(f_2(x))))$$

The auxiliary $f_2(x)$ term preserves 2D frequency-local information that might be lost when averaging across frequency.

![[raw/papers/kim-2021-broadcasted-residual-learning/figures/bc-resblock.png|Broadcasted residual block]]
*Figure 1: Broadcasted residual learning combines a frequency-depthwise 2D path with a temporal residual path expanded back over frequency.*

## Why It Is Efficient

In spectrogram CNNs, pointwise and temporal convolutions become expensive when applied to full $F \times T$ feature maps. Broadcasted residual learning first reduces the feature map to $1 \times T$, applies temporal depthwise and pointwise operations there, and then expands the result to $F \times T$. This reduces the cost of those operations by roughly the frequency dimension factor while retaining a lightweight 2D path.

## Design Implications

- It bridges the gap between pure 1D temporal CNNs and full 2D time-frequency CNNs.
- It is especially useful when frequency-local information matters but edge deployment forbids repeated full 2D convolution.
- Its additive residual mapping outperforms a temporal-channel attention variant in the BC-ResNet ablation.

## Related Concepts

- [[concepts/keyword-spotting|Keyword Spotting]]
- [[concepts/bc-resnet|BC-ResNet]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]
- [[concepts/subspectral-normalization|SubSpectral Normalization]]
- [[concepts/time-frequency-separate-convolutions|Time-Frequency Separate Convolutions]]
- [[concepts/neural-networks|Neural Networks]]

## Related Sources

- [[sources/kim-2021-broadcasted-residual-learning|Kim, Chang, Lee & Sung 2021: Broadcasted Residual Learning]]
