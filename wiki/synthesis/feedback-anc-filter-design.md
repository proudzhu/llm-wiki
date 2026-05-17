---
type: synthesis
created: 2026-04-12
updated: 2026-04-29
sources:
- zotero://select/items/0_2LKM9QRI
- zotero://select/items/0_XLZPIW68
- zotero://select/items/0_VRSLTC2L
- zotero://select/items/0_846A4RH7
- zotero://select/items/0_Vaudrey2003
- zotero://select/items/0_BPH79CM5
- zotero://select/items/0_D2BV74LJ
- zotero://select/items/0_Z7FUV6LL
- zotero://select/items/0_IA5SPUL5
- zotero://select/items/0_97XR3LJ7
- zotero://select/items/0_T3GXM3RI
tags:
- constrained-lms
- feedback-anc
- filter-design
- robust-control
- stability
- waterbed-effect
- acoustic-feedback-cancellation
- deep-learning
- step-size-control
- variable-step-size
- uncertainty-modeling
aliases:
- Feedback ANC and Acoustic Feedback Cancellation
- Adaptive Step-Size Control in Feedback ANC
---

# Feedback ANC Filter Design: Stability, Robustness, and Performance Trade-offs

> Cross-source synthesis connecting: Pawelczyk (1997) fixed/adaptive feedback ANC, Vaudrey & Baumann (2003) LMS feedback stability, Arablouei & Doğançay (2015) constrained LMS, Morari & Zafiriou (2002) robust control, Albertos & Mareels (2010) control theory, and Zhao & Zeng (2010) reduced feedback FLNN.

---

## The Fundamental Problem: No Reference Signal

In feedforward ANC, the filter design problem is straightforward: measure the noise upstream, adapt the filter to predict the downstream noise. In **feedback ANC**, there is no upstream reference — the controller must generate anti-noise based only on the error sensor reading.

This changes everything.

### The Feedback Loop

```
Primary noise d(n) ──→ (+) ──→ Error e(n) ──→ Controller W(z) ──→ Secondary S(z) ──→ (-)
                       ↑                                                         │
                       └─────────────────────────────────────────────────────────┘
                                        Feedback path
```

The error signal is:
$$E(z) = D(z) - S(z)W(z)E(z)$$

Solving for $E(z)$:
$$E(z) = \frac{D(z)}{1 + S(z)W(z)}$$

The **sensitivity function** $S_{sens}(z) = \frac{1}{1 + S(z)W(z)}$ determines how much noise is attenuated. For noise reduction at frequency $\omega$:
$$|S_{sens}(e^{j\omega})| < 1 \implies |1 + S(e^{j\omega})W(e^{j\omega})| > 1$$

---

## 1. Fixed Feedback Controller (Pawelczyk 1997)

### Design Philosophy

A fixed feedback controller $W(z)$ is designed **offline** to minimize the error variance:
$$\min_W E[|e(n)|^2]$$

This is equivalent to minimizing the $H_2$ norm of the sensitivity function:
$$\min_W \|S_{sens}(z)\|_2$$

### The MVC Solution

**Minimum Variance Control** (MVC) provides the optimal fixed controller:
$$W_{\text{MVC}}(z) = \frac{1 - F(z)}{S(z) \cdot F(z)}$$

where $F(z)$ is the **minimum-phase spectral factor** of the primary noise:
$$\Phi_{dd}(z) = \sigma^2 \cdot F(z)F(z^{-1})$$

### The Waterbed Effect

The sensitivity function obeys the **Bode integral constraint**:
$$\int_0^\pi \log |S_{sens}(e^{j\omega})| \, d\omega = 0$$

This means: **any noise reduction in one frequency band must be paid for by noise amplification in another**. The fixed MVC controller pushes the amplification to frequencies where the primary noise is weakest.

### Design Procedure (Pawelczyk 1997)

