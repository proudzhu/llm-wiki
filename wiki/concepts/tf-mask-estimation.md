---
type: concept
created: 2026-08-16
updated: 2026-08-20
sources:
  - raw/papers/taseska-2018-informed-spatial-filters/full-text.md
  - raw/papers/ansari-2023-ai-bss-survey/full-text.md
tags:
  - blind-source-separation
  - speech-enhancement
  - sparsity
  - clustering
  - tf-mask
  - em-algorithm
  - deep-learning
---

# TF Mask Estimation

**TF mask estimation** is the process of determining, for each Short-Time Fourier Transform (STFT) time-frequency (TF) bin, which source is dominant — producing a (binary or soft) **TF mask** per source. It is the central building block of sparsity-based blind source separation (BSS): the masks are used to estimate per-source PSD matrices, which drive [[concepts/informed-spatial-filter|informed spatial filters]] for separation. The speech-sparsity assumption (each TF bin dominated by one source) is what makes per-bin labelling meaningful.

## Mask Types

- **Binary mask**: 1 for the dominant source at a bin, 0 for all others.
- **Soft mask**: the entry at each bin represents the *probability* that the corresponding source is dominant — i.e., the posterior source-index probability $p(Z_{tk}=j \mid \mathcal{V}_{1:t})$, where $Z_{tk}$ is the dominant-source label RV.

## Estimation Approaches

- **Clustering-based** (static sources): features (narrowband positions, DOAs, binaural cues, or signal vectors) are modelled as a mixture density; EM estimates the parameters and the posterior source-index probabilities serve as the masks. Taseska & Habets propose an EM variant that *jointly estimates the number of sources* while clustering, using narrowband position estimates from distributed arrays, with a Gaussian-model SPP accounting for speech presence uncertainty.
- **Tracking-based** (moving sources): the masks are obtained from the **data-association probabilities** of an approximate Bayesian multi-source tracker. The measurement-to-source association at each TF bin *is* the mask entry. This avoids the sub-optimality of online clustering for moving sources.
- **DNN-based mask prediction** (single-channel SCSS): a DNN is trained to predict the time-frequency mask directly from the mixture spectrogram. The survey by [[sources/ansari-2023-ai-bss-survey|Ansari et al. 2023]] reports that **DNNs are the most-employed deep-learning algorithm for BSS**, with multi-DNN mask ensembles [126] (softmax/IBM/direct-source/discriminative-constraint cost functions concatenated) outperforming single-DNN predictions. Different mask types trade off distortion vs. cross-talk: ideal binary mask (IBM), ideal ratio mask (IRM), and direct soft-mask prediction each occupy a different point on the SAR/SDR/SIR frontier.

## From Masks to Separation

The TF masks update each source's PSD matrix $\boldsymbol{\Phi}_{\mathbf{s}_j}$ (rank-one, via the RTF vector), and the undesired-signal PSD matrix for each source's ISF is the sum of all *other* sources' PSD matrices plus the noise PSD matrix. Informed MVDR or MWF filters then extract each source. Incorporating SDR-based SPP estimation provides simultaneous noise PSD matrix estimation and noise reduction.

## Open Challenge

A "large gap" remains between ISFs using *oracle* TF masks and those using *estimated* masks — motivating integration of spectral features and DNN-based mask estimation.

## Related Concepts

- [[concepts/informed-spatial-filter|Informed Spatial Filter (ISF)]]
- [[concepts/sparsity-based-source-tracking|Sparsity-Based Source Tracking]]
- [[concepts/acoustic-spotforming|Acoustic Spotforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/multi-channel-wiener-filter|Multichannel Wiener Filter]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]

## Related Sources

- [[sources/taseska-2018-informed-spatial-filters|Taseska 2018: Informed Spatial Filters for Speech Enhancement]] (Chapters 7–8)
- [[sources/ansari-2023-ai-bss-survey|Ansari et al. 2023: AI Approaches in BSS Survey]] — surveys DNN-based mask prediction (Refs. [124, 126, 133, 160, 167]) as a deep-learning BSS sub-area
