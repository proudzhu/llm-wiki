---
type: concept
created: 2026-08-16
updated: 2026-08-16
sources:
  - raw/papers/taseska-2018-informed-spatial-filters/full-text.md
tags:
  - source-tracking
  - blind-source-separation
  - bayesian-filtering
  - multi-array
  - data-association
  - sparsity
---

# Sparsity-Based Source Tracking

**Sparsity-based source tracking** is a multi-source tracking framework that exploits speech sparsity in the STFT domain to simultaneously track moving sources and estimate the TF masks required for informed-spatial-filter-based blind source separation (BSS). It was developed by Taseska & Habets (IEEE/ACM TASLP 2018) using an approximate Bayesian tracker with a **narrowband augmented measurement model**, where the data-association probabilities *are* the TF masks.

## Measurement Model

With $\geq 2$ distributed arrays, each TF bin provides:

- A **narrowband position estimate** $\hat{\mathbf{r}}_{tk}$ (from triangulating per-array DOAs).
- The **STFT-domain signal vector** $\mathbf{y}(t,k)$.

The augmented measurement is $\mathbf{o}_{tk} = \{\hat{\mathbf{r}}_{tk}, \mathbf{y}(t,k)\}$. The position and signal vector are assumed independent, so the likelihood factorizes. The position follows a Gaussian (clutter model: uniform over the room for noise-dominated bins), and the signal vector follows the Gaussian signal model used for SPP estimation. Crucially, the model allows **multiple measurements per source per frame** — required because, in narrowband processing, the same source can be dominant at different frequency bins.

## Tracker Formulation

Tracking is formulated as a **missing-data problem**: the dominant-source labels $Z_{tk}$ are hidden, and the tracker estimates the source states (positions) $\mathbf{x}_t^j$ and the associations $p(Z_{tk} \mid \mathcal{V}_{1:t})$ jointly. An EM-style iterative scheme estimates the measurement-noise covariances (which are source-dependent and time-varying) and the source states.

## Relation to JPDA and PMHT

The tracker relates to:
- **Joint Probabilistic Data Association (JPDA)**: shares the Gaussian-plus-clutter measurement model, but JPDA's single-measurement-per-source assumption is *invalid* for narrowband features; the proposed model handles multiple measurements per source.
- **Probabilistic Multi-Hypothesis Tracker (PMHT)**: shares the soft-association idea, but the proposed tracker is consistent with the narrowband model where associations are independent across measurements.

## Track Management

- **Source detection**: new tracks are initialized when measurement clusters persistently fail to associate with existing sources.
- **Source removal**: tracks are deleted when their association probabilities decay below a threshold.

## Result

Competitive with state-of-the-art sparsity-based and Independent Vector Analysis (IVA)-based BSS on both simulated and real measurements, with efficient track management for appearing/disappearing moving sources. The Markovian motion model ensures source association is consistent across time frames, and the approach avoids the frequency-permutation problem of convolutive BSS.

## Related Concepts

- [[concepts/tf-mask-estimation|TF Mask Estimation]]
- [[concepts/informed-spatial-filter|Informed Spatial Filter (ISF)]]
- [[concepts/acoustic-spotforming|Acoustic Spotforming]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[sources/taseska-2018-informed-spatial-filters|Taseska 2018: Informed Spatial Filters for Speech Enhancement]] (Chapter 8)
