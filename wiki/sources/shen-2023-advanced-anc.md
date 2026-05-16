---
type: source
created: 2026-04-22
updated: 2026-04-28
sources:
  - raw/papers/shen-2023-advanced-anc/full-text.txt
  - https://doi.org/10.32657/10356/166615
  - zotero://select/items/0_EUIIZATZ
tags:
  - active-noise-control
  - anc-headphones
  - doctoral-dissertation
  - wireless-anc
  - adaptive-gain
  - hybrid-anc
---

# Shen 2023: Advanced Active Noise Control Headphone: Algorithm and Implementation

**Author**: Xiaoyi Shen
**Supervisor**: Prof Gan Woon Seng
**University**: Nanyang Technological University, Singapore
**Year**: 2023
**Thesis Type**: Doctoral Dissertation
**DOI**: [10.32657/10356/166615](https://doi.org/10.32657/10356/166615)
**📎 Zotero**: [zotero://select/items/0_EUIIZATZ](zotero://select/items/0_EUIIZATZ)

## Summary

This dissertation addresses practical challenges in ANC headphones: adaptive algorithm instability, computational complexity, dynamic noise reduction in multi-noise environments, low reference-to-interference ratio, and causality constraints. Four core innovations are proposed: (1) Adaptive Gain (AG) algorithm for fast convergence, (2) Alternating Switching Hybrid ANC (ASHANC) for non-coherent noise handling, (3) Wireless Reference ANC with coherence-based selection, and (4) Error Separation Module (ESM) for multi-path weight competition resolution.

## Problem Formulation

Traditional FxLMS in headphones faces three pain points:
1. **Convergence lag**: High-order FIR filters (>256 taps) react too slowly to non-stationary noise
2. **Non-coherent interference**: Internal speech or noise not captured by reference mic causes FF weight fluctuations
3. **Causality failure**: Sound propagation delay limits maximum effective noise reduction bandwidth

## Methodology

### 1. Adaptive Gain (AG) Algorithm

#### Core Idea

Pre-train $N_g$ fixed filters $\mathbf{w}_i$ (for different sound source directions), online only update weight gains $\mathbf{g}(n)$, compressing parameter space from $L$ dimensions to $N_g$ dimensions.

#### MSE Surface and Convergence

Error signal:
```
e(n) = d(n) + y'^T(n) g(n)
```

MSE cost function:
```
ξ(n) = E[e²(n)] = E[d²(n)] + 2P_{dy'}^T g(n) + g^T(n) R_{y'y'} g(n)
```

where $R_{y'y'} = E[y'(n)y'^T(n)]$ is the autocorrelation matrix (Hessian matrix).

Optimal solution:
```
g_opt = -R_{y'y'}^{-1} P_{dy'}
```

Step size bound:
```
0 < μ_g < 2 / λ_max(R_{y'y'})
```

Since $R_{y'y'}$ is very small dimension, its maximum eigenvalue $\lambda_{max}$ is relatively small and concentrated, allowing very large step size $\mu_g$, achieving 10x faster convergence than FxLMS.

#### Why AG Tolerates Larger Step Size than FxLMS?

AG improves the Hessian matrix condition number through dimensionality reduction. In FxLMS, 256-tap FIR has extreme eigenvalue spread; to prevent fastest mode from diverging, overall step size must be sacrificed. AG's small-scale matrix has more concentrated eigenvalue distribution, allowing step size to span 2-3 orders of magnitude.

### 2. Alternating Switching Hybrid ANC (ASHANC)

#### State Machine Control

Traditional hybrid (FF+FB) systems face perturbation from non-coherent noise $v(n)$ — FF tries to compensate $v(n)$ causing weight fluctuation. ASHANC introduces state machine decoupling:

When updating FF weights $\mathbf{w}_f$ with $v(n)$ present, steady-state weight error fluctuation:
```
E[ε_f(∞)] = R_{x'x'}^{-1} E[x'(n) v(n)]
```

Although expectation is 0, $v(n)$ power directly contributes excess MSE:
```
J_ex = E[v²(n)] · Tr(R_{x'x'}^{-1} ...)
```

ASHANC triggers switching via $|S_p| < S_T$, ensuring FB first suppresses $v(n)$, then FF updates on "clean" error signal, eliminating intermodulation interference.

#### Does State Switching Cause Pop Noise?

Experiments show slope judgment criterion is smooth, and weights remain continuous at switching instant. In actual headphone implementation, progressive gain switching avoids transient acoustic impact.

### 3. Wireless Reference ANC

#### Spatial Look-ahead and Causality

Wireless transmission (light speed) provides physical `look-ahead time`. System causality requires:
```
δ_p > δ_r + δ_e + δ_s
```

Using CD4046 PLL scheme, source distance must be **> 0.72m** to ensure anti-noise arrives in time.

#### Coherence-Based Selection (CBS)

Noise reduction (NR) and coherence $C_{xd}$ satisfy:
```
NR(ω) = -10 log₁₀(1 - C_{xd}(ω))
```

Inverting for minimum coherence to achieve target NR:
```
C_T = 1 - 10^{-(NR_target/10)}
```

CBS automatically discards low-coherence reference sources, preventing system divergence from irrelevant noise.

### 4. Error Separation Module (ESM)

To prevent multi-path weight competition, ESM constructs orthogonal errors:
```
e_w(n) = e(n) - ŝ(n) * y_{fb}(n)
e_{fb}(n) = e(n) - ŝ(n) * y_w(n)
```

This ensures joint cost function $J = E[e_w²] + E[e_{fb}²]$ has unique global minimum, avoiding convergence local traps.

## Performance

| Metric | Result |
|--------|--------|
| AG convergence | Stable within 1 second (10x faster than FxLMS) |
| Wireless ANC gain | +5.8 dB in 300-800 Hz band |
| ASHANC stability MSE | ~5 dB lower than traditional HANC under strong non-coherent interference |
| Causality distance | > 0.72m (CD4046 PLL) |

## Key Contributions

1. **AG Algorithm**: Single-parameter adaptive gain achieves ultra-fast convergence by reducing optimization dimensionality
2. **ASHANC Architecture**: State-machine controlled FF/FB switching solves non-coherent interference
3. **Wireless Reference ANC**: Quantified wireless transmission's contribution to ANC causality
4. **CBS/ESM Modules**: Precise error signal decoupling in multi-source environments

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/hybrid-anc|Hybrid ANC]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/causality|Causality in ANC]]

## Related Synthesis

- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]
- [[synthesis/adaptive-algorithm-tradeoffs|Adaptive Algorithm Trade-offs]]

## Related Entities

- [[entities/xiaoyi-shen|Xiaoyi Shen]]
- [[entities/woon-seng-gan|Woon-Seng Gan]]
