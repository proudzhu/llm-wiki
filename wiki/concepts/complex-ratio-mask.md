---
type: concept
created: 2026-05-20
updated: 2026-09-06
sources:
  - raw/papers/zhao-2026-spectrally-adaptive-loss/full-text.md
tags:
  - speech-enhancement
  - deep-learning
  - mask
---

# Complex Ratio Mask (cRM)

The **Complex Ratio Mask (cRM)** is a mask-based speech enhancement target that estimates both the magnitude and phase of the clean speech in the time-frequency domain. Unlike magnitude-only masks such as the ideal ratio mask (IRM), the cRM models the complex-valued ratio between clean and noisy STFT coefficients, enabling phase-aware reconstruction.

A compressed-domain variant appears in [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026]]'s [[concepts/hyst-net|HyST-Net]]: the network estimates a complex-valued ideal ratio mask in the power-law-compressed ($c=0.3$) spectrogram domain, $\widehat{M}_c = |S|^c e^{j\phi_S}/(|X|^c e^{j\phi_X}+\gamma)$, applied to the compressed noisy spectrum and then decompressed — with a small regularisation constant $\gamma$ for numerical stability.

## Related Concepts

- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/complex-convolving-mask|Complex Convolving Mask]]
- [[concepts/ulcnet|ULCNet]]
- [[concepts/munet|μNet]]
- [[concepts/hyst-net|HyST-Net]] — compressed-domain cRM estimation

## Related Sources

- [[sources/shetu-2024-hybrid-low-complexity-aenr|Shetu et al. 2024: Hybrid Low-Complexity AENR]]
- [[sources/shetu-2026-munet|Shetu et al. 2026: μNet]] — second-stage CRM estimation on top of a magnitude mask, inherited from the ULCNet backbone
- [[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng et al. 2023: Sixty Years of Frequency-Domain Monaural Speech Enhancement]] — surveys cIRM (Williamson et al. 2016) and compares masking-based vs. mapping-based training targets
- [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026: Spectrally Adaptive Loss for Streaming Speech Enhancement]] — compressed-domain cRM in HyST-Net
