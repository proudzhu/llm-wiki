---
type: concept
created: 2026-07-23
updated: 2026-07-23
tags:
  - spectral-analysis
  - filter-banks
  - music-signal-processing
  - piecewise-linear-frequency-spacing
---

# Bounded-Q Transform (BQT)

The **Bounded-Q Transform (BQT)**, proposed by Kashima and Mont-Reynaud (1985), is a fast approximation of the [[concepts/constant-q-transform|Constant-Q Transform (CQT)]] in which only the octaves are geometrically spaced, while the channels inside each octave are linearly spaced. The resulting **piecewise-linear frequency grid** is a good approximation to the full geometric grid when the number of channels per octave is chosen appropriately. The original algorithm is described in [[sources/kashima-1985-bounded-q-frequency-transform|Kashima & Mont-Reynaud 1985]].

## Overview

The CQT distributes channels with strictly geometric spacing, which matches the musical scale but is computationally expensive. The BQT trades the strict geometric spacing for a piecewise-linear one:

- **Octaves** are geometrically spaced (factor-of-2 center-frequency progression).
- **Within each octave**, channels are uniformly (linearly) spaced.

This allows the BQT to use standard (fast) DFT machinery inside each octave while preserving the musical-scale-like octave-level spacing.

## Bandwidth Comparison with CQT

For a CQT with $R$ channels per octave starting at $f_0$, the per-channel bandwidth inside the octave is

$$
BW_{\text{CQ}}(k) = f_0 \left[ \left(\sqrt[R]{2}\right)^k - \left(\sqrt[R]{2}\right)^{k-1} \right], \quad k = 1, \ldots, R.
$$

For a BQT with $N = 2^L$ linearly spaced channels per octave, the bandwidth is constant:

$$
BW_{\text{BQ}} = \frac{f_0}{N}.
$$

Matching the BQT bandwidth to the **narrowest** CQT bandwidth (the lowest channel within the octave) gives the minimum number of BQT channels per octave needed to dominate the CQT:

$$
N_{\min} = 2^{\lceil \log_2(1 / (\sqrt[R]{2} - 1)) \rceil}.
$$

For quartertone resolution $R = 24$, $N_{\min} = 64$ — though $N = 32$ is shown in practice to suffice, as only 3 of the 24 CQFFB channels are narrower than their BQFFB counterparts.

## Properties

- **Piecewise-linear frequency spacing**: octaves geometric, intra-octave linear.
- **Medium computational complexity**: cheaper than CQT, more expensive than FFT/FFB.
- **Low channel selectivity**: inherited from FFT-based design — ~13 dB sidelobe rejection (same limitation as the CQT).
- **Invertible** (unlike the CQT): the original Kashima & Mont-Reynaud (1985) algorithm uses a sharp ~80 dB lowpass cutoff in the octave-separation step, which allows the original signal to be reconstructed nearly distortion-free by reversing the split-and-downsample procedure. This invertibility is a by-product of the implementation rather than of the piecewise-linear grid itself.

## Relation to Other Tools

The BQT is the **piecewise-linear-frequency-spacing parent** of the BQFFB, the high-selectivity variant introduced in [[sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music|Diniz et al. 2006]]. The BQFFB replaces the BQT's low-selectivity FFT kernel with a high-selectivity [[concepts/fast-filter-bank|FFB]] kernel while keeping the piecewise-linear octave/channel structure.

## Related Concepts

- [[concepts/constant-q-transform|Constant-Q Transform (CQT)]]
- [[concepts/bounded-q-fast-filter-bank|Bounded-Q Fast Filter Bank (BQFFB)]]
- [[concepts/constant-q-fast-filter-bank|Constant-Q Fast Filter Bank (CQFFB)]]
- [[concepts/fast-filter-bank|Fast Filter Bank (FFB)]]

## Related Sources

- [[sources/kashima-1985-bounded-q-frequency-transform|Kashima & Mont-Reynaud 1985: The Bounded-Q Frequency Transform]] — the original paper introducing the BQT, including the iterative FFT + downsample algorithm, frequency-domain lowpass filtering, dovetailing, and the invertibility property.
- [[sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music|Diniz, Kothe, Netto & Biscainho 2006: High-Selectivity Filter Banks for Spectral Analysis of Music Signals]] — extends the BQT into the high-selectivity BQFFB.
