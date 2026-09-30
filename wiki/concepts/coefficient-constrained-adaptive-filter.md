---
type: concept
created: 2026-09-30
updated: 2026-09-30
sources:
  - raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/full-text.md
tags:
  - beamforming
  - adaptive-filtering
  - microphone-arrays
  - robust-beamforming
---

# Coefficient-Constrained Adaptive Filter (CCAF)

**Category**: Constrained adaptive algorithm / robust beamforming

## Definition

A **coefficient-constrained adaptive filter (CCAF)** is an adaptive filter in which *every individual tap* is clamped to its own interval $[\psi_{m,n}, \phi_{m,n}]$ after each adaptation step. The constraint therefore defines a **box region** in coefficient space that the filter trajectory can never leave — a stricter and more *shape-controllable* device than a single scalar constraint such as leakage, noise injection, or a norm bound.

The concept was introduced by [[entities/osamu-hoshuyama|Hoshuyama]], [[entities/akihiko-sugiyama|Sugiyama]] & [[entities/akihiro-hirano|Hirano]] (IEEE TSP 1999) specifically to build a robust [[concepts/adaptive-blocking-matrix|adaptive blocking matrix]] inside a [[concepts/gsc-beamformer|generalized sidelobe canceller]].

## Key Formulations

Each CCAF inside the blocking matrix is an adaptive noise canceller driven by the fixed-beamformer output $d(k)$ as a common reference:

$$y_m(k) = x_m(k-P) - H_m^T(k)D(k) \tag{1}$$

$$H_m(k) \triangleq [h_{m,0}(k), \dots, h_{m,N-1}(k)]^T, \qquad D(k) \triangleq [d(k), \dots, d(k-N+1)]^T \tag{2,3}$$

Adaptation is NLMS followed by a **per-coefficient clamp**:

$$h'_{m,n} = h_{m,n}(k) + \alpha \frac{y_m(k)}{\lVert D(k) \rVert^2} d(k-n) \tag{4}$$

$$h_{m,n}(k+1) = \begin{cases} \phi_{m,n}, & h'_{m,n} > \phi_{m,n} \\ \psi_{m,n}, & h'_{m,n} < \psi_{m,n} \\ h'_{m,n}, & \text{otherwise} \end{cases} \tag{5}$$

with $\alpha$ the step size and $\phi_{m,n}$, $\psi_{m,n}$ the upper and lower limits of the $(m,n)$-th coefficient.

## Designing the Constraint Region

The limits are *derived from the task*, not tuned blindly. The procedure is:

1. Compute the optimal (Wiener) coefficient vectors that minimize the **target** signal at the blocking-matrix output, for each candidate target DOA across the sector one wants to support.
2. Take the upper and lower envelope of those coefficient trajectories as $[\psi_{m,n}, \phi_{m,n}]$.

The resulting region has a characteristic "hump" shape: the coefficients that cancel a target arriving on-axis differ strongly from those that cancel a target arriving off-axis, and the difference grows with the DOA offset. Hoshuyama et al. show that the **fixed beamformer's target enhancement is what creates this spread** — with a single microphone (no target enhancement) the target-minimizing and interference-minimizing coefficient sets are nearly indistinguishable and the mechanism has nothing to exploit.

## Why It Works

Two effects follow directly from clamping the coefficients:

| Effect | Mechanism |
|:-------|:----------|
| **Bounded target tracking** | Inside the designed sector the target-minimizing solution is reachable, so the filter converges there and the blocking matrix's spatial pattern follows the target. Outside the sector the target-minimizing solution is *unreachable*, so the filter cannot mistrack onto interference — the maximum allowable target-direction error is an explicit design output (4°–20° demonstrated in the source paper). |
| **Preserved interference at the reference** | The filter also cannot converge to the *interference*-minimizing solution, so a large residual interference remains at the blocking-matrix outputs. That residual is exactly the target-free reference the downstream canceller needs, so interference reduction goes **up** rather than down. |

This is the conceptual inversion that separates CCAFs from earlier robustness fixes: previous constraints (leakage, noise injection, norm constraint) traded interference reduction for robustness, whereas constraining the *blocking matrix* converts the same robustness requirement into a better reference signal for the canceller.

## Relation to Other Constraint Families

| Constraint | Where applied | Effect |
|:-----------|:--------------|:-------|
| Leakage / noise injection | Noise canceller | Prevent misadjustment from target leakage; cost interference reduction |
| [[concepts/norm-constrained-adaptive-filter\|Norm constraint]] | Noise canceller | Cap total tap energy; cost interference reduction at large direction error |
| **Per-coefficient box (CCAF)** | **Blocking matrix** | **Bounded tracking with no loss of interference-reduction degrees of freedom** |
| Target tracking / calibration | Whole beamformer | Larger error tolerance, but mistracks burst signals and needs matrix products |

## Limitations

- The constraint region is array- and sector-specific and must be re-derived for a different microphone arrangement.
- Because blocking is frequency dependent, a region calibrated on white signals is only approximately valid for colored signals — a colored interference just outside the nominal sector can be partially absorbed by the blocking matrix and thereby becomes unavailable to the canceller.
- Performance is sensitive to both the CCAF step size and the downstream canceller's step size, adapted in opposite directions.

## Related Concepts

- [[concepts/adaptive-blocking-matrix|Adaptive Blocking Matrix (ABM)]]
- [[concepts/norm-constrained-adaptive-filter|Norm-Constrained Adaptive Filter (NCAF)]]
- [[concepts/gsc-beamformer|Generalized Sidelobe Canceller (GSC)]]
- [[concepts/target-signal-cancellation|Target-Signal Cancellation]]
- [[concepts/steering-vector-error|Steering-Vector Error]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]
- [[concepts/fixed-beamformer|Fixed Beamformer]]

## Related Sources

- [[sources/hoshuyama-1999-robust-adaptive-beamformer-ccaf|Hoshuyama, Sugiyama & Hirano 1999: A Robust Adaptive Beamformer with a Blocking Matrix Using Constrained Adaptive Filters]] — introduces the CCAF and the constraint-region design procedure
