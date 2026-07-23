---
type: concept
created: 2026-07-23
updated: 2026-07-23
sources:
  - raw/papers/harma-2000-frequency-warped-signal-processing/full-text.md
tags:
  - signal-processing
  - linear-prediction
  - frequency-warping
  - audio-coding
  - speech-coding
---

# Warped Linear Prediction

**Warped Linear Prediction (WLP)** is a variant of linear predictive coding (LPC) in which the unit-delay shift register is replaced by a chain of first-order [[concepts/all-pass-filter|all-pass filters]], yielding an all-pole spectral model whose resolution follows a nonuniform (typically Bark-like) frequency scale. WLP provides significantly finer low-frequency resolution than conventional LPC at the same model order, making it especially advantageous for wideband audio and speech coding.

## Key Formulations

The WLP prediction error filter is:

$$A(z) = 1 - \sum_{k=1}^{N} a_k D(z)^k$$

where $D(z) = \frac{z^{-1} - \lambda}{1 - \lambda z^{-1}}$ is the all-pass warping element, $\lambda$ is the warping parameter (e.g., $\lambda \approx 0.756$ at 44.1 kHz for Bark warping), and $N$ is the model order.

In the time domain, $D(z)^{-k}$ acts as a **generalized shift operator** $d_k[\cdot]$, and the minimum mean-square error estimate leads to normal equations of the Wiener–Hopf form:

$$E\{d_m[x(n)] d_0[x(n)]\} - \sum_{k=1}^{N} a_k E\{d_k[x(n)] d_m[x(n)]\} = 0$$

Because $D(z)$ is all-pass, the correlation terms are shift-invariant along the chain:

$$E\{d_m[x(n)] d_k[x(n)]\} = E\{d_{m+p}[x(n)] d_{k+p}[x(n)]\}$$

This means the **Levinson–Durbin algorithm** can be used to solve for the coefficients $a_k$ efficiently, exactly as in conventional LPC. The correlation values are computed via a **warped autocorrelation network** — an all-pass chain that produces the warped autocorrelation taps continuously from the input.

### Spectral Matching

In the spectral domain, WLP matches the signal's power spectrum $P(f)$ on the **warped frequency scale** $f'$:

$$P(f') \sim \frac{G^2}{\left|1 + \sum_{k=1}^{M} a_k e^{-j 2\pi f'/N}\right|^2}$$

where $f'$ are warped frequency bins. This concentrates spectral resolution at low frequencies (where hearing is most sensitive) and relaxes it at high frequencies, matching auditory perception.

### Automatic Noise Masking

A characteristic of D*PCM (residual-driven) LPC coding is that the quantization error spectrum inherits the spectral shape of the all-pole model. In WLP this effect is **more pronounced**: the noise spectrum automatically follows the masked threshold related to the original signal, similar to what a psychoacoustic model would prescribe. [[sources/harma-2000-frequency-warped-signal-processing|Härmä et al. 2000]] show that a simple WLP-D*PCM codec without an auditory model produces noise spectra comparable to MPEG-1 Layer 3.

## Quantitative Results

Listening tests (12 test signals, 2 subjects, method of adjustment) compared WLP vs. conventional LPC in a generalized LP audio codec:

| Sampling rate | WLP gain (residual SNR) | Bit savings | Notes |
|:---:|:---:|:---:|:---|
| 48 kHz | ~6 dB | 1 bit/sample (48 kbit/s) | Clear advantage across all orders |
| 32 kHz | ~6 dB | 1 bit/sample (32 kbit/s) | Clear advantage across all orders |
| 16 kHz | Decreasing | < 1 bit | Gain vanishes for order ≥ 50 |
| 8 kHz | Small | ~0.5 bit (at order 10) | Gain vanishes for order ≥ 35 |

The SNR threshold corresponds to bit rate via $\mathrm{SNR}/\mathrm{dB} = 6b + \gamma$, where $b$ is the number of bits per sample. Thus a 6 dB SNR reduction translates to 1 bit/sample savings.

## Applications

- **Wideband audio coding**: WLP-D*PCM achieves 1 bit/sample savings at 32–48 kHz with automatic noise masking.
- **Backward-adaptive warped lattice**: Enables one-sample coding delay (vs. conventional coders that require block-based FFT psychoacoustic models).
- **Speech synthesis**: Reduced filter order due to WLP helps parametric control of text-to-speech synthesis.
- **Narrow-band speech coding**: Earlier work by Strube and Koishida et al. showed similar gains.

## Related Concepts

- [[concepts/frequency-warping|Frequency Warping]] — the underlying methodology
- [[concepts/all-pass-filter|All-Pass Filter]] — the warping building block
- [[concepts/warped-fir-filter|Warped FIR Filter]] — related warped filter structure
- [[concepts/warped-iir-filter|Warped IIR Filter]] — the WLP synthesis filter is a WIIR
- [[concepts/erb-scale|ERB Scale]] / [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]] — psychoacoustic scales approximated by warping

## Related Sources

- [[sources/harma-2000-frequency-warped-signal-processing|Härmä et al. 2000: Frequency-Warped Signal Processing for Audio Applications]] — presents the WLP theory, autocorrelation network, listening tests, and comparison with MPEG-1 Layer 3
