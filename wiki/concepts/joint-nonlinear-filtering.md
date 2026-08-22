---
type: concept
created: 2026-05-13
updated: 2026-08-22
sources:
  - raw/papers/tesch-2024-spatially-selective-nonlinear-filters/full-text.md
  - raw/papers/huang-2026-ndf-joint-neural-directional-filtering/full-text.md
tags:
  - neural-network
  - spatial-audio
  - deep-learning
  - speech-enhancement
  - speech-separation
  - multi-channel
---

# Joint Nonlinear Filtering

Joint nonlinear filtering (JNF) refers to neural network architectures that jointly process spatial and temporal-spectral information for signal estimation. The **FT-JNF** framework, introduced by Tesch, Mohrmann & Gerkmann (Interspeech 2022) [27] and analysed in depth by Tesch & Gerkmann (IEEE/ACM TASLP 2023) [22], operates in the frequency domain with LSTM-based temporal and spectral processing and is the architectural basis for the [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Filter (SSF)]] and for [[concepts/mcnet|McNet]] in multi-channel speech separation/enhancement. The same FT-JNF backbone also underpins [[concepts/neural-directional-filtering|Neural Directional Filtering (NDF)]] for virtual directional microphones, where it has been extended with dual coherent/diffuse masks by Huang et al. (2026).

## FT-JNF Architecture

The FT-JNF framework for NDF uses:
- **Input**: Concatenated real/imaginary STFT coefficients $[B,T,F,2Q]$
- **Frequency processing**: BiLSTM along frequency dimension
- **Temporal processing**: UniLSTM along time dimension
- **Mask estimation**: Complex-valued mask applied to reference channel

## FT-JNF in Speech Separation (Tesch & Gerkmann 2022, 2023, 2024)

In Tesch & Gerkmann's speech-enhancement/separation line, the FT-JNF is described as a two-LSTM stack (named with Tesch's terminology):

1. **F-LSTM** — a bidirectional LSTM that processes the *frequency* dimension independently for each time frame (time moved into the batch dimension so that frames share weights). Designed to extract spatial/spectral features and their relationships while excluding temporal correlations. The F-LSTM is the layer that controls the spatial selectivity of the resulting filter [22].
2. **T-LSTM** — a (unidirectional) LSTM that processes the *time* dimension independently for each frequency bin, modelling temporal correlations.
3. **Linear output layer** — produces a complex-valued mask in $[-1, 1]$ which is expanded following the complex ratio masking scheme of [33] (Williamson & Wang 2016) and applied to the reference-channel STFT to obtain the source estimate: $\hat{S}_p(k, i) = Y^0(k, i) \cdot \mathcal{M}_p(k, i)$.

The design is inspired by Li & Horaud [32], who stack two T-LSTMs; Tesch & Gerkmann's replacement of the first T-LSTM with an F-LSTM is what produces the strong spatial selectivity on which the [[concepts/spatially-selective-nonlinear-filter|SSF]] depends.

## Dual-Mask Extension (NDF+)

NDF+ extends FT-JNF with:
- Two parallel UniLSTM branches replacing single UniLSTM
- Two complex masks: $\mathcal{M}_{\mathrm{coh}}$ and $\mathcal{M}_{\mathrm{diff}}$
- Joint estimation of coherent and diffuse components

## Related Concepts

- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]
- [[concepts/mcnet|McNet (Multi-Cue Network)]]
- [[concepts/direct-separation|Direct Separation (DS)]]
- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]
- [[concepts/diffuse-sound-extraction|Diffuse Sound Extraction]]

## Related Sources

- [[sources/tesch-2024-spatially-selective-nonlinear-filters|Tesch & Gerkmann 2024: Multi-channel Speech Separation Using Spatially Selective Deep Non-linear Filters]]
- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
