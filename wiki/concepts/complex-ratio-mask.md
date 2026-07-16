---
type: concept
created: 2026-05-20
updated: 2026-06-06
tags:
  - speech-enhancement
  - deep-learning
  - mask
---

# Complex Ratio Mask (cRM)

The **Complex Ratio Mask (cRM)** is a mask-based speech enhancement target that estimates both the magnitude and phase of the clean speech in the time-frequency domain. Unlike magnitude-only masks such as the ideal ratio mask (IRM), the cRM models the complex-valued ratio between clean and noisy STFT coefficients, enabling phase-aware reconstruction.

## Related Concepts

- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/complex-convolving-mask|Complex Convolving Mask]]
- [[concepts/ulcnet|ULCNet]]

## Related Sources

- [[sources/shetu-2024-hybrid-low-complexity-aenr|Shetu et al. 2024: Hybrid Low-Complexity AENR]]
