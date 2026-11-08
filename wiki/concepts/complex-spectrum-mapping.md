---
type: concept
created: 2026-04-25
updated: 2026-11-08
sources:
  - raw/papers/wang-2025-multi-modal-deep-filtering-bc/full-text.md
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

## Complex-Domain Deep Filtering as CSM (Wang et al. 2025)

[[sources/wang-2025-multi-modal-deep-filtering-bc|Wang, Kuang, Li, Yang, Bai & Liu 2025]] provide an argument for CSM on **recognition** grounds rather than the perceptual grounds usually cited. Their MDFNet operates directly in the complex domain (high-band ERB gains plus low-band [[concepts/multi-modal-deep-filtering|multi-modal deep filtering]]), and although it trails the time-domain MTINet on PESQ/STOI/ESTOI (3.21/0.79/0.69 vs. 3.29/0.91/0.84), it beats it on ASR character error rate (24.8% vs. 27.3%). The authors' explanation: the time-domain model encodes and decodes the multi-modal waveform through convolutions, whereas the complex-domain model needs no feature learning or reconstruction and therefore "better preserves spectral details" — the spectral detail that an ASR front-end consumes even when perceptual metrics do not reward it.

This is a useful counterweight to the general rule that time-domain and complex-domain systems track each other on quality metrics: the two targets can disagree, and CSM's advantage can be invisible in PESQ. Note also that the phase argument in "Why CSM Is Needed" above reappears here in a multi-modal form — at low SNR the noisy-AC phase is corrupted and the BC phase above the BC passband simply does not exist, so learned complex coefficients are the mechanism that sidesteps explicit phase estimation.

## Related Concepts
- [[convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/multi-modal-deep-filtering|Multi-Modal Deep Filtering]]
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
- [[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng et al. 2023: Sixty Years of Frequency-Domain Monaural Speech Enhancement]] — surveys complex-spectrum DNNs (GCRN, DPCRN, Uformer, DCCRN) and the magnitude-phase "compensation effect" in RI-MSE loss
- [[sources/liu-2021-igcrn|Liu & Zhang 2021: IGCRN]] — uses a [[concepts/mask-mapping-amplitude-prediction|mask + mapping + phase]] target rather than pure CSM, decomposing the prediction into amplitude mask, amplitude mapping, and normalized phase. The ablation (Table 3) shows this explicit decomposition outperforms direct complex spectral mapping (GCRN(CS)) at low SNR, because amplitude and phase are coupled in the complex spectrum and predicting them separately is more effective. IGCRN's successor ICCRN reverts to a pure CSM target with a weighted L1 RI+amplitude loss.
- [[sources/liu-2023-iccrn|Liu & Zhang 2023: ICCRN]] — uses CSM with a weighted L1 RI+amplitude loss ($\alpha=2$ on amplitude); the estimated spectrum is inverted to time domain and re-transformed before the loss to enforce [[concepts/stft-consistency|STFT consistency]]. ICCRN reports that DCCRN(CSM) and DPCRN(CSM) outperform their magnitude-mask counterparts, consistent with the literature.
- [[sources/wang-2025-multi-modal-deep-filtering-bc|Wang, Kuang, Li, Yang, Bai & Liu 2025: Multi-Modal Deep-Filtering-Based Speech Enhancement via BC Speech]] — complex-domain model wins on ASR CER (24.8% vs. 27.3%) while losing on PESQ/STOI to the time-domain baseline; spectral-detail preservation as a recognition-specific argument for CSM
