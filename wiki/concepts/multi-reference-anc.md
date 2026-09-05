---
type: concept
created: 2026-09-05
updated: 2026-09-05
sources:
  - raw/papers/he-2026-neural-projection-filter-anc/full-text.md
tags:
  - active-noise-control
  - multi-channel
  - reference-projection
  - road-noise
---

# Multi-Reference ANC

## Overview

**Multi-reference ANC** is a feedforward [[concepts/active-noise-control|ANC]] configuration in which many reference sensors ($P$ channels, typically structural-vibration accelerometers or reference microphones) feed the adaptive controller. It is the standard architecture for automotive road-noise control, where a single reference cannot capture the distributed, multi-path nature of the tire/road excitation.

More reference channels improve attainable attenuation (each channel adds information about the primary field), but introduce three coupled difficulties:

1. **Inter-channel correlation** — the references are highly correlated, ill-conditioning the adaptive control problem and slowing convergence;
2. **High-dimensional redundancy** — controller input dimension grows with $P$, inflating computational cost;
3. **Deployment limits** — real-time embedded targets cannot sustain the resulting MAC counts.

This motivates a distinct family of methods — **reference compression / projection** — that reduces the $P$ raw references to $Q \ll P$ virtual/projected references before the control filter.

## Reference-Compression Approaches

| Family | Mechanism | Representative |
|---|---|---|
| Decorrelation / prewhitening preconditioning | Fixed linear transforms (EVD/SVD-based) that decouple and whiten references | Bai & Elliott 2004; causal preconditioning filters (Wang 2025) |
| Subspace / virtual references | Online SVD/PCA to retain dominant components | iSVD-VR — 28 virtual references at 95% cumulative contribution (Xia et al. 2026) |
| Point-wise neural projection | DNN generates projected reference samples at sampling rate | NRP-FxAP (He et al., JASA 2026) — strong performance, 17.9 GMAC/s |
| Block-wise neural filter generation | DNN generates causal FIR projection filters per block; projection applied sample-wise | [[concepts/condition-aware-projection-filtering|CAPF]] (He et al. 2026) — NRP-FxAP-level performance at 374 MMAC/s |

Fixed linear preconditioning captures only simple correlation structures, while point-wise neural projection is accurate but computationally heavy; block-wise filter generation (CAPF) keeps the neural inference at block rate and the projection itself linear, bridging the two.

## Relation to Multi-Channel ANC

[[concepts/multi-channel-anc|Multi-channel ANC]] concerns the general MIMO problem of $M$ error sensors and $C$ secondary sources; multi-reference ANC stresses the *input* side (many correlated references). The two combine in road-noise systems (e.g., 42 references → 2 sources → 2 error microphones), where reference compression reduces the back-end controller from a $P$-input to a $Q$-input system (e.g., $Q = 4$), shortening the control filter and improving conditioning.

## Related Concepts

- [[concepts/condition-aware-projection-filtering|Condition-Aware Projection Filtering (CAPF)]]
- [[concepts/multi-channel-anc|Multi-Channel ANC]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/frequency-domain-anc|Frequency-Domain ANC]]
- [[concepts/feedforward-anc|Feedforward ANC]]

## Related Sources

- [[sources/he-2026-neural-projection-filter-anc|He et al. 2026: Neural Projection Filter Generation for Multi-Reference ANC]]
- [[sources/zhang-2023-deep-mcanc|Zhang et al. 2023: Deep MCANC]]
