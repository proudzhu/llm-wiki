---
type: concept
created: 2026-04-28
updated: 2026-04-28
sources:
  - raw/papers/frank-2026-low-latency-roi-beamforming/full-text.txt
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

The **Least-Distortion Maximum-Gain (LDMG)** ROI beamformer solves:

```
max  hH h / (hH Rv h)   subject to h = d
```

where:
- h is the beamformer weight vector
- Rv is the noise covariance matrix
- d is the ROI-averaged steering vector/matrix

### Solution via Generalized Eigenvalue Decomposition

```
h_K,ε = Σ_{p=1}^{K} (tp tpH / (λp + ε)) d
```

with final normalization so the average desired signal reduction factor equals 1.

**Parameters**:
- **K**: Number of eigenvectors (decreasing K improves array gain but degrades distortion)
- **ε**: Regularization constant (increasing ε improves robustness but degrades distortion)

## Time-Domain vs STFT-Domain Implementation

| Aspect | Time-Domain | STFT-Domain |
|--------|-------------|-------------|
| **Latency** | Ly/2 samples | Ly samples |
| **Complexity** | M Ly² real multiplications | O(M Ly log₂ Ly) |
| **Steering** | Real matrix D (M Ly × L) | Complex vector d(k) (M × 1) |
| **Approximation** | Noncausal FIR of length Ld | Multiplicative Transfer Function (MTF) |

### Key Trade-offs

- **Time-domain**: 2x lower latency, higher performance, but higher computation
- **STFT-domain**: Lower computation, but higher latency and slightly degraded performance due to windowing and MTF approximation

## Applications

- **Smart glasses audio front-ends**: Aligning audio capture with wearer's field of view
- **Wearable audio**: Robust to head motion and DOA uncertainty
- **Hearing aids**: Preserving speech from front-facing speakers

## Related Concepts

- [[beamforming|Beamforming]]
- [[signal-processing|Signal Processing]]
- [[active-noise-control|Active Noise Control]]

## Related Sources

- [[sources/frank-2026-low-latency-roi-beamforming|Frank & Cohen 2026: Low-latency Audio Front-end ROI Beamforming for Smart Glasses]]
