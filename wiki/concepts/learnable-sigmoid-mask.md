---
type: concept
created: 2026-11-01
updated: 2026-11-22
sources:
  - raw/papers/yan-2025-lisennet/full-text.md
  - raw/papers/fu-2019-metricgan/full-text.md
  - raw/papers/fu-2021-metricgan-plus/full-text.md
  - raw/papers/close-2022-metricgan-plus-minus/full-text.md
tags:
  - mask
  - speech-enhancement
  - neural-network-architecture
---

# Learnable Sigmoid Mask

The **learnable Sigmoid (LSigmoid)** is a mask activation function that replaces the fixed Sigmoid at the output of a speech-enhancement decoder, introduced by [[sources/fu-2021-metricgan-plus|MetricGAN+ (Fu et al., Interspeech 2021)]] and adopted as the mask head of [[concepts/lisennet|LiSenNet]] (Yan et al., ICASSP 2025):
$$\mathrm{LSigmoid}(x) = \frac{\beta}{1 + e^{-\alpha x}}$$

where $\beta$ is a constant scalar and $\boldsymbol{\alpha} \in \mathbb{R}^{F}$ is a **trainable, frequency-dependent** vector.

### Predecessor: the Fixed Sigmoid with a Floor

The original [[sources/fu-2019-metricgan|MetricGAN (ICML 2019)]] used a plain sigmoid mask head (257 bins) and handled its failure mode with a **fixed floor**: the estimated mask was clamped at a lower threshold of 0.05 before T-F masking, following Koizumi et al., to prevent musical noise. MetricGAN+ **retains the 0.05 floor** but makes the activation's slope and ceiling trainable per frequency bin — the "learnable" refers to the transfer shape, not to removing the floor.

## Why per-frequency α?

Speech signals exhibit **distinct patterns in high and low frequency bands**. A standard Sigmoid applies one fixed input–output slope everywhere; LSigmoid lets each frequency band learn its own slope $\alpha_f$, so the mask's transfer shape adapts per band. In LiSenNet, $\beta = 2.0$ (allowing mask values up to 2, beyond the usual $[0,1]$ range — useful where the noisy magnitude is under-attenuated).

In the originating [[sources/fu-2021-metricgan-plus|MetricGAN+]] paper, $\beta = 1.2$ is motivated by phase: $|X(t,f)| \neq |Y(t,f)| + |N(t,f)|$, so the ideal magnitude mask $|Y|/|X|$ is not bounded by 1 and a $[0,1]$ sigmoid cannot represent it. Making $\beta$ learnable as well was tried and did **not** improve performance.

## Effect

In LiSenNet's ablation (VoiceBank+DEMAND), freezing the learnable parameters ("w/o LSigmoid") drops PESQ from 3.07 to 3.05 — a small but consistent gain at **zero parameter cost** (α is only F parameters).

In MetricGAN+'s own ablation the learnable sigmoid is the largest final step: PESQ 3.05 → **3.15** (+0.10), also improving training efficiency. The learned slopes are informative: most bins settle near $\alpha \approx 0.5$ (below the fixed sigmoid's 1) — a near-linear transfer that backpropagates more efficiently than saturated regions — while **high-frequency bins learn $\alpha \gg 1$**, behaving like a binary mask. The authors conjecture this reflects training noises not occupying high frequencies, or PESQ's own characteristics, and flag it as unverified.

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

- [[sources/fu-2019-metricgan|Fu, Liao, Tsao & Lin 2019: MetricGAN]] — the predecessor's fixed sigmoid mask head, where musical noise was handled by clamping the mask at 0.05 rather than by a trainable slope
- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]]
- [[sources/fu-2021-metricgan-plus|Fu et al. 2021: MetricGAN+]] — the originating paper: $\beta = 1.2$, per-bin $\alpha$, +0.10 PESQ in ablation; learned $\alpha \approx 0.5$ for most bins and $\alpha \gg 1$ at high frequencies
- [[sources/close-2022-metricgan-plus-minus|Close, Hain & Goetze 2022: MetricGAN+/-]] — uses LSigmoid ($\beta = 1.2$) in both the generator and the de-generator; making $\beta$ learnable in the de-generator trades PESQ (3.21 → 3.17) for the best CSIG 4.16 / COVL 3.65 — a second data point that learnable $\beta$ shifts the quality trade rather than uniformly helping
