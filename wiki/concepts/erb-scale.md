---
type: concept
created: 2026-06-07
updated: 2026-06-07
tags:
  - psychoacoustics
  - speech-enhancement
  - signal-processing
---

# ERB Scale

The Equivalent Rectangular Bandwidth (ERB) scale is a psychoacoustic frequency scale that models the frequency resolution of the human auditory system. It is based on the bandwidth of the human auditory filters, which increase with center frequency. The ERB scale is used in speech enhancement and audio processing to reduce dimensionality while preserving perceptual information.

## Definition

The ERB of the human auditory filter at a given center frequency $f$ (in kHz) is approximated by:

$$
\text{ERB}(f) = 24.7 \cdot (4.37 \cdot f + 1)
$$

The ERB scale maps physical frequency to a perceptually uniform scale:

$$
\text{ERBS}(f) = 21.4 \cdot \log_{10}(0.00437 \cdot f + 1)
$$

## Usage in DeepFilterNet

In [[sources/schroter-2022-deepfilternet|DeepFilterNet]], the ERB scale is used to compress the frequency axis from full FFT resolution to just 32 bands:

1. A log-power spectrogram is computed from the STFT
2. An ERB filter bank reduces the input and output dimensions to $N_{\text{ERB}} = 32$ bands
3. The encoder-decoder network predicts gains on this compact representation
4. An inverse ERB filter bank transforms gains back to full frequency resolution

This perceptual compression allows the network to operate efficiently — the minimum ERB bandwidth ranges from ~100 Hz (low frequencies) to ~250 Hz (high frequencies, depending on FFT size).

## Relationship to Other Scales

| Scale | Formula | Bands | Application |
|-------|---------|-------|-------------|
| ERB | $21.4 \cdot \log_{10}(0.00437f + 1)$ | 32 (typical) | Speech enhancement |
| Mel | $2595 \cdot \log_{10}(1 + f/700)$ | 40 (typical) | ASR, speaker recognition |
| Bark | $13 \arctan(0.00076f) + 3.5 \arctan((f/7500)^2)$ | 24 | Psychoacoustics |

The ERB scale provides finer frequency resolution at low frequencies compared to the Mel scale, which is advantageous for speech enhancement where low-frequency harmonics carry important periodicity information.

## Related Concepts

- [[concepts/deep-filtering|Deep Filtering]]

## Related Sources

- [[sources/schroter-2022-deepfilternet|Schröter et al. 2022: DeepFilterNet]]
