---
type: concept
created: 2026-05-20
updated: 2026-09-13
sources:
  - raw/papers/zhao-2026-spectrally-adaptive-loss/full-text.md
  - raw/papers/zhang-2021-adl-mvdr/full-text.md
  - raw/papers/pandey-2025-ultra-low-compute/full-text.md
  - raw/papers/zhang-2024-enhanced-hybrid-ahs/full-text.md
tags:
  - speech-enhancement
  - deep-learning
  - mask
---

# Complex Ratio Mask (cRM)

The **Complex Ratio Mask (cRM)** is a mask-based speech enhancement target that estimates both the magnitude and phase of the clean speech in the time-frequency domain. Unlike magnitude-only masks such as the ideal ratio mask (IRM), the cRM models the complex-valued ratio between clean and noisy STFT coefficients, enabling phase-aware reconstruction.

A compressed-domain variant appears in [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026]]'s [[concepts/hyst-net|HyST-Net]]: the network estimates a complex-valued ideal ratio mask in the power-law-compressed ($c=0.3$) spectrogram domain, $\widehat{M}_c = |S|^c e^{j\phi_S}/(|X|^c e^{j\phi_X}+\gamma)$, applied to the compressed noisy spectrum and then decompressed — with a small regularisation constant $\gamma$ for numerical stability.

A **complex ratio filter (cRF)** — the multi-tap T-F generalization of the cRM (a cRM is a 1×1 cRF), introduced by Mack & Habets 2019 as deep filtering — exploits neighboring T-F bins instead of pointwise multiplication; see [[concepts/deep-filtering|Deep Filtering]]. [[sources/zhang-2021-adl-mvdr|Zhang et al. 2021]] provide multi-channel evidence for the generalization: a 3×3 cRF consistently outperforms the cRM in both purely NN systems (Si-SNR 12.50 vs. 12.23 dB; WER 22.07 vs. 22.49%) and MVDR-based systems, with the gap widening when the filtered estimates recursively drive frame-level covariance computation in [[concepts/adl-mvdr|ADL-MVDR]].

[[sources/pandey-2025-ultra-low-compute|Pandey & Azcarreta 2025]] provide two findings for the low-compute multichannel regime. First, a **simplified complex multiplication** — applying the real and imaginary parts of the mask separately to the corresponding parts of the noisy spectrum, $\hat{\mathbf{S}}_r = \Re(\mathbf{Y}_r)\cdot\Re(\mathbf{M}) + j\,\Im(\mathbf{Y}_r)\cdot\Im(\mathbf{M})$ — performs on par with full complex multiplication at lower computational cost. Second, the cRM's advantage over magnitude masking **emerges only when a multichannel Wiener filter is in the loop**: standalone, their TinyGRU performs comparably across sigmoid/softplus magnitude and complex masking, but with MCWF integration complex masking pulls clearly ahead (STOI 73.9 vs 71.7), indicating the spatial information enables more precise phase estimation. Conversely, the ERB magnitude-masking MC-CRN baseline *degrades* when paired with MCWF.

[[sources/zhang-2024-enhanced-hybrid-ahs|Zhang et al. 2024]] contribute an acoustic-howling-suppression data point on cRM **input design**: with a small 2-layer LSTM (8 ms frames, magnitude-only features), a complex ratio mask whose input concatenates magnitude and complex spectrograms (cRM2: $[|\mathbf{Y}|, |\mathbf{E}|, \mathbf{Y}_r, \mathbf{Y}_i]$) beats the purely complex input (cRM1) and all magnitude-only masks (RM, PSM) in SDR, resolving the mild residual howling (continuous horizontal spectrogram lines) left by magnitude-only estimation — at a slight PESQ cost, and with slightly *worse* WER than plain RM, plausibly because the small network cannot support the higher complexity of complex-domain estimation.

## Related Concepts

- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/complex-convolving-mask|Complex Convolving Mask]]
- [[concepts/ulcnet|ULCNet]]
- [[concepts/munet|μNet]]
- [[concepts/hyst-net|HyST-Net]] — compressed-domain cRM estimation
- [[concepts/tinygru|TinyGRU]] — ultra-low-compute multichannel cRM whose advantage emerges with MCWF integration
- [[concepts/deep-filtering|Deep Filtering]] — multi-tap (cRF) generalization of the cRM
- [[concepts/adl-mvdr|ADL-MVDR]] — multi-channel system where 3×3 cRF beats cRM and drives frame-level covariance estimation

## Related Sources

- [[sources/shetu-2024-hybrid-low-complexity-aenr|Shetu et al. 2024: Hybrid Low-Complexity AENR]]
- [[sources/shetu-2026-munet|Shetu et al. 2026: μNet]] — second-stage CRM estimation on top of a magnitude mask, inherited from the ULCNet backbone
- [[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng et al. 2023: Sixty Years of Frequency-Domain Monaural Speech Enhancement]] — surveys cIRM (Williamson et al. 2016) and compares masking-based vs. mapping-based training targets
- [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026: Spectrally Adaptive Loss for Streaming Speech Enhancement]] — compressed-domain cRM in HyST-Net
- [[sources/zhang-2021-adl-mvdr|Zhang et al. 2021: ADL-MVDR]] — multi-channel cRM vs. cRF comparison; cRF wins consistently
- [[sources/pandey-2025-ultra-low-compute|Pandey & Azcarreta 2025: Ultra Low-Compute Complex Spectral Masking for Multichannel Speech Enhancement]] — simplified Re/Im complex multiplication; cRM advantage emerges only with MCWF integration
- [[sources/zhang-2024-enhanced-hybrid-ahs|Zhang, Zhang, Yu & Yu 2024: Enhanced Acoustic Howling Suppression]] — cRM2 (magnitude + complex input) resolves residual howling where magnitude masks fail, at a WER cost for small networks
