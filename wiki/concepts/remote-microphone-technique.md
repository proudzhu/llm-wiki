---
type: concept
created: 2026-04-29
updated: 2026-05-27
tags:
  - virtual-sensing
  - anc
  - remote-microphone
  - observation-filter
---

# Remote Microphone Technique

The **Remote Microphone Technique (RMT)** is a virtual sensing method that estimates the error signal at a target (virtual) location using signals from nearby physical microphones combined with domain knowledge of the acoustic paths and an **observation filter** $\mathbf{O}(z)$.

## Formulation

### Signal Model

The residual noise at the listener's (virtual error) position is decomposed into contributions from the primary noise sources and the control signal:

$$E(z) = D_e(z) + G_e(z)U(z)$$

where $E(z)$, $D_e(z)$, and $U(z)$ are the $z$-transforms of the residual error, primary disturbances at the virtual position, and control signal respectively, and $G_e(z)$ is the secondary path to the virtual position.

### Remote Microphone Signals

The $R$ physical remote microphones capture:

$$\mathbf{M}(z) = \mathbf{D}_m(z) + \mathbf{G}_m(z)U(z)$$

where $\mathbf{M}(z) = [M_0(z), ..., M_{R-1}(z)]^T$, $\mathbf{D}_m(z)$ are the primary disturbances at the remote positions, and $\mathbf{G}_m(z) = [G_{m,0}(z), ..., G_{m,R-1}(z)]^T$ are the secondary paths to the remote microphones.

### Observation Filter

By subtracting the filtered control signal (using modeled secondary paths $\hat{\mathbf{G}}_m(z)$), the primary disturbances at the remote positions are extracted:

$$\hat{\mathbf{D}}_m(z) = \mathbf{M}(z) - \hat{\mathbf{G}}_m(z)U(z)$$

These are processed by the **observation filter** $\mathbf{O}(z) = [O_0(z), O_1(z), ..., O_{R-1}(z)]$ to estimate the primary disturbances at the virtual error microphone:

$$\hat{D}_e(z) = \mathbf{O}(z) \hat{\mathbf{D}}_m(z)$$

Finally, the filtered control signal at the virtual position is added to obtain the estimated residual error:

$$\hat{E}(z) = \hat{D}_e(z) + \hat{G}_e(z)U(z)$$

### Filter Estimation

Conventionally, the observation filter is computed in a training phase using recordings of primary disturbances at both remote and virtual microphone positions. Filters are estimated via cross-correlations [22] or cross-spectral densities (CSDs) [23] between remote and virtual error microphones, forming an inverse problem.

## Limitations

- Fixed compensation filter assumes stationary acoustic paths
- Sensitive to changes in noise characteristics and acoustic environment
- Requires accurate estimation of transfer functions
- Pre-computed filter databases for multiple scenarios become large and require selection logic
- Conventional filters are tied to specific virtual microphone positions

## Neural Observation Filters

Recent advances replace the pre-computed filter bank with a neural network that estimates $\mathbf{O}(z)$ online:

- **CNN-based** (Holzmuller & Sontacchi 2025): Encoder-decoder CNN takes GCC-PHAT features + virtual microphone coordinates as input, outputs FIR coefficients asynchronously (every 500ms)
- **Obs-TasNet** (Holzmuller & Sontacchi 2026): Modified Conv-TasNet architecture reduces parameters by ~40% while improving estimation accuracy

## Related Concepts

- [[concepts/virtual-sensing|Virtual Sensing]]
- [[concepts/relative-path-virtual-sensing|Relative Path Virtual Sensing]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/neural-observation-filter|Neural Observation Filter]]

## Related Sources

- [[sources/a-review-of-virtual-sensing-algorithms-for-active-|Moreau 2008: Review of Virtual Sensing Algorithms for ANC]]
- [[sources/toyooka-2026-hybrid-anc-remote-sensing|Toyooka 2026: Hybrid ANC with Dual Compensation]]
- [[sources/holzmuller-2025-deep-observation-filter-virtual-sensing-active-noise-control|Holzmuller & Sontacchi 2025: Deep Observation Filter for Virtual Sensing ANC]]
- [[sources/holzmueller-2026-obs-tasnet-virtual-sensing|Holzmüller & Sontacchi 2026: Obs-TasNet for Virtual Sensing]]
