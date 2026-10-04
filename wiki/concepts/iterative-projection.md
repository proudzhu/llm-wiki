---
type: concept
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/ono-2011-stable-fast-update-rules-iva/full-text.md
tags:
  - optimization-algorithms
  - blind-source-separation
  - independent-vector-analysis
  - computational-efficiency
---

# Iterative Projection (IP)

**Iterative Projection (IP)** is the demixing-matrix update rule of **AuxIVA**, the auxiliary-function-based (majorization-minimization) solver for [[concepts/independent-vector-analysis|IVA]] introduced by [[entities/nobutaka-ono|Nobutaka Ono]] (WASPAA 2011). It updates **one demixing filter at a time** in closed form — a projection that makes the updated row orthogonal (in the weighted inner product) to all other rows — alternating with updates of the weighted covariance matrices. IP requires **no step size** and guarantees monotonic decrease of the IVA cost function, which made AuxIVA the de-facto standard IVA solver.

## Key Formulations

### The IP update

With the auxiliary (majorizing) function

$$
\mathcal{L}_2=\sum_{f}\sum_{k}\boldsymbol{w}_{kf}^{\mathsf{H}}\boldsymbol{V}_{kf}\boldsymbol{w}_{kf}-2\sum_f\log|\det(\boldsymbol{W}_f)|,
\qquad
\boldsymbol{V}_{kf}=\frac{1}{N}\sum_n\varphi(r_{kn})\,\boldsymbol{x}_{fn}\boldsymbol{x}_{fn}^{\mathsf{H}},
$$

the update of row $k$ keeping all others fixed has the closed form

$$
\boldsymbol{w}_{kf}\leftarrow(\boldsymbol{W}_f\boldsymbol{V}_{kf})^{-1}\boldsymbol{e}_k,
\qquad
\boldsymbol{w}_{kf}\leftarrow\frac{\boldsymbol{w}_{kf}}{\sqrt{\boldsymbol{w}_{kf}^{\mathsf{H}}\boldsymbol{V}_{kf}\boldsymbol{w}_{kf}}}.
$$

The stationary conditions are $\boldsymbol{w}_l^{\mathsf{H}}\boldsymbol{V}_k\boldsymbol{w}_k=\delta_{lk}$ — the new row is $\boldsymbol{V}_k$-orthogonal to every other row (hence "projection") and $\boldsymbol{V}_k$-normalized.

### Why sequential?

Minimizing $\mathcal{L}_2$ over **all** rows of $\boldsymbol{W}_f$ simultaneously is a Hybrid Exact-Approximate joint Diagonalization (HEAD) problem (Yeredor 2009) with no known closed-form solution; the block-coordinate (one row at a time) relaxation is what makes the closed form possible.

## Properties

- **Tuning-free and monotonic**: inherits MM guarantees — every update decreases the true IVA objective; no step size as in the [[concepts/natural-gradient|natural gradient]].
- **Cost**: $M$ covariance matrices and $M$ matrix inversions per iteration; complexity $O(FM^3\max(M,N))$ — cubic-plus in the number of microphones.
- **Stability caveat**: the inherent matrix inversion can become unstable if some $\boldsymbol{V}_{kf}$ turns ill-conditioned — the motivation for the inverse-free [[concepts/iterative-source-steering|ISS]].
- **Two-source case**: for $M=2$ the joint problem reduces to a $2\times2$ [[concepts/generalized-eigenvalue-decomposition|generalized eigenvalue problem]] solvable globally — the basis of IP2 pairwise updates (Ono 2018).

## Position in the AuxIVA Update Family

| Update | What changes per step | Others frozen? | Subproblem |
|--------|----------------------|----------------|------------|
| **IP** (Ono 2011) | One demixing filter, closed form | Yes | Linear system + normalization |
| IP2 (Ono 2018) | Two filters via $2\times2$ GEVD | Yes | Generalized eigenvalue problem |
| [[concepts/iterative-source-steering|ISS]] (Scheibler & Ono 2020) | Rank-1 steering update of all rows | No (rank-1 only) | Scalar quadratic (inverse-free) |
| [[concepts/iterative-projection-with-adjustment|IPA]] (Scheibler 2021) | One filter replaced + all others adjusted | **No** | [[concepts/log-quadratically-penalized-quadratic-minimization|LQPQM]] (secular equation) |

Because IP's machinery is reused by many source-model extensions — most prominently [[concepts/independent-low-rank-matrix-analysis|ILRMA]], but also IDLMA and VAE-based models — any faster or stabler variant of these updates propagates to the whole family.

## Related Concepts

- [[concepts/independent-vector-analysis|Independent Vector Analysis]] — the parent framework
- [[concepts/natural-gradient|Natural Gradient]] — the step-size-based predecessor
- [[concepts/iterative-source-steering|Iterative Source Steering]] — the inverse-free quadratic-complexity alternative
- [[concepts/iterative-projection-with-adjustment|Iterative Projection with Adjustment]] — the joint-update extension
- [[concepts/generalized-eigenvalue-decomposition|Generalized Eigenvalue Decomposition]] — the two-source closed form
- [[concepts/blind-source-separation|Blind Source Separation]]

## Related Sources

- [[sources/ono-2011-stable-fast-update-rules-iva|Ono 2011: Stable and Fast Update Rules for IVA]] — introduces AuxIVA and the IP rule
- [[sources/scheibler-2020-fast-stable-bss-rank-1-updates|Scheibler & Ono 2020: Fast and Stable BSS with Rank-1 Updates]] — ISS as the inverse-free replacement
- [[sources/scheibler-2021-log-quadratically-penalized-iva|Scheibler 2021: IVA via LQPQM]] — IPA, which removes the frozen-others limitation
- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]] — surveys the family
