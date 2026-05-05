---
type: source
created: 2026-04-19
updated: 2026-04-19
sources:
- https://doi.org/10.1016/j.sigpro.2015.09.015
tags:
- active-noise-control
- adaptive-filtering
- fxap-sign-algorithm
- impulsive-noise
---

# A new efficient filtered-x affine projection sign algorithm for active control of impulsive noise

**Authors**: Longshuai Xiao, Ming Wu, Jun Yang
**Journal**: Signal Processing
**Year**: 2016

## Summary
This paper introduces an efficient Filtered-x Affine Projection Sign (FxAPS) algorithm designed specifically for the active control of impulsive noise. The FxAPS algorithm addresses the convergence and robustness issues typically encountered when using standard FXLMS or FXAPS algorithms in impulsive noise environments, where the noise distribution is often non-Gaussian (e.g., alpha-stable distribution).

## Key Contributions
- **Robustness**: Utilizes the sign function within the affine projection framework to achieve robustness against impulsive disturbances.
- **Computational Efficiency**: Proposes an efficient implementation to reduce the computational complexity associated with standard affine projection algorithms.
- **Performance**: Demonstrates superior convergence speed and stability compared to conventional algorithms in the presence of heavy-tailed impulsive noise.

## Relevance
- **Context**: Useful for improving ANC systems in environments where impulsive noise (like clanks, clicks, or transient shocks) is prevalent.
- **Related Concepts**: [[concepts/active-noise-control]], [[concepts/adaptive-filtering]], [[concepts/impulsive-noise]], [[concepts/filtered-x-lms-algorithm]].

## Related Concepts

- [[concepts/active-noise-control]]
- [[concepts/adaptive-filtering]]
- [[concepts/filtered-x-lms-algorithm]]
- [[concepts/impulsive-noise]]

## Related Synthesis
