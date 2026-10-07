---
type: concept
created: 2026-04-28
updated: 2026-10-07
sources:
  - raw/papers/frank-2026-low-latency-roi-beamforming/full-text.md
  - raw/papers/itzhak-2025-stft-roi-beamforming/full-text.md
tags:
  - beamforming
  - spatial-filtering
  - wearable-audio
  - roi
---

# Region-of-Interest Beamforming

## Overview

**Region-of-Interest (ROI) beamforming** is a spatial filtering technique that preserves signals from a spatial region (rather than a single direction) while suppressing sounds from elsewhere. This accommodates direction-of-arrival (DOA) uncertainty due to head motion, moving or switching sources, background noise, and reverberation.

## Why ROI Instead of Single-DOA?

Traditional beamformers focus on a specific DOA, which is problematic when:
- The wearer's head moves
- The source moves or switches
- Background noise and reverberation create DOA uncertainty

ROI beamforming defines a spatial region Ω (set of polar and azimuthal angles) and minimizes **average distortion** across the entire region.

## LDMG ROI Beamformer

The **Least-Distortion Maximum-Gain (LDMG)** ROI beamformer (Frank & Cohen 2026) maximizes the average array gain over the ROI subject to a minimum-distortion constraint:

```
max_h  h^H Γ_Ω h / (h^H Γ_v h)   subject to  Γ_Ω h = d_Ω
```

where:
- **h** is the beamformer weight vector (real, length $M L_y$ for time-domain; complex, length $M$ per frequency bin for STFT-domain)
- **Γ_Ω** and **d_Ω** are the ROI-averaged steering outer product and steering vector/matrix
- **Γ_v** is the (normalized) noise covariance matrix

### Solution via Generalized Eigenvalue Decomposition

```
h_K,μ = [ Σ_{p=1}^{K} (t_p t_p^H / (λ_p + μ)) ] d_Ω
```

with a final normalization so the average desired-signal reduction factor equals 1.

**Parameters**:
- **K**: Number of eigenvectors of $\Gamma_v^{-1} \Gamma_\Omega$ retained (decreasing K improves array gain but degrades distortion)
- **μ**: Regularization constant (increasing μ improves robustness but degrades distortion)

## STFT-Domain Origin: LD-MWNG and LD-MDF

The STFT-domain instance of this formulation was introduced by [[sources/itzhak-2025-stft-roi-beamforming|Itzhak & Cohen 2025]] as two beamformers, each maximizing a different array-gain measure under the ROI-distortion constraint $\boldsymbol{\Gamma}_{\mathbf{d},\Omega}(k)\, \mathbf{h}(k) = \mathbf{d}_\Omega(k)$:

- **LD-MWNG** (least-distortion maximum WNG): EVD of $\boldsymbol{\Gamma}_{\mathbf{d},\Omega}$; maximizes the ROI-averaged [[concepts/white-noise-gain|WNG]]; reduces to the delay-and-sum beamformer for a single-DOA ROI
- **LD-MDF** (least-distortion maximum DF): GEVD of $(\boldsymbol{\Gamma}_{\mathbf{d},\Omega}, \boldsymbol{\Gamma}_0)$ with the diffuse-noise pseudo-correlation; maximizes the ROI-averaged [[concepts/directivity-factor|DF]]; reduces to the classical maximum-DF (superdirective) beamformer for a single-DOA ROI

Both use the eigenvector-truncation parameter $K$ alone (no $\mu$): $K = 1$ recovers the unconstrained maximum-gain solution with minimal ROI-average distortion, $K = P$ (rank of $\boldsymbol{\Gamma}_{\mathbf{d},\Omega}$) gives the least-distortion solution. The larger the ROI, the higher the rank and the larger the usable $K$ (eigenvalue analysis suggests $K \leq 3$ for a $\pm 30°$ azimuth ROI, $K \leq 7$ for the largest ROI tested); empirically the best $K$ grows with the actual DOA deviation. Frank & Cohen 2026 unified both implementations under the LDMG framework with $K$ and a regularization $\mu$.

## Time-Domain vs STFT-Domain Implementation

| Aspect | Time-Domain | STFT-Domain |
|--------|-------------|-------------|
| **Latency** | $\lfloor L_y/2 \rfloor$ samples (center-sample target) | $L_y$ samples (full frame accumulation) |
| **Complexity** | $M L_y^2$ real multiplications | $\mathcal{O}(M L_y \log_2 L_y)$ |
| **Steering** | Real matrix D ($M L_y \times L$) | Complex vector d(k) ($M \times 1$) |
| **Approximation** | Noncausal FIR of length $L_d$ | Multiplicative Transfer Function (MTF) |

### Key Trade-offs

- **Time-domain**: 2× lower latency, higher performance, but higher computation
- **STFT-domain**: Lower computation, but higher latency and slightly degraded performance due to windowing and the MTF approximation
- **Why time-domain wins**: it filters the waveform directly (spatiotemporal filtering), whereas the STFT implementation relies on the MTF approximation, which is inaccurate when the frame length is shorter than the effective support of the relative impulse responses

## Applications

- **Smart glasses audio front-ends**: Aligning audio capture with wearer's field of view
- **Wearable audio**: Robust to head motion and DOA uncertainty
- **Hearing aids**: Preserving speech from front-facing speakers

## Related Concepts

- [[concepts/beamforming|Beamforming]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/directivity-factor|Directivity Factor]]
- [[concepts/signal-processing|Signal Processing]]
- [[concepts/active-noise-control|Active Noise Control]]

## Related Sources

- [[sources/frank-2026-low-latency-roi-beamforming|Frank & Cohen 2026: Low-latency Audio Front-end ROI Beamforming for Smart Glasses]]
- [[sources/itzhak-2025-stft-roi-beamforming|Itzhak & Cohen 2025: STFT-Domain Least-Distortion Region-of-Interest Beamforming]] — the original STFT-domain least-distortion ROI formulation (LD-MWNG / LD-MDF) that the LDMG framework unifies
