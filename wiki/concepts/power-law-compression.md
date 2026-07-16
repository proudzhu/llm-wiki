---
type: concept
created: 2026-07-16
updated: 2026-07-16
tags:
  - signal-processing
  - speech-enhancement
  - feature-engineering
---

# Power-Law Compression

**Power-law compression** is a nonlinear magnitude compression technique used in speech enhancement and acoustic echo reduction systems to reduce the dynamic range of spectral magnitudes before feeding them into a neural network. The compressed magnitude is computed as:

$$\tilde{X}_m = |X|^\alpha$$

where $\alpha \in (0, 1)$ is the compression factor (typically 0.3 in ULCNet-based systems).

## Purpose

- Reduces the large dynamic range of speech spectra, making it easier for DNNs to learn
- Preserves relative spectral structure while compressing large values
- Avoids the information loss of logarithmic compression near zero

## Trade-offs

The compression factor $\alpha$ affects the balance between echo reduction and speech quality. As noted in Shetu et al. (2024), the modified power-law compression contributes to slightly lower DMOS scores in double-talk scenarios due to the aggressive nature of the suppression.

## Related Concepts

- [[concepts/ulcnet|ULCNet]]
- [[concepts/channel-wise-feature-reorientation|Channel-Wise Feature Reorientation]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/shetu-2024-hybrid-low-complexity-aenr|Shetu et al. 2024: Hybrid Low-Complexity AENR]]
