---
type: concept
created: 2026-07-23
updated: 2026-07-23
tags:
  - filter-banks
  - high-selectivity
  - frequency-response-masking
  - linear-phase
---

# Fast Filter Bank (FFB)

The **Fast Filter Bank (FFB)** is a high-selectivity filter bank structure proposed by Lim and Farhang-Boroujeny (1992) that inherits the modular tree-like (radix-2) structure of the [[concepts/frequency-response-masking|FFT filter bank]] but replaces its low-order kernel filter with distinct higher-order kernels designed via [[concepts/frequency-response-masking|Frequency Response Masking (FRM)]].

## Overview

When the FFT is interpreted as an $N = 2^L$ channel filter bank (the sliding FFT, sFFT), each channel is built by cascading $L$ instances of the simple kernel $H(z) = 1 + z^{-1}$. This yields very low cost ($C_{\text{FFT}} = 1$ complex multiplication per channel per input sample) but only ~13 dB sidelobe rejection, which causes interchannel interference when adjacent frequency components must be discriminated (e.g., musical notes/harmonics).

The FFB keeps the same tree topology but uses, at each cascade level $l$, a distinct higher-order kernel filter designed via FRM. The result is a linear-phase filter bank whose channels exhibit very steep passband-stopband transitions, attaining ~56 dB attenuation at the worst-case sidelobes — roughly 43 dB better than the FFT — at approximately twice the FFT cost:

$$
C_{\text{FFB}}(l) = \frac{2N + 23}{N} \approx 2 \text{ complex multiplications per channel per input sample (for } l \geq 5 \text{)}.
$$

## Tree Structure

Each channel is the cascade of $L$ subfilters. At each node of the tree there is a prototype filter and its complementary filter; the latter halves the multiplication count by exploiting the symmetric tree decomposition. The kernel filter at level $l$ is built by replacing $z$ in $H(z)$ by $W_N^{-\tilde{b}}\, z^{2^{L-l-1}}$, where $\tilde{b}$ is the bit-reversed representation of the within-level filter index $b$.

A distinctive feature of the FFB is that the **singular FFB-filter stopbands** result from the cascade of several masking filters, each contributing its own distinct stopband response — which collectively yield the steep transition bands unattainable by a single windowed-FFT design.

## Filter Coefficient Budget

The accumulated number of distinct nonzero coefficients grows with cascade level $l$ as given in Table 1 of [[sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music|Diniz et al. 2006]]:

| Level $l$ | Distinct coef/filter | Prototype filters | Coef/level | Accumulated $C(l)$ |
|-----------|----------------------|--------------------|------------|---------------------|
| 1 | 7 | 1 | 7 | 7 |
| 2 | 6 | 2 | 12 | 19 |
| 3 | 3 | 4 | 12 | 31 |
| 4 | 3 | 8 | 24 | 55 |
| 5 | 2 | 16 | 32 | 87 |
| 6 | 2 | 32 | 64 | 151 |
| 7 | 2 | 64 | 128 | 279 |
| 8 | 2 | 128 | 256 | 535 |
| $\vdots$ | $\vdots$ | $\vdots$ | $\vdots$ | $\vdots$ |
| $\log_2 N$ | 2 | $N/2$ | $N$ | $2N + 23$ |

Beyond level 5, the budget saturates to ~$2N + 23$ coefficients. A matrix formulation of the FFB (Lim & Wei, 2004) provides a faster implementation path.

## Properties

- **Linear phase**: inherited from the FFT tree structure — no phase distortion on the signal.
- **Linear frequency spacing**: all channels share the same bandwidth.
- **High selectivity**: ~56 dB worst-case sidelobe attenuation, suitable for separating closely spaced tonal components.
- **Slightly higher complexity than FFT**: ~2× radix-2 FFT cost — a small price for the selectivity gain.

## Use as a Building Block

The FFB is the key selectivity-providing primitive for two novel tools introduced in [[sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music|Diniz et al. 2006]]:

- The [[concepts/constant-q-fast-filter-bank|CQFFB]] uses an FFB as a high-selectivity filter centered at each CQT bin frequency.
- The [[concepts/bounded-q-fast-filter-bank|BQFFB]] uses a small (typically 10-channel) CQFFB to separate octaves and an FFB inside each octave to provide linearly spaced high-selectivity channels.

## Related Concepts

- [[concepts/frequency-response-masking|Frequency Response Masking (FRM)]]
- [[concepts/constant-q-transform|Constant-Q Transform (CQT)]]
- [[concepts/bounded-q-transform|Bounded-Q Transform (BQT)]]
- [[concepts/constant-q-fast-filter-bank|Constant-Q Fast Filter Bank (CQFFB)]]
- [[concepts/bounded-q-fast-filter-bank|Bounded-Q Fast Filter Bank (BQFFB)]]

## Related Sources

- [[sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music|Diniz, Kothe, Netto & Biscainho 2006: High-Selectivity Filter Banks for Spectral Analysis of Music Signals]]
