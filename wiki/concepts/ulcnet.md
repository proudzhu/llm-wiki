---
type: concept
created: 2026-07-16
updated: 2026-07-16
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

## Related Concepts

- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask]]
- [[concepts/power-law-compression|Power-Law Compression]]
- [[concepts/channel-wise-feature-reorientation|Channel-Wise Feature Reorientation]]

## Related Sources

- [[sources/shetu-2024-hybrid-low-complexity-aenr|Shetu et al. 2024: Hybrid Low-Complexity AENR]]
