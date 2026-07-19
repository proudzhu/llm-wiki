---
type: concept
created: 2026-05-23
updated: 2026-05-23
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

$$\mathcal{L}_{\text{MR}} = \sum_s \left( \mathcal{L}_{\text{SC}}^{(s)} + \mathcal{L}_{\text{mag}}^{(s)} \right)$$

Uses multiple STFT configurations (different window sizes) for robustness across temporal/spectral resolutions.

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

## Related Sources

- [[sources/pandey-2019-cnn-speech-enhancement-time-domain|Pandey & Wang 2019: CNN-Based Speech Enhancement in the Time Domain]]
- [[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng et al. 2023: Sixty Years of Frequency-Domain Monaural Speech Enhancement]] — surveys frequency-domain loss functions (Mag-MSE, RI-MSE, RI+Mag combined, log-spectral, power-law-compressed) and the magnitude-phase "compensation effect" in RI-MSE
