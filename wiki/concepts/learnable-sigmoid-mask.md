---
type: concept
created: 2026-11-01
updated: 2026-11-01
sources:
  - raw/papers/yan-2025-lisennet/full-text.md
tags:
  - mask
  - speech-enhancement
  - neural-network-architecture
---

# Learnable Sigmoid Mask

The **learnable Sigmoid (LSigmoid)** is a mask activation function that replaces the fixed Sigmoid at the output of a speech-enhancement decoder, introduced for [[concepts/pesq|MetricGAN+]] (Fu et al., Interspeech 2021) and adopted as the mask head of [[concepts/lisennet|LiSenNet]] (Yan et al., ICASSP 2025):

$$\mathrm{LSigmoid}(x) = \frac{\beta}{1 + e^{-\alpha x}}$$

where $\beta$ is a constant scalar and $\boldsymbol{\alpha} \in \mathbb{R}^{F}$ is a **trainable, frequency-dependent** vector.

## Why per-frequency α?

Speech signals exhibit **distinct patterns in high and low frequency bands**. A standard Sigmoid applies one fixed input–output slope everywhere; LSigmoid lets each frequency band learn its own slope $\alpha_f$, so the mask's transfer shape adapts per band. In LiSenNet, $\beta = 2.0$ (allowing mask values up to 2, beyond the usual $[0,1]$ range — useful where the noisy magnitude is under-attenuated).

## Effect

In LiSenNet's ablation (VoiceBank+DEMAND), freezing the learnable parameters ("w/o LSigmoid") drops PESQ from 3.07 to 3.05 — a small but consistent gain at **zero parameter cost** (α is only F parameters).

## Relation to Other Flexible Mask Activations

- **[[concepts/phase-aware-beta-sigmoid-mask|Phase-aware β-sigmoid mask]]** (Choi et al. 2021): a per-T-F-unit learned $\beta_{t,f}$ computed by a network layer with softplus, motivated by triangle-inequality constraints in complex decomposition — learned *upper bound* per unit.
- **LSigmoid**: learned *slope* per frequency band — a coarser but far cheaper parameterization (F values, not T×F).

Both relax the fixed $[0, 1]$ sigmoid of the classic [[concepts/ideal-ratio-mask|ratio mask]] along different axes.

## Related Concepts

- [[concepts/lisennet|LiSenNet]]
- [[concepts/ideal-ratio-mask|Ideal Ratio Mask (IRM)]]
- [[concepts/phase-aware-beta-sigmoid-mask|Phase-aware β-sigmoid Mask (PHM)]]
- [[concepts/pesq|PESQ]]

## Related Sources

- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]]
