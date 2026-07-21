---
type: concept
created: 2026-07-21
updated: 2026-07-21
tags:
  - speech-enhancement
  - beamforming
  - hearing-aid
  - speech-intelligibility
  - system-architecture
---

# Output-based Speech Enhancement

**Output-based Speech Enhancement** is a processing paradigm in which the configuration of a sound-processing system (e.g., beamformer weights, post-filter settings) is selected by evaluating speech-intelligibility / sound-quality measures computed from the system's *output*, rather than by extracting acoustic features from its noisy *input*. Introduced by Apostolidis et al. (2026) for hearing-aid multi-microphone speech enhancement.

## Motivation

Conventional hearing-aid SE pipelines are *input-based*: a [[concepts/voice-activity-detection|VAD]] operating directly on noisy microphone signals produces masks used to estimate target/noise [[concepts/spatial-covariance-matrix|spatial covariance matrices]] and the [[concepts/relative-transfer-function|RTF]], which then parameterize a [[concepts/mvdr-beamformer|MVDR]] beamformer. VAD decisions degrade precisely in challenging acoustic scenes (low SNR, reverberation, multiple interferers) — the conditions under which HA users most need support. Output-based processing sidesteps this by pushing the SI/SQ evaluation to *after* the SE stage, where speech has already been partially separated from noise.

## General Formulation

Given a set of $N$ candidate system configurations $\{\mathcal{S}_i\}_{i=1}^{N}$, each producing an output $\hat{S}_i$ from the same noisy input $\mathbf{X}$:

$$\mathcal{S}^\star = \arg\max_{\mathcal{S}_i} \; \mathrm{Metric}\!\left(\hat{S}_i\right)$$

where $\mathrm{Metric}(\cdot)$ is a perceptually inspired SI/SQ estimator (e.g., [[concepts/glimpse-proportion|Glimpse Proportion]]) evaluated on each candidate's output.

## Instantiation: Output-based MPDR Beamforming

Apostolidis et al. (2026) instantiate the paradigm with a dictionary of $N$ candidate [[concepts/mpdr-beamformer|MPDR beamformers]], each constructed with a candidate [[concepts/relative-transfer-function|RTF]] $\mathbf{d}_{\theta_i}(k)$ from a pre-enrolled dictionary $\mathbf{d}_\theta(k) = \{\mathbf{d}_{\theta_1}, \ldots, \mathbf{d}_{\theta_N}\}$:

$$\mathbf{W}_{\text{MPDR}}^{(i)}(k,l) = \frac{\mathbf{C}_{\mathbf{X}}^{-1}(k,l)\,\mathbf{d}_{\theta_i}(k)}{\mathbf{d}_{\theta_i}^{H}(k)\,\mathbf{C}_{\mathbf{X}}^{-1}(k,l)\,\mathbf{d}_{\theta_i}(k)}$$

MPDR is a natural fit because it uses the noisy covariance $\mathbf{C}_{\mathbf{X}}$ directly — no VAD-based noise statistics are required to *construct* any candidate. The candidate whose output maximizes [[concepts/glimpse-proportion|GP]] (estimated by a neural VAD run on the output) is selected per segment.

## Why MPDR Becomes Usable

[[concepts/mpdr-beamformer|MPDR]] is typically avoided in practice because steering-vector (RTF) mismatch causes target cancellation: the beamformer treats the true target as interference and suppresses it. Inside the output-based wrapper, however, the system *searches* over a discrete set of steering directions rather than committing to a single (potentially mismatched) one, and the GP-based selector reliably identifies the correct candidate. Apostolidis et al. show that the proposed system still significantly outperforms an input-based [[concepts/mvdr-beamformer|MVDR]] baseline even under coarse (15° spaced) or non-individualized (HATS-measured) RTF dictionaries.

## Relation to Prior Output-driven Work

Earlier output-driven mechanisms modified individual components:
- Rascon (2025): output-based SQ estimates for DOA correction
- Kienegger et al. (2025): enhanced outputs for target tracking
- Hafezi et al. (2023): subspace hybrid MVDR for augmented hearing

The output-based paradigm of Apostolidis et al. is more general: it selects among *any* candidate SE system configurations, not just one component.

## Related Concepts

- [[concepts/glimpse-proportion|Glimpse Proportion]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]
- [[concepts/relative-transfer-function|Relative Transfer Function]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/beamforming|Beamforming]]

## Related Sources

- [[sources/apostolidis-2026-listen-first-output-based-multi-microphone|Apostolidis et al. 2026: Listen first — output-based multi-microphone speech enhancement]]
