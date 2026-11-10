---
type: concept
created: 2026-06-01
updated: 2026-11-01
sources:
  - raw/papers/liu-2025-pcen-mask-vad-speech-enhancement/full-text.md
  - raw/papers/yan-2025-lisennet/full-text.md
  - raw/papers/zhao-2025-lightweight-transformer/full-text.md
tags:
  - speech-separation
  - time-frequency-masking
  - training-target
---

# Ideal Ratio Mask (IRM)

The Ideal Ratio Mask (IRM) is a soft-mask training target for supervised speech separation, representing the proportion of target speech energy within each time-frequency unit.

## Definition

$$IRM(t,f) = (S^2 / (S^2 + N^2))^beta$$

where beta is a scaling parameter (commonly 0.5).

## Properties

- **Soft masking**: Provides a continuous mask, reducing musical noise artifacts
- **Relation to Wiener filter**: Without the square root (beta=1), equivalent to the classical Wiener filter
- **Cost function**: Mean squared error (MSE) is typically used

## Comparison

The IRM emerged as one of the preferred training targets. Masking-based targets outperform mapping-based targets for intelligibility (STOI).

## Variants

- **Dual decoupled IRMs ([[concepts/cofi-lite|CoFi-Lite]], Yang et al. 2026)**: two IRMs predicted by separate coarse/fine paths and applied **sequentially** — a full-band coarse mask restoring the magnitude envelope, then a fine mask refining only low frequencies ($f \leq f_\text{low}$, 2 kHz). This band-decoupled masking lets each mask specialize: the coarse mask needs no fine spectral detail (tolerates ×16 compression), the fine mask focuses capacity where salient speech structure concentrates.
- **PCEN-thresholded IRM (Liu et al. 2025)**: a training-target modification rather than a new mask type. The standard IRM (here written with an echo term, $IRM = S/(S+N+E)$) is zeroed on any time-frequency band whose [[concepts/per-channel-energy-normalization|PCEN]] value falls below a band-level threshold $TH_\text{band}$, and on all bands of frames a PCEN-VAD flags as non-speech. This removes stationary noise buried in the "clean" target $S(t,f)$ and drops perceptually insignificant low-energy bands, reducing target variability. The IRM formula itself is unchanged — PCEN is used only as a threshold oracle, and only at training time.
- **Compressed-domain real IRM (LCT-GAN, Zhao & Madhu 2025)**: the target is estimated at compression $c=0.3$, $\widehat{\mathrm{IRM}}_c(k,l)=\lvert S(k,l)\rvert^{c}/(\lvert X(k,l)\rvert^{c}+\gamma)$, and the *linear*-domain mask is recovered by exponentiating with $1/c$ — i.e. the network learns a real magnitude ratio and the noisy phase is reused, rather than learning a complex mask. The same $c=0.3$ is applied on the input side, so the network sees and predicts in one compressed representation. Benchmarked in-situ against complex-valued variants (RI masking/mapping, MCS mapping/hybrid) inside the same architecture, the real compressed IRM was never beaten on PESQ/STOI/SI-SDR/DNSMOS — 2.68 vs 2.65 PESQ for the best complex variant.

## Related Concepts

- [[concepts/ideal-binary-mask|Ideal Binary Mask (IBM)]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cIRM)]]
- [[concepts/learnable-sigmoid-mask|Learnable Sigmoid Mask]] — flexible-slope mask activation
- [[concepts/permutation-invariant-training|Permutation Invariant Training (PIT)]]
- [[concepts/per-channel-energy-normalization|Per-Channel Energy Normalization (PCEN)]] — used as a threshold oracle to zero the IRM on stationary-noise bands

## Related Sources

- [[sources/wang-2018-supervised-speech-separation-deep-learning-overview|Wang & Chen 2018: Supervised Speech Separation Based on Deep Learning: An Overview]]
- [[sources/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement|Yang et al. 2026: CoFi-Lite]] — dual band-decoupled IRMs applied sequentially
- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]] — magnitude mask estimated via a [[concepts/learnable-sigmoid-mask|learnable Sigmoid]] with per-frequency slope, applied to the power-compressed magnitude before [[concepts/gla-phase-refinement|GLA phase refinement]]
- [[sources/liu-2025-pcen-mask-vad-speech-enhancement|Liu et al. 2025: PCEN-Based Mask Thresholding and VAD]] — PCEN-thresholded IRM training target
- [[sources/zhao-2025-lightweight-transformer|Zhao & Madhu 2025: Study of Lightweight Transformer Architectures for Single-Channel Speech Enhancement]] — compressed-domain real IRM ($c=0.3$) benchmarked against complex-valued RI/MCS masking and mapping in one architecture