1. **Model the primary noise**: Estimate $\Phi_{dd}(z)$ from error sensor data
2. **Spectral factorization**: Compute $F(z)$ such that $\Phi_{dd}(z) = \sigma^2 F(z)F(z^{-1})$
3. **Compute MVC controller**: $W_{\text{MVC}}(z) = \frac{1 - F(z)}{S(z) \cdot F(z)}$
4. **Check stability**: Verify that all poles of $\frac{1}{1 + S(z)W(z)}$ are inside the unit circle
5. **If unstable**: Reduce controller gain or add roll-off at high frequencies

### Performance

| Noise Type | NR Achieved | Bandwidth | Limiting Factor |
|-----------|------------|-----------|----------------|
| Narrow-band (tonal) | 15-25 dB | ±5% of center freq | Waterbed effect |
| Broadband (low-freq) | 8-15 dB | 20-200 Hz | Phase margin |
| Broadband (full) | 5-10 dB | 20-1000 Hz | Causality + waterbed |

---

## 2. Adaptive Feedback Controller (Pawelczyk 1997)

### The IMC Approach

Internal Model Control synthesizes a reference signal:
$$\hat{X}(z) = E(z) + \hat{S}(z)Y(z)$$

Then applies FxLMS:
$$w(n+1) = w(n) + \mu \cdot e(n) \cdot \hat{x}_f(n)$$

### The Stability Problem

Vaudrey & Baumann (2003) identified the **fundamental stability constraint** for adaptive LMS-based feedback control:

**Theorem** (Vaudrey & Baumann 2003): The adaptive feedback loop is stable if and only if:

1. **Phase constraint**: $\angle \hat{S}(e^{j\omega}) - \angle S(e^{j\omega}) < 90^\circ$ for all $\omega$ where the loop gain exceeds 1
2. **Gain constraint**: $\mu < \frac{2}{\lambda_{\max}(R_{\hat{x}\hat{x}})}$ where $R_{\hat{x}\hat{x}}$ is the autocorrelation of the synthesized reference
3. **Delay constraint**: The total loop delay must be $< \frac{1}{2f_{\max}}$ where $f_{\max}$ is the highest frequency to be cancelled

### Practical Implications

| Constraint | What It Means | Typical Limit |
|-----------|--------------|--------------|
| Phase error < 90° | $\hat{S}(z)$ must be within 90° of $S(z)$ | ~5% modeling error at low freq |
| Step size bound | $\mu$ limited by synthesized reference power | $\mu < 0.01$ for typical ANC |
| Loop delay | Physical delay limits bandwidth | < 0.5 ms for 1 kHz cancellation |

The **phase constraint** is the most restrictive: if the secondary path model $\hat{S}(z)$ has more than 90° phase error from the true $S(z)$ at any frequency, the adaptive loop becomes **unconditionally unstable** at that frequency.

---

## 3. Constrained LMS for Robust Feedback (Arablouei & Doğançay 2015)

### The Problem

Standard LMS/FxLMS does not constrain the filter coefficients. In feedback ANC, this can lead to:
- **Coefficient blow-up**: Unbounded growth when the loop is near instability
- **Wind-up**: Accumulated error during saturation
- **Oscillation**: Limit cycles in the adaptive loop

### Constrained LMS Formulation

Arablouei & Doğançay (2015) formulate the constrained LMS problem:

$$\min_w E[e^2(n)] \quad \text{subject to} \quad \|w\|^2 \leq \gamma^2$$

The solution is a **projected** LMS update:
$$w(n+1) = \begin{cases} w(n) + \mu \cdot e(n) \cdot x(n) & \text{if } \|w(n+1)_{\text{unconstrained}}\| \leq \gamma \\ \gamma \cdot \frac{w(n+1)_{\text{unconstrained}}}{\|w(n+1)_{\text{unconstrained}}\|} & \text{otherwise} \end{cases}$$

### Mean-Square Performance

The constrained LMS has **worse** steady-state MSE than the unconstrained LMS (the constraint prevents the optimal solution if it lies outside the constraint set). But it is **more stable**:

