---
type: concept
created: 2026-04-25
updated: 2026-04-25
sources:
tags:
  - signal-processing
  - audio-processing
  - phase-estimation
  - deep-learning
---

# Complex Spectrum Mapping

**Complex Spectrum Mapping (CSM)** is a signal processing strategy that simultaneously estimates both the real and imaginary components of a target signal's complex spectrum, rather than predicting only the magnitude (amplitude) spectrum. CSM is critical for applications like [[active-noise-control|Active Noise Control]] where phase accuracy directly determines cancellation effectiveness.

## Why CSM Is Needed

Traditional speech enhancement methods estimate only the magnitude spectrum and reuse the noisy phase for waveform reconstruction. This works acceptably for enhancement but fails for ANC because:

- **Phase is critical for ANC**: Anti-noise must maintain an exact inverse phase (180° difference) from the original noise. Any phase error causes constructive interference instead of cancellation, potentially amplifying noise.
- **Magnitude masking ignores phase**: A ratio mask applied to the magnitude spectrum cannot correct phase distortions introduced by the secondary path or nonlinearities.

## How CSM Works

1. **STFT Analysis**: Convert time-domain signal $x(n)$ to complex spectrum $X(m,k)$ via Short-Time Fourier Transform
2. **Channel Decomposition**: Split into real part $X_r(m,k)$ and imaginary part $X_i(m,k)$ as two independent input channels
3. **Network Processing**: A neural network (typically a [[convolutional-recurrent-network|CRN]]) processes both channels and outputs predicted real $Y_r(m,k)$ and imaginary $Y_i(m,k)$ components
4. **iSTFT Synthesis**: Reconstruct time-domain signal: $y(n) = \text{iSTFT}(Y_r + jY_i)$

By jointly estimating real and imaginary parts, CSM implicitly models both amplitude and phase information, ensuring phase consistency during waveform reconstruction.

## Typical Configuration (from Dai 2026)

| Parameter | Value |
|-----------|-------|
| FFT size | 320 points (20 ms at 16 kHz) |
| Hop length | 160 samples (10 ms) |
| Window | Hanning |
| Overlap | 50% |
| Input channels | 2 (real, imaginary) |
| Output channels | 2 (real, imaginary) |

## Historical Context

- **Tan & Wang (2019)**: Proposed CSM with CRN for monaural speech enhancement, demonstrating that jointly estimating real/imaginary components outperforms magnitude-only approaches
- **Hu et al. (2020)**: DCCRN (Deep Complex Convolution Recurrent Network) using CSM won 1st place in the Interspeech 2020 Deep Noise Suppression Challenge (real-time track)
- **Zhang & Wang (2021)**: Applied CSM to Deep ANC, proving feasibility of supervised learning for anti-noise generation

## CSM vs. Magnitude Masking

| Aspect | Magnitude Masking | Complex Spectrum Mapping |
|--------|------------------|--------------------------|
| Phase handling | Reuses noisy phase | Estimates clean phase |
| ANC suitability | Poor (phase errors amplify noise) | Excellent (precise phase control) |
| Computational cost | Lower | Higher (2× output channels) |
| Speech enhancement | Adequate | Superior |

## Related Concepts

- [[convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[active-noise-control|Active Noise Control]]
- [[speech-preserving-anc|Speech-Preserving ANC]]
- [[deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]]
- [[concepts/frequency-domain-loss|Frequency Domain Loss for Time-Domain Networks]]
- [[concepts/invalid-stft-problem|Invalid STFT Problem]]

## Related Concepts

- [[concepts/deep-marginal-feedback-cancellation|Deep Marginal Feedback Cancellation]]

## Related Sources

- [[sources/hao-2025-l3c-deepmfc|Hao et al. 2025: L3C-DeepMFC]] — Gain-shape complex spectrum mapping for hearing aid feedback cancellation
- [[sources/dai-2026-speech-preserving-deep-anc|Dai 2026: Speech-Preserving Deep ANC]]
- [[sources/pandey-2019-cnn-speech-enhancement-time-domain|Pandey & Wang 2019: CNN-Based Speech Enhancement in the Time Domain]]
