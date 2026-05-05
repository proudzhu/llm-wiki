---
type: source
created: 2026-05-03
updated: 2026-05-03
sources:
  - raw/papers/jin-2026-momentum-lms-nonstationarity/full-text.md
  - https://doi.org/10.48550/arXiv.2602.11995
  - zotero://select/items/0_2APS3GHC
tags:
  - adaptive-filtering
  - online-learning
  - momentum
  - nonstationarity
  - tracking
  - regret
---

# Jin, Zheng & Guo 2026: Momentum LMS Theory beyond Stationarity

**Authors**: [[../entities/yifei-jin|Yifei Jin]], [[../entities/xin-zheng|Xin Zheng]], [[../entities/lei-guo|Lei Guo]]

**Affiliation**: Academy of Mathematics and Systems Science, Chinese Academy of Sciences; University of Chinese Academy of Sciences, Beijing, China

**Venue**: arXiv preprint, 2026 (arXiv:2602.11995)

**Type**: Preprint

**DOI**: [10.48550/arXiv.2602.11995](https://doi.org/10.48550/arXiv.2602.11995)

**Zotero**: [2APS3GHC](zotero://select/items/0_2APS3GHC)

## Summary

This paper establishes rigorous tracking performance and regret bounds for the Momentum Least Mean Squares (MLMS) algorithm in time-varying stochastic linear systems under general nonstationary conditions. By augmenting the error state to convert a second-order random vector difference equation into a first-order system, the authors overcome the fundamental analytical barrier that distinguishes MLMS from classical LMS, where stability analysis involves products of more complicated random matrices.

## Problem Formulation

Consider the time-varying linear regression model:

$$y_{k+1} = \varphi_k^\top \theta_k + v_{k+1}, \quad k = 0, 1, 2, \ldots$$

where $\theta_k \in \mathbb{R}^m$ is the unknown time-varying parameter, $y_{k+1} \in \mathbb{R}$ is the output, $\varphi_k \in \mathbb{R}^m$ is the stochastic regressor, and $v_{k+1} \in \mathbb{R}$ is the noise.

The parameter-variation process is $\Delta_k = \theta_k - \theta_{k-1}$.

### Key Assumption: Conditional Excitation (Assumption 1)

The stochastic regressor $\{\varphi_k, \mathcal{F}_k\}$ is adapted, and there exist $\alpha > 0$ and integer $h > 0$ such that:

$$\mathbb{E}\left[\sum_{i=kh+1}^{(k+1)h} \frac{\varphi_i \varphi_i^\top}{1 + \|\varphi_i\|^2} \;\middle|\; \mathscr{F}_{kh}\right] \geq \alpha I > 0, \quad \text{a.s.}$$

This is more general than deterministic PE conditions — it does not require independence or stationarity and includes signals from stochastic systems with feedback.

## Methodology

### MLMS Algorithm (Algorithm 1)

The MLMS augments normalized LMS with a Polyak heavy-ball momentum term:

$$\alpha_k = \frac{\mu}{\delta + \|\varphi_k\|^2}$$

$$\hat{y}_{k+1} = \varphi_k^\top \hat{\theta}_k$$

$$e_k = y_{k+1} - \hat{y}_{k+1}$$

$$\hat{\theta}_{k+1} = \hat{\theta}_k + \alpha_k e_k \varphi_k + \beta(\hat{\theta}_k - \hat{\theta}_{k-1})$$

where $\beta = C_\beta \mu^\kappa$ with $C_\beta \in (0, 1]$ and $\kappa > 1$.

### State-Space Error Dynamics

The parameter estimation error $\tilde{\theta}_k = \theta_k - \hat{\theta}_k$ satisfies a second-order recursion. By stacking successive errors and applying a scaled transformation $P = \text{diag}[I, \mu I]$, the error dynamics become:

$$Z_{k+1} = (I_0 - \bar{A}_k) Z_k + \begin{pmatrix} \tau_k \\ \mathbf{0} \end{pmatrix}$$

where $I_0 = \begin{pmatrix} I & \mathbf{0} \\ \mathbf{0} & \mathbf{0} \end{pmatrix}$ and $\bar{A}_k = \begin{pmatrix} A_k & \mu I \\ -\mu I & \mathbf{0} \end{pmatrix}$.

This is fundamentally different from LMS analysis because $I_0$ is not the identity and $\bar{A}_k$ is not symmetric.

### Projection-Based MLMS

For prediction analysis without excitation conditions, a projection operator $\pi_\mathcal{D}(\cdot)$ constrains estimates to a known compact set:

$$\hat{\theta}_{k+1} = \pi_\mathcal{D}\left[\hat{\theta}_k + \alpha_k e_k \varphi_k + \beta(\hat{\theta}_k - \hat{\theta}_{k-1})\right]$$

## Main Theoretical Results

### Exponential Stability (Theorem 4)

Under Assumption 1, for any integer $p \geq 1$:

$$\left\|\prod_{k=ih+1}^{jh+1} (I_0 - \bar{A}_k)\right\|_p \leq \lambda_p^{j-i}, \quad j \geq i \geq 0$$

where $\lambda_p = \left(1 - \frac{\alpha\mu}{8}\right)^{1/p} \in (0,1)$ and $\mu$ satisfies a bound depending on $h$, $p$, and $\alpha$.

### Tracking Performance: Bounded Case (Theorem 8)

Under bounded noises and parameter variations ($\sigma = \sup_k \|v_k\|_{2p}$, $\nu = \sup_k \|\Delta_k\|_{2p}$):

$$\|\tilde{\theta}_{k+1}\|_p = O\left(\lambda_{2p}^{\lfloor k/h \rfloor} \|\tilde{\theta}_0\|_{2p}\right) + O\left(\frac{\nu}{\mu} + \sigma\right)$$

The first term decays exponentially; the asymptotic tracking error is small when $\nu$ and $\sigma$ are small.

### Tracking Performance: Zero-Mean Random Case (Theorem 10)

Under zero-mean random parameter variations and noises in the class $\mathcal{M}_{2p}$:

$$\|\tilde{\theta}_{k+1}\|_p = O\left(\lambda_{2p}^{\lfloor k/h \rfloor} \|\tilde{\theta}_0\|_{2p}\right) + O\left(\frac{c_{2p}^\Delta}{\sqrt{\mu}} + c_{2p}^v \sqrt{\mu}\right)$$

This exhibits the familiar **tracking–noise tradeoff**: small $\mu$ improves noise sensitivity but degrades tracking ability, and vice versa.

### Prediction Regret (Theorem 14)

Under the projection-based MLMS with no excitation conditions:

$$\limsup_{n_2 - n_1 \to \infty} \frac{1}{n_2 - n_1} \sum_{k=n_1+1}^{n_2} (y_k - \hat{y}_k)^2 \leq (1 + \mu)\sigma_v^2 + O\left(\mu^{\kappa-1} + \mu^\kappa \sigma_v + \frac{\xi}{\mu}\right)$$

For constant parameters ($\xi = 0$), the averaged prediction error approaches $\sigma_v^2$ as $\mu \to 0$.

## Experimental Setup

| Experiment | Data | Model | Metrics | Compared Methods |
|-----------|------|-------|---------|-----------------|
| Synthetic jumping parameters | 6D linear stochastic system with abrupt parameter jumps every 100 steps | MLMS ($\mu=0.1$, $\delta=0.1$, $\beta=0.099$) | Tracking MSE (dB) | SGD, SGD-Momentum, LMS, MLMS |
| Speech enhancement | NOIZEUS corpus, airport noise, 30 utterances | 50-tap adaptive filter, MLMS ($\mu=0.25$, $\delta=10^{-12}$, $\beta=0.15$) | SNR improvement (dB) | SGD, SGD-Momentum, RLS, GNGD, LMS, MLMS |

## Results

### Synthetic Data

Algorithms with momentum respond more rapidly to abrupt parameter jumps and exhibit faster re-convergence. MLMS achieves the lowest tracking MSE among all methods.

### Speech Enhancement (SNR Improvement in dB)

| Filter | 5 dB | 10 dB | 15 dB |
|--------|------|-------|-------|
| SGD | 7.72 ± 1.47 | 6.39 ± 3.38 | 4.94 ± 7.38 |
| SGD-M | 7.74 ± 1.61 | 6.42 ± 4.09 | 4.91 ± 10.58 |
| RLS | 3.92 ± 2.75 | 2.84 ± 6.70 | 3.08 ± 15.31 |
| GNGD | 6.44 ± 1.32 | 5.14 ± 3.00 | 3.76 ± 7.43 |
| LMS | 7.86 ± 1.52 | 6.79 ± 3.29 | 5.69 ± 8.63 |
| **MLMS** | **7.91 ± 1.57** | **6.86 ± 3.36** | **5.79 ± 8.78** |

MLMS consistently achieves the highest SNR improvement across all noise conditions. The momentum effect on SNR peaks at approximately $\beta \approx 0.3$ and gradually decreases beyond that.

## Key Contributions

1. **Stability guarantee under general data conditions**: Establishes $L_p$-exponential stability of MLMS error dynamics under conditional excitation (Assumption 1), which does not require stationarity or independence — applicable to stochastic systems with feedback
2. **State augmentation technique**: Converts the second-order MLMS error recursion into a first-order system via stacking and scaled transformation, overcoming the fundamental analytical barrier where $I_0$ is not identity and $\bar{A}_k$ is not symmetric
3. **Tracking performance bounds**: Derives two tracking error bounds — crude bound for bounded disturbances (Theorem 8) and refined bound for zero-mean random processes (Theorem 10) exhibiting the tracking–noise tradeoff
4. **Prediction regret without excitation**: Establishes averaged prediction error bounds for projection-based MLMS without any excitation conditions (Theorem 14), with the bound approaching $\sigma_v^2$ for constant parameters
5. **Empirical validation**: Demonstrates MLMS superiority on synthetic jumping-parameter systems and real-world speech enhancement (NOIZEUS corpus), consistently outperforming SGD, SGD-Momentum, RLS, GNGD, and LMS

## Related Concepts

- [[../concepts/momentum-lms|Moment LMS]]
- [[../concepts/adaptive-filtering|Adaptive Filtering]]
- [[../concepts/variable-step-size-lms|Variable Step Size LMS]]
- [[../concepts/robust-adaptive-filtering|Robust Adaptive Filtering]]
- [[../concepts/online-learning|Online Learning]]
- [[../concepts/kalman-filter|Kalman Filter]]

## Related Sources

- [[../sources/akhtar-2006-vss-lms-online-spm|Akhtar 2006: VSS LMS for Online SPM]]
- [[../sources/chen-2016-generalized-correntropy-robust-adaptive-filtering|Chen 2016: Generalized Correntropy for Robust Adaptive Filtering]]
