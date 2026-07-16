---
type: concept
created: 2026-07-10
updated: 2026-07-16
sources:
  - raw/papers/benslimane-2026-tango-quantized-distributed/full-text.md
tags:
  - speech-enhancement
  - binaural
  - distributed
  - hearing-aid
  - multi-channel
---

# Distributed Binaural Speech Enhancement

**Distributed binaural speech enhancement** addresses the problem of enhancing speech for a two-device (left/right) hearing system — such as a pair of hearing aids — where each ear-node processes its local microphone signals and exchanges only a minimal, compressed representation with the contra-lateral node over a wireless link. Unlike centralized multi-channel processing, which assumes all microphone signals are available at a single node, the distributed setting is imposed by the severe energy and bandwidth constraints of wearable hearing devices.

## Motivation

Binaural hearing devices (hearing aids, earbuds) place microphones on physically separated nodes. Centralized processing would require continuous high-bandwidth wireless transmission of multi-channel audio, which is infeasible under the energy and latency budgets of battery-powered wearables. Distributed frameworks balance speech enhancement (SE) performance against bandwidth-efficient inter-device communication, exchanging only a low-rate compressed signal rather than raw microphone data.

## Key Characteristics

- **Two-stage processing**: A local (single-node) stage estimates initial masks and spatial filters; a second (multi-node) stage refines them using the exchanged representation.
- **Inter-node communication**: Only a compressed signal (or mask) is transmitted, not full-bandwidth multichannel audio.
- **Strict causality and low latency**: Hearing-aid applications demand algorithmic latency of $\leq 10$ ms to preserve lip-reading sync and conversational naturalness.
- **Interaural balance**: Preserving left/right perceptual balance is critical for stable spatial perception and listening comfort.

## Representative Frameworks

- **Tango** (Furnon et al., 2021): A two-stage distributed architecture using DNN-based mask estimation and a Speech Distortion Weighted Multichannel Wiener Filter (SDW-MWF). Each ear-node estimates speech/noise masks, computes a compressed signal via SDW-MWF, transmits it to the contra-lateral node, then a Multi-Node DNN refines the masks for a final SDW-MWF. See [[concepts/tango-framework|Tango Framework]].
- **RT-Tango** (Benslimane et al., 2026): A real-time, low-latency redesign of Tango for hearing aids, adding [[concepts/erb-scale|ERB]] feature compression, [[concepts/grouped-recurrent-neural-network|grouped RNN]] mask estimation, [[concepts/asymmetric-stft|asymmetric STFT]], and [[concepts/fixed-rate-skipping|temporal sparsification]]. See [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026]].
- **MN-TANGO** (Benslimane et al., 2026): A simplified single-stage variant that removes the SN-DNN entirely, retaining only the MN-DNN and the final [[concepts/gevd-spatial-filtering|GEVD-based]] spatial filter. Combined with [[concepts/quantization-aware-training|W8A8 quantization]], ERB compression, and grouped LSTM, it reaches as low as 4.65 MMAC/s and 0.177 MB. See [[concepts/mn-tango|MN-TANGO]] and [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026]].

## Robustness of Hybrid Neural-Spatial Architectures

A distinguishing property of distributed binaural SE frameworks with a hybrid neural-mask + classical-spatial-filter structure is that the **spatial filter compensates for most errors in the neural mask estimators** — including errors introduced by INT8 quantization. In MN-TANGO, W8A8 quantization degrades the intermediate MN-DNN mask output SI-SIR by ~1.5 dB, but the final GEVD-filtered output is within 0.1–0.6 dB of the FP32 baseline. This makes hybrid distributed binaural SE particularly well-suited to aggressive neural compression for resource-constrained hearing-aid deployment.

## Relationship to Multi-Channel Speech Enhancement

Distributed binaural SE is a special case of [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] with the additional constraints of (1) physically separated microphone subsets, (2) limited inter-node communication bandwidth, and (3) real-time/ultra-low-latency operation. The spatial filtering is typically performed via [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]] variants (e.g., SDW-MWF) guided by neural mask estimators.

## Related Concepts

- [[concepts/tango-framework|Tango Framework]]
- [[concepts/mn-tango|MN-TANGO]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/gevd-spatial-filtering|GEVD-Based Spatial Filtering]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/asymmetric-stft|Asymmetric STFT]]
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]]
- [[concepts/fixed-rate-skipping|Fixed-Rate Skipping]]
- [[concepts/erb-scale|ERB Scale]]
- [[concepts/quantization-aware-training|Quantization-Aware Training (QAT)]]
- [[concepts/audio-latency|Audio Latency]]

## Related Sources

- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
- [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026: Quantized TANGO / MN-TANGO]]
