---
type: concept
created: 2026-05-03
updated: 2026-05-03
sources:
  - raw/papers/sharma-1998-momentum-adaptive-filtering/full-text.md
tags:
  - adaptive-filtering
  - convergence-analysis
  - stochastic-approximation
  - ODE-method
---

# Asymptotic Analysis of Adaptive Algorithms

**Asymptotic analysis** of adaptive algorithms uses weak convergence theory and functional central limit theorems to characterize the almost sure behavior and limiting distribution of parameter estimates, without requiring Gaussian or independence assumptions on the input process.

## Overview

Two complementary asymptotic results are typically derived for adaptive filtering algorithms:

1. **Almost sure convergence** (ODE method): The interpolated parameter estimates converge uniformly to the solution of an associated ODE as the step size $\mu \to 0$
2. **Central limit result**: The parameter estimates are asymptotically Gaussian with computable mean and covariance

## The ODE Method

For a stochastic recursion $W_{k+1} = W_k + \mu H(W_k, Y_k)$, define $W_\mu(t) = W_{[t/\mu]}$. Under appropriate ergodicity and moment conditions:

$$\lim_{\mu \to 0} \sup_{t \leq T} |W_\mu(t) - \mathcal{W}(t)| = 0 \quad \text{w.p.1}$$

where $\mathcal{W}(t)$ solves the ODE $\dot{w} = \bar{h}(w)$ with $\bar{h}(w) = E[H(w, Y_0)]$.

### Key Properties

- The ODE equilibrium $W^*$ is globally stable if $\partial\bar{h}(W^*)/\partial w$ is negative definite
- Convergence rate is governed by the eigenvalues of the ODE's Jacobian at equilibrium
- The result holds with probability one (for essentially any realization)

## Central Limit Theorem for Adaptive Algorithms

Under a functional CLT assumption on the noise process $Z_k = H(W^*, Y_k)$:

$$\sqrt{\mu}\sum_{k=0}^{[t/\mu]-1} Z_k \Rightarrow B(t)$$

the parameter estimates $W_k$ are asymptotically Gaussian with mean $W^*$ and covariance proportional to $\mu$. The exact covariance depends on the long-run covariance $R_L$ of the noise sequence.

## Advantages over Mean-Square Analysis

| Aspect | Mean-Square Analysis | Asymptotic Analysis |
|--------|---------------------|-------------------|
| Input assumptions | Often requires Gaussian, independence | Stationary ergodic, no distributional assumptions |
| $W_k$ and $X_k$ independence | Typically assumed | Not required |
| Type of result | $E[W_k]$, $E[W_k W_k^T]$ | Almost sure behavior, asymptotic distribution |
| Validity | Small $\alpha$ approximations | All $\alpha \in (-1,1)$ for momentum algorithms |
| Practical interpretation | Average behavior | Holds w.p.1 for any single realization |

## Application to Momentum LMS

For MLMS with momentum factor $\alpha$, the ODE becomes $\dot{w} = \beta(P - Rw)$ where $\beta = 1/(1-\alpha)$. This reveals:

- $\beta$ acts as a convergence rate multiplier relative to LMS
- The asymptotic covariance scales as $\mu\beta\Sigma$, directly linking momentum to misadjustment
- As $\alpha \to 1$, $\beta \to \infty$ causing both infinite convergence speed and unbounded variance

## Related Concepts

- [[concepts/momentum-lms|Momentum LMS]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]
- [[concepts/kalman-filter|Kalman Filter]]

## Related Sources

- [[sources/sharma-1998-momentum-adaptive-filtering|Sharma, Sethares & Bucklew 1998: Analysis of Momentum Adaptive Filtering Algorithms]]
