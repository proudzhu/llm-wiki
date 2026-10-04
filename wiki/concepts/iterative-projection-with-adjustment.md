---
type: concept
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/scheibler-2021-log-quadratically-penalized-iva/full-text.md
tags:
  - optimization-algorithms
  - blind-source-separation
  - independent-vector-analysis
  - computational-efficiency
---

# Iterative Projection with Adjustment (IPA)

**Iterative Projection with Adjustment (IPA)** is an update rule for auxiliary-function-based [[concepts/independent-vector-analysis|IVA]] (AuxIVA) proposed by [[entities/robin-scheibler|Robin Scheibler]] (IEEE TSP 2021). Unlike the classic IP, IP2, and [[concepts/iterative-source-steering|ISS]] updates — which freeze all other sources while updating one — IPA **replaces one demixing filter while jointly adjusting all the others** along the current direction of that source, so every update makes progress on all sources at once.

## Key Formulations

### Multiplicative rank-2 update

The demixing matrix is updated as

$$
\boldsymbol{W}\leftarrow\boldsymbol{T}_{k}(\boldsymbol{u},\boldsymbol{q})\,\boldsymbol{W},
\qquad
\boldsymbol{T}_{k}(\boldsymbol{u},\boldsymbol{q})=\boldsymbol{I}+\boldsymbol{e}_{k}(\boldsymbol{u}-\boldsymbol{e}_{k})^{\mathsf{H}}+\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*}\boldsymbol{e}_{k}^{\top}
$$

where $\boldsymbol{u}$ is the new $k$-th demixing filter (as in IP, completely replaced) and $\boldsymbol{q}\in\mathbb{C}^{M-1}$ holds one adjustment coefficient per other source (an ISS-style rank-1 correction). The perturbation $\boldsymbol{T}_k-\boldsymbol{I}$ has rank 2.

### Reduction to LQPQM

Minimizing the AuxIVA quadratic surrogate over $(\boldsymbol{u},\boldsymbol{q})$ jointly (Theorem 1 of the source paper) yields:

1. A closed form for the filter,
$$
\boldsymbol{u}^{\star}=\frac{\boldsymbol{V}_{k}^{-1}\tilde{\boldsymbol{q}}_{k}}{\sqrt{\tilde{\boldsymbol{q}}_{k}^{\mathsf{H}}\boldsymbol{V}_{k}^{-1}\tilde{\boldsymbol{q}}_{k}}}\,e^{j\theta},
\qquad \tilde{\boldsymbol{q}}_{k}=\boldsymbol{e}_{k}-\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*}
$$
2. The optimal adjustment $\boldsymbol{q}^{\star}$ as the solution of a [[concepts/log-quadratically-penalized-quadratic-minimization|LQPQM]] — the quadratic terms of the other sources against the log-determinant of the update — solvable globally in a few Newton-Raphson iterations via its secular equation.

## Properties and Performance

- **Monotonic convergence**: IPA is an MM-compatible block update of the AuxIVA surrogate, inheriting the no-step-size, monotone-decrease guarantees of the auxiliary-function framework.
- **Cost per update**: comparable to or cheaper than IP (no per-source matrix inversion of the IP kind is needed beyond the $\boldsymbol{V}_k$-related transform); ISS remains cheaper per update but converges in more iterations.
- **Convergence speed** (100 random reverberant rooms, 2–5 sources, SNR 5–25 dB, CMU Arctic speech):
  - Same or higher final SI-SDR/SI-SIR than IP, ISS, IP2 after 100 iterations in essentially all conditions.
  - Ties IP2 in iteration count for 2–3 sources; faster in runtime.
  - **More than twice as fast** as all competing methods (iterations and runtime) for 4–5 sources.
  - For two sources, even beats IP2 despite IP2 performing globally optimal surrogate minimization there — suggesting IPA's joint updates also accelerate the underlying IVA objective, not just the surrogate.

## Position in the AuxIVA Update Family

| Update | What changes per step | Others frozen? | Subproblem |
|--------|----------------------|----------------|------------|
| IP (Ono 2011) | One demixing filter, closed form | Yes | Linear system |
| IP2 (Ono 2018) | Two filters via $2\times2$ GEVD | Yes | Generalized eigenvalue problem |
| ISS (Scheibler & Ono 2020) | Rank-1 steering update of all rows | No (but only along rank-1) | Scalar quadratic |
| **IPA** (Scheibler 2021) | One filter replaced + all others adjusted | **No** | [[concepts/log-quadratically-penalized-quadratic-minimization|LQPQM]] (secular equation) |

Because many AuxIVA descendants (ILRMA source models, overdetermined IVA, geometrically constrained variants) reuse the IP/ISS machinery, IPA updates are expected to transfer to those frameworks as well.

## Related Concepts

- [[concepts/log-quadratically-penalized-quadratic-minimization|LQPQM]] — the subproblem each IPA step must solve
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/iterative-source-steering|Iterative Source Steering]] — the rank-1 update family IPA extends
- [[concepts/blind-source-separation|Blind Source Separation]]

## Related Sources

- [[sources/scheibler-2021-log-quadratically-penalized-iva|Scheibler 2021: Independent Vector Analysis via Log-Quadratically Penalized Quadratic Minimization]] — introduces IPA
- [[sources/scheibler-2020-fast-independent-vector-extraction|Scheibler & Ono 2020: Fast Independent Vector Extraction]] — the companion special case where the surrogate admits a global closed-form solver
- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]] — context of the IP/ISS families IPA builds on
