---
type: synthesis
created: 2026-04-12
updated: 2026-04-29
sources:
- zotero://select/items/0_QKJ2PV93
- zotero://select/items/0_FV5SBLPI
- zotero://select/items/0_XIBFSW3Y
- zotero://select/items/0_NCKN38JM
- zotero://select/items/0_XAZIKCJU
- zotero://select/items/0_LJDPCZ9G
- zotero://select/items/0_3AHG6GXW
- zotero://select/items/0_64FSB2AU
tags:
- filtered-x-lms-algorithm
- fxlms-f
- impulsive-noise
- stable-distribution
- versoria
- correntropy
- generalized-maximum-correntropy-criterion
- information-theoretic-learning
- robust-filtering
- adaptive-filtering
- robust-control
aliases:
- Robust ANC: From Correntropy to GMCC
- Robust ANC: Impulsive and Non-Stationary Environments
---

# Robust ANC for Impulsive and Non-Gaussian Noise

> Cross-source synthesis connecting: Liu & Lei (2024) impulsive noise review, Zeb & Mirza (2017) FxRLS for impulsive noise, Huang et al. (2017) Maximum Versoria Criterion, Tian & Feng (2026) modified Versoria VSS-LMS, Chen (2016) Generalized Correntropy, Zhu (2020) FxGMCC for ANC, and recent AI-driven robust control strategies.

---

## The Problem: When Noise Isn't Gaussian

Standard FxLMS assumes the noise follows a Gaussian (or at least finite-variance) distribution. This assumption breaks catastrophically under **impulsive noise**:

- **Machinery faults**: Bearing impacts, gear meshing
- **Rain on vehicles**: Random droplet impacts on surfaces
- **HVAC clicks**: Relay switching, compressor startup
- **Wind gusts on microphones**: Turbulent pressure spikes
- **Speech bursts**: Sudden loud speech in conversation environments

### Why FxLMS Fails

The FxLMS cost function is $J = E[e^2(n)]$. Under impulsive noise:

1. **Outliers dominate**: A single impulse with amplitude $100\times$ normal noise contributes $10,000\times$ to the cost
2. **Coefficient divergence**: The filter update $\Delta w = \mu \cdot e(n) \cdot x_f(n)$ sends coefficients flying
3. **Instability**: The algorithm may never recover — each impulse pushes it further from optimal

### Characterizing Impulsive Noise

**Alpha-stable distributions** are the standard model:
$$f(x; \alpha, \beta, \gamma, \delta)$$

where $\alpha \in (0, 2]$ is the **characteristic exponent**:
- $\alpha = 2$: Gaussian (finite variance)
- $1 < \alpha < 2$: Impulsive (infinite variance, finite mean)
- $0 < \alpha \leq 1$: Highly impulsive (infinite mean)

The key property: **heavy tails** that decay as $|x|^{-(\alpha+1)}$ rather than $e^{-x^2}$ (Gaussian).

---

## Approach 1: FxLMS/F — Least Mean Square/Fourth

### The Idea

Replace the squared error cost with a **mixed** cost function:
$$J = E[|e(n)|^p]$$

where $p$ is the norm order:
- $p = 2$: Standard FxLMS (optimal for Gaussian)
- $p = 4$: Least Mean Fourth (robust to impulses)
- $p \in (2, 4)$: Mixed, balances convergence and robustness

### FxLMS/F Algorithm

The update becomes:
$$w(n+1) = w(n) + \mu \cdot |e(n)|^{p-1} \cdot \text{sgn}(e(n)) \cdot x_f(n)$$

For $p = 4$:
$$w(n+1) = w(n) + \mu \cdot e^3(n) \cdot x_f(n)$$

**Paradox**: $e^3$ seems worse than $e$ for outliers! But the key insight from Liu & Lei (2024) is that **FxLMS/F is combined with a variable step size** that decreases when $|e(n)|$ is large:

$$\mu(n) = \frac{\mu_0}{1 + |e(n)|^2}$$

This gives the effective update:
$$w(n+1) = w(n) + \frac{\mu_0 \cdot e^3(n)}{1 + e^2(n)} \cdot x_f(n)$$

