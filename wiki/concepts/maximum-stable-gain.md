---
type: concept
created: 2026-05-15
updated: 2026-08-20
sources:
  - raw/papers/vanwaterschoot-2011-fifty-years-afc/full-text.md
  - raw/papers/schepker-2016-sdp-minmax-acoustic-feedback/full-text.md
  - raw/papers/zhan-2025-deeppem-afc/full-text.txt
  - raw/papers/lydaki-2026-deep-feedback-cancellation-hearing-aids/full-text.md
  - raw/papers/mounir-2025-robust-early-howling-detection-sparsity/full-text.md
tags:
  - hearing-aids
  - feedback-cancellation
  - stability
---

# Maximum Stable Gain

**Maximum Stable Gain (MSG)** is the maximum amplification gain a hearing aid can provide before the acoustic feedback loop becomes unstable and produces howling.

## Definition

The MSG is determined by the acoustic feedback path transfer function F(k):

```
MSG = -20 · log₁₀(max_k |F(k)|)
```

### General PA-System Definition

For a single-channel sound-reinforcement system with forward path $G(q,t) = K(t)J(q,t)$ (broadband gain $K(t)$ extracted from $G$), the MSG is defined as the largest $K(t)$ such that the loop gain just reaches unity at a frequency satisfying the Nyquist phase condition (van Waterschoot & Moonen 2011):

$$\mathrm{MSG}(t)\,[\mathrm{dB}] = -20\log_{10}\!\left[\max_{\omega \in \mathcal{P}} |J(\omega,t)F(\omega,t)|\right]$$

with $\mathcal{P} = \{\omega \mid \angle G(\omega,t)F(\omega,t) = n \cdot 2\pi\}$. A **gain margin of 2–3 dB** below the MSG is recommended to avoid audible ringing.

### Schroeder's Statistical Bound

From statistical room acoustics, assuming a flat forward path and unity average feedback-path magnitude, the expected MSG for a room with reverberation time $T_{60}$ and bandwidth $B$ is:

$$\mathrm{MSG}\,[\mathrm{dB}] = -10\log_{10}[\log_{10}(BT_{60}/22)] - 3.8$$

The peak-to-average magnitude ratio of a room response is ~10 dB, which sets a **theoretical upper bound** on the MSG increase achievable by loop-gain-smoothing methods ([[concepts/phase-modulating-feedback-control|PFC]], [[concepts/notch-filter-based-howling-suppression|NHS]], automatic equalization). Room-modeling methods ([[concepts/adaptive-feedback-cancellation|AFC]]) are not bound by this limit because they remove the coupling rather than smooth it.

## Importance

- Limits the effectiveness of hearing aids for severe/profound hearing loss
- Higher MSG allows greater amplification without howling
- AFC methods aim to increase the effective MSG by estimating and canceling the feedback path

## Added Stable Gain (ASG)

**ASG** measures the improvement in stability provided by an AFC method:

```
ASG(l) = -20 · log₁₀(max_k |F(k,l) - F̂(k,l)| / |F(k,l)|)
```

where F̂(k,l) is the estimated feedback path.

## Tracking Time

**Tracking time** is defined as the time required for the average ASG to exceed the MSG by 3 dB following a feedback path change. This metric is critical for evaluating AFC performance in real-world scenarios where the feedback path changes (e.g., hat on/off, phone near ear).

## Direct MSG Maximization via Min-max Optimization

While most AFC methods aim to minimize the misalignment (filter estimation error) as a proxy for increasing MSG, [[entities/henning-schepker|Schepker]] & [[entities/simon-doclo|Doclo]] (2016) proposed directly maximizing the MSG by formulating the common part estimation as a [[concepts/min-max-common-part-estimation|min-max optimization problem solved via semidefinite programming]]. This approach minimizes the worst-case output-error across all frequencies and paths (rather than the sum of squared errors), yielding 2–5 dB MSG improvement over least-squares optimization. The trade-off is a 1–4 dB increase in misalignment — acceptable since MSG directly determines the applicable hearing aid gain, while misalignment does not.

## Related Concepts

- [[concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]]
- [[concepts/acoustic-feedback|Acoustic Feedback]]
- [[concepts/adaptive-feedback-control|Adaptive Feedback Control]]
- [[concepts/adaptive-feedback-cancellation|Adaptive Feedback Cancellation (AFC)]] — not bound by Schroeder's smoothing bound
- [[concepts/phase-modulating-feedback-control|Phase-Modulating Feedback Control (PFC)]] — bounded by Schroeder's ~10 dB smoothing limit
- [[concepts/notch-filter-based-howling-suppression|Notch-Filter-Based Howling Suppression (NHS)]] — bounded by the same smoothing limit

## Related Sources

- [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] — the general PA-system MSG definition, the Nyquist-criterion derivation, Schroeder's statistical bound, and the 2–3 dB gain-margin recommendation
- [[sources/lydaki-2026-deep-feedback-cancellation-hearing-aids|Lydaki 2026: Deep Feedback Cancellation]] — DFC achieves ~23 dB MSG for speech, ~21.5 dB for music
- [[sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]] — ASG and tracking time evaluation
- [[sources/mounir-2025-robust-early-howling-detection-sparsity|Mounir, Bernardi & van Waterschoot 2025]] — uses MSG to normalize feedback paths and define the time-varying gain profile (MSG−6 dB → MSG) that triggers howling onset in the HD dataset; the howling frequency is predicted from the Nyquist criterion at $G=\mathrm{MSG}$
- [[sources/schepker-2016-sdp-minmax-acoustic-feedback|Schepker & Doclo 2016]] — directly maximizes MSG via min-max SDP optimization of common part, yielding 2–5 dB improvement over least-squares
