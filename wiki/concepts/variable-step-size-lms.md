---
type: concept
created: 2026-04-27
updated: 2026-04-27
sources:
  - raw/papers/akhtar-2006-vss-lms-online-spm/full-text.txt
tags:
  - adaptive-filtering
  - lms-algorithm
  - variable-step-size
  - active-noise-control
---

# Variable Step Size LMS

**Variable Step Size (VSS) LMS** algorithms dynamically adjust the step-size parameter $\mu(n)$ during adaptation, balancing convergence speed and steady-state misadjustment.

## Conventional VSS Strategy

Most VSS algorithms (Kwong-Johnston 1992, Aboulnasr-Mayyas 1997, Pazaitis-Constantinides 1999, Ang-Boroujeny 2001, Koike 2002) follow the same principle:

- **Initially**: Large $\mu$ → fast convergence
- **Steady state**: Small $\mu$ → low misadjustment

This is appropriate when the desired response has stationary or slowly varying statistics.

## Inverse VSS Strategy (Akhtar 2006)

In online secondary path modeling for ANC, the disturbance in the modeling filter's desired response is **decreasing in nature** (ideally converging to zero). Akhtar's VSS LMS algorithm uses the **opposite** strategy:

- **Initially**: Small $\mu$ → avoid instability when disturbance is large
- **Later**: Large $\mu$ → fast convergence when disturbance has decreased

### Step Size Mechanism

$$\mu(n) = \text{clip}\left[\alpha(n),\ \mu_{\min},\ \mu_{\max}\right]$$

where $\alpha(n) = 1 - \frac{\hat{P}_e(n)}{\hat{P}_{e_s}(n)}$ tracks the ratio of residual error power to modeling error power.

- Initially: $\hat{P}_e \approx \hat{P}_{e_s}$ → $\alpha \approx 0$ → $\mu = \mu_{\min}$
- Steady state: $\hat{P}_e \gg \hat{P}_{e_s}$ → $\alpha \to 1$ → $\mu = \mu_{\max}$

### Comparison with NLMS

NLMS varies the step size with the **power of the reference signal**. Akhtar's VSS LMS varies it with the **power of the disturbance signal** in the desired response — a fundamentally different criterion.

## Performance

In ANC online secondary path modeling:
- Achieves −12.35 dB NMSE (cited in Fareedha 2026)
- Outperformed by [[../concepts/deep-secondary-path-estimation|DeepSPE]] which achieves −16.27 dB NMSE

## Related Concepts

- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[../concepts/online-secondary-path-modeling|Online Secondary-Path Modeling]]
- [[../concepts/deep-secondary-path-estimation|Deep Secondary Path Estimation]]
- [[../concepts/active-noise-control|Active Noise Control]]

## Related Sources

- [[../sources/akhtar-2006-vss-lms-online-spm|Akhtar 2006: VSS LMS for Online Secondary Path Modeling]]
- [[../sources/fareedha-2026-joint-deep-spe-anc|Fareedha 2026: Joint Deep SPE and Adaptive Control for ANC]]
