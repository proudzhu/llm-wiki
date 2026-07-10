---
type: concept
created: 2026-07-10
updated: 2026-07-10
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

## Relationship to Other Grouped Architectures

- [[concepts/gtcrn|GTCRN]] applies grouped RNN within a Dual-Path RNN (G-DPRNN) bottleneck, splitting features and hidden states into 2 groups.
- GRNN as used in RT-Tango originates from the group recurrent networks of Gao et al. (2018) for efficient sequence learning.

## Related Concepts

- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/tango-framework|Tango Framework]]
- [[concepts/gtcrn|GTCRN]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]
- [[concepts/erb-scale|ERB Scale]]

## Related Sources

- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