| Metric | Unconstrained LMS | Constrained LMS |
|--------|------------------|-----------------|
| Steady-state MSE | $\sigma_v^2 \cdot \mu \cdot \text{tr}(R)$ | $\sigma_v^2 \cdot \mu \cdot \text{tr}(R) + \delta$ |
| Stability guarantee | Conditional (depends on $\mu$) | Unconditional (if $\gamma$ chosen correctly) |
| Divergence recovery | No (diverges to infinity) | Yes (bounded by $\gamma$) |

### Design Rule for Feedback ANC

Choose $\gamma$ based on the **expected optimal filter norm**:
$$\gamma = \alpha \cdot \|w_{\text{opt}}\|$$

where $\alpha \approx 1.2$-$1.5$ provides enough margin for the optimal solution while preventing blow-up.

---

## 4. Robust Control Perspective (Morari & Zafiriou 2002)

### H∞ Design for Feedback ANC

Morari & Zafiriou's robust control framework formulates feedback ANC as an $H_\infty$ optimization problem:

$$\min_W \|W_1(z) \cdot S_{sens}(z)\|_\infty$$

where $W_1(z)$ is a **weighting function** that specifies which frequencies matter most.

### Advantages over MVC

| Aspect | MVC | $H_\infty$ |
|--------|-----|-----------|
| **Optimality** | Minimizes average error ($H_2$) | Minimizes worst-case error ($H_\infty$) |
| **Robustness** | No explicit robustness guarantee | Explicit robustness to model uncertainty |
| **Constraint handling** | None | Can incorporate constraints |
| **Computation** | Spectral factorization (closed-form) | Convex optimization (numerical) |
| **Waterbed effect** | Implicit (cannot avoid) | Explicit (can shape the trade-off) |

### The Structured Singular Value ($\mu$)

For feedback ANC with model uncertainty $\Delta$ in the secondary path:
$$S(z) = \hat{S}(z) \cdot (1 + \Delta(z)), \quad \|\Delta\|_\infty \leq \delta$$

The **robust stability condition** is:
$$\|\hat{S}(z)W(z)\|_\infty < \frac{1}{\delta}$$

This provides an **explicit bound** on the maximum allowable controller gain at each frequency, given the level of uncertainty in $\hat{S}(z)$.

---

## 5. Reduced Feedback FLNN (Zhao & Zeng 2010)

For **nonlinear** feedback ANC, Zhao & Zeng replace the linear controller with a FLNN:

$$y(n) = \sum_{m=0}^{M} w_m \cdot \phi_m(e(n))$$

where $\phi_m(\cdot)$ are trigonometric basis functions: $\phi_m(x) = \sin(m\pi x)$ or $\cos(m\pi x)$.

**Reduced feedback variant**: Only update the weights every $P$ samples, reducing computation by $P\times$ with < 1 dB NR loss.

**Stability constraint**: The FLNN must satisfy a Lipschitz condition:
$$\left|\sum_{m=0}^{M} w_m \cdot \phi_m(e)\right| \leq L \cdot |e|$$

for some finite $L$. This ensures the feedback loop does not amplify errors.

---

## 6. Feedback ANC vs. Acoustic Feedback Cancellation

While historically separated into "noise control" and "hearing aid" silos, feedback ANC and AFC are fundamentally governed by the same stability constraints.

### Comparative Matrix

| Feature | Feedback ANC | Acoustic Feedback Cancellation (AFC) |
| :--- | :--- | :--- |
| **Primary Goal** | Broadband Noise Suppression | Howl (Oscillation) Prevention |
| **Input Signal** | Ambient Noise | User Speech / Ambient Audio |
| **Constraint** | Waterbed Effect (Bode) | Feedback Loop Gain (1/$\Delta$) |
| **Critical Challenge** | Latency | Speech/Feedback Decorrelation |
| **State-of-Art** | Hybrid FF+FB+IMC | DeepPEM + Neural Observers |

### Deep AFC (Gen 3)

- **DeepPEM-AFC**: Uses Prediction-Error Methods (PEM) embedded in a deep learning framework to separate feedback from speech, significantly improving system stability in speech-heavy environments.
- **Nested RNNs (Z7FUV6LL)**: Directly generates feedback cancellation filters by learning the underlying structural mappings of the feedback path, effectively bypassing the need for explicit path identification.

