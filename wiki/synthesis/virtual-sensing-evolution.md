---
type: synthesis
created: 2026-04-18
updated: 2026-06-25
tags:
- active-noise-control
- deep-learning
- kalman-filter
- signal-processing
- virtual-sensing
- adjoint-lms
sources:
  - raw/papers/zhang-2024-active-noise-control-soundfield-interpolation-pinn/full-text.md
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

The RMT uses an **observation filter** $\mathbf{O}(z)$ to map primary disturbances from physical remote microphones to the virtual error position. Conventionally, these filters are pre-computed via cross-correlations or cross-spectral densities during a training phase and stored in a database indexed by acoustic scenario. During operation, a selection mechanism picks the appropriate filter set. This approach requires [^5]:
- A large pre-computed database encompassing all anticipated scenarios
- A filter-selection or interpolation mechanism for time-varying conditions
- Fixed virtual microphone positions per filter
The most common approach. It uses a preliminary "training phase" where a physical microphone is temporarily placed at the virtual location to identify the transfer function between the permanent physical error mic and the target.
- **Limitation**: Highly sensitive to changes in the acoustic path (e.g., the user moving their head).

### 2.2 Virtual Microphone Arrangement (VMA)
Uses an array of physical microphones to interpolate the sound pressure at the virtual point.
- **Advantage**: Does not strictly require a training phase.
- **Limitation**: Performance degrades as frequency increases due to spatial aliasing.

### 2.3 Auxiliary Filter Method
Introduced to improve robustness by using an auxiliary filter to model the primary noise path difference. This is often combined with hybrid FF/FB structures[^2].

---

### 2.4 PINN-Based Soundfield Interpolation for Virtual Sensing

Zhang et al. (2024)[^zhang2024] proposed a [[concepts/physics-informed-neural-network|physics-informed neural network (PINN)]] approach for soundfield interpolation in [[concepts/active-noise-control|active noise control]]. Unlike classical VMA and RMT methods that rely on fixed filters or array geometry, the PINN is trained to solve the acoustic wave equation:

