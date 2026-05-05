---
type: concept
created: 2026-04-19
updated: 2026-04-19
tags:
- active-noise-control
- convex-optimization
- optimization
- personal-sound-zones
sources: []
---
# SOCP Optimization

Second-Order Cone Programming (SOCP) is a class of convex optimization problems that generalize linear and quadratic programming.

## Role in Sound Control
In Personal Sound Zone (PSZ) and Active Noise Control (ANC) systems, SOCP is used to solve robust optimization problems where performance objectives (like sound pressure matching or acoustic contrast) are subject to uncertainty constraints (e.g., norm-bounded transfer function perturbations).

## Advantages
- **Tractability**: Reformulates inherently non-convex "worst-case" design problems into convex forms that guarantee globally optimal solutions.
- **Efficiency**: Allows for real-time computational performance on DSP/embedded hardware compared to iterative biconvex solvers.
- **Robustness**: Provides a framework to explicitly include uncertainty ellipsoids in the control design.

## Related Sources
- [[../sources/zhu-2025-robust-hybrid-acc-pm-psz|Zhu 2025]]: Uses SOCP to reformulate robust hybrid ACC-PM optimization for Personal Sound Zones.

## Related Concepts
- [[active-noise-control|Active Noise Control]]
