---
type: concept
created: 2026-05-18
updated: 2026-10-17
sources:
  - raw/papers/rout-2012-pso-anc-without-secondary-path/full-text.txt
  - raw/papers/maeda-1999-anc-simultaneous-perturbation/full-text.md
aliases:
- Heuristic ANC
- Evolutionary ANC
tags:
- active-noise-control
- nonlinear-systems
- optimization
- meta-heuristics
---

# Heuristic ANC Algorithms

## Overview

**Heuristic ANC algorithms** apply population-based, biologically inspired global optimisers to active noise control problems that are difficult for gradient-based methods — typically [[nonlinear-active-noise-control|NLANC]] settings where the secondary path is non-convex or NP-hard, and conventional adaptive filters get trapped in local minima. A distinctive practical advantage of many heuristic ANC algorithms is that they can operate **without explicit estimation of the secondary path $S(z)$**. A non-population gradient-free relative is the [[concepts/simultaneous-perturbation|simultaneous perturbation]] method ([[sources/maeda-1999-anc-simultaneous-perturbation|Maeda & Yoshida 1999]]), which estimates the error-surface gradient from one or two perturbed measurements along a single filter trajectory rather than a population — cheaper per step, but without global-search guarantees.

## Algorithm Catalogue

| Year | Algorithm | Inspiration | NLANC Properties |
|:-----|:----------|:------------|:-----------------|
| 1994 | **Genetic Algorithm (GA)** | Darwinian evolution | First heuristic for ANC; adaptive GA + interior-point method (IPM) |
| 2006 | **Particle Swarm Optimisation (PSO)** | Bird flocking | Cooperation/competition; works with $\tanh\{\cdot\}$ saturation models |
| 2012 | **Conditional Reinitialized PSO (CRPSO)** | Bird flocking + change detection | Online linear ANC; no secondary path estimate; survives abrupt path changes |
| 2010s | **Backtracking Search (BSA)** | Evolutionary algorithm | Population-based EA + sequential quadratic programming |
| 2010s | **Bacterial Foraging Optimisation (BFO)** | *E. coli* chemotaxis | ~5 dB better steady-state vs GA-ANC |
| — | **Firefly (FF)** | Firefly luminescence | Cascades FLANN+FIR with FF coefficient search |
| — | **Fireworks Algorithm (FWA)** | Fireworks explosion | Three variants studied for NLANC |
| — | **Memetic Algorithm (MA)** | Cultural evolution | Distributed adaptation for zone-of-quiet design |

## Why Use Heuristic Methods?

1. **Local-minima escape**: Non-convex NLANC cost surfaces (especially with saturating actuators) trap gradient methods.
2. **No secondary-path estimate required**: GA-ANC and PSO-ANC can work directly on residual error.
3. **Black-box objective compatibility**: Allow non-differentiable cost functions such as **Wilcoxon norm** for outlier-contaminated data.
4. **Multi-channel/distributed scenarios**: Naturally parallel population evaluations.

## Trade-offs

| Pro | Con |
|:----|:----|
| Global optima reachable | High computational cost per iteration |
| Robust to non-differentiable costs | Slow convergence vs gradient methods |
| Avoid secondary-path identification | Sensitive to population size & operators |
| Useful for nonlinear secondary paths | Hard to provide convergence guarantees |

## Hybrid Approaches

- **GA + IPM** — interior-point method searches the feasible region for linear/quadratic constraints.
- **BSA + SQP** — sequential quadratic programming for sinusoidal and complex random signals.
- **FLANN + FF** — neural expansion with firefly weight adaptation.
- **Empirical Weight Update (EWU)** — addresses slow convergence of stochastic approximation and PSO via [[remote-microphone-technique|RMT]].

## Open Problems

- Selecting **optimal population size** for heuristic-NLANC is largely heuristic itself.
- Theoretical convergence analysis under impulsive/non-Gaussian noise is missing.
- Combining heuristic optimisers with **distributed ANC** for WASNs remains underexplored.

## Related Concepts

- [[nonlinear-active-noise-control|Nonlinear ANC]]
- [[active-noise-control|Active Noise Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS]]
- [[remote-microphone-technique|Remote Microphone Technique]]
- [[secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/conditional-reinitialized-pso|Conditional Reinitialized PSO]]
- [[concepts/simultaneous-perturbation|Simultaneous Perturbation]] — single-trajectory gradient-free optimization via random coefficient perturbations

## Related Sources

- [[../sources/lu-2021-anc-survey-nonlinear|Lu et al. 2021: Survey on ANC — Part II (Nonlinear)]]
- [[sources/rout-2012-pso-anc-without-secondary-path|Rout, Das & Panda 2012: PSO-Based ANC Without Secondary Path Identification]] — systematic online PSO-ANC with the CRPSO change-detection/reinitialization mechanism
- [[../sources/yang-2014-cuckoo-search-review|Yang 2014: Cuckoo Search Review]] — Related metaheuristic
- [[sources/maeda-1999-anc-simultaneous-perturbation|Maeda & Yoshida 1999: ANC Using Simultaneous Perturbation]] — non-population gradient-free relative: perturbation-measured stochastic gradient, no secondary-path estimate