- A fully connected network (1 hidden layer, 16 neurons) takes space-time coordinates $(x, y, z, n)$ as input and outputs pressure $\hat{p}(x, y, z, n)$
- **Dual loss**: MSE at monitoring microphone positions + PDE residual enforcing $
abla^2 p - \frac{1}{c^2} \partial^2 p / \partial t^2 = 0$ at random collocation points
- **Key advantage**: Monitoring microphones can be placed *outside* the ROI (e.g., on a sphere around the user's ears), giving the user more freedom of movement
- **Performance**: ~8 dB lower interpolation error than SH methods with Q=8 microphones; the PINN-assisted ANC system achieves −13 dB more noise reduction than multiple-point ANC
- **Limitation**: Expensive training phase ($5 \times 10^5$ epochs) with sensitivity to learning rate and loss weighting

This approach bridges classical soundfield interpolation (SH-based) with modern deep learning (PINNs), offering a path to embedding physical knowledge directly into the VS pipeline without pre-computed filter databases.

---

### 2.5 Unified Framework: RP-VS

Shi et al. (2020)[^shi2020] provided a unified theoretical framework showing that AF-VS and RM-VS are not fundamentally distinct but are special cases of a more general **Relative Path VS (RP-VS)** method:

| Condition | RP-VS degenerates to | Rationale |
|-----------|---------------------|-----------|
| Invariant secondary paths | RM-VS | $W_{RP} \to W_{RM}$ when $S_{m'} = S_m$ |
| Invariant primary paths | AF-VS | $W_{RP} \to W_{AF}$ when $P_{m'} = P_m$ |

Key analytical result — residual noise under varying acoustic paths:

| Method | Invariant Secondary Paths | Invariant Primary Paths | All Paths Varying |
|--------|--------------------------|------------------------|-------------------|
| FC Filter | $P_{v'} - P_v$ | $\left(1 - \frac{S_{v'}}{S_v}\right)P_v$ | $P_{v'} - \frac{S_{v'}}{S_v}P_v$ |
| AF-VS | $P_{v'} - P_{v} + \frac{S_{v'}}{S_{m'}}(P_m - P_{m'})$ | $\left(1 - \frac{S_{v'} S_m}{S_v S_{m'}}\right)P_v$ | $P_{v'} - \frac{S_{v'} S_m}{S_v S_{m'}}P_v + \frac{S_{v'}}{S_{m'}}(P_m - P_{m'})$ |
| RM-VS | $P_{v'} - \frac{P_{m'}}{P_m}P_v$ | $\left(1 - \frac{S_{v'}}{S_v}\right)P_v$ | $P_{v'} - \frac{S_{v'} P_{m'}}{S_v P_m}P_v$ |
| RP-VS | $P_{v'} - \frac{P_{m'}}{P_m}P_v$ | $\left(1 - \frac{S_{v'} S_m}{S_v S_{m'}}\right)P_v$ | $P_{v'} - \frac{S_{v'} S_m P_{m'}}{S_v S_m' P_m}P_v$ |

The RP-VS method achieves optimal noise reduction when relative changes in primary and secondary paths are balanced ($P_{v'}/P_v = P_{m'}/P_m$ and $S_{v'}/S_v = S_{m'}/S_m$). An ANC casing prototype with (1,4,4) configuration validated that RP-VS is as effective as AF-VS and RM-VS for broadband fan noise, while showing superior robustness under varying noise frequency bands.

[^shi2020]: [[sources/shi-2020-active-noise-control-casing-virtual-sensing|Shi, Jia, Xie & Li 2020: ANC Casing with RP-VS]]

## 3. Statistical and Optimal Estimation

Moving beyond fixed transfer functions, researchers have applied optimal control and estimation theory to virtual sensing:

- **Kalman Filter Approach[^3]**: Formulates virtual sensing as a state-space estimation problem. By modeling the noise as a stochastic process, the Kalman Filter provides an optimal estimate of the virtual error signal in the presence of measurement noise.
- **Adjoint LMS[^4]**: Focuses on computational efficiency. The multichannel adjoint least mean square (MCALMS) algorithm filters the error signal instead of the reference signal, achieving up to 10× computational savings at 10 channels compared to MCFxLMS, while maintaining equivalent noise reduction (~35 dB) at virtual locations. Key insight: broadband tuning noise should encompass the control stage frequency range for optimal performance.

---

## 4. The AI Frontier: Neural Virtual Sensing

The state-of-the-art is shifting toward data-driven, time-variant observation filters:

- **CNN Neural Observation Filter[^7]**: First demonstration of online observation filter estimation using an encoder-decoder CNN (367k params). Takes GCC-PHAT features between remote microphones plus virtual microphone coordinates as input. Enables asynchronous computation (2 Hz inference on co-processor, real-time filtering on DSP). Achieves −33.53 dB NMSE with accurate position data; position information alone accounts for ~20 dB improvement.
- **Obs-TasNet[^5]**: Follow-up work replacing the CNN encoder-decoder with a modified Conv-TasNet, reducing parameters by ~40% while improving accuracy. Demonstrates adaptation to time-variant environments with moving listeners.
- **Metric Learning[^6]**: Recent preprints suggest using metric learning to make virtual sensing transferable across different environments, reducing the need for site-specific training.

---

## 5. Comparative Analysis of Techniques

| Feature | RMT | VMA | Kalman Filter | Neural (CNN) | Neural (Obs-TasNet) |
|---------|-----|-----|---------------|------------------|-------------------|
| **Requires Training** | Yes | No | Partial | Yes (Pre-training) | Yes (Pre-training) |
| **Robustness** | Low | Moderate | High | High | Very High |
| **Complexity** | $O(L)$ | $O(M \cdot L)$ | $O(N^3)$ | $O(367\text{k})$ | $O(220\text{k})$ |
| **Environment** | Static | Diffuse | Stochastic | Dynamic | Dynamic |
| **Position Info** | Fixed per filter | Fixed | Fixed | Variable (input) | Variable (input) |
| **Async. Update** | No | No | No | Yes (500ms) | Yes (500ms) |

Note: Secondary path interpolation (DTW-based) addresses the moving-listener problem from a different angle — updating the secondary path model rather than the virtual sensing filter — and can be combined with any of the above techniques.

---

## References

[^1]: [[sources/a-review-of-virtual-sensing-algorithms-for-active-|A Review of Virtual Sensing Algorithms for Active Noise Control]] (Zotero: [items/0_LJDPCZ9G](zotero://select/items/0_LJDPCZ9G))
[^2]: [[sources/toyooka-2026-hybrid-anc-remote-sensing|Toyooka 2026: Hybrid ANC with Dual Compensation]] (Zotero: [items/0_AMKNDVMJ](zotero://select/items/0_AMKNDVMJ))
[^3]: [[sources/petersen-2008-kalman-filter-virtual-sensing-anc|A Kalman filter approach to virtual sensing for active noise control]] (Zotero: [items/0_WX2XSXDA](zotero://select/items/0_WX2XSXDA))
[^4]: [[sources/wang-2024-computation-efficient-virtual-sensing|Wang 2024: Computation-Efficient Virtual Sensing with MCALMS]] (Zotero: [items/0_YHFLXFQH](zotero://select/items/0_YHFLXFQH))
[^5]: [[sources/holzmueller-2026-obs-tasnet-virtual-sensing|Holzmüller 2026: Obs-TasNet for Virtual Sensing]] (Zotero: [items/0_WY4S7C6Z](zotero://select/items/0_WY4S7C6Z))
[^6]: [[sources/wang-2024-metric-learning-virtual-sensing|Wang 2024: Transferable Selective Virtual Sensing]] (Zotero: [items/0_NBYTXNH4](zotero://select/items/0_NBYTXNH4))
[^7]: [[sources/holzmuller-2025-deep-observation-filter-virtual-sensing-active-noise-control|Holzmuller & Sontacchi 2025: Deep Observation Filter for Virtual Sensing ANC]] (Zotero: [items/0_5KW3SUYE](zotero://select/items/0_5KW3SUYE))
[^zhang2024]: [[sources/zhang-2024-active-noise-control-soundfield-interpolation-pinn|Zhang et al. 2024: ANC with PINN-based Soundfield Interpolation]] (Zotero: [items/0_PYI2K3NS](zotero://select/items/0_PYI2K3NS))

---

## Related Concepts

- [[concepts/virtual-sensing|Virtual Sensing Concept]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/kalman-filter|Kalman Filter]]
- [[concepts/state-space-model|State-Space Model]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]

## Related Synthesis

- [[computational-efficiency-evolution|Computational Efficiency Evolution]]
- [[anc-architecture-evolution|ANC Architecture Evolution]]

## Related Sources

- [[sources/a-review-of-virtual-sensing-algorithms-for-active-|A Review of Virtual Sensing Algorithms for Active Noise Control]]
- [[sources/wang-2024-computation-efficient-virtual-sensing|Wang 2024: Computation-Efficient Virtual Sensing with MCALMS]]
- [[sources/holzmuller-2025-deep-observation-filter-virtual-sensing-active-noise-control|Holzmuller & Sontacchi 2025: Deep Observation Filter for Virtual Sensing ANC]]
- [[sources/holzmueller-2026-obs-tasnet-virtual-sensing|Holzmüller 2026: Obs-TasNet for Virtual Sensing]]
- [[sources/petersen-2008-kalman-filter-virtual-sensing-anc|A Kalman filter approach to virtual sensing for active noise control]]
- [[sources/toyooka-2026-hybrid-anc-remote-sensing|Toyooka 2026: Hybrid ANC with Dual Compensation]]
- [[sources/wang-2024-metric-learning-virtual-sensing|Wang 2024: Transferable Selective Virtual Sensing]]
- [[sources/holzmuller-2026-dtw-secondary-path-anc|Holzmüller & Sontacchi 2026: DTW for Secondary Path Interpolation in ANC]]
- [[sources/zhang-2024-active-noise-control-soundfield-interpolation-pinn|Zhang et al. 2024: ANC with PINN-based Soundfield Interpolation]]
