---
type: synthesis
created: 2026-04-12
updated: 2026-05-17
sources:
- zotero://select/items/0_IZATI7ZF
- zotero://select/items/0_9KNF4YUC
- zotero://select/items/0_FERIFUEJ
- zotero://select/items/0_NEWLEZ9B
- zotero://select/items/0_QVJMFTWC
tags:
- adaptive-algorithms
- algorithm-selection
- convergence
- trade-off-analysis
- variable-step-size
---

# Adaptive Algorithm Trade-offs: A Decision Framework

> Cross-source synthesis connecting 10+ papers on adaptive filtering for ANC: FxLMS, Leaky FxLMS, Simplified Feedback, GMCC, MPC, and VSS variants.

---

## The Design Space

Every adaptive ANC algorithm makes trade-offs across three dimensions:

```
                    Performance (NR dB)
                          ▲
                         /│\
                        / │ \
                       /  │  \
                      /   │   \
                     /    │    \
                    /     │     \
      Robustness ◄────────┼────────► Computational Cost
                   \      │      /
                    \     │     /
                     \    │    /
                      \   │   /
                       \  │  /
                        \ │ /
                         \│/
```

No algorithm dominates on all three dimensions simultaneously.

---

## 1. Algorithm Catalog

### 1.1 FxLMS ([[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]])

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Performance | ★★★☆☆ | 10-25 dB NR for predictable noise |
| Robustness | ★★☆☆☆ | Fails under impulsive noise |
| Computational Cost | ★★★★★ | $O(L)$ multiplications per sample |

**Best for**: Standard single-channel ANC with Gaussian/mild noise.

**Worst for**: Impulsive noise environments, actuator-constrained systems.

### 1.2 Leaky FxLMS ([[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]])

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Performance | ★★★☆☆ | Similar to FxLMS, slight degradation |
| Robustness | ★★★★☆ | Leakage prevents coefficient blow-up |
| Computational Cost | ★★★★★ | Same as FxLMS + 1 multiplication |

**Best for**: Feedback ANC systems where coefficient growth is a concern.

**Trade-off**: Leakage coefficient $\gamma \approx 0.9998$ slightly reduces steady-state NR (1-2 dB loss).

### 1.3 Simplified Adaptive Feedback ([[sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]])

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Performance | ★★☆☆☆ | 3-5 dB less than IMC-based systems |
| Robustness | ★★★☆☆ | Same as Leaky FxLMS (uses it internally) |
| Computational Cost | ★★★★★ | $O(L)$ — eliminates IMC convolution |

**Best for**: DSP-constrained feedback ANC where computational simplicity is critical.

**Trade-off**: 3-5 dB NR loss for eliminating the $\hat{S}(z)$ convolution.

### 1.4 GMCC-based ANC (FxGMCC, IFxGMCC, C-IFxGMCC)

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Performance | ★★★★☆ | 18-22 dB NR under impulsive noise |
| Robustness | ★★★★★ | Automatic outlier rejection via correntropy |
| Computational Cost | ★★★☆☆ | $O(L)$ + kernel evaluation (~10-20% overhead) |

**Best for**: Impulsive noise environments (wind, mechanical impacts, speech bursts).

**Trade-off**: Extra computation for kernel evaluation; requires tuning $\alpha$ and $\beta$ parameters.

### 1.5 MPC ([[concepts/model-predictive-control|Model Predictive Control]])

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Performance | ★★★★☆ | 12-14 dB NR, but with explicit constraint handling |
| Robustness | ★★★★★ | Handles saturation, stability, and model uncertainty |
| Computational Cost | ★★☆☆☆ | QP: 150 μs/sample; Closed-form: < 10 μs/sample |

**Best for**: Actuator-constrained systems, multi-channel ANC, systems requiring explicit stability guarantees.

**Trade-off**: High computational cost (QP solver) or complex analytical derivation (closed-form).

### 1.6 VSS-FxLMS (Variable Step Size)

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Performance | ★★★★☆ | Faster convergence than fixed-step FxLMS |
| Robustness | ★★★☆☆ | Depends on VSS method (Versiera vs noise power vs error autocorrelation) |
| Computational Cost | ★★★★☆ | $O(L)$ + 2-4 extra multiplications for step size |

**Best for**: Non-stationary noise environments where convergence speed matters.

**Trade-off**: Additional parameters to tune ($\mu_{\max}$, smoothing factor $\alpha$).

---

## 2. The Performance-Robustness Frontier

Plotting all algorithms on the performance-robustness plane:

```
Robustness
    ▲
  5 │                          MPC
    │                    C-IFxGMCC
    │               IFxGMCC
  4 │          FxGMCC
    │     VSS-FxLMS
    │  Leaky FxLMS
  3 │
    │    FxLMS
  2 │  Simplified FB
    │
  1 │
    └─────────────────────────────────► Performance
    1    2    3    4    5    6    7
              Noise Reduction (dB, normalized)
```

