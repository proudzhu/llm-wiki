---
type: source
created: 2026-05-27
updated: 2026-05-27
sources:
  - raw/papers/shi-2020-active-noise-control-casing-virtual-sensing/full-text.md
  - https://doi.org/10.1016/j.ymssp.2020.106878
  - zotero://select/items/0_DAGTQQLP
tags:
  - active-noise-control
  - virtual-sensing
  - multi-channel-feedforward
  - anc-casing
  - relative-path
---

# Chuang Shi, Zhuoying Jia, Rong Xie & Huiyong Li 2020: An Active Noise Control Casing Using the Multi-Channel Feedforward Control System and the Relative Path Based Virtual Sensing Method

| Field | Value |
|-------|-------|
| **Authors** | [[entities/chuang-shi\|Chuang Shi]], [[entities/zhuoying-jia\|Zhuoying Jia]], [[entities/rong-xie\|Rong Xie]], [[entities/huiyong-li\|Huiyong Li]] |
| **Institution** | School of Information and Communication Engineering, University of Electronic Science and Technology of China, Chengdu |
| **Venue** | Mechanical Systems and Signal Processing, Vol. 144, pp. 106878 |
| **Year** | 2020 |
| **DOI** | [10.1016/j.ymssp.2020.106878](https://doi.org/10.1016/j.ymssp.2020.106878) |
| **Zotero** | [Link](zotero://select/items/0_DAGTQQLP) |

## Summary

This paper proposes a **Relative Path based Virtual Sensing (RP-VS)** method for multi-channel feedforward active noise control (ANC) systems. RP-VS estimates both the disturbance signal and the anti-noise signal at the target zone of quiet (ZoQ) by training two relative path models — a relative primary path $C_p(z)$ and a relative secondary path $C_s(z)$ — during a tuning stage. Theoretical analysis shows that RP-VS degenerates to the Auxiliary Filter VS (AF-VS) method when secondary paths are invariant and to the Remote Microphone VS (RM-VS) method when primary paths are invariant. Simulations on single-channel (1,1,1) and dual-channel (1,2,2) systems validate the analysis, demonstrating that RP-VS achieves the best average noise reduction under varying acoustic paths and varying noise frequency bands. An ANC casing prototype with a (1,4,4) configuration is built on a real-time DSP platform, confirming RP-VS is as effective as AF-VS and RM-VS for broadband fan noise reduction.

## Problem Formulation

### ANC Casing Configuration

An ANC casing encloses a noise source inside a sound-proof shield with an opening for ventilation. Control sources (loudspeakers) are distributed at the opening to emit anti-noise waves. However, error microphones must be placed close to the control sources to avoid protuberance, while the target ZoQ is desired farther away — creating the need for virtual sensing.

![[raw/papers/shi-2020-active-noise-control-casing-virtual-sensing/figures/947a5a464ab8e96f0949203c6a911cc22516f97d50cd28614cb955c0d993b791.jpg|ANC casing concept: noise source enclosed in a casing with control sources at the opening, error microphones nearby, and the target ZoQ farther away]]

*Figure 1: Illustration of the ANC casing concept. Control sources at the opening emit anti-noise; error (monitoring) microphones are near the sources; the target ZoQ is at a distance.*

### Signal Model

In the tuning stage (temporal microphones placed at target ZoQ), the virtual error signal is:

$$E_v(z) = D_v(z) + S_v(z) Y(z)$$

where $D_v(z) = P_v(z) X(z)$ is the disturbance at the virtual mic, $Y(z) = W_o(z) X(z)$ is the control signal, $P_v(z)$ and $S_v(z)$ are the virtual primary and secondary paths.

The optimal control filter is:

$$W_o(z) = -\frac{P_v(z)}{S_v(z)}$$

## Methodology

### Auxiliary Filter Based VS (AF-VS)

The AF-VS method trains an auxiliary filter $H(z)$ during tuning to capture the relationship between the reference signal and the monitoring microphone error:

$$H(z) = -\left[P_m(z) + S_m(z) W_o(z)\right]$$

In the control stage, the converged filter minimizes $E_{m'}(z) + H(z) X'(z)$:

$$W_{AF}(z) = -\frac{P_{m'}(z) + H(z)}{S_{m'}(z)}$$

**Strengths**: Can leverage online secondary path modeling (monitoring mic available in control stage). **Weakness**: Sensitive to primary path changes.

### Remote Microphone Based VS (RM-VS)

The RM-VS method trains a relative primary path model $C_p(z)$ during tuning:

$$C_p(z) = \frac{P_v(z)}{P_m(z)}$$

In the control stage, it estimates the disturbance at the monitoring mic, then projects it to the virtual location:

$$W_{RM}(z) = -\frac{C_p(z) P_{m'}(z)}{S_v(z)}$$

**Strengths**: Robust to primary path changes. **Weakness**: Requires accurate $S_v(z)$ model that cannot be updated in the control stage (no virtual mic present).

### Relative Path Based VS (RP-VS) — Proposed

The RP-VS method adds a second relative path model — the relative secondary path $C_s(z)$:

$$C_s(z) = \frac{S_v(z)}{S_m(z)}$$

In the control stage, the virtual error is estimated using both relative models:

$$\widehat{E}_{v'}(z) = C_p(z) \widehat{D}_{m'}(z) + C_s(z) S_{m'}(z) Y'(z)$$

The converged control filter is:

$$W_{RP}(z) = -\frac{C_p(z) P_{m'}(z)}{C_s(z) S_{m'}(z)}$$

**Key insight**: RP-VS unifies AF-VS and RM-VS — when secondary paths are invariant ($S_{m'} = S_m$), $W_{RP} \to W_{RM}$; when primary paths are invariant ($P_{m'} = P_m$), $W_{RP} \to W_{AF}$.

![[raw/papers/shi-2020-active-noise-control-casing-virtual-sensing/figures/3a02c4ea1e7e78293aff47025d8306149caa2d76f080c11ca8d9730d329ef7ef.jpg|RP-VS method control stage block diagram]]

*Figure 2: Control stage of the RP-VS method. Both $C_p(z)$ and $C_s(z)$ are used to estimate the virtual error signal from monitoring microphone measurements.*

### Multi-Channel Extension

For a MCFFANC system with $I$ reference microphones, $J$ secondary sources, $K$ monitoring microphones and $L$ virtual microphones:

$$\mathbf{W}_o^{(J \times I)} = -\left[\mathbf{S}_v^{(L \times J)}\right]^\dagger \mathbf{P}_v^{(L \times I)}$$

$$\mathbf{C}_p^{(L \times K)} = \mathbf{P}_v^{(L \times I)} \left[\mathbf{P}_m^{(K \times I)}\right]^\dagger$$

$$\mathbf{C}_s^{(L \times K)} = \mathbf{S}_v^{(L \times J)} \left[\mathbf{S}_m^{(K \times J)}\right]^\dagger$$

$$\mathbf{W}_{RP}(z) = \left[\mathbf{S}_{m'}^{(K \times J)}\right]^\dagger \mathbf{S}_m^{(K \times J)} \mathbf{W}_o^{(J \times I)} \left[\mathbf{P}_m^{(K \times I)}\right]^\dagger \mathbf{P}_{m'}^{(K \times I)}$$

## Experimental Setup

### Simulations

| Parameter | Single-Channel | Dual-Channel |
|-----------|---------------|--------------|
| **Configuration** | (1,1,1) | (1,2,2) |
| **Frequency band** | 400–1600 Hz | 400–1600 Hz |
| **Primary path length** | 75 ms | 75 ms |
| **Secondary path length** | 25 ms | 25 ms |
| **Filter taps** | 400 | 400 |
| **Normalized step size** | 0.01 | 0.01 |
| **Sampling rate** | 16 kHz | 16 kHz |
| **Path changes** | Microphones moved 12 cm | Microphones moved 12 cm |

### ANC Casing Prototype

| Component | Specification |
|-----------|--------------|
| **Configuration** | (1,4,4) feedforward ANC |
| **Controller** | Real-time DSP platform (TMS320C6748) |
| **DA converter** | 4-channel AD5724 |
| **AD converter** | 8-channel AD7606 |
| **Microphones** | CRY333 electret |
| **Noise source** | Computer fan (0–2500 rpm) |
| **Tuning condition** | 30% fan speed (58 dB SPL at ZoQ) |

## Results

### Varying Acoustic Paths — Single-Channel (dB reduction)

| Condition | FC Filter | AF-VS | RM-VS | RP-VS |
|-----------|-----------|-------|-------|-------|
| Tuning | 24.3 | 24.2 | 23.7 | 23.7 |
| Primary Paths Changed | 4.2–15.8 | 6.4–16.5 | 13.3–15.3 | 13.3–15.3 |
| Secondary Paths Changed | 7.4–11.8 | 12.3–13.8 | 7.3–11.8 | 12.2–13.9 |
| All Paths Changed | 7.6–14.7 | 10.3–12.7 | 7.0–9.0 | 10.5–14.5 |

### Varying Noise Frequency Band — Single-Channel (dB)

| Band | FC Filter | AF-VS | RM-VS | RP-VS |
|------|-----------|-------|-------|-------|
| 400–800 Hz (outside tuning) | −5.2 | 3.5 | 8.4 | **10.1** |
| 800–1600 Hz | 3.4 | 5.6 | 4.6 | **11.3** |
| 400–1600 Hz (all bands) | 3.1 | 5.5 | 4.6 | **11.3** |

### ANC Casing Experiment

At 30% fan speed (tuning condition), all three VS methods achieved broadband noise reduction comparable to the FxLMS baseline. At 100% fan speed (untrained), RP-VS was as effective as AF-VS and RM-VS. The monitoring microphone showed increased SPL when ZoQ was formed at the virtual location, confirming the necessity of virtual sensing — the monitoring mics (near the control sources) experience local SPL increase while the target ZoQ farther away benefits from noise reduction.

![[raw/papers/shi-2020-active-noise-control-casing-virtual-sensing/figures/990b1c13305a45f94ab74140c892f526602fd01df4e73d727f6126f98a915863.jpg|3D design model of the ANC casing prototype]]

*Figure 3: 3D design model (left) and prototype photo (right) of the ANC casing with (1,4,4) configuration.*

## Key Contributions

1. **Relative Path based Virtual Sensing (RP-VS)**: A new VS method that estimates both disturbance and anti-noise signals at the target ZoQ using two relative path models ($C_p$ and $C_s$).
2. **Unified theoretical framework**: Provides explicit z-domain analysis showing that RP-VS degenerates to AF-VS under invariant secondary paths and to RM-VS under invariant primary paths — demonstrating these methods are not fundamentally distinct but special cases of a more general approach.
3. **Robustness to varying acoustic paths**: RP-VS achieves optimal noise reduction when relative changes in primary and secondary paths are balanced, outperforming both AF-VS and RM-VS in the all-paths-varying scenario.
4. **Robustness to varying noise characteristics**: RP-VS produces control filters with closest phase response to optimal when noise frequency bands vary, achieving the best average noise reduction across different testing bands.
5. **ANC casing implementation**: First demonstration of a (1,4,4) ANC casing on a real-time DSP platform, validating RP-VS effectiveness for broadband fan noise reduction.

## Related Concepts

- [[concepts/virtual-sensing|Virtual Sensing]]
- [[concepts/remote-microphone-technique|Remote Microphone Technique]]
- [[concepts/relative-path-virtual-sensing|Relative Path Virtual Sensing]]
- [[concepts/multi-channel-anc|Multi-Channel ANC]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/active-noise-control|Active Noise Control]]

## Related Synthesis

- [[synthesis/virtual-sensing-evolution|Evolution of Virtual Sensing in ANC]]

## Related Sources

- [[sources/a-review-of-virtual-sensing-algorithms-for-active-|Moreau 2008: Review of Virtual Sensing Algorithms for ANC]]
- [[sources/petersen-2008-kalman-filter-virtual-sensing-anc|Petersen 2008: Kalman Filter for Virtual Sensing]]
- [[sources/wang-2024-computation-efficient-virtual-sensing|Wang 2024: Computation-Efficient Virtual Sensing]]
- [[sources/toyooka-2026-hybrid-anc-remote-sensing|Toyooka 2026: Hybrid ANC with Dual Compensation]]
