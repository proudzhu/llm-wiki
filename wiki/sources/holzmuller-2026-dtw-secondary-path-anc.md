---
type: source
created: 2026-05-06
updated: 2026-05-06
sources:
  - raw/papers/holzmuller-2026-dtw-secondary-path-anc/full-text.md
  - https://doi.org/10.1109/OJSP.2026.3689448
  - zotero://select/items/0_ZV3BCM38
tags:
  - active-noise-control
  - dynamic-time-warping
  - secondary-path
  - interpolation
  - fxlms
---

# Holzmüller & Sontacchi 2026: DTW for Secondary Path Interpolation in ANC

**Authors**: [[../entities/felix-holzmueller|Felix Holzmüller]], [[../entities/alois-sontacchi|Alois Sontacchi]]
**Institution**: Institute of Electronic Music and Acoustics, University of Music and Performing Arts Graz, Austria
**Venue**: IEEE Open Journal of Signal Processing
**Year**: 2026
**Type**: Journal Article
**DOI**: [10.1109/OJSP.2026.3689448](https://doi.org/10.1109/OJSP.2026.3689448)
**Zotero**: [ZV3BCM38](zotero://select/items/0_ZV3BCM38)

## Summary

Proposes a [[../concepts/dynamic-time-warping|Dynamic Time Warping]]-based interpolation method for secondary path filter coefficients in local [[../concepts/active-noise-control|ANC]] systems with moving listeners. By aligning impulse responses via DTW in an offline analysis before interpolation and de-warping during operation, the technique achieves substantially lower system mismatch and extends the stable frequency range compared to nearest-neighbor and linear interpolation, especially for coarse measurement grids and lateral translation.

## Problem Formulation

In local ANC with moving points of cancellation (PoC), the [[../concepts/secondary-path-modeling|secondary path]] $\hat{\mathbf{g}}(\Psi)$ must be updated as the listener moves to position $\Psi_{\text{int}}[n]$. When paths are pre-recorded at $N_\Psi$ discrete positions $\underline{\Psi} := \{\Psi_f\}_{f=1}^{N_\Psi}$, interpolation is required for intermediate positions. Direct time-domain interpolation of impulse responses produces pre-echo effects and temporal smearing because adjacent responses exhibit different propagation delays and reflection patterns.

The **system mismatch** quantifies interpolation accuracy:

$$\text{SM}(\Psi) = 20\log_{10}\left(\frac{\|\mathbf{g}(\Psi) - \tilde{\mathbf{g}}(\Psi)\|_2}{\|\mathbf{g}(\Psi)\|_2}\right)$$

Stability of the [[../concepts/filtered-x-lms-algorithm|FxLMS]] algorithm requires:

$$\Re\left\{\text{eig}\left[\hat{\mathbf{G}}^H(\omega)\mathbf{G}(\omega)\right]\right\} > 0 \quad \forall\omega$$

## Methodology

### Benchmark Methods

1. **Nearest-Neighbor (NN)**: Select the secondary path from the closest measurement position.
2. **Linear Interpolation (LI)**: Linearly blend coefficients from adjacent positions with factor $\alpha$.
3. **Global Time Alignment (GA)**: Cross-correlation-based offset estimation before linear interpolation.

### DTW-Based Interpolation

The proposed method extends linear interpolation by warping one adjacent response onto the other via DTW before blending:

1. **Offline DTW Analysis**: For each pair of adjacent measurement positions, compute the optimal warping path between their impulse responses using DTW. This aligns corresponding sound events (direct sound, reflections) across positions.

2. **Interpolation**: At runtime, given position $\Psi_{\text{int}}[n]$ between $\Psi_-$ and $\Psi_+$ with factor $\alpha$:

$$\check{\tilde{\mathbf{g}}}_{\text{DTW}}[n] = (1 - \alpha[n])\hat{\mathbf{g}}_- [n] + \alpha[n]\hat{\mathbf{g}}_+[n]$$

The unwarped coefficients always receive higher weight than the warped version to minimize artifact influence.

3. **De-warping**: Warped indices are interpolated back to integer positions via:

$$\check{b}_i := \begin{cases} i + \alpha[n](i - b_i), & \text{if } \alpha[n] < 0.5 \\ i + (1 - \alpha[n])(i - b_i), & \text{else} \end{cases}$$

Since $\check{b}_i \in \mathbb{R}$, cubic spline interpolation extracts the de-warped coefficients at integer positions.

### Complexity

| Method | Overall Complexity |
|--------|-------------------|
| NN | 2 |
| LI | 3I + 7 |
| GA | 3I + 9 |
| DTW | 29I − 3 |

The DTW method's dominant cost is cubic spline interpolation (23I − 7 operations). However, since coefficient updates run asynchronously (only when position changes), this can be offloaded to a co-processor.

### DTW Step Patterns

Different continuity conditions (step patterns) were evaluated:
- **symmetric1**: Classic step pattern emphasizing diagonal steps; best for lateral translation (global time offset dominates)
- **symmetricP1/P2**: Sakoe-Chiba patterns with slope constraint; better for yaw rotation
- **Rabiner-Juang II(b)**: Good compromise for both translation and rotation

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Yaw rotation dataset | Neumann KU100 HRIRs, 1° resolution, 25 cm distance |
| Lateral translation dataset | TASCAR simulation, 0.5 cm spacing, 25–100 cm distance |
| Sample rate | 16 kHz (KU100 downsampled from 48 kHz ×3) |
| FIR filter order (secondary path) | I = 121 |
| Control filter order | J = 255 |
| FxLMS step size | μ = 0.001 |
| ANC simulation room | (2.5, 1.5, 1.0) m, second-order image source model |
| Primary source position | (−0.5, 0, 0) m |
| Secondary source positions | (0.2, ±0.2, 0) m |
| Measurement positions | Ψx = {0.4, 0.55, 0.7, 0.85, 1.0} m |
| Primary disturbance | Lowpass white noise, 1 kHz cutoff |
| DTW implementation | dtw-python package |

## Results

### System Mismatch (Lateral Translation, 15 cm spacing)

| Method | SM (dB) |
|--------|---------|
| NN | 2.49 |
| LI | 1.78 |
| GA | −9.85 |
| **DTW (symmetric1)** | **−17.65** |

### Stable Frequency Range (Lateral Translation)

| Spacing | NN (Hz) | LI (Hz) | GA (Hz) | DTW (Hz) |
|---------|---------|---------|---------|----------|
| 5 cm | 3375 | 3406 | 7906 | 7594 |
| 15 cm | 1156 | 1125 | 7688 | **7750** |
| 25 cm | 688 | 688 | 7656 | **7531** |

DTW and GA both maintain stable operation up to ~7.5 kHz even for 25 cm spacing, while NN and LI collapse below 1.2 kHz.

### Yaw Rotation (30° spacing)

| Method | SM (dB) | f_stab (Hz) |
|--------|---------|-------------|
| NN | −6.56 | 1281 |
| LI | −8.37 | 1562 |
| GA | −10.10 | 1500 |
| **DTW** | **−13.69** | **1750** |

### Key Findings

1. DTW achieves the lowest system mismatch in almost all configurations, especially for coarse measurement grids
2. For lateral translation, DTW extends the stable frequency range from ~1.1 kHz (NN/LI) to ~7.7 kHz even at 25 cm spacing
3. For yaw rotation, contralateral sources (45°–135°) produce higher error due to multiple propagation paths around the head with similar delays, causing DTW alignment difficulties near 90°
4. In dynamic ANC simulation, DTW provides the highest noise reduction and remains stable throughout, while GA diverges at positions with wall reflections
5. The Rabiner-Juang II(b) step pattern offers a good compromise for both translation and rotation

## Key Contributions

1. First application of DTW to secondary path interpolation in local ANC, adapting techniques from HRIR interpolation in spatial audio
2. Asymmetric warping strategy: only one response is warped, and the unwarped response always receives higher weight to minimize artifacts
3. De-warping via cubic spline interpolation of non-integer indices, enabling smooth position-dependent coefficient extraction
4. Comprehensive evaluation of DTW step patterns for both lateral translation and yaw rotation scenarios
5. Demonstration that DTW-based interpolation can reduce required measurement positions substantially while extending the controlled frequency bandwidth

## Related Concepts

- [[../concepts/dynamic-time-warping|Dynamic Time Warping]]
- [[../concepts/secondary-path-interpolation|Secondary Path Interpolation]]
- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[../concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[../concepts/offline-secondary-path-modeling|Offline Secondary-Path Modeling]]

## Related Synthesis

- [[../synthesis/virtual-sensing-evolution|Virtual Sensing Evolution]]