For large $e$: $\frac{e^3}{1+e^2} \approx e$ → bounded growth
For small $e$: $\frac{e^3}{1+e^2} \approx e^3$ → fast convergence near optimum

### Performance

| Algorithm | Gaussian NR | Impulsive NR ($\alpha=1.5$) | Stability |
|-----------|------------|---------------------------|-----------|
| FxLMS | 20 dB | **Diverges** | Unstable |
| FxLMS/F ($p=4$) | 18 dB | 14 dB | Stable |
| FxLMS/F (VSS) | 19 dB | 16 dB | Stable |

---

## Approach 2: FxRLS for Impulsive Noise

### Zeb & Mirza (2017)

**FxRLS** (Filtered-x Recursive Least Squares) converges faster than FxLMS but is even **more sensitive** to impulses because it minimizes a weighted sum of squared errors.

**Solution**: Combine FxRLS with **clipping** or **M-estimation**:

**Clipped FxRLS**:
$$e_{clip}(n) = \begin{cases} e(n) & |e(n)| \leq T \\ T \cdot \text{sgn}(e(n)) & |e(n)| > T \end{cases}$$

where $T$ is a threshold (typically $3-5 \times$ the estimated noise standard deviation).

**Performance improvement**:
| Algorithm | Convergence (iterations) | Impulsive NR | Complexity |
|-----------|------------------------|-------------|------------|
| FxLMS | 500 | Diverges | $O(L)$ |
| FxRLS | 50 | Diverges | $O(L^2)$ |
| Clipped FxRLS | 50 | 18 dB | $O(L^2)$ |

**Limitation**: Threshold $T$ must be tuned manually and depends on the impulsive noise statistics.

---

## Approach 3: Correntropy → MCC → GMCC

### What is Correntropy?

Chen (2016) introduces **correntropy** as a nonlinear similarity measure:
$$V_\sigma(X, Y) = E[\kappa_\sigma(X - Y)]$$

where $\kappa_\sigma(\cdot)$ is a **kernel function**. The default is the Gaussian kernel:
$$\kappa_\sigma(x) = \frac{1}{\sqrt{2\pi}\sigma} e^{-x^2 / (2\sigma^2)}$$

The Gaussian kernel **saturates** for large errors:
- Small error ($e \approx 0$): $\kappa_\sigma(e) \approx 1$ → full learning
- Large error ($e \gg \sigma$): $\kappa_\sigma(e) \approx 0$ → ignore the impulse

This provides **automatic outlier rejection** without any threshold or detection mechanism.

### Maximum Correntropy Criterion (MCC)

The MCC replaces MSE with correntropy:
$$J_{\text{MCC}} = \max E[\kappa_\sigma(e(n))]$$

The resulting adaptive algorithm uses a **score function** that replaces the linear error $e(n)$ with a **bounded** function:
$$w(n+1) = w(n) + \mu \cdot f_\sigma(e(n)) \cdot x_f(n)$$

where for Gaussian kernel MCC:
$$f_\sigma(e) = e \cdot e^{-e^2 / (2\sigma^2)}$$

This score function has the critical property: $\lim_{|e|\to\infty} f_\sigma(e) = 0$. Large errors are **down-weighted to zero** rather than amplified.

### Generalized Correntropy (GGD Kernel)

The standard Gaussian kernel has a **fixed** shape. Chen (2016) introduces the Generalized Gaussian Distribution as the kernel:
$$\kappa_{\alpha,\beta}(x) = \frac{\beta}{2\alpha\Gamma(1/\beta)} e^{-(|x|/\alpha)^\beta}$$

where:
- $\alpha > 0$: scale parameter
- $0 < \beta \leq 2$: shape parameter

**Key insight**: $\beta$ controls the kernel's tail behavior:
- $\beta = 2$: Gaussian kernel (light tails, MCC)
- $\beta = 1$: Laplacian kernel (heavier tails)
- $\beta \to 0$: Extremely heavy tails (for severe impulsive noise)

This gives the **Generalized Maximum Correntropy Criterion (GMCC)**:
$$J_{\text{GMCC}} = \max E[\kappa_{\alpha,\beta}(e(n))]$$