### Multi-Modal AFC (Gen 4)

- **IMU-based step-size control** (Miran et al. 2026): Head movement acceleration from an IMU integrated in the hearing aid triggers fast adaptation when path changes are anticipated, and slow adaptation otherwise. Outperforms audio-only VSS and shadow filter methods in steady-state by avoiding audio-induced biases.
- **Limitation**: Cannot detect path changes from external objects (phone, hand) that precede head movement → motivates a combined audio + IMU multi-modal approach.

---

## 7. Step-Size Control Hierarchy

### The Step-Size Dilemma

Every adaptive feedback ANC system faces the fundamental tension:

$$\text{Large } \mu \xrightarrow{\text{fast convergence, poor steady state}} \quad \text{Small } \mu \xrightarrow{\text{slow convergence, accurate steady state}}$$

### Audio-Driven Step-Size Adaptation

**Conventional VSS** (Kwong-Johnston 1992): $\mu(n) = \alpha \mu(n-1) + \gamma e^2(n)$
- Failure mode in feedback ANC: cannot distinguish secondary path changes from primary noise changes

**Inverse VSS** (Akhtar 2006): For online SPM where disturbance decreases by nature:
$$\alpha(n) = 1 - \frac{\hat{P}_e(n)}{\hat{P}_{e_s}(n)}$$
Step size increases over time as the modeling error decreases.

**Leaky FxLMS** (Wu 2014): Constrains the effective step size structurally:
$$w(n+1) = \gamma \cdot w(n) + \mu \cdot e(n) \cdot x_f(n), \quad 0 < \gamma \leq 1$$
The leakage coefficient $\gamma$ acts as a soft step-size ceiling. Essential for SimpAFB where the error signal is used directly as reference.

### Uncertainty-Aware Step-Size Boundaries (Hilgemann 2024)

The conventional disk uncertainty model $\Pi_\mu^{(NB)}$ covers a full circle of radius $R_\mu$ — much of which has no actual measurements, forcing 10–18 dB of conservatism. The **elliptic** and **convex hull** models reduce the uncertainty set area to ~60% by capturing the directional nature of plant variations.

| Approach | When Applied | What It Optimizes |
|:---------|:-------------|:------------------|
| Data-driven uncertainty | Design time | Maximum safe baseline gain |
| VSS step-size | Run time | Dynamic step size for path tracking |
| Leaky FxLMS | Run time | Structural step-size ceiling |

### Neural Step-Size Estimation

**Neural Kalman Gain** (Zhang 2024): A neural network predicts process/measurement covariances $Q(n)$ and $R(n)$ in real-time, replacing heuristic VSS rules with learned covariance estimation.

**DNoiseNet MLP** (Cha 2023): A small MLP (65 parameters) models the secondary path online, improving filtered reference quality and allowing larger effective step sizes.

### The Three-Layer Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 3: Meta-Step-Size (What step-size strategy to use?)     │
│  → Neural step-size estimator (Zhang 2024)                     │
│                           │                                     │
│  Layer 2: Step-Size Switching (When to change step size?)      │
│  → Audio-based VSS (Akhtar 2006), inverse VSS                  │
│                           │                                     │
│  Layer 1: Step-Size Boundaries (How large is safe?)            │
│  → Uncertainty model (Hilgemann 2024) + Leaky/Constrained LMS │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Open Problems

1. **Step-size scheduling across architectures**: In hybrid ANC (FF+FB+IMC, Benois 2020), the feedback controller step size affects the feedforward controller's operating point. Coordinated step-size scheduling across both loops is an open problem.

2. **Neural step size with stability guarantees**: Zhang 2024's neural covariance estimator has no formal stability guarantee. Combining neural step-size estimation with constrained LMS or robust stability constraints would provide a safety net.

3. **Non-acoustic sensor integration for ANC**: While IMU-based step-size control has been demonstrated for AFC in hearing aids (Miran 2026), applying similar multi-modal sensing to feedback ANC step-size control remains unexplored.

