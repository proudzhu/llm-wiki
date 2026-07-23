---
type: concept
created: 2026-07-23
updated: 2026-07-23
tags:
  - filter-banks
  - high-selectivity
  - piecewise-linear-frequency-spacing
  - music-signal-processing
  - low-complexity
---

# Bounded-Q Fast Filter Bank (BQFFB)

The **Bounded-Q Fast Filter Bank (BQFFB)** is a high-selectivity, piecewise-linearly spaced filter bank for music signal analysis, and the central contribution of [[sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music|Diniz et al. 2006]]. It combines three desirable properties:

- **FFT-like low computational complexity**,
- **BQT-like piecewise-linear (octave-geometric, intra-octave linear) frequency distribution**, well-suited to the equal-tempered musical scale, and
- **FFB-like high channel selectivity** (~56 dB worst-case sidelobe attenuation).

## Overview

The BQFFB combines a small [[concepts/constant-q-fast-filter-bank|CQFFB]] for octave separation with a per-octave [[concepts/fast-filter-bank|FFB]] for intra-octave channelization:

1. **Octave separation**: A CQFFB with $D$ output channels (typically $D = 10$ for the human auditory range) splits the input into geometrically spaced octaves.
2. **Intra-octave channelization**: Each octave signal is downsampled by $2^{(D-d+1)}$ and submitted to a $2N$-channel FFB, producing $N$ linearly spaced channels per octave (the FFB also generates the negative part of the filter responses, hence the $2N$).

## Octave-Separation Filter Design

The octave-separation filter procedure is:

1. The **highest octave** ($d = D$) filter is the second filter of a 2-channel FFB. (It is wider than necessary because the input is real, so the band is limited to the left half of the spectrum.)
2. For each remaining octave $d = (D-1), \ldots, 1$: cascade the **second filter of a $2^{(D-d+1)}$-channel FFB** with the **first filter of a $2^{(D-d)}$-channel FFB**.

The constraints come from the octave band edges: octave $D-1$ must be lower bounded by $\pi/4$ and upper bounded by $\pi/2$, which is reached by combining the lowpass filter of octave $D$ with the bandpass filter of octave $D-1$.

The accumulated number of nonzero coefficients $F(D)$ for octave separation grows as (Table 2 of [[sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music|Diniz et al. 2006]]):

| Octaves $D$ | Octave $d$ | Coef/octave | Accumulated $F(D)$ |
|--------------|------------|-------------|---------------------|
| 1 | $D$ | 7 | 7 |
| 2 | $D-1$ | 6 | 13 |
| 3 | $D-2$ | 3 | 16 |
| 4 | $D-3$ | 3 | 19 |
| 5 | $D-4$ | 2 | 21 |
| 6 | $D-5$ | 2 | 23 |
| 7 | $D-6$ | 2 | 25 |
| 8 | $D-7$ | 2 | 27 |
| 9 | $D-8$ | 2 | 29 |
| 10 | $D-9$ | 2 | 31 |

## Anti-Aliasing Without Decimation Filters (Key Improvement)

A key contribution of [[sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music|Diniz et al. 2006]] is **eliminating the additional decimation filters** required by the earlier BQFFB concept (Diniz et al., ITS 2006). The high-selectivity FFB octave-separation filters themselves are sufficient to prevent aliasing after the per-octave downsampling, so the per-octave downsampling can be performed directly — yielding **negligible added complexity** compared to the earlier implementation while improving frequency discrimination.

## Computational Complexity

The total cost of the BQFFB is

$$
C_{\text{BQFFB,Total}} = \left( F(D) + D \right) + 2\, C(l)\, D,
$$

where $F(D)$ is the accumulated octave-separation coefficient count (table above) and $C(l)$ is the per-level FFB coefficient count from the [[concepts/fast-filter-bank|FFB]] table.

For a 10-octave spectrum at typical channel counts (100–320 channels), the BQFFB requires roughly **five orders of magnitude fewer complex multiplications** than the [[concepts/constant-q-fast-filter-bank|CQFFB]] at the same selectivity.

## Properties

- **Piecewise-linear frequency spacing**: octave-level geometric, intra-octave linear.
- **High channel selectivity**: ~56 dB worst-case sidelobe attenuation (FFB-level).
- **Medium computational complexity**: between FFT/FFB and CQT/CQFFB; ~5 orders of magnitude lower than CQFFB at typical channel counts.
- **Not structurally invertible**: direct resynthesis requires a synthesis filter bank approximating perfect reconstruction (inherited from the BQT/CQT non-invertibility).

## Validation

Experiments on (i) synthetic pure-tone sums, (ii) a real organ recording (Cesar Franck, A-Major chord with A0 pedal), (iii) a Bach flute excerpt (BWV 1013, Corrente), and (iv) a Shostakovich piano excerpt (Prelude op. 34/5) confirm:

- BQFFB matches FFB selectivity at much lower cost and channel count.
- BQFFB detects low-pedal-bass harmonics (27.5 Hz spacing) that the FFT-based tools miss.
- BQFFB resolves note harmonics, vibrato, trill, legato overlaps, and bass resonance on real audio signals.

## Applications

Well suited to **automatic music transcription (AMT)** and **music feature extraction** as a music-oriented time-frequency representation producing $(\text{magnitude}, \text{frequency}) \times \text{time}$ outputs for downstream processing layers.

## Related Concepts

- [[concepts/bounded-q-transform|Bounded-Q Transform (BQT)]]
- [[concepts/constant-q-transform|Constant-Q Transform (CQT)]]
- [[concepts/constant-q-fast-filter-bank|Constant-Q Fast Filter Bank (CQFFB)]]
- [[concepts/fast-filter-bank|Fast Filter Bank (FFB)]]
- [[concepts/frequency-response-masking|Frequency Response Masking (FRM)]]

## Related Sources

- [[sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music|Diniz, Kothe, Netto & Biscainho 2006: High-Selectivity Filter Banks for Spectral Analysis of Music Signals]]
