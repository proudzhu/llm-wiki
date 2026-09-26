---
type: concept
created: 2026-09-26
updated: 2026-09-26
sources:
  - raw/papers/haeb-umbach-2024-microphone-array-deep-learning/full-text.md
tags:
  - speech-separation
  - speech-enhancement
  - deep-learning
  - multi-channel
  - neural-beamforming
---

# TF-GridNet

**TF-GridNet** (Wang, Cornell, Choi, Lee, Kim & Watanabe, IEEE/ACM TASLP 2023) is a neural architecture for **joint denoising, dereverberation, and source separation** that integrates full-band and sub-band modeling with an explicit beamforming stage. Haeb-Umbach et al. 2024 present it as the prototypical **Class 3 hybrid** — a system whose *enhancement operation itself* combines model-based and data-driven modules ([[sources/haeb-umbach-2024-microphone-array-deep-learning|Haeb-Umbach et al. 2024]]).

## Architecture

- **Alternating full-/sub-band processing**: network layers capture correlations along the time axis (per frequency bin — "subband") and along the frequency axis (per frame — "fullband"). Fullband processing is particularly effective for spatial information, since a source's direction of arrival produces a characteristic phase-change pattern along frequency.
- **Self-attention** layers leverage global information across frames.
- **DNN–BF–DNN structure**: spatial information is aggregated both by multi-channel DNN inputs and by a **multi-frame Wiener filter** beamformer sandwiched between two DNNs — the model-based spatial operation embedded inside the neural enhancement operation (see [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]).

## Significance

TF-GridNet exploits the complementarity that motivates hybrid systems: beamformers are optimal at exploiting spatial information under Gaussian assumptions, while DNNs capture spectro-temporal structure without simplifying assumptions. It has become a standard backbone for multichannel speech separation/enhancement (e.g., serving as the fixed-array backbone that [[concepts/geometry-aware-dynamic-convolution|Geo-DConv]] converts into array-invariant systems).

## Related Concepts

- [[concepts/hybrid-speech-enhancement|Hybrid Speech Enhancement]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/permutation-invariant-training|Permutation Invariant Training (PIT)]]
- [[concepts/attention-mechanism|Attention Mechanism]]

## Related Sources

- [[sources/haeb-umbach-2024-microphone-array-deep-learning|Haeb-Umbach et al. 2024: Microphone Array Signal Processing and Deep Learning for Speech Enhancement]] — Section IV-C treatment as the prototypical joint hybrid