4. **From binary to continuous VSS**: Many VSS implementations use binary switching between $\mu_L$ and $\mu_S$. A continuous mapping (proportional or learned) could provide smoother transitions.

---

## 9. Unified Design Framework

### The Filter Design Decision Tree

```
What type of feedback ANC do you need?
│
├─ Linear, stationary noise → MVC (fixed controller)
│   → Design: Spectral factorization + waterbed shaping
│   → Stability: Check poles of 1/(1+S·W)
│
├─ Linear, non-stationary noise → IMC + FxLMS (adaptive)
│   → Design: FxLMS with $\hat{S}(z)$ estimation
│   → Stability: Phase error < 90°, $\mu$ bounded, delay < 0.5 ms
│   → Step-size: VSS (Akhtar 2006) + Leaky FxLMS safety net
│
├─ Linear, uncertain plant → H∞ robust controller
│   → Design: Min ‖W₁·S_sens‖∞ with robustness constraint
│   → Stability: ‖Ŝ·W‖∞ < 1/δ
│   → Uncertainty: Data-driven elliptic/convex hull models (Hilgemann 2024)
│
├─ Nonlinear distortion → Reduced feedback FLNN
│   → Design: Trigonometric expansion + periodic weight update
│   → Stability: Lipschitz condition on FLNN output
│
├─ Actuator-constrained → Constrained LMS or MPC
│   → Design: Projected gradient or QP with constraints
│   → Stability: Unconditional (bounded coefficients)
│
├─ Speech + feedback (AFC) → DeepPEM-AFC or Nested RNN
│   → Design: Neural observer for feedback path estimation
│   → Stability: Decorrelation (phase modulation / frequency shifting)
│
└─ Need dynamic step-size → Neural Kalman gain (Zhang 2024)
    → Design: Learned Q(n), R(n) for Kalman gain
    → Stability: Combine with constrained LMS safety net
```

### The Stability-Robustness-Performance Triangle

Every feedback ANC design faces the same trade-off:

```
              Performance (NR dB)
                   ▲
                  /│\
                 / │ \
                /  │  \
               /   │   \
    Robustness ◄────┼────► Stability
               \    │    /
                \   │   /
                 \  │  /
                  \ │ /
                   \│/
```

| Design | Performance | Robustness | Stability |
|--------|:----------:|:----------:|:---------:|
| MVC (fixed) | ★★★ | ★ | ★★★ |
| IMC + FxLMS | ★★★★ | ★★ | ★★ |
| H∞ robust | ★★ | ★★★★★ | ★★★★★ |
| Constrained LMS | ★★★ | ★★★★ | ★★★★ |
| Reduced FLNN | ★★★★ (nonlinear) | ★★ | ★★★ |

---

## Related Concepts

- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/acoustic-feedback|Acoustic Feedback]]
- [[concepts/internal-model-control|Internal Model Control]]
- [[concepts/adaptive-feedback-control|Adaptive Feedback Control]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/model-predictive-control|Model Predictive Control]]
- [[concepts/robust-adaptive-filtering|Robust Adaptive Filtering]]
- [[concepts/minimum-variance-control|Minimum Variance Control]]
- [[concepts/variable-step-size-lms|Variable Step Size LMS]]
- [[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]]
- [[concepts/uncertainty-modeling-for-anc|Uncertainty Modeling for ANC]]
- [[concepts/robust-stability-constraint|Robust Stability Constraint]]
- [[concepts/online-secondary-path-modeling|Online Secondary Path Modeling]]

## Related Synthesis

- [[adaptive-algorithm-tradeoffs|Adaptive Algorithm Trade-offs]]
- [[ai-driven-anc|AI-Driven ANC]]
- [[secondary-path-modeling-evolution|Secondary Path Modeling Evolution]]
- [[anc-architecture-evolution|ANC Architecture Evolution]]

## Related Sources

- [[sources/lu-2021-survey-active-noise-control-linear|Lu et al. 2021: Survey on ANC — Part I: Linear Systems]]
