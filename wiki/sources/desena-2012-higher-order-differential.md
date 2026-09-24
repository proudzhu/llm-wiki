---
type: source
created: 2026-09-24
updated: 2026-09-24
sources:
  - raw/papers/desena-2012-higher-order-differential/full-text.md
  - https://doi.org/10.1109/TASL.2011.2159204
  - zotero://select/items/0_QX5MBZMB
tags:
  - beamforming
  - differential-microphone-array
  - directivity-pattern
  - microphone-arrays
  - spatial-audio
  - fixed-beamformer
---

# De Sena, Hacihabiboglu & Cvetkovic 2012: On the Design and Implementation of Higher Order Differential Microphones

**Authors**: [[entities/enzo-de-sena|Enzo De Sena]], [[entities/huseyin-hacihabiboglu|Hüseyin Hacihabiboglu]], [[entities/zoran-cvetkovic|Zoran Cvetkovic]]
**Institution**: Centre for Digital Signal Processing Research / Department of Electronic Engineering, King's College London, London, U.K.
**Venue**: IEEE Transactions on Audio, Speech, and Language Processing, vol. 20, no. 1, pp. 162–174, Jan. 2012
**Type**: Journal article
**DOI**: [10.1109/TASL.2011.2159204](https://doi.org/10.1109/TASL.2011.2159204)
**Zotero**: [QX5MBZMB](zotero://select/items/0_QX5MBZMB)

## Summary

This paper proposes a systematic design framework for the directivity patterns of higher order differential microphones: patterns are obtained by minimizing a cost function that is a convex combination of a within/out-of-sector energy ratio and a uniformity term inside a frontal sector of interest, controlled by two physically meaningful parameters — the sector width $\alpha$ and the convex combination factor $\lambda$. All standard patterns (omnidirectional, subcardioid, cardioid, hypercardioid, supercardioid) are shown to be particular solutions of this optimization for specific $(\alpha, \lambda)$ pairs. Since many optimal patterns are trigonometric polynomials with complex-conjugate roots, which conventional cascaded differential arrays cannot implement, the authors further propose a new second-order differential array structure using three omnidirectional microphones and a central correction filter that realizes arbitrary real coefficients — and thus complex-root patterns — with the same complexity and noise sensitivity as the conventional design.

## Problem Formulation

An $N$-th order frequency-independent directivity pattern is written as a trigonometric polynomial in the angle of incidence, normalized so that $\Gamma_{\mathbf{a}}(0) = 1$:

$$
\Gamma_{\mathbf{a}} (\theta) = 1 - \sum_{i=1}^{N} a_{i} + \sum_{i=1}^{N} a_{i} \cos^{i}(\theta), \qquad \mathbf{a} = [a_1, \ldots, a_N] \in \mathbb{R}^N
$$

Two problems motivate the paper:

1. **No unifying design criterion.** Standard patterns are isolated optima: the hypercardioid maximizes the directivity factor $Q_{\mathbf{a}}$ (under a cylindrically isotropic sound field), the supercardioid maximizes the front–back ratio $F_{\mathbf{a}}$, while cardioid and subcardioid are heuristic designs with no optimality criterion at all. For higher orders, the coefficient space grows and no systematic, user-friendly design interface exists.
2. **Implementation restriction to real roots.** A conventional $N$-th order differential array is a cascade of $N$ first-order stages, so the achievable patterns are products of first-order factors — i.e., only trigonometric polynomials with **real** roots. Optimal patterns for many $(\alpha, \lambda)$ pairs have **complex-conjugate** roots and cannot be built this way. The differential-integral arrays of Abhayapala & Gupta (2010) can realize general second-order patterns but need $2N+1$ microphones (vs. $N+1$) and cover only one octave band.

## Methodology

### Directivity design framework

The proposed cost function over the sector $\theta \in [0, \alpha]$ is

$$
\Phi_{\mathbf{a}} (\alpha, \lambda) = \lambda \frac{\int_{\alpha}^{\pi} |\Gamma_{\mathbf{a}} (\theta)|^2 d\theta}{\int_{0}^{\alpha} |\Gamma_{\mathbf{a}} (\theta)|^2 d\theta} + (1 - \lambda) \int_{0}^{\alpha} |\Gamma_{\mathbf{a}}' (\theta)|^2 d\theta
$$

and the optimal coefficients are $\tilde{\mathbf{a}} (\alpha, \lambda) = \arg\min_{\mathbf{a}} \Phi_{\mathbf{a}} (\alpha, \lambda)$, with $\lambda \in [0,1]$ and $\alpha \in [0,\pi]$. The first term is the ratio of out-of-sector to in-sector energy (rejection of sources outside the sector of interest); the second term penalizes the derivative of the pattern inside the sector (uniformity of response over the sources of interest). A spherically isotropic variant inserts $\sin(\theta)$ weights into every integral.

**Standard patterns as special cases** (see [[concepts/sector-directivity-design|Sector-Based Directivity Design]]):

| Pattern | $(\lambda, \alpha)$ | Note |
|---|---|---|
| Omnidirectional | $(0, \pi)$ | Trivial constant solution |
| Supercardioid | $(1, \pi/2)$ | Cost becomes inverse front–back ratio |
| Hypercardioid | $(1, \alpha \to 0)$ | Cost becomes total energy → max directivity factor |
| Subcardioid | $\approx(0.5, 2.247\,\mathrm{rad})$ | Approximation error $\ll -100$ dB |
| Cardioid (1st order) | $\approx(1, \pi)$ | Error $\ll -100$ dB; rejects $\theta=\pi$ while keeping sensitivity elsewhere |

Higher-order cardioid-A/B patterns also fit the framework with approximation errors from $-43$ dB down to $\ll -100$ dB. The design space of the framework, with markers for the standard patterns and the regions where optimal patterns have complex roots, is illustrated in Fig. 2; example patterns across the $(\alpha, \lambda)$ grid are shown in Fig. 3.

![[raw/papers/desena-2012-higher-order-differential/figures/416bcdcf35cc6c84416a2910f73546c060bb33248dd3fb6501508065657a9609.jpg|Design space, first order]]
![[raw/papers/desena-2012-higher-order-differential/figures/df474b7e1d553b3729ed0d0177ff8aae697cc7e2f1e94a872d77c2f35688e1c9.jpg|Design space, second order]]
![[raw/papers/desena-2012-higher-order-differential/figures/af5d9aaf2622820e2d1856f9adc9f3fb5da103efc0db21ae193473c790cb2b02.jpg|Design space, third order]]
![[raw/papers/desena-2012-higher-order-differential/figures/b1268c612f15348e3c41e94befd46ba9422e11c4eebdc1eb28ef8a45046b04f0.jpg|Design space, fourth order]]

*Figure 2: Overview of the design space with markers on the existing directivity patterns for (a) first-, (b) second-, (c) third-, and (d) fourth-order patterns. Shaded areas are $(\alpha,\lambda)$ regions whose optimal patterns are trigonometric polynomials with complex roots.*

![[raw/papers/desena-2012-higher-order-differential/figures/464dbb0b64354c1a466305f02413c6872a3755fdd6457d2e04650f2cf6f72798.jpg|Examples of directivity functions]]

*Figure 3: Directivity functions (dB scale) generated by the design framework for a grid of $(\alpha,\lambda)$ pairs and orders 1–4.*

Applications include orchestra recording ($\alpha = \pi/2$ with reduced $\lambda$ for uniform frontal pickup), "acoustical zoom" coupled to a video camera's optical zoom, and teleconferencing where the pattern widens as speaker-position estimates become less reliable.

### Differential array structure with complex roots

The proposed second-order structure uses **three** omnidirectional microphones at positions $[0, -d]$, $[0, 0]$, $[0, +d]$. The outer microphones are delayed by $\tau$ and differenced around the central branch filter $H_0(\omega)$:

$$
x(t, \omega, \theta) = P_0 e^{j\omega t} H_c(\omega) \left( e^{-jkd\cos\theta} - H_0(\omega) + e^{j(kd\cos\theta - \omega 2\tau)} \right)
$$

A second-order Taylor expansion (valid for $|\omega\tau| \ll \pi/2$ and $|kd| \ll \pi/2$), together with the choice

$$
H_0 (\omega) = e^{-j\omega\tau} (2 - \omega^2 \tau^2 + \omega^2 \kappa), \qquad
\kappa = \frac{(1 - a_1 - a_2)}{a_2} \tau_0^2, \qquad
\tau = -\frac{a_1}{a_2} \frac{\tau_0}{2}, \qquad \tau_0 = d/c
$$

makes the array output proportional to any prescribed second-order pattern $\Gamma_{\mathbf{a}}(\theta) = (1-a_1-a_2) + a_1\cos\theta + a_2\cos^2\theta$; the correction filter $H_c(\omega) = 1/\omega^2$ (a double integrator) equalizes the frequency dependence. Because the $\omega^2$ component of $H_0$ cancels against $H_c$, the only hardware actually needed is a fractional delay in the central branch — giving the same filter complexity as the conventional cascade (Figs. 4–5, vs. the conventional design in Fig. 1).

![[raw/papers/desena-2012-higher-order-differential/figures/e09da3c83f77fa4d0839d4aecdcc6c29f4ffb695524b0f5ae0437245fd59491a.jpg|Conventional differential microphone design]]

*Figure 1: Conventional design of differential microphones (Elko 2004). (a) First-order differential microphone. (b) Second-order obtained by cascading two first-order stages — restricted to real-root patterns.*

![[raw/papers/desena-2012-higher-order-differential/figures/cfc1d9cd5c11f9acef2aa377d656ea83006577e56009e8d5d53886740ae04b11.jpg|Proposed second-order differential microphone array structure]]

*Figure 4: Proposed second-order differential microphone array structure with central filter $H_0(\omega)$.*

![[raw/papers/desena-2012-higher-order-differential/figures/e49a43d9b661e521e01dcfddab7752077bd440248a2c105a29e1b28339bebcf7.jpg|Implementation of the proposed structure]]

*Figure 5: Implementation of the proposed structure — the central branch reduces to a fractional delay; the correction filter is a standard double integrator.*

### White noise gain and operational bandwidth

The look-direction [[concepts/white-noise-gain|white noise gain]] of the proposed (complex-root) and conventional (real-root) second-order structures admits closed forms that depend on $a_1, a_2$ only through the product $kd \cdot f(a_1, a_2)$; the two structures have very similar WNG in their respective regions of the $(a_1, a_2)$ plane (Fig. 6). Both become unusable around $kd = 0.1$ unless very low-noise capsules are available.

![[raw/papers/desena-2012-higher-order-differential/figures/d99511cb5f3ab2682b1c1b7363e87bd5cb4fb63b13982c69446e4608a6d1c16a.jpg|WNG, kd = 1]]
![[raw/papers/desena-2012-higher-order-differential/figures/b00de611221bb433ac6364b82e2cc61e49c6bdf130b8a7a0dbc4d60617973105.jpg|WNG, kd = 0.5]]
![[raw/papers/desena-2012-higher-order-differential/figures/58a0f930dbb2adbe531ddc419cf314021773acf32a7aeb6290924fbd5db2b332.jpg|WNG, kd = 0.25]]
![[raw/papers/desena-2012-higher-order-differential/figures/46673a828a8cc3c921af47a8046945bbefde9cb45c0d4526c771d990313d448e.jpg|WNG, kd = 0.1]]

*Figure 6: White noise gain (dB) of the second-order structures for (a) $kd=1$, (b) $kd=0.5$, (c) $kd=0.25$, (d) $kd=0.1$. The proposed structure covers the "complex roots" region, the conventional cascade the "real roots" region.*

The operational bandwidth follows from the Taylor-approximation upper bound and the WNG lower bound:

$$
f_{\min} = \frac{\gamma c}{2\pi d}, \qquad f_{\max} = \frac{c}{4d}
$$

where $\gamma$ is the smallest acceptable $kd$. With $\gamma = 0.25$ (WNG $\geq$ about $-30$ dB; e.g., at $kd = 0.25$ the second-order hypercardioid has WNG $\approx -29.9$ dB, cardioid-B $\approx -25.9$ dB, cardioid-A $\approx -20$ dB, supercardioid $\approx -24.3$ dB), a single array covers more than 2.5 octaves. Bandwidth can be extended by combining arrays with different inter-element distances (e.g., $d_{i+1} = 2d_i$ sharing microphones, or spaced so that sub-band edges meet), at the cost of a few extra capsules; the resulting element counts and bandwidths are tabulated in the paper (Table III).

## Experimental Setup

| Item | Value |
|---|---|
| Optimization | Nelder–Mead (Mathematica `NMinimize`), converges within 0.1 s up to 4th order |
| Design example | Third-order pattern for $(\alpha, \lambda) = (\pi/2, 0.5)$; $\mathbf{a} = [0.7164, 0.4841, -0.3096, 0.1091]$; roots $\theta \approx 1.85 \pm 2.05j$ and $\cos\theta = -0.86$ |
| Implementation | Cascade of 2 complex blocks + 1 real block; maximally flat allpass fractional delays; Al-Alaoui integrator (real block), cascade of 2 Simpson integrators (complex block); 50 Hz high-pass for stability |
| Simulation | $d_1 = 1.27$ cm single array; two-array combination $d_1 = 1.27$ cm, $d_2 = 4d_1 = 5.08$ cm with crossover at $c/4d_2 = 1688$ Hz; input SNR 50 dB; $f_s = 96$ kHz |
| Measurement array | 3+ microphones, AKG C 417 omnidirectional capsules (7.5 mm, 34 dBA self-noise) on a Meccano strip; MOTU 896HD interface; Mackie HR824 loudspeaker |
| Measurement method | Anechoic-style booth (4.56 m × 3.52 m × ...), stepper motor, exponential sine sweeps (1.5 s), 100 angles at 3.6° steps; first 300 reflection-free samples → response down to 320 Hz; per-capsule equalization by 8th-order IIR filters (substitution method) |

## Results

- **Design example** (Fig. 7): the third-order pattern for $(\pi/2, 0.5)$ combines an 8.13 dB front–back ratio with a uniform frontal lobe; sources at $\pi/2$ are attenuated by only ~3 dB. Because this $(\alpha, \lambda)$ pair lies in the complex-root region, it is implemented with two complex blocks plus one real block (Fig. 8).
- **Simulations** (Fig. 9): a single $d = 1.27$ cm array holds the desired response over ~2 octaves (WNG $\geq -20$ dB); combining $d = 1.27$ cm and $d = 5.08$ cm arrays via crossover extends this to ~4 octaves at WNG $\geq -20$ dB with 7 microphones.
- **Measurements** (Fig. 10): the built array reproduces the ideal third-order pattern over **5 octaves** after crossover; the short-spacing array matches at high frequencies, the long-spacing array at low frequencies, and the merged response tracks the ideal pattern across all measured octave bands.

![[raw/papers/desena-2012-higher-order-differential/figures/80d3227f25ab1052adde339b156d3d2a33d24b91f047c01ba2fc48e74ea65d07.jpg|Third-order directivity pattern]]

*Figure 7: Third-order directivity pattern obtained for $\lambda = 0.5$ and $\alpha = \pi/2$.*

![[raw/papers/desena-2012-higher-order-differential/figures/c3ce41cdb6f3ee37b11c8625114be90ae2ee1e80de56fe3ab5d83aa779088a45.jpg|Third-order structure]]

*Figure 8: Structure implementing a third-order directivity pattern with a pair of complex conjugate roots (two complex blocks + one real block).*

![[raw/papers/desena-2012-higher-order-differential/figures/08ecf91667c55350444ed0cb6ff8104e70cf7fdeb670ee9a2c9175cb2facd132.jpg|Simulation, single array]]
![[raw/papers/desena-2012-higher-order-differential/figures/993d7c3552596f45e849d7b3735cee0bd3df93cfffa96c3550092d87a6c95cc6.jpg|Simulation, two arrays]]

*Figure 9: Simulated signal/noise energy and theoretical WNG for the third-order microphone, $\Gamma_{\tilde{\mathbf{a}}(0.5, \pi/2)}$. (a) Single array, $d_1 = 1.27$ cm (2 usable octaves). (b) Two arrays, $d_1 = 1.27$ cm and $d_2 = 5.08$ cm with crossover (4 usable octaves).*

![[raw/papers/desena-2012-higher-order-differential/figures/31479576ae6f4feea17ff4c00d1d9c9ec157dff557cb0a7512964ba6ddefb478.jpg|Measured directivity, short-spacing array]]
![[raw/papers/desena-2012-higher-order-differential/figures/9e6156d7029411ab6edec410f5af8c7c7db539b2af7023018d03032c1877bd42.jpg|Measured directivity, long-spacing array]]
![[raw/papers/desena-2012-higher-order-differential/figures/e87722869fb100b11d0dfec2c5d297060b9544aebdea248975d2f0a951cb92a7.jpg|Measured directivity, merged arrays]]

*Figure 10: Ideal and measured directivity patterns of the third-order differential microphone. (a) $d_1 = 1.27$ cm. (b) $d_2 = 5.08$ cm. (c) Merged via crossover filters — the desired pattern over 5 octaves.*

## Key Contributions

1. **Unifying $(\alpha, \lambda)$ design framework**: a convex-combination cost function (sector energy ratio + in-sector uniformity) whose two free parameters are physically meaningful (sector width, rejection/uniformity trade-off), replacing empirical coefficient tuning for higher order microphones.
2. **Standard patterns as special cases**: omnidirectional, subcardioid, cardioid, hypercardioid, and supercardioid are all shown to be (approximate or exact) minimizers of the same cost function at specific $(\alpha, \lambda)$ pairs, with quantified approximation errors.
3. **Complex-root differential array structure**: a three-microphone second-order structure whose central branch filter $H_0(\omega)$ realizes arbitrary real coefficient pairs — lifting the real-root restriction of cascaded differential arrays at no additional filter complexity.
4. **Closed-form WNG and bandwidth analysis**: WNG expressions for both structures showing dependence on the product $kd$, the operational band $[\gamma c / 2\pi d,\ c/4d]$, and microphone-sharing schemes for multi-array bandwidth extension.
5. **Experimental validation**: a built third-order microphone (two complex blocks + one real block) whose measured directivity matches the designed pattern over 5 octaves.

## Related Concepts

- [[concepts/sector-directivity-design|Sector-Based Directivity Design]] — the $(\alpha, \lambda)$ optimization framework introduced by this paper
- [[concepts/complex-root-differential-array|Complex-Root Differential Array]] — the proposed implementation structure
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/frequency-invariant-beamforming|Frequency-Invariant Beamforming]]
- [[concepts/superdirective-beamforming|Superdirective Beamforming]]
- [[concepts/fixed-beamformer|Fixed Beamformer]]
- [[concepts/beamforming|Beamforming]]

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — classical DMA design lineage (Elko 2004 → De Sena 2012 → null-constraint/Kronecker designs)
