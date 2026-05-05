---
type: concept
created: 2026-05-03
updated: 2026-05-03
sources:
  - raw/papers/jin-2026-momentum-lms-nonstationarity/full-text.md
  - raw/papers/sharma-1998-momentum-adaptive-filtering/full-text.md
tags:
  - adaptive-filtering
  - momentum
  - online-learning
  - tracking
---

# Momentum LMS

**Momentum Least Mean Squares (MLMS)** is an adaptive filtering algorithm that augments the LMS update with a momentum term, enabling faster convergence and improved tracking of time-varying parameters. The classical MLMS recursion (Proakis 1974) is:

$$W_{k+1} = W_k + \mu(D_k - W_k^T X_k)X_k + \alpha(W_k - W_{k-1})$$

where $\alpha \in (-1,1)$ is the momentum factor. The momentum term adds an exponentially decaying memory of past update directions, low-pass filtering the weight updates to resist erratic changes caused by gradient noise while accelerating motion along consistent update directions.

## Key Distinction from LMS

While LMS error dynamics lead to a first-order random vector difference equation, MLMS introduces an additional dynamical state due to momentum, resulting in a **second-order** time-varying random vector difference equation. The stability analysis hinges on products of more complicated random matrices.

### State Augmentation

By stacking successive error vectors and applying a scaled transformation $P = \text{diag}[I, \mu I]$, the error dynamics become:

$$Z_{k+1} = (I_0 - \bar{A}_k) Z_k + \begin{pmatrix} \tau_k \\ \mathbf{0} \end{pmatrix}$$

where $I_0 = \begin{pmatrix} I & \mathbf{0} \\ \mathbf{0} & \mathbf{0} \end{pmatrix}$ and $\bar{A}_k = \begin{pmatrix} A_k & \mu I \\ -\mu I & \mathbf{0} \end{pmatrix}$.

This is fundamentally different from LMS because $I_0$ is not the identity matrix and $\bar{A}_k$ is not symmetric.

## Asymptotic Analysis (Sharma, Sethares & Bucklew 1998)

Using weak convergence theory without Gaussian or independence assumptions on the input, the MLMS dynamics converge to the ODE $\dot{w} = \beta(P - Rw)$ where $\beta = 1/(1-\alpha)$:

- **Almost sure convergence**: $W_k \to W^*$ w.p.1 for all $\alpha \in (-1,1)$
- **Convergence rate**: $\alpha > 0$ accelerates convergence by factor $\beta > 1$; $\alpha < 0$ decelerates it
- **Asymptotic distribution**: $W_k$ is Gaussian with mean $W^*$ and covariance $\mu\beta\Sigma$
- **Misadjustment tradeoff**: The $\beta$ factor scales both convergence speed and steady-state variance — setting $\mu_{\text{MLMS}} = (1-\alpha)\mu_{\text{LMS}}$ yields identical misadjustment and convergence rate as LMS
- **Instability**: As $\alpha \to 1$, $\beta \to \infty$ causing unbounded variance

The analysis extends to other momentum algorithms (e.g., sign-sign with momentum) via the general form $W_{k+1} = \alpha_0 W_k + \mu H(W_k, Y_k, U_{k+1})$.

## Theoretical Guarantees (Jin, Zheng & Guo 2026)

### Exponential Stability

Under conditional excitation (Assumption 1), the homogeneous system $Z_{k+1} = (I_0 - \bar{A}_k)Z_k$ is $L_p$-exponentially stable:

$$\left\|\prod_{k=ih+1}^{jh+1} (I_0 - \bar{A}_k)\right\|_p \leq \lambda_p^{j-i}, \quad \lambda_p = \left(1 - \frac{\alpha\mu}{8}\right)^{1/p} \in (0,1)$$

### Tracking Bounds

| Condition | Tracking Error Bound |
|-----------|---------------------|
| Bounded disturbances ($\sigma, \nu$) | $O(\nu/\mu + \sigma)$ |
| Zero-mean random ($\mathcal{M}_{2p}$) | $O(c_{2p}^\Delta / \sqrt{\mu} + c_{2p}^v \sqrt{\mu})$ |

The zero-mean case exhibits the tracking–noise tradeoff: small $\mu$ reduces noise sensitivity but degrades tracking.

### Prediction Regret

Without excitation conditions, projection-based MLMS achieves:

$$\limsup \frac{1}{n} \sum (y_k - \hat{y}_k)^2 \leq (1+\mu)\sigma_v^2 + O\left(\mu^{\kappa-1} + \mu^\kappa \sigma_v + \frac{\xi}{\mu}\right)$$

For constant parameters ($\xi = 0$), this approaches $\sigma_v^2$ as $\mu \to 0$.

## Comparison with Related Algorithms

| Algorithm | Momentum | Normalization | Tracking | Complexity |
|-----------|----------|---------------|----------|------------|
| LMS | No | No | Moderate | $O(m)$ |
| NLMS | No | Yes | Moderate | $O(m)$ |
| SGD-Momentum | Yes | No | Fast | $O(m)$ |
| **MLMS** | **Yes** | **Yes** | **Fast** | **$O(m)$** |

## Related Concepts

- [[../concepts/adaptive-filtering|Adaptive Filtering]]
- [[../concepts/variable-step-size-lms|Variable Step Size LMS]]
- [[../concepts/robust-adaptive-filtering|Robust Adaptive Filtering]]
- [[../concepts/online-learning|Online Learning]]
- [[../concepts/kalman-filter|Kalman Filter]]
- [[../concepts/asymptotic-analysis-adaptive-algorithms|Asymptotic Analysis of Adaptive Algorithms]]

## Related Sources

- [[../sources/sharma-1998-momentum-adaptive-filtering|Sharma, Sethares & Bucklew 1998: Analysis of Momentum Adaptive Filtering Algorithms]]
- [[../sources/jin-2026-momentum-lms-nonstationarity|Jin, Zheng & Guo 2026: Momentum LMS Theory beyond Stationarity]]
