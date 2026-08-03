---
type: concept
created: 2026-06-07
updated: 2026-08-03
sources:
  - raw/papers/benslimane-2026-tango-quantized-distributed/full-text.md
  - raw/papers/harma-2000-frequency-warped-signal-processing/full-text.md
  - raw/papers/jiang-2026-lightweight-speech-enhancement-ssm-dsc/full-text.md
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

## Usage in AdaptCRN

[[sources/wang-2025-adaptive-convolution-cnn-speech-enhancement|Wang et al. 2025]]'s [[concepts/adaptcrn|AdaptCRN]] reuses GTCRN's ERB band-merging scheme for its **spectral compression** module: the first 65 low-frequency bins (below 2 kHz) are kept unaltered, while the 192 high-frequency bins (above 2 kHz) are downsampled to 64 ERB bands via a triangular ERB filter. The 129-D compressed feature is then expanded to 9 channels × 129 D per frame via SFE (subband feature extraction, kernel 3) before entering the encoder. Spectral decompression applies the **transpose** of the (non-learnable) downsampling matrix. Combined with dynamic-range compression ($\log_{10}$ on magnitude, $|S|^{0.7}$ on real/imag — see [[concepts/power-law-compression|Power-Law Compression]]), this module reduces both frequency dimension and dynamic range before the network. This design pattern (ERB band merging + SFE + transposed-matrix decompression) originates from [[concepts/gtcrn|GTCRN]] and is reused by [[concepts/cofi-lite|CoFi-Lite]] and AdaptCRN in the same NJU/Horizon Robotics lab lineage.

## Usage in AISC (Jiang et al. 2026)

[[sources/jiang-2026-lightweight-speech-enhancement-ssm-dsc|Jiang et al. 2026]]'s [[concepts/auditory-inspired-spectral-compressor|Auditory-Inspired Spectral Compressor (AISC)]] applies a **perceptually-motivated low/high split**: low frequencies below 1.5 kHz are preserved at full resolution (where cochlear sensitivity is highest for harmonics/formants), while high frequencies above 1.5 kHz are projected onto the ERB scale via a fixed triangular filter bank $W_{\mathrm{ERB}} \in \mathbb{R}^{F_{\mathrm{ERB}} \times F_H}$. The decoder inverts the projection via $W_{\mathrm{ERB}}^T$. This parameter-free module delivers a **2.6× MACs reduction** (1.32 → 0.50 G) with only 0.04 PESQ loss vs. full-resolution processing. Distinctive vs. GTCRN/AdaptCRN (which use a hard 2 kHz split with full low-res preservation): AISC explicitly frames the split as a cochlea-motivated design choice (low frequencies need fine resolution; high frequencies are perceived via critical-band energy integration), and applies ERB compression only to the high-frequency branch.

## Relationship to Other Scales

| Scale | Formula | Bands | Application |
|-------|---------|-------|-------------|
| ERB | $21.4 \cdot \log_{10}(0.00437f + 1)$ | 32 (typical) | Speech enhancement |
| Mel | $2595 \cdot \log_{10}(1 + f/700)$ | 40 (typical) | ASR, speaker recognition |
| Bark | $13 \arctan(0.00076f) + 3.5 \arctan((f/7500)^2)$ | 24 | Psychoacoustics |

The ERB scale provides finer frequency resolution at low frequencies compared to the Mel scale, which is advantageous for speech enhancement where low-frequency harmonics carry important periodicity information.

### Foundational Context

[[sources/harma-2000-frequency-warped-signal-processing|Härmä et al. 2000]] provide a foundational comparison of auditory scales, noting that the ERB scale (Moore, Peters & Glasberg 1990) matches Greenwood's cochlear frequency-position mapping better than the Bark scale — ERBs are very close to Greenwood's bandwidth measure, while Bark bands are 2–4× wider than ERBs below 200 Hz and 1.5–2× wider above 5 kHz. This motivates ERB-like [[concepts/frequency-warping|frequency warping]] for auditory-matched DSP, though the first-order all-pass Bark bilinear mapping can only approximate the ERB scale globally.

## Related Concepts

- [[concepts/deep-filtering|Deep Filtering]]
- [[concepts/frequency-warping|Frequency Warping]] — ERB-like warping approximates the ERB scale via all-pass mapping
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]]
- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/tango-framework|Tango Framework]]
- [[concepts/mn-tango|MN-TANGO]]
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]] — alternative perceptual scale used by later PercepNet-style AEC works (Bark-AEC, EchoFree)
- [[concepts/trainable-frequency-compression|Trainable Frequency Compression]] — Chen et al. 2023 show fixed ERB filters underperform trainable Mel filters on WB-PESQ across all compression ratios
- [[concepts/gtcrn|GTCRN]] — origin of the ERB + SFE + transposed-decompression pattern reused by AdaptCRN
- [[concepts/adaptcrn|AdaptCRN]] — reuses GTCRN's ERB spectral compression scheme
- [[concepts/auditory-inspired-spectral-compressor|Auditory-Inspired Spectral Compressor (AISC)]] — Jiang et al. 2026's perceptually-motivated low/high split + ERB compression on high band

## Related Sources

- [[sources/harma-2000-frequency-warped-signal-processing|Härmä et al. 2000: Frequency-Warped Signal Processing for Audio Applications]] — foundational comparison of ERB, Bark, and Greenwood scales in the context of frequency warping
- [[sources/valin-2021-percepnet-joint-echo-control|Valin et al. 2021: PercepNet Joint Echo Control]] — original PercepNet uses 32 ERB bands (NOT Bark)
- [[sources/schroter-2022-deepfilternet|Schröter et al. 2022: DeepFilterNet]]
- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
- [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026: Quantized TANGO / MN-TANGO]]
- [[sources/li-2025-echofree-neural-aec|Li et al. 2025: EchoFree]] — later PercepNet-style work that switched to the Bark scale (100 bands)
- [[sources/chen-2023-ultra-dual-path-compression|Chen et al. 2023: Ultra Dual-Path Compression]] — benchmarks FixedERB vs. FixedMel vs. TrainMel frequency compression; ERB wins SI-SNR at large ratios because SI-SNR weights all frequencies equally (Mel emphasises lows)
- [[sources/wang-2025-adaptive-convolution-cnn-speech-enhancement|Wang et al. 2025: Adaptive Convolution for CNN-based Speech Enhancement Models]] — AdaptCRN's spectral compression uses ERB band merging (65 low + 64 ERB)
- [[sources/jiang-2026-lightweight-speech-enhancement-ssm-dsc|Jiang, Gao, Wang, Zou & Liu 2026: Lightweight SE with SSM and DSConv]] — AISC uses 1.5 kHz perceptual split + ERB compression on the high-frequency branch
