---
type: synthesis
created: 2026-04-18
updated: 2026-04-28
tags:
- active-noise-control
- deep-learning
- kalman-filter
- signal-processing
- virtual-sensing
- adjoint-lms
sources: []
---
# Evolution of Virtual Sensing in Active Noise Control

> **Objective**: Synthesize the development of virtual sensing algorithms, from foundational pressure-based estimation to modern neural observation filters, addressing the challenge of creating "zones of quiet" at remote locations.

---

## 1. The Spatial Bottleneck of ANC

Traditional ANC systems create a "zone of silence" centered at the physical error microphone. For hearables and automotive headrests, the desired quiet zone is the listener's ear canal, where placing a microphone is often uncomfortable or design-prohibitive. Virtual sensing overcomes this by estimating the error signal at a "virtual" location using information from physical sensors located elsewhere.

---

## 2. Foundational Methodologies

According to the comprehensive review[^1], classical virtual sensing falls into three main categories:

### 2.1 Remote Microphone Technique (RMT)
The most common approach. It uses a preliminary "training phase" where a physical microphone is temporarily placed at the virtual location to identify the transfer function between the permanent physical error mic and the target.
- **Limitation**: Highly sensitive to changes in the acoustic path (e.g., the user moving their head).

### 2.2 Virtual Microphone Arrangement (VMA)
Uses an array of physical microphones to interpolate the sound pressure at the virtual point.
- **Advantage**: Does not strictly require a training phase.
- **Limitation**: Performance degrades as frequency increases due to spatial aliasing.

### 2.3 Auxiliary Filter Method
Introduced to improve robustness by using an auxiliary filter to model the primary noise path difference. This is often combined with hybrid FF/FB structures[^2].

---

## 3. Statistical and Optimal Estimation

Moving beyond fixed transfer functions, researchers have applied optimal control and estimation theory to virtual sensing:

- **Kalman Filter Approach[^3]**: Formulates virtual sensing as a state-space estimation problem. By modeling the noise as a stochastic process, the Kalman Filter provides an optimal estimate of the virtual error signal in the presence of measurement noise.
- **Adjoint LMS[^4]**: Focuses on computational efficiency. The multichannel adjoint least mean square (MCALMS) algorithm filters the error signal instead of the reference signal, achieving up to 10× computational savings at 10 channels compared to MCFxLMS, while maintaining equivalent noise reduction (~35 dB) at virtual locations. Key insight: broadband tuning noise should encompass the control stage frequency range for optimal performance.

---

## 4. The AI Frontier: Neural Virtual Sensing

The state-of-the-art is shifting toward data-driven, time-variant observation filters:

- **Obs-TasNet[^5]**: A neural network architecture designed to estimate virtual sensing observation filters online. Unlike RMT, which assumes a static path, Obs-TasNet adapts to time-variant settings (e.g., a moving listener) by estimating filter coefficients in real-time.
- **Metric Learning[^6]**: Recent preprints suggest using metric learning to make virtual sensing transferable across different environments, reducing the need for site-specific training.

---

## 5. Comparative Analysis of Techniques

| Feature | RMT | VMA | Kalman Filter | Neural (Obs-TasNet) |
|---------|-----|-----|---------------|-------------------|
| **Requires Training** | Yes | No | Partial | Yes (Pre-training) |
| **Robustness** | Low | Moderate | High | Very High |
| **Complexity** | $O(L)$ | $O(M \cdot L)$ | $O(N^3)$ | $O(\text{Network})$ |
| **Environment** | Static | Diffuse | Stochastic | Dynamic |

Note: Secondary path interpolation (DTW-based) addresses the moving-listener problem from a different angle — updating the secondary path model rather than the virtual sensing filter — and can be combined with any of the above techniques.

---

## References

[^1]: [[../sources/a-review-of-virtual-sensing-algorithms-for-active-|A Review of Virtual Sensing Algorithms for Active Noise Control]] (Zotero: [items/0_LJDPCZ9G](zotero://select/items/0_LJDPCZ9G))
[^2]: [[../sources/toyooka-2026-hybrid-anc-remote-sensing|Toyooka 2026: Hybrid ANC with Dual Compensation]] (Zotero: [items/0_AMKNDVMJ](zotero://select/items/0_AMKNDVMJ))
[^3]: [[../sources/petersen-2008-kalman-filter-virtual-sensing-anc|A Kalman filter approach to virtual sensing for active noise control]] (Zotero: [items/0_WX2XSXDA](zotero://select/items/0_WX2XSXDA))
[^4]: [[../sources/wang-2024-computation-efficient-virtual-sensing|Wang 2024: Computation-Efficient Virtual Sensing with MCALMS]] (Zotero: [items/0_YHFLXFQH](zotero://select/items/0_YHFLXFQH))
[^5]: [[../sources/holzmueller-2026-obs-tasnet-virtual-sensing|Holzmüller 2026: Obs-TasNet for Virtual Sensing]] (Zotero: [items/0_WY4S7C6Z](zotero://select/items/0_WY4S7C6Z))
[^6]: [[../sources/wang-2024-metric-learning-virtual-sensing|Wang 2024: Transferable Selective Virtual Sensing]] (Zotero: [items/0_NBYTXNH4](zotero://select/items/0_NBYTXNH4))

---

## Related Concepts

- [[../concepts/virtual-sensing|Virtual Sensing Concept]]
- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/kalman-filter|Kalman Filter]]
- [[../concepts/state-space-model|State-Space Model]]
- [[../concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]

## Related Synthesis

- [[computational-efficiency-evolution|Computational Efficiency Evolution]]
- [[anc-architecture-evolution|ANC Architecture Evolution]]

## Related Sources

- [[../sources/a-review-of-virtual-sensing-algorithms-for-active-|A Review of Virtual Sensing Algorithms for Active Noise Control]]
- [[../sources/wang-2024-computation-efficient-virtual-sensing|Wang 2024: Computation-Efficient Virtual Sensing with MCALMS]]
- [[../sources/holzmueller-2026-obs-tasnet-virtual-sensing|Holzmüller 2026: Obs-TasNet for Virtual Sensing]]
- [[../sources/petersen-2008-kalman-filter-virtual-sensing-anc|A Kalman filter approach to virtual sensing for active noise control]]
- [[../sources/toyooka-2026-hybrid-anc-remote-sensing|Toyooka 2026: Hybrid ANC with Dual Compensation]]
- [[../sources/wang-2024-metric-learning-virtual-sensing|Wang 2024: Transferable Selective Virtual Sensing]]
- [[../sources/holzmuller-2026-dtw-secondary-path-anc|Holzmüller & Sontacchi 2026: DTW for Secondary Path Interpolation in ANC]]
