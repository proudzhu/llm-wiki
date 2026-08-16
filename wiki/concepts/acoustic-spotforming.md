---
type: concept
created: 2026-08-16
updated: 2026-08-16
sources:
  - raw/papers/taseska-2018-informed-spatial-filters/full-text.md
tags:
  - spatial-filter
  - speech-enhancement
  - multi-array
  - position-based
  - sound-acquisition
---

# Acoustic Spotforming

**Acoustic spotforming** is a position-selective sound-acquisition technique that extracts signals originating from a user-defined **Spot of Interest (SOI)** — a 2D region in the room — while reducing noise and interference from outside the spot. It generalizes direction-based source extraction to a *spatial region* rather than a single direction. The data-dependent spotforming framework was introduced by Taseska & Habets (IEEE/ACM TASLP 2016) using distributed microphone arrays and the [[concepts/informed-spatial-filter|informed spatial filtering]] paradigm.

## Method

With $\geq 2$ spatially separated arrays whose locations and orientations are known:

1. **Narrowband position estimation** — per-array narrowband DOAs are triangulated to obtain a 2D position estimate $\hat{\mathbf{r}}_{tk}$ at each TF bin.
2. **Spot signal detection** — a Gaussian model for the position estimate (mean at the cluster, covariance from estimation noise) yields a likelihood under "spot signal dominant" vs. "undesired signal dominant"; a Gaussian signal model provides the SPP for noise detection. The posterior determines whether each TF bin originates from the SOI.
3. **Statistics update** — the spot-signal PSD matrix is estimated recursively from bins where the spot signal is detected as dominant. Due to speech sparsity, small spot size, and temporal averaging, this PSD matrix is approximately **rank-one**.
4. **MVDR spotformer** — because the spot-signal PSD matrix is rank-one, a single-constraint MVDR filter suffices. This contrasts with *fixed* spotformers, which need multiple linear constraints to ensure low distortion across the entire SOI, thereby sacrificing degrees of freedom for undesired-signal reduction.

For scenarios with multiple sources inside the SOI, a **projection-based RTF estimator** reduces distortion compared to the rank-one-model RTF estimator.

## Advantages

- Adapts almost instantaneously to changing acoustic conditions and appearing/disappearing sources (inherent to the ISF paradigm).
- Single-constraint MVDR (vs. multi-constraint fixed spotformer) preserves degrees of freedom for noise/interference reduction.
- The position-based detector operates at very low false-positive rates while still detecting sufficient spot-signal TF bins.

## Related Concepts

- [[concepts/informed-spatial-filter|Informed Spatial Filter (ISF)]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/relative-transfer-function|Relative Transfer Function (RTF)]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[sources/taseska-2018-informed-spatial-filters|Taseska 2018: Informed Spatial Filters for Speech Enhancement]] (Chapter 6)
