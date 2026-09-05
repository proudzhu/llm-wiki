---
type: concept
created: 2026-05-13
updated: 2026-09-05
sources:
  - raw/papers/tesch-2023-insights-deep-nonlinear-filters/full-text.md
  - raw/papers/tesch-2024-spatially-selective-nonlinear-filters/full-text.md
  - raw/papers/huang-2026-ndf-joint-neural-directional-filtering/full-text.md
  - raw/papers/wechsler-2024-neural-directional-filtering/full-text.md
  - raw/papers/huang-2025-steerable-neural-directional-filtering/full-text.md
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

## Application to Directional Filtering (Wechsler et al. 2024)

The founding NDF study adopted the single-mask FT-JNF (BiLSTM-frequency → UniLSTM-time → linear+tanh complex mask, 873K parameters) to estimate a VDM from a 4-microphone array, trained with the SA-ε-tSDR loss on simulated multi-speaker scenes — establishing that the pattern itself can be learned implicitly from data, with training-set speaker density determining pattern fidelity.

## Dual-Mask Extension (NDF+)

NDF+ extends FT-JNF with:
- Two parallel UniLSTM branches replacing single UniLSTM
- Two complex masks: $\mathcal{M}_{\mathrm{coh}}$ and $\mathcal{M}_{\mathrm{diff}}$
- Joint estimation of coherent and diffuse components

## Steering-Conditioned Extension (SNDF)

[[concepts/steerable-neural-directional-filtering|SNDF]] (Huang et al. 2025) reuses the single-mask FT-JNF unchanged for mask estimation but adds a steering branch: the desired steering direction is one-hot encoded, mapped through a linear layer, and used to initialize the forward/backward states of the F-BiLSTM per time frame — the same conditioning mechanism Tesch & Gerkmann use for angular-region conditioning in the SSF. This turns the fixed-look-direction NDF into a model steerable to any direction at inference.

## Related Concepts

- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]
- [[concepts/mcnet|McNet (Multi-Cue Network)]]
- [[concepts/direct-separation|Direct Separation (DS)]]
- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/steerable-neural-directional-filtering|Steerable Neural Directional Filtering]]
- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]
- [[concepts/diffuse-sound-extraction|Diffuse Sound Extraction]]

## Related Sources

- [[sources/tesch-2023-insights-deep-nonlinear-filters|Tesch & Gerkmann 2023: Insights Into Deep Non-linear Filters for Improved Multi-channel Speech Enhancement]] — introduces the FT-JNF architecture and the T-JNF/F-JNF/FT-JNF/NSF/PF variant family; the foundational analysis of spatial-spectral-temporal interplay
- [[sources/tesch-2024-spatially-selective-nonlinear-filters|Tesch & Gerkmann 2024: Multi-channel Speech Separation Using Spatially Selective Deep Non-linear Filters]]
- [[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024: Neural Directional Filtering]] — first application of the single-mask FT-JNF to directivity-pattern learning
- [[sources/huang-2025-steerable-neural-directional-filtering|Huang et al. 2025: Steerable Neural Directional Filtering]] — steering-direction conditioning of the F-BiLSTM initial states
- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
