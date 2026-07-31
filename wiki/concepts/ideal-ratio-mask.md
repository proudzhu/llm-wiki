---
type: concept
created: 2026-06-01
updated: 2026-08-01
sources:
  - raw/papers/liu-2025-pcen-mask-vad-speech-enhancement/full-text.md
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

## Related Concepts

- [[concepts/ideal-binary-mask|Ideal Binary Mask (IBM)]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cIRM)]]
- [[concepts/permutation-invariant-training|Permutation Invariant Training (PIT)]]
- [[concepts/per-channel-energy-normalization|Per-Channel Energy Normalization (PCEN)]] — used as a threshold oracle to zero the IRM on stationary-noise bands

## Related Sources

- [[sources/wang-2018-supervised-speech-separation-deep-learning-overview|Wang & Chen 2018: Supervised Speech Separation Based on Deep Learning: An Overview]]
- [[sources/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement|Yang et al. 2026: CoFi-Lite]] — dual band-decoupled IRMs applied sequentially
- [[sources/liu-2025-pcen-mask-vad-speech-enhancement|Liu et al. 2025: PCEN-Based Mask Thresholding and VAD]] — PCEN-thresholded IRM training target
