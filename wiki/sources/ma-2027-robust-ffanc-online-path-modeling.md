---
type: source
created: 2026-07-15
updated: 2026-07-15
sources:
  - raw/papers/ma-2027-robust-ffanc-online-path-modeling/full-text.md
  - https://doi.org/10.1016/j.sigpro.2026.110818
  - zotero://select/items/0_953HRBRT
tags:
  - active-noise-control
  - feedforward-anc
  - online-secondary-path-modeling
  - online-feedback-path-modeling
  - supporting-filter
  - auxiliary-noise-scaling
  - adaptive-filtering
---

# Ma, Xiao, Wu, Ma & Khorasani 2027: Robust FFANC with Simultaneous Online Secondary- and Feedback-Path Modeling

**Authors**: [[entities/yaping-ma|Yaping Ma]], [[entities/yegui-xiao|Yegui Xiao]] (corresponding), [[entities/wenyi-wu|Wenyi Wu]], [[entities/liying-ma|Liying Ma]], [[entities/khashayar-khorasani|Khashayar Khorasani]]
**Affiliations**:
- a: Institute of Automation, Jiangnan University, Wuxi, 214122, China
- b: Dept. of Information Science, Prefectural University of Hiroshima, Hiroshima, 734-8558, Japan
- c: Beijing Aerospace Measurement & Control Technology Co., Ltd., Beijing, 100043, China
- d: Dept. of Electrical and Computer Engineering, Concordia University, Montreal, H3G 1M8, Canada

