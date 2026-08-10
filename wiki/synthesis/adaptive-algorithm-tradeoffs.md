---
type: synthesis
created: 2026-04-12
updated: 2026-08-10
sources:
- zotero://select/items/0_IZATI7ZF
- zotero://select/items/0_9KNF4YUC
- zotero://select/items/0_FERIFUEJ
- zotero://select/items/0_NEWLEZ9B
- zotero://select/items/0_QVJMFTWC
- raw/papers/guo-2024-anc-saturation-survey/full-text.md
tags:
- adaptive-algorithms
- algorithm-selection
- convergence
- trade-off-analysis
- variable-step-size
- output-constraint-algorithms
- output-saturation
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

### 1.7 Output Constraint Family ([[concepts/output-constraint-anc-algorithms|Output Constraint ANC Algorithms]])

Per [[sources/guo-2024-anc-saturation-survey|Guo et al. 2024]], this family mitigates the [[output-saturation-effect|output saturation effect]] by limiting output power so the secondary-path amplifier stays linear. They are the **only family that preserves stability under severe saturation** (when the fundamental cannot be fully cancelled and unconstrained filters diverge).

| Algorithm | Mechanism | Multiplications | Notes |
|-----------|-----------|-----------------|-------|
| **2-GD FxLMS** | Two gradient directions; weight-reduction when $|y|>C$ | $2N + L + 1$ (matches FxLMS) | Lowest cost in family |
| **Re-scaling FxLMS** | Rescales $\mathbf{w}$ and $y$ by $C/|y|$ when threshold exceeded | $3N + L + 2$ | Simple amplitude clamp |
| **Leaky FxLMS** | Scalar leakage $\gamma$ penalises $\mathbf{w}^T\mathbf{w}$ | $3N + L + 1$ | Also used for feedback ANC stability |
| **Extended Leaky FxLMS** | Matrix leakage $\boldsymbol{\gamma}=\mathbf{C}^T\mathbf{C}$ | $2N^2 + 2N + L + 1$ | More control freedom, $O(N^2)$ |
| **OLFxLMS** (Optimal Leaky) | $\boldsymbol{\gamma}=\Lambda_o \mathbf{R}_x$; converges to QCQP optimum | $2N^2 + 2N + L$ | Needs offline inverse-modeling of $G_s$ |
| **MOV FxLMS** | Penalty $\alpha\,\mathbb{E}[y^2]$ on output variance | $3N + L + 1$ (basic); $4N + L + 7$ (optimal) | Power constraint |
| **MOV-Modified FxLMS** | Online estimation of $G_s \approx \sigma_{x'}^2/\sigma_x^2$ via moving filter; variable $\alpha(n)$ | $4N + L + K + 7$ | Tracks time-varying noise/environments |

| Dimension | Rating (MOV-Modified) | Notes |
|-----------|----------------------|-------|
| Performance | ★★★☆☆ | Cancels what the linear-region budget allows; harmonic distortion left untreated |
| Robustness | ★★★★★ | Preserves stability under severe saturation — only family that does |
| Computational Cost | ★★★★☆ | $O(N)$ for most variants; $O(N^2)$ only for optimal-leaky |

**Best for**: Severe output saturation where unconstrained FxLMS/NLANC diverge; dynamic noise environments (MOV-Modified).

**Trade-off**: Does not cancel harmonic distortion under mild saturation — for that, pair with an [[nonlinear-active-noise-control|NLANC]] algorithm.

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
| **Actuator saturation (large speakers)** | MOV-Modified FxLMS (severe) or MPC (Liang 2026 closed-form) | Output-constraint family preserves stability under severe saturation; NLANC diverges (Guo 2024) |
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
- [[concepts/output-saturation-effect|Output Saturation Effect]]
- [[concepts/output-constraint-anc-algorithms|Output Constraint ANC Algorithms]]

## Related Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]]
- [[sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]]
- [[sources/chen-2016-generalized-correntropy-robust-adaptive-filtering|Chen 2016: Generalized Correntropy for Robust Adaptive Filtering]]
- [[sources/zhu-2020-robust-gmcc-anc-paper-reading-note|Zhu 2020: Robust GMCC for ANC Paper Reading Note]]
- [[sources/wills-2008-mpc-constraint-handling-anc-avc|Wills 2008: MPC Constraint Handling in ANC/AVC]]
- [[sources/liang-2026-delayed-mpc-anc-paper-reading-note|Liang 2026: Delayed MPC for ANC Paper Reading Note]]
- [[sources/fujii-2006-simultaneous-equations-anc|Fujii et al. 2006: Verification of Simultaneous Equations Method]] — Frequency-domain adaptive algorithm with faster convergence than filtered-x NLMS, no secondary path model required
- [[sources/guo-2024-anc-saturation-survey|Guo et al. 2024: ANC Algorithms Overcoming Output Saturation]] — introduces the output-constraint family (Section 1.7) as the practical default for severe saturation; provides per-algorithm complexity table and the mild-vs-severe saturation regime distinction
