---
type: synthesis
created: 2026-04-12
updated: 2026-04-12
sources:
- zotero://select/items/0_N8MHRKXP
- zotero://select/items/0_FERIFUEJ
tags:
- flnn
- kernel
- nonlinear-anc
- spline
- volterra
---

# Nonlinear ANC: When Linear Filters Aren't Enough

> Cross-source synthesis connecting: Zhao & Zeng (2010) FLNN for nonlinear ANC, Zhao & Chen (2023) nonlinear adaptive filters book, and Song & Zhao (2019) convex combination FxLMS/F.

---

## The Problem: Nonlinear Distortion in ANC

Standard FxLMS assumes a **linear** relationship between the reference signal and the anti-noise. This assumption breaks when:

1. **Loudspeaker nonlinearity**: Speaker distortion at high volumes creates harmonics not present in the reference
2. **Acoustic nonlinearity**: High SPL (> 110 dB) creates shock waves and harmonic generation
3. **Electronics nonlinearity**: Amplifier saturation, ADC/DAC clipping
4. **Structural nonlinearity**: Nonlinear vibration of panels, ducts

When the secondary path or primary path contains nonlinearities, a linear FxLMS controller can only cancel the **linear component** of the noise — the nonlinear distortion remains.

---

## Approach 1: Functional Link Neural Network (FLNN)

### Zhao & Zeng (2010)

**Core idea**: Replace the linear FIR filter with a **FLNN** that applies nonlinear basis functions to the input before the adaptive weights:

```
Reference x(n) ──→ Nonlinear expansion ──→ Adaptive weights ──→ Anti-noise
                      ↓
              Trigonometric expansion:
              [x, sin(πx), cos(πx), sin(2πx), cos(2πx), ...]
```

**FLNN expansion**:
$$\phi(x) = [x, \sin(\pi x), \cos(\pi x), \sin(2\pi x), \cos(2\pi x), \dots, \sin(M\pi x), \cos(M\pi x)]$$

The output:
$$y(n) = \sum_{m=1}^{2M+1} w_m \cdot \phi_m(x(n))$$

**Advantage over Volterra**: FLNN has $O(M)$ parameters vs. $O(N^P)$ for Volterra (where $P$ is the polynomial order).

**Reduced feedback variant**: Zhao & Zeng propose feeding back only a **reduced** error signal to the weight update, cutting computation by 50% with < 1 dB NR loss.

**Performance**:
| Controller | Linear noise NR | Nonlinear noise NR | Parameters |
|------------|----------------|-------------------|------------|
| FxLMS | 20 dB | 8 dB | $L$ |
| FLNN-FxLMS (M=3) | 20 dB | 15 dB | $7L$ |
| FLNN-FxLMS (M=5) | 20 dB | 17 dB | $11L$ |
| FLNN-FxLMS (reduced) | 20 dB | 16 dB | $11L$ (50% less compute) |

---

## Approach 2: Volterra Filters

### Zhao & Chen (2023) Book

The **Volterra series** is the most general nonlinear system representation:
$$y(n) = \sum_{k=1}^{P} \sum_{i_1=0}^{L-1} \cdots \sum_{i_k=0}^{L-1} h_k(i_1, \dots, i_k) \cdot x(n-i_1) \cdots x(n-i_k)$$

where $P$ is the **Volterra order** (degree of nonlinearity).

**The complexity explosion**:
| Order | Parameters | Example: $L=64$ |
|-------|-----------|-----------------|
| 1 (linear) | $L$ | 64 |
| 2 (quadratic) | $L + L(L+1)/2$ | 2,080 |
| 3 (cubic) | $L + L(L+1)/2 + L(L+1)(L+2)/6$ | 45,760 |

**Practical use**: Only 2nd-order Volterra is feasible for real-time ANC, and even then requires complexity reduction:
- **Diagonal Volterra**: Keep only diagonal terms → $O(L)$ parameters
- **Laguerre expansion**: Use orthogonal basis → fewer parameters for same accuracy
- **Subband Volterra**: Apply per subband → $O(L/S \cdot P^2)$

**Performance**: 2nd-order Volterra achieves 18-22 dB NR under moderate nonlinear distortion — but only with $O(L^2)$ complexity.

---

## Approach 3: Kernel Adaptive Filters

### Kernel Method

Map the input to a high-dimensional (possibly infinite-dimensional) **reproducing kernel Hilbert space (RKHS)**:
$$\phi: x \mapsto \mathcal{H}$$