The resulting score function:
$$f_{\alpha,\beta}(e) = \text{sgn}(e) \cdot |e|^{\beta-1} \cdot e^{-(|e|/\alpha)^\beta}$$

### Limiting Cases of GMCC

| $\beta$ | Kernel | Score Function | Noise Regime |
|---------|--------|---------------|-------------|
| $\beta = 2$ | Gaussian | $e \cdot e^{-e^2/(2\alpha^2)}$ | Near-Gaussian |
| $\beta = 1$ | Laplacian | $\text{sgn}(e) \cdot e^{-|e|/\alpha}$ | Moderate impulsive |
| $\beta \to 0$ | Uniform-like | $\text{sgn}(e) \cdot e^{-1}$ | Severe impulsive |
| $\beta \to \infty$ | Rectangular | Hard thresholding | Binary outliers |

**Zero Point of Derivative (ZPD) property**: The GMCC score function has a zero crossing at a finite error magnitude, meaning errors beyond a certain threshold are **completely ignored**.

### FxGMCC Variants (Zhu 2020)

Zhu (2020) applies GMCC to ANC, creating the **Filtered-x GMCC (FxGMCC)** algorithm:

1. **FxGMCC**: Basic GMCC-based ANC — uses FxLMS structure with GMCC score function
2. **IFxGMCC**: Improved FxGMCC — adds variable step size for better convergence
3. **C-IFxGMCC**: Constrained IFxGMCC — adds coefficient constraints to prevent divergence

| Algorithm | Gaussian Noise | Impulsive Noise (GSNR = 5 dB) | Computational Cost |
|-----------|---------------|-------------------------------|-------------------|
| FxLMS | 25 dB NR | 8 dB NR (unstable) | $O(L)$ |
| FxGMCC | 23 dB NR | 18 dB NR | $O(L)$ + kernel eval |
| IFxGMCC | 24 dB NR | 20 dB NR | $O(L)$ + VSS |
| C-IFxGMCC | 24 dB NR | **22 dB NR** | $O(L)$ + VSS + constraint |

## Approach 4: Maximum Versoria Criterion (MVC)

### Huang et al. (2017)

The **Versoria function** provides a different geometric interpretation of robustness:

$$V(e) = \frac{\gamma^2}{e^2 + \gamma^2}$$

where $\gamma$ is the kernel size (analogous to $\sigma$ in correntropy).

**MVC cost function**:
$$J_{\text{MVC}} = \max E\left[\frac{\gamma^2}{e^2(n) + \gamma^2}\right]$$

The resulting adaptive update:
$$w(n+1) = w(n) + \mu \cdot \frac{2\gamma^2 e(n)}{(e^2(n) + \gamma^2)^2} \cdot x_f(n)$$

### MVC vs GMCC: Two Paths to Robustness

Both MVC and [[../concepts/generalized-maximum-correntropy-criterion|Generalized Maximum Correntropy Criterion]] provide robustness to impulsive noise, but through different mechanisms:

| Aspect | MVC | GMCC |
|--------|-----|------|
| **Kernel** | Versoria: $\frac{\gamma^2}{e^2+\gamma^2}$ | GGD: $e^{-(|e|/\alpha)^\beta}$ |
| **Score function** | $\frac{2\gamma^2 e}{(e^2+\gamma^2)^2}$ | $\text{sgn}(e)|e|^{\beta-1}e^{-(|e|/\alpha)^\beta}$ |
| **Tail behavior** | Polynomial decay ($\sim e^{-3}$) | Exponential decay ($\sim e^{-|e|^\beta}$) |
| **Robustness** | Good | Better (adjustable via $\beta$) |
| **Parameters** | 1 ($\gamma$) | 2 ($\alpha, \beta$) |
| **Computation** | Division + square | Exponential + power |

**Key insight from Tian & Feng (2026)**: The **modified Versoria** function introduces a shape parameter $\gamma$ analogous to $\beta$ in GMCC:

$$V_{\text{mod}}(e) = \left(\frac{\gamma^2}{e^2 + \gamma^2}\right)^\eta$$

where $\eta$ controls the tail behavior — making Versoria a one-parameter special case of the GMCC family.

---

