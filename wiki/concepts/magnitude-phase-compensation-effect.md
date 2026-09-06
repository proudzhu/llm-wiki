---
type: concept
created: 2026-09-06
updated: 2026-09-06
sources:
  - raw/papers/zhao-2026-spectrally-adaptive-loss/full-text.md
tags:
  - speech-enhancement
  - deep-learning
  - loss-function
  - spectral-analysis
---

# Magnitude-Phase Compensation Effect

The **magnitude-phase compensation effect** is a failure mode of phase-aware training objectives in speech enhancement: when the network's phase predictions are unreliable, the phase-aware loss term is minimised by driving the estimated magnitude toward zero, producing systematic **magnitude over-attenuation**. Named and analysed by Wang, Wichern & Le Roux (IEEE SPL 2021) in the context of speech separation, and prominent in RI-MSE-style losses surveyed by Zheng et al. 2023.

## Properties

- **Spectral non-uniformity**: the over-attenuation concentrates in **mid-to-high frequency** regions (where phase estimation is hardest), degrading perceptual brightness while broadband metrics — dominated by low-frequency energy — barely register it.
- **Phase-accuracy correlation**: phase estimation accuracy correlates with spectral magnitude — high-magnitude regions yield accurate phase predictions, low-magnitude regions are error-prone. The attenuation therefore also follows signal-dependent patterns, not just frequency.
- **Scalar-weight dilemma**: in the mixed loss $\mathcal{L}_{\mathrm{Mix}}=(1-\lambda)\mathcal{L}_{\mathrm{Mag}}+\lambda\mathcal{L}_{\mathrm{Pha}}$, an insufficient $\lambda$ under-suppresses noise while an excessive $\lambda$ over-attenuates; a single scalar cannot capture the spectral variation of the effect.

## Remedies in the Literature

| Strategy | Approach | Example |
|----------|----------|---------|
| Architectural decoupling | Separate magnitude and phase decoders / residual complex branches | MP-SENet, CTSNet, G2Net (see Zheng 2023 survey) |
| Loss-side spectral weighting | Replace the scalar $\lambda$ with a frequency-wise (or signal-dependent) weight on the phase-aware term | [[concepts/spectrally-adaptive-loss|Spectrally Adaptive Loss]] (Zhao & Madhu 2026) |

The loss-side remedy is motivated directly by the effect's two properties: the frequency sigmoid targets the mid-to-high concentration, and the signal-dependent weight targets the magnitude-phase accuracy correlation.

## Related Concepts

- [[concepts/spectrally-adaptive-loss|Spectrally Adaptive Loss]] — loss-side remedy
- [[concepts/frequency-domain-loss|Frequency Domain Loss for Time-Domain Networks]] — the loss family where the effect arises
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cRM)]] — phase-aware targets inherit the effect
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026: Spectrally Adaptive Loss for Streaming Speech Enhancement]] — characterises the effect's spectral non-uniformity and proposes the loss-side remedy
- [[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng et al. 2023: Sixty Years of Frequency-Domain Monaural Speech Enhancement]] — surveys the effect in RI-MSE losses and the architectural-decoupling response
