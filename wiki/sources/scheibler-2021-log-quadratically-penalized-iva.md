---
type: source
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/scheibler-2021-log-quadratically-penalized-iva/full-text.md
  - https://doi.org/10.1109/TSP.2021.3072228
  - https://arxiv.org/abs/2008.10048
  - zotero://select/items/0_YUQG9IYI
tags:
  - blind-source-separation
  - independent-vector-analysis
  - optimization-algorithms
  - audio-source-separation
  - numerical-algorithms
---

# Scheibler 2021: Independent Vector Analysis via Log-Quadratically Penalized Quadratic Minimization

**Author**: [[entities/robin-scheibler|Robin Scheibler]]
**Affiliation**: Tokyo Metropolitan University, Hino, Japan
**Venue**: IEEE Transactions on Signal Processing, 2021
**Year**: 2021
**Type**: Journal article
**DOI**: [10.1109/TSP.2021.3072228](https://doi.org/10.1109/TSP.2021.3072228)
**arXiv**: [2008.10048](https://arxiv.org/abs/2008.10048)
**Zotero**: [YUQG9IYI](zotero://select/items/0_YUQG9IYI)

## Summary

This paper proposes **iterative projection with adjustment (IPA)**, a new update rule for auxiliary-function-based independent vector analysis (AuxIVA) that updates one demixing filter while *jointly adjusting all the others* along its current direction — unlike IP, IP2, and ISS, which freeze the remaining filters until later updates. The adjustment is implemented as a multiplicative rank-2 perturbation of the demixing matrix, and each update requires solving a non-convex problem the author names **log-quadratically penalized quadratic minimization (LQPQM)**. The paper proves that the global minimum of an LQPQM is the largest zero of a secular equation, computable in a few Newton-Raphson iterations seeded by the real root of a cubic polynomial. On simulated reverberant speech mixtures, AuxIPA converges faster than IP, ISS, and IP2 both per iteration and per unit runtime — more than twice as fast for four and five sources.

## Problem Formulation

Determined blind source separation of $F$ mixtures of $K$ sources recorded by $M=K$ sensors in the STFT domain:

$$
\boldsymbol{x}_{fn}=\boldsymbol{A}_{f}\boldsymbol{s}_{fn}
$$

[[concepts/independent-vector-analysis|IVA]] estimates demixing matrices $\boldsymbol{W}_f$ by minimizing the negative log-likelihood under source independence and a spherical super-Gaussian contrast function $F(\check{\boldsymbol{s}}_{kn})=G(\|\check{\boldsymbol{s}}_{kn}\|)$:

$$
\ell(\mathcal{W})=\sum_{kn}G(\|\check{\boldsymbol{y}}_{kn}\|)-2\sum_{f}\log|\det\boldsymbol{W}_{f}|
$$

AuxIVA majorizes this cost (majorization-minimization) by the quadratic surrogate

$$
\ell_{2}(\mathcal{W})=\sum_{kf}\boldsymbol{w}_{kf}^{\mathsf{H}}\boldsymbol{V}_{kf}\boldsymbol{w}_{kf}-2\sum_{f}\log|\det\boldsymbol{W}_{f}|,
\qquad
\boldsymbol{V}_{kf}=\frac{1}{N}\sum_{n}\frac{G^{\prime}(r_{kn})}{2r_{kn}}\boldsymbol{x}_{fn}\boldsymbol{x}_{fn}^{\mathsf{H}}
$$

Closed-form minimization of the surrogate is possible only for two sources (generalized eigenvalue decomposition); the general case is attacked by block-coordinate descent:

- **IP** (iterative projection, Ono 2011): updates one demixing filter $\boldsymbol{w}_{kf}$ in closed form per step, via $(\boldsymbol{W}_f\boldsymbol{V}_{kf})^{-1}$.
- **IP2** (Ono 2018): pairwise updates of two filters at a time via a $2\times 2$ generalized eigenvalue problem.
- **ISS** ([[concepts/iterative-source-steering|iterative source steering]], Scheibler & Ono 2020): rank-1 updates of the whole matrix, no matrix inversion.

The shared limitation: when updating source $k$, **all other rows stay frozen** — corrections can only arrive at the next iteration. (This "fix the others" structure is also what underlies [[concepts/switching-independent-vector-analysis|Switching IVA]] and other AuxIVA descendants, so any improvement propagates widely.)

## Methodology

### Iterative Projection with Adjustment (IPA)

IPA blends IP and ISS: the $k$-th demixing filter is completely replaced (as in IP), while all other filters are jointly adjusted by a step aligned with the current estimate of source $k$ (as in ISS). The update is multiplicative:

$$
\boldsymbol{W}\leftarrow\boldsymbol{T}_{k}(\boldsymbol{u},\boldsymbol{q})\,\boldsymbol{W},
\qquad
\boldsymbol{T}_{k}(\boldsymbol{u},\boldsymbol{q})=\boldsymbol{I}+\boldsymbol{e}_{k}(\boldsymbol{u}-\boldsymbol{e}_{k})^{\mathsf{H}}+\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*}\boldsymbol{e}_{k}^{\top}
$$

a rank-2 perturbation of the identity, where $\boldsymbol{u}\in\mathbb{C}^M$ is the new $k$-th filter and $\boldsymbol{q}\in\mathbb{C}^{M-1}$ holds the per-source adjustment coefficients.

**Theorem 1** reduces the joint minimization of the surrogate over $(\boldsymbol{u},\boldsymbol{q})$ to:

1. A closed form for the filter,
$$
\boldsymbol{u}^{\star}=\frac{\boldsymbol{V}_{k}^{-1}\tilde{\boldsymbol{q}}_{k}}{\sqrt{\tilde{\boldsymbol{q}}_{k}^{\mathsf{H}}\boldsymbol{V}_{k}^{-1}\tilde{\boldsymbol{q}}_{k}}}\,e^{j\theta},
\qquad \tilde{\boldsymbol{q}}_{k}=\boldsymbol{e}_{k}-\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*}
$$
2. The optimal adjustment $\boldsymbol{q}^{\star}$ as the solution of an LQPQM (below), with $\boldsymbol{A}=\operatorname{diag}(\ldots,\boldsymbol{w}_{k}^{\mathsf{H}}\boldsymbol{V}_{m}\boldsymbol{w}_{k},\ldots)$, $\boldsymbol{b}=[\ldots,\boldsymbol{w}_{k}^{\mathsf{H}}\boldsymbol{V}_{m}\boldsymbol{w}_{m},\ldots]^{\top}$, and $\boldsymbol{C},\boldsymbol{g},z$ formed from the inverse of the weighted covariance $\boldsymbol{V}_k$.

### LQPQM: Log-Quadratically Penalized Quadratic Minimization

> **Problem (LQPQM).** For $\boldsymbol{A},\boldsymbol{C}\in\mathbb{C}^{d\times d}$ Hermitian positive (semi-)definite, $\boldsymbol{b},\boldsymbol{d}\in\mathbb{C}^{d}$, $z\ge 0$:
> $$
> \min_{\boldsymbol{x}\in\mathbb{C}^{d}}\ (\boldsymbol{x}-\boldsymbol{b})^{\mathsf{H}}\boldsymbol{A}(\boldsymbol{x}-\boldsymbol{b})-\log\left((\boldsymbol{x}-\boldsymbol{d})^{\mathsf{H}}\boldsymbol{C}(\boldsymbol{x}-\boldsymbol{d})+z\right)
> $$

Despite being non-convex (the log term "pinches and pulls up" the quadratic bowl, creating multiple stationary points — five in the 2D example of Fig. 1), the global minimum can be computed efficiently:

- **Reduction**: a Cholesky factor $\boldsymbol{G}$ of $\boldsymbol{A}$ converts the problem to the canonical form $\min_{\boldsymbol{y}}\ \boldsymbol{y}^{\mathsf{H}}\boldsymbol{y}-\log((\boldsymbol{y}+\boldsymbol{v})^{\mathsf{H}}\boldsymbol{U}(\boldsymbol{y}+\boldsymbol{v})+z)$.
- **Special case $\boldsymbol{v}=0$** (Theorem 2): the solution follows directly from the eigendecomposition of $\boldsymbol{U}$ — either $\boldsymbol{y}^{\star}=0$ (if $z\ge\varphi_d$) or the top eigenvector scaled by $\sqrt{(\varphi_d-z)/(\boldsymbol{\sigma}_d^{\mathsf{H}}\boldsymbol{U}\boldsymbol{\sigma}_d)}$.
- **General case** (Theorem 3): all stationary points are zeros of the **secular equation**
$$
f(\lambda)=\lambda^{2}\sum_{m\in\mathcal{S}}\frac{\varphi_{m}|\tilde{v}_{m}|^{2}}{(\lambda-\varphi_{m})^{2}}-\lambda+z,
\qquad
\boldsymbol{y}^{\star}=(\lambda^{\star}\boldsymbol{I}-\boldsymbol{U})^{-1}\boldsymbol{U}\boldsymbol{v}
$$
where $\varphi_m$ are the eigenvalues of $\boldsymbol{U}$ and $\tilde{v}_m$ the coefficients of $\boldsymbol{v}$ in the eigenbasis. The objective along the stationary branch, $g(\lambda)=1-\sum_{m}\frac{\varphi_m|\tilde v_m|^2}{\lambda-\varphi_m}-\frac{z}{\lambda}-\log\lambda$, satisfies $g'(\lambda)=f(\lambda)/\lambda^{2}$, so the objective *decreases for increasing roots* — the global minimum is the **largest zero**, which is the unique root in $(\max(\varphi_{\max},z),+\infty)$ where $f$ is strictly decreasing (Lemmas 2–4).

### Root finding

The largest zero is found by **Newton-Raphson** restricted to the safe interval, with two practical ingredients:

1. **Initialization**: keeping only the dominant $(\varphi_{\max},\tilde v_{\max})$ term of $f$ and clearing denominators yields a cubic polynomial whose **largest real root** is a guaranteed-safe, accurate starting point (convergence in a few iterations).
2. **Numerical stability**: all quantities are scaled by $\varphi_{\max}$ (solve $\hat f(\mu)=f(\varphi_{\max}\mu)/\varphi_{\max}=0$) to avoid overflow of $(\lambda-\varphi_m)^{-2}$; a bisection-style fallback ($\lambda\leftarrow(\varphi_{\max}+\lambda)/2$) keeps iterates above $\varphi_{\max}$.

The secular-equation structure is reminiscent of modified eigenvalue problems (Golub 1973), generalized trust-region subproblems, and their appearances in robust beamforming, multi-lateration, and DOA estimation — but to the author's knowledge the LQPQM itself had not been solved before.

## Experimental Setup

| Item | Value |
|------|-------|
| Task | Determined BSS of reverberant speech mixtures |
| Baselines | AuxIVA with IP, ISS, IP2 updates |
| Rooms | 100 random rectangular rooms ([[entities/robin-scheibler|Scheibler]]'s pyroomacoustics); walls 6–10 m, ceiling 2.8–4.5 m |
| Reverberation | $T_{60}\sim$ uniform 60–450 ms |
| Array | Circular, 2–5 mics, 10 cm neighbor spacing; ≥50 cm from walls, 1–2 m high |
| Sources | Placed beyond the critical distance $d_{\text{crit}}=0.057\sqrt{V/T_{60}}$ |
| Signals | CMU Arctic concatenated 15 s utterances, 16 kHz |
| STFT | 4096-point Hamming window, 3/4 overlap, optimal synthesis window (Griffin–Lim) |
| Noise | Uncorrelated Gaussian; SNR $\in\{5,15,25\}$ dB |
| Iterations | 100 (IP2/IPA iterations counted twice — they update twice as many parameters) |
| Scale restoration | Minimal distortion principle w.r.t. first microphone |
| Metrics | SI-SDR, SI-SIR; runtime as real-time factor |

## Results

- **Final quality (100 iterations)**: IPA attains the same or higher final SI-SDR and SI-SIR in essentially all conditions; for many sources and low SNR it clearly beats even IP2. For two sources IP and ISS end slightly higher on SI-SIR — they converge slower but overshoot.
- **Convergence speed**: IPA outperforms all other methods for every source count when runtime is considered. In iteration count it ties IP2 for 2–3 sources. Surprisingly, even in the two-source case (where IP2 performs globally optimal surrogate minimization) IPA converges faster, suggesting subtle effects in minimizing the underlying IVA objective that the author flags for further study.
- **Four and five sources**: IPA converges **more than twice as fast** as IP2, ISS, and IP — in both iterations and runtime — making it attractive for high-performance implementations.

## Key Contributions

1. **IPA update scheme**: the first AuxIVA block-coordinate update that does not freeze the other sources — one demixing filter is replaced while all others are jointly adjusted along its direction, as a multiplicative rank-2 perturbation of the identity.
2. **LQPQM problem class**: a new non-convex optimization problem (quadratic cost minus log-quadratic penalty) with an efficient, provably global solution, argued to be of independent interest (interior-point/barrier methods, capacity maximization under quadratic constraints).
3. **Secular-equation characterization**: all stationary points of an LQPQM are zeros of a secular equation; the objective decreases with increasing roots, so the global minimum is the largest zero — unique, isolated in $(\max(\varphi_{\max},z),\infty)$, and computable by Newton-Raphson seeded from a cubic-polynomial root.
4. **Empirical validation**: on reverberant speech mixtures with 2–5 sources, AuxIVA-IPA dominates the IP/ISS/IP2 family in convergence speed, with >2× speedup for ≥4 sources.

## Related Concepts

- [[concepts/iterative-projection-with-adjustment|Iterative Projection with Adjustment (IPA)]] — the proposed update scheme
- [[concepts/log-quadratically-penalized-quadratic-minimization|LQPQM]] — the introduced optimization problem and its secular-equation solution
- [[concepts/independent-vector-analysis|Independent Vector Analysis]] — the parent framework; AuxIPA is a new BCD family entry alongside IP/IP2/ISS
- [[concepts/iterative-source-steering|Iterative Source Steering]] — the rank-1 update family IPA blends with IP
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/independent-vector-extraction|Independent Vector Extraction]] / [[concepts/fast-independent-vector-extraction|FIVE]] — related special cases where the surrogate *can* be minimized globally
- [[concepts/independent-low-rank-matrix-analysis|ILRMA]] — source-model extension where IPA updates may transfer (flagged as future work)
- [[concepts/generalized-eigenvalue-decomposition|Generalized Eigenvalue Decomposition]] — the two-source closed form and the eigenstructure underlying the secular equation
- [[concepts/si-sdr|SI-SDR]] — evaluation metric

## Related Sources

- [[sources/scheibler-2020-fast-independent-vector-extraction|Scheibler & Ono 2020: Fast Independent Vector Extraction]] — the same author's globally-optimal special-case solver, contrasted with the general-case IPA
- [[sources/nakatani-2022-switching-iva|Nakatani et al. 2022: Switching IVA]] — a downstream AuxIVA descendant whose optimization would benefit from faster updates
- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]] — surveys the IP/ISS families that IPA extends

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — new data point on the convergence-speed frontier of AuxIVA-style BSS
