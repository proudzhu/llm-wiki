---
type: concept
created: 2026-09-06
updated: 2026-09-06
sources:
  - raw/papers/zhao-2026-spectrally-adaptive-loss/full-text.md
  - raw/papers/wang-2021-magnitude-phase-compensation/full-text.md
tags:
  - speech-enhancement
  - deep-learning
  - loss-function
  - spectral-analysis
---

# Magnitude-Phase Compensation Effect

The **magnitude-phase compensation effect** is a failure mode of phase-aware training objectives in speech enhancement: when the network's phase predictions are unreliable, the phase-aware loss term is minimised by driving the estimated magnitude toward zero, producing systematic **magnitude over-attenuation**. Named and analysed by Wang, Wichern & Le Roux (IEEE SPL 2021) in the context of speech separation, and prominent in RI-MSE-style losses surveyed by Zheng et al. 2023.

## Formulation (Wang 2021)

At each T-F unit, a loss defined only in the complex or time domain drives the estimate $\hat{S}(t,f)$ toward the clean $S(t,f)$. Because phase is hard to estimate, $\angle\hat{S}(t,f)$ differs from $\angle S(t,f)$ (especially at low SNR), and the closest approximation of $S(t,f)$ *along the estimated-phase direction* is the projection $|S(t,f)|\cos(\angle S-\angle\hat{S})$ — a magnitude that is **compensated** for the phase error rather than accurate. The magnitude error grows with the phase error, and beyond a $\pi/2$ phase error the optimal projection magnitude is **zero** (full over-attenuation).

The effect explains a widely observed asymmetry in evaluation metrics:

- [[concepts/pesq|PESQ]] (segment-wise time alignment, then Bark-scale spectra) and eSTOI (magnitude envelope) favour an accurate magnitude — they improve when a magnitude loss is added.
- SI-SDR measures sample-level time-domain error — it *favours* a compensated magnitude and therefore degrades slightly when a magnitude loss is added.

[[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021]] verify the decomposition with [[concepts/magnitude-phase-snr|mSNR/pSNR]]: adding a magnitude loss to an RI loss improves mSNR (12.66 → 12.84 dB) while *degrading* pSNR (10.8 → 10.35 dB) on WHAMR!; direct magnitude estimation (MSA) reaches the best learned mSNR (13.05 dB without re-synthesis) because its teacher-forced formulation (target phase assumed) avoids compensation entirely. The view generalises the [[concepts/phase-sensitive-mask|phase-sensitive mask]], which *explicitly* computes the compensated magnitude along the mixture phase.

![[raw/papers/wang-2021-magnitude-phase-compensation/figures/fig1.png|2D histograms of phase difference vs. magnitude ratio for MSA, RI, RI+Mag, Wav, Wav+Mag]]

*Figure: 2D histograms (WHAMR! test mixture) of phase difference $\cos(\angle S-\angle Y)$ vs. magnitude ratio $\hat{M}/|S|$. RI (and Wav) compress magnitudes toward zero where the phases differ; MSA stays near the perfect-estimation line; RI+Mag partially recovers.*

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
- [[concepts/phase-sensitive-mask|Phase-Sensitive Mask (PSM)]] — the mask that explicitly encodes the compensation
- [[concepts/magnitude-phase-snr|mSNR and pSNR]] — diagnostic metrics isolating magnitude vs. phase accuracy
- [[concepts/complex-spectral-mapping|Complex Spectral Mapping]] — the paradigm where the effect was first named
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021: On the Compensation Between Magnitude and Phase in Speech Separation]] — the primary source: names and formulates the effect, validates it with mSNR/pSNR decomposition
- [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026: Spectrally Adaptive Loss for Streaming Speech Enhancement]] — characterises the effect's spectral non-uniformity and proposes the loss-side remedy
- [[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng et al. 2023: Sixty Years of Frequency-Domain Monaural Speech Enhancement]] — surveys the effect in RI-MSE losses and the architectural-decoupling response
