---
type: concept
created: 2026-09-07
updated: 2026-09-07
sources:
  - raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/full-text.md
tags:
  - active-noise-control
  - speech-enhancement
  - wiener-filter
  - hearing-aids
  - multi-channel
---

# Filtered-x MWF (FxMWF)

The **Filtered-x Multichannel Wiener Filter (FxMWF)** integrates noise reduction (NR) and active noise control (ANC) into a *single* set of adaptive filters, for hearing aids with an open fitting. Introduced by [[entities/romain-serizel|Serizel]] et al. (2010), it applies the filtered-x principle of ANC to the [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]: each microphone signal is pre-filtered by an estimate of the [[concepts/secondary-path-modeling|secondary path]] $\hat{S}$ (loudspeaker → tympanic membrane), and the MSE criterion is defined on the signal reaching the tympanic membrane rather than the loudspeaker input.

## Key Formulations

With filtered references $\hat{\mathbf{y}}(k)$ (each channel of $\mathbf{y}(k)$ convolved with $\hat{S}$), the MSE criterion minimized by the FxMWF is

$$J = \mathbb{E}\left[|\tilde{d}(k) - \mathbf{w}^\mathsf{T}\hat{\mathbf{y}}(k)|^2\right]$$

where $\tilde{d}$ is the desired signal at the tympanic membrane (amplified enhanced speech plus the leakage speech component). Assuming speech and noise uncorrelated, the criterion decomposes into:

1. a **secondary-path compensation** term on the speech component of the output, and
2. an **ANC** term specifying the noise sound pressure at the tympanic membrane (canceling the [[concepts/open-fitting-noise-leakage|noise leakage]]).

The optimal filter is the Wiener solution on the filtered references:

$$\mathbf{w}_{\text{FxMWF}} = \mathbf{R}_{\hat{y}\hat{y}}^{-1}\,\mathbf{r}_{\hat{y}d}$$

with speech statistics estimated during speech-plus-noise periods and noise statistics during noise-only periods — the same second-order-statistics estimation cycle as the standard MWF.

### Filter Decomposition and Causality Decoupling

Under the speech–noise uncorrelatedness assumption, the FxMWF splits into

$$\mathbf{w} = \mathbf{w}^{\parallel} + \mathbf{w}^{\perp}$$

where $\mathbf{w}^{\parallel}$ is an NR filter that also compensates the secondary path, and $\mathbf{w}^{\perp}$ is an ANC filter canceling the leakage noise. Because the ANC part does not depend on the NR algorithmic delay $\Delta$, there is **no performance trade-off between NR and ANC** — unlike cascaded NR+ANC schemes, where the NR delay consumes the ANC causality margin. The only requirement is that the overall system remain causal.

## Relation to FxLMS

Both algorithms filter the reference through $\hat{S}$ to account for the secondary path, but:

| Aspect | [[concepts/filtered-x-lms-algorithm|FxLMS]] | FxMWF |
|--------|-------|-------|
| Adaptation | Stochastic gradient, sample-by-sample | Closed form from estimated second-order statistics |
| Update periods | Noise-only (in the hearing-aid NR+ANC setting) | Both noise-only and speech-plus-noise periods |
| Function | Pure ANC (cancel noise) | Joint NR + secondary-path compensation + ANC |
| Motivation for statistics-based solution | — | Gradient estimation is inconvenient when the filter must adapt during speech-plus-noise periods too |

## Performance

On manikin acoustic-path measurements (two-microphone BTE hearing aid, speech at 0°, multitalker babble at 270°, 16 kHz), the FxMWF achieves an almost constant intelligibility-weighted SNR improvement of ~12 dB across hearing-aid gains from 0–20 dB — versus ~4 dB for a cascaded multichannel ANC + NR scheme at a relaxed degree of causality ($\nu = 48$), and >10 dB vs. ~1 dB for the cascade at the realistic hearing-aid margin ($\nu = 2$ samples). In the non-causal regime ($\nu = -16$), an FxMWF variant *without* the ANC branch achieves similar performance, showing that the surviving benefit there comes from the secondary-path compensation alone.

![[raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/figures/crop-p06-005.png|Integrated multichannel active noise control and noise reduction system]]

*Figure 5 from Serizel et al. 2010: the integrated scheme — a single filter set on secondary-path-filtered references performs NR and ANC jointly.*

## Limitations

- Requires an ear-canal error microphone (not present in commercial hearing aids).
- Assumes small secondary-path identification error and slowly-adapting filters in the derivations.
- The ANC benefit vanishes once the overall system is non-causal.

## Related Concepts

- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/open-fitting-noise-leakage|Open-Fitting Noise Leakage]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/causality|Causality in ANC]]
- [[concepts/multi-channel-anc|Multi-Channel ANC]]
- [[concepts/feedforward-anc|Feedforward ANC]]

## Related Sources

- [[sources/serizel-2010-integrated-anc-nr-hearing-aids|Serizel, Moonen, Wouters & Jensen 2010: Integrated Active Noise Control and Noise Reduction in Hearing Aids]]
