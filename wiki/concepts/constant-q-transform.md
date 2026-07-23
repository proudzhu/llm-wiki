---
type: concept
created: 2026-07-23
updated: 2026-07-23
tags:
  - spectral-analysis
  - filter-banks
  - music-signal-processing
  - geometric-frequency-spacing
---

# Constant-Q Transform (CQT)

The **Constant-Q Transform (CQT)**, introduced by Brown (1991), is a spectral analysis tool in which the channel center frequency $f_k$ and the channel bandwidth $\Delta f_k$ are tied by a constant ratio $Q = f_k / \Delta f_k$. As a result, **channels are geometrically spaced** along frequency — matching the geometric spacing of musical notes in the Western equal-tempered scale.

## Overview

In the standard short-time DFT, the window length $N$ is the same for every bin, producing a uniform linear frequency grid. In the CQT, each bin uses its own window length $N_k$:

$$
N_k = \frac{f_s}{\Delta f_k} = \frac{f_s}{f_k}\, Q,
$$

so the channel bandwidth grows proportionally with $f_k$, keeping the quality factor $Q$ constant across the spectrum.

The $k$-th CQT spectral component is

$$
X_{\text{CQ}}[k] = \frac{1}{N_k} \sum_{n=0}^{N_k - 1} w[n, k]\, x[n]\, e^{-j 2 \pi k n / N_k}.
$$

## Why It Matters for Music

Notes in the equal-tempered scale follow a geometric progression with ratio $\sqrt[12]{2} \approx 1.06$ per semitone. With a linear FFT grid, discriminating low-pitched notes requires a resolution that is wasteful at high frequencies, while a resolution suited for high pitches is insufficient at low pitches. The geometric spacing of the CQT maps contiguous notes to **equally spaced CQT bins**, making the detection of musical notes homogeneous along the spectrum.

For quartertone resolution, $Q \approx 34.6$ (rounded to 35):

$$
Q = \frac{f_k}{(\Delta f)_{\text{CQ}}} = \frac{f_k}{(2^{1/48} - 2^{-1/48})\, f_k} \approx \frac{1}{0.0289} \approx 34.6.
$$

## Limitations

- **High computational cost**: each bin uses a different DFT length, and even the fast implementation by Brown & Puckette (1992) is much heavier than the FFT.
- **Low selectivity**: the CQT inherits the FFT's ~13 dB sidelobe rejection — the same interchannel-interference problem.
- **Non-invertible**: direct signal resynthesis requires a synthesis filter bank that can only approximate perfect reconstruction.

## Relation to Other Tools

The CQT is the **geometric-frequency-spacing parent** of two families:

- **CQFFB** (high-selectivity variant) — [[concepts/constant-q-fast-filter-bank|Constant-Q Fast Filter Bank]]: replaces CQT's variable windows with variable-bandwidth FFB filters.
- **BQT** (low-cost variant) — [[concepts/bounded-q-transform|Bounded-Q Transform]]: approximates the geometric grid by a piecewise-linear one.

## Related Concepts

- [[concepts/bounded-q-transform|Bounded-Q Transform (BQT)]]
- [[concepts/constant-q-fast-filter-bank|Constant-Q Fast Filter Bank (CQFFB)]]
- [[concepts/bounded-q-fast-filter-bank|Bounded-Q Fast Filter Bank (BQFFB)]]
- [[concepts/fast-filter-bank|Fast Filter Bank (FFB)]]

## Related Sources

- [[sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music|Diniz, Kothe, Netto & Biscainho 2006: High-Selectivity Filter Banks for Spectral Analysis of Music Signals]]
