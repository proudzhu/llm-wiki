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
  - dual-path
---

# CIE-mDPTNet

**CIE-mDPTNet** (Contextual Information Exploitation multi-scale Dual-Path Transformer Network) is an embedding-free target speech extraction (TSE) backbone proposed by Yang et al. (Interspeech 2024). It directly exploits contextual information in the time–frequency domain and represents a state-of-the-art TSE architecture against which newer methods are benchmarked.

## Architecture

The detailed architecture is given in Yang et al. (Interspeech 2024). At a high level, CIE-mDPTNet performs context interaction between enrollment and mixture directly in the STFT domain (rather than via explicit speaker embeddings) and processes the fused representation with a dual-path Transformer network. It is lighter in parameters than CNN-based competitors but more compute-intensive.

## Role as SOTA Baseline

In Huang et al. (2026), CIE-mDPTNet is included as a strong baseline to validate the generalizability of the D-LGTSE framework across backbones. D-LGTSE-mDPTNet (Offline) equips CIE-mDPTNet with the [[concepts/noise-agnostic-enrollment-guidance|noise-agnostic enrollment guidance]] and [[concepts/distortion-aware-training|distortion-aware training]] extensions:

| Backbone | Params (M) | MACs (G/s) | SI-SDR (dB) | PESQ | STOI (%) |
|:---------|:----------:|:----------:|:-----------:|:----:|:--------:|
| CIE-mDPTNet | 2.87 | 22.25 | 10.87 | 2.73 | 87.26 |
| D-LGTSE-mDPTNet (Offline) | 2.92 | 22.28 | 11.70 | 2.86 | 88.83 |

D-LGTSE-mDPTNet adds +0.83 dB SI-SDR, +0.13 PESQ, and +1.57% STOI over the CIE-mDPTNet baseline, at negligible overhead (+0.05 M params, +0.03 GMACs/s).

## Efficiency Note

Although CIE-mDPTNet has fewer parameters than [[concepts/sef-pnet|SEF-PNet]] (2.87 M vs 6.08 M), its MACs/s is ~2.6× higher (22.25 vs 8.50 GMACs/s). This is why absolute quality metrics under CIE-mDPTNet exceed those under SEF-PNet — the comparison is not parameter-matched. The D-LGTSE framework's gains are consistent across both backbones, indicating that noise-agnostic guidance and distortion-aware training are orthogonal to the backbone's architecture.

## Related Concepts

- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/sef-pnet|SEF-PNet]]
- [[concepts/noise-agnostic-enrollment-guidance|Noise-agnostic Enrollment Guidance]]
- [[concepts/distortion-aware-training|Distortion-aware Training]]
- [[concepts/speaker-embedding|Speaker Embedding]]

## Related Sources

- [[sources/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction|Huang et al. 2026: Lightweight Speech Enhancement Guided Target Speech Extraction in Noisy Multi-Speaker Scenarios]] — uses CIE-mDPTNet as SOTA baseline backbone.
