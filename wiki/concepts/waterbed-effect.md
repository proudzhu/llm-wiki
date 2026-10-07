---
type: concept
created: 2026-05-20
updated: 2026-10-07
sources:
  - raw/papers/xiao-2023-spatially-selective-anc/full-text.md
  - wiki/sources/liebich-2022-occlusion-effect-cancellation.md
tags:
  - control-theory
  - feedback
  - active-noise-control
---

# Waterbed Effect

The **waterbed effect** (also known as the Bode sensitivity integral) is a fundamental limitation in feedback control systems: improving disturbance rejection (lowering the sensitivity function) in one frequency band necessarily increases the sensitivity in another band, leading to noise amplification or "boosting." In ANC systems, this constrains how much noise attenuation can be achieved without creating audible artifacts.

In [[concepts/spatially-selective-anc|spatially selective ANC]], the feedback subsystem's waterbed effect surfaces in the directivity pattern: for directions where causality is violated (noise reaches the error microphone before the reference microphones), only feedback control operates, and high frequencies are slightly **amplified** as a consequence ([[sources/xiao-2023-spatially-selective-anc|Xiao 2023]]).

In [[concepts/occlusion-effect-cancellation|occlusion effect cancellation]], the $\mathcal{H}_\infty$ feedback controller's waterbed amplification appears at 1.5–4 kHz — deliberately accepted by design and compensated in the hear-through filter $W(z)$, which accounts for the boosted band ([[sources/liebich-2022-occlusion-effect-cancellation|Liebich & Vary 2022]]).

## Related Concepts

- [[concepts/sensitivity-function|Sensitivity Function]]
- [[concepts/robust-control|Robust Control]]
- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/occlusion-effect-cancellation|Occlusion Effect Cancellation]]

## Related Sources

- [[sources/xiao-2023-spatially-selective-anc|Xiao 2023: Spatially Selective Active Noise Control Systems]]
- [[sources/liebich-2022-occlusion-effect-cancellation|Liebich & Vary 2022: Occlusion Effect Cancellation in Headphones and Hearing Devices]]
