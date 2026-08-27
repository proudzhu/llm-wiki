---
type: synthesis
created: 2026-04-12
updated: 2026-08-27
sources:
- zotero://select/items/0_N8MHRKXP
- zotero://select/items/0_FERIFUEJ
- raw/papers/guo-2024-anc-saturation-survey/full-text.md
- raw/papers/rafaely-2000-constrained-fdlms/full-text.md
tags:
- flnn
- kernel
- nonlinear-anc
- spline
- volterra
- output-saturation
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

## The Saturation Regime: When NLANC Diverges (Guo 2024)

A critical limitation absent from the individual NLANC algorithm papers is highlighted by [[sources/guo-2024-anc-saturation-survey|Guo et al. 2024]]: **NLANC algorithms themselves diverge under severe output saturation**. The survey distinguishes two saturation regimes:

| Regime | Definition | NLANC behaviour | Recommended family |
|:-------|:-----------|:----------------|:-------------------|
| **Mild saturation** | Fundamental still cancelable; only harmonics remain | Effective — pre-distortion cancels harmonics | NLANC (this page) |
| **Severe saturation** | Fundamental not fully cancelable; amplifier clips | **Diverges** — residual error retains phase of filtered reference, coefficients grow without bound | [[output-constraint-anc-algorithms|Output constraint algorithms]] |

The divergence result (Eq. 12 of the survey) applies to *all* unconstrained adaptive filters — linear FxLMS and NLANC alike — once the amplifier enters its severe nonlinear region. The practical implication: NLANC is the right tool only when the saturation is mild enough that the fundamental can still be cancelled. Under severe saturation, an output constraint algorithm (e.g., MOV-Modified FxLMS) is required to preserve stability, at the cost of not fully cancelling the disturbance.

The output-constraint idea itself long predates the survey: [[sources/rafaely-2000-constrained-fdlms|Rafaely & Elliott 2000]] introduced [[concepts/constrained-fdlms|constrained FDLMS]], which enforces magnitude and output-power limits online via a penalty function in the frequency domain — and showed that explicit, frequency-selective penalties dominate the leaky-LMS-style global penalty that otherwise keeps unconstrained adaptation stable. The later time-domain family (MOV, OLFxLMS, etc.) can be read as porting this penalty-function principle to FxLMS.

### Additional NLANC Algorithms for Output Saturation

The survey also covers two NLANC algorithms not elsewhere in this synthesis:

- **THF-FxLMS** (Sahib 2012): Hammerstein model with tangential hyperbolic nonlinearity $f(y) = \alpha_f \tanh(\beta y)$. Lowest computational cost among NLANC algorithms ($2N + 2L + 3$ multiplications), but effective only for periodic noise and requires a small step size.
- **MLPNN-FxLMS** (Elliott 2001): Multi-layer perceptron with backpropagation. Universal approximator with the strongest nonlinear modelling ability, but at an unachievable computational burden for real-time ANC ($O(M^2 L)$); suffers from gradient vanishing with depth.

---

## Related Concepts

- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/robust-adaptive-filtering|Robust Adaptive Filtering]]
- [[concepts/generalized-maximum-correntropy-criterion|Generalized Maximum Correntropy Criterion]]
- [[concepts/information-theoretic-learning|Information Theoretic Learning]]
- [[concepts/nonlinear-active-noise-control|Nonlinear Active Noise Control]]
- [[concepts/output-saturation-effect|Output Saturation Effect]]
- [[concepts/output-constraint-anc-algorithms|Output Constraint ANC Algorithms]] — the complementary family required under severe saturation

## Related Sources

- [[sources/guo-2024-anc-saturation-survey|Guo et al. 2024: ANC Algorithms Overcoming Output Saturation]] — surveys NLANC algorithms for output saturation; proves NLANC divergence under severe saturation; covers THF-FxLMS and MLPNN-FxLMS
- [[sources/rafaely-2000-constrained-fdlms|Rafaely & Elliott 2000: Computationally Efficient Frequency-Domain LMS with Constraints]] — frequency-domain origin of the output-constraint principle (penalty-function constrained adaptation)
