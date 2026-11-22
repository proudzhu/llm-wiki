---
type: concept
created: 2026-06-19
updated: 2026-11-22
sources:
  - raw/papers/dang-2022-dpt-fsnet/full-text.md
  - raw/papers/shetu-2026-generative-discriminative-comparison/full-text.md
  - raw/papers/pandey-2025-ultra-low-compute/full-text.md
  - raw/papers/ohlenbusch-2026-pas-se/full-text.md
  - wiki/sources/wu-2026-dbmif-multimodal-fusion.md
  - raw/papers/zhao-2025-lightweight-transformer/full-text.md
  - raw/papers/li-2024-dbccrn/full-text.md
  - raw/papers/fu-2020-metricgan-post-processing/full-text.md
tags:
  - dataset
  - challenge
  - speech-enhancement
---

# DNS Challenge (Deep Noise Suppression)

The DNS Challenge (Deep Noise Suppression) is a series of challenges organized by Microsoft to advance speech enhancement research. The DNS Challenge 2020 dataset provides large-scale clean speech and noise recordings with standardized evaluation sets. It is commonly used for cross-domain evaluation of speech enhancement models trained on other datasets.

The Microsoft DNS Challenge inspired the [[concepts/intel-neuromorphic-dns-challenge|Intel Neuromorphic DNS Challenge]] ([[sources/timcheck-2023-intel-neuromorphic-dns-challenge|Timcheck et al. 2023]]), which reuses the Microsoft DNS Challenge corpus for its 500-hour dataset but reframes the task around neuromorphic hardware (Loihi 2) with holistic evaluation of audio quality, power, latency, and chip resources — rather than the Microsoft DNS Challenge's CPU architecture constraint and audio-quality-centric metrics. The Intel N-DNS Challenge also benchmarks against Microsoft [[concepts/nsnet2|NsNet2]] (the DNS 2022 baseline) as its conventional comparison point.

The DNS Challenge corpus is also the basis for large controlled training regimes: [[sources/shetu-2026-generative-discriminative-comparison|Shetu, Habets & Brendel 2026]] derive ~1000-hour high-SNR ([-5,30] dB) and low-SNR ([-25,0] dB) training sets and the non-reverberant test set from the Interspeech 2020 DNS Challenge to compare generative and discriminative SE methods.

[[sources/pandey-2025-ultra-low-compute|Pandey & Azcarreta 2025]] use the Interspeech 2020 DNS Challenge corpus (85/5/10 split) to generate multichannel training pairs for an 8-microphone circular array simulated with Pyroomacoustics — SNR [−10, 10] dB, SIR [−5, 15] dB, 1–10 noise sources plus babble from 8–16 interfering talkers — for their ultra-low-compute TinyGRU multichannel enhancement model.

The fifth DNS Challenge noise set was used by [[sources/ohlenbusch-2026-pas-se|Ohlenbusch et al. 2026]] to spatialize the Oldenburg cross-dataset evaluation of hearable own-voice enhancement: noise signals convolved with per-user impulse responses measured from 8 evenly spaced loudspeakers in a circle around the device user yield multi-channel spatialized noise.

[[sources/li-2024-dbccrn|Li et al. 2024]] use the Interspeech 2020 DNS corpus (180 h noise, 500+ h speech from 2150 speakers at 44.1 kHz) to synthesize 100 h of training pairs with the official script (SNR uniform −5…20 dB), evaluating on the official non-reverberant test set: their VoiceBank-trained [[concepts/dbccrn|DBCCRN]] transfers zero-shot to PESQ 2.220 — matching a DNS-trained DCCRN (2.204) — and retraining with [[concepts/scale-aware-snr|SA-SNR]] reaches 2.638 (vs NSNet 1.811, RNNoise 1.973).

[[sources/dang-2022-dpt-fsnet|Dang, Chen & Zhang 2022]] train [[concepts/dpt-fsnet|DPT-FSNet]] on the Interspeech 2020 DNS corpus with dynamic mixing (75% of clean speech convolved with ICASSP-2021 RIRs each epoch, SNR uniform −5…20 dB) and evaluate on both non-blind sets: WB-PESQ 3.53 (`with_reverb`) / 3.26 (`no_reverb`), STOI 95.23 / 97.68%, SI-SDR 18.14 / 20.36 dB — ahead of NSNet, FullSubNet, CTS-Net and GaGNet on every metric, with the margin over the full-band baseline larger on the reverberant set (attributed to sub-band temporal modeling).

[[sources/fu-2020-metricgan-post-processing|Fu et al. 2020]] submitted an APSIPA ASC system to the Interspeech 2020 DNS Challenge: a causal Transformer with convolutional positional encoding, trained on a 10,000-utterance subset of the default synthetic configuration and fine-tuned with MetricGAN. On the no-reverb synthetic set it scores PESQ 3.104 / STOI 0.946 vs the NSNet baseline's 2.692 / 0.906 (noisy 2.454 / 0.915 — NSNet lowers STOI below noisy), and on the organizer-run P.808 blind test (10 judges/clip, 95% CI ≈ 0.02) MOS 3.21 overall vs NSNet 3.03, winning all three categories (noreverb 3.63, realrec 3.18, reverb 2.83 — NSNet degrades reverb below noisy, 2.64 vs 2.78).

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
- [[sources/pandey-2025-ultra-low-compute|Pandey & Azcarreta 2025: Ultra Low-Compute Complex Spectral Masking for Multichannel Speech Enhancement]] — DNS 2020 corpus + simulated 8-mic array for TinyGRU training
- [[sources/ohlenbusch-2026-pas-se|Ohlenbusch, Kegler & Stamenovic 2026: PAS-SE]] — DNS-5 noise spatialized for the Oldenburg cross-dataset evaluation
- [[sources/wu-2026-dbmif-multimodal-fusion|Wu et al. 2026: DBMIF]] — DNS Challenge noise as training interference for AC/BC enhancement; DNSMOS as the non-intrusive evaluation metric
- [[sources/zhao-2025-lightweight-transformer|Zhao & Madhu 2025: LCT-GAN]] — DNS3 140 h synthesised training (SNR −5…20 dB), evaluated on the blind real-recorded English test set with DNSMOS P.835: BAK 4.04 ± 0.09 / SIG 3.06 / OVL 2.80 at 0.14 M params, beating DeepFilterNet1–3 on BAK with half the score variance
- [[sources/li-2024-dbccrn|Li, Sun, Zhang & Van hamme 2024: DBCCRN]] — 100 h DNS-2020 synthesized training (SNR −5…20 dB); zero-shot VBD→DNS transfer matches DNS-trained DCCRN, retrain PESQ 2.638
- [[sources/dang-2022-dpt-fsnet|Dang, Chen & Zhang 2022: DPT-FSNet]] — DNS 2020 dynamic mixing (75% RIR, SNR −5…20 dB); WB-PESQ 3.53/3.26 on with/without reverb, best of eight compared systems
- [[sources/fu-2020-metricgan-post-processing|Fu et al. 2020: MetricGAN Post-Processing]] — DNS 2020 submission: causal Transformer + MetricGAN fine-tuning, PESQ 3.104 / STOI 0.946 and P.808 MOS 3.21 vs NSNet 3.03