---
type: concept
created: 2026-10-18
updated: 2026-10-18
sources:
  - raw/papers/wishnick-2014-time-varying-filters-musical/full-text.md
tags:
  - time-varying-systems
  - filter-design
  - digital-filters
  - audio-processing
  - adaptive-filtering
---

# Time-Varying Filter

A **time-varying filter** has coefficients that change over time — in digital audio, any filter with a user-controllable parameter (an equalizer, an LFO- or envelope-modulated filter such as a phaser). While most classical filter theory assumes time-invariance, changing coefficients of a recursive filter raises two distinct problems: **stability** (the filter may blow up even if every frozen coefficient set is stable) and **transients** (the state must re-adjust, producing artifacts).

## Musical vs. Speech-Coding Requirements

The two dominant application domains have conflicting goals ([[sources/wishnick-2014-time-varying-filters-musical|Wishnick 2014]]):

| Requirement | Musical applications | Speech coding (e.g., LPC) |
|---|---|---|
| Parameter change rate | Every sample (LFO, envelope) | Sparingly (per frame) |
| Ideal on change | *Smooth* transition — abrupt jumps click | **Output switching** — output equals old filter's output before the change, new filter's after |
| Transients | Pole-change transients are perceptually benign and even *desirable* (they smooth the change) | Transients are defects to eliminate |

An instantaneous parameter change corresponds to an instantaneous jump in amplitude/phase, whose spectrum shows high **sidebands** audible as a click. Output switching removes state transients but preserves — and thus emphasizes — the discontinuity itself, which is why transient-minimization methods from speech coding score "poor" in musical listening tests.

## Stability of Time-Varying Recursive Filters

A filter whose coefficients at every instant match a stable time-invariant filter may still be unstable when coefficients change. Laroche (2007) gives stricter criteria, both stated on the **state transition matrix** $\mathbf{P}$ (the matrix mapping the state vector from $n-1$ to $n$):

1. **Criterion 1**: there exists $0 \leq \gamma < 1$ with $\|\mathbf{P}\| \leq \gamma$ (Euclidean norm);
2. **Criterion 2**: there exists a change of basis $\mathbf{T}$ with $\|\mathbf{T}\mathbf{P}\mathbf{T}^{-1}\| \leq \gamma$.

Structure-dependence is decisive: Direct-Form II, lattice, and normalized ladder structures are not necessarily stable under coefficient change; the coupled form (Gold & Rader) and the trapezoidally-integrated [[concepts/state-variable-filter|state variable filter]] are time-varying stable (the latter proven by Wishnick via Criterion 2).

## Taxonomy of Approaches

**Transient minimization** — techniques that reduce the transient signal, defined as the deviation from the output-switching model:

- *Zetterberg & Zhang (1988)*: exact output switching via state recomputation; requires the entire input signal — not realtime.
- *Välimäki & Laakso (1998)*: finite-history approximation, realtime but designed for sparsely occurring changes; audio-rate modulation would require many parallel filters.
- *Rabenstein (1988)*: intermediate coefficients minimizing transient-signal variance; also intended for widely spaced changes.

**Stabilization** — forcing an ordinarily unstable-when-time-varying structure to stay stable:

- *Rabenstein & Czarnach (1985)*: state-vector transformation relating the structure to the coupled form; applicable every sample, absorbable into the coefficient matrix (no extra filtering cost, costlier coefficient computation). Confirmed effective in listening tests, with only a small quality decrease.

**Inherently stable structures** — choose a structure that is time-varying stable by construction, e.g., the coupled form or the TDF-II SVF.

## Evaluation Criteria

- **Steady-state DC response** (objective): feed constant DC, change parameters instantaneously; the ideal output is unchanged (matching the output switching model when DC gain is unchanged). The TDF-II SVF achieves this exactly and provably; most structures do not.
- **Transient-signal variance**: the classical speech-coding objective — but essentially *uncorrelated* with musical listening-test scores (Pearson's $r = 0.11$).
- **Sideband energy** (proposed by Wishnick): spectral energy around the change point outside the immediate analysis band (one ERB); negatively correlated with MUSHRA scores ($r = -0.59$), making it a candidate design objective for musical time-varying filters.

## Related Concepts

- [[concepts/state-variable-filter|State Variable Filter]] — the structure recommended for musical time-varying filtering
- [[concepts/state-space-model|State-Space Model]] — stability criteria are stated on the state transition matrix
- [[concepts/adaptive-filtering|Adaptive Filtering]] — adaptive algorithms also vary coefficients, though typically guided by an error signal rather than user/LFO control

## Related Sources

- [[sources/wishnick-2014-time-varying-filters-musical|Wishnick 2014: Time-Varying Filters for Musical Applications]] — taxonomy, SVF stability proof, and the MUSHRA evidence separating musical from speech-coding goals
