---
type: concept
created: 2026-07-17
updated: 2026-08-30
sources:
  - raw/papers/valin-2018-lpcnet/full-text.md
  - raw/papers/li-2025-echofree-neural-aec/full-text.md
  - raw/papers/seidel-2024-bark-scale-nn-residual-suppression/full-text.md
  - raw/papers/zheng-2023-survey-frequency-domain-speech-enhancement/full-text.md
  - raw/papers/harma-2000-frequency-warped-signal-processing/full-text.md
  - raw/papers/valin-2022-real-time-plc/full-text.md
  - raw/papers/valin-2024-fargan/full-text.md
tags:
  - psychoacoustics
  - speech-enhancement
  - signal-processing
  - acoustic-echo-cancellation
  - low-complexity
---

# Bark-Scale Spectral Features

**Bark-scale spectral features** are perceptually motivated low-dimensional representations of audio obtained by projecting the linear-frequency STFT magnitude onto the Bark psychoacoustic frequency scale. They compress the full spectrogram (typically 257 bins at 16 kHz) into a much smaller set of bands (typically ~24 critical bands, or expanded to 100 sub-bands in Bark-AEC / EchoFree), preserving perceptually relevant information while dramatically reducing the input dimensionality and downstream computational cost.

## Definition

The Bark scale models the critical bands of human hearing, where each Bark corresponds to a critical band about 100 Hz wide at low frequencies and progressively wider at high frequencies. The mapping from linear frequency $f$ (in Hz) to Bark $b$ is:

$$
b(f) = 13 \arctan(0.00076 f) + 3.5 \arctan\left((f/7500)^2\right)
$$

In practical speech-enhancement / AEC systems, the linear STFT magnitude $|Y| \in \mathbb{R}^{T \times F}$ is multiplied by a fixed mapping matrix $\mathbf{B} \in \mathbb{R}^{F \times N_{\text{Bark}}}$ to obtain a Bark-scale power spectrum, which is then log-compressed:

$$
\mathbf{X}_{\text{Bark}} = \log\left( |Y|^{\,2} \cdot \mathbf{B} \right)
$$

The inverse operation $\mathbf{B}^\top$ expands a predicted Bark gain back to the linear STFT resolution for waveform resynthesis.

## Role in Low-Complexity Neural AEC

Bark-scale features are a foundational design choice in lightweight AEC post-filters because they allow the neural network to operate on a compact representation rather than the full 257-bin spectrum. Three lightweight AEC lines of work build directly on this idea:

| System | Bark bands | Input dim | Reference |
|--------|-----------:|----------:|-----------|
| Ma et al. 2020 (ADF + RNN) | 100 | 100 + derivatives | [[sources/li-2025-echofree-neural-aec\|EchoFree, ref. 6]] |
| Seidel et al. ICASSP 2024 (Bark-AEC) | **86** (0–8 kHz, PEAQ-style uniform Bark) | 86 × 3 (mic, error, far-end log-power) | [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Seidel et al. 2024]] |
| **EchoFree** (Li et al. 2025) | 100 | **112** (100 Bark + 6 first-order + 6 second-order derivatives) | [[sources/li-2025-echofree-neural-aec\|Li et al. 2025]] |

> **Note on band counts**: Seidel et al. 2024 reports **86 Bark bands** over 0–8 kHz using a PEAQ-style filterbank design (Kabal 2003). EchoFree (Li 2025) and the earlier Ma 2020 use **100 bands**. The later EchoFree paper cites "Bark-AEC (Seidel et al. ICASSP 2024)" with 100 bands, but this appears to be a citation discrepancy — the original Seidel paper reports 86.

In [[sources/li-2025-echofree-neural-aec\|EchoFree]] the 112-dim Bark feature vector is fed to a [[concepts/u-net-post-filter\|U-Net post filter]] that predicts a 100-dim Bark gain mask $\hat{\mathbf{g}} \in [0, 1]^{100}$. The mask is expanded back to 257 bins via $\mathbf{B}^\top \hat{\mathbf{g}}$ and applied to $|Y|$ to recover the near-end magnitude spectrum.

## Use in Neural Vocoding

[[concepts/lpcnet|LPCNet]] (Valin & Skoglund 2018) conditions speech synthesis on just **18 Bark-scale cepstral coefficients** plus two pitch parameters (period and correlation) — one of the smallest Bark-cepstral instances in the wiki, using the band layout of Valin's hybrid DSP/deep-learning full-band speech enhancement work (MMSP 2018). The cepstrum serves a second purpose beyond conditioning: LPCNet derives its **linear prediction coefficients** from it (18-band cepstrum → linear-frequency PSD → auto-correlation via inverse FFT → Levinson-Durbin), so the all-pole synthesis filter needs no information beyond the 20 transmitted/synthesized features.

