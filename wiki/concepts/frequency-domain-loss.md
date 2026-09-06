---
type: concept
created: 2026-05-23
updated: 2026-09-06
sources:
  - raw/papers/valin-2024-fargan/full-text.md
  - raw/papers/mustafa-2023-framewise-wavegan/full-text.md
  - raw/papers/li-2020-residual-noise-control/full-text.md
  - raw/papers/zhao-2026-spectrally-adaptive-loss/full-text.md
  - raw/papers/wang-2021-magnitude-phase-compensation/full-text.md
tags:
  - loss-function
  - deep-learning
  - speech-enhancement
  - spectral-analysis
---

# Frequency Domain Loss for Time-Domain Networks

**Frequency Domain Loss** refers to the training paradigm where a neural network operates in the time domain but is optimised using a loss function computed in the frequency domain. This approach exploits the structural properties of spectral representations while avoiding the [[concepts/invalid-stft-problem|invalid STFT problem]].

## Key Insight

The DFT is a linear transformation expressible as matrix multiplication:

$$\mathbf{x}_f = \mathbf{D}\mathbf{x}_t$$

Since matrix multiplication is differentiable, gradients from a frequency-domain loss propagate back through the time-domain network without issues. This enables training on spectral features (which have clearer structure for speech) while producing valid time-domain signals.

## Loss Function Variants

### STFT Magnitude MAE (L1) — Best for PESQ/STOI

$$\mathcal{L}_{\text{SM1}} = \frac{1}{N}\sum_n \left| \text{mag}(\hat{\mathbf{x}}_f[n]) - \text{mag}(\mathbf{x}_f[n]) \right|$$

### STFT Magnitude MSE (L2)

$$\mathcal{L}_{\text{SM2}} = \frac{1}{N}\sum_n \left( \sqrt{\hat{x}_{fr}^2[n] + \hat{x}_{fi}^2[n]} - \sqrt{x_{fr}^2[n] + x_{fi}^2[n]} \right)^2$$

### Real-Imaginary Loss — Best for SI-SDR

$$\mathcal{L}_{\text{RI}} = \frac{1}{N}\sum_n \left[ (\hat{x}_{fr}[n] - x_{fr}[n])^2 + (\hat{x}_{fi}[n] - x_{fi}[n])^2 \right]$$

### RI + Magnitude Combined — the Compensation Trade-off (Wang 2021)

[[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021]] give the fundamental explanation for the mag-vs-RI split above: the RI loss alone is minimised by a magnitude that **compensates** for the inaccurate estimated phase (the [[concepts/magnitude-phase-compensation-effect|magnitude-phase compensation effect]]), so SI-SDR is favoured while PESQ/eSTOI/WER suffer. Adding a magnitude term ($\mathcal{L}_{\text{RI+Mag}}$, $L_1$ form) rebalances the two: better PESQ/eSTOI/WER and slightly worse SI-SDR, on both WHAMR! enhancement and SMS-WSJ separation+ASR. The same holds for time-domain losses ($\mathcal{L}_{\text{Wav+Mag}}$), and even a magnitude-only loss through the waveform ($\mathcal{L}_{\text{Wav}\times 0+\text{Mag}}$) retains good PESQ/eSTOI while SI-SDR collapses — strong evidence that these perceptual metrics depend largely on magnitude alone.

### Multi-Resolution STFT Loss

$$
\mathcal{L}_{\text{MR}} = \sum_s \left( \mathcal{L}_{\text{SC}}^{(s)} + \mathcal{L}_{\text{mag}}^{(s)} \right)
$$

Uses multiple STFT configurations (different window sizes) for robustness across temporal/spectral resolutions.

### Spectrally Weighted Phase-Aware Losses (Zhao & Madhu 2026)

The phase-aware compressed loss mixes magnitude and phase-aware terms with a scalar $\lambda$ — but the [[concepts/magnitude-phase-compensation-effect|magnitude-phase compensation effect]] makes the resulting over-attenuation spectrally non-uniform (concentrated in mid-to-high frequencies), which a scalar cannot express. [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026]] replace $\lambda$ with a frequency-wise weight: a fixed sigmoid of normalised frequency ($\mathcal{L}_{\mathrm{Sig}}$) or a signal-dependent weight derived from the time-averaged clean log-magnitude spectrogram ($\mathcal{L}_{\mathrm{Adp}}$) — see [[concepts/spectrally-adaptive-loss|Spectrally Adaptive Loss]]. On DNS (HyST-Net backbone), both cut HF-band C-RMSE ~9.5% and M-RMSE ~15.2% with broadband metrics unchanged — broadband instrumental metrics are dominated by low frequencies and mask exactly the distortion this weighting fixes, which is why the evaluation uses band-conditional (2–4 kHz / 4–8 kHz) C-RMSE, M-RMSE, and LSD.

### Generalized Exponent Family with Residual Noise Control (Li et al. 2020)

The magnitude-domain generalized loss of [[sources/li-2020-residual-noise-control|Li et al. 2020]],

$$\mathcal{J}_x^{\gamma,\alpha} = \sum_{l,k}\left|(1-M_l^{\alpha}(k))\,S_l^{\alpha}(k)\right|^{\gamma} + \mu\sum_{l,k}\left||M_l(k)D_l(k)|^{\alpha\gamma} - |\beta_0 D_l(k)|^{\alpha\gamma}\right|,$$

