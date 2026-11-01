---
type: source
created: 2026-11-01
updated: 2026-11-01
sources:
  - raw/papers/klatt-2025-laguerre-feedback-anc/full-text.md
  - https://doi.org/10.23919/EUSIPCO63237.2025.11226553
  - zotero://select/items/0_WTD24SX6
tags:
  - active-noise-control
  - feedback-anc
  - laguerre-filter
  - filter-design
  - filter-optimization
  - robust-control
  - internal-model-control
  - low-order-filter
---

# Klatt & Martin 2025: Laguerre Filter-based Robust Feedback Active Noise Control

**Authors**: [[entities/willem-alexander-klatt|Willem Alexander Klatt]]¹, [[entities/rainer-martin|Rainer Martin]]¹

**Affiliation**: ¹ Institute of Communication Acoustics, Ruhr-Universität Bochum, Bochum, Germany

**Venue**: 33rd European Signal Processing Conference (EUSIPCO 2025), pp. 386–390

**Year**: 2025

**Type**: Conference Paper

**DOI**: [10.23919/EUSIPCO63237.2025.11226553](https://doi.org/10.23919/EUSIPCO63237.2025.11226553)

**Zotero**: [WTD24SX6](zotero://select/items/0_WTD24SX6)

## Summary

This paper replaces the FIR control filter of an [[concepts/internal-model-control|Internal Model Control]] (IMC) feedback ANC controller with a [[concepts/laguerre-filter|Laguerre filter]] network — the first time Laguerre filters are combined with the IMC topology for FBANC (prior Laguerre-ANC work used non-IMC topologies). Because the Laguerre frequency response $Q_\ell(\mathrm{e}^{\mathrm{j}\Omega_k})$ is an affine function of the coefficient vector $\mathbf{q}$, the coefficients can be optimized by exactly the same convex program as FIR-based IMC designs, yet an order-17 Laguerre filter ($\alpha = 0.92$, 18 coefficients) matches the nominal noise attenuation of order-255/501 FIR-IMC designs and beats orders 63–255 at low frequencies. Robust stability is verified against 100 augmented secondary paths using a convex-set-based uncertainty model; gain/phase margins and non-nominal sensitivity behavior are comparable to FIR-IMC.

## Problem Formulation

Conventional IMC filter design for FBANC optimizes an FIR control filter $Q$ by minimizing the $W_d$-weighted magnitude-squared nominal sensitivity

$$
|S(\mathrm{e}^{\mathrm{j}\Omega_k})|^2 = \left| 1 - Q(\mathrm{e}^{\mathrm{j}\Omega_k}) \widehat{G}(\mathrm{e}^{\mathrm{j}\Omega_k}) \right|^2,
$$

where $\widehat{G}$ is the secondary path model. The optimum $Q = \widehat{G}^{-1}$ is unstable for non-minimum-phase plants (loudspeaker–microphone distances with spatial separation), and robust stability constraints further limit how close $Q$ may approach the optimum — so the design is effectively a constrained approximation of the inverse minimum-phase component of $\widehat{G}$.

At high sampling rates (here 48 kHz), an FIR $Q$ needs a **high order** to resolve low frequencies: each FIR tap buys a fixed spectral resolution, so attenuating a sub-1-kHz control band at 48 kHz wastes most taps on the inaudible upper spectrum. The paper asks: can a different filter basis achieve the same IMC-FBANC performance with far fewer coefficients, while keeping the optimization convex?

## Methodology

### Laguerre Network as the Control Filter

Any discrete-time system can be expanded in the Laguerre basis

$$
Q_\ell(z) = \sum_{m=0}^{M} q_m(\alpha)\, \Lambda_m(z, \alpha), \qquad
\Lambda_m(z, \alpha) = \sqrt{1 - \alpha^2} \, \frac{(z^{-1} - \alpha)^m}{(1 - \alpha z^{-1})^{m + 1}},
$$

where $\alpha \in (-1, 1)$ is the **Laguerre parameter** (the pole position of the all-pass sections). Key structural facts:

- $\alpha = 0$ reduces the network to a plain M-th order FIR filter
- The network is realized as a chain of all-pass sections behind a first-order low-pass input stage (Fig. 1) — the coefficient vector $\mathbf{q}(\alpha) = [q_0, \ldots, q_M]^{\mathsf{T}}$ multiplies a **generalized delay operator** $\boldsymbol{\Lambda}(z, \alpha)$
- On the unit circle, $Q_\ell(\mathrm{e}^{\mathrm{j}\Omega_k}) = \mathbf{q}^{\mathsf{T}} \boldsymbol{\Lambda}(\mathrm{e}^{\mathrm{j}\Omega_k}, \alpha)$ is **affine in $\mathbf{q}$**, so plugging it into the established IMC optimization preserves convexity

![[raw/papers/klatt-2025-laguerre-feedback-anc/figures/fd667c0363168201a8796e6970dcc7d072f12bac4f857f7eb2bae2b3f1ac0177.jpg|Laguerre network structure]]

*Figure 1: Laguerre network with coefficients $\mathbf{q} = q_0, q_1, \ldots, q_M$ that resemble a transversal filter of order M.*

### Choosing the Laguerre Parameter

In classical system identification, $\alpha$ is optimized against the target response. For IMC-FBANC the boundary conditions differ — minimize sensitivity given a secondary-path model, at minimal complexity — so the paper recommends **setting $\alpha$ as close to 1 as possible**: $\alpha$ is the pole of the low-pass input stage, so $\alpha \to 1$ gives a strongly low-pass-shaped basis that pre-emphasizes exactly the sub-1-kHz range where FBANC is physically feasible, and fewer stages are needed for the same transfer function.

A grid study over $(\alpha, M)$-pairs — $\alpha \in \{0, 0.25, 0.5, 0.75, 0.925, 0.95\} \times M \in \{15, 31, 47, 63, 79, 95\}$, i.e. 36 optimized controllers with the convex-set uncertainty model — evaluated the mean $W_d$-weighted nominal sensitivity. Performance improves monotonically with $\alpha$ and converges to the minimum for $0.75 \le \alpha < 1$ (Fig. 2).

![[raw/papers/klatt-2025-laguerre-feedback-anc/figures/0f676108fe44fda00f08f1c7498a1200c170d428feb9ad52c45ea8aeee1f6cce.jpg|Grid study of mean weighted sensitivity vs alpha and M]]

*Figure 2: Mean values of the $W_d$-weighted nominal sensitivity spectrum over the $(\alpha, M)$ grid.*

### IMC Topology and Optimization Problem

The controller embeds the Laguerre filter in the IMC structure (Fig. 3):

$$
C(z) = \frac{Q_\ell(z)}{1 - Q_\ell(z)\widehat{G}(z)},
$$

with sensitivity and complementary sensitivity

$$
S(z) = \frac{1 - Q_\ell(z)G(z)}{1 + Q_\ell(z)\Delta_G(z)}, \qquad
T(z) = \frac{Q_\ell(z)G(z)}{1 + Q_\ell(z)\Delta_G(z)}, \qquad S(z) + T(z) = 1,
$$

where $\Delta_G(z) = G(z) - \widehat{G}(z)$ is the model mismatch. The $S + T = 1$ identity is the fundamental dilemma of control: $S$ and $T$ cannot be simultaneously small.

![[raw/papers/klatt-2025-laguerre-feedback-anc/figures/4ad6dba3f015f8f1d7af2a5453afd10801f75560baf63d17a93e8916095e4f45.jpg|Feedback ANC block diagram with IMC controller]]

*Figure 3: Block diagram of the feedback active noise control system with the internal model filter topology of the controller C.*

The optimization is the standard [[concepts/q-parameterization|Q-parameterized]] convex program with the Laguerre substitution:

$$
\min_{\mathbf{q}} \; \frac{1}{N_\Omega} \sum_{k=0}^{N_\Omega - 1} \left| \left[ 1 - Q_\ell(\mathrm{e}^{\mathrm{j}\Omega_k}) \widehat{G}(\mathrm{e}^{\mathrm{j}\Omega_k}) \right] W_d(\mathrm{e}^{\mathrm{j}\Omega_k}) \right|^2
$$

subject to (for all $k$)

$$
\left| Q_\ell \widehat{G} W_T^{\chi} \right|^2 - 1 < 0 \quad \text{(robust stability)}, \qquad
\left| \left[ 1 - Q_\ell \widehat{G} \right] W_S \right|^2 - 1 < 0 \quad \text{(noise amplification limit)},
$$

where $W_d$ weights the expected noise spectrum, $W_S$ bounds amplification due to the [[concepts/waterbed-effect|waterbed effect]], and $W_T^{\chi}$ is the secondary-path uncertainty weight. Instead of the conventional disk (multiplicative) uncertainty model, the paper uses the **convex-set-based uncertainty model** of Klatt & Martin (EURASIP JASP 2025), in which frequency-dependent convex sets around the nominal open-loop response are computed dynamically during optimization. The secondary path model itself is a rational transfer function of order $N_G = 10$.

The problem is solved with an **SQP** active-set line-search algorithm with adaptive step-size control and BFGS Hessian estimates, terminated at a target objective of $10^{-4}$.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Sampling rate | $f_s = 48$ kHz |
| Secondary path data | Acoustic path database for ANC in-ear headphone development (Liebich et al. 2019) |
| Nominal secondary path | Average over all normal-fitting responses; identified via Steiglitz–McBride iteration, rational model of order $N_G = 10$ |
| Secondary path properties | Resonances at 150 Hz and 4 kHz; non-minimum phase (zeros outside the unit circle) |
| Disturbance weighting $W_d$ | Band-pass, 77–850 Hz |
| Amplification limit $W_S$ | Constant 0.625 (i.e. $1/W_S = 4$ dB) |
| Uncertainty model | Convex-set-based, dynamic ([Klatt & Martin 2025]) |
| Optimizer | SQP, active-set line search, BFGS Hessian, adaptive step size, stop at objective $10^{-4}$ |
| Laguerre design (L-IMC) | $M = 17$, $\alpha = 0.92$ |
| Baselines | FIR-IMC with $M = 63, 127, 255, 501$ |
| Non-nominal evaluation | $I = 100$ augmented secondary paths |

![[raw/papers/klatt-2025-laguerre-feedback-anc/figures/e19138747111ebfa842bfa80c90598e567e9faa27b66fd015db599a15879e311.jpg|Secondary path model magnitude and phase]]

*Figure 4: Frequency response of the secondary path model with order 10.*

For the non-nominal evaluation, artificial secondary paths are generated from pairs of measured impulse responses $g_1, g_2$ via data augmentation:

$$
\check{G}(\mathrm{e}^{\mathrm{j}\Omega_k}) = \frac{1}{2} \sum_{j=1}^{2} \mathrm{DFT}\left[ \gamma_j \, g_j(n + \Delta_j) \right],
\qquad \gamma_j \sim \mathcal{N}(1, 0.1^2), \quad \Delta_j \sim \mathcal{U}(-2, 2),
$$

which avoids evaluating the design on the same data used during optimization.

## Results

### Nominal Performance

The optimized L-IMC satisfies both constraint sets ($|T| < 1/|W_T^{\chi}|$ and $|S| < 1/|W_S|$ at every frequency):

- **3 dB noise attenuation bandwidth** ($|S| < 0.707$): ≈ **700 Hz**
- **20 dB noise attenuation bandwidth**: ≈ **250 Hz**
- Maximum attenuation is **on par with FIR-IMC orders 501 and 255**; low-frequency attenuation **exceeds FIR-IMC orders 255, 127, and 63** (Fig. 7)
- Without any additional regularization, L-IMC shows up to **24 dB less filter gain than FIR-IMC above 9 kHz** (at 20 kHz) — FIR designs must approximate $\widehat{G}^{-1}$, which blows up where $|\widehat{G}|$ is small, while the low-pass-shaped Laguerre basis does not

![[raw/papers/klatt-2025-laguerre-feedback-anc/figures/0cdcc2618fc00985168dbe5ecf60528fe38dd6152bcc9432a081890c2037cf77.jpg|L-IMC nominal sensitivity and complementary sensitivity with bounds]]

*Figure 6: Top: nominal sensitivity function of the Laguerre-based IMC design with noise amplification limit $1/W_S$. Bottom: nominal complementary sensitivity function of L-IMC with the associated uncertainty bound $1/W_T^{\chi}$.*

![[raw/papers/klatt-2025-laguerre-feedback-anc/figures/f63c31920c9a35739b5cb96bdf3b9667fc532b5098e1db2b9928ae3ed617907a.jpg|Sensitivity comparison FIR vs Laguerre]]

*Figure 7: Comparison of nominal IMC sensitivity functions of optimized FIR filters with order M = 63, 127, 255, 501 and the Laguerre filter with order M = 17.*

### Computational Complexity

In multiply–accumulate (MAC) operations per sample: Laguerre filter costs $2 + 4M$ MACs vs $M_{\mathrm{FIR}}$ MACs for FIR. With $M = 17$ (70 MACs) replacing $M_{\mathrm{FIR}} \ge 255$, this is roughly a **3.6× per-sample reduction** against the matched-performance FIR baseline.

### Non-Nominal Performance (Robustness)

Across $I = 100$ augmented secondary paths (Fig. 8):

- Nominal sensitivity ≈ the expected value of the non-nominal sensitivity set for both designs
- Below 800 Hz both designs perform similarly; L-IMC yields **slightly more amplification between 1–2 kHz**
- FIR-IMC shows a **peak at 3.6 kHz** — exactly the ear-canal resonance region, significant for in-the-ear devices — which L-IMC avoids
- Above 2 kHz, model mismatch causes less amplification for L-IMC; **above 10 kHz, no amplification at all**

![[raw/papers/klatt-2025-laguerre-feedback-anc/figures/741c63d70f85edd7d665c45bdc72fac3756df5827506df5aa6da5024f47a1ab5.jpg|Non-nominal sensitivity function sets FIR vs Laguerre]]

*Figure 8: Sets of sensitivity functions in the non-nominal case. Top: FIR filter-based IMC design. Bottom: Laguerre filter-based IMC design. Green/red lines indicate the minimum/maximum values of the sensitivity set.*

Gain and phase margins across all 100 paths:

| Margin | Statistic | FIR-IMC | L-IMC |
|:-------|:----------|:--------|:------|
| Gain margin (dB) | min | 2.34 | 3.69 |
| | max | 17.17 | 16.06 |
| | mean | 9.06 | 8.73 |
| Phase margin (deg) | min | 19.61 | 16.11 |
| | max | 74.56 | 68.47 |
| | mean | 45.87 | 36.95 |

Mean gain margins differ by only 0.3 dB; L-IMC's phase margins are lower overall, but **both designs remained stable in all experiments** — comparable robustness.

## Key Contributions

1. **First Laguerre–IMC combination for FBANC** — prior Laguerre-filter ANC work (Yuan 2007; Veena & Narasimhan 2007) used non-IMC feedforward/feedback topologies; this paper restructures the $Q$ filter inside the IMC feedback topology
2. **Convexity preservation** — because $Q_\ell(\mathrm{e}^{\mathrm{j}\Omega_k})$ is affine in $\mathbf{q}$, the existing convex IMC optimization machinery (robust stability + nominal performance constraints) applies unchanged to Laguerre coefficients
3. **Laguerre-parameter guidance** — a 36-controller $(\alpha, M)$ grid study showing disturbance attenuation improves monotonically with $\alpha$ and converges for $0.75 \le \alpha < 1$, justifying $\alpha$ close to 1 (low-pass pre-emphasis matched to the sub-1-kHz ANC control band)
4. **Order reduction with matched performance** — order-17 Laguerre ($\alpha = 0.92$) matches FIR orders 255–501 in maximum attenuation and beats orders 63–255 at low frequencies, at $2 + 4M$ MACs vs $M_{\mathrm{FIR}}$ MACs
5. **Intrinsic high-frequency gain control** — the Laguerre design needs no extra regularization to avoid the out-of-band $Q$-gain blowup that FIR designs suffer when approximating $\widehat{G}^{-1}$ (24 dB less gain at 20 kHz)
6. **Robustness verification** — non-nominal evaluation over 100 augmented secondary paths shows comparable gain/phase margins and stable behavior throughout, including avoiding the FIR design's 3.6 kHz amplification peak at the ear-canal resonance

## Related Concepts

- [[concepts/laguerre-filter|Laguerre Filter]]
- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/internal-model-control|Internal Model Control]]
- [[concepts/q-parameterization|Q-Parameterization]]
- [[concepts/sensitivity-function|Sensitivity Function]]
- [[concepts/robust-stability-constraint|Robust Stability Constraint]]
- [[concepts/uncertainty-modeling-for-anc|Uncertainty Modeling for ANC]]
- [[concepts/frequency-warping|Frequency Warping]]
- [[concepts/warped-fir-filter|Warped FIR Filter]]
- [[concepts/waterbed-effect|Waterbed Effect]]
- [[concepts/robust-control|Robust Control]]

## Related Synthesis

- [[synthesis/feedback-anc-filter-design|Feedback ANC Filter Design: Stability, Robustness, and Performance Trade-offs]]
- [[synthesis/iir-filter-fitting-frequency-response|IIR 滤波器拟合频响曲线：从测量到状态空间模型]]

## Related Sources

- [[sources/seo-2016-feedback-anc-constrained-optimization|Seo, Park & Youn 2016: Feedback ANC via Constrained Optimization for Headphones]] — the closest prior art: low-order feedback ANC via warping instead of Laguerre basis (16th-order WFIR ≈ 128th-order FIR)
- [[sources/hilgemann-2024-data-driven-uncertainty-anc|Hilgemann, Chatzimoustafa & Jax 2024: Data-Driven Uncertainty Modeling for Robust Feedback ANC]] — data-driven uncertainty models for the same IMC optimization framework
- [[sources/kuo-2006-anc-headphones|Kuo, Mitra & Gan 2006: Active Noise Control System for Headphone Applications]] — IMC-based feedback ANC headphone implementation
- [[sources/pawelczyk-1997-anc-feedback-fixed-adaptive|Pawelczyk 1997: ANC Feedback Fixed/Adaptive]] — fixed feedback controller benchmark
