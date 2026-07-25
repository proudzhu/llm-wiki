---
type: concept
created: 2026-07-25
updated: 2026-07-25
sources:
  - raw/papers/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction/full-text.md
tags:
  - neural-network
  - target-speech-extraction
  - embedding-free
  - personalized-speech-enhancement
---

# SEF-PNet

**SEF-PNet** (Speaker Encoder-Free Personalized Network) is an embedding/encoder-free target speech extraction (TSE) backbone proposed by Huang et al. (ICASSP 2025). It belongs to the embedding-free family of [[concepts/personalized-speech-enhancement|personalized speech enhancement]] methods, which avoid explicit pretrained speaker embeddings and instead model enrollment–mixture interactions directly. SEF-PNet serves as the competitive baseline backbone for the LGTSE and D-LGTSE frameworks.

## Architecture

SEF-PNet consists of:

- An **encoder** and symmetric **decoder**
- A **Temporal Convolutional Network (TCN)** module
- A **PyramidBlock** for multi-scale feature aggregation
- A **Deconv2d** layer
- (In the original design) an **Iterative Feature Integration (IFI)** block

The enrollment guidance is obtained by direct context interaction between the enrollment and the noisy mixture in the STFT domain (see [[concepts/noise-agnostic-enrollment-guidance|Noise-agnostic Enrollment Guidance]] for the formulation), and concatenated with the noisy feature for the backbone.

## Role as Baseline

In Huang et al. (2026), SEF-PNet is used in a **simplified form**: the IFI block is removed to ensure a fair comparison with LGTSE and D-LGTSE. All other architectural details remain as in the original ICASSP 2025 paper. The simplified SEF-PNet establishes the baseline performance on Libri2Mix (2-speaker + noise):

| Backbone | Params (M) | MACs (G/s) | SI-SDR (dB) | PESQ | STOI (%) |
|:---------|:----------:|:----------:|:-----------:|:----:|:--------:|
| SEF-PNet (simplified) | 6.08 | 8.50 | 7.43 | 2.14 | 80.31 |
| D-LGTSE (SEF-PNet + GTCRN) | 6.13 | 8.53 | 8.32 | 2.30 | 82.28 |

## Position in the Embedding-free TSE Landscape

Embedding-free TSE methods — including SEF-Net, SEF-PNet, [[concepts/cie-mdptnet|CIE-mDPTNet]], and CIE-mDPTNet — avoid the storage and inference cost of pretrained speaker-embedding models and have increasingly approached or exceeded SOTA performance. SEF-PNet is a CNN-based backbone (6.08 M params, 8.50 GMACs/s), whereas CIE-mDPTNet is a lighter but more compute-intensive alternative (2.87 M params, 22.25 GMACs/s) that achieves higher absolute quality.

## Related Concepts

- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/personalized-speech-enhancement|Personalized Speech Enhancement]]
- [[concepts/noise-agnostic-enrollment-guidance|Noise-agnostic Enrollment Guidance]]
- [[concepts/distortion-aware-training|Distortion-aware Training]]
- [[concepts/cie-mdptnet|CIE-mDPTNet]]
- [[concepts/speaker-embedding|Speaker Embedding]]

## Related Sources

- [[sources/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction|Huang et al. 2026: Lightweight Speech Enhancement Guided Target Speech Extraction in Noisy Multi-Speaker Scenarios]] — uses simplified SEF-PNet as baseline backbone.