[[concepts/fargan|FARGAN]] ([[sources/valin-2024-fargan|Valin et al. 2024]]) inherits this exact 18-BFCC feature vector (with a voicing indicator replacing the pitch correlation), demonstrating that the representation outlives the architecture: it conditions a GAN-based subframe synthesizer that no longer performs any LPC analysis at all — the Bark cepstrum is purely a conditioning signal there.

## Comparison with Other Perceptual Scales

| Scale | Formula (Hz → scale) | Bands | Application |
|-------|----------------------|------:|-------------|
| [[concepts/erb-scale\|ERB]] | $21.4 \cdot \log_{10}(0.00437 f + 1)$ | 32 (DeepFilterNet) | Speech enhancement (DeepFilterNet, TANGO) |
| Mel | $2595 \cdot \log_{10}(1 + f/700)$ | 40 | ASR, speaker recognition |
| **Bark** | $13 \arctan(0.00076 f) + 3.5 \arctan((f/7500)^2)$ | 24 critical / 100 sub | AEC post filters (Bark-AEC, EchoFree, PercepNet) |

Bark and ERB are both perceptually motivated. Notably, the original [[concepts/percepnet|PercepNet]] (Valin et al. ICASSP 2020/2021) uses the **ERB scale** (32 bands), while later "PercepNet-style" AEC post filters (Bark-AEC, EchoFree) switched to the Bark scale. ERB also dominates the DeepFilterNet / TANGO family. The two scales produce qualitatively similar compression ratios (8:1–32:1) and similar parameter savings when used as a network front-end.

### Foundational Context

The Bark scale's relationship to auditory filter banks and cochlear mapping is surveyed in [[sources/harma-2000-frequency-warped-signal-processing|Härmä et al. 2000]], which compares the Bark, ERB, and Greenwood scales and presents the Bark bilinear mapping — an all-pass [[concepts/frequency-warping|frequency warping]] that approximates the Bark scale for DSP implementation. The paper notes that the ERB scale matches Greenwood's physiological mapping better than Bark, but the first-order all-pass Bark mapping remains the most practical approximation for real-time warped signal processing.

## Related Concepts

- [[concepts/erb-scale\|ERB Scale]]
- [[concepts/percepnet-style-neural-post-filter\|PercepNet-Style Neural Post Filter]]
- [[concepts/lpcnet\|LPCNet]] — uses 18 BFCCs as a smaller-scale Bark-cepstral instance for neural vocoding
- [[concepts/u-net-post-filter\|U-Net Post Filter]]
- [[concepts/acoustic-echo-cancellation\|Acoustic Echo Cancellation]]
- [[concepts/speech-enhancement\|Speech Enhancement]]
- [[concepts/deep-filtering\|Deep Filtering]]
- [[concepts/trainable-frequency-compression\|Trainable Frequency Compression]] — Chen et al. 2023 show that making the Mel-scale filterbank trainable (TrainMel) beats both fixed ERB and fixed Mel filters on WB-PESQ across all compression ratios

## Related Sources

- [[sources/valin-2018-lpcnet|Valin & Skoglund 2018: LPCNet]] — 18 Bark-scale cepstral coefficients as vocoder conditioning, also the source of the LPC analysis
- [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Seidel, Mowlaee & Fingscheidt 2024]] — original Bark-AEC paper; 86-band PEAQ-style Bark filterbank with NSNet2-style FC+GRU backbone
- [[sources/li-2025-echofree-neural-aec\|Li et al. 2025: EchoFree]]
- [[sources/indenbom-2023-deepvqe\|Indenbom et al. 2023: DeepVQE]] — comparison point in the AEC lightweight hierarchy
- [[sources/shetu-2024-hybrid-low-complexity-aenr|Shetu et al. 2024: Hybrid Low-Complexity AENR]] — ULCNet-AER baseline (uses linear-frequency sub-band stacking rather than Bark)
- [[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng et al. 2023: Sixty Years of Frequency-Domain Monaural Speech Enhancement]] — surveys Bark/ERB-band perceptual features (Valin 2018 BFCCs, Valin et al. 2020 ERB-band features) as the dominant strategy for reducing full-band input feature dimensionality
- [[sources/valin-2022-real-time-plc|Valin et al. 2022: Real-Time PLC]] — uses 18 BFCCs (LPCNet features) plus pitch period/correlation as conditioning for the autoregressive vocoder
- [[sources/valin-2024-fargan|Valin, Mustafa & Büthe 2024: FARGAN]] — same 18-BFCC features (voicing indicator in place of pitch correlation) conditioning a GAN vocoder with no LPC analysis
