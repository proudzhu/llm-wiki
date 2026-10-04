---
type: concept
created: 2026-06-01
updated: 2026-10-04
sources:
  - raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/full-text.md
  - raw/papers/yamaoka-2021-bin-wise-beamformer-combination/full-text.md
tags:
  - speech-separation
  - time-frequency-masking
  - training-target
---

# Ideal Binary Mask (IBM)

The Ideal Binary Mask (IBM) is a binary time-frequency mask that labels each T-F unit as either target-dominated (1) or interference-dominated (0). It was the first training target used in supervised speech separation and is inspired by the auditory masking phenomenon and the exclusive allocation principle in auditory scene analysis.

## Definition

$$IBM(t,f) = 1 if SNR(t,f) > LC, else 0$$

where $SNR(t,f)$ is the local signal-to-noise ratio within the T-F unit, and $LC$ is the local criterion (threshold, typically 0 dB).

## Properties

- **Binary nature**: Treats speech separation as a binary classification problem
- **Intelligibility benefit**: IBM masking dramatically improves speech intelligibility for both normal-hearing and hearing-impaired listeners
- **Cost function**: Cross-entropy is commonly used for IBM estimation

## Role in Target Speech Extraction

Zmolikova et al. 2023 [[sources/zmolikova-2023-neural-target-speech-extraction-overview|(Zmolikova 2023)]] use the IBM as the conceptual basis for the **time-frequency masking** target extractor in their general neural TSE framework. The motivation is the **sparseness assumption of speech**: different speakers rarely overlap in a single time-frequency bin of a mixture spectrum, so a mask indicating the bins where the target is dominant suffices to isolate it. The IBM is the idealized version of this mask, assigning each T-F bin entirely to one speaker; modern TSE systems relax this assumption by using **real-valued** or **complex-valued** masks estimated by a neural network $\mathrm{MaskNet}(\mathbf{Z}_{s})$, where $\mathbf{Z}_{s}$ is the mixture representation conditioned on the target clue.

## Binary Masking vs. Binary Beamformer Switching

The IBM multiplies each TF bin by 0/1 based on target dominance — excellent noise reduction, no distortionless guarantee. [[sources/yamaoka-2021-bin-wise-beamformer-combination|Yamaoka, Ono & Makino 2021]] apply the same binary selection logic to *beamformer outputs* instead (their TFS beamformer picks, per TF bin, the MVDR beamformer with minimum output power among $K$ filters that each null a different interferer set), which keeps the masking-style per-bin adaptivity while provably preserving the distortionless property. In their SRDR experiment the IBM showed significant SDR improvement but low SRDR, whereas the switching/combination variants achieved comparable SDR gains with MVDR-level (near-infinite) SRDR.

## Related Concepts

- [[concepts/ideal-ratio-mask|Ideal Ratio Mask (IRM)]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cRM)]]
- [[concepts/permutation-invariant-training|Permutation Invariant Training (PIT)]]
- [[concepts/deep-clustering-speech-separation|Deep Clustering for Speech Separation]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/tflc-beamformer|TFLC Beamforming]] — binary beamformer switching as the distortionless analogue of IBM selection
- [[concepts/w-disjoint-orthogonality|W-Disjoint Orthogonality]] — the sparsity assumption behind per-bin binary selection

## Related Sources

- [[sources/wang-2018-supervised-speech-separation-deep-learning-overview|Wang & Chen 2018: Supervised Speech Separation Based on Deep Learning: An Overview]]
- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova et al. 2023: Neural Target Speech Extraction: An Overview]]
- [[sources/yamaoka-2021-bin-wise-beamformer-combination|Yamaoka, Ono & Makino 2021: TF-Bin-Wise Linear Combination of Beamformers]] — IBM as high-SDR/low-SRDR baseline against distortionless beamformer switching
