---
type: concept
created: 2026-05-23
updated: 2026-08-31
sources:
  - raw/papers/valin-2024-fargan/full-text.md
  - raw/papers/mustafa-2023-framewise-wavegan/full-text.md
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

### Multi-Resolution STFT Loss

$$
\mathcal{L}_{\text{MR}} = \sum_s \left( \mathcal{L}_{\text{SC}}^{(s)} + \mathcal{L}_{\text{mag}}^{(s)} \right)
$$

Uses multiple STFT configurations (different window sizes) for robustness across temporal/spectral resolutions.

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

## Related Sources

- [[sources/pandey-2019-cnn-speech-enhancement-time-domain|Pandey & Wang 2019: CNN-Based Speech Enhancement in the Time Domain]]
- [[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng et al. 2023: Sixty Years of Frequency-Domain Monaural Speech Enhancement]] — surveys frequency-domain loss functions (Mag-MSE, RI-MSE, RI+Mag combined, log-spectral, power-law-compressed) and the magnitude-phase "compensation effect" in RI-MSE
- [[sources/valin-2024-fargan|Valin, Mustafa & Büthe 2024: FARGAN]] — GAN-vocoder instance: six-resolution power-law-compressed magnitude loss and frequency-domain discriminators
- [[sources/mustafa-2023-framewise-wavegan|Mustafa et al. 2023: Framewise WaveGAN]] — earliest GAN-vocoder instance: sqrt-compressed multi-resolution loss; spectrogram discriminators adopted after time-domain discriminators failed to train stably
