---
type: concept
created: 2026-04-18
updated: 2026-05-20
sources:
  - raw/papers/cai-2024-tf-sepnet/full-text.md
tags:
  - acoustic-signal-processing
  - spectrogram-analysis
  - feature-extraction
---

# Spectrogram Analysis

**Spectrogram Analysis** is the process of studying and extracting features from 2D time-frequency representations (spectrograms) of acoustic signals. Unlike raw time-domain waveforms, spectrograms capture how the frequency content of a signal evolves over time, matching the frequency-dependent nature of human hearing and physical acoustics.

## Key Formulations

A spectrogram is computed by taking the magnitude of the **Short-Time Fourier Transform (STFT)** of a signal $x(t)$.

### 1. Short-Time Fourier Transform (STFT)
The STFT divides a continuous signal into short, overlapping segments and applies the Discrete Fourier Transform (DFT) to each segment:

$$X(m, k) = \sum_{n=-\infty}^{\infty} x(n) w(n - mH) e^{-j \frac{2\pi}{N} k n}$$

Where:
- $w(n)$ is a window function (e.g., Hann or Hamming window) of length $L$ that smooths the segment to reduce spectral leakage.
- $H$ is the hop size (number of samples shifted between consecutive windows).
- $N$ is the FFT size (number of frequency bins).
- $m$ is the time frame index, and $k$ is the frequency bin index.

The **spectrogram** is the squared magnitude of the STFT:
$$S(m, k) = |X(m, k)|^2$$

### 2. Log-Mel Spectrogram
For classification and learning tasks (e.g., Acoustic Scene Classification), the raw spectrogram is typically mapped to the Mel scale, which models the non-linear pitch perception of the human ear:

1. **Mel Filterbank**: A set of triangular bandpass filters spacing frequencies logarithmically above 1 kHz:
   $$M(m, b) = \sum_{k=0}^{N/2} S(m, k) H_b(k)$$
   Where $H_b(k)$ is the transfer function of the $b$-th Mel filter, and $b \in [1, B]$ ($B$ is typically 128 or 256).
2. **Log-Amplitude Scaling**: The filterbank outputs are scaled logarithmically to match human loudness perception:
   $$\text{Log-Mel}(m, b) = \log\left(M(m, b) + \epsilon\right)$$

In TF-SepNet, audio signals are down-sampled to 32 kHz, and STFT is applied with a window size of 3072 and a hop size of 500. A Mel-scaled filter bank with 256 frequency bins and 4096 FFT is then applied to produce the Log-Mel spectrogram.

## Related Concepts

- [[concepts/acoustic-scene-classification|Acoustic Scene Classification]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/time-frequency-separate-convolutions|Time-Frequency Separate Convolutions]]

## Related Sources

- [[sources/cai-2024-tf-sepnet|Cai, Zhang & Li 2024: TF-SepNet]]
