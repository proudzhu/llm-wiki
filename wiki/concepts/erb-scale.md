---
type: concept
created: 2026-06-07
updated: 2026-07-16
sources:
  - raw/papers/benslimane-2026-tango-quantized-distributed/full-text.md
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

## Usage in TANGO-Family Frameworks

Both [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|RT-Tango]] and [[sources/benslimane-2026-tango-quantized-distributed|Quantized MN-TANGO]] use an ERB-scaled filterbank as the front-end for the mask-estimation DNNs. After a point-wise channel-mixing layer, the 257-bin linear-frequency STFT is projected onto a compact ERB scale, reducing the recurrent input dimension; the predicted ERB-domain mask is mapped back to the linear STFT bins via an inverse ERB transform before the [[concepts/multi-channel-wiener-filter|SDW-MWF]] spatial filtering stage. In MN-TANGO, the configuration is 64 low-frequency linear bins + 64 ERB bands → 128-dimensional recurrent input (adjusted for divisibility by the group count $G$).

## Relationship to Other Scales

| Scale | Formula | Bands | Application |
|-------|---------|-------|-------------|
| ERB | $21.4 \cdot \log_{10}(0.00437f + 1)$ | 32 (typical) | Speech enhancement |
| Mel | $2595 \cdot \log_{10}(1 + f/700)$ | 40 (typical) | ASR, speaker recognition |
| Bark | $13 \arctan(0.00076f) + 3.5 \arctan((f/7500)^2)$ | 24 | Psychoacoustics |

The ERB scale provides finer frequency resolution at low frequencies compared to the Mel scale, which is advantageous for speech enhancement where low-frequency harmonics carry important periodicity information.

## Related Concepts

- [[concepts/deep-filtering|Deep Filtering]]
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]]
- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/tango-framework|Tango Framework]]
- [[concepts/mn-tango|MN-TANGO]]
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]] — alternative perceptual scale used by later PercepNet-style AEC works (Bark-AEC, EchoFree)
- [[concepts/trainable-frequency-compression|Trainable Frequency Compression]] — Chen et al. 2023 show fixed ERB filters underperform trainable Mel filters on WB-PESQ across all compression ratios

## Related Sources

- [[sources/valin-2021-percepnet-joint-echo-control|Valin et al. 2021: PercepNet Joint Echo Control]] — original PercepNet uses 32 ERB bands (NOT Bark)
- [[sources/schroter-2022-deepfilternet|Schröter et al. 2022: DeepFilterNet]]
- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
- [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026: Quantized TANGO / MN-TANGO]]
- [[sources/li-2025-echofree-neural-aec|Li et al. 2025: EchoFree]] — later PercepNet-style work that switched to the Bark scale (100 bands)
- [[sources/chen-2023-ultra-dual-path-compression|Chen et al. 2023: Ultra Dual-Path Compression]] — benchmarks FixedERB vs. FixedMel vs. TrainMel frequency compression; ERB wins SI-SNR at large ratios because SI-SNR weights all frequencies equally (Mel emphasises lows)