**Pareto frontier**: C-IFxGMCC, MPC, and VSS-FxLMS form the current frontier. No other algorithm dominates them on both dimensions.

---

## 3. Decision Matrix

| Scenario | Recommended Algorithm | Why |
|----------|----------------------|-----|
| **Quiet office, single-channel** | FxLMS | Minimum complexity, adequate performance |
| **Wind noise (outdoor earbuds)** | FxGMCC ($\beta \approx 1.0$) | Automatic wind impulse rejection |
| **Mechanical impacts (industrial)** | C-IFxGMCC ($\beta \approx 0.5$) | Severe impulse robustness + convergence |
| **Headphones, DSP-constrained** | Simplified Feedback (Leaky FxLMS) | Eliminate IMC convolution |
| **Headphones, premium (no constraint)** | Hybrid FF+MVC+IMC (N-FxLMS) | Maximum NR across all frequencies |
| **Actuator saturation (large speakers)** | MPC (Liang 2026 closed-form) | Explicit saturation handling |
| **Multi-channel (6+ speakers)** | MPC or Frequency-Domain ANC | Naturally handles MIMO |
| **Changing noise conditions** | VSS-FxLMS (noise power estimate) | Fast adaptation to non-stationary noise |
| **Ultra-low latency (< 1 ms)** | FxLMS or Simplified FB | Minimal computation per sample |
| **Real-time embedded (2020s DSP)** | Leaky FxLMS or VSS-FxLMS | Balanced cost and performance |

---

## 4. The Convergence-Speed Trade-off

All adaptive algorithms face the same fundamental tension:

$$\text{Convergence Speed} \propto \mu \quad \text{vs} \quad \text{Steady-State Error} \propto \frac{1}{\mu}$$

| Algorithm | How It Addresses This | Residual Trade-off |
|-----------|----------------------|-------------------|
| FxLMS | Fixed $\mu$ | Must choose: fast or accurate |
| VSS-FxLMS | $\mu(n)$ adapts automatically | Extra parameters to tune |
| GMCC | Score function bounds the effective step size | Shape parameter $\beta$ affects both |
| MPC | Batch optimization over horizon | Prediction horizon $N_p$ vs compute |
| Simplified FB | Uses leaky FxLMS internally | Same as FxLMS |

---

## 5. Computational Cost Summary

| Algorithm | Multiplications/Sample | Additions/Sample | Memory |
|-----------|----------------------|-----------------|--------|
| FxLMS | $L + L_{\hat{S}}$ | $L + L_{\hat{S}}$ | $L + L_{\hat{S}}$ |
| Leaky FxLMS | $L + L_{\hat{S}} + 1$ | $L + L_{\hat{S}}$ | $L + L_{\hat{S}}$ |
| Simplified FB | $L$ | $L$ | $L$ |
| FxGMCC | $L + L_{\hat{S}} + 3$ (kernel) | $L + L_{\hat{S}} + 2$ | $L + L_{\hat{S}} + 2$ |
| VSS-FxLMS | $L + L_{\hat{S}} + 4$ (VSS) | $L + L_{\hat{S}} + 4$ | $L + L_{\hat{S}} + 3$ |
| MPC (QP) | $O(N_{state}^3 \cdot N_p)$ | $O(N_{state}^3 \cdot N_p)$ | $O(N_{state}^2 \cdot N_p)$ |
| MPC (closed-form) | $O(N_{state}^2)$ | $O(N_{state}^2)$ | $O(N_{state}^2)$ |

Where $L$ = filter length, $L_{\hat{S}}$ = secondary path length, $N_{state}$ = model order, $N_p$ = prediction horizon.

**Typical values**: $L = 256$, $L_{\hat{S}} = 128$, $N_{state} = 18$, $N_p = 10$.

---

## Related Concepts

- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]]
- [[concepts/simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]]
- [[concepts/generalized-maximum-correntropy-criterion|Generalized Maximum Correntropy Criterion]]
- [[concepts/model-predictive-control|Model Predictive Control]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/internal-model-control|Internal Model Control]]
- [[concepts/robust-adaptive-filtering|Robust Adaptive Filtering]]
- [[concepts/impulsive-noise|Impulsive Noise]]
- [[concepts/information-theoretic-learning|Information Theoretic Learning]]

## Related Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]]
- [[sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]]
- [[sources/chen-2016-generalized-correntropy-robust-adaptive-filtering|Chen 2016: Generalized Correntropy for Robust Adaptive Filtering]]
- [[sources/zhu-2020-robust-gmcc-anc-paper-reading-note|Zhu 2020: Robust GMCC for ANC Paper Reading Note]]
- [[sources/wills-2008-mpc-constraint-handling-anc-avc|Wills 2008: MPC Constraint Handling in ANC/AVC]]
- [[sources/liang-2026-delayed-mpc-anc-paper-reading-note|Liang 2026: Delayed MPC for ANC Paper Reading Note]]
