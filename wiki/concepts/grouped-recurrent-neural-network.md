---
type: concept
created: 2026-07-10
updated: 2026-07-22
sources:
  - raw/papers/benslimane-2026-tango-quantized-distributed/full-text.md
tags:
  - neural-network
  - recurrent
  - efficiency
  - speech-enhancement
  - grouped-convolution
---

# Grouped Recurrent Neural Network (GRNN)

A **Grouped Recurrent Neural Network (GRNN)** partitions the hidden state of a recurrent layer into $G$ independent groups, each processed by a smaller recurrent sub-network. Grouping exploits the localized nature of spectral dependencies in speech signals — spectral correlations are typically stronger within nearby frequency sub-bands than across the entire spectrum — while reducing the quadratic computational cost of recurrent layers.

## Computational Motivation

The computational cost of a standard recurrent layer scales approximately quadratically with the hidden state dimension $H$:

$$\mathcal{O}(H^{2})$$

By partitioning the feature space into $G$ groups of size $H/G$, each processed independently, the total recurrent complexity becomes:

$$G \cdot \mathcal{O}\!\left(\left(\frac{H}{G}\right)^{2}\right) = \mathcal{O}\!\left(\frac{H^{2}}{G}\right)$$

a $G$-fold reduction over a full-band RNN.

## Cross-Band Information Exchange

Although processing is performed independently within each group, cross-band dependencies are captured through a **representation rearrangement** (channel-shuffle) mechanism that periodically exchanges information between groups. This enables global spectral modeling while keeping per-step recurrent cost low — analogous to grouped convolution with channel shuffling in ShuffleNet.

## Application in RT-Tango

In [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|RT-Tango (Benslimane et al., 2026)]], GRNNs replace standard recurrent layers in both the Single-Node (SN-DNN) and Multi-Node (MN-DNN) mask estimators of the [[concepts/tango-framework|Tango]] baseline:

- **SN-DNN**: $G=8$ groups — significantly reduces cost with negligible impact on quality (SI-SDR maintained at 4.7/4.9 dB, DNN cost reduced from 1.06 to 0.59 MMAC/frame).
- **MN-DNN**: $G=2$ groups — the MN-DNN is more sensitive to grouping; $G=8$ degrades SI-SDR/SI-SAR by ~0.8–1 dB, so a conservative 2-group configuration is adopted.

The combined strategy (SN=8, MN=2) reduces total DNN complexity from 67.2 to 18.2 MMAC/s while preserving interaural balance.

## Application in Quantized MN-TANGO

In [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026 (Quantized TANGO)]], grouped LSTM layers are used inside [[concepts/mn-tango|MN-TANGO]] (the single-stage simplification of TANGO). The original 3-layer unidirectional LSTM is replaced with a 2-layer grouped LSTM (128 hidden units), with $G \in \{1, 2, 4, 6, 8, 10\}$ evaluated.

Key findings:

- The LSTM dominates neural compute: 459.26 kMAC/frame at $G=1$ vs. 27.04 kMAC/frame at $G=10$ — a ~17× reduction.
- The grouping effect is **not strictly monotonic**: $G=2$ gives the best quality, $G=4$/$6$ degrade noticeably, and $G=8$/$10$ partially recover (depending on how the recurrent representation partitions across groups).
- **Best trade-off**: $G=2$ → 10.79 MMAC/s, 0.179 M params, 0.274 MB (after W8A8 quantization).
- **Most compact**: $G=8$ → 4.65 MMAC/s, 0.081 M params, 0.177 MB.
- Because the downstream [[concepts/gevd-spatial-filtering|GEVD-based]] filter absorbs most mask-estimation degradation, the grouped + quantized MN-TANGO variants retain competitive final SI-SIR/STOI/PESQ even at extreme compression.

## Relationship to Other Grouped Architectures

- [[concepts/gtcrn|GTCRN]] applies grouped RNN within a Dual-Path RNN (G-DPRNN) bottleneck, splitting features and hidden states into 2 groups.
- [[concepts/adaptcrn|AdaptCRN]] (Wang et al. 2025) inherits GTCRN's grouped-DPRNN pattern verbatim (2 groups, intra-frame grouped GRU hidden 8, inter-frame grouped GRU hidden 16) for its bottleneck — and goes further by removing the representation rearrangement after the grouped RNN, noting that the subsequent FC layer inherently performs inter-group fusion and rearrangement is mathematically equivalent to permuting the FC weight rows. This is a useful simplification for ultra-lightweight models where every parameter counts.
- GRNN as used in RT-Tango and MN-TANGO originates from the group recurrent networks of Gao et al. (2018) for efficient sequence learning.

## Related Concepts

- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/tango-framework|Tango Framework]]
- [[concepts/mn-tango|MN-TANGO]]
- [[concepts/quantization-aware-training|Quantization-Aware Training (QAT)]]
- [[concepts/gtcrn|GTCRN]]
- [[concepts/adaptcrn|AdaptCRN]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]
- [[concepts/erb-scale|ERB Scale]]

## Related Sources

- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
- [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026: Quantized TANGO / MN-TANGO]]
- [[sources/wang-2025-adaptive-convolution-cnn-speech-enhancement|Wang et al. 2025: Adaptive Convolution for CNN-based Speech Enhancement Models]] — AdaptCRN's grouped-DPRNN bottleneck (with rearrangement removed)
