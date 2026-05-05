---
type: source
created: 2026-04-27
updated: 2026-04-27
sources:
  - raw/papers/akhtar-2006-vss-lms-online-spm/full-text.txt
  - https://ieeexplore.ieee.org/document/1585805
  - zotero://select/items/0_9PFUVDQJ
tags:
  - active-noise-control
  - secondary-path-estimation
  - variable-step-size
  - lms-algorithm
  - online-modeling
  - adaptive-filtering
---

# Akhtar, Abe & Kawamata 2006: VSS LMS for Online Secondary Path Modeling

**Authors**: [[../entities/muhammad-tahir-akhtar|Muhammad Tahir Akhtar]], [[../entities/masahide-abe|Masahide Abe]], [[../entities/masayuki-kawamata|Masayuki Kawamata]]
**Institutions**: Graduate School of Engineering, Tohoku University, Sendai, Japan
**Published**: IEEE Transactions on Audio, Speech, and Language Processing, vol. 14, no. 2, pp. 720–726, March 2006
**Type**: Journal Article
**DOI**: [10.1109/TSA.2005.855829](https://doi.org/10.1109/TSA.2005.855829)
**Zotero**: [9PFUVDQJ](zotero://select/items/0_9PFUVDQJ)

---

## Summary

This paper proposes a two-adaptive-filter method for online secondary path modeling in ANC systems, replacing the three-filter structure of existing methods (Zhang et al. 2001). The key innovations are: (1) using the **Modified-FxLMS (MFxLMS)** algorithm for the noise control filter, which allows larger step sizes and faster convergence than standard FxLMS; and (2) a novel **Variable Step Size (VSS) LMS** algorithm for the modeling filter that starts with a small step size (when disturbance is large) and increases it as the disturbance decreases — the opposite of conventional VSS strategies.

---

## Problem Formulation

### Existing Methods: Three-Filter Structure

Prior methods (Eriksson 1989, Bao 1993, Kuo 1997, Zhang 2001) for online secondary path modeling use **three adaptive filters**:
1. **Noise control filter** $W(z)$ — adapted via FxLMS
2. **Secondary path modeling filter** $\hat{S}(z)$ — adapted via LMS with auxiliary noise injection
3. **Third filter** — used to reduce cross-interference between control and modeling processes

Zhang's cross-updated method (2001) gives the best performance among three-filter methods but adds design complexity.

### Key Issues with Three-Filter Methods
- Increased design complexity
- The auxiliary noise $v(n)$ appears in the residual error, constraining it to low levels and causing slow convergence
- Control and modeling processes intrude on each other

---

## Methodology

### 1. Two-Filter Architecture

The proposed method uses only **two adaptive filters**:
- **Control filter** $W(z)$: adapted via MFxLMS algorithm
- **Modeling filter** $\hat{S}(z)$: adapted via the new VSS LMS algorithm

Two additional **fixed FIR filters** $\hat{S}'(z)$ and $W'(z)$ are used in the MFxLMS structure (not adaptive — copies of the current estimates).

### 2. Modified-FxLMS (MFxLMS) for Control Filter

In standard FxLMS, the secondary path delay reduces the upper bound for the step size from $\mu_{\max} = 1/(L \cdot P_{x'})$ to $\mu_{\max} = 1/(\Delta \cdot P_{x'})$, where $\Delta$ is the delay introduced by $S(z)$.

MFxLMS uses two extra fixed filters:
- $\hat{S}'(z)$: generates a modified error signal for $W(z)$
- $W'(z)$: avoids FxLMS adaptation

The control filter is adapted using **simple LMS** (not FxLMS), so the upper bound for the step size is larger → **faster convergence**.

### 3. VSS LMS Algorithm for Modeling Filter

**Core insight**: The disturbance signal $d'(n) = d(n) - y'(n)$ in the desired response of the modeling filter is **decreasing in nature** (ideally converging to zero). Therefore:
- **Initially**: Large disturbance → use **small** step size to avoid instability
- **Later**: Small disturbance → use **large** step size for fast convergence

This is the **opposite** of conventional VSS algorithms (Kwong-Johnston, Aboulnasr-Mayyas, etc.) which start large and decrease.

**Step size mechanism**:

$$\mu(n) = \begin{cases} \mu_{\min} & \text{if } \alpha(n) \leq \mu_{\min} \\ \alpha(n) & \text{if } \mu_{\min} < \alpha(n) < \mu_{\max} \\ \mu_{\max} & \text{if } \alpha(n) \geq \mu_{\max} \end{cases}$$

where $\alpha(n) = 1 - \frac{\hat{P}_e(n)}{\hat{P}_{e_s}(n)}$, with:
- $\hat{P}_e(n)$: estimated power of residual error signal $e(n)$
- $\hat{P}_{e_s}(n)$: estimated power of modeling error signal $e_s(n)$

Power estimates use exponential forgetting:
$$\hat{P}_e(n) = \lambda \hat{P}_e(n-1) + (1-\lambda) e^2(n)$$
$$\hat{P}_{e_s}(n) = \lambda \hat{P}_{e_s}(n-1) + (1-\lambda) e_s^2(n)$$

**Initialization**: Both estimators initialized to the same value (preferably unity) to ensure $\mu(0) = \mu_{\min}$.

### 4. Mutual Convergence Dependence

The error signal for both filters is the same: $e_s(n)$. Analysis shows:
- $W(z)$ converges to optimal $\iff$ modeling error reduces to zero
- Modeling error reduces to zero $\iff$ $W(z)$ converges to optimal

The convergence of control and modeling filters is **mutually dependent**.

---

## Computational Complexity

| Method | Multiplications | Additions |
|:-------|:---------------|:----------|
| Eriksson | $2L + 2M$ | $2L + 2M - 2$ |
| Kuo | $2L + 3M$ | $2L + 3M - 2$ |
| Zhang | $2L + 2M + 2J + 2$ | $2L + 2M + 2J$ |
| **Proposed** | $2L + 2M + 2M + 6$ | $2L + 2M + 2M + 2$ |

Where $L$, $M$, $J$ are tap-weight lengths of $W(z)$, $\hat{S}(z)$, and the third filter respectively. The proposed method avoids the third adaptive filter but adds two fixed FIR filters, making complexity comparable to Zhang's method.

---

## Experimental Results

### Setup
- Primary path $P(z)$: FIR, 48 taps
- Secondary path $S(z)$: FIR, 16 taps
- Control filter: $L = 48$ taps
- Modeling filter: $M = 16$ taps
- Sampling frequency: 2 kHz
- Auxiliary noise: white Gaussian, variance 0.05
- Results averaged over 10 experiments

### Case 1: Tonal Reference (300 Hz)
- Proposed method achieves faster modeling error convergence than Zhang's method
- Step size starts small, increases toward $\mu_{\max}$

### Case 2: Narrowband Reference (100, 200, 300, 400 Hz)
- Similar improvement over Zhang's method

### Case 3: Broadband Reference (100–400 Hz bandpass filtered)
- Performance comparable to Zhang's method

### Case 4: Time-Varying Acoustic Paths
- At $n = 20000$, both $P(z)$ and $S(z)$ change
- Proposed method gives better performance before and after the change
- Step size drops to $\mu_{\min}$ at the path change, then recovers toward $\mu_{\max}$

---

## Key Contributions

1. **Two-filter structure**: Eliminates the third adaptive filter while maintaining or improving performance
2. **MFxLMS for control**: Larger step size bound → faster convergence than standard FxLMS
3. **Inverse VSS strategy**: Small-to-large step size, exploiting the decreasing nature of the disturbance signal — fundamentally different from conventional VSS approaches
4. **Mutual convergence**: Theoretical analysis showing control and modeling filter convergence are interdependent

---

## Limitations

- Requires offline pre-modeling (5 dB modeling error) to initialize $\hat{S}(z)$ before online operation
- Slightly higher computational complexity than three-filter methods due to MFxLMS structure
- VSS bounds $\mu_{\min}$ and $\mu_{\max}$ must be experimentally determined

---

## Related Concepts

- [[../concepts/online-secondary-path-modeling|Online Secondary-Path Modeling]]
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[../concepts/variable-step-size-lms|Variable Step Size LMS]]
- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/secondary-path-modeling|Secondary Path Modeling]]

## Related Sources

- [[../sources/fareedha-2026-joint-deep-spe-anc|Fareedha 2026: Joint Deep SPE and Adaptive Control for ANC]] — DeepSPE outperforms Akhtar's VSS-LMS by 3.92 dB NMSE

## Related Entities

- [[../entities/muhammad-tahir-akhtar|Muhammad Tahir Akhtar]]
- [[../entities/masahide-abe|Masahide Abe]]
- [[../entities/masayuki-kawamata|Masayuki Kawamata]]
