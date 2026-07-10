---
type: concept
created: 2026-07-10
updated: 2026-07-10
tags:
  - speech-enhancement
  - distributed
  - binaural
  - hearing-aid
  - mask-estimation
---

# Tango Framework

The **Tango** framework (Furnon et al., 2021) is a two-stage distributed binaural speech enhancement architecture for spatially unconstrained microphone arrays. Each ear-node independently estimates speech and noise masks using a Single-Node DNN (SN-DNN) and computes a Speech Distortion Weighted Multichannel Wiener Filter (SDW-MWF), producing an ear-specific compressed signal that is transmitted to the contra-lateral ear-node. A Multi-Node DNN (MN-DNN) then refines the masks using both local signals and the exchanged representation, from which a final SDW-MWF generates the enhanced binaural output.

## Two-Stage Distributed Architecture

1. **Stage 1 — Single-Node (SN-DNN)**: Each ear independently estimates speech/noise masks from its local microphones and applies an SDW-MWF to produce a compressed signal. This compressed representation (not raw audio) is transmitted to the other ear-node.
2. **Stage 2 — Multi-Node (MN-DNN)**: Each ear combines its local signals with the received contra-lateral compressed representation to refine the masks. A final SDW-MWF produces the enhanced binaural output.

## Key Properties

- **Distributed (fusion-center-free)**: No central node has access to all microphones; only a low-rate compressed signal is exchanged between ears.
- **Spatially unconstrained**: Works with arbitrary microphone configurations, not requiring known geometry or steering vectors.
- **Hybrid neural+linear**: DNNs estimate time-frequency masks that guide classical spatial filters (SDW-MWF), combining data-driven adaptability with interpretable linear filtering.

## Limitations Addressed by RT-Tango

The original Tango formulation imposes no latency or computational complexity constraints, making it unsuitable for direct on-device deployment in hearing aids. [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|RT-Tango (Benslimane et al., 2026)]] revisits Tango from a system-level perspective, adding [[concepts/erb-scale|ERB]] feature compression, [[concepts/grouped-recurrent-neural-network|grouped RNN]] mask estimation, [[concepts/asymmetric-stft|asymmetric STFT]], and [[concepts/fixed-rate-skipping|temporal sparsification]] to satisfy strict causality, ultra-low latency, and low-power constraints while preserving the two-stage distributed spatial filtering scheme.

## Related Concepts

- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]]
- [[concepts/fixed-rate-skipping|Fixed-Rate Skipping]]

## Related Sources

- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
