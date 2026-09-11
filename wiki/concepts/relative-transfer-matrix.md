---
type: concept
created: 2026-09-11
updated: 2026-09-11
sources:
  - raw/papers/zhang-2026-feedback-path-mitigation-mcanc/full-text.md
tags:
  - spatial-filtering
  - acoustic-modeling
  - transfer-function
  - active-noise-control
  - microphone-arrays
---

# Relative Transfer Matrix (ReTM)

The **Relative Transfer Matrix (ReTM)** generalizes the [[concepts/relative-transfer-function|Relative Transfer Function (RTF)]] from a single source to an arbitrary number of sources, and from a single reference microphone to a whole **group** of reference microphones. Where the RTF is a vector $\mathbf{a}(k,\theta) \in \mathbb{C}^{M}$ describing one source's propagation across $M$ microphones relative to one reference channel, the ReTM is a **matrix** $\mathbf{R} \in \mathbb{C}^{J_{\mathrm{R}} \times J_{\mathrm{F}}}$ describing the linear spatial mapping between two microphone *groups*.

## Definition

Given a reference microphone group $\mathbf{M}_{\mathrm{R}} \in \mathbb{C}^{J_{\mathrm{R}}}$ and a second (auxiliary) microphone group $\mathbf{M}_{\mathrm{F}} \in \mathbb{C}^{J_{\mathrm{F}}}$, the ReTM is defined by

$$
\mathbf{M}_{\mathrm{R}} = \mathbf{R}_{\mathrm{RF}}\, \mathbf{M}_{\mathrm{F}}.
$$

Unlike the RTF, the ReTM is **not normalized** to unity at a reference channel, and it does not assume a single dominant source: the mapping is exact whenever both groups observe the same source set.

## Secondary-Field ReTM in Multichannel ANC

In the ANC feedback-mitigation formulation of [[sources/zhang-2026-feedback-path-mitigation-mcanc|Zhang et al. 2026]], the auxiliary group is a dedicated **feedback microphone group** placed to observe secondary-loudspeaker leakage. Restricting attention to the **secondary-loudspeaker-only** field, with $\mathbf{F}_{\mathrm{R}} = \mathbf{S}_{\mathrm{ref}}\mathbf{y}$ and $\mathbf{F}_{\mathrm{F}} = \mathbf{S}_{\mathrm{fb}}\mathbf{y}$ for the reference-group and feedback-group secondary paths $\mathbf{S}_{\mathrm{ref}} \in \mathbb{C}^{J_{\mathrm{R}} \times L}$ and $\mathbf{S}_{\mathrm{fb}} \in \mathbb{C}^{J_{\mathrm{F}} \times L}$ ($L$ loudspeakers), the secondary-field ReTM is

$$
\mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})} \triangleq \mathbf{S}_{\mathrm{ref}}\, \mathbf{S}_{\mathrm{fb}}^{\dagger},
$$

with $(\cdot)^{\dagger}$ the pseudo-inverse. Two structural properties follow, and they are the reason the construction is attractive:

1. **Signal independence.** $\mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})}$ is a function of the acoustic transfer structure $(\mathbf{S}_{\mathrm{ref}}, \mathbf{S}_{\mathrm{fb}})$ only. It does **not** depend on the emitted loudspeaker signal $\mathbf{y}$, nor on the primary-noise signal or its statistics.
2. **Path-count compression.** One $J_{\mathrm{R}} \times J_{\mathrm{F}}$ matrix replaces the $J_{\mathrm{R}} \times L$ individual loudspeaker-to-reference-microphone feedback paths that conventional [[concepts/online-feedback-path-modeling|FBPM]] would have to identify separately.

Property 1 is what makes a ReTM identified once usable across changes in primary source location and primary noise signal; property 2 is what makes the approach scale to multichannel arrays.

## Estimation from Second-Order Statistics

The ReTM is estimated from [[concepts/spatial-covariance-matrix|spatial covariance matrices]] rather than from direct path measurements:

