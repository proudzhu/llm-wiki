---
type: source
created: 2026-09-28
updated: 2026-09-28
sources:
  - raw/papers/rout-2012-pso-anc-without-secondary-path/full-text.txt
  - https://doi.org/10.1109/TIM.2011.2169180
  - zotero://select/items/0_4GXVZ5JC
tags:
  - active-noise-control
  - adaptive-filtering
  - optimization
  - meta-heuristics
  - secondary-path
  - time-varying-systems
---

# Rout, Das & Panda 2012: PSO-Based ANC Without Secondary Path Identification

| Field | Detail |
|-------|--------|
| **Authors** | [[entities/nirmal-kumar-rout\|Nirmal Kumar Rout]], [[entities/debi-prasad-das\|Debi Prasad Das]], [[entities/ganapati-panda\|Ganapati Panda]] |
| **Institution** | KIIT University, Bhubaneswar (Rout); CSIR-Institute of Minerals and Materials Technology, Bhubaneswar (Das); IIT Bhubaneswar (Panda) |
| **Venue** | IEEE Transactions on Instrumentation and Measurement, Vol. 61, No. 2, pp. 554–563 |
| **Year** | 2012 |
| **Type** | Journal article |
| **DOI** | [10.1109/TIM.2011.2169180](https://doi.org/10.1109/TIM.2011.2169180) |
| **Zotero** | [Link](zotero://select/items/0_4GXVZ5JC) |

## Summary

This paper develops a systematic online **particle swarm optimization (PSO)** training scheme for linear feedforward ANC that requires **no secondary path identification** whatsoever. Because the population-based fitness is computed from blocks of residual-error samples rather than instantaneous gradients, the algorithm is immune to secondary-path time variations that destabilize FxLMS and avoids the gradient-descent local-minima problem. The basic PSO, however, loses population diversity once converged and cannot track abrupt primary/secondary path changes, so the authors introduce the **conditional reinitialized PSO (CRPSO)**, which detects path changes via a jump in the gbest squared error and re-randomizes the particle population — restoring global convergence after every abrupt change.

## Problem Formulation

A single-channel feedforward ANC uses an FIR control filter $W(z)$ driven by the reference signal $x(n)$; the anti-noise travels through the secondary path $S(z)$ and superimposes acoustically with the primary disturbance $d(n)$ at the error microphone:

$$e(n) = d(n) + \hat{d}(n)$$

The classical [[concepts/filtered-x-lms-algorithm|FxLMS]] solution has two structural weaknesses that this paper targets:

1. **Secondary path dependence** — the weight update requires a pre-estimated $\hat{S}(z)$ to filter the reference; if $S(z)$ is time-varying or misestimated, performance degrades or the algorithm diverges.
2. **Gradient local minima** — being gradient-based, FxLMS is susceptible to initialization and may converge to local minima.

The optimization objective is restated in a form usable by a non-gradient, population-based method: minimize the **mean square of the residual error over a block of $M$ samples**, evaluated separately for each of $P$ candidate filters (particles). Prior GA-based ANC existed without secondary path estimation, but used binary-coded chromosomes with single-point crossover (slow, many untouched weights per generation) and did not address time-varying paths.

## Methodology

### Online PSO Adaptation Scheme

Evolutionary algorithms are inherently block-based (fitness from a set of samples), while ANC runs sample-by-sample on a non-repeatable noise stream — the same data cannot be replayed for each candidate. The proposed scheme resolves this:

- The $P$ particles are the coefficient vectors of $P$ parallel adaptive FIR filters (columns of $\mathbf{W} \in \mathbb{R}^{N \times P}$).
- A MUX/DMUX pair controlled by the PSO processor routes the live reference signal to **one filter at a time**, each receiving $M$ consecutive fresh samples per generation.
- Each filter's block mean-square error, $e_p(n) = d(n) + \hat{d}_p(n)$ averaged over its $M$ samples, is that particle's fitness.
- Every generation therefore spans $M \times P$ samples; adaptation never stops (no GA-style stopping criterion), so the controller can follow path changes.

### PSO Update Equations

With $W_{pbest_i}$ the best position of particle $i$ and $W_{gbest}$ the global best:

$$V_i(k) = V_i(k-1) + r_1\left[W_{pbest_i} - W_i(k)\right] + r_2\left[W_{gbest} - W_i(k)\right]$$

$$W_i(k) = W_i(k-1) + V_i(k)$$

where $r_1, r_2$ are independent random numbers in $[0,1]$ — simplified from Kennedy–Eberhart's random **vectors** to scalars to reduce complexity. This is the original inertia-free PSO form.

### CRPSO: Conditional Reinitialization for Time-Varying Paths

Once all particles converge, their randomization is lost — they collapse onto one point and cannot adapt to an abrupt primary/secondary path change (e.g., a door opening in a room or vehicle cabin). The gbest squared error $E^2_{gbest}$ signals such changes: it is nearly constant at convergence but jumps suddenly when a path changes. CRPSO inserts:

$$\text{If } \left|E^2_{gbest}(n-1) - E^2_{gbest}(n-2)\right| \le k_1 \;\&\; \left|E^2_{gbest}(n) - E^2_{gbest}(n-1)\right| \ge k_2 \;\text{ then reinitialize } V \text{ and } W$$

with $k_1 < k_2$: $k_1$ near zero ("previously converged") and $k_2$ tuned by experiment ("now significantly degraded"). Re-randomizing the population restores the diversity needed to re-converge to the new global optimum. See [[concepts/conditional-reinitialized-pso|Conditional Reinitialized PSO]].

### Comparison Basis

- **vs FxLMS**: PSO updates weights per generation ($M \times P$ samples) rather than per sample; needs no $\hat{S}(z)$; being evolutionary with random initialization, it has a low chance of local minima. FxLMS "fails miserably" when the true $S(z)$ departs from $\hat{S}(z)$.
- **vs GA**: PSO updates all filter coefficients via the simple algebraic update equations; GA's single-point crossover on binary-coded chromosomes leaves many weights untouched per generation, converges slowly, and pays coding/decoding cost. The MUX/DMUX online scheme is reusable for other evolutionary algorithms.

## Experimental Setup

| Item | Detail |
|------|--------|
| **Platform** | Computer simulation |
| **Primary path** $P(z)$ | $z^{-5} + 0.2z^{-6} + 0.5z^{-7} - 0.9z^{-8}$ (default) |
| **Secondary path** $S(z)$ | $z^{-1} + 1.5z^{-2} - z^{-3}$ (default) |
| **Primary noise** | Zero-mean uniform white noise |
| **ANC filter** | FIR, $N = 10$ taps (swept 5–40; Exp. 1) |
| **Fitness block length** | $M = 20$ samples (swept 10–60; Exp. 2) |
| **Population size** | $P = 200$ particles (swept 10–200; Exp. 3) |
| **Time-varying tests** | Primary path sign flip at gen. 200 (revert at 300); secondary path change to $z^{-1} + 0.5z^{-2}$ at gen. 200 |
| **GA baseline** | Russo–Sicuranza-style GA, population 600 or 100, 8-bit binary coding, 10 coefficients |

## Results

| Experiment | Finding |
|-----------|---------|
| **1: Filter order $N$** | Convergence degrades beyond $N = 10$ (model mismatch; more parameters need larger population). $N = 8$ converges faster but with higher steady-state error; $N = 10$ chosen. |
| **2: Block length $M$** | $M = 20$ onward gives identical convergence and steady-state error; $M = 10$ is degraded. Rule of thumb: $M \ge 2N$. |
| **3: Population $P$** | Larger population → faster convergence and lower steady-state $E^2_{gbest}$; $P = 200$ ideal for this setup. |
| **4: Time-varying primary path** | Basic PSO stays trapped after the abrupt change (all particles stabilized at the old optimum). Manual reinitialization at generation 200 restores convergence; CRPSO recovers **automatically**, including when the path reverts at generation 300. |
| **5: Time-varying secondary path** | CRPSO re-converges to the global minimum after the secondary path change; FxLMS would fail under the same condition since $\hat{S}(z) \ne S(z)$. |
| **6: Robustness (10 runs, seed 0)** | Conventional PSO misses the global minimum in most runs after the primary-path change; CRPSO achieves the global-minimum steady-state squared error in **every** run, for both primary- and secondary-path changes. |
| **7: GA vs CRPSO** | CRPSO (population 100) converges faster than GA (population 600 or 100). After 200 generations, the CRPSO-optimized weights **exactly match the FxLMS weights** (computed with an exact secondary path estimate), while the GA weights do not. |

## Key Contributions

1. **Online PSO training scheme for ANC**: a MUX/DMUX-based implementation that evaluates $P$ candidate filters on consecutive fresh blocks of the live noise stream, removing the offline/repeated-data assumption of evolutionary optimization and running continuously with no stopping criterion.
2. **Secondary-path-free adaptation**: the algorithm never estimates $S(z)$, making it immune to secondary-path time variation and robust where FxLMS diverges — a property shared with GA-based ANC but achieved with faster convergence and no binary coding.
3. **CRPSO**: a conditional reinitialization mechanism that detects abrupt primary/secondary path changes from a jump in the gbest squared error (after a converged plateau) and re-randomizes the population, restoring global convergence — the first PSO-ANC treatment of abrupt path changes (prior dynamic-environment PSO work addressed only slow drift).
4. **Systematic parameter studies**: isolated guidelines for filter length ($N=10$), fitness block length ($M \ge 2N$), and population size ($P=200$ for a 10-tap filter), plus GA and FxLMS comparisons verifying that PSO reaches the true FxLMS optimum.

## Related Concepts

- [[concepts/conditional-reinitialized-pso|Conditional Reinitialized PSO (CRPSO)]]
- [[concepts/heuristic-anc-algorithms|Heuristic ANC Algorithms]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/secondary-path-variability|Secondary Path Variability]]
- [[concepts/primary-path-variability|Primary Path Variability]]
- [[concepts/simultaneous-equations-method|Simultaneous Equations Method]]

## Related Synthesis

- [[synthesis/ai-driven-anc|AI-Driven Active Noise Control]] — the evolutionary-computation (pre-deep-learning) branch of non-gradient ANC control