**Published**: *Signal Processing*, Vol. 214, 2027, Art. 110818 (DOI issued 2026)
**DOI**: [10.1016/j.sigpro.2026.110818](https://doi.org/10.1016/j.sigpro.2026.110818)
**URL**: [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0165168426003312)
**📎 Zotero**: [zotero://select/items/0_953HRBRT](zotero://select/items/0_953HRBRT)

## Summary

A new feedforward active noise control (FFANC) system is proposed that simultaneously performs online secondary-path modeling (OSPM) and online feedback-path modeling (OFBPM). Two key innovations over prior art (Ahmed–Akhtar 2013; Bai et al. 2019): (1) a **new FIR supporting filter (SF) $H_2(z)$** is added whose output $y_2(n)$ — a less noisy estimate of the remaining target noise — is used both to update the controller via FXLMS and to drive the auxiliary-noise (AWGN) scaling, thereby decoupling the FFANC controller from the OSPM subsystem; (2) a **global AWGN scaling scheme** driven by $y_2(n)$ instead of the residual error $e(n)$, significantly reducing the injected-AWGN contribution to the residual error. An approximate steady-state statistical analysis yields closed-form expressions for $E[y_2^2(\infty)]$, $G_s(\infty)$, and $E[e^2(\infty)]$, providing tuning insight. Simulations with synthetic paths, real IIR paths, and a real hybrid-car road-noise recording show that the proposed system matches the ideal-benchmark Sys-A (with true SP/FBP) within 0.01–2.4 dB and outperforms Sys-B (Ahmed–Akhtar 2013) by 3–6 dB in NRP while running faster (no divisions or square roots).

## Problem Formulation

The FFANC must contend with three physical paths:

- **Primary path (PP)** $P(z)$: from reference signal to residual error
- **Secondary path (SP)** $S(z)$: from secondary source to residual error — *time-varying in practice*
- **Feedback path (FBP)** $F(z)$: from secondary source back to reference microphone — *time-varying in practice*

When SP and FBP drift during operation, the fixed-estimate FFANC of [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999]] (Fig. 1) degrades or becomes unstable. Including OSPM and OFBPM simultaneously is technically demanding; only four prior FFANC architectures equipped with both had been published (Kuo–Ill 1999; Ahmed–Akhtar 2013; Xiao et al. 2019; Bai et al. 2019). The two recurring issues are:

- **I1 — Adverse coupling** between the FFANC controller and the OSPM subsystem (the residual error contains remaining target noise that acts as additive noise for OSPM).
- **I2 — Inadequate AWGN reduction**: prior AWGN scaling strategies are either "local" (driven by OSPM/OFBPM errors, Ahmed–Akhtar 2013) or "global" but driven by the residual error $e(n)$ which contains additive noise $v_p(n)$ (Bai et al. 2019).

The primary-noise / reference / feedback signals are

$$
p(n) = p_r(n) + v_p(n) = \sum_{j=0}^{M_p-1} s_{p,j}\, x_r(n-j) + v_p(n),
$$

$$
r(n) = x_r(n) + y_f(n), \qquad y_f(n) = \sum_{m=0}^{M_f-1} s_{f,m}\, y(n-m),
$$

with $x_r(n) = x_s(n) + x_b(n)$ composed of a narrowband component $x_s(n)$ (sum of $q$ sinewaves) and a broadband component $x_b(n)$ of variance $\sigma_b^2$. The residual error is $e(n) = p(n) - y_p(n)$, with $y_p(n)$ the $S(z)$-filtered secondary source.

![[raw/papers/ma-2027-robust-ffanc-online-path-modeling/figures/e1c73c9a0809e2f65eab201cff856bad83675f494803888c5e06be1ad38f0ca9.jpg|Figure 1: Original FFANC system with FBP compensation (Kuo 1999).]]
*Figure 1: Original FFANC system with FBP compensation [1].*

## Methodology

### System architecture

The proposed system (Fig. 4) consists of five subsystems:

1. **First SF $H_1(z)$** — extracts from the FBP-compensated signal $x(n)$ the remaining broadband component due to the injected AWGN (inherited from Ahmed–Akhtar 2013).
2. **Second SF $H_2(z)$** *(newly added)* — applied to the FBP-compensated reference $x(n)$; its output $y_2(n)$ is a less noisy estimate of the remaining target noise.
3. **FFANC subsystem** — FIR controller $W(z)$ updated by FXLMS but driven by $y_2(n)$ rather than $e(n)$.
4. **OSPM subsystem** — adaptive $\hat{S}_n(z)$, desired signal is $e_2(n) = e(n) - y_2(n)$ (the $H_2$ error).
5. **OFBPM subsystem** — adaptive $\hat{F}_n(z)$, driven by the same scaled AWGN $v(n)$.

![[raw/papers/ma-2027-robust-ffanc-online-path-modeling/figures/675fb056d02a2ce02a7390e84ea78b20a2b695962c705b14eb4a04db91a79adf.jpg|Figure 4: Proposed FFANC system with OSPM and OFBPM.]]
*Figure 4: Proposed FFANC system with simultaneous OSPM and OFBPM. The red-dashed square marks the newly added second SF $H_2(z)$; the green-dashed square marks the modified global AWGN scaling.*

### Second supporting filter $H_2(z)$

$$
y_2(n) = \sum_{j=0}^{L_2-1} h_{2,j}(n)\, x(n-j),
$$

updated by LMS using the OSPM error $e_s(n)$ (rather than $e_2(n)$) to mitigate mutual interference with $\hat{S}_n(z)$:

$$
h_{2,j}(n+1) = h_{2,j}(n) + \mu_2\, e_s(n)\, x(n-j), \qquad e_s(n) = e_2(n) + y_s(n), \quad e_2(n) = e(n) - y_2(n).
$$

The $H_2(z)$ error $e_2(n)$ serves *exclusively* as the OSPM desired signal — this is the key decoupling mechanism (feature F1).

### Controller update (modified FXLMS)

$$
w_j(n+1) = w_j(n) + \mu_c\, y_2(n)\, \hat{x}(n-1-j), \qquad \hat{x}(n) = \sum_{m=0}^{\hat{M}_s-1} \hat{s}_m(n)\, x(n-m).
$$

Using $y_2(n)$ instead of $e(n)$ substantially dampens the influence of $v_p(n)$ and the injected AWGN $v(n)$.

### Global AWGN scaling driven by $y_2(n)$

$$
G_s(n) = \alpha_d\, G_s(n-1) + \beta_d\, |y_2(n-1)|^{\gamma_d}, \qquad v(n) = G_s(n)\, v_o(n),
$$

where $v_o(n)$ is zero-mean AWGN with variance $\sigma_o^2$, and $\gamma_d \in \{1,2,3,4\}$. Because the additive noise $v_p(n)$ is *not* directly involved in $y_2(n)$, the steady-state $G_s(\infty)$ can converge to a lower level than the "local" scheme of Ahmed–Akhtar 2013 (Eq. 22) or the "global" scheme of Bai et al. 2019 (Eq. 37) — feature F2.

### Approximate steady-state analysis

Under a near-steady-state approximation (the first SF and OFBPM have converged, $v_p(n)$ dominates the residual error, and the unneutralized AWGN in $e_s(n)$ is negligible), the analysis yields

$$
E[h_{2,j}^2(\infty)] \approx \tfrac{1}{2}\, \mu_2\, \sigma_p^2 \quad \text{(for small } \mu_2 \text{)},
$$

$$
E[y_2^2(\infty)] \approx \tfrac{1}{2}\, \mu_2\, \sigma_p^2\, L_2\, P_{x_r}, \qquad P_{x_r} = \tfrac{1}{2}\sum_{i=1}^{q} A_i^2 + \sigma_b^2,
$$

$$
G_s(\infty) \approx \frac{\beta_d\, \mu_2}{2(1-\alpha_d)}\, \sigma_p^2\, L_2\, P_{x_r},
$$

$$
E[e^2(\infty)] \approx \sigma_p^2 + \frac{1}{4}\, \mu_2^2\, \sigma_p^4\, \sigma_o^2\, L_2^2\, P_{x_r}^2 \left(\frac{\beta_d}{1-\alpha_d}\right)^2 \sum_{m=0}^{M-1} s_m^2.
$$

Key observation (O3): when $\tfrac{1}{2}\,\mu_2\, L_2\, P_{x_r} \ll 1$, the driving term of the proposed scaling is smaller than those in both Eq. (22) and Eq. (37), so the proposed system injects less AWGN — directly improving NRP.

## Experimental Setup

| Item | Case 1 (synthetic) | Case 2 (FIR-est. real paths) | Case 3 (real IIR + real noise) |
|------|--------------------|------------------------------|--------------------------------|
| **Noise** | 5 sinewaves $\{0.10, 0.15, 0.30, 0.40, 0.45\}\pi$ + white $x_b$ ($\sigma_b^2=0.001$); additive $\sigma_p^2=0.01$ | same sinewaves; $\sigma_b^2=0.002$; $\sigma_p^2=0.1$ | Real hybrid-car road noise @ 4 kHz; $\sigma_p^2=2\%$ of $p(n)$ |
| **Paths** | FIR `fir1`, cutoff 0.4π; $M_p=48$, $M_s=21/19$, $M_f=32/30$ (1st/2nd half) | FIR estimates of 3 real IIR paths from Kuo 1996; $M_p=48$, $M_s=16$, $M_f=32$ | Real IIR paths from Kuo 1996 |
| **AWGN** $\sigma_o^2$ | 1.0 | 1.0 | 0.5 |
| **Adaptation** $N$ | 70,000 | 70,000 | 240,000 |
| **NRP eval.** | last 7,000 samples | last 7,000 samples | last 20,000 samples |
| **Runs** | 100 | 100 | 100 |
| **OSPM/OFBPM lengths** | $\hat{M}_s=31$, $\hat{M}_f=42$ | $\hat{M}_s=18$, $\hat{M}_f=35$ | $\hat{M}_s=\hat{M}_f=128$ |
| **Abrupt changes** | SP & FBP swap mid-run | SP & FBP swap mid-run | IIR SP & FBP swap mid-run; **refreshment scheme** (Eqs. 93–95) required for Sys-B and Sys-D |
| **Compared systems** | Sys-A (Kuo 1999), Sys-B (Ahmed 2013), Sys-C (Bai 2019, narrowband only), Sys-D (proposed) | Same as Case 1 | Sys-A, Sys-B, Sys-D (Sys-C excluded — narrowband only) |

The four systems are tuned so that Sys-B and Sys-D have *similar* convergence rate to Sys-A; the steady-state NRP is then compared.

## Results

### NRP summary (dB; lower is better)

| System | Case 1 (1st/2nd half) | Case 2 (1st/2nd half) | Case 3 (1st/2nd half) |
|--------|----------------------|----------------------|----------------------|
| **Sys-A** (ideal SP/FBP) | −21.08 / −21.07 | −21.38 / −21.39 | −14.31 / −13.15 |
| **Sys-B** (Ahmed 2013) | −18.08 / −18.07 | −17.29 / −17.27 | −8.13 / −7.82 *(requires known SP/FBP for 2nd-half init.)* |
| **Sys-C** (Bai 2019, narrowband) | −20.03 / −19.41 | −16.38 / −18.71 | n/a |
| **Sys-D** (proposed) | **−21.07 / −21.07** | **−21.05 / −21.00** | **−11.94 / −12.52** |

### Per-iteration running time

| Case | Sys-A | Sys-B | Sys-C | Sys-D |
|------|-------|-------|-------|-------|
| 1 | 1.42e-5 s | 8.46e-5 s | 1.15e-4 s | **6.17e-5 s** |
| 2 | 1.66e-5 s | 6.43e-5 s | 6.62e-5 s | **3.69e-5 s** |
| 3 | 1.89e-5 s | 8.85e-4 s | — | **1.04e-4 s** |

### Key findings (D1–D6)

- **D1**: Sys-D significantly outperforms Sys-B and Sys-C in mean residual error and NRP for *every* one of 100 runs; convergence is comparable to or slightly faster than Sys-B.
- **D2**: Steady-state scaling factor $G_s(\infty)$ of Sys-D is much smaller than Sys-C, confirming lower AWGN contribution to the residual noise.
- **D3**: OSPM/OFBPM MSE convergence of Sys-D is similar to Sys-B in Cases 1–2; in Case 3 (real IIR paths), Sys-B is given an *unfair* advantage (pre-initialized SP/FBP for 2nd half) yet its OSPM/OFBPM advantage over Sys-D remains limited.
- **D4**: The closed-form expressions (84)–(86) match simulations within ~23% (scaling factor) and ~15% ($y_2$ and $e$ powers) over wide parameter ranges.
- **D5**: Sys-D is the fastest among Sys-B/C/D because it requires *no divisions or square roots* (Sys-B needs 2 each; Sys-C needs $q$ divisions).
- **D6**: The refreshment scheme (Eqs. 93–95) is essential for surviving abrupt IIR path changes in Case 3 but is not a panacea — proper selection of $\alpha_d, \beta_d, \gamma_d$ is still required.

## Key Contributions

1. **New second supporting filter $H_2(z)$** applied to the FBP-compensated reference; its output $y_2(n)$ (a less noisy estimate of the remaining target noise) is used (i) to update the controller via FXLMS, (ii) as the OSPM desired-signal source via $e_2(n)$, and (iii) to drive the AWGN scaling — substantially decoupling the controller from the OSPM (feature F1).
2. **Global AWGN scaling driven by $y_2(n)$** instead of the residual error; because the additive noise $v_p(n)$ is not directly in $y_2(n)$, $G_s(\infty)$ converges to a lower level, reducing the injected-AWGN contribution to the residual error (feature F2).
3. **Use of $e_s(n)$ to update both OSPM and $H_2(z)$**, reducing the interference between $H_2(z)$ and $\hat{S}_n(z)$ (feature F3).
4. **Null-vector initialization** of OSPM and OFBPM filters is admissible (feature F4), unlike the delicate proportional-to-truth initialization required by Sys-B.
5. **Approximate steady-state statistical analysis** yielding closed-form expressions for $E[y_2^2(\infty)]$, $G_s(\infty)$, and $E[e^2(\infty)]$ — provides tuning guidance and *analytically* shows why the proposed scaling outperforms priors (observation O3).
6. **Extensive validation** with synthetic paths, real IIR paths, and a real hybrid-car road-noise recording; Sys-D matches the ideal Sys-A within 0.01–2.4 dB while running faster than Sys-B and Sys-C.

## Related Concepts

- [[concepts/feedforward-anc|Feedforward ANC]] — host architecture
- [[concepts/active-noise-control|Active Noise Control]] — parent domain
- [[concepts/online-secondary-path-modeling|Online Secondary-Path Modeling]] (OSPM) — one of two online modeling sub-problems tackled
- [[concepts/online-feedback-path-modeling|Online Feedback-Path Modeling]] (OFBPM) — newly created concept page; the second online modeling sub-problem
- [[concepts/supporting-filter-anc|Supporting Filter in ANC]] — newly created concept page covering the $H_1$/$H_2$ SF mechanism
- [[concepts/auxiliary-noise-scaling|Auxiliary Noise Scaling]] — newly created concept page covering the AWGN scheduling strategies compared in this paper
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the physical phenomenon OFBPM compensates
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — controller update rule (modified to use $y_2(n)$)
- [[concepts/secondary-path-modeling|Secondary Path Modeling]] — broader context
- [[concepts/adaptive-feedback-control|Adaptive Feedback Control]] — related feedback ANC paradigm

## Related Synthesis

- [[synthesis/anc-architecture-evolution|ANC Architecture Evolution]] — situates the proposed system within the broader FFANC → FBANC → HANC taxonomy; the simultaneous OSPM+OFBPM extension represents an architectural refinement of the basic feedforward paradigm for time-varying environments