$$
\mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})} \approx \boldsymbol{\Phi}_{\mathrm{RR}}^{(\mathrm{Sec})}\, \boldsymbol{\Phi}_{\mathrm{FR}}^{(\mathrm{Sec})^{\dagger}}, \qquad
\boldsymbol{\Phi}_{\mathrm{RR}}^{(\mathrm{Sec})} = \mathbb{E}\{\mathbf{M}_{\mathrm{R}}^{(\mathrm{Sec})}\mathbf{M}_{\mathrm{R}}^{(\mathrm{Sec})^H}\}, \quad
\boldsymbol{\Phi}_{\mathrm{FR}}^{(\mathrm{Sec})} = \mathbb{E}\{\mathbf{M}_{\mathrm{F}}^{(\mathrm{Sec})}\mathbf{M}_{\mathrm{R}}^{(\mathrm{Sec})^H}\},
$$

with the expectation approximated by time-frame averaging.

In the ancestor RTF literature the corresponding estimator is **covariance whitening** (noise covariance borrowed from noise-only frames, then the dominant eigenvector of the whitened target covariance). The ReTM counterpart cannot borrow a silence-only noise segment in the ANC setting, because the "noise" here *is* the persistent primary field — which is why the ReTM estimator is built on **[[concepts/covariance-subtraction|covariance subtraction]]** instead.

## Use for Feedback Subtraction

Once identified, the ReTM is applied as a direct subtraction on the reference signal before the adaptive controller:

$$
\mathbf{M}_{\mathrm{R}}^{(\mathrm{filt})} = \mathbf{M}_{\mathrm{R}} - \mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})}\mathbf{M}_{\mathrm{F}}
\approx \mathbf{P}_{\mathrm{R}} - \mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})}\mathbf{P}_{\mathrm{F}}.
$$

The loudspeaker-leakage term cancels because $\mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})}\mathbf{S}_{\mathrm{fb}}\mathbf{y} \approx \mathbf{S}_{\mathrm{ref}}\mathbf{y}$ by construction. Note what the operation does *not* do: it does not recover the clean primary reference $\mathbf{P}_{\mathrm{R}}$, but the modified combination $\mathbf{P}_{\mathrm{R}} - \mathbf{R}_{\mathrm{RF}}^{(\mathrm{Sec})}\mathbf{P}_{\mathrm{F}}$ — i.e. it reshapes the effective primary path seen by the controller as a side effect of removing the feedback.

## Relation to Other Relative-Transfer Constructions

| Construction | Dimension | Sources | Normalized? | Typical use |
|---|---|---|---|---|
| [[concepts/relative-transfer-function\|RTF]] $\mathbf{a}(k,\theta)$ | vector $\mathbb{C}^M$ | one | yes (reference channel = 1) | beamforming, GSC blocking matrix, dictionary-based beamformer selection |
| **ReTM** $\mathbf{R}_{\mathrm{RF}}$ | matrix $\mathbb{C}^{J_{\mathrm{R}} \times J_{\mathrm{F}}}$ | many | no | group-to-group spatial mapping; ANC feedback subtraction |
| Relative impulse response (ReIR) | filters (time domain) | one per desired direction | design-time quantity | [[concepts/spatially-selective-anc\|spatially selective ANC]] constraints |

## Related Concepts

- [[concepts/relative-transfer-function|Relative Transfer Function (RTF)]] — the single-source, single-reference ancestor
- [[concepts/covariance-subtraction|Covariance Subtraction]] — the estimator that isolates the secondary-only covariances
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]] — the statistic the ReTM is estimated from
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the phenomenon the ReTM is used to mitigate
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/multi-channel-anc|Multi-Channel ANC]]
- [[concepts/spatially-selective-anc|Spatially Selective ANC]]

## Related Sources

- [[sources/zhang-2026-feedback-path-mitigation-mcanc|Zhang, Abhayapala, Samarasinghe & Bastine 2026: Acoustic Feedback Path Mitigation for Multichannel ANC]] — uses the secondary-field ReTM with covariance subtraction to neutralize loudspeaker leakage ahead of a multichannel FxLMS controller, without silencing the primary noise
