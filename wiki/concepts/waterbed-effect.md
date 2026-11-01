---
type: concept
created: 2026-05-20
updated: 2026-11-01
sources:
  - raw/papers/xiao-2023-spatially-selective-anc/full-text.md
  - wiki/sources/liebich-2022-occlusion-effect-cancellation.md
  - raw/papers/klatt-2025-laguerre-feedback-anc/full-text.md
tags:
  - control-theory
  - feedback
  - active-noise-control
---

# Waterbed Effect

The **waterbed effect** (also known as the Bode sensitivity integral) is a fundamental limitation in feedback control systems: improving disturbance rejection (lowering the sensitivity function) in one frequency band necessarily increases the sensitivity in another band, leading to noise amplification or "boosting." In ANC systems, this constrains how much noise attenuation can be achieved without creating audible artifacts.

In [[concepts/spatially-selective-anc|spatially selective ANC]], the feedback subsystem's waterbed effect surfaces in the directivity pattern: for directions where causality is violated (noise reaches the error microphone before the reference microphones), only feedback control operates, and high frequencies are slightly **amplified** as a consequence ([[sources/xiao-2023-spatially-selective-anc|Xiao 2023]]).

In [[concepts/occlusion-effect-cancellation|occlusion effect cancellation]], the $\mathcal{H}_\infty$ feedback controller's waterbed amplification appears at 1.5–4 kHz — deliberately accepted by design and compensated in the hear-through filter $W(z)$, which accounts for the boosted band ([[sources/liebich-2022-occlusion-effect-cancellation|Liebich & Vary 2022]]).

In constrained IMC filter design, the waterbed effect is bounded explicitly rather than accepted: a performance weight $W_S$ caps the maximum amplification, appearing as the constraint $|[1 - Q\widehat{G}]W_S|^2 < 1$. [[sources/klatt-2025-laguerre-feedback-anc|Klatt & Martin 2025]] set $W_S = 0.625$ (a 4 dB amplification ceiling) and report that the resulting Laguerre-based controller keeps amplification below the bound everywhere, while its non-nominal behavior differs from FIR designs in where the boosting lands: slightly more at 1–2 kHz, but none above 10 kHz and no 3.6 kHz peak (the ear-canal resonance region).

## Related Concepts

- [[concepts/sensitivity-function|Sensitivity Function]]
- [[concepts/robust-control|Robust Control]]
- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/occlusion-effect-cancellation|Occlusion Effect Cancellation]]

## Related Sources

- [[sources/xiao-2023-spatially-selective-anc|Xiao 2023: Spatially Selective Active Noise Control Systems]]
- [[sources/liebich-2022-occlusion-effect-cancellation|Liebich & Vary 2022: Occlusion Effect Cancellation in Headphones and Hearing Devices]]
- [[sources/klatt-2025-laguerre-feedback-anc|Klatt & Martin 2025: Laguerre Filter-based Robust Feedback Active Noise Control]] — $W_S$-bounded amplification (4 dB ceiling) in the convex IMC program