## Approach 5: Variable Step Size for Impulsive Noise

### Modified Versoria VSS-LMS (Tian & Feng, 2026)

Combines VSS with Versoria robustness:

$$\mu(n) = \mu_{\max} \cdot \left(\frac{a^3}{e^2(n) + a^2}\right)^\gamma$$

where $a$ is estimated from the running average of $|e(n)|$ (not $e^2(n)$, to reduce impulse sensitivity).

**Anti-jamming design**: Using $|e(n)|$ instead of $e^2(n)$ for the power estimate prevents large impulses from corrupting the step size estimate.

---

## The AI-Driven Frontier (2025-2026)

Recent reviews highlight the shift from hand-tuned adaptive filters to AI-driven control strategies.

### Neural Noise Estimation

Instead of manually tuning the step size ($\mu$) or the kernel bandwidth ($\sigma$), modern AI-driven controllers use **Recurrent Neural Networks (RNNs)** to predict the noise statistic in real-time. This dynamic tuning enables the controller to adjust its "robustness" (the amount of clipping/kernel-weighting) based on the instantaneous impulsive energy of the environment.

### Implementation Strategy

To build a modern, robust ANC system, the current literature suggests a hybrid architectural approach:
1. **Front-end**: Use frequency-domain decomposition to minimize secondary path modeling latency.
2. **Robustness Engine**: Implement GMCC-based updates if the environment is known to have impulsive, non-stationary noise.
3. **Control Core**: Replace static filter parameters with AI-driven estimators (e.g., a learned step-size or noise-model) to handle the non-stationarity of the acoustic environment.
4. **Virtual Sensing**: If physical mic placement is constrained, employ an observer-based state-space model to project the zone of silence.

## Design Guidelines for GMCC

### Choosing $\beta$

The shape parameter $\beta$ is the single most important design choice:
- **Gaussian/mild noise**: $\beta \approx 2$ (reduces to MCC)
- **Moderate impulsive** (e.g., wind on microphones): $\beta \approx 1.0$-$1.5$
- **Severe impulsive** (e.g., mechanical impacts): $\beta \approx 0.5$-$1.0$

### Choosing $\alpha$

The scale parameter $\alpha$ sets the threshold at which errors are down-weighted:
- Rule of thumb: $\alpha \approx 2 \cdot \sigma_v$ where $\sigma_v$ is the expected noise standard deviation
- Too small: even normal errors are ignored → poor convergence
- Too large: impulses are not rejected → behaves like LMS

### When NOT to Use GMCC

- Pure Gaussian noise: standard FxLMS is optimal (no benefit from correntropy)
- Real-time systems with tight latency: kernel evaluation adds ~10-20% computation overhead
- Multi-channel ANC: the computational cost multiplies with channel count

---

## Design Decision Tree

```
Is your noise impulsive?
│
├─ No (Gaussian/mild) → Standard FxLMS
│
└─ Yes
   │
   ├─ Need fastest convergence? → Clipped FxRLS (if O(L²) acceptable)
   │
   ├─ Need simplest implementation? → FxLMS/F with VSS
   │
   ├─ Need tunable robustness? → GMCC (tune β) or C-IFxGMCC
   │
   ├─ Need minimum parameters? → MVC (tune γ only)
   │
   └─ Need dynamic adaptation? → AI-driven step-size + GMCC core
```

---

## Related Concepts

- [[../concepts/impulsive-noise|Impulsive Noise]]
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[../concepts/robust-adaptive-filtering|Robust Adaptive Filtering]]
- [[../concepts/generalized-maximum-correntropy-criterion|Generalized Maximum Correntropy Criterion]]
- [[../concepts/maximum-correntropy-criterion|Maximum Correntropy Criterion]]
- [[../concepts/correntropy|Correntropy]]
- [[../concepts/generalized-correntropy|Generalized Correntropy]]
- [[../concepts/generalized-gaussian-distribution|Generalized Gaussian Distribution]]
- [[../concepts/information-theoretic-learning|Information Theoretic Learning]]
- [[../concepts/virtual-sensing|Virtual Sensing]]
- [[../concepts/active-noise-control|Active Noise Control]]

## Related Sources
