---
type: concept
created: 2026-06-19
updated: 2026-09-03
sources:
  - raw/papers/shetu-2026-generative-discriminative-comparison/full-text.md
tags:
  - dataset
  - challenge
  - speech-enhancement
---

# DNS Challenge (Deep Noise Suppression)

The DNS Challenge (Deep Noise Suppression) is a series of challenges organized by Microsoft to advance speech enhancement research. The DNS Challenge 2020 dataset provides large-scale clean speech and noise recordings with standardized evaluation sets. It is commonly used for cross-domain evaluation of speech enhancement models trained on other datasets.

The Microsoft DNS Challenge inspired the [[concepts/intel-neuromorphic-dns-challenge|Intel Neuromorphic DNS Challenge]] ([[sources/timcheck-2023-intel-neuromorphic-dns-challenge|Timcheck et al. 2023]]), which reuses the Microsoft DNS Challenge corpus for its 500-hour dataset but reframes the task around neuromorphic hardware (Loihi 2) with holistic evaluation of audio quality, power, latency, and chip resources — rather than the Microsoft DNS Challenge's CPU architecture constraint and audio-quality-centric metrics. The Intel N-DNS Challenge also benchmarks against Microsoft [[concepts/nsnet2|NsNet2]] (the DNS 2022 baseline) as its conventional comparison point.

The DNS Challenge corpus is also the basis for large controlled training regimes: [[sources/shetu-2026-generative-discriminative-comparison|Shetu, Habets & Brendel 2026]] derive ~1000-hour high-SNR ([-5,30] dB) and low-SNR ([-25,0] dB) training sets and the non-reverberant test set from the Interspeech 2020 DNS Challenge to compare generative and discriminative SE methods.

## Related Concepts

- [[concepts/voicebank-demand|VoiceBank+DEMAND (VBD)]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/intel-neuromorphic-dns-challenge|Intel Neuromorphic DNS Challenge]] — neuromorphic counterpart inspired by the Microsoft DNS Challenge
- [[concepts/nsnet2|NSNet2]] — Microsoft DNS 2022 baseline

## Related Sources

- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]
- [[sources/zhao-2024-sicrn|Zhao, He & Zhang 2024: SICRN]] — single-channel SE on DNS Challenge 2020; 2.16 M params, 4.24 G/s MACs, 0 ms look-ahead, near-FullSubNet quality
- [[sources/timcheck-2023-intel-neuromorphic-dns-challenge|Timcheck et al. 2023: The Intel Neuromorphic DNS Challenge]] — derives its 500-hour dataset from the Microsoft DNS Challenge corpus and benchmarks against NsNet2
- [[sources/liu-2026-sse-net|Liu et al. 2026: SSE-Net]] — SNN-based SE trained/evaluated on WSJ0-SI84 + DNS-Challenge noise (causal setup) and VoiceBank+DEMAND; benchmarked against Intel N-DNS Challenge power-proxy metrics (0.44 G/s MACs, 19.70 M Ops/s power proxy)
- [[sources/shetu-2026-generative-discriminative-comparison|Shetu, Habets & Brendel 2026: Generative vs. Discriminative SE]] — ~1000-h DNS-derived high/low-SNR training sets and non-reverb test set for the 14-model paradigm comparison