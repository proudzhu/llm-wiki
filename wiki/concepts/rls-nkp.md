---
type: concept
created: 2026-09-18
updated: 2026-09-18
tags:
  - adaptive-filtering
  - echo-cancellation
  - low-rank-approximation
  - kronecker-product
  - system-identification
---

# RLS-NKP

**RLS-NKP** (Recursive Least-Squares with Nearest Kronecker Product) is a family of adaptive filtering algorithms introduced by Elisei-Iliescu et al. (2019) for identifying long, low-rank systems such as network and acoustic echo paths. It reformulates a single $L$-tap ($L = L_1 L_2$) RLS identification as two coupled, shorter RLS filters of lengths $P L_1$ and $P L_2$ (with $P \ll L_2$), yielding lower complexity and faster tracking than regular RLS.

## Principle

The impulse response estimate mirrors the rank-$P$ [[concepts/nearest-kronecker-product|nearest Kronecker product]] decomposition:

$$\hat{\mathbf{h}}(t) = \sum_{p=1}^{P} \hat{\mathbf{h}}_{2;p}(t) \otimes \hat{\mathbf{h}}_{1;p}(t),$$

i.e., two stacked shorter filters $\hat{\mathbf{h}}_1(t)$ (length $P L_1$) and $\hat{\mathbf{h}}_2(t)$ (length $P L_2$). Using the Kronecker identities $(\hat{\mathbf{h}}_{2;p} \otimes \mathbf{I}_{L_1})\hat{\mathbf{h}}_{1;p} = (\mathbf{I}_{L_2} \otimes \hat{\mathbf{h}}_{1;p})\hat{\mathbf{h}}_{2;p}$, the error signal takes two equivalent forms

$$e_1(t) = d(t) - \hat{\mathbf{h}}_1^T(t-1)\,\mathbf{x}_2(t), \qquad e_2(t) = d(t) - \hat{\mathbf{h}}_2^T(t-1)\,\mathbf{x}_1(t),$$

where the auxiliary inputs $\mathbf{x}_2, \mathbf{x}_1$ mix the far-end input with the *current* estimate of the other filter — a **bilinear alternating optimization** in which each filter is optimized while the other is held fixed over past time indices, with the cross-dependence attenuated by forgetting factors $\lambda_1, \lambda_2$.

Two exponentially weighted least-squares cost functions (one per filter) lead to normal equations $\mathbf{R}_2(t)\hat{\mathbf{h}}_1(t) = \mathbf{p}_2(t)$ and $\mathbf{R}_1(t)\hat{\mathbf{h}}_2(t) = \mathbf{p}_1(t)$. Applying the matrix inversion lemma gives Kalman gain updates of standard RLS form but on the *smaller* matrices, with conversion factors $\gamma_1(t), \gamma_2(t) \in (0, 1]$ guaranteeing $|\varepsilon_i(t)| \leq |e_i(t)|$ (convergence). Forgetting factors follow $\lambda_i = 1 - 1/(K \cdot \text{filter length})$.

**Limitation**: RLS-NKP is not a "fast" RLS algorithm — complexity remains quadratic in the (shorter) filter lengths, because the tap-delay-line time-shift structure of $\mathbf{x}_1, \mathbf{x}_2$ is destroyed by the Kronecker mixing, so the low-complexity tricks of RLS-DCD / QRD-LSL do not apply straightforwardly.

## Variable-Regularized Variant: VR-RLS-NKP-DCD

For [[concepts/acoustic-echo-cancellation|echo cancellation]], double-talk (near-end speech acting as a large disturbance) is handled through *regularization* rather than a forgetting factor close to 1 (which would destroy tracking). The regularized costs $J + \delta_1\|\hat{\mathbf{h}}_1(t)\|_2^2$ and $J + \delta_2\|\hat{\mathbf{h}}_2(t)\|_2^2$ yield closed-form optimal regularization parameters derived from the condition that the expected squared error of the correction components equals the noise power:

$$\delta_i = \alpha_i \left(1 + \sqrt{1 + \mathrm{SNR}}\right) / \mathrm{SNR}, \qquad \alpha_1 = L_1 E[\|\hat{\mathbf{h}}_2\|_2^2]\sigma_x^2, \;\; \alpha_2 = L_2 E[\|\hat{\mathbf{h}}_1\|_2^2]\sigma_x^2.$$

The SNR is estimated online as $\widehat{\mathrm{SNR}}(t) = \hat{\sigma}_y^2(t) / |\hat{\sigma}_d^2(t) - \hat{\sigma}_y^2(t)|$, which folds the near-end speech into the denominator — this is exactly what provides double-talk robustness (an "ideal" version given the true background-noise SNR cannot cope with near-end speech). Because the regularization parameters enter the matrix to be inverted, the matrix inversion lemma no longer applies; the normal equations are instead solved with multiplication-free **dichotomous coordinate descent (DCD)** iterations ($N_u = 1$, $M_b = 16$ step sizes suffice).

## Properties

- **Tracking**: with the same forgetting-factor setting, RLS-NKP ($P \geq 3$) matches RLS's convergence and steady-state misalignment but reacts markedly faster to abrupt echo-path changes, because it adapts two short filters instead of one long one.
- **Complexity**: for $L = 500$ ($L_1 = 25$, $L_2 = 20$), RLS-NKP is cheaper than RLS for $P < 16$; VR-RLS-NKP-DCD stays below RLS even for large $P$ and is comparable to QRD-LSL for $P \ll L_2$.
- **Relation to beamforming analogues**: the bilinear fix-one-optimize-the-other strategy is the two-filter special case of the alternating updates used in [[concepts/kronecker-product-beamforming|Kronecker product beamforming]].

## Related Concepts

- [[concepts/nearest-kronecker-product|Nearest Kronecker Product]] — the decomposition the algorithm is built on
- [[concepts/kronecker-product|Kronecker Product]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/system-identification|System Identification]]
- [[concepts/wiener-filter|Wiener Filter]] — the time-invariant predecessor framework (iterative Wiener filter with NKP decomposition)
- [[concepts/robust-adaptive-filtering|Robust Adaptive Filtering]] — variable regularization as a robustness mechanism
- [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]] — the beamforming-side analogue

## Related Sources

- [[sources/elisei-iliescu-2019-low-rank-rls|Elisei-Iliescu et al. 2019: Recursive Least-Squares Algorithms for the Identification of Low-Rank Systems]] — the paper introducing the algorithm family
- [[sources/wang-2021-kronecker-adaptive-beamforming|Wang et al. 2021: Kronecker Product Adaptive Beamforming]] — rank-$P$ Kronecker decomposition with alternating updates, applied to MVDR beamforming
- [[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025: Low-Rank Robust Superdirective Beamforming]] — N-way rank-$P$ Kronecker decomposition, the beamforming analogue of the bilinear strategy
