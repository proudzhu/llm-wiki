---
type: concept
created: 2026-05-23
updated: 2026-05-23
tags:
  - speech-enhancement
  - deep-learning
  - time-domain
  - waveform-processing
---

# Time-Domain Speech Enhancement

**Time-Domain Speech Enhancement** refers to neural network approaches that operate directly on raw waveform samples rather than on spectral representations (e.g., STFT magnitude). These methods avoid the phase reconstruction problem inherent in frequency-domain approaches by producing valid time-domain signals directly.

## Motivation

Frequency-domain methods typically estimate a magnitude mask or spectral mapping, then reconstruct the waveform using the noisy phase. This introduces two issues:

1. **[[concepts/invalid-stft-problem|Invalid STFT problem]]**: The combination of enhanced magnitude and noisy phase may not correspond to any real signal
2. **Phase degradation**: The noisy phase becomes increasingly suboptimal at low SNRs

Time-domain methods sidestep both issues by generating the output waveform directly.

## Key Architectures

| Architecture | Key features | Loss domain | Reference |
|:-------------|:-------------|:------------|:----------|
| SEGAN | U-Net + GAN discriminator | Time + adversarial | Pascual et al. 2017 |
| **AECNN** | U-Net encoder-decoder, compact | **Frequency (STFT magnitude)** | [[sources/pandey-2019-cnn-speech-enhancement-time-domain\|Pandey & Wang 2019]] |
| Conv-TasNet | Temporal convolutional network | Time (SI-SNR) | Luo & Mesgarani 2019 |
| DEMUCS | U-Net + LSTM bottleneck | Time + frequency | Défossez et al. 2020 |
| FullSubNet+ | Full-band + sub-band fusion | Frequency | Chen et al. 2022 |
| [[concepts/mamba-mingru\|Mamba-MinGRU]] | Mamba blocks + [[concepts/mingru\|MinGRU]] temporal mixing | Time (thresholded SDR) | Østergaard et al. 2026 |

## Loss Functions

The choice of training loss critically affects performance even for time-domain architectures:

| Loss type | Domain | Characteristics |
|:----------|:-------|:----------------|
| Waveform MAE/MSE | Time | Simple but poor perceptual quality |
| SI-SNR / SI-SDR | Time | Scale-invariant, good for separation tasks |
| STFT magnitude MAE | Frequency | Best for perceptual quality (PESQ/STOI) |
| Multi-resolution STFT | Frequency | Multiple STFT configurations for robustness |
| Complex STFT (RI) | Frequency | Best for SI-SDR, explicit phase learning |

The [[concepts/frequency-domain-loss|frequency domain loss for time-domain networks]] paradigm, proposed by Pandey & Wang (2019), demonstrated that spectral losses provide significantly better training signals than waveform losses for perceptual quality metrics.

## Key Properties

- **Valid output guarantee**: Output is always a valid time-domain signal (no reconstruction artefacts)
- **Implicit phase learning**: Network learns phase structure without explicit phase supervision
- **Context dependency**: Performance scales with input frame length (more context → better enhancement)
- **Computational efficiency**: Can be more efficient than iterative phase reconstruction methods

## Related Concepts

- [[concepts/frequency-domain-loss|Frequency Domain Loss for Time-Domain Networks]]
- [[concepts/invalid-stft-problem|Invalid STFT Problem]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]

## Related Sources

- [[sources/pandey-2019-cnn-speech-enhancement-time-domain|Pandey & Wang 2019: CNN-Based Speech Enhancement in the Time Domain]]
- [[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng et al. 2023: Sixty Years of Frequency-Domain Monaural Speech Enhancement]] — companion survey to frequency-domain methods; notes that frequency-domain methods historically outperform time-domain methods (though partly because more research effort has been invested in frequency-domain methods)
