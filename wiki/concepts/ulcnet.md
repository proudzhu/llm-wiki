---
type: concept
created: 2026-07-16
updated: 2026-07-19
tags:
  - deep-learning
  - speech-enhancement
  - low-complexity
  - noise-suppression
---

# ULCNet

**ULCNet** (Ultra-Low Complexity Network) is a DNN architecture designed for real-time noise suppression on resource-constrained platforms. Originally proposed by Shetu et al. (ICASSP 2024) for the noise suppression task, it achieves state-of-the-art noise reduction performance with ultra-low computational complexity.

## Architecture

ULCNet employs a channel-wise feature reorientation and stacking method to process sub-band features efficiently:

1. The input magnitude spectrum is split into $B$ sub-bands of length $K_B$ with overlap factor $\beta$
2. Sub-band features are reoriented and stacked for efficient processing
3. An Intermediate Feature Computation block uses phase information for complex ratio mask estimation
4. Power-law compression with factor $\alpha$ is applied to input magnitudes

## Extension for AENR

In the hybrid AENR system (Shetu et al., IWAENC 2024), ULCNet was modified with three key changes:

1. **Multi-input**: Takes three inputs $\{Z, \hat{E}, Y\}$ (error signal, echo estimate, far-end signal) instead of single microphone input
2. **Interleaved sub-band stacking**: Sub-bands from three inputs are interleaved before stacking
3. **Phase from error signal**: Uses phase of the error signal instead of microphone signal

## Computational Requirements

| Variant | Parameters | GMACs |
|---------|-----------|-------|
| ULCNet_MS | 0.68M | 0.09 |
| ULCNet_Freq | 0.68M | 0.09 |
| ULCNet_AENR | 0.69M | 0.10 |

For the original (single-task NS) ULCNet configuration re-implemented in TensorFlow by Larraza & de Koeijer (2026), the reported baseline is 0.685M parameters and 2.057M MACs with RTF 0.976 on a Raspberry Pi 3 B+ and 0.927 on an Arm Cortex-A53.

## Extension: Fast-ULCNet

[[sources/larraza-2026-fast-ulcnet-speech-enhancement|Larraza & de Koeijer 2026]] propose [[concepts/fast-ulcnet|Fast-ULCNet]], an extension that replaces ULCNet's GRU layers with [[concepts/fastgrnn|FastGRNN]]-based layers (optionally with the [[concepts/comfi-fastgrnn|Comfi-FastGRNN]] drift-correction variant). The substitution halves the parameter count (0.685M → 0.338M), reduces MACs by ~18%, and improves RTF by ~34% on embedded ARM targets, at matched noise-suppression quality on standard 10 s DNS test signals. The Comfi-FastGRNN variant additionally preserves quality on long (>60 s) streaming sequences where plain FastGRNN suffers from inference-time state drift.

## Extension: μNet

[[sources/shetu-2026-munet|Shetu et al. 2026]] propose [[concepts/munet|μNet]], another descendant of the ULCNet two-stage backbone (magnitude-mask stage + complex ratio mask stage) targeting embedded digital signal processors. μNet keeps the power-law compressed input and channel-wise feature reorientation, but: (i) reverts to standard convolutions instead of depthwise separable ones, since depthwise separable convolutions suffer from fragmented memory access and poor hardware utilization on consumer DSPs; (ii) shares one GRU across subbands and shares a single linear projection across overlapping segments of the latent vector; (iii) supports latencies down to 4 ms via an asymmetric analysis–synthesis window pair and int8 quantization. It requires 46 K parameters, 28 MMACs, and 90 KB static memory — roughly an order of magnitude smaller than ULCNet itself (0.685M parameters), at the cost of reduced enhancement performance (PESQ 1.90–2.27 vs. ULCNet_MS 2.64 on DNS).

While Fast-ULCNet targets floating-point ARM Cortex-A processors, μNet targets integer-only DSPs (Cadence Tensilica HiFi 4/5, ADI SHARC, Qualcomm Hexagon) and neural accelerators, making the two extensions complementary deployment paths for the ULCNet backbone.

## Related Concepts

- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask]]
- [[concepts/power-law-compression|Power-Law Compression]]
- [[concepts/channel-wise-feature-reorientation|Channel-Wise Feature Reorientation]]
- [[concepts/fast-ulcnet|Fast-ULCNet]]
- [[concepts/munet|μNet]]
- [[concepts/fastgrnn|FastGRNN]]
- [[concepts/comfi-fastgrnn|Comfi-FastGRNN]]

## Related Sources

- [[sources/shetu-2024-hybrid-low-complexity-aenr|Shetu et al. 2024: Hybrid Low-Complexity AENR]]
- [[sources/larraza-2026-fast-ulcnet-speech-enhancement|Larraza & de Koeijer 2026: Fast-ULCNet]]
- [[sources/shetu-2026-munet|Shetu et al. 2026: μNet]]
