---
type: concept
created: 2026-07-23
updated: 2026-07-23
tags:
  - filter-banks
  - high-selectivity
  - geometric-frequency-spacing
  - music-signal-processing
---

# Constant-Q Fast Filter Bank (CQFFB)

The **Constant-Q Fast Filter Bank (CQFFB)** is a high-selectivity, geometrically spaced filter bank introduced by Graziosi, dos Santos, Netto, and Biscainho (2004) and analyzed in detail in [[sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music|Diniz et al. 2006]]. It combines the high channel selectivity of the [[concepts/fast-filter-bank|FFB]] with the constant-$Q$ geometric frequency distribution of the [[concepts/constant-q-transform|CQT]].

## Overview

In the CQT, each geometrically spaced bin uses a different window length $N_k$. The CQFFB replaces this scheme with **filters of varying bandwidth** centered at the CQT bin frequencies:

- The CQT bin frequencies become the **center frequencies** of the CQFFB filters.
- The distance between two CQT neighbor bins becomes **one CQFFB filter bandwidth**.
- Each filter is a high-selectivity [[concepts/fast-filter-bank|FFB]] filter.

## Design Procedure

1. Given the desired $Q$, design an FFB with the minimum integer $L$ such that $N = 2^L \geq 2Q$ channels, and take the filter at channel index $Q$.
2. For each CQFFB channel $k$, either:
   - **Resampling implementation**: resample the input so that the new sampling frequency $f_s(k) = (N/Q)\, f_{\min}\, r^{k-1}$ moves the desired band into the FFB passband, then filter with the chosen FFB filter. The center-frequency ratio between contiguous channels is

     $$
     r = \frac{2 + 1/Q^2 + (1/Q)\sqrt{4 + 1/Q^2}}{2}.
     $$

     The resampling cost dominates this implementation.
   - **Direct implementation** (omits resampling): yields a lower-cost variant; total cost

     $$
     C_{\text{CQFFB,Total}} = \sum_{k=q_1}^{q_2} \left( C_Q\, r^{-k} + 1 \right),
     $$

     where $q_1 = \lfloor \log_r(2^{-D}(N/2Q)) \rfloor$, $q_2 = \lfloor \log_r(N/2Q) \rfloor$, and $D$ is the number of octaves.

## Properties

- **Geometric frequency spacing**: matches the equal-tempered musical scale.
- **High channel selectivity**: ~56 dB worst-case sidelobe attenuation (FFB-level).
- **High computational cost**: at typical channel counts (100–320 channels over a 10-octave spectrum), the CQFFB requires **~5 orders of magnitude more** complex multiplications than the [[concepts/bounded-q-fast-filter-bank|BQFFB]] for the same selectivity (see Figure 6 of [[sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music|Diniz et al. 2006]]).
- **Non-invertible**: direct resynthesis requires a synthesis filter bank approximating perfect reconstruction (inherited from the CQT).

## Role in the Paper

The CQFFB is presented as a high-resolution (but expensive) variant of the CQT. Its main role in the paper is as a **building block** for the [[concepts/bounded-q-fast-filter-bank|BQFFB]]: a small CQFFB with only 10 output channels (one per octave of the human auditory range) is used to perform octave separation in the BQFFB. Because the channel count is small (10), this stage is computationally cheap, while the per-octave FFB provides the high-selectivity intra-octave channels.

## Applications

Well suited to **automatic music transcription (AMT)**, where the geometric spacing makes the detection of musical notes homogeneous along the spectrum and the high selectivity helps separate notes and their harmonics. However, in polyphonic AMT, the linear spacing of harmonics within a note must be handled separately (e.g., by sufficient intra-octave granularity in the BQFFB).

## Related Concepts

- [[concepts/constant-q-transform|Constant-Q Transform (CQT)]]
- [[concepts/bounded-q-transform|Bounded-Q Transform (BQT)]]
- [[concepts/bounded-q-fast-filter-bank|Bounded-Q Fast Filter Bank (BQFFB)]]
- [[concepts/fast-filter-bank|Fast Filter Bank (FFB)]]
- [[concepts/frequency-response-masking|Frequency Response Masking (FRM)]]

## Related Sources

- [[sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music|Diniz, Kothe, Netto & Biscainho 2006: High-Selectivity Filter Banks for Spectral Analysis of Music Signals]]