generalizes mag-MSE ($\gamma=2$, $\alpha=1$, no control) with a power-law spectral exponent and a **residual-noise-control term** that targets a preset noise floor $\beta_0$ instead of zero suppression — the training-time member of the noise-shaping family. See [[concepts/generalized-loss-function|Generalized Loss Function]] for the full family and special cases.

A GAN-vocoder instance appears in [[concepts/fargan|FARGAN]] ([[sources/valin-2024-fargan|Valin et al. 2024]]): the pre-training loss sums **six** resolutions (window sizes 80–2560 samples at 75% overlap) of a magnitude loss with **power-law compression** $\gamma=0.5$ chosen to approximate perceived loudness,

$$
\mathcal{L}_{L}=\sum_{\ell}\sum_{k}\left||\hat{X}_{L}(\ell,k)|^{0.5}-|X_{L}(\ell,k)|^{0.5}\right|,
$$

and the same spectral loss is retained alongside the adversarial terms during fine-tuning. Notably, FARGAN's discriminators are also frequency-domain (log-magnitude STFT, UnivNet-style): the authors found time-domain multi-scale/multi-period discriminators *degrade* quality on block-wise generators, because they win by flagging temporally irregular but perceptually irrelevant detail — small temporal irregularities are easier to detect in a raw waveform than in a log-magnitude spectrogram.

This recipe traces directly to FARGAN's predecessor [[concepts/framewise-wavegan|Framewise WaveGAN]] ([[sources/mustafa-2023-framewise-wavegan|Mustafa et al. 2023]]), the earliest instance in the wiki: six power-of-two FFT sizes 64–2048 at 75% overlap with a $sqrt$ magnitude non-linearity (chosen over $log$ for better early convergence) for spectral pre-training, followed by adversarial training with six UnivNet-style spectrogram discriminators under a least-squares GAN objective. FWGAN's authors report that time-domain discriminators (MelGAN, StyleMelGAN, HiFi-GAN styles) *failed to achieve stable training* on the framewise generator at all — the stronger form of the finding FARGAN later refined.

## Why Frequency Loss Outperforms Time-Domain Loss

1. **Structural clarity**: STFT magnitude has clearer temporal-spectral structure than raw waveform oscillations
2. **Non-negativity**: Magnitude spectrum is non-negative, easier for networks to learn
3. **Perceptual alignment**: Spectral magnitude correlates better with human auditory perception
4. **Phonetic discrimination**: Frequency-domain features better separate speech from non-speech noises

## Practical Considerations

- **Window function**: The STFT window (e.g., Hamming) multiplied at the analysis stage must match the training configuration
- **Frame size**: Larger analysis frames give better frequency resolution but reduce temporal detail
- **Combination losses**: Many modern systems combine time-domain and frequency-domain losses (e.g., DEMUCS uses both)

## Related Concepts

- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]]
- [[concepts/invalid-stft-problem|Invalid STFT Problem]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[concepts/fargan|FARGAN]] — six-resolution γ=0.5 spectral pre-training loss plus STFT discriminators
- [[concepts/framewise-wavegan|Framewise WaveGAN]] — the earlier instance: six-resolution sqrt-compressed spectral pre-training plus spectrogram discriminators
- [[concepts/generalized-loss-function|Generalized Loss Function]] — exponent-parameterized magnitude-loss family with residual noise control
- [[concepts/spectrally-adaptive-loss|Spectrally Adaptive Loss]] — frequency-wise / signal-dependent weighting of the phase-aware term
- [[concepts/magnitude-phase-compensation-effect|Magnitude-Phase Compensation Effect]] — the failure mode spectrally weighted phase-aware losses target

## Related Sources

- [[sources/pandey-2019-cnn-speech-enhancement-time-domain|Pandey & Wang 2019: CNN-Based Speech Enhancement in the Time Domain]]
- [[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng et al. 2023: Sixty Years of Frequency-Domain Monaural Speech Enhancement]] — surveys frequency-domain loss functions (Mag-MSE, RI-MSE, RI+Mag combined, log-spectral, power-law-compressed) and the magnitude-phase "compensation effect" in RI-MSE
- [[sources/valin-2024-fargan|Valin, Mustafa & Büthe 2024: FARGAN]] — GAN-vocoder instance: six-resolution power-law-compressed magnitude loss and frequency-domain discriminators
- [[sources/mustafa-2023-framewise-wavegan|Mustafa et al. 2023: Framewise WaveGAN]] — earliest GAN-vocoder instance: sqrt-compressed multi-resolution loss; spectrogram discriminators adopted after time-domain discriminators failed to train stably
- [[sources/li-2020-residual-noise-control|Li, Peng, Zheng & Li 2020: Supervised Speech Enhancement with Residual Noise Control]] — generalizes mag-MSE with exponents γ, α and a residual-noise-control term targeting a preset noise floor
- [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026: Spectrally Adaptive Loss for Streaming Speech Enhancement]] — spectrally weighted phase-aware STFT losses; HF-band C-RMSE/M-RMSE gains invisible to broadband metrics
- [[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021: On the Compensation Between Magnitude and Phase in Speech Separation]] — the fundamental explanation of why magnitude terms improve perceptual metrics in RI/Wav losses
