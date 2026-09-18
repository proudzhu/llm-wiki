---
type: source
created: 2026-09-18
updated: 2026-09-18
sources:
  - raw/papers/elisei-iliescu-2019-low-rank-rls/full-text.txt
  - https://doi.org/10.1109/TASLP.2019.2903276
  - zotero://select/items/0_ZUMGZQNZ
tags:
  - adaptive-filtering
  - echo-cancellation
  - low-rank-approximation
  - kronecker-product
  - system-identification
  - regularization
---

# Elisei-Iliescu, Paleologu, Benesty, Stanciu, Anghel & Ciochină 2019: Recursive Least-Squares Algorithms for the Identification of Low-Rank Systems

**Authors**: [[entities/camelia-elisei-iliescu|Camelia Elisei-Iliescu]], [[entities/constantin-paleologu|Constantin Paleologu]], [[entities/jacob-benesty|Jacob Benesty]], [[entities/cristian-stanciu|Cristian Stanciu]], [[entities/cristian-anghel|Cristian Anghel]], [[entities/silviu-ciochina|Silviu Ciochină]]
**Institutions**: University Politehnica of Bucharest, Romania; INRS-EMT, University of Quebec, Montreal, Canada
**Venue**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, 2019
**Type**: Journal article
**DOI**: [10.1109/TASLP.2019.2903276](https://doi.org/10.1109/TASLP.2019.2903276)
**Zotero**: [Open item](zotero://select/items/0_ZUMGZQNZ)
**Extraction note**: Plain-text extraction (pypdf) — no figures available; figure references below follow the paper's captions.

## Summary

This paper develops recursive least-squares (RLS) adaptive filters for identifying long, low-rank systems such as network and acoustic echo paths. The impulse response of length $L = L_1 L_2$ is decomposed via the nearest Kronecker product and a rank-$P$ low-rank approximation, so that a single $L$-tap identification problem is reformulated as two coupled shorter filters of lengths $P L_1$ and $P L_2$ (with $P \ll L_2$), yielding both lower complexity and faster tracking than the regular RLS algorithm. A variable regularized version (VR-RLS-NKP-DCD), which estimates the SNR online and solves the regularized normal equations with dichotomous coordinate descent (DCD) iterations, adds robustness to double-talk.

## Problem Formulation

The signal model is the classical system identification setup

$$d(t) = \mathbf{h}^T \mathbf{x}(t) + w(t) = y(t) + w(t),$$

where $\mathbf{h}$ is the unknown impulse response (the echo path, in echo cancellation), $\mathbf{x}(t)$ contains the most recent $L$ input samples, and $w(t)$ is additive noise with $\mathrm{SNR} = \sigma_y^2 / \sigma_w^2$.

The RLS algorithm converges fast but its $O(L^2)$ complexity is prohibitive for echo paths with hundreds or thousands of coefficients; fast variants (DCD-based, QR-decomposition-based) reduce the constant but still face the convergence/tracking challenges of long adaptive filters. The paper instead attacks the *dimension* of the problem.

**Nearest Kronecker product decomposition.** Split $\mathbf{h}$ into $L_2$ short responses $\mathbf{s}_l$ of length $L_1$ and rearrange them into the $L_1 \times L_2$ matrix $\mathbf{H} = [\mathbf{s}_1 \, \mathbf{s}_2 \, \cdots \, \mathbf{s}_{L_2}]$. The normalized misalignment between $\mathbf{h}$ and a Kronecker factorization $\mathbf{h}_2 \otimes \mathbf{h}_1$ equals the relative Frobenius-norm distance between $\mathbf{H}$ and the rank-1 matrix $\mathbf{h}_1 \mathbf{h}_2^T$, which the SVD solves exactly ([[concepts/nearest-kronecker-product|nearest Kronecker product]], [[concepts/eckart-young-theorem|Eckart–Young theorem]]): with $\mathbf{H} = \mathbf{U}_1 \boldsymbol{\Sigma} \mathbf{U}_2^T$, the optimal factors are $\mathbf{h}_1 = \sqrt{\sigma_1}\mathbf{u}_{1;1}$, $\mathbf{h}_2 = \sqrt{\sigma_1}\mathbf{u}_{2;1}$. The rank-$P$ generalization approximates

$$\mathbf{h} \approx \mathbf{h}^{(P)} = \sum_{p=1}^{P} \mathbf{h}_{2;p} \otimes \mathbf{h}_{1;p} = \sum_{p=1}^{P} \sigma_p\, \mathbf{u}_{2;p} \otimes \mathbf{u}_{1;p}, \qquad P \leq L_2,$$

with approximation quality measured by the normalized misalignment $M[\mathbf{h}^{(P)}] = \|\mathbf{h} - \mathbf{h}^{(P)}\|_2 / \|\mathbf{h}\|_2$. If $\mathrm{rank}(\mathbf{H}) = P \ll L_2$, the system can be identified *at least as well* as with the conventional approach while adapting far fewer parameters. Echo-path matrices are never really full rank (redundancies from reflections and sparseness), so the framework fits echo cancellation naturally; sparsity helps by lowering the rank but is not the only factor.

## Methodology

### RLS-NKP algorithm (Section III)

The adaptive filter mirrors the decomposition: $\hat{\mathbf{h}}(t) = \sum_{p=1}^{P} \hat{\mathbf{h}}_{2;p}(t) \otimes \hat{\mathbf{h}}_{1;p}(t)$, i.e., two stacked shorter filters $\hat{\mathbf{h}}_1(t)$ (length $P L_1$) and $\hat{\mathbf{h}}_2(t)$ (length $P L_2$). Using the Kronecker identities $(\hat{\mathbf{h}}_{2;p} \otimes \mathbf{I}_{L_1})\hat{\mathbf{h}}_{1;p} = (\mathbf{I}_{L_2} \otimes \hat{\mathbf{h}}_{1;p})\hat{\mathbf{h}}_{2;p}$, the error signal takes two equivalent forms

$$e_1(t) = d(t) - \hat{\mathbf{h}}_1^T(t-1)\,\mathbf{x}_2(t), \qquad e_2(t) = d(t) - \hat{\mathbf{h}}_2^T(t-1)\,\mathbf{x}_1(t),$$

where the auxiliary inputs $\mathbf{x}_{2;p}(t) = [\hat{\mathbf{h}}_{2;p}(t-1) \otimes \mathbf{I}_{L_1}]^T \mathbf{x}(t)$ and $\mathbf{x}_{1;p}(t) = [\mathbf{I}_{L_2} \otimes \hat{\mathbf{h}}_{1;p}(t-1)]^T \mathbf{x}(t)$ mix the far-end input with the *current* estimate of the other filter — a bilinear optimization strategy in which each filter is optimized while the other is held fixed over past time indices, with the cross-dependence attenuated by forgetting factors $\lambda_1, \lambda_2$.

Two exponentially weighted least-squares cost functions (one per filter) lead to normal equations $\mathbf{R}_2(t)\hat{\mathbf{h}}_1(t) = \mathbf{p}_2(t)$ and $\mathbf{R}_1(t)\hat{\mathbf{h}}_2(t) = \mathbf{p}_1(t)$, where $\mathbf{R}_2, \mathbf{p}_2$ (resp. $\mathbf{R}_1, \mathbf{p}_1$) accumulate the auxiliary regressors $\mathbf{x}_2$ (resp. $\mathbf{x}_1$). Applying the matrix inversion lemma gives Kalman gain updates of standard RLS form but on the *smaller* matrices:

$$\hat{\mathbf{h}}_1(t) = \hat{\mathbf{h}}_1(t-1) + \mathbf{k}_2(t)\,e(t), \qquad \hat{\mathbf{h}}_2(t) = \hat{\mathbf{h}}_2(t-1) + \mathbf{k}_1(t)\,e(t),$$

with $\mathbf{k}_2(t) = \mathbf{R}_2^{-1}(t-1)\mathbf{x}_2(t) / [\lambda_1 + \mathbf{x}_2^T(t)\mathbf{R}_2^{-1}(t-1)\mathbf{x}_2(t)]$ (and symmetrically for $\mathbf{k}_1$). The conversion factors $\gamma_1(t), \gamma_2(t) \in (0, 1]$ satisfy $|\varepsilon_i(t)| \leq |e_i(t)|$, so the algorithm is convergent. Forgetting factors follow the rule $\lambda_i = 1 - 1/(K \cdot \text{filter length})$.

**Limitation**: RLS-NKP is *not* a "fast" RLS algorithm — complexity remains quadratic in the (shorter) filter lengths, because the tap-delay-line time-shift structure of $\mathbf{x}_1, \mathbf{x}_2$ is destroyed by the Kronecker mixing, so the low-complexity tricks of RLS-DCD / QRD-LSL cannot be applied straightforwardly.

### Variable regularized VR-RLS-NKP-DCD algorithm (Section IV)

Double-talk (near-end speech acting as a large disturbance) is handled through *regularization* rather than a forgetting factor close to 1 (which would destroy tracking). The regularized cost functions $J + \delta_1\|\hat{\mathbf{h}}_1(t)\|_2^2$ and $J + \delta_2\|\hat{\mathbf{h}}_2(t)\|_2^2$ yield updates with $[\mathbf{R}_2(t) + \delta_1 \mathbf{I}_{PL_1}]^{-1}$ and $[\mathbf{R}_1(t) + \delta_2 \mathbf{I}_{PL_2}]^{-1}$ in place of the inverse covariance matrices.

The optimal regularization parameters are found by requiring the expected squared error of the correction components to equal the noise power, $E[\bar{e}_i^2(t)] = \sigma_w^2$. Under simplifying approximations (diagonal input covariance $\approx \sigma_x^2 \mathbf{I}$, statistically independent short filters with equal norms, i.e., block-diagonal $\mathbf{R}$), the conditions reduce to quadratic equations $\delta_i^2 - 2(\alpha_i/\mathrm{SNR})\delta_i - \alpha_i^2/\mathrm{SNR} = 0$ with $\alpha_1 = L_1 E[\|\hat{\mathbf{h}}_2\|_2^2]\sigma_x^2$ and $\alpha_2 = L_2 E[\|\hat{\mathbf{h}}_1\|_2^2]\sigma_x^2$, whose positive roots are

$$\delta_i = \alpha_i \left(1 + \sqrt{1 + \mathrm{SNR}}\right) / \mathrm{SNR}.$$

In practice the SNR is estimated online via recursive power estimates of the desired and estimated signals, $\widehat{\mathrm{SNR}}(t) = \hat{\sigma}_y^2(t) / |\hat{\sigma}_d^2(t) - \hat{\sigma}_y^2(t)|$, which conveniently folds the near-end speech into the denominator — this is exactly what provides double-talk robustness (an "ideal" version given the true background-noise SNR cannot cope with near-end speech). Constant regularization is used for the first $L$ iterations, since the SNR estimate is biased before initial convergence.

Because the regularization parameters enter the matrix to be inverted, the matrix inversion lemma no longer applies; the auxiliary normal equations for the weight increments are instead solved with **dichotomous coordinate descent (DCD)** iterations (multiplication-free, bit-shift based, hardware friendly), with the number of successful updates $N_u = 1$ and $M_b = 16$ predefined step-size values sufficing in practice. The symmetric block-Toeplitz structure of the outer-product updates $\mathbf{x}_i(t)\mathbf{x}_i^T(t)$ gives a further complexity reduction factor $P(P+1)/(4P^2)$.

### Computational complexity (Table III)

| Algorithm | Multiplications per iteration |
|-----------|-------------------------------|
| RLS | $2L^2 + 2L$ |
| RLS-NKP | $(P+2)L + 2(PL_1)^2 + 2(PL_2)^2 + 2PL_1 + 3PL_2$ |
| VR-RLS-NKP-DCD | $(P+2)L + \frac{P(P+1)}{4P^2}[(PL_1)^2 + (PL_2)^2] + \dots$ (DCD: additions only, $N_u = 1$) |
| RLS-DCD | $5L$ multiplications (cheapest) |
| QRD-LSL | $25L + 11$ |

For $L = 500$ ($L_1 = 25$, $L_2 = 20$), RLS-NKP becomes more expensive than RLS only for $P \geq 16$; for $L = 1024$ ($L_1 = L_2 = 32$), for $P \geq 23$. VR-RLS-NKP-DCD stays below RLS even for large $P$ and is comparable to QRD-LSL for $P \ll L_2$.

## Experimental Setup

| Element | Setting |
|---------|---------|
| Impulse responses | Six echo paths: G168 network echo paths (a) single 64-tap cluster and (b) two clusters (64 + 96 taps); (c), (d) burst responses of one/two Gaussian random clusters; (e), (f) two measured acoustic echo paths — (a)–(d) $L = 500$, (e)–(f) $L = 1024$ |
| Decomposition | $L_1 = 25$, $L_2 = 20$ for $L = 500$; $L_1 = L_2 = 32$ for $L = 1024$ |
| Sparseness measure | $\xi_{12}(\mathbf{h})$ (ℓ1/ℓ2-based), decreasing from 0.8957 (a) to 0.6475 (f) |
| Input signal | AR(1) process ($1/(1-0.9z^{-1})$) or speech sequence, 8 kHz sampling |
| Noise | White Gaussian, SNR = 20 dB |
| Forgetting factors | $\lambda = 1 - 1/(K \cdot \text{length})$, $K = 10$ (plus variations) |
| Benchmarks | RLS, RLS-DCD ($M_b = 16$, $N_u = 1$), QRD-LSL; "ideal" R-RLS-NKP with true SNR |
| Metric | Normalized misalignment (dB), averaged over 20 independent trials |
| Tracking test | Abrrupt echo-path changes (12-sample right shift, sign flip, or switch to another path) at fixed times |

## Results

- **Approximation validity (Figs. 3–4)**: singular values of $\mathbf{H}$ decay fast for the network and burst paths, so small $P$ suffices (misalignment $\leq -100$ dB-scale for G168 paths already at small $P$); acoustic paths are close to full rank and need larger $P$ (e.g., $P = 10$ vs. $L_2 = 32$ for about $-20$ dB attenuation). Notably, the *less* sparse acoustic path (f) is *better* approximated than (e) — sparsity helps but the decomposition is the decisive factor.
- **Tracking (Figs. 5–10)**: with forgetting factors set by the same $K$, RLS-NKP ($P \geq 3$) matches the initial convergence and steady-state misalignment of RLS/RLS-DCD but reacts markedly faster to abrupt echo-path changes, because it adapts two short filters instead of one long one. Alternatively, with larger forgetting factors it reaches a *lower* misalignment level while keeping tracking similar to RLS with a smaller factor.
- **Double-talk robustness (Figs. 11–15)**: in double-talk (near-end speech for 1 s), RLS-NKP diverges, the "ideal" R-RLS-NKP (true SNR) also degrades, while VR-RLS-NKP-DCD remains stable and clearly outperforms both, thanks to the online SNR estimate absorbing the near-end speech. Its only cost is a slower tracking reaction right after path changes (bias of the $\hat{\sigma}_y^2 \approx \hat{\sigma}_y^2$ approximation during reconvergence).

## Key Contributions

1. **RLS-NKP algorithm**: the first RLS formulation built on the nearest Kronecker product decomposition + low-rank approximation of the impulse response (extending the authors' earlier iterative Wiener filter from a time-invariant batch method to a practical adaptive one), turning an $L$-dimensional identification problem into two coupled $PL_1$/$PL_2$-dimensional problems.
2. **Optimal regularization for the decomposed filters**: closed-form variable regularization parameters $\delta_i(t) = L_i \|\hat{\mathbf{h}}_j(t-1)\|_2^2\, s(t)\, \sigma_x^2$ (with $s(t) = [1+\sqrt{1+\widehat{\mathrm{SNR}}(t)}]/\widehat{\mathrm{SNR}}(t)$) derived from the condition $E[\bar{e}_i^2] = \sigma_w^2$, yielding double-talk robustness without sacrificing tracking.
3. **Practical SNR estimation**: recursive power-difference estimate $\widehat{\mathrm{SNR}}(t) = \hat{\sigma}_y^2(t)/|\hat{\sigma}_d^2(t) - \hat{\sigma}_y^2(t)|$ that automatically includes near-end speech in the "noise" term.
4. **DCD-based implementation**: VR-RLS-NKP-DCD replaces the cubic-cost matrix inversion with leading-element dichotomous coordinate descent iterations ($N_u = 1$ suffices), making the regularized version cheaper than RLS-NKP and comparable in complexity to QRD-LSL for $P \ll L_2$.

## Related Concepts

- [[concepts/rls-nkp|RLS-NKP]] — the algorithm family introduced by this paper
- [[concepts/nearest-kronecker-product|Nearest Kronecker Product]] — the decomposition underlying the approach
- [[concepts/kronecker-product|Kronecker Product]]
- [[concepts/singular-value-decomposition|Singular Value Decomposition]]
- [[concepts/eckart-young-theorem|Eckart–Young Theorem]] — optimality of the rank-$P$ approximation
- [[concepts/adaptive-filtering|Adaptive Filtering]]
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/system-identification|System Identification]]
- [[concepts/wiener-filter|Wiener Filter]] — the time-invariant predecessor framework
- [[concepts/robust-adaptive-filtering|Robust Adaptive Filtering]] — variable regularization as a robustness mechanism

## Related Sources

- [[sources/wikipedia-kronecker-product|Wikipedia: Kronecker Product]] — mathematical background for the Kronecker product and its identities
- [[sources/wang-2021-kronecker-adaptive-beamforming|Wang et al. 2021: Kronecker Product Adaptive Beamforming]] — the same rank-$P$ Kronecker decomposition idea applied to MVDR beamforming rather than system identification
- [[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025: Low-Rank Robust Superdirective Beamforming]] — N-way rank-$P$ Kronecker decomposition with alternating updates, the beamforming-side analogue of the bilinear strategy used here
- [[sources/fang-2020-robust-residual-echo-suppression|Fang 2020: Robust Residual Echo Suppression]] — a different (statistical-correlation based) route to double-talk robustness in echo control
