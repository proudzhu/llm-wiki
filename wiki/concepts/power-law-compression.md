---
type: concept
created: 2026-07-16
updated: 2026-09-06
sources:
  - raw/papers/li-2020-residual-noise-control/full-text.md
  - raw/papers/zhao-2026-spectrally-adaptive-loss/full-text.md
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

Zheng et al. (2023) report a surprising listener-dependent effect of input-feature compression: compressed features improve PESQ/ESTOI/SDR/DNSMOS/HASQI scores for simulated normal-hearing listeners, but do *not* help (and sometimes slightly hurt) HASQI/HASPI scores for simulated hearing-impaired listeners (audiograms N2 mild, N3 moderate). This asymmetry is attributed to reduced speech distortion being inaudible to hearing-impaired listeners at high SNRs, and suggests compression may not benefit hearing-aid applications.

## Equivalence with Noise Attenuation Control

[[sources/shetu-2026-munet|Shetu et al. 2026]] show empirically (with [[concepts/munet|μNet]] on DNS) that the compression factor $\alpha$ and the post-processing [[concepts/noise-attenuation-control|noise attenuation level]] (NAL) act as **near-equivalent controls** of the same speech-quality vs. noise-suppression trade-off: increasing $\alpha$ improves speech quality at the cost of less suppression, functionally like a higher NAL. The practical difference is that each $\alpha$ requires retraining, whereas NAL is adjustable at inference time — so they recommend training with aggressive compression (low $\alpha$) and exposing NAL as the user-facing knob.

## Compressed-Domain Phase-Aware Losses

The compression factor also appears inside the phase-aware compressed STFT loss ($c=0.3$), where compressed magnitudes are compared with and without the complex phase term. [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026]] note that the [[concepts/magnitude-phase-compensation-effect|compensation effect]] of this loss acts on the *compressed* magnitudes — the over-attenuation it induces in mid-to-high frequencies is a direct interaction between the compression and the phase-aware term, motivating their spectrally adaptive reweighting of the phase-aware contribution.

## Loss-Side Exponent (Li 2020)

A *loss-side* counterpart appears in the [[concepts/generalized-loss-function|generalized loss function]] of [[sources/li-2020-residual-noise-control|Li et al. 2020]], where the spectral exponent $\alpha \ge 1$ is applied to the spectra inside the loss (and, analytically, inside the generalized Wiener gain $M = \left(\xi^{\alpha}/(\mu + \xi^{\alpha})\right)^{1/\alpha}$) rather than to input features. The suppression direction matches feature compression: raising $\alpha$ pushes the gain toward 1, reducing both noise attenuation and speech attenuation. The quality direction differs, however — Li et al. report PESQ/SDR *declining* as $\alpha$ goes from 1 to 2 (the preserved residual noise outweighs the reduced distortion), whereas Shetu et al. report quality gains from raising the feature-compression α. Li et al. also restrict $\alpha \ge 1$ because smaller exponents cause infinite gradients during backpropagation.

## Related Concepts

- [[concepts/ulcnet|ULCNet]]
- [[concepts/munet|μNet]]
- [[concepts/noise-attenuation-control|Noise Attenuation Control]]
- [[concepts/channel-wise-feature-reorientation|Channel-Wise Feature Reorientation]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/adaptcrn|AdaptCRN]]
- [[concepts/generalized-loss-function|Generalized Loss Function]]
- [[concepts/magnitude-phase-compensation-effect|Magnitude-Phase Compensation Effect]] — interaction between compression and the phase-aware loss term

## Related Sources

- [[sources/shetu-2024-hybrid-low-complexity-aenr|Shetu et al. 2024: Hybrid Low-Complexity AENR]]
- [[sources/wang-2025-adaptive-convolution-cnn-speech-enhancement|Wang et al. 2025: Adaptive Convolution for CNN-based Speech Enhancement Models]] — AdaptCRN uses exponent 0.3 for magnitude MSE loss and 0.7 for real/imag MSE loss (i.e., real/imag parts compressed by $|S|^{0.7}$ before MSE), with $\log_{10}$ applied to compress magnitude input features in the spectral compression module. Ablation: removing dynamic-range compression costs ~0.2 dB SI-SNR and ~0.05 PESQ on AdaptCRN.
- [[sources/shetu-2026-munet|Shetu et al. 2026: μNet]] — documents the PF vs. NAL equivalence
- [[sources/li-2020-residual-noise-control|Li et al. 2020: Supervised Speech Enhancement with Residual Noise Control]] — loss-side spectral exponent α (≥1) with the opposite quality-vs-α direction
- [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026: Spectrally Adaptive Loss for Streaming Speech Enhancement]] — compressed-domain (c=0.3) phase-aware loss and its compensation-effect interaction
