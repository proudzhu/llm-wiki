---
type: concept
created: 2026-09-18
updated: 2026-09-18
tags:
  - linear-algebra
  - kronecker-product
  - low-rank-approximation
  - signal-processing
---

# Nearest Kronecker Product

The **nearest Kronecker product (NKP)** problem asks for factors $\mathbf{A}, \mathbf{B}$ minimizing $\lVert \mathbf{M} - \mathbf{A} \otimes \mathbf{B} \rVert$ for a matrix given only numerically, since exact factorizations rarely exist. It is solved exactly by the [[concepts/singular-value-decomposition|SVD]] (Van Loan & Pitsianis 1992).

## Solution via SVD and Eckart–Young

Reshape the target vector $\mathbf{h}$ (length $L = L_1 L_2$) into the $L_1 \times L_2$ matrix $\mathbf{H}$ (e.g., for an impulse response: $L_2$ short responses of length $L_1$ as columns). The normalized misalignment between $\mathbf{h}$ and a Kronecker factorization $\mathbf{h}_2 \otimes \mathbf{h}_1$ equals the relative Frobenius-norm distance between $\mathbf{H}$ and the rank-1 matrix $\mathbf{h}_1 \mathbf{h}_2^T$. Hence the best rank-1 Kronecker approximation is given by the leading singular triplet of $\mathbf{H} = \mathbf{U}_1 \boldsymbol{\Sigma} \mathbf{U}_2^T$:

$$\mathbf{h}_1 = \sqrt{\sigma_1}\,\mathbf{u}_{1;1}, \qquad \mathbf{h}_2 = \sqrt{\sigma_1}\,\mathbf{u}_{2;1},$$

which is exactly the [[concepts/eckart-young-theorem|Eckart–Young theorem]] in disguise.

## Rank-P Generalization

The **rank-$P$ nearest Kronecker product** approximates

$$\mathbf{h} \approx \mathbf{h}^{(P)} = \sum_{p=1}^{P} \mathbf{h}_{2;p} \otimes \mathbf{h}_{1;p} = \sum_{p=1}^{P} \sigma_p\, \mathbf{u}_{2;p} \otimes \mathbf{u}_{1;p}, \qquad P \leq L_2,$$

with approximation quality measured by the normalized misalignment $\lVert \mathbf{h} - \mathbf{h}^{(P)} \rVert_2 / \lVert \mathbf{h} \rVert_2$. If $\mathrm{rank}(\mathbf{H}) = P \ll L_2$, the parameter count drops from $L$ to $P(L_1 + L_2)$. Splitting into **more than two** factors (N-way Kronecker decomposition) is harder and is treated as a tensor-decomposition problem — the setting used in [[concepts/kronecker-product-beamforming|Kronecker product beamforming]].

## Applications

- **Echo-path identification**: network echo paths (G168) and burst-type responses have fast-decaying singular values of $\mathbf{H}$, so small $P$ suffices; measured acoustic paths are closer to full rank and need larger $P$. Echo-path matrices are never really full rank (redundancies from reflections and sparseness). Sparsity helps by lowering the rank but is not the only factor — [[concepts/rls-nkp|RLS-NKP]] builds an adaptive filter directly on this decomposition.
- **Beamforming**: sum-of-$P$-Kronecker-products filter representations for arbitrary array geometries ([[concepts/kronecker-product-beamforming|Kronecker product beamforming]]), where the low-rank structure also improves robustness.
- **Subband adaptive filters** and parameter reduction for multichannel ANC controllers.

## Related Concepts

- [[concepts/kronecker-product|Kronecker Product]]
- [[concepts/singular-value-decomposition|Singular Value Decomposition]]
- [[concepts/eckart-young-theorem|Eckart–Young Theorem]]
- [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]]
- [[concepts/rls-nkp|RLS-NKP]]

## Related Sources

- [[sources/wikipedia-kronecker-product|Wikipedia: Kronecker Product]] — mathematical background
- [[sources/elisei-iliescu-2019-low-rank-rls|Elisei-Iliescu et al. 2019: Recursive Least-Squares Algorithms for the Identification of Low-Rank Systems]] — rank-$P$ NKP as the foundation of low-rank adaptive identification
- [[sources/wang-2021-kronecker-adaptive-beamforming|Wang et al. 2021: Kronecker Product Adaptive Beamforming]] — the same decomposition applied to MVDR beamforming
- [[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025: Low-Rank Robust Superdirective Beamforming]] — N-way rank-$P$ Kronecker decomposition with alternating updates
