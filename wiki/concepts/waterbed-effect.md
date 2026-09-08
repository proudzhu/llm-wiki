---
type: concept
created: 2026-05-20
updated: 2026-09-08
sources:
  - raw/papers/xiao-2023-spatially-selective-anc/full-text.md
tags:
  - control-theory
  - feedback
  - active-noise-control
---

# Waterbed Effect

The **waterbed effect** (also known as the Bode sensitivity integral) is a fundamental limitation in feedback control systems: improving disturbance rejection (lowering the sensitivity function) in one frequency band necessarily increases the sensitivity in another band, leading to noise amplification or "boosting." In ANC systems, this constrains how much noise attenuation can be achieved without creating audible artifacts.

In [[concepts/spatially-selective-anc|spatially selective ANC]], the feedback subsystem's waterbed effect surfaces in the directivity pattern: for directions where causality is violated (noise reaches the error microphone before the reference microphones), only feedback control operates, and high frequencies are slightly **amplified** as a consequence ([[sources/xiao-2023-spatially-selective-anc|Xiao 2023]]).

## Related Concepts

- [[concepts/sensitivity-function|Sensitivity Function]]
- [[concepts/robust-control|Robust Control]]
- [[concepts/feedback-anc|Feedback ANC]]

## Related Sources

- [[sources/xiao-2023-spatially-selective-anc|Xiao 2023: Spatially Selective Active Noise Control Systems]]
