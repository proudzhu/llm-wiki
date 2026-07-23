---
type: source
created: 2026-07-23
updated: 2026-07-23
sources:
  - raw/papers/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music/full-text.md
  - https://doi.org/10.1155/2007/94704
  - zotero://select/items/0_HSWGWJQ6
tags:
  - filter-banks
  - spectral-analysis
  - music-signal-processing
  - constant-q
  - bounded-q
  - frequency-response-masking
---

# Diniz, Kothe, Netto & Biscainho 2006: High-Selectivity Filter Banks for Spectral Analysis of Music Signals

> Filipe C. C. B. Diniz, Iuri Kothe, Sergio L. Netto, Luiz W. P. Biscainho

| Field | Value |
|-------|-------|
| **Institutions** | LPS-PEE/COPPE and DEL/Poli, Universidade Federal do Rio de Janeiro (UFRJ), Brazil |
| **Venue** | EURASIP Journal on Advances in Signal Processing, 2007, Article ID 94704 |
| **Year** | 2006 (received Dec 2005; revised Aug 2006; accepted Sep 2006) |
| **Type** | Journal article |
| **DOI** | [10.1155/2007/94704](https://doi.org/10.1155/2007/94704) |
| **Recommended by** | Masataka Goto |
| **Zotero** | [Open in Zotero](zotero://select/items/0_HSWGWJQ6) |

## Summary

This paper presents a unified framework for spectral analysis of music signals, covering four established algorithms — FFT, [[concepts/fast-filter-bank|Fast Filter Bank (FFB)]], [[concepts/constant-q-transform|Constant-Q Transform (CQT)]], and [[concepts/bounded-q-transform|Bounded-Q Transform (BQT)]] — and introducing two novel high-selectivity variants: the [[concepts/constant-q-fast-filter-bank|Constant-Q Fast Filter Bank (CQFFB)]] and the [[concepts/bounded-q-fast-filter-bank|Bounded-Q Fast Filter Bank (BQFFB)]]. The BQFFB is the central contribution, combining the FFT-like low complexity, the BQT-like piecewise-linear frequency distribution suited to music, and the FFB-like high channel selectivity. In typical configurations (100–320 channels over a 10-octave spectrum), the BQFFB achieves roughly **five orders of magnitude reduction in computational complexity** over the CQFFB while preserving the same selectivity performance, making it an attractive tool for automatic music transcription and music feature extraction.

## Problem Formulation

Spectral analysis of music signals is constrained by three competing requirements:

1. **Efficient frequency distribution** — Western equal-tempered scale notes are geometrically spaced, so a uniform (linear) channel grid wastes resolution at high frequencies while lacking it at low frequencies.
2. **Reduced computational complexity** — needed for real-time and large-scale music information retrieval.
3. **High channel selectivity** — needed to discriminate adjacent notes/harmonics without interchannel interference.

No existing single tool satisfies all three simultaneously: the FFT is cheap but poorly selective; the FFB is selective but linearly spaced; the CQT is geometrically spaced but expensive; the BQT trades the strict geometric spacing for piecewise-linear to lower cost but still lacks selectivity.

The short-time DFT (basis of FFT/CQT/BQT) is

$$
X[k] = \frac{1}{N} \sum_{n=0}^{N-1} w[n]\, x[n]\, e^{-j 2 \pi k n / N}
$$

and the constant-Q constraint $Q = f_k / \Delta f_k = \text{const}$ implies a per-channel window length $N_k = (f_s / f_k) Q$.

## Methodology

The paper organizes six spectral analysis tools along two axes: (i) frequency spacing (linear / geometric / piecewise-linear) and (ii) channel selectivity (low = FFT-based, high = FFB-based).

### Linear Frequency Spacing

- **FFT / sliding FFT (sFFT)**: Tree-structured $N = 2^L$ channel bank with kernel $H(z) = 1 + z^{-1}$; ~13 dB sidelobe rejection; cost $C_{\text{FFT}} = 1$ complex multiplication per channel per input sample.
- **FFB** (Lim & Farhang-Boroujeny, 1992): Same tree structure but each level uses a distinct higher-order kernel designed via [[concepts/frequency-response-masking|Frequency Response Masking (FRM)]]; ~56 dB sidelobe rejection at approximately twice the FFT cost ($C_{\text{FFB}} \approx 2$).

### Geometric Frequency Spacing

- **CQT** (Brown, 1991): DFT evaluated with per-channel window length $N_k = (f_s/f_k) Q$; channels geometrically spaced, ideal for the equal-tempered scale, but high computational cost.
- **CQFFB** (novel): Replaces CQT's variable windows with variable-bandwidth FFB filters centered at CQT bin frequencies. Two implementations are given (resampling-based, and direct). Total cost:

$$
C_{\text{CQFFB,Total}} = \sum_{k=q_1}^{q_2} \left( C_Q\, r^{-k} + 1 \right),
$$

where $r = (2 + 1/Q^2 + (1/Q)\sqrt{4 + 1/Q^2})/2$ is the contiguous-channel center-frequency ratio.

### Piecewise-Linear Frequency Spacing

- **BQT** (Kashima & Mont-Reynaud, 1985): Octaves geometrically spaced, channels inside each octave linearly spaced. Reduces CQT cost while approximating the geometric grid.
- **BQFFB** (novel, central contribution): Uses a CQFFB to separate the input into $D$ octaves (typically $D = 10$ for the human auditory range) and applies an FFB within each octave. The octave-separation filter procedure is:

  1. Take the second filter of a 2-channel FFB as the highest-octave filter.
  2. For each remaining octave $d = (D-1), \ldots, 1$, cascade the second filter of a $2^{(D-d+1)}$-channel FFB with the first filter of a $2^{(D-d)}$-channel FFB.

  After octave separation, each octave is downsampled by $2^{(D-d+1)}$ and submitted to a $2N$-channel FFB. The high-selectivity FFB octave-separation filters themselves provide anti-aliasing, **avoiding the need for additional decimation filters** — a key improvement over the earlier BQFFB concept in reference [9] of the paper. The total cost is:

$$
C_{\text{BQFFB,Total}} = \left( F(D) + D \right) + 2\, C(l)\, D,
$$

  where $F(D)$ is the accumulated coefficient count for octave separation (Table 2 of the paper) and $C(l)$ comes from the per-level FFB coefficient table.

A summary of all six tools appears in Table 3 of the paper.

| Tool | Frequency Spacing | Selectivity | Complexity |
|------|-------------------|-------------|------------|
| FFT | Linear | Low | Low |
| FFB | Linear | High | Low (*) |
| CQT | Geometric | Low | High |
| CQFFB | Geometric | High | High (*) |
| BQT | Piecewise Linear | Low | Medium |
| BQFFB | Piecewise Linear | High | Medium (*) |

(*) FFB-based tools are slightly more complex than FFT-based counterparts.

### Practical Parameter Choices

For quartertone resolution ($R = 24$ channels per octave) the constant-Q factor is $Q \approx 34.6$ (rounded to 35). The minimum bounded-Q channels per octave from $N_{\min} = 2^{\lceil \log_2(1/(\sqrt[R]{2} - 1)) \rceil}$ is 64, but $N = 32$ is shown to suffice in practice since only 3 of 24 CQFFB channels are narrower than their BQFFB counterparts.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Sampling rate** | 44100 Hz |
| **Spectrum analyzed** | 0–22050 Hz |
| **Number of octaves** | $D = 7$ to $10$ (10-octave human auditory range for complexity comparison) |
| **Channels per octave (BQFFB)** | $N = 32$ |
| **Total channels (FFT/FFB)** | 4096 (5.38 Hz wide each, to satisfy quartertone at the lowest test tone) |
| **Q factor (CQFFB)** | 35 (quartertone) |
| **Test signals** | (1) 1-second sum of 8 pure tones (C4=263 Hz, D4=295 Hz slightly detuned, plus 3 harmonics each); (2) 4-second extract of an organ work by Cesar Franck containing an A-Major chord (A3, E4, A4, C#5, E5, C#6) plus A0 pedal bass; (3) Bach flute excerpt (BWV 1013, Corrente); (4) Shostakovich piano excerpt (Prelude op. 34/5) |
| **Baselines** | FFT, FFB, CQFFB |

## Results

### Synthetic Two-Note Signal

- **FFT**: detects tones but with a visible noise floor around them due to ~13 dB sidelobe rejection; this can mask medium-level tones in real signals.
- **FFB**: clearly detects peaks at the same unnecessarily large channel count as FFT.
- **CQFFB**: identifies tones with fewer channels but at considerably higher computational cost.
- **BQFFB**: matches FFB selectivity at roughly five orders of magnitude lower complexity than the CQFFB.

### Real Organ Recording (Cesar Franck)

- All four tools discriminate the A-Major chord components (220 Hz, 329.63 Hz, 440 Hz, 554.37 Hz, 659.26 Hz, 1108.73 Hz) plus the 27.5 Hz pedal bass and its harmonics.
- FFT output is noisy, masking some information.
- FFB requires excessively many channels; CQFFB requires excessive computation; BQFFB is the best compromise.
- Harmonics of the lowest note (27.5 Hz spacing) were detected **only** by the FFB-based tools (FFB, CQFFB, BQFFB), not by the FFT.

### Time-Varying Real Audio

- BQFFB analyses of a Bach flute solo and a Shostakovich piano prelude show clear discrimination of note harmonics, vibrato, trill (after 2.5 s in the flute), legato overlaps (piano right hand at ~13 notes/s), and bass resonance.

### Complexity Comparison

For a 10-octave spectrum, the BQFFB outperforms the CQFFB by about **five orders of magnitude** in number of complex multiplications for typical channel counts (100–320 channels). See Figure 6 of the paper.

## Key Contributions

1. **Unified framework** for the spectral analysis of music signals covering FFT, FFB, CQT, and BQT under a single structural perspective, exposing the orthogonal axes of frequency spacing and channel selectivity.
2. **Introduction of the CQFFB**, a high-selectivity, geometrically spaced filter bank combining FFB selectivity with the CQT frequency distribution; identified as a high-resolution but computationally expensive variant.
3. **Introduction of the BQFFB**, a high-selectivity, piecewise-linearly spaced filter bank combining the best properties of FFT (low complexity), BQT (efficient frequency distribution), and FFB (high selectivity).
4. **Improved BQFFB implementation** that eliminates the decimation filters required by the earlier BQFFB concept (reference [9]), by exploiting the high-selectivity FFB octave-separation filters themselves as anti-aliasing filters.
5. **Quantitative complexity analysis** showing the BQFFB attains a ~5-order-of-magnitude cost reduction over the CQFFB at typical channel counts.
6. **Music-oriented validation** through synthetic-tone, real-organ, flute, and piano experiments confirming that the BQFFB matches FFB selectivity at a fraction of the cost.

## Related Concepts

- [[concepts/fast-filter-bank|Fast Filter Bank (FFB)]]
- [[concepts/constant-q-transform|Constant-Q Transform (CQT)]]
- [[concepts/bounded-q-transform|Bounded-Q Transform (BQT)]]
- [[concepts/constant-q-fast-filter-bank|Constant-Q Fast Filter Bank (CQFFB)]]
- [[concepts/bounded-q-fast-filter-bank|Bounded-Q Fast Filter Bank (BQFFB)]]
- [[concepts/frequency-response-masking|Frequency Response Masking (FRM)]]

## Related Synthesis

_(No synthesis pages yet reference this paper. Candidates for future synthesis: comparison of high-selectivity spectral analysis tools for music/audio; filter bank design techniques for music information retrieval.)_
