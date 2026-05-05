---
type: source
created: 2026-04-18
updated: 2026-04-28
sources:
  - raw/papers/wang-2024-computation-efficient-virtual-sensing/full-text.txt
  - https://arxiv.org/abs/2405.14158
  - zotero://select/items/0_YHFLXFQH
tags:
  - active-noise-control
  - virtual-sensing
  - multichannel-anc
  - adjoint-lms
  - computational-efficiency
  - inter-noise
---

# Wang, Ji, Shen, Shi & Gan 2024: Computation-Efficient Virtual Sensing with MCALMS

**Authors**: [[../entities/boxiang-wang|Boxiang Wang]], [[../entities/junwei-ji|Junwei Ji]], [[../entities/xiaoyi-shen|Xiaoyi Shen]], [[../entities/dongyuan-shi|Dongyuan Shi]], [[../entities/woon-seng-gan|Woon-Seng Gan]]
**Institution**: Digital Signal Processing Lab, Nanyang Technological University, Singapore
**Published**: INTER-NOISE 2024, Vol. 270, No. 10, pp. 1638–1650
**Type**: Conference Paper
**DOI**: [10.3397/IN_2024_3031](https://doi.org/10.3397/IN_2024_3031)
**arXiv**: [2405.14158](https://arxiv.org/abs/2405.14158)
**Zotero**: [YHFLXFQH](zotero://select/items/0_YHFLXFQH)

---

## Summary

This paper proposes a feedforward multichannel virtual sensing ANC (MVANC) system that incorporates the **multichannel adjoint least mean square (MCALMS)** algorithm instead of the conventional multichannel filtered-x LMS (MCFxLMS) algorithm. The MCALMS algorithm filters the error signal instead of the reference signal, achieving up to **10× computational savings** at 10 channels while maintaining equivalent noise reduction performance (~35 dB attenuation at virtual locations).

---

## Problem Formulation

### Virtual Sensing Challenge

In multichannel ANC, error microphones must be placed in the desired zone of quietness (ZoQ), but physical constraints often prevent this (e.g., near the user's eardrum in ANC headrests). [[../concepts/virtual-sensing|Virtual sensing]] techniques create quiet zones at desired 'virtual' locations far from physical error sensors.

### Computational Bottleneck

The conventional MVANC system based on MCFxLMS suffers from high computational complexity as the number of channels increases. The virtual sensing technique adds extra computational demands during both the auxiliary filter training and execution phases.

---

## Methodology

### Two-Stage Virtual Sensing

**Stage 1 — Tuning Stage**:
1. Obtain optimal control filters for virtual error microphones using MCALMS
2. Control signal: $y_k(n) = \sum_{j=1}^{J} \mathbf{w}_{kj}^T(n) \mathbf{x}_j(n)$
3. Virtual error: $e_{v,q}(n) = d_{v,q}(n) - \sum_{k=1}^{K} y_k(n) * s_{v,qk}$
4. MCALMS update (filters error signal, not reference):
   $$\mathbf{w}_{kj}(n+1) = \mathbf{w}_{kj}(n) - \mu_1 \mathbf{x}_j(n-L+1) \sum_{q=1}^{Q} e'_{v,kq}(n)$$
   where $e'_{v,kq}(n)$ is the time-reversed filtered error signal
5. Train auxiliary filters using LMS to map physical microphone signals to virtual locations

**Stage 2 — Control Stage**:
- Virtual microphones removed; physical microphones remain
- Pre-trained auxiliary filters integrated into MCALMS
- Control filter update:
  $$\mathbf{w}_{kj}(n+1) = \mathbf{w}_{kj}(n) - \mu_3 \mathbf{x}_j(n-L+1) \sum_{m=1}^{M} e'_{h,km}(n)$$

### Key Difference: MCFxLMS vs MCALMS

| Aspect | MCFxLMS | MCALMS |
|:-------|:--------|:-------|
| **Filtered signal** | Reference signal $x(n)$ through $\hat{S}(z)$ | Error signal $e(n)$ through $\hat{S}(z)$ |
| **Multiplications** | $JKM(L+N_x+1) + MJN_h$ | $K(LM+JN_x+1) + MJN_h$ |
| **Additions** | $JKM(L+N_x-1) + M(J+N_h-1)$ | $K[(L-1)M+J(N_x+M-1)] + M(J+N_h-1)$ |
| **Scaling with channels** | $O(JKM)$ — cubic | $O(K)$ — linear in K |

At 10 channels: MCALMS requires ~1/10 the computation of MCFxLMS.

---

## Experimental Setup

| Parameter | Value |
|:----------|:------|
| System | 4 × 2 × 4 feedforward MVANC (J=4, K=2, M=4, Q=4) |
| Sampling rate | 16 kHz |
| Control filter length | 512 taps |
| Auxiliary filter length | 256 taps |
| Primary path length | 128 taps |
| Secondary path length | 32 taps |
| Frequency range | 500–5000 Hz (bandpass) |
| SNR | 40 dB (white noise added) |

---

## Results

### MCALMS vs MCFxLMS Performance

- Both algorithms achieve **~35 dB noise attenuation** at steady state
- Control filters produced by both algorithms are nearly identical (frequency spectrum match)
- MCALMS achieves equivalent performance with significantly lower computation

### Tuning Noise Impact on Control Stage Performance

| Scenario | Tuning Noise | Control Noise | NR (dB) |
|:---------|:-------------|:--------------|:--------|
| 1 | Gaussian (800–1800 Hz) | Uniform (800–1800 Hz) | ~38 |
| 2 | Broadband (800–1800 Hz) | Narrowband (800–1000 Hz) | ~40 |
| 3 | Narrowband (800–1000 Hz) | Broadband (800–1800 Hz) | ~22 |

**Key findings**:
1. **Broadband tuning noise is advantageous**: When tuning noise frequency range encompasses control noise range, NR is maximized (~40 dB)
2. **Narrowband tuning limits performance**: When tuning noise is narrower than control noise, the control filter passband is attenuated in the uncovered range → NR drops to ~22 dB
3. **Matching distributions improve convergence**: When noise distributions in tuning and control stages match, convergence speed improves

---

## Key Contributions

1. **First application of MCALMS to MVANC**: Demonstrates that filtering the error signal (adjoint approach) is more computationally efficient than filtering the reference signal for multichannel virtual sensing
2. **10× computational savings at 10 channels**: MCALMS scales linearly with channel count, while MCFxLMS scales cubically
3. **Equivalent NR performance**: MCALMS produces nearly identical control filters to MCFxLMS, achieving ~35 dB attenuation at virtual locations
4. **Tuning noise guidelines**: Broadband tuning noise should encompass the control stage frequency range for optimal performance

---

## Related Concepts

- [[../concepts/virtual-sensing|Virtual Sensing]]
- [[../concepts/multi-channel-anc|Multi-Channel ANC]]
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[../concepts/adjoint-lms-algorithm|Adjoint LMS Algorithm]]

## Related Synthesis

- [[../synthesis/virtual-sensing-evolution|Evolution of Virtual Sensing in ANC]]
- [[../synthesis/computational-efficiency-evolution|Computational Efficiency Evolution]]
- [[../synthesis/multichannel-anc-efficiency-and-robustness|Multichannel ANC Efficiency and Robustness]]
