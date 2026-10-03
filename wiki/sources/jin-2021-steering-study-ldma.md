---
type: source
created: 2026-10-03
updated: 2026-10-03
sources:
  - raw/papers/jin-2021-steering-study-ldma/full-text.txt
  - https://doi.org/10.1109/TASLP.2020.3038566
  - zotero://select/items/0_YBYGP2JB
tags:
  - beamforming
  - differential-microphone-array
  - microphone-arrays
  - beam-steering
  - fixed-beamformer
  - spatial-audio
---

# Jin, Huang, Wang, Chen, Benesty & Cohen 2021: Steering Study of Linear Differential Microphone Arrays

**Authors**: [[entities/jilu-jin|Jilu Jin]], [[entities/gongping-huang|Gongping Huang]], [[entities/xuehan-wang|Xuehan Wang]], [[entities/jingdong-chen|Jingdong Chen]], [[entities/jacob-benesty|Jacob Benesty]], [[entities/israel-cohen|Israel Cohen]]
**Institution**: Center of Intelligent Acoustics and Immersive Communications, Northwestern Polytechnical University, Xi'an, China; Technion — Israel Institute of Technology, Haifa, Israel; INRS-EMT, University of Quebec, Montreal, Canada
**Venue**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 29, pp. 158–170, 2021
**Type**: Journal article
**DOI**: [10.1109/TASLP.2020.3038566](https://doi.org/10.1109/TASLP.2020.3038566)
**Zotero**: [YBYGP2JB](zotero://select/items/0_YBYGP2JB)

## Summary

Most linear differential microphone array (LDMA) beamformers assume the source of interest lies at the endfire direction (0°). This paper studies when and how an LDMA's mainlobe can be steered to an arbitrary look direction. Through analysis of the **ideal function** — the Nth-order polynomial $P_N(x)$, $x = \cos\theta$, underlying every DMA beampattern — the authors prove that first-order LDMAs are **not steerable** (their extrema can only occur at endfire), deduce the fundamental null-position conditions under which Nth-order ($N \geq 2$) LDMAs are **partially steerable**, and propose a null-constrained design method for steerable LDMAs (SLDMAs) validated in simulation and with an 8-microphone prototype array measured in an anechoic chamber.

## Problem Formulation

A plane wave impinges on a uniform linear array of $M$ omnidirectional microphones with spacing $\delta \ll \lambda$. With $x = \cos\theta$ and $\varepsilon = \omega\delta/c$, the phase vector is

$$
\mathbf{d}(\omega, \cos\theta) = \begin{bmatrix} 1 & e^{-j\varepsilon\cos\theta} & \cdots & e^{-j(M-1)\varepsilon\cos\theta} \end{bmatrix}^T
$$

and the beamformer output is $Z(\omega) = \mathbf{h}^H(\omega)\mathbf{y}(\omega)$ subject to the distortionless constraint $\mathbf{h}^H(\omega)\mathbf{d}(\omega, \cos\theta_s) = 1$ at the look direction $\theta_s$. Performance is evaluated by beampattern, [[concepts/white-noise-gain|white noise gain]] (WNG), and directivity factor (DF).

For steering, three scenarios are distinguished:

1. **Steerable** — $|\mathcal{B}_{\theta_s}(\theta_s)|^2 = 1$, $|\mathcal{B}_{\theta_s}(\theta)|^2 \leq 1$ everywhere, and the pattern is a rotation of the endfire pattern. *Unachievable with LDMAs.*
2. **Partially steerable** — distortionless and bounded ($\leq 1$), but the pattern varies with $\theta_s$ rather than rotating. *The best achievable with LDMAs; the case studied here.*
3. **Non-steerable** — the pattern exceeds 1 in some directions, amplifying noise/interference; must be avoided by design.

## Methodology

### Ideal function and visible zone

The Nth-order target beampattern is a polynomial $P_N(x) = \sum_{n=0}^{N} a_{N,n} x^n$, factored through its $N$ nulls as $P_N(x) = a_{N,N}\prod_{n=1}^{N}(x - x_n)$ with normalization $P_N(x_s) = 1$. Because the beampattern is periodic in $x$ with period $c/(f\delta) \gg 1$ for small arrays, only the part of $P_N$ inside the **visible zone** $-1 \leq x \leq 1$ maps to physical directions $\theta \in [0°, 180°]$; nulls placed *outside* the visible zone (e.g., the subcardioid's $x_1 = -1.5$) still shape the visible pattern.

### Non-steerability of first-order LDMAs

For $P_1(x) = a_{1,1}x + a_{1,0}$ with $a_{1,1} \neq 0$, the derivative $dP_1/d\theta = -a_{1,1}\sqrt{1-x^2}$ vanishes **only at $x = \pm 1$** (the endfire directions). Hence the mainlobe of a first-order LDMA can only point at 0° or 180°, regardless of the beamforming method used.

### Fundamental steering conditions (N ≥ 2)

Setting $dP_N/dx |_{x=x_s} = 0$ yields the general condition

$$
\sum_{n=1}^{N} n(-1)^{N-n}\,\zeta_{N,n}\, x_s^{\,n-1} = 0,
$$

where $\zeta_{N,n}$ are the elementary symmetric polynomials in the nulls $x_1, \ldots, x_N$. Special cases:

- **Second order**: $x_1 + x_2 = 2x_s$ — the nulls must be placed symmetrically about the steering direction.
- **Third order**: $3x_s^2 - 2\sum_{n=1}^{3} x_n x_s + (x_1x_2 + x_2x_3 + x_1x_3) = 0$.

### SLDMA design with null constraints

Given $\theta_s$, the designer fixes the first $N-1$ nulls per application needs and solves for the last null from the steering condition. With $\mathbf{q}_N(x) = [1, x, \ldots, x^N]^T$ and $\boldsymbol{\Sigma}_N = \mathrm{diag}(0, 1, \ldots, N)$, the coefficient vector follows from the linear system $\mathbf{Q}(\mathbf{x})\,\mathbf{a}_N = \mathbf{i}_1$ (stacking $\mathbf{q}_N^T(x_s)$, the derivative row $\mathbf{q}_N^T(x_s)\boldsymbol{\Sigma}_N$, and null rows), and the last null from $x_N = -a_{N,N-1}/a_{N,N} - \sum_{n=1}^{N-1} x_n$. Nulls with multiplicity $P$ are handled by adding derivative rows $\mathbf{q}_N^T\Sigma_N^p$, $p = 1, \ldots, P-1$ at the repeated null. The beamforming filter is finally obtained from the null-constrained linear system $\mathbf{D}(\omega, \mathbf{x}_N)\mathbf{h}(\omega) = \mathbf{i}_1$ — exactly ($M = N+1$) or by the minimum-norm solution ($M > N+1$), which improves WNG as $M$ grows.

## Experimental Setup

| Item | Value |
|---|---|
| Simulations: 2nd order (SSLDMA-I/II) | $M = 3$, $\delta = 1$ cm; mainlobes at 90° and 75°; $x_1$ pre-specified, $x_2$ from $x_1 + x_2 = 2x_s$ |
| Simulations: 3rd order (TSLDMA-I/II) | $M = 4$, $\delta = 1$ cm; mainlobes at 70° and 45°; $x_3$ from the 3rd-order condition |
| Simulations: 4th order (FSLDMA-I–IV) | $M = 5$, $\delta = 1$ cm; $\mathbf{a}_N$ and $x_4$ from (56)/(57) |
| Nulls with multiplicity | TSLDMA-I ($M=4$) and FSLDMA-II ($M=5$), look direction 60°, null at cos(135°) with multiplicity 2 and 3 |
| Robust design | 2nd-order SLDMA, $x_s = \cos 90°$, $x_1 = \cos 0°$, $x_2 = \cos 180°$, with $M \in \{3, 7, 11, 15\}$ (minimum-norm) |
| Prototype array | 8 omnidirectional electret microphones, 1.1 cm spacing |
| Measurements | Anechoic chamber 11.8 m × 4.2 m × 3.8 m; loudspeaker 2 m from array center, both 60 cm above the absorption floor; rotating platform, 1° steps every 5 s; narrowband excitation; TSLDMA-I ($x_s=\cos 60°$, $x_3=1.1000$) and TSLDMA-II ($x_s=\cos 45°$, $x_3=1.1949$) |

## Results

- **Steering succeeds for $N \geq 2$**: second-, third-, and fourth-order SLDMAs achieve distortionless response at the target look direction with beampatterns that are frequency invariant across the band — the ideal-function parabolas of second-order SLDMAs visibly place nulls symmetrically about $x_s$.
- **DF and WNG vary with $\theta_s$**: a second-order SLDMA attains its maximum DF at endfire, explaining why most LDMA literature fixes the look direction at 0°.
- **Order trade-off persists**: third-order SLDMAs have higher DF but lower WNG than second-order designs, as in conventional DMAs.
- **Robustness via more microphones**: with the minimum-norm solution, WNG improves monotonically as $M$ increases from 3 to 15; the cost is extra high-frequency nulls, i.e., the effective DMA order can exceed the specified order at high frequencies.
- **Measurements match design**: measured beampatterns of TSLDMA-I/II at 3.5 kHz agree with the designed patterns; residual differences are attributed to array imperfections and measurement errors and are negligible.

## Key Contributions

1. **Ideal-function framework**: defines the ideal functions $P_N(x)$ and the visible-zone concept, cleanly separating the polynomial structure of DMA beampatterns from what is physically observable — including the observation that invisible (out-of-zone) nulls are legitimate design degrees of freedom.
2. **Non-steerability proof for first-order LDMAs**: the extrema of $P_1$ can only occur at $x = \pm 1$, so no first-order linear differential beamformer can point its mainlobe off endfire — a negative result delimiting the design space.
3. **Fundamental steering conditions**: closed-form null-position equations (elementary symmetric polynomials in the nulls vs. $x_s$) that an Nth-order LDMA must satisfy for the mainlobe to sit at $\theta_s$.
4. **SLDMA design method**: a null-constrained procedure — fix $N-1$ nulls, solve the steering condition for the last — handling multiple nulls and delivering WNG-robust filters via the minimum-norm solution with extra microphones.
5. **Experimental validation**: an 8-element, 1.1 cm-spaced prototype whose anechoic-chamber beampattern measurements confirm the designed steerable patterns.

## Related Concepts

- [[concepts/steerable-ldma|Steerable LDMA]] — the steering conditions and design method introduced by this paper
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/frequency-invariant-beamforming|Frequency-Invariant Beamforming]]
- [[concepts/beamforming|Beamforming]]

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — classical DMA design lineage (Elko 2004 → De Sena 2012 → null-constraint/steerable designs)
