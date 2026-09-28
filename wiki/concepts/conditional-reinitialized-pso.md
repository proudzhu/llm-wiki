---
type: concept
created: 2026-09-28
updated: 2026-09-28
sources:
  - raw/papers/rout-2012-pso-anc-without-secondary-path/full-text.txt
tags:
  - active-noise-control
  - optimization
  - meta-heuristics
  - time-varying-systems
---

# Conditional Reinitialized PSO (CRPSO)

**Conditional Reinitialized PSO** is a modification of the particle swarm optimization algorithm introduced by [[entities/nirmal-kumar-rout|Rout]], [[entities/debi-prasad-das|Das]] & [[entities/ganapati-panda|Panda]] (2012) for [[concepts/active-noise-control|active noise control]] systems whose primary or secondary paths change **abruptly**. It detects such changes from a jump in the swarm's global-best squared error and re-randomizes the particle population, restoring the diversity needed to re-converge to the new global optimum.

## Motivation: Diversity Collapse

PSO converges by collapsing its population onto the best-found position. Once converged:

- All particles stabilize at the same point; the randomness of the initial distribution is lost.
- If the optimization landscape changes abruptly (an ANC path change), the swarm sits at the **old** optimum — a local minimum of the new problem — and cannot escape.

Prior dynamic-environment PSO variants (composite particles, multiswarms, clustering) address only **slow** environmental drift by reusing particle experience; ANC path changes (a door opening, a cabin change) are abrupt, so those methods are unsuitable.

## Reinitialization Condition

The gbest squared error $E^2_{gbest}$ is nearly constant while the swarm is fully optimized but jumps suddenly when a path changes. CRPSO monitors consecutive generations and reinitializes the velocity and position vectors when:

$$\left|E^2_{gbest}(n-1) - E^2_{gbest}(n-2)\right| \le k_1 \;\;\&\;\; \left|E^2_{gbest}(n) - E^2_{gbest}(n-1)\right| \ge k_2$$

with $k_1 < k_2$: $k_1$ is near zero (verifying the swarm *was* converged) and $k_2$ is tuned experimentally (verifying the error *has* degraded significantly). The conjunction prevents spurious reinitialization during normal convergence transients.

## Properties in ANC

- Runs inside the online PSO-ANC scheme of [[sources/rout-2012-pso-anc-without-secondary-path|Rout et al. 2012]], where $P$ parallel adaptive FIR filters are evaluated on consecutive blocks of the live noise stream — no secondary path estimate is ever needed.
- In ten independent runs (fixed random seed), CRPSO reached the global-minimum steady-state squared error after every abrupt primary- or secondary-path change, while conventional PSO missed it in most runs.
- After convergence on a static path, the CRPSO-optimized filter weights **exactly match** the FxLMS optimum computed with an exact secondary path — but without requiring that estimate.

## Related Concepts

- [[concepts/heuristic-anc-algorithms|Heuristic ANC Algorithms]] — the broader family of population-based ANC optimizers
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — the gradient-based counterpart that motivates the design
- [[concepts/secondary-path-variability|Secondary Path Variability]] / [[concepts/primary-path-variability|Primary Path Variability]] — the abrupt-change phenomena CRPSO is built to track
- [[concepts/secondary-path-modeling|Secondary Path Modeling]] — the estimation-based alternative CRPSO avoids

## Related Sources

- [[sources/rout-2012-pso-anc-without-secondary-path|Rout, Das & Panda 2012: PSO-Based ANC Without Secondary Path Identification]]
- [[sources/lu-2021-anc-survey-nonlinear|Lu et al. 2021: Survey on ANC — Part II (Nonlinear)]] — situates PSO-ANC within heuristic ANC algorithms
