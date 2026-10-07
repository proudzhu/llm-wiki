---
type: concept
created: 2026-05-20
updated: 2026-10-07
sources:
  - wiki/sources/liebich-2022-occlusion-effect-cancellation.md
tags:
  - control-theory
  - robust-control
---

# Robust Control

**Robust control** is a branch of control theory that explicitly deals with uncertainty in the design of controllers. In the context of active noise control, robust control methods ensure that the noise reduction performance remains stable even when the acoustic plant (secondary path) deviates from the nominal model.

Key concepts include:
- **Sensitivity function** $S$ — characterizes disturbance rejection
- **Complementary sensitivity function** $T = 1 - S$ — characterizes noise amplification and robustness
- **Waterbed effect** — improvement in attenuation at one frequency band comes at the cost of amplification (boosting) at another
- **Mixed-sensitivity $\mathcal{H}_\infty$ synthesis** — designing $K(z)$ against secondary-path uncertainty margins so stability holds for all plants covered by the uncertainty set; used for both ANC feedback controllers and the occlusion-effect-cancellation controller of Liebich & Vary 2022, whose $K(z)$ remains fixed while an adaptive factor $\alpha$ scales the loop gain for individual ears

## Related Concepts

- [[concepts/sensitivity-function|Sensitivity Function]]
- [[concepts/waterbed-effect|Waterbed Effect]]
- [[concepts/q-parameterization|Q-Parameterization]]
- [[concepts/uncertainty-modeling-for-anc|Uncertainty Modeling for ANC]]
- [[concepts/spatially-selective-anc|Spatially Selective ANC]]
- [[concepts/soft-constrained-anc|Soft-Constrained ANC]]

## Related Sources

- [[sources/hilgemann-2024-data-driven-uncertainty-anc|Hilgemann 2024: Data-Driven Uncertainty Modeling for Robust Feedback ANC]]
- [[sources/xiao-2026-robust-spatially-selective-anc|Xiao 2026: Robust Soft-Constrained SSANC for Hearables]]
- [[sources/liebich-2022-occlusion-effect-cancellation|Liebich & Vary 2022: Occlusion Effect Cancellation in Headphones and Hearing Devices]]
