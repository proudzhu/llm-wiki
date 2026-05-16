---
type: concept
created: 2026-05-20
updated: 2026-05-20
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

## Related Concepts

- [[concepts/sensitivity-function|Sensitivity Function]]
- [[concepts/waterbed-effect|Waterbed Effect]]
- [[concepts/q-parameterization|Q-Parameterization]]
