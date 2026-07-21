---
type: concept
created: 2026-07-21
updated: 2026-07-21
tags:
  - speech-intelligibility
  - perception-model
  - speech-enhancement
  - hearing-aid
---

# Glimpse Proportion

**Glimpse Proportion (GP)** is a speech-intelligibility-inspired measure that quantifies the fraction of time-frequency (T-F) tiles in which the target speech is audible above background noise. Originally proposed by Cooke (2006) as a glimpsing model of speech perception in noise, GP was adopted by Apostolidis et al. (2026) as the selection criterion for [[concepts/output-based-speech-enhancement|output-based speech enhancement]].

## Definition

For a T-F audibility map $\widehat{\mathrm{AUD}}(k,l) \in [0,1]$ over $K$ frequency bins and $L$ time frames:

$$\mathrm{GP} = \frac{1}{KL}\sum_{k=1}^{K}\sum_{l=1}^{L} U\!\left(\widehat{\mathrm{AUD}}(k,l) - \gamma_{\mathrm{GP}}\right)$$

where $U(\cdot)$ is the unit step function and $\gamma_{\mathrm{GP}}$ is a configurable threshold. GP is the proportion of T-F tiles whose estimated audibility (i.e., SNR) exceeds $\gamma_{\mathrm{GP}}$ — the "glimpses" of speech that survive masking.

## Audibility Map

The audibility map is adopted from the Speech Intelligibility Index (SII; ANSI S3.5-1997). It is computed from the T-F SNR at the reference microphone,

$$\mathrm{SNR}(k,l) = 20 \log_{10}\!\left(\frac{|\tilde{S}_\alpha(k,l)|}{|V_\alpha(k,l)|}\right) \;[\mathrm{dB}]$$

by clipping to $[-15, 15]$ dB and linearly mapping to $[0, 1]$.

In practice, $\widehat{\mathrm{AUD}}(k,l)$ is *estimated* by a neural [[concepts/voice-activity-detection|VAD]] (a [[concepts/convolutional-recurrent-network|CRN]]) run on the signal whose GP is being measured — without access to separated speech or noise. The CRN is trained with MSE against ground-truth AUD computed from clean separated components.

## Why GP for Output-based Selection

Apostolidis et al. (2026) report that in an initial comparison (omitted for space), GP consistently outperformed other SI/SQ measures estimated from beamformer outputs. GP emphasizes **speech-dominant T-F regions** rather than overall energy, making it more sensitive to whether the candidate beamformer is pointed at the true target direction. A candidate pointing away from the target produces many noise-dominated T-F tiles (low GP), while the correct candidate preserves glimpses of speech (high GP) — even at low input SNR where input-based VAD masks are unreliable.

## Properties

- **Perceptually inspired**: directly motivated by the glimpsing model of speech perception
- **Robust to noise**: emphasizes speech audibility rather than absolute level
- **Threshold-tunable**: $\gamma_{\mathrm{GP}}$ trades off false-positive glimpses against misses; tuned on validation data
- **Output-side**: computable from a candidate output without oracle knowledge of speech/noise separation

## Related Concepts

- [[concepts/output-based-speech-enhancement|Output-based Speech Enhancement]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[sources/apostolidis-2026-listen-first-output-based-multi-microphone|Apostolidis et al. 2026: Listen first — output-based multi-microphone speech enhancement]]