Then apply linear adaptive filtering in $\mathcal{H}$.

**Key advantage**: The kernel trick means we never compute $\phi(x)$ explicitly — we only need the kernel function:
$$K(x, x') = \langle \phi(x), \phi(x') \rangle$$

Common kernels:
- **Gaussian**: $K(x, x') = \exp(-\|x-x'\|^2 / (2\sigma^2))$
- **Polynomial**: $K(x, x') = (x^T x' + c)^d$

**The growth problem**: Kernel filters grow with the number of samples — each new sample adds a new basis function. Solutions:
- **Novelty criterion**: Only add samples that are "novel" (distant from existing centers)
- **Budget maintenance**: Keep only $B$ centers, prune the least useful
- **Random Fourier features**: Approximate the kernel with fixed-size random features

**Performance**: Kernel FxLMS achieves 20-25 dB NR under arbitrary nonlinear distortion, but with $O(B \cdot L)$ complexity where $B$ is the budget size.

---

## Approach 4: Spline Adaptive Filters

### Zhao & Chen (2023)

**Spline filters** model nonlinearity as a cascade:
$$y(n) = \text{spline}(w^T x(n))$$

where the spline is a piecewise polynomial defined by $K$ control points.

**Advantage**: Only $L + K$ parameters (linear filter + spline knots), vs. $O(L^2)$ for Volterra.

**Adaptation**: Both the linear weights $w$ and the spline control points are adapted simultaneously using gradient descent.

**Performance**: 16-20 dB NR under smooth nonlinear distortion — less than Volterra for the same complexity, but much simpler to implement.

---

## Approach 5: Convex Combination of Linear and Nonlinear Filters

### Song & Zhao (2019)

Instead of choosing between linear and nonlinear, **combine both**:
$$y(n) = \lambda(n) \cdot y_{\text{linear}}(n) + (1-\lambda(n)) \cdot y_{\text{nonlinear}}(n)$$

where $\lambda(n) \in [0, 1]$ adapts automatically:

$$\lambda(n) = \frac{1}{1 + e^{-a(n)}}$$
$$a(n+1) = a(n) + \mu_a \cdot e(n) \cdot (y_{\text{linear}}(n) - y_{\text{nonlinear}}(n)) \cdot x_f^T(n) \cdot w(n)$$

**Why this works**:
- When the system is linear: $\lambda \to 1$ (linear filter dominates, minimal overhead)
- When nonlinearity appears: $\lambda \to 0$ (nonlinear filter takes over)
- Smooth transition: no abrupt switching artifacts

**Computational advantage**: The nonlinear filter runs in the background and only contributes when needed — the effective complexity is close to $O(L)$ most of the time.

---

## Comparison: When to Use Which

| Scenario | Recommended | Why | Complexity |
|----------|------------|-----|-----------|
| **Mild speaker distortion** | FLNN (M=2-3) | Simple, captures harmonic distortion | $O(5L)$ |
| **Severe nonlinear distortion** | Kernel FxLMS (budget $B$) | Universal approximation | $O(B \cdot L)$ |
| **Smooth nonlinearity** | Spline FxLMS | Few parameters, stable | $O(L + K)$ |
| **Unknown/mixed nonlinearity** | Convex combination (linear + nonlinear) | Automatic switching | $O(L) + O(\text{nonlinear})$ |
| **Polynomial nonlinearity known** | Diagonal Volterra (2nd order) | Matches the distortion model | $O(L)$ |
| **Maximum performance, no constraint** | Full Volterra (2nd order) | Optimal for polynomial distortion | $O(L^2)$ |

---

## The Nonlinearity Detection Problem

A practical challenge: **how do you know if your ANC system has nonlinear distortion?**

**Diagnostic test** (Zhao & Chen 2023):
1. Run standard FxLMS and measure steady-state NR
2. Inject a sinusoidal reference at frequency $f_0$
3. Check the error signal spectrum for harmonics at $2f_0, 3f_0, \dots$
4. If harmonics exceed -40 dB relative to the fundamental → nonlinear distortion is present

**Rule of thumb**: If the loudspeaker is driven above 80% of its maximum SPL, nonlinear distortion is likely significant.

---

## Related Concepts

- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/robust-adaptive-filtering|Robust Adaptive Filtering]]
- [[concepts/generalized-maximum-correntropy-criterion|Generalized Maximum Correntropy Criterion]]
- [[concepts/information-theoretic-learning|Information Theoretic Learning]]

## Related Sources
