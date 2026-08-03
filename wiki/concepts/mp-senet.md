---
type: concept
created: 2026-06-19
updated: 2026-08-03
sources:
  - raw/papers/chao-2024-mamba-speech-enhancement/full-text.md
tags:
  - speech-enhancement
  - neural-network-architecture
---

# MP-SENet

MP-SENet is a time-frequency domain speech enhancement model that serves as the backbone for G-MaP-SE. It uses a magnitude-phase estimation framework with TF blocks and attention mechanisms (Conformer) as the core sequence model. The model processes STFT spectrograms and estimates both magnitude and phase components.

## Architecture

MP-SENet's pipeline:

1. **STFT** on the noisy waveform
2. **Magnitude compression** ($log1p$) and stacking with the phase
3. **Feature encoder**: dilated DenseNet flanked by two convolutional layers
4. **TF blocks** (repeated $N$ times): Conformer-based time-frequency modeling
5. **Two decoders**: separate magnitude and phase decoders, each = dilated DenseNet + deconvolution + 2D-conv output
6. **Loss**: PESQ-based GAN discriminator + time + magnitude + complex + phase losses

## Role as a Backbone

MP-SENet serves as the architectural backbone for several derived systems:

- **[[concepts/semamba|SEMamba]]** (Chao et al. 2024) — replaces the Conformer-based TF block with a Time-Frequency [[concepts/mamba|Mamba]] block. SEMamba matches MP-SENet's PESQ at ~12% lower FLOPs and reaches SOTA PESQ 3.69 on VoiceBank-DEMAND when combined with [[concepts/perceptual-contrast-stretching|PCS]].
- **G-MaP-SE** (Zhu et al. 2026) — backbone for GMM-based prior matching guided speech enhancement.

## Key Formulations

- $Architecture: Encoder + TF blocks with multi-head attention + Decoder$
- $Loss: Multi-component including PESQ-based GAN loss, STFT consistency, magnitude, complex-spectrum, phase, and time-domain losses$

## Related Concepts

- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/prior-matching|Prior Matching]]
- [[concepts/semamba|SEMamba]] — Mamba-based SE system that uses MP-SENet as its advanced backbone
- [[concepts/mamba|Mamba]] — replaces the Conformer in SEMamba-advanced
- [[concepts/perceptual-contrast-stretching|Perceptual Contrast Stretching (PCS)]] — post-processing used with SEMamba

## Related Sources

- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]
- [[sources/chao-2024-mamba-speech-enhancement|Chao et al. 2024: An Investigation of Incorporating Mamba for Speech Enhancement]] — uses MP-SENet as the advanced backbone, replacing Conformer with Mamba