---
type: concept
created: 2026-09-11
updated: 2026-09-11
sources:
  - raw/papers/zhang-2026-feedback-path-mitigation-mcanc/full-text.md
tags:
  - spatial-statistics
  - system-identification
  - acoustic-feedback
  - active-noise-control
---

# Covariance Subtraction

**Covariance subtraction** is a two-stage identification principle that isolates the contribution of one source component from second-order statistics measured in the presence of an *uncontrollable* interfering component. It is the mechanism that lets [[concepts/relative-transfer-matrix|Relative Transfer Matrix (ReTM)]] estimation proceed when the primary noise cannot be switched off — the practical blocker for conventional offline [[concepts/online-feedback-path-modeling|feedback-path modeling]] in ANC.

## Principle: Covariance Additivity

For a set of **mutually independent** zero-mean components $s_1, \dots, s_N$, the covariance of their sum is the sum of their covariances:

$$
\boldsymbol{\Phi}_{\text{total}} = \mathbb{E}\left\{\left(\sum_i s_i\right)\left(\sum_j s_j\right)^H\right\} = \sum_i \mathbb{E}\{s_i s_i^H\} = \sum_i \boldsymbol{\Phi}_i ,
$$

because all cross terms $\mathbb{E}\{s_i s_j^H\} = 0$ for $i \neq j$. The same holds for the cross-covariance between two signal vectors.

This is the same additivity of second-order statistics that underlies the decomposition of a [[concepts/spatial-covariance-matrix|spatial covariance matrix]] into target-plus-noise contributions in multichannel speech enhancement — the difference is that here the additivity is used **constructively, as a subtraction operator** rather than as a modelling assumption.

## Two-Stage Measurement Protocol

The interfering contribution is measured once and then removed by subtraction, using two stages that both contain the interference:

| Stage | Secondary loudspeakers | Primary noise | Statistics obtained |
|---|---|---|---|
| **1 — Primary-only** | disabled | **present** | $\boldsymbol{\Phi}^{(\mathrm{Pri})} = \sum_j \boldsymbol{\Phi}^{(j)}$ |
| **2 — Total** | emitting (independent probes) | **present** | $\boldsymbol{\Phi}^{(\mathrm{Tot})} = \sum_j \boldsymbol{\Phi}^{(j)} + \sum_l \boldsymbol{\Phi}^{(l)}$ |

The secondary-only contribution then follows exactly:

$$
\boldsymbol{\Phi}^{(\mathrm{Sec})} = \boldsymbol{\Phi}^{(\mathrm{Tot})} - \boldsymbol{\Phi}^{(\mathrm{Pri})} = \sum_{l} \boldsymbol{\Phi}^{(l)} .
$$

Crucially, **the primary noise never has to be silenced** — it is present in both stages and cancels in the difference. This is what distinguishes the method from the classical ANC offline-identification recipe of probing the secondary source with the controller frozen while the primary noise is off.

## Why It Matters for Feedback Identification

Naively estimating a feedback or ReTM mapping from total-field covariances is catastrophic rather than merely suboptimal: the pseudo-inverse is dominated by the (typically much stronger) persistent primary field, so the estimate is heavily biased toward the interference subspace. Empirically, in the multichannel ANC setting of [[sources/zhang-2026-feedback-path-mitigation-mcanc|Zhang et al. 2026]], the un-subtracted "Total-ReTM" variant collapses to ≈ −1 to −2 dB of noise reduction (essentially no control), whereas the covariance-subtracted estimator lands within 0.4–2.8 dB of an oracle that measured the secondary-only field directly. Covariance subtraction is therefore a prerequisite for identification under persistent noise, not a refinement.

## Assumptions and Failure Modes

- **Independence.** Cross terms must vanish: the probing signal must be uncorrelated with the primary noise, and the probing signals for different secondary sources must be mutually independent.
- **Wide-sense stationarity over the averaging window.** The expectation is approximated by frame averaging; if the primary field changes between or within the stages, the two covariance estimates no longer share an identical interference term and the subtraction leaves a residual bias.
- **Numerical cancellation.** Differencing two statistics dominated by a large common term loses precision and amplifies estimation noise; the conditioning of the resulting $\boldsymbol{\Phi}^{(\mathrm{Sec})}$ depends on how much energy the secondary probes actually deliver to the microphone groups relative to the primary field. A stronger probe (or longer averaging) improves conditioning but costs more disturbance.
- **Not a bias-free estimator in general.** Only the *interference* term cancels; residual measurement noise, quantization, or any component that is not independent of the probes remains.

## Related Concepts

- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]] — the statistic operated on
- [[concepts/relative-transfer-matrix|Relative Transfer Matrix (ReTM)]] — the quantity estimated by covariance subtraction in the ANC case
- [[concepts/relative-transfer-function|Relative Transfer Function (RTF)]] — whose estimator uses covariance *whitening* rather than subtraction, since a noise-only segment is available
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the target phenomenon
- [[concepts/offline-secondary-path-modeling|Offline Secondary-Path Modeling]] — the classical alternative that requires an ANC-idle (noise-free) training window
- [[concepts/online-feedback-path-modeling|Online Feedback-Path Modeling]] — the adaptive alternative that injects auxiliary noise instead of differencing covariances
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/active-noise-control|Active Noise Control]]

## Related Sources

- [[sources/zhang-2026-feedback-path-mitigation-mcanc|Zhang, Abhayapala, Samarasinghe & Bastine 2026: Acoustic Feedback Path Mitigation for Multichannel ANC]] — applies covariance subtraction to the secondary-field ReTM, enabling multichannel feedback neutralization under ongoing primary noise
