---
type: source
created: 2026-04-12
updated: 2026-04-28
sources:
tags:
- correntropy
- generalized-gaussian
- generalized-maximum-correntropy-criterion
- non-gaussian
- robust-adaptive-filtering
aliases:
- 'Chen 2016: Generalized Correntropy for Robust Adaptive Filtering'
---

# Chen 2016: Generalized Correntropy for Robust Adaptive Filtering

**Authors**: [[../entities/badong-chen|Badong Chen]], [[../entities/lei-xing|Lei Xing]], [[../entities/haiquan-zhao|Haiquan Zhao]], [[../entities/nanning-zheng|Nanning Zheng]], [[../entities/jose-c-principe|José C. Príncipe]]
**Published**: IEEE Transactions on Signal Processing, Vol. 64, No. 13, pp. 3376–3387, July 2016
**DOI**: [10.1109/TSP.2016.2539127](https://doi.org/10.1109/TSP.2016.2539127)
**📎 Zotero**: [zotero://select/items/0_HEYN2NCY](zotero://select/items/0_HEYN2NCY)

## Summary

Proposes **generalized correntropy** using the generalized Gaussian density (GGD) as the kernel function, extending the standard correntropy (which uses only Gaussian kernel). The resulting **Generalized Maximum Correntropy Criterion (GMCC)** yields a highly stable adaptive filtering algorithm with zero probability of divergence (POD), robust to both light-tailed and heavy-tailed non-Gaussian noises.

## Motivation

Standard correntropy uses a Gaussian kernel, which is not always optimal. Adaptive filter cost functions need to handle both light-tailed and heavy-tailed non-Gaussian noise:

| Non-Gaussian Type | Examples | Suitable Statistic | Representative Algorithm |
|-------------------|----------|-------------------|-------------------------|
| Light-tailed | Uniform, binary | Higher-order statistics (HOS) | LMF |
| Heavy-tailed | Laplace, α-stable | Lower-order statistics (LOS) | Sign Algorithm, MCC |

Core idea: replace the Gaussian kernel with the Generalized Gaussian Density (GGD).

## Key Takeaways

### 1. Generalized Correntropy Definition

Standard correntropy uses a Gaussian kernel:

$$V(X,Y) = \mathbb{E}[G_\sigma(e)] = \mathbb{E}\left[\frac{1}{\sqrt{2\pi}\sigma} \exp\left(-\frac{e^2}{2\sigma^2}\right)\right]$$

where $e = X - Y$. The **generalized correntropy** replaces the Gaussian with the GGD:

$$V_{\alpha,\beta}(X,Y) = \mathbb{E}[G_{\alpha,\beta}(e)] = \mathbb{E}[\gamma_{\alpha,\beta} \exp(-\lambda|e|^\alpha)]$$

where:
- **α > 0**: shape parameter (α = 2 → Gaussian, α = 1 → Laplace, α → ∞ → uniform)
- **β > 0**: scale (bandwidth) parameter
- **λ = 1/β^α**: kernel parameter
- **γ_{α,β} = α/(2βΓ(1/α))**: normalization constant

Sample estimator:

$$\hat{V}_{\alpha,\beta}(X,Y) = \frac{1}{N} \sum_{i=1}^N G_{\alpha,\beta}(x_i - y_i)$$

### 2. Generalized Correntropic Loss (GC-loss)

$$J_{GC-loss}(X,Y) = G_{\alpha,\beta}(0) - V_{\alpha,\beta}(X,Y) = \gamma_{\alpha,\beta} - \frac{1}{N} \sum_{i=1}^N G_{\alpha,\beta}(e_i)$$

Minimizing GC-loss ≡ maximizing generalized correntropy.

For 0 < α ≤ 2, GC-loss equals mean-square loss in the feature space induced by the Mercer kernel.

### 3. GCIM: Generalized Correntropy Induced Metric

The GCIM behaves like **different norms in different regions**:

| Parameter Limit | GCIM Approaches |
|----------------|-----------------|
| λ → 0⁺ (large bandwidth) | **L_α norm** |
| λ → ∞ (small bandwidth) | **L_0 norm** |

### 4. GMCC Estimation Properties

The GMCC estimator has three important limiting behaviors:

| Limit | GMCC becomes | Intuition |
|-------|-------------|-----------|
| β → 0⁺ (λ → ∞) | **MAP estimation** | Kernel → δ, take posterior mode |
| β → ∞ (λ → 0⁺) | **LMP estimation** with p = α | Flat kernel, reduces to least mean p-power |
| α = 2, λ → 0⁺ | **Wiener solution** (MSE/LMS) | Returns to classical minimum mean square |

**Key theorem**: The GMCC estimator is a **smoothed MAP estimate**:

$$g_{GMCC}(y) = \arg\max_x \rho_{\alpha,\beta}(x|y)$$

where $\rho_{\alpha,\beta}(x|y) = G_{\alpha,\beta}(x) * p_{X|Y}(x|y)$ is the smoothed posterior PDF.

**Error concentration interpretation**: A good estimate should make the error distribution form a sharp peak around zero.

### 5. Optimal Solution

Under GMCC, the optimal weight vector has a Wiener-like form but with error-dependent weighting:

$$W_{opt} = [R_{XX}^h]^{-1} P_{dX}^h$$

where:
- **$R_{XX}^h = \mathbb{E}[h(e(i)) X(i) X(i)^T]$**: weighted autocorrelation matrix
- **$P_{dX}^h = \mathbb{E}[h(e(i)) d(i) X(i)]$**: weighted cross-correlation vector
- **$h(e) = \exp(-\lambda|e|^\alpha) |e|^{\alpha-2}$**: error nonlinearity (weighting function)

When x(i) and d(i) are zero-mean Gaussian, W_opt equals the **Wiener solution**.

### 6. GMCC Adaptive Algorithm

Stochastic gradient descent on the GMCC cost:

$$W(i+1) = W(i) + \eta \cdot \exp(-\lambda|e(i)|^\alpha) \cdot |e(i)|^{\alpha-1} \cdot \text{sign}(e(i)) \cdot X(i)$$

Equivalently:

$$W(i+1) = W(i) + \eta(i) \cdot e(i) \cdot X(i)$$

where the **variable step size** is:

$$\eta(i) = \eta \cdot \exp(-\lambda|e(i)|^\alpha) \cdot |e(i)|^{\alpha-2}$$

**Key insight**: Large error → exponentially decaying step size → outliers are suppressed.

### 7. Special Cases

| α value | Algorithm |
|---------|-----------|
| α = 2 | **MCC** (maximum correntropy criterion, Gaussian kernel) |
| α = 2, λ → 0 | **LMS** (least mean squares) |
| α = 1 | **Sign algorithm** (robust to outliers) |
| α → 0⁺ | Approaches **L_0** minimization (sparse) |
| λ → 0 (any α) | **LMP** (least mean p-power, p = α) |

### 8. Zero Probability of Divergence (POD)

**Why LMF diverges**: LMF update contains $|e(i)|^3$ term, large errors amplify step size, can become unstable.

**Why GMCC doesn't diverge**: The weighting function $h(e) = \exp(-\lambda|e|^\alpha) \cdot |e|^{\alpha-2}$ **decays exponentially** for large errors. Unlike LMP algorithms (which can diverge depending on input/noise power and initial weights), the GMCC step size $\eta(i) \to 0$ for large $|e(i)|$. This means large outliers (impulsive noise) cause **vanishing updates** rather than catastrophic weight changes.

**Experimental verification** (1000 Monte Carlo runs):

| Algorithm | POD (as step size increases) |
|-----------|------------------------------|
| LMF (α=4) | 0 → ~12% |
| **GMCC (α=4)** | **Always 0** |

### 9. Steady-State Performance

The steady-state excess mean square error (EMSE) of GMCC:

$$S = \frac{\eta \cdot \text{Tr}(R_{XX}) \cdot \mathbb{E}[f^2(v)]}{2\mathbb{E}[f'(v)] - \eta \cdot \text{Tr}(R_{XX}) \cdot \mathbb{E}[\zeta(v)]}$$

where $f(e) = \exp(-\lambda|e|^\alpha) \cdot |e|^{\alpha-1} \cdot \text{sign}(e)$.

Small step size approximation:

$$S \approx \frac{\eta \cdot \text{Tr}(R_{XX}) \cdot \mathbb{E}[\exp(-2\lambda|v|^\alpha) |v|^{2\alpha-2}]}{2\mathbb{E}[\exp(-\lambda|v|^\alpha) |v|^{\alpha-2} ((\alpha-1) - \lambda\alpha |v|^\alpha)]}$$

### 10. System Comparison

| Algorithm | Cost Function | Divergence Risk | Impulsive Noise Robustness |
|-----------|--------------|-----------------|---------------------------|
| LMS | MSE | Zero (Gaussian input) | Poor |
| LMP (p=α) | $\mathbb{E}[|e|^\alpha]$ | **Non-zero** (LMF severe) | Moderate |
| Sign Algorithm | $\mathbb{E}[|e|]$ | Zero | Good |
| MCC | $\mathbb{E}[\exp(-\lambda e^2)]$ | Zero | Good |
| **GMCC** | $\mathbb{E}[\exp(-\lambda|e|^\alpha)]$ | **Zero** | **Controllable (via α)** |

### 11. Design Intuition for α

| α | Applicable Scenario |
|---|---------------------|
| α = 2 | Moderate non-Gaussian, general impulsive noise |
| α = 1 | Strong impulsive noise, heavy-tailed interference |
| 1 < α < 2 | Mixed light-tailed + heavy-tailed |
| α > 2 | Light-tailed non-Gaussian (e.g., uniform noise) |

### 12. Computational Complexity

Nearly identical to LMP. The only extra cost is computing $\exp(-\lambda|e(i)|^\alpha)$, which is very cheap on modern processors.

## Key Equations

| Description | Equation |
|-------------|----------|
| Generalized correntropy | $V_{\alpha,\beta}(X,Y) = \mathbb{E}[\gamma_{\alpha,\beta} \exp(-\lambda|X-Y|^\alpha)]$ |
| GC-loss | $J_{GC-loss} = \gamma_{\alpha,\beta} - \frac{1}{N} \sum G_{\alpha,\beta}(e_i)$ |
| GMCC cost | $J_{GMCC} = \mathbb{E}[G_{\alpha,\beta}(e(i))] = \gamma_{\alpha,\beta} \mathbb{E}[\exp(-\lambda|e(i)|^\alpha)]$ |
| Optimal weights | $W_{opt} = [R_{XX}^h]^{-1} P_{dX}^h$ |
| GMCC update | $W(i+1) = W(i) + \eta \cdot \exp(-\lambda|e(i)|^\alpha) \cdot |e(i)|^{\alpha-1} \cdot \text{sign}(e(i)) \cdot X(i)$ |
| Variable step size | $\eta(i) = \eta \cdot \exp(-\lambda|e(i)|^\alpha) \cdot |e(i)|^{\alpha-2}$ |
| Weighting function | $h(e) = \exp(-\lambda|e|^\alpha) \cdot |e|^{\alpha-2}$ |

## Limitations and Open Questions

1. **Complete POD analysis**: Only proven for scalar noiseless case; vector + noise case remains open
2. **Steady-state EMSE applicability**: Taylor expansion assumes a priori error is small, less accurate for large step sizes
3. **Parameter selection**: Optimal α and λ depend on noise distribution prior
4. **Nonlinear extensions**: Kernel methods (Kernel GMCC) or neural network extensions worth exploring

## Q&A

**Q1: Why can GGD kernel be used as optimization cost even when it's not always a Mercer kernel?**

Mercer kernel necessary and sufficient condition is 0 < α ≤ 2. When α > 2 the kernel may not be positive definite, but the optimization cost function doesn't require positive definiteness — only monotonic differentiability. GMCC remains valid for α > 2.

**Q2: What is the essential difference between GMCC and LMP?**

They differ only by an exponential weighting term:

$$\text{LMP}: \Delta W = \eta |e|^{\alpha-1} \text{sign}(e) X$$
$$\text{GMCC}: \Delta W = \eta \exp(-\lambda|e|^\alpha) |e|^{\alpha-1} \text{sign}(e) X$$

LMP's power-law growth $|e|^{\alpha-1}$ becomes unstable for large errors, while GMCC's exponential decay $\exp(-\lambda|e|^\alpha)$ suppresses it → zero POD.

**Q3: What advantage does GMCC have over FXLMS in ANC applications?**

FXLMS degrades severely under impulsive noise (large error × fixed step size → destroys filter). GMCC's variable step size automatically attenuates during impulse interference, providing intrinsic robustness.

## Related Concepts

- [[../concepts/correntropy|Correntropy]]
- [[../concepts/generalized-correntropy|Generalized Correntropy]]
- [[../concepts/maximum-correntropy-criterion|Maximum Correntropy Criterion]]
- [[../concepts/robust-adaptive-filtering|Robust Adaptive Filtering]]
- [[../concepts/generalized-gaussian-distribution|Generalized Gaussian Distribution]]
- [[../concepts/active-noise-control|Active Noise Control]] — GMCC can be applied to ANC in impulsive noise environments
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — GMCC as a robust alternative to FXLMS

## Related Entities

- [[../entities/badong-chen|Badong Chen]] — First author, Xi'an Jiaotong University
- [[../entities/haiquan-zhao|Haiquan Zhao]] — Co-author, Southwest Jiaotong University (also appears in ANC literature)
- [[../entities/jose-c-principe|José C. Príncipe]] — Co-author, University of Florida, pioneer of correntropy theory

## Related Synthesis
