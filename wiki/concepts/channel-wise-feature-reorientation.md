---
type: concept
created: 2026-07-16
updated: 2026-07-16
tags:
  - signal-processing
  - speech-enhancement
  - feature-engineering
---

# Channel-Wise Feature Reorientation

**Channel-wise feature reorientation** is a feature processing technique used in low-complexity speech enhancement networks (notably ULCNet) to efficiently organize and process sub-band spectral features. The method splits the frequency axis into overlapping sub-bands, reorients them along the channel dimension, and stacks them for efficient convolutional processing.

## Method

1. Split the compressed magnitude spectrum into $B$ sub-bands of length $K_B$ with overlap factor $0 \leq \beta < 1$
2. Reorient sub-bands along the channel dimension
3. Stack reoriented features for input to the network

## Multi-Input Extension

For the joint AENR task with three inputs $\{Z, \hat{E}, Y\}$, the sub-bands are interleaved:

$$[\tilde{Z}_{m,0}, \tilde{E}_{m,0}, \tilde{Y}_{m,0}, \ldots, \tilde{Z}_{m,B-1}, \tilde{E}_{m,B-1}, \tilde{Y}_{m,B-1}]$$

This interleaving preserves the frequency-wise correspondence between inputs while enabling the network to learn cross-input relationships within each sub-band.

## Related Concepts

- [[concepts/ulcnet|ULCNet]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/power-law-compression|Power-Law Compression]]

## Related Sources

- [[sources/shetu-2024-hybrid-low-complexity-aenr|Shetu et al. 2024: Hybrid Low-Complexity AENR]]
