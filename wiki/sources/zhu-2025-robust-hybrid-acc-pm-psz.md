---
type: source
created: 2026-04-19
updated: 2026-04-19
sources:
- https://doi.org/10.21437/Interspeech.2025-65
tags:
- acoustic-contrast-control
- personal-sound-zones
- pressure-matching
- robust-optimization
- socp
---

# A Robust Hybrid ACC-PM Approach for Personal Sound Zones

**Authors**: Yaqi Zhu, Lei Zhou, Hongqing Liu, Liming Shi, Lu Gan
**Conference**: Interspeech 2025
**DOI**: 10.21437/Interspeech.2025-65

## Abstract Synthesis
This paper addresses the performance degradation of Personal Sound Zone (PSZ) systems due to transfer function uncertainties (temperature drift, head movement).

- **Objective**: Robust control balancing acoustic contrast (AC) and signal distortion.
- **Methodology**: A robust hybrid optimization framework (ACC-PM).
- **Mathematical Reformulation**: Models uncertainties as norm-bounded, transforming the inherently non-convex optimization into a solvable **Second-Order Cone Programming (SOCP)** problem.
- **Performance**: Demonstrates >18% improvement in Acoustic Contrast compared to vanilla (non-robust) ACC-PM in numerical simulations.

## Key Contributions
1. **Robustness**: Provides a framework to mitigate sensitivity to environmental perturbations.
2. **Computational Tractability**: Converts worst-case optimization into a tractable SOCP form, enabling real-time potential.
3. **Optimality Trade-off**: Effectively balances contrast vs. target reproduction accuracy.

## Relevance
Essential reading for robust PSZ system design, particularly where environmental positioning is non-static.

## Related Concepts

## Related Synthesis
