---
type: concept
created: 2026-04-22
updated: 2026-05-13
sources:
  - wiki/sources/kuo-1999-active-noise-control-tutorial-review.md
  - wiki/sources/pawelczyk-1997-anc-feedback-fixed-adaptive.md
  - wiki/sources/wu-2014-simplified-adaptive-feedback-anc.md
  - wiki/sources/seo-2016-feedback-anc-constrained-optimization.md
  - wiki/sources/lu-2021-survey-active-noise-control-linear.md
tags:
  - active-noise-control
  - control-theory
  - feedback
  - stability
---

# Feedback ANC

**Feedback Active Noise Control (FB-ANC)** is an architecture where only the error sensor (microphone) is available. Unlike [[wiki/concepts/feedforward-anc|Feedforward ANC]], it does not use a reference microphone to capture the noise source upstream. It is primarily used in headphones, hearing aids, and communication headsets where external reference sensors are impractical.

## 1. Fundamental Architecture
In FB-ANC, the controller $W(z)$ uses the residual error signal $e(n)$ to generate anti-noise. This creates a closed-loop system:

```
Primary noise d(n) ──→ (+) ──→ Error e(n) ──→ Controller W(z) ──→ Secondary S(z) ──→ (-)
                       ↑                                                         │
                       └─────────────────────────────────────────────────────────┘
                                        Feedback path
```

The error signal in the frequency domain is governed by the **Sensitivity Function** $S_{sens}(z)$:
$$E(z) = \frac{1}{1 + S(z)W(z)} D(z)$$

## 2. Theoretical Constraints
### The Waterbed Effect (Bode's Integral)
Feedback systems are bound by the **Bode Integral Theorem**:
$$\int_0^\pi \log |S_{sens}(e^{j\omega})| \, d\omega = 0$$
This implies that any noise reduction (where $|S_{sens}| < 1$) must be compensated by noise amplification elsewhere (where $|S_{sens}| > 1$). This is a physical limit: you cannot reduce noise at all frequencies simultaneously in a feedback loop.

### Stability vs. Bandwidth
Stability is the primary bottleneck. According to **Vaudrey & Baumann (2003)**, the system is stable if:
- **Phase Margin**: The phase error between the true secondary path $S(z)$ and the model $\hat{S}(z)$ is less than **90°**.
- **Loop Delay**: Total latency must be low (typically < 0.5 ms for 1 kHz bandwidth).

## 3. Control Structures

### Internal Model Control (IMC)
The most common structure for **Adaptive Feedback ANC**. It uses a model of the secondary path $\hat{S}(z)$ to estimate the primary noise (regenerate the reference signal):
$$\hat{x}(n) = e(n) + \sum_{m=0}^{M-1} \hat{s}_m y(n-m)$$
The regenerated $\hat{x}(n)$ is then used as a reference for the standard [[wiki/concepts/filtered-x-lms-algorithm|FxLMS Algorithm]].

For **fixed (non-adaptive) feedback controllers**, the IMC structure simplifies controller design. The controller transfer function is:
$$K(z) = \frac{Q(z)}{1 - \hat{G}(z) Q(z)}$$
where $Q(z)$ is the feedforward filter and $\hat{G}(z)$ is the internal model. Nominal stability is guaranteed for any $Q(z)$ if $\hat{G}(z) = G(z)$. The sensitivity function becomes:
$$S(z) = 1 - Q(z) \hat{G}(z)$$

### Robust Controller Optimization (Hilgemann 2024)
Fixed feedback controllers can be optimized via constrained least-squares over $Q(z)$, with robust stability constraints derived from [[wiki/concepts/uncertainty-modeling-for-anc|uncertainty models]]. Data-driven models (elliptic, convex hull) that more accurately capture plant variations enable 10–18 dB more attenuation than conventional disk models while maintaining robust stability.

### Constrained Optimization with Frequency Warping (Seo 2016)
**Seo et al. (2016)** designed low-order feedback ANC filters using constrained optimization in the warped frequency domain. By combining [[concepts/q-parameterization|Q-parameterization]] with [[concepts/frequency-warping|frequency warping]], a 16th-order WFIR filter achieves ~19dB attenuation matching a 128th-order FIR at low frequencies. The warping parameter $\lambda$ provides a tunable trade-off between low-frequency resolution and noise boosting.

### Simplified Adaptive Feedback ANC (SimpAFB)
Proposed by **Wu et al. (2014)**, this method uses the error signal $e(n)$ **directly** as the reference signal. It eliminates the expensive IMC convolution, but relies heavily on the [[wiki/concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]] for stability.

### Minimum Variance Control (MVC)
An optimal fixed-controller approach (Pawelczyk 1997) that minimizes the variance of the error signal. It provides the mathematical benchmark for feedback performance.

## 4. DOA Independence

A key advantage of feedback ANC is that it is independent of the direction of arrival (DOA) of the noise. The sensitivity function $S_{\text{FB}}(z) = 1/(1 + G(z)K(z))$ depends only on the secondary path $G(z)$ and the controller $K(z)$, not on the primary path $P(z)$. Since the loudspeaker and inner microphone have fixed positions in close proximity, $G(z)$ does not vary with DOA.

Liebich et al. (2018) confirmed this experimentally: feedback ANC showed consistent attenuation across all azimuth angles on the horizontal plane, while [[feedforward-anc|Feedforward ANC]] showed significant DOA-dependent degradation. This makes feedback ANC particularly valuable in [[hybrid-anc|Hybrid ANC]] systems, where it compensates for the feedforward component's DOA sensitivity.

## 5. Comparisons

| Feature | Feedforward | Feedback |
| :--- | :--- | :--- |
| **Reference Sensor** | Yes (Upstream) | No (Uses Error) |
| **Stability** | Highly Stable | More Fragile |
| **Noise Type** | Multi-source/Broadband | Narrow-band/Predictable |
| **Waterbed Effect** | Negligible | **Dominant** |
| **Typical App** | Duct/Open Room | Headphones/In-ear |

## Related
- [[wiki/concepts/adaptive-feedback-control]]
- [[wiki/concepts/internal-model-control]]
- [[wiki/concepts/simplified-adaptive-feedback-anc]]
- [[wiki/concepts/uncertainty-modeling-for-anc]]
- [[wiki/concepts/robust-stability-constraint]]
- [[wiki/concepts/convex-hull-uncertainty-model]]
- [[wiki/concepts/elliptic-uncertainty-model]]
- [[wiki/synthesis/feedback-anc-filter-design]]
- [[wiki/synthesis/feedback-anc-filter-design]]

## Related Sources

- [[sources/pawelczyk-1997-anc-feedback-fixed-adaptive|Pawelczyk 1997: ANC Feedback Fixed/Adaptive]]
- [[sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]]
- [[sources/hilgemann-2024-data-driven-uncertainty-anc|Hilgemann 2024: Data-Driven Uncertainty Modeling for Robust Feedback ANC]]
- [[sources/liebich-2018-doa-dependency-anc-headphones|Liebich 2018: DOA Dependency of ANC Headphones]]
- [[sources/seo-2016-feedback-anc-constrained-optimization|Seo et al. 2016: Feedback ANC via Constrained Optimization]]

## Related Concepts

- [[wiki/concepts/adaptive-feedback-control]]
- [[wiki/concepts/feedforward-anc|Feedforward ANC]]
- [[wiki/concepts/filtered-x-lms-algorithm|FxLMS Algorithm]]
- [[wiki/concepts/internal-model-control]]
- [[wiki/concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]]
- [[wiki/concepts/simplified-adaptive-feedback-anc]]
