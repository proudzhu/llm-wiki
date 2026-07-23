---
type: source
created: 2026-07-23
updated: 2026-07-23
sources:
  - raw/papers/kashima-1985-bounded-q-frequency-transform/full-text.md
  - https://www.ee.columbia.edu/~dpwe/papers/KashMR85-bQ-stanm28.pdf
  - zotero://select/items/0_U5AP27SH
tags:
  - spectral-analysis
  - filter-banks
  - music-signal-processing
  - constant-q
  - bounded-q
  - polyphonic-music-transcription
  - fft
  - downsampling
---

# Kashima & Mont-Reynaud 1985: The Bounded-Q Frequency Transform

> Kyle L. Kashima, Bernard Mont-Reynaud

| Field | Value |
|-------|-------|
| **Institutions** | Center for Computer Research in Music and Acoustics (CCRMA), Department of Music, Stanford University |
| **Venue** | Department of Music Report STAN-M-28 |
| **Year** | 1985 |
| **Type** | Technical report (departmental report series) |
| **URL** | [KashMR85-bQ-stanm28.pdf](https://www.ee.columbia.edu/~dpwe/papers/KashMR85-bQ-stanm28.pdf) |
| **Zotero** | [Open in Zotero](zotero://select/items/0_U5AP27SH) |
| **Acknowledgements** | Julius O. Smith III (guidance), Chris Chafe, Andrew Schloss, David Jaffe, Phil Gossett |
| **Funding** | NSF grants MCS-8012476 and DCR-8214350 |

## Summary

This report introduces the **Bounded-Q Transform (BQT)**, an FFT-based front-end spectral analyzer developed for the intelligent music-transcription system at CCRMA. The BQT is a compromise between the linear spacing of a single FFT and the geometric spacing of a [[concepts/constant-q-transform|Constant-Q Transform (CQT)]]: filters are *linearly* spaced within an octave but stand in a 2:1 ratio from octave to octave, so the Q values are *bounded* within a fixed one-octave range rather than held constant across the spectrum. The algorithm achieves roughly **three orders of magnitude lower computational cost** than an equivalent DFT-based constant-Q filter bank by combining a fixed-size FFT with iterative factor-of-2 downsampling and frequency-domain lowpass filtering.

## Problem Formulation

Transcription of digitally recorded polyphonic Western music requires a spectral analysis front end that can resolve overlapping partials, time-varying spectra, and time-varying tempi. The well-tempered 12-tone chromatic scale places note fundamentals at geometric intervals of $2^{n/12}$, and harmonic instruments produce partials at approximately integer multiples of the fundamental that fall within a few percent of a semitone of the scale tones. An ideal analyzer would therefore be a **constant-Q filter bank** with bandwidth proportional to center frequency, since:

1. The proportional bandwidth matches the geometric musical scale.
2. The inversely proportional time window matches the physical fact that high-frequency partials of harmonic instruments attack and decay faster than low-frequency ones.

The difficulty is computational: a constant-Q filter bank requires a *separate* DFT for each (differently sized) windowed sinusoid, which is too expensive on a serial processor. Frequency-warping of a single FFT and the chirp-z transform were considered but were not easily applicable to the requirements of the CCRMA transcription system.

## Methodology

### The Bounded-Q Compromise

The BQT keeps octave-to-octave geometric spacing (2:1 center-frequency ratio) but uses linear spacing within each octave. Filters exactly an octave apart share the same Q, and the Q values across the spectrum span only a fixed 2:1 range — hence "bounded-Q."

![[raw/papers/kashima-1985-bounded-q-frequency-transform/figures/5316814a104910640b148c00831b0dc2a9df536f00685ce193b2ea7aa6b81c85.jpg|Comparison of filter spacings]]
*Figure 1: Filter spacings — linear (FFT), geometric (constant-Q), and piecewise-linear (bounded-Q).*

A minimum of **three filters per semitone** is used so that a note excites more than one filter even when the music's absolute tuning is unknown, avoiding ambiguous frequency results from spectral smearing or noise.

### Iterative FFT + Downsample Procedure

The algorithm centers on an iterative procedure (Figure 2):

1. Group input into blocks of 256 samples; zero-pad to 512 and take a 512-point FFT (zero padding prevents aliasing during the subsequent downsampling).
2. Output the **upper half** of the FFT (one octave, 32 complex points) to the music-analysis system.
3. Lowpass the signal by complex-multiplying the FFT spectrum with the frequency response of a halfband FIR, then inverse-FFT back to the time domain.
4. Downsample by a factor of 2 (drop every other sample).
5. Dovetail the downsampled output (including pre-/post-ringing from the filter) with the corresponding samples from the previous and following iterations.
6. Repeat on the downsampled data: the next iteration produces the next-lower octave with twice the window size and twice the frequency resolution, while the FFT size stays fixed at 512.

![[raw/papers/kashima-1985-bounded-q-frequency-transform/figures/073d97069d5e8260c8d8ad412a176fdcca91f00dc2e48c7a920701e6de8c0702.jpg|Central procedure of the algorithm]]
*Figure 2: The central FFT → output upper octave → frequency-domain lowpass → downsample → repeat procedure.*

Because downsampling halves the sample rate while the window doubles, the FFT length remains constant across octaves. The hop size is one full data group (256 samples); halving it would double the cost for better time resolution.

### Frequency-Domain Lowpass Filtering

A key efficiency trick: rather than convolving the input with a 256-tap FIR in the time domain ($256 \times 256 = 65{,}536$ real multiplications), the algorithm performs the lowpass in the frequency domain by complex-multiplying the already-computed FFT with the filter's frequency response, then inverse-FFTing. This costs $257$ complex multiplications plus $2304$ butterflies for the inverse FFT — about $2561$ complex operations, a substantial saving. The filter is a 256-point symmetric non-causal FIR with approximately 80 dB stopband attenuation. The zero-padding in step 1 absorbs the filter's pre-/post-ringing without aliasing.

### Dovetailing

The energy spread by the non-trivial lowpass filter (pre-ring and post-ring) is *saved* and combined with the appropriate downsampled samples from neighboring iterations (Figure 3), reproducing exactly what a time-domain FIR convolution would have produced. Three downsampled streams are dovetailed into one before the next octave is processed.

![[raw/papers/kashima-1985-bounded-q-frequency-transform/figures/ac1d883dd71cf39dbe42239b29eb17cdc8fb7ffd89b376dba62f5ce8c35657b8.jpg|Diagram of algorithm output]]
*Figure 4: Octave-by-octave output order of the algorithm (numbers indicate execution order).*

### Invertibility

Because the lowpass filter has a sharp cutoff, the procedure is **invertible**: the original signal can be reconstructed nearly distortion-free by reversing the octave-splitting and downsampling steps. This is an incidental benefit not present in the standard CQT.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Sampling rate** | 22028 Hz |
| **Input block size** | 256 samples |
| **FFT size** | 512 (256 zero-padded) |
| **First time window** | 11.62 ms |
| **Output per octave** | 32 complex points |
| **Filter spacing** | 2.72 filters/semitone (low end) to 5.28 filters/semitone (high end) |
| **Lowpass filter** | 256-point symmetric non-causal FIR, ~80 dB cutoff |
| **Hop size** | 256 samples (one data group) |
| **Windowing** | None (rectangular) — windowing would complicate the downsampling; can be applied by spectral convolution if needed |
| **Target application** | Front end for the CCRMA intelligent polyphonic music-transcription system |

The report does not include a quantitative evaluation on musical test signals; the analysis is an algorithmic and computational-cost study. The authors note that further work would determine whether the generated spectra suffice for accurate transcription.

## Results

### Computational Efficiency

Per iteration of the central procedure:

| Stage | Complex operations |
|-------|-------------------|
| Forward FFT (512-point) | $n/2 \log_2 n = 2304$ |
| Frequency-domain lowpass | $n/2 + 1 = 257$ |
| Inverse FFT (512-point) | $2304$ |
| **Total per iteration** | $4865 = n \log_2 n + n + 1$ |

Because each lower octave is computed on data downsampled by 2, the average cost over a fixed time interval converges as a geometric series $[1 + \tfrac{1}{2} + \tfrac{1}{4} + \dots]$, giving an average of **~9730 complex operations per data-set interval**.

| Method | Operations per data-set interval |
|--------|----------------------------------|
| **BQT** | ~9 730 |
| DFT filter bank (32 filters/octave × 6 octaves = 192 filters) | $192 \times 256^2 \approx 12.6 \times 10^6$ |
| DFT filter bank with per-octave downsampling | $\approx 4.2 \times 10^6 + 2L$ |

The BQT is therefore roughly **three orders of magnitude cheaper** than a direct DFT constant-Q filter bank, and still substantially cheaper than a DFT filter bank that uses downsampling. The sharp lowpass cutoff additionally enables near-distortion-free **invertibility**, a property not offered by the standard CQT.

## Key Contributions

1. **Introduced the Bounded-Q Transform (BQT)** — a piecewise-linear frequency grid (linear within an octave, geometric across octaves) that approximates the constant-Q grid at a fraction of the cost. This is the foundational paper for the BQT concept later extended by [[sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music|Diniz et al. 2006]].
2. **Iterative FFT + factor-of-2 downsampling algorithm** that keeps the FFT size fixed across octaves while doubling the effective window length, yielding logarithmic time-resolution scaling matched to harmonic-instrument physics.
3. **Frequency-domain lowpass filtering** via complex multiplication on the already-computed FFT spectrum plus an inverse FFT — replacing time-domain FIR convolution and yielding a ~25× per-stage saving.
4. **Dovetailing** of downsampled streams across iterations to correctly account for filter pre-/post-ringing, exactly reproducing the time-domain convolution result.
5. **Computational-cost analysis** showing ~3 orders of magnitude speedup over the equivalent DFT filter bank (and over a downsampled DFT bank), at ~9730 complex operations per data-set interval.
6. **Invertibility** of the transform as a by-product of the sharp lowpass cutoff — enabling near-distortion-free signal reconstruction.

## Related Concepts

- [[concepts/bounded-q-transform|Bounded-Q Transform (BQT)]] — the central concept introduced by this paper
- [[concepts/constant-q-transform|Constant-Q Transform (CQT)]] — the geometrically spaced baseline that the BQT approximates
- [[concepts/bounded-q-fast-filter-bank|Bounded-Q Fast Filter Bank (BQFFB)]] — the high-selectivity successor by Diniz et al. 2006

## Related Synthesis

_(No synthesis pages yet reference this paper. Candidate: a comparison of constant-Q, bounded-Q, and their fast-filter-bank successors for music spectral analysis — this paper provides the original BQT cost baseline.)_
