---
type: concept
created: 2026-07-17
updated: 2026-07-17
sources:
  - raw/papers/seidel-2024-bark-scale-nn-residual-suppression/full-text.md
tags:
  - signal-processing
  - acoustic-echo-cancellation
  - subband-processing
  - adaptive-filtering
---

# Oversampled Filterbank

An **oversampled filterbank** is a multi-rate filterbank in which the total output sampling rate (summed across all subbands) exceeds the input sampling rate. In acoustic echo cancellation (AEC) and speech enhancement, oversampled filterbanks are used to reduce aliasing in subband adaptive filters, allowing for simpler and more effective per-subband adaptation.

## Motivation

In critically sampled filterbanks (where the total output rate equals the input rate), subband signals contain significant aliasing — energy from one frequency band "leaks" into adjacent bands due to imperfect filter skirts. This aliasing degrades the performance of per-subband adaptive filters, because the filter sees aliased components that do not obey the assumed single-tap-per-subband model.

Oversampling (typically by a factor of 2 or more) reduces in-band and cross-band aliasing at the cost of increased computation, making per-subband adaptive filters more effective.

## Harteneck–Weiss–Stewart Design

A widely used design for oversampled filterbanks in AEC is the **near-perfect-reconstruction oversampled filterbank** of Harteneck, Weiss & Stewart (IEEE TCS II, 1999), which uses:

- **Prototype lowpass filter** designed via spectral factorization.
- **Cosine modulation** to generate the analysis and synthesis filters from the prototype.
- **Near-perfect reconstruction** (NPR) property: aliasing is not exactly zero, but is small enough for practical AEC use.

This design is used in the LEC stage of [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Seidel et al. 2024]] to "assure a minimal aliasing level both in-band and across sub-bands" before applying subband NLMS adaptation.

## Role in Hybrid AEC

In a hybrid AEC system like [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Seidel et al. 2024]]:

1. The over-sampled filterbank decomposes mic and far-end signals into subbands.
2. A subband [[concepts/subband-adaptive-filter\|NLMS]] filter estimates the linear echo path in each subband.
3. The estimated echo is subtracted from the mic signal in each subband.
4. The residual (error) signal is reconstructed to fullband (or kept in subband) for input to the neural postfilter.

The low aliasing of the oversampled design ensures that the LEC's per-subband NLMS converges to a good echo path estimate without aliasing-induced bias.

## Comparison with Other Filterbanks

| Filterbank type | Sampling rate | Aliasing | Use case |
|-----------------|---------------|----------|----------|
| Critically sampled DFT filterbank | $f_s/N$ per band | High | Frequency analysis, not direct adaptive filtering |
| **Oversampled filterbank** (Harteneck 1999) | $>f_s/N$ per band | Low | [[concepts/subband-adaptive-filter\|Subband adaptive filtering]], AEC |
| Weighted overlap-add (WOLA) | Configurable | Low | Hearing aids, low-delay SE |
| Gammatone / Bark / ERB filterbank | Perceptual | N/A | Perceptual feature extraction (not for adaptive filtering) |

Note: the [[concepts/bark-scale-spectral-features\|Bark-scale filterbank]] used in neural postfilters (e.g., the $\mathbf{B}$ matrix in Seidel 2024) is **not** an oversampled filterbank in this sense — it is a perceptually motivated static projection for feature extraction, not a multi-rate analysis-synthesis system.

## Related Concepts

- [[concepts/subband-adaptive-filter\|Subband Adaptive Filter]]
- [[concepts/adaptive-filtering\|Adaptive Filtering]]
- [[concepts/acoustic-echo-cancellation\|Acoustic Echo Cancellation]]
- [[concepts/bark-scale-spectral-features\|Bark-Scale Spectral Features]]

## Related Sources

- [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Seidel, Mowlaee & Fingscheidt 2024]] — uses Harteneck–Weiss–Stewart oversampled filterbank in the LEC stage
