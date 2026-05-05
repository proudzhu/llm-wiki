---
type: source
created: 2026-04-28
updated: 2026-04-28
sources:
  - raw/papers/frank-2026-low-latency-roi-beamforming/full-text.txt
  - https://ieeexplore.ieee.org/abstract/document/11462987
  - zotero://select/items/0_DE8N9LJ7
tags:
  - beamforming
  - wearable-audio
  - smart-glasses
  - low-latency
  - roi-beamforming
  - time-domain
  - stft
---

# Frank & Cohen 2026: Low-latency Audio Front-end ROI Beamforming for Smart Glasses

**Authors**: [[../entities/ariel-frank|Ariel Frank]], [[../entities/israel-cohen|Israel Cohen]]
**Institution**: Technion — Israel Institute of Technology
**Year**: 2026
**Type**: Conference Paper
**Venue**: ICASSP 2026 — IEEE International Conference on Acoustics, Speech and Signal Processing
**DOI**: [10.1109/ICASSP55912.2026.11462987](https://doi.org/10.1109/ICASSP55912.2026.11462987)
**Zotero**: [DE8N9LJ7](zotero://select/items/0_DE8N9LJ7)

## Summary

This paper presents a head-to-head comparison of time-domain and STFT-domain implementations of least-distortion maximum-gain (LDMG) region-of-interest (ROI) beamformers for smart glasses. Using real multichannel recordings from a 6-microphone smart-glasses platform, the authors show that the time-domain implementation delivers higher performance with 2x lower algorithmic latency, at the cost of increased computation.

## Problem Formulation

Smart glasses with integrated microphone arrays need low-latency, low-power spatial filtering on resource-constrained hardware. ROI beamforming preserves signals from a spatial region while suppressing sounds from elsewhere, accommodating DOA uncertainty due to head motion, moving sources, background noise, and reverberation.

The signal model for M microphones:

```
ym(t) = gm(t) * x(t) + vm(t)
      = dm(t) * x1(t) + vm(t)
      = xm(t) + vm(t)
```

where x(t) is the desired source, gm(t) is the acoustic response to microphone m, and vm(t) is noise.

## Methodology

### Unified ROI Formulation

Both time-domain and STFT-domain implementations are unified under a common optimization framework:

**Objective**: Maximize average array gain subject to minimum-distortion constraint:

```
max  hH h / (hH Rv h)   subject to h = d
```

where d is the ROI-averaged steering vector/matrix, and Rv is the noise covariance matrix.

**Solution** via generalized eigenvalue decomposition:

```
h_K,ε = Σ_{p=1}^{K} (tp tpH / (λp + ε)) d
```

with final normalization so the average desired signal reduction factor equals 1.

### Time-Domain vs STFT-Domain

| Aspect | Time-Domain | STFT-Domain |
|--------|-------------|-------------|
| **Latency** | Ly/2 samples | Ly samples |
| **Complexity** | M Ly² real multiplications | O(M Ly log₂ Ly) |
| **Steering** | Real matrix D (M Ly × L) | Complex vector d(k) (M × 1) |
| **Approximation** | Noncausal FIR of length Ld | Multiplicative Transfer Function (MTF) |

### Experimental Setup

- **Hardware**: Smart glasses with M = 6 microphones on a manikin
- **Environment**: Anechoic chamber, rotating podium (360° in 10.4 min)
- **Source**: Stationary broadband white noise loudspeaker
- **Sampling**: 16 kHz
- **ROI**: Azimuth [-5°, 5°] at elevation 0°
- **Frame lengths**: Ly ∈ {16, 32, 64, 128} → latencies {0.5, 1, 2, 4} ms (time) and {1, 2, 4, 8} ms (STFT)

### Three Beamformer Types

| Beamformer | Noise Covariance Rv | Optimization Goal |
|------------|---------------------|-------------------|
| Maximum DF | Averaged over 360° azimuth | Maximize directivity factor |
| Maximum WNG | Identity matrix | Maximize white noise gain |
| Maximum OV | Estimated from own-voice recordings | Maximize own-voice suppression |

## Results

All beamformers were tuned to SI-SDR = 14.9 dB for fair comparison.

### Key Findings

1. **Directivity Factor**: Time-domain implementation consistently outperforms STFT-domain across all frame lengths. DF increases monotonically with frame length for both.

2. **White Noise Gain**: Same trend — time-domain superior to STFT-domain.

3. **Own-Voice Reduction**: Time-domain provides better own-voice suppression (critical for smart glasses where wearer's voice is a major interference).

4. **Latency Advantage**: Time-domain achieves 2x lower algorithmic latency (Ly/2 vs Ly samples).

5. **Complexity Trade-off**: Time-domain requires M Ly² real multiplications vs O(M Ly log₂ Ly) for STFT-domain — higher computation but acceptable when modest additional on-device computing power is available.

### Performance vs Frame Length

| Frame Length (Ly) | Time Latency | STFT Latency | DF Advantage |
|-------------------|--------------|--------------|--------------|
| 16 | 0.5 ms | 1 ms | Time > STFT |
| 32 | 1 ms | 2 ms | Time > STFT |
| 64 | 2 ms | 4 ms | Time > STFT |
| 128 | 4 ms | 8 ms | Time > STFT |

## Key Contributions

1. **Unified formulation** spanning time- and STFT-domain LDMG ROI beamformers, making each domain's modeling approximations explicit.
2. **Real-world evaluation** on multichannel smart-glasses recordings (not simulations).
3. **Latency-complexity-performance trade-off analysis** providing practical guidance for wearable deployment.
4. **Conclusion**: When low latency is critical and modest additional on-device computing power is available, time-domain ROI beamforming is the preferred choice for smart-glasses front ends.

## Related Concepts

- [[../concepts/beamforming|Beamforming]]
- [[../concepts/signal-processing|Signal Processing]]
- [[../concepts/active-noise-control|Active Noise Control]]

## Related Entities

- [[../entities/ariel-frank|Ariel Frank]]
- [[../entities/israel-cohen|Israel Cohen]]
