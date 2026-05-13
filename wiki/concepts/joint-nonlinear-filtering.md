---
type: concept
created: 2026-05-13
updated: 2026-05-13
tags:
  - neural-network
  - spatial-audio
  - deep-learning
---

# Joint Nonlinear Filtering

Joint nonlinear filtering (JNF) refers to neural network architectures that jointly process spatial and temporal-spectral information for signal estimation. The FT-JNF framework extends this by operating in the frequency domain with LSTM-based temporal and spectral processing.

## FT-JNF Architecture

The FT-JNF framework for NDF uses:
- **Input**: Concatenated real/imaginary STFT coefficients $[B,T,F,2Q]$
- **Frequency processing**: BiLSTM along frequency dimension
- **Temporal processing**: UniLSTM along time dimension
- **Mask estimation**: Complex-valued mask applied to reference channel

## Dual-Mask Extension (NDF+)

NDF+ extends FT-JNF with:
- Two parallel UniLSTM branches replacing single UniLSTM
- Two complex masks: $\mathcal{M}_{\mathrm{coh}}$ and $\mathcal{M}_{\mathrm{diff}}$
- Joint estimation of coherent and diffuse components

## Related Concepts

- [[../concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[../concepts/virtual-directional-microphone|Virtual Directional Microphone]]
- [[../concepts/diffuse-sound-extraction|Diffuse Sound Extraction]]

## Related Sources

- [[../sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
