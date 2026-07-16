---
type: concept
created: 2026-07-16
updated: 2026-07-16
sources:
  - raw/papers/benslimane-2026-tango-quantized-distributed/full-text.md
tags:
  - speech-enhancement
  - distributed
  - binaural
  - hearing-aid
  - model-compression
  - low-compute
  - mask-estimation
---

# MN-TANGO

**MN-TANGO** is a simplified single-stage variant of the [[concepts/tango-framework|Tango]] distributed binaural speech enhancement framework, introduced by [[entities/zahra-benslimane|Benslimane et al. (2026)]]. It removes the first-stage Single-Node DNN (SN-DNN) entirely, retaining only the Multi-Node DNN (MN-DNN) and the final spatial filtering stage. The motivation is that, once inter-node information is available, the SN-DNN stage is no longer necessary for strong final enhancement — the final [[concepts/gevd-spatial-filtering|GEVD-based]] spatial filter contributes most of the enhancement and compensates for imperfections in the mask estimates.

## Architecture

In MN-TANGO, each ear-node:

1. Exchanges its local reference signal with the contra-lateral ear-node (single inter-node exchange, as in original Tango).
2. Runs a single **MN-DNN** that estimates speech/noise time-frequency masks using both local signals and the received contra-lateral representation.
3. Applies a [[concepts/multi-channel-wiener-filter|SDW-MWF]] / [[concepts/gevd-spatial-filtering|GEVD-based]] spatial filter using the estimated masks and [[concepts/spatial-covariance-matrix|spatial covariance matrices]] to produce the final enhanced binaural output.

This is in contrast to the original two-stage Tango, where a first SN-DNN + SDW-MWF produces a compressed signal that is exchanged and then refined by the MN-DNN + final SDW-MWF.

## Justification

The simplification is justified by three observations from [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026]]:

- The **final spatial filtering stage provides most of the enhancement gain** (e.g., SI-SIR lifts from 13.0/7.8 dB after MN-DNN to 24.3/25.6 dB after GEVD for full TANGO).
- The **spatial filter is robust to mask-estimation errors**, including those introduced by INT8 quantization, so a slightly weaker mask estimator is acceptable.
- MN-TANGO **preserves final enhancement quality** while halving parameters (1.0 M → 0.5 M) and compute (65.65 → 30.79 MMAC/s) compared to full TANGO.

## Low-Compute Variants

MN-TANGO is the vehicle for the paper's combined compression strategy:

- **[[concepts/quantization-aware-training|QAT]] with W8A8** (INT8 weights and activations, 16-bit I/O tensors).
- **[[concepts/erb-scale|ERB]] feature compression** (64 linear + 64 ERB bands → 128-dim recurrent input).
- **[[concepts/grouped-recurrent-neural-network|Grouped LSTM]]** ($G \in \{1,2,4,6,8,10\}$) with deterministic interleaving.

The resulting operating points are:

| Variant | G | MMACs/s | #Params | Memory | SI-SIR L/R (dB) |
|---------|---|---------|---------|--------|------------------|
| MN-TANGO W8A8 | 1 | 30.79 | 0.5 M | 0.508 MB | 23.7 / 24.2 |
| MN-TANGO W8A8 | 2 | **10.79** | 0.179 M | 0.274 MB | 22.7 / 22.8 |
| MN-TANGO W8A8 | 8 | **4.65** | 0.081 M | **0.177 MB** | 21.2 / 21.3 |

The $G=2$ configuration is identified as the best complexity-performance trade-off; $G=8$ is the most compact. Grouping effect is non-monotonic: $G=4$/$6$ degrade noticeably, while $G=8$/$10$ partially recover.

## Relationship to Other Tango Variants

- **[[concepts/tango-framework|Tango]]** (Furnon et al., 2021): Original two-stage architecture (SN-DNN → SDW-MWF → exchange → MN-DNN → SDW-MWF). MN-TANGO removes the first stage.
- **[[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|RT-Tango]]** (Benslimane et al., 2026, arXiv:2607.01834): Real-time, low-latency streaming variant of the full two-stage Tango for hearing-aid deployment; uses ERB + grouped RNN + asymmetric STFT + fixed-rate skipping. MN-TANGO reuses RT-Tango's compression strategy (ERB + grouped LSTM) but applies it to the simplified single-stage architecture and adds INT8 quantization.

## Related Concepts

- [[concepts/tango-framework|Tango Framework]]
- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/quantization-aware-training|Quantization-Aware Training (QAT)]]
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]]
- [[concepts/erb-scale|ERB Scale]]
- [[concepts/gevd-spatial-filtering|GEVD-Based Spatial Filtering]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]

## Related Sources

- [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026: Quantized TANGO / MN-TANGO]]
- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
