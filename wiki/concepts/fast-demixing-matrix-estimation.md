---
type: concept
created: 2026-08-19
updated: 2026-08-19
sources:
  - raw/papers/ishikawa-2025-real-time-speech-extraction/full-text.md
tags:
  - blind-source-separation
  - independent-low-rank-matrix-analysis
  - optimization-algorithms
  - computational-efficiency
  - numerical-stability
---

# Fast Demixing Matrix Estimation (FastVCD / FastIP)

**Fast Demixing Matrix Estimation** refers to the **FastVCD** and **FastIP** update rules for the demixing matrix $\mathbf{W}_i$ in [[concepts/independent-low-rank-matrix-analysis|ILRMA]] and spatially regularized ILRMA, derived by applying four algebraic transformations to the conventional **Vectorwise Coordinate Descent (VCD)** and **Iterative Projection (IP)** updates. The Fast variants are **analytically equivalent** to the originals (the cost function is monotone non-increasing along the update sequence) but achieve ~33% speedup and improved numerical stability.

## Background: VCD and IP in ILRMA

The standard ILRMA demixing-matrix update rule is **Iterative Projection (IP)**, which updates one row $\mathbf{w}_{in}$ of $\mathbf{W}_i$ at a time by solving a generalized eigenvector problem involving the source's weighted sample covariance and a normalization. IP requires a **general matrix inversion** per source per frequency bin.

When spatial regularization is added (SR-ILRMA), the IP rule no longer has a closed form and is replaced by **Vectorwise Coordinate Descent (VCD)**, which solves a quartic minimization per row using an auxiliary-vector technique. VCD is more expensive than IP and contains a **conditional branch** that can produce NaNs when the auxiliary quadratic form degenerates.

## Four Algebraic Transformations

The Fast variants apply the following sequence of transformations to VCD/IP. Each step preserves the cost-monotonicity guarantee.

### (i) Sherman–Morrison Hermitian-Inversion Trick

Replace the **general** matrix inversion that appears in the VCD/IP update (the $D$ or $\Phi$ matrix) with a **Hermitian** matrix inversion. Use the Sherman–Morrison formula to convert the general matrix into a rank-1 perturbation of a Hermitian matrix, then invert it in $\mathcal{O}(N^2)$ rather than $\mathcal{O}(N^3)$.

This removes the dominant computational bottleneck of the original VCD/IP.

### (ii) Replace Two MatVecs with One MatVec + Two Memory Accesses

Two matrix–vector products in the original update are shown to be redundant — one of them can be replaced by a memory access to a quantity that has already been computed. This is a small but consistent constant-factor speedup.

### (iii) Replace MatMat with Row/Column Updates Using Structure of $\mathbf{F}_{in}^{(l)}$

The auxiliary matrix $\mathbf{F}_{in}^{(l)}$ has the special structure $\mathbf{F}_{in}^{(l)} = \mathbf{w}_{in}^{\mathsf{H}} \boldsymbol{\Xi}_{in} \mathbf{w}_{in} + \ldots$, where $\boldsymbol{\Xi}_{in}$ is fixed across iterations. Matrix–matrix products can therefore be replaced by **row/column updates** that reuse already-computed values. After this transformation, $\mathbf{W}_i$ only appears in its own update — there are no cross-row products.

This is the largest single speedup contributor.

### (iv) Collapse Conditional Branch into Single Closed Form

The original VCD contains a conditional branch on $|\tilde{h}_{in}|$ vs. $\varepsilon$ to avoid division by zero when computing the update scalar $\varphi_{in}$. The Fast variant uses a single closed-form expression involving the phase of a complex auxiliary quantity $\chi_{in}$:

$$\varphi_{in} = e^{j\theta_{in}}\,\frac{\sqrt{\bar{\chi}_{in}^2 + 1} - \bar{\chi}_{in}}{\sqrt{\eta_{inn}}},$$

which is **continuous** in the auxiliary variables and never produces NaNs.

## FastVCD vs FastIP

| Variant | Used in | Update rule | Complexity per row |
|---|---|---|---|
| **VCD** (original) | SR-ILRMA | Coordinate descent with auxiliary vector + conditional branch | $\mathcal{O}(N^3)$ |
| **FastVCD** | SR-ILRMA | VCD after transformations (i)–(iv) | $\mathcal{O}(N^2)$ |
| **IP** (original) | Naive-ILRMA, NSR-ILRMA | Eigenvector-based projection | $\mathcal{O}(N^3)$ |
| **FastIP** | Naive-ILRMA, NSR-ILRMA | IP after transformations (i)–(iv) (without the VCD-specific parts) | $\mathcal{O}(N^2)$ |

Both FastVCD and FastIP share transformations (i) and (iii); FastVCD additionally uses (ii) and (iv) which arise only in the VCD auxiliary-vector machinery.

## Empirical Gains

- **Speed**: FastVCD runs in ~2/3 the time of Normal VCD on Intel Core i9-13900KF.
- **Numerical stability**: FastVCD is more stable than Normal VCD across all values of an ill-conditioning parameter $\varsigma$ in toy-model experiments (Fig. 7 of [[sources/ishikawa-2025-real-time-speech-extraction|Ishikawa et al. 2025]]).
- **Edge devices**: FastIP + NSR-ILRMA runs in real time on NVIDIA Jetson AGX Xavier and AGX Orin, with the same SDR/SIR as a desktop CPU.

## Relationship to ISS

The [[concepts/iterative-source-steering|Iterative Source Steering (ISS)]] family of updates for IVA achieves a similar speedup by avoiding matrix inversions entirely via rank-one updates. FastVCD/FastIP are a **complementary** line of work: they keep the IP/VCD structure but remove the expensive inversions, and they are designed to integrate with spatial regularization, whereas ISS requires a different cost-function formulation.

## Related Concepts

- [[concepts/independent-low-rank-matrix-analysis|Independent Low-Rank Matrix Analysis (ILRMA)]]
- [[concepts/rank-constrained-spatial-covariance-matrix-estimation|Rank-Constrained Spatial Covariance Matrix Estimation (RCSCME)]]
- [[concepts/spatial-regularization|Spatial Regularization]]
- [[concepts/iterative-source-steering|Iterative Source Steering (ISS)]] (related fast-update paradigm for IVA)

## Related Sources

- [[sources/ishikawa-2025-real-time-speech-extraction|Ishikawa et al. 2025: Real-Time RCSCME-based Speech Extraction]]
