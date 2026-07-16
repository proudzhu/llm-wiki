---
type: concept
created: 2026-07-10
updated: 2026-07-16
sources:
  - raw/papers/benslimane-2026-tango-quantized-distributed/full-text.md
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

The SDW-MWF is implemented at inference via its [[concepts/gevd-spatial-filtering|GEVD-based]] rank-constrained form, which improves robustness to spatial-covariance-matrix estimation noise and reduces the cost of the matrix inversion.

## Key Properties

- **Distributed (fusion-center-free)**: No central node has access to all microphones; only a low-rate compressed signal is exchanged between ears.
- **Spatially unconstrained**: Works with arbitrary microphone configurations, not requiring known geometry or steering vectors.
- **Hybrid neural+linear**: DNNs estimate time-frequency masks that guide classical spatial filters (SDW-MWF), combining data-driven adaptability with interpretable linear filtering.
- **Spatial-filter robustness**: The downstream GEVD-based spatial filter contributes most of the final enhancement and compensates for errors in the neural mask estimates — including errors introduced by INT8 quantization. This makes Tango particularly amenable to aggressive neural compression.

## Variants and Simplifications

- **RT-Tango** ([[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al., 2026, arXiv:2607.01834]]): Real-time, low-latency streaming variant that preserves the two-stage architecture while adding [[concepts/erb-scale|ERB]] feature compression, [[concepts/grouped-recurrent-neural-network|grouped RNN]] mask estimation, [[concepts/asymmetric-stft|asymmetric STFT]], and [[concepts/fixed-rate-skipping|temporal sparsification]] to satisfy strict causality, ultra-low latency, and low-power constraints.
- **MN-TANGO** ([[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al., 2026, arXiv:2607.08645]]): A simplified single-stage variant that removes the SN-DNN entirely. Justified by the observation that, once inter-node information is available, the SN-DNN is no longer necessary — the final GEVD filter provides most of the enhancement. See [[concepts/mn-tango|MN-TANGO]].
- **Quantized TANGO / MN-TANGO** (same paper): Applies [[concepts/quantization-aware-training|W8A8 quantization-aware training]] to the neural mask estimators and shows that the spatial filter absorbs most of the resulting mask-error degradation. Combined with ERB compression and grouped LSTM layers, MN-TANGO reaches as low as 4.65 MMAC/s and 0.177 MB.

## Limitations Addressed by RT-Tango

The original Tango formulation imposes no latency or computational complexity constraints, making it unsuitable for direct on-device deployment in hearing aids. RT-Tango addresses the latency/complexity axis; MN-TANGO + quantization addresses the memory/precision axis.

## Related Concepts

- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/gevd-spatial-filtering|GEVD-Based Spatial Filtering]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]]
- [[concepts/fixed-rate-skipping|Fixed-Rate Skipping]]
- [[concepts/mn-tango|MN-TANGO]]
- [[concepts/quantization-aware-training|Quantization-Aware Training (QAT)]]
- [[concepts/post-training-quantization|Post-Training Quantization (DPTQ)]]

## Related Sources

- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
- [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026: Quantized TANGO / MN-TANGO]]
