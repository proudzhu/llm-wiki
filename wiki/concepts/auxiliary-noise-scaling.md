---
type: concept
created: 2026-07-15
updated: 2026-07-15
sources:
  - raw/papers/ma-2027-robust-ffanc-online-path-modeling/full-text.md
tags:
  - active-noise-control
  - adaptive-filtering
  - online-modeling
  - auxiliary-noise
---

# Auxiliary Noise Scaling

## Overview

**Auxiliary noise scaling** (also called *AWGN power scheduling* or *AWGN scaling*) in active noise control refers to dynamic adjustment of the gain $G_s(n)$ applied to the auxiliary white Gaussian noise (AWGN) $v_o(n)$ injected into the secondary source for [[online-secondary-path-modeling|OSPM]] and [[online-feedback-path-modeling|OFBPM]]. The scaled AWGN

$$
v(n) = G_s(n)\, v_o(n)
$$

serves as the common excitation signal for both online modeling sub-systems, but it also leaks directly into the residual error $e(n)$ — degrading the noise-reduction performance (NRP). The central trade-off is:

- **Too much $v(n)$**: accurate OSPM/OFBPM, but high residual-AWGN floor → low NRP
- **Too little $v(n)$**: poor OSPM/OFBPM tracking → controller divergence or instability

## Two Families of Strategies

### 1. Local Scheduling (Zhang 2003; Ahmed–Akhtar 2013, Eq. 22)

Driven by the OSPM and OFBPM **modeling error powers**:

$$
G_s(n) = \alpha\, G_s(n-1) + \gamma \max\!\left\{ \sqrt{\frac{P_{e_1}(n-1)}{\sum_m \hat{s}_{f,m}^2(n)}},\; \sqrt{\frac{P_{e_s}(n-1)}{\sum_m \hat{s}_m^2(n)}} \right\},
$$

with $P_{e_1}, P_{e_s}$ exponentially smoothed error powers. **Aim**: minimize the *modeling* error powers — hence "local". Does **not** directly target the global residual error.

### 2. Global Scheduling

Driven by a nonlinear function of a *global* signal (the residual error or a supporting-filter output):

$$
G_s(n) = \alpha\, G_s(n-1) + \beta\, |\text{driver}(n-1)|^{\gamma}.
$$

- **Bai 2019 (Eq. 37)** — driver = residual error $e(n)$. Directly targets the global residual but is contaminated by the additive noise $v_p(n)$, which keeps $G_s(\infty)$ elevated.
- **Ma 2027 (Eq. 43)** — driver = second SF output $y_2(n)$. The additive noise $v_p(n)$ is *not* directly in $y_2(n)$, so the steady-state scaling factor

$$
G_s(\infty) \approx \frac{\beta_d\, \mu_2}{2(1-\alpha_d)}\, \sigma_p^2\, L_2\, P_{x_r}
$$

can be made much smaller than in the local scheme or in Bai 2019's residual-driven scheme, *provided* $\tfrac{1}{2}\mu_2 L_2 P_{x_r} \ll 1$ (observation O3 in Ma 2027). The injected-AWGN contribution to the residual is

$$
P_v(\infty) = \sigma_o^2\, G_s^2(\infty) \sum_{m=0}^{M-1} s_m^2,
$$

so a smaller $G_s(\infty)$ directly improves NRP.

## User Parameters

The three parameters $\{\alpha, \beta, \gamma\}$ (or $\{\alpha_d, \beta_d, \gamma_d\}$ in Ma 2027) govern the scaling dynamics:

- $\alpha$ (closer to 1 → slower startup from 0, higher peak, but smoother)
- $\beta$ (larger → larger scaling factor)
- $\gamma \in \{1, 2, 3, 4\}$ (nonlinearity order; integers < 4 are typical)

The steady-state scaling factor is proportional to $\beta/(1-\alpha)$. A trial-and-error process is inevitable in real applications to balance startup speed, peak height, and steady-state level.

## Comparison Table (Ma 2027 Table 1 + Discussion)

| Scheme | Driver | Pros | Cons |
|--------|--------|------|------|
| **Local (Ahmed 2013)** | OSPM & OFBPM error powers | Direct control of modeling accuracy | Local — does not target global residual; requires 2 divisions + 2 square roots per iteration |
| **Global, residual-driven (Bai 2019)** | $\|e(n)\|^{\gamma_c}$ | Direct global target | Contaminated by $v_p(n)$ → elevated $G_s(\infty)$; requires $q$ divisions |
| **Global, SF-driven (Ma 2027)** | $\|y_2(n)\|^{\gamma_d}$ | Decoupled from $v_p(n)$ → lowest $G_s(\infty)$; **no divisions or square roots** | Requires additional SF $H_2(z)$; user-parameter tuning still needed |

## Initialization Coupling

In Ahmed–Akhtar 2013, the local scheduling uses $\sum_m \hat{s}_{f,m}^2(n)$ and $\sum_m \hat{s}_m^2(n)$ in the denominator, which **cannot be zero** — hence the OFBPM and OSPM filters cannot be initialized to null vectors. The Ma 2027 global scheme removes this constraint, enabling null-vector initialization (feature F4).

## Related Concepts

- [[online-secondary-path-modeling|Online Secondary-Path Modeling]] — primary consumer of the scaled AWGN
- [[online-feedback-path-modeling|Online Feedback-Path Modeling]] — secondary consumer of the scaled AWGN
- [[supporting-filter-anc|Supporting Filter in ANC]] — the SF $H_2(z)$ whose output drives the Ma 2027 scaling
- [[variable-step-size-lms|Variable Step Size LMS]] — related adaptive step-size idea in the LMS family
- [[feedforward-anc|Feedforward ANC]] — host architecture

## Related Sources

- [[sources/ma-2027-robust-ffanc-online-path-modeling|Ma 2027: Robust FFANC with Simultaneous OSPM and OFBPM]] — introduces the SF-driven global scaling and derives its steady-state statistics
- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section VI discusses early online secondary-path modeling and the AWGN injection trade-off
