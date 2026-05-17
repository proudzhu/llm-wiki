---
type: concept
created: 2026-05-17
updated: 2026-05-17
tags:
  - active-noise-control
  - adaptive-filtering
  - signal-processing
---

# Online Secondary Path Estimation

## Overview

**Online secondary path estimation** refers to the continuous adaptation of the secondary path model $\hat{S}(z)$ in an [[concepts/active-noise-control|Active Noise Control]] system while it operates, as opposed to offline pre-calibration. This is necessary when the secondary path varies due to environmental changes, temperature, or mechanical drift.

## Why Online?

In many real-world ANC applications, the secondary path $S(z)$ (from the anti-noise loudspeaker to the error microphone) changes over time. Offline estimation cannot track these changes, leading to degraded noise reduction — or even instability if the phase error exceeds $\pi/2$.

## Main Approaches

### 1. Auxiliary Noise Injection

White Gaussian noise is injected as a probe signal to continuously identify $S(z)$ via system identification. The injected noise itself contributes to the residual error, so its power must be carefully managed.

- **Fixed power**: Simple but degrades steady-state noise reduction
- **Variable power**: Reduces injected noise when the secondary path is stable (e.g., [[concepts/offline-secondary-path-modeling|Offline Secondary Path Modeling]] switching)
- **Power scheduling**: Adaptive control of injection level based on convergence state

### 2. Modified FxLMS (MFxLMS)

Akhtar's MFxLMS algorithm (2006) uses an additional filter to reduce interference from the ANC controller in the secondary path estimation, improving the signal-to-noise ratio for the estimation filter.

### 3. Mirror-FxLMS

A family of algorithms that switch between MoFxLMS (stable under high modeling error) and MMoFxLMS (fast convergence regardless of modeling error) based on weight coefficient magnitudes. Phase-locked loop (PLL) enhances tracking.

### 4. Parameter-Free Methods

- **Least squares (LS)** with maximum likelihood (ML) — requires one parameter
- **Maximum a posteriori (MAP)** — Bayesian, stable
- **Tuning-less LS** — zero parameters, easy implementation

### 5. LMS-Newton and Selective Updating

The filtered-x LMS-Newton algorithm converges faster for highly correlated inputs (identical to RLS when $2\mu = 1-\lambda$). Selective updating (set-membership filtering with a threshold) reduces per-iteration complexity.

## Key Challenges

- **Injected noise vs. convergence speed**: More injected noise gives faster estimation but worsens ANC performance
- **Computational cost**: Online estimation adds filtering operations per iteration
- **Stability bound**: Modeling error shrinks the stable step-size range

## Related Concepts

- [[concepts/offline-secondary-path-modeling|Offline Secondary Path Modeling]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/active-noise-control|Active Noise Control]]

## Related Sources

- [[sources/lu-2021-survey-active-noise-control-linear|Lu et al. 2021: Survey on ANC — Part I: Linear Systems]]
