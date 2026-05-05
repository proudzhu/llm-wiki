---
type: source
created: 2026-05-03
updated: 2026-05-03
sources:
  - raw/papers/sharma-1998-momentum-adaptive-filtering/full-text.md
  - https://doi.org/10.1109/78.668805
  - zotero://select/items/0_SGFLZXZU
tags:
  - adaptive-filtering
  - momentum
  - asymptotic-analysis
  - convergence
  - LMS
---

# Sharma, Sethares & Bucklew 1998: Analysis of Momentum Adaptive Filtering Algorithms

**Authors**: [[../entities/rajesh-sharma|Rajesh Sharma]], [[../entities/william-sethares|William A. Sethares]], [[../entities/james-bucklew|James A. Bucklew]]

**Institution**: ERIM International (Sharma); University of Wisconsin–Madison (Sethares, Bucklew)

**Published**: IEEE Transactions on Signal Processing, Vol. 46, No. 5, pp. 1431–1434, May 1998

**Type**: Journal Article (Correspondence)

**DOI**: [10.1109/78.668805](https://doi.org/10.1109/78.668805)

**Zotero**: [SGFLZXZU](zotero://select/items/0_SGFLZXZU)

## Summary

This paper analyzes the momentum LMS (MLMS) algorithm and other momentum adaptive algorithms using asymptotic techniques (weak convergence and central limit theorems) that provide almost sure behavior of parameter estimates and their asymptotic Gaussian distribution. Unlike prior analysis by Roy & Shynk (1990), this work makes no assumptions on the autocorrelation function or distribution of the input process, and no independence assumption between the weight vector and input.

## Problem Formulation

The MLMS recursion is:

$$W_{k+1} = W_k + \mu(D_k - W_k^T X_k)X_k + \alpha(W_k - W_{k-1}) \tag{1}$$

where $W_k \in \mathbb{R}^d$ is the parameter estimate, $D_k$ is the desired response, $X_k \in \mathbb{R}^d$ is the input process, $\alpha \in (-1,1)$ is the momentum factor, and $\mu > 0$ is the step size.

**Assumptions:**

| Label | Assumption |
|-------|-----------|
| H1 | $\{(X_k, D_k)\}$ is zero-mean stationary ergodic; $E[|X_0|^2]$ and $E[|D_0|^2]$ finite |
| H2 | $R = E[X_0 X_0^T]$ is positive definite |
| H3 | Algorithm initialized with $W_0 = 0$ |
| H4 | $\sqrt{\mu}\sum_{k=0}^{[t/\mu]-1} Z_k \Rightarrow B(t)$ (functional CLT for $Z_k = (D_k - X_k^T W^*)X_k$) |
| H4' | $D_k = X_k^T W^* + U_{k+1}$, with $\{U_k\}$ i.i.d. independent of $\{X_k\}$ |

The optimum Wiener solution is $W^* = R^{-1}P$ where $P = E[X_k D_k]$.

## Methodology

### Asymptotic Convergence (ODE Method)

Define $W_\mu(t) = W_{[t/\mu]}$ and $\beta = 1/(1-\alpha)$. Using weak convergence theory, for fixed $\alpha \in (-1,1)$:

$$\lim_{\mu \to 0} \sup_{t \leq T} |W_{\mu,\alpha}(t) - \mathcal{W}_\alpha(t)| = 0 \quad \text{w.p.1} \tag{2}$$

where the limiting ODE solution is:

$$\mathcal{W}_\alpha(t) = W^* - \delta_\alpha(t) \tag{3}$$

$$\delta_\alpha(t) = \sum_{i=1}^{d} \frac{e^{-\beta\lambda_i t}}{\lambda_i} q_i q_i^T p \tag{4}$$

The ODE governing the dynamics is $\dot{w} = \beta(P - Rw)$, with $\beta = 1/(1-\alpha)$ acting as a convergence rate accelerator.

### Convergence Rate Analysis

The transient decay:

$$|\delta_\alpha(t)|^2 = \sum_{i=1}^{d} \left(\frac{q_i^T p}{\lambda_i^2}\right)^2 e^{-2\beta\lambda_i t}$$

- **$\alpha > 0$**: $\beta > 1$, so $\delta_\alpha(t) \to 0$ faster → faster convergence than LMS
- **$\alpha < 0$**: $\beta < 1$, so $\delta_\alpha(t) \to 0$ slower → slower convergence than LMS
- **$\alpha = 0$**: $\beta = 1$, recovers standard LMS behavior

### Uniformity in $\alpha$

For $\alpha^* \in (0,1)$ and any $T > 0$:

$$\lim_{\mu \to 0} \sup_{\alpha \in [-\alpha^*, \alpha^*]} \sup_{t \leq T} |W_{\mu,\alpha}(t) - \mathcal{W}_\alpha(t)| = 0 \quad \text{w.p.1} \tag{9}$$

This means $\mu_0$ does not depend on $\alpha$ when $\alpha$ is restricted to $[-\alpha^*, \alpha^*]$.

### Asymptotic Distribution (Central Limit Result)

Under H4, $W_k$ is asymptotically Gaussian with mean $W^*$ and covariance $\mu\beta\Sigma$, where:

$$\Sigma = \sum_{k=1}^{d}\sum_{l=1}^{d}\sum_{m=1}^{d} q_k q_k^T \bar{q}_l \bar{q}_l^T q_m q_m^T \frac{\bar{\lambda}_l}{\lambda_k + \lambda_m} \tag{11}$$

Under H4' (independent noise), the covariance simplifies to:

$$\frac{\mu\beta E[U_1^2]}{2} I_{d \times d} \tag{12}$$

**Key insight**: As $\alpha \to 1$, $\beta \to \infty$, and the covariance becomes unbounded — confirming the instability of MLMS when $|\alpha| \to 1$.

### Convergence–Misadjustment Tradeoff

From Example 1: Setting $\mu_{\text{MLMS}} = (1-\alpha)\mu_{\text{LMS}}$ yields identical covariance (same misadjustment) and identical convergence rate. This means the convergence speedup from $\alpha > 0$ comes with a proportional increase in misadjustment.

## Extension to Other Momentum Algorithms

The analysis extends to any algorithm of the form:

$$W_{k+1} = \alpha_0 W_k + \mu H(W_k, Y_k, U_{k+1}) \tag{13}$$

### Sign-Sign Algorithm with Momentum

$$\hat{W}_{k+1} = \hat{W}_k - \mu\,\text{sgn}(X_k)\,\text{sgn}(X_k^T\hat{W}_k + U_k) + \alpha(\hat{W}_k - \hat{W}_{k-1}) \tag{14}$$

Local stability requires eigenvalues of $E[\text{sgn}(X_0)X_0^T]$ to have strictly positive real parts. At equilibrium with i.i.d. symmetric inputs, the asymptotic covariance is:

$$\frac{\beta\mu}{4 f_u(0)\sigma} I_{d \times d}$$

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| System | First-order AR: $X_{k+1} = rX_k + e_{k+1}$, $r = 0.8182$ |
| Step size | $\mu = 0.001$ |
| Momentum factors | $\alpha \in \{-0.8, -0.5, 0, 0.5, 0.8\}$ |
| Trajectory validation | ODE solution vs. simulated trajectory |
| Density estimation | 1M iterations, last 500K for steady-state density |

## Results

1. **Trajectory matching**: Theoretical ODE trajectories closely match simulated parameter estimates for all tested $\alpha$ values
2. **Convergence rate**: $\alpha > 0$ accelerates convergence; $\alpha < 0$ decelerates it — consistent with Roy & Shynk (1990)
3. **Steady-state density**: Simulated error densities match the predicted Gaussian distribution
4. **Stability**: All $\alpha \in (-1,1)$ yield stable algorithms; instability occurs as $|\alpha| \to 1$
5. **Misadjustment**: The $\beta = 1/(1-\alpha)$ factor directly scales the asymptotic variance — faster convergence comes with proportionally larger misadjustment

## Key Contributions

1. **Almost sure convergence** of MLMS for all $\alpha \in (-1,1)$ without Gaussian or independence assumptions on the input
2. **ODE characterization** of MLMS dynamics with $\beta = 1/(1-\alpha)$ as the effective convergence rate multiplier
3. **Asymptotic Gaussian distribution** of parameter estimates with explicit covariance formulas
4. **Uniformity result**: the approximation holds uniformly over $\alpha \in [-\alpha^*, \alpha^*]$ for any $\alpha^* < 1$
5. **Extension to general momentum algorithms** including sign-sign with momentum
6. **Confirmation of convergence–misadjustment tradeoff**: $\alpha > 0$ speeds convergence but increases misadjustment proportionally

## Related Concepts

- [[../concepts/momentum-lms|Momentum LMS]]
- [[../concepts/adaptive-filtering|Adaptive Filtering]]
- [[../concepts/asymptotic-analysis-adaptive-algorithms|Asymptotic Analysis of Adaptive Algorithms]]

## Related Synthesis

- [[../synthesis/adaptive-algorithm-tradeoffs|Adaptive Algorithm Trade-offs]]
