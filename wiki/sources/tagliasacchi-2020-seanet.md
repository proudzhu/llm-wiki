---
type: source
created: 2026-05-17
updated: 2026-05-17
sources:
  - raw/papers/tagliasacchi-2020-seanet/full-text.md
  - https://arxiv.org/abs/2009.02095
  - zotero://select/items/0_BW784N4C
tags:
  - speech-enhancement
  - multi-modal
  - accelerometer
  - bone-conduction
  - adversarial-training
  - wave-to-wave
  - interspeech-2020
---

# Tagliasacchi, Li, Misiunas & Roblek 2020: SEANet — A Multi-modal Speech Enhancement Network

**Authors**: [[../entities/marco-tagliasacchi|Marco Tagliasacchi]], [[../entities/yunpeng-li|Yunpeng Li]], [[../entities/karolis-misiunas|Karolis Misiunas]], [[../entities/dominik-roblek|Dominik Roblek]]
**Affiliation**: Google Research
**Venue**: INTERSPEECH 2020
**Type**: Conference paper
**DOI**: —
**Zotero**: [Link](zotero://select/items/0_BW784N4C)

---

## Summary

SEANet proposes using **accelerometer data** from bone-conductance sensors mounted in earbuds as a multi-modal conditioning signal for speech enhancement. The model is a fully convolutional **wave-to-wave UNet** generator that takes both microphone audio and accelerometer signals as input, trained with a combination of **MelGAN-style adversarial losses** and **feature reconstruction losses**. The accelerometer provides a noise-immune signal that captures the user's voice via skull vibrations, enabling SEANet to achieve 9.6 dB SI-SDRi improvement in overlapping-speaker scenarios — a setting where audio-only models fail entirely.

---

## Problem Formulation

Given a noisy microphone signal $x_m$ and an accelerometer signal $x_a$ (time-aligned, interpolated to match the microphone sampling rate), SEANet learns a generator $G(x_m, x_a)$ that produces enhanced speech $\hat{x}_m$ approximating the clean target $y_m$.

The accelerometer operates at a lower native sampling rate (4 kHz, 2-axis) than the microphone (16 kHz). One axis is selected and interpolated to 16 kHz before input. Signals are high-pass filtered at 20 Hz and amplitude-normalized.

---

## Methodology

### Generator: Multi-modal UNet

The generator is a **symmetric encoder-decoder** with skip connections, processing both audio and accelerometer waveforms directly (no STFT or mel spectrograms):

- **Encoder**: 4 blocks with downsampling strides (2, 2, 8, 8); channel count doubles at each downsampling step
- **Decoder**: 4 blocks mirroring the encoder; each contains a transposed 1D convolution followed by 3 residual units with dilations 1, 3, 9
- **Skip connections**: Between each encoder block and its mirrored decoder block (outermost skip connects only the speech channel)
- **Multi-modal input**: Audio + accelerometer channels are concatenated at the input; the outer skip connection only passes the speech channel to the output
- **Weight normalization** and **ELU activations** throughout the generator

### Discriminator: Multi-Resolution MelGAN

Three structurally identical discriminators at different resolutions (original, 2× downsampled, 4× downsampled), each consisting of grouped convolutions with group size 4. Outputs multiple logits proportional to input length, each judging a segment of the input. Uses **layer normalization** and **Leaky ReLU** ($\alpha = 0.3$).

### Loss Functions

**Adversarial loss** (hinge loss, averaged over resolutions and time):

$$
\mathcal{L}_D = \mathbb{E}_{y_m}\left[\frac{1}{K}\sum_{k,t}\frac{1}{T_k}\max(0, 1 - D_{k,t}(y_m))\right] + \mathbb{E}_{(x_m,x_a)}\left[\frac{1}{K}\sum_{k,t}\frac{1}{T_k}\max(0, 1 + D_{k,t}(G(x_m,x_a)))\right]
$$

$$
\mathcal{L}_G^{\text{adv}} = \mathbb{E}_{(x_m,x_a)}\left[\frac{1}{K}\sum_{k,t}\frac{1}{T_k}\max(0, 1 - D_{k,t}(G(x_m,x_a)))\right]
$$

**Feature reconstruction loss** (normalized L1 distance between discriminator internal layer outputs):

$$
\mathcal{L}_G^{\text{rec}} = \mathbb{E}_x\left[\frac{1}{K}\sum_{k,l}\frac{1}{L}\frac{\|D_k^{(l)}(y_m) - D_k^{(l)}(G(x_m,x_a))\|_1}{T_{k,l}}\right]
$$

**Overall generator loss**: $\mathcal{L}_G = \mathcal{L}_G^{\text{adv}} + \lambda \cdot \mathcal{L}_G^{\text{rec}}$ with $\lambda = 100$

### Training

- Adam optimizer, batch size 16, learning rate $10^{-4}$, $\beta_1 = 0.5$, $\beta_2 = 0.9$
- 200k iterations (2M on LibriSpeech), single GPU
- No early stopping or parameter tuning

---

## Experimental Setup

| Aspect | Detail |
|--------|--------|
| **Dataset** | In-house: 25 subjects, ~1.25 h total, 5-fold cross-validation (20 train / 5 test per fold) |
| **Synthetic extension** | Trained audio→accelerometer mapping model; applied to LibriSpeech train-clean-100 for larger-scale evaluation |
| **Input** | Microphone: 16 kHz; Accelerometer: 4 kHz (2-axis, 1 axis used), interpolated to 16 kHz |
| **Noise types** | (i) Mixed speech: other-speaker utterances at unit gain; (ii) Mixed noise: Freesound samples at unit gain |
| **Baselines** | iTDCN++ (universal sound separation), Wavesplit (end-to-end speaker clustering), SEANet audio-only |
| **Metric** | Scale-Invariant Signal-to-Distortion Ratio improvement (SI-SDRi) |

---

## Results

### In-House Dataset

| Scenario | SEANet (audio + accel) | SEANet (audio only) |
|----------|----------------------|-------------------|
| Mixed noise | **8.9 dB** SI-SDRi avg | 8.0 dB |
| Mixed speech | **9.6 dB** SI-SDRi avg | −0.9 dB (fails) |

Key finding: The audio-only variant fails entirely in the mixed-speech scenario (−0.9 dB), while SEANet with accelerometer conditioning achieves 9.6 dB. In the mixed-noise scenario, SEANet audio+accel provides modest improvement (8.9 vs 8.0 dB).

### LibriSpeech (Synthetic Accelerometer)

| Scenario | SEANet (audio + accel) |
|----------|----------------------|
| Mixed noise | **12.4 dB** SI-SDRi |
| Mixed speech | **12.4 dB** SI-SDRi |

Larger training data (LibriSpeech) improves results significantly, reaching 12.4 dB in both scenarios.

### Effect of Accelerometer Sampling Rate

- Speech separation degrades rapidly when accelerometer sampling rate drops below **400 Hz**
- Below 200 Hz, the model cannot separate speakers at all
- For background noise, degradation is minimal even at very low sampling rates (8.0 dB SI-SDRi with drastically reduced bandwidth)

### Comparison with Baselines

| Method | Mixed noise SI-SDRi | Mixed speech SI-SDRi |
|--------|-------------------|-------------------|
| SEANet (audio + accel) — in-house | 8.9 dB | 9.6 dB |
| SEANet (audio only) — in-house | 8.0 dB | −0.9 dB |
| iTDCN++ (audio only) | 7.5 dB | 4.2 dB |
| Wavesplit (audio only) | — | 8.8 dB |

---

## Key Contributions

1. **First demonstration** of using **accelerometer data** from earbud-mounted sensors for speech enhancement, leveraging noise-immune bone-conducted vibration signals.
2. **Multi-modal wave-to-wave UNet** architecture that operates directly on raw waveforms (no STFT or mel spectrograms), fusing audio and accelerometer modalities at the input level.
3. **Adversarial + feature loss training** adapted from MelGAN, enabling the generator to produce natural-sounding enhanced speech while the feature loss preserves content and suppresses noise.
4. **Systematic analysis** of the effect of accelerometer bandwidth on enhancement performance, showing that speech separation requires >400 Hz accelerometer sampling, while noise suppression is robust to much lower bandwidths.

---

## Related Concepts

- [[../concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]]
- [[../concepts/bone-conduction|Bone Conduction]]
- [[../concepts/bone-conduction-function|Bone Conduction Function (BCF)]]
- [[../concepts/inertial-measurement-unit|Inertial Measurement Unit]]
- [[../concepts/voice-activity-detection|Voice Activity Detection]]
- [[../concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[../concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]

## Related Synthesis

- [[../synthesis/multimodal-bc-speech-enhancement|Multimodal BC Speech Enhancement]]
