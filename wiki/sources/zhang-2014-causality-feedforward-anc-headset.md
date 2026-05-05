---
type: source
created: 2026-05-05
updated: 2026-05-05
sources:
  - raw/papers/zhang-2014-causality-feedforward-anc-headset/full-text.md
  - https://doi.org/10.1016/j.apacoust.2014.01.004
  - zotero://select/items/0_65C4ZVGB
tags:
  - active-noise-control
  - feedforward-anc
  - causality
  - direction-of-arrival
  - headset
---

# Zhang & Qiu 2014: Causality Study on Feedforward ANC Headset with Different Noise Directions

**Authors**: [[../entities/limin-zhang|Limin Zhang]]\*, [[../entities/xiaojun-qiu|Xiaojun Qiu]]
**Institution**: Key Laboratory of Modern Acoustics, Institute of Acoustics, Nanjing University, Nanjing 210093, China
**Venue**: Applied Acoustics, Vol. 80, pp. 36–44
**Year**: 2014
**Type**: Journal Article
**DOI**: [10.1016/j.apacoust.2014.01.004](https://doi.org/10.1016/j.apacoust.2014.01.004)
**Zotero**: [65C4ZVGB](zotero://select/items/0_65C4ZVGB)

## Summary

This paper develops a systematic analysis to predict the performance of a feedforward ANC headset as a function of delay, particularly the non-causal delay caused by different noise arrival directions. Using Wiener filter theory with measured primary and secondary paths, the authors show that a typical headset is causal for a 0° source but non-causal for a 90° source, explaining the significant performance degradation at lateral angles. The analysis is validated in both anechoic and reverberant chambers.

## Problem Formulation

The ideal feedforward control filter must satisfy:

$$\mathbf{W}_o(z) = \mathbf{P}(z) / \mathbf{S}(z) \tag{1}$$

where $\mathbf{P}(z)$ is the primary path and $\mathbf{S}(z)$ is the secondary path. When both paths are pure delays, $\mathbf{P}(z) = z^{-\Delta_p}$ and $\mathbf{S}(z) = z^{-\Delta_s}$, the ideal filter becomes:

$$\mathbf{W}_o(z) = z^{-(\Delta_p - \Delta_s)} = z^{-\delta} \tag{3}$$

- If $\delta = \Delta_p - \Delta_s \geq 0$: the system is **causal** — the ideal filter is a pure delay, realizable by an FIR Wiener filter
- If $\delta < 0$: the **causality constraint is violated** — the system is equivalent to a predictor with $|\delta|$ samples delay

## Methodology

### Simplified Pure Delay Model

For band-limited noise modeled as a first-order autoregressive process $q(n) = \alpha q(n-1) + v(n)$, the overall noise reduction is:

$$\eta = 10\log_{10}\frac{1}{1 - \alpha^{2\delta}\mathbf{r}_0^T\mathbf{R}_q^{-1}\mathbf{r}_0} \tag{8a}$$

Key finding: for band-limited noise, non-causal delay degrades performance in **two ways**:
1. **Narrowed attenuation bandwidth** — the frequency range of effective cancellation shrinks
2. **Decreased maximum noise reduction** — the peak cancellation level drops

### Systematic Method with Measured Paths

For practical primary and secondary paths (not pure delays), the Wiener filter is:

$$\mathbf{w} = \mathbf{R}_r^{-1}\mathbf{r}_{rd} \tag{9}$$

where $\mathbf{R}_r = \mathbf{S}\mathbf{R}_{x,L+L_s-1}\mathbf{S}^T$ and $\mathbf{r}_{rd}$ depends on both the secondary path filter $\mathbf{w}_s$ and primary path filter $\mathbf{w}_p$.

The overall noise reduction with measured paths:

$$\eta = 10\log_{10}\frac{r_d(0)}{r_d(0) - \mathbf{r}_{rd}^T(\mathbf{SR}_{x,L+L_s-1}\mathbf{S}^T)^{-1}\mathbf{r}_{rd}} \tag{14a}$$

This formulation applies to both causal and non-causal single-channel systems in various acoustic fields.

### Key Insight on Filter Length

For a practical secondary path with broadband white noise reference:

$$\mathbf{w} = (\mathbf{SS}^T)^{-1}\mathbf{w}_{sp} \tag{18a}$$

where $\mathbf{w}_{sp}$ contains elements from the secondary path filter starting at tap $\Delta_p$. Increasing the control filter length $L$ **cannot** improve non-causal performance (when $\Delta_p < \Delta_s$), because the front part of the ideal impulse response is missing. Larger $L$ can help only when $\Delta_p$ is large enough that the tail of the response is pushed out of the filter window.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| ANC Controller | Tiger ANC II (commercial FXLMS) |
| Sampling Rate | 16 kHz |
| Control Filter Length | 256 taps |
| Secondary/Primary Path Filter Length | 256 taps |
| Head Simulator | B&K 4128C |
| Reference-to-Error Distance | ~5 cm |
| Secondary Source-to-Error Distance | ~2 cm |
| Primary Source Distance | ~50 cm |
| Test Noise | Broadband white, 100–4000 Hz |
| Secondary Path Delay $\Delta_s$ | ~6 samples |
| Primary Path Delay $\Delta_p$ (0°) | ~7 samples (causal) |
| Primary Path Delay $\Delta_p$ (90°) | ~5 samples (non-causal) |

![Block diagram of the feedforward ANC system](raw/papers/zhang-2014-causality-feedforward-anc-headset/figures/fb595bcc7d03dedc08fc8f261695895f37146f1df022c2894360b03abdc05971.jpg)
*Figure 1: Block diagram of a feedforward ANC system with the FXLMS algorithm.*

## Results

### Free-Field Experiments (Anechoic Chamber)

- **0° position** ($\Delta_p = 7 > \Delta_s = 6$, causal): Good agreement between predicted and measured performance. Broadband noise reduction achieved across the target bandwidth.
- **90° position** ($\Delta_p = 5 < \Delta_s = 6$, non-causal): Significantly degraded performance. Both predicted and experimental results show reduced attenuation bandwidth and lower maximum noise reduction, consistent with the theoretical analysis.

![Experimental setup showing 0° and 90° source positions](raw/papers/zhang-2014-causality-feedforward-anc-headset/figures/f31b482f0459ae9013e5e620adb3ca3a7406619422d7be657fc103ea2e512294.jpg)
*Figure 6: Active headset system in the anechoic chamber with two different primary source locations (0° and 90°).*

### Reverberant Chamber Experiments

The systematic analysis method was also validated in a reverberation chamber, showing good agreement between predicted and experimental results. This demonstrates that the proposed method applies not only to free-field conditions but also to more practical sound fields.

### Direction-Dependent Performance

The primary path delay varies with source direction according to:

$$\Delta_p = [(l_2 - l_1)/c + t_a]f_s \tag{19}$$

where $l_1$ is the source-to-reference-microphone distance, $l_2$ is the source-to-error-microphone distance, $c$ is the speed of sound, $f_s$ is the sampling rate, and $t_a$ is the earmuff delay.

## Key Contributions

1. **Quantitative analysis of non-causal performance degradation**: Shows that for band-limited noise, non-causal delay narrows the attenuation bandwidth AND decreases the maximum noise reduction — extending prior work that only considered overall noise reduction
2. **Systematic prediction method (Eqs. 9–14)**: Enables performance prediction with measured primary and secondary paths in arbitrary sound fields, going beyond simplified pure-delay models
3. **Filter length analysis**: Demonstrates that increasing control filter length cannot compensate for non-causality — the missing front part of the impulse response cannot be recovered
4. **Direction-dependent causality demonstration**: Experimentally confirms that a typical feedforward ANC headset is causal at 0° but non-causal at 90°, providing the physical explanation for direction-dependent ANC performance
5. **Reverberant field validation**: Shows the systematic method generalizes beyond free-field conditions

## Related Concepts

- [[../concepts/causality|Causality in ANC]] — the core topic of this paper
- [[../concepts/feedforward-anc|Feedforward ANC]] — the ANC architecture studied
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — the adaptive algorithm used
- [[../concepts/wiener-filter|Wiener Filter]] — the optimal filter framework for the analysis
- [[../concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]] — direction-dependent ANC performance motivates D-SFANC
- [[../concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]] — DoA determines causality condition
- [[../concepts/active-noise-control|Active Noise Control]]

## Related Synthesis

- [[../synthesis/anc-architecture-evolution|ANC Architecture Evolution]]
