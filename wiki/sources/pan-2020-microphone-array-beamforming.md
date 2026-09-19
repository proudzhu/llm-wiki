---
type: source
created: 2026-09-19
updated: 2026-09-19
sources:
  - raw/papers/pan-2020-microphone-array-beamforming/full-text.txt
  - https://doi.org/10.16798/j.issn.1003-0530.2020.06.002
  - https://signal.ejournal.org.cn/cn/article/id/10822
  - zotero://select/items/0_Q4KEE9U8
tags:
  - beamforming
  - microphone-arrays
  - survey
  - spatial-audio
  - speech-enhancement
---

# Pan, Huang & Chen 2020: Microphone Array Beamforming Methods for Speech Communication and Interaction

**Authors**: [[entities/chao-pan|Chao Pan]], [[entities/gongping-huang|Gongping Huang]], [[entities/jingdong-chen|Jingdong Chen]]
**Affiliations**: 1. Center of Intelligent Acoustics and Immersive Communications, Northwestern Polytechnical University, Xi'an, China; 2. Technion — Israel Institute of Technology, Haifa, Israel
**Venue**: 信号处理 (Journal of Signal Processing), Vol. 36, No. 6, pp. 804–815, June 2020
**Type**: journalArticle (review/survey, Chinese-language; English title "Microphone Array Beamforming: an Overview")
**DOI**: [10.16798/j.issn.1003-0530.2020.06.002](https://doi.org/10.16798/j.issn.1003-0530.2020.06.002)
**Zotero**: [Q4KEE9U8](zotero://select/items/0_Q4KEE9U8)
**Funding**: National Key R&D Program 2018AAA0102200; NSFC Key Project 61831019; NSFC Young Scientists 61901318; China–Israel Cooperation 61761146001
**References**: 93

## Summary

This is a Chinese-language overview of microphone array beamforming for immersive speech communication (临境语音通信) and intelligent voice interaction (智能语音交互), both of which face the problem of far-field, high-fidelity sound acquisition in complex acoustic environments. The review surveys six beamforming method families — delay-and-sum, superdirective, differential, orthogonal-series-expansion, Kronecker product, and adaptive — organized by their underlying design philosophies, and unifies them through a three-axis performance framework: directivity factor (DF), white noise gain (WNG), and beampattern frequency invariance. The focus is on principles, mechanisms, and architectures rather than algorithmic implementation details.

## Taxonomy

The review's central organizing device is a **design-philosophy taxonomy** of six beamforming families, together with the challenges that motivate them:

**Application challenges** (Section 1): pickup distance growing from centimeters to meters (inverse-square law: SNR drops at least 6 dB per doubling of distance); complex environments with noise, echo, multi-source interference, multipath, and late-reverberation; fast time-varying, highly nonstationary acoustics (temperature, wind, moving platforms); and multi-function systems requiring far-field pickup, duplex communication, wake-up, and recognition simultaneously. Single-sensor systems cannot meet these needs; the resulting demands on a beamformer are (i) consistent array response over a 20 Hz–20 kHz bandwidth, (ii) high gain from small apertures / few sensors (especially at low frequencies), and (iii) robustness to fast time-varying, nonstationary environments.

| Method family | Design philosophy | Strengths | Weaknesses |
|---|---|---|---|
| Delay-and-sum (DSBF) | Coherent summation of time-aligned target components | Maximum WNG (most robust), simple | Poor low-frequency directivity; frequency-varying beampattern |
| Superdirective | Maximize directivity factor against isotropic noise | Highest DF (up to $M^2$ for small arrays); near-equal sidelobes; good frequency consistency | Low WNG, sensitive to sensor self-noise/mismatch |
| Differential (DMA) | Measure the differential sound field | Frequency-invariant directivity; high DF per sensor; ideal for small apertures | Severe white-noise amplification at low frequencies; limited steering (linear arrays) |
| Orthogonal series expansion | Approximate a target beampattern via orthogonal series | Flexible beampattern design; relaxed sensor-placement requirements; analytic performance relations | Robustness/pattern-accuracy trade-off via loading parameter; Bessel-zero singularities (circular arrays) |
| Kronecker product | Task decomposition into subarray subfilters | Divide-and-conquer design; one subfilter for pattern, one for WNG; low-dimensional covariance inversions | Requires array geometry that factorizes (original formulation) |
| Adaptive (MVDR/LCMV/GSC) | Optimization using noise statistics | Optimal noise suppression for the actual noise field | Parameter estimation is hard in nonstationary, reverberant scenes; self-cancellation and distortion from steering errors |

**Unifying performance framework** (Section 2): all fixed designs are evaluated on the directivity factor

$$\mathcal{D}[\mathbf{h}(\omega)] = \frac{|\mathbf{h}^H(\omega)\mathbf{d}(\theta_s,\omega)|^2}{\mathbf{h}^H(\omega)\boldsymbol{\Gamma}(\omega)\mathbf{h}(\omega)}$$

(with $\boldsymbol{\Gamma}$ the isotropic-noise covariance; directivity index $= 10\log_{10}\mathcal{D}$), the white noise gain $= |\mathbf{h}^H\mathbf{d}|^2 / (\mathbf{h}^H\mathbf{h})$, and beampattern frequency invariance. The review's recurring theme is that these three axes trade off against each other and that each method family is a different point on — or a different way of navigating — this trade-off surface.

## Methodology (Surveyed Methods)

### Delay-and-Sum Beamforming

$\mathbf{h}_{\mathrm{DS}} = \mathbf{d}(\theta_s,\omega)/M$: delay each channel so target components are time-synchronous, then sum. Distortionless in the look direction ($|\mathcal{A}| = 1$) with maximum WNG, but for an $M=8$, 1 cm-spacing ULA the low-frequency beampatterns are nearly omnidirectional (poor noise suppression) and the beampattern changes with frequency — processing broadband speech with it easily introduces spectral distortion.

### Superdirective Beamforming

Maximize DF subject to distortionless response: $\mathbf{h}_{\mathrm{SD}} = \boldsymbol{\Gamma}^{-1}\mathbf{d} / (\mathbf{d}^H\boldsymbol{\Gamma}^{-1}\mathbf{d})$, with DF approaching $M^2$ for small apertures. The review highlights three alternative interpretations: it is a special case of differential beamforming (both respond to the differential field), and it is the MVDR beamformer specialized to isotropic noise. Its Achilles' heel is low WNG; remedies surveyed include (i) combining with DSBF to trade directivity against WNG, (ii) subspace methods, (iii) diagonal loading (equivalent to modeling a mixture of isotropic noise and sensor self-noise; $\epsilon = 10^{-3}$ shown), and (iv) explicit WNG/norm constraints via convex optimization. Most classical remedies, however, seriously degrade frequency invariance. A two-stage cascade design (beamformer = convolution of two subfilters; beampattern = product of sub-patterns; one stage maximizes DF, the other improves WNG) preserves frequency consistency — this cascade was later generalized into Kronecker product beamforming.

### Differential Beamforming

Like the pressure-gradient microphone, DMAs measure spatial derivatives of the pressure field (finite-order spatial differences approximating the differential field; inter-element spacing must be far below the smallest wavelength). Properties: frequency-invariant beampattern, higher DF than DSBF with the same sensor count, superdirective beamforming as a special case. The traditional multistage cascade (an $N$th-order DMA = difference of two $(N{-}1)$th-order DMAs; $N{+}1$ pressure microphones) has fixed structure, poor robustness handling, and is awkward to analyze. The **null-constraint design** (Benesty & Chen) writes beampattern null positions plus the distortionless constraint as a linear system $\mathbf{C}^T(\omega)\mathbf{h}(\omega) = \mathbf{g}_1$; with $M > N{+}1$ microphones the remaining degrees of freedom maximize WNG, giving the robust max-WNG null-constraint DMA — increasing sensor count raises WNG, directly attacking the white-noise amplification bottleneck. This framework flexibly produces the classical patterns (dipole, cardioid, hypercardioid, supercardioid, Chebyshev); the $N$th-order minimum null position cannot be smaller than a bound. Further surveyed lines: multistage-cascade theory (equivalence to linear-constraint DMAs; robust DMAs decomposable into a differential stage plus a robustness stage; excess sensors introduce high-frequency extra nulls, requiring order constraints), circular DMAs with Jacobi-series design and concentric circular arrays (improved high-frequency frequency invariance, robustness, directivity), **fractional-order DMAs** (lifting the integer-order restriction; the order can be computed from a target DF or WNG threshold), planar-array generalizations, and time-domain DMAs. Linear DMAs steer poorly (end-fire by construction; steering off end-fire can yield negative gain).

### Orthogonal Series Expansion Beamforming

A beampattern-approximation approach for small apertures: expand the target beampattern in an orthogonal series (Chebyshev, Legendre, Jacobi, spherical harmonics) $\mathcal{B}_N(\theta) = \sum_{n=0}^{N} a_n \mathcal{P}_n(\theta)$ and solve the linear system $\boldsymbol{\Psi}(\omega)\mathbf{h}(\omega) = \boldsymbol{\varrho}$ so the array beampattern approximates it. Minimizing $\mathbf{h}^H\boldsymbol{\Psi}\mathbf{h}$ controls the pattern error; a loading parameter $\delta$ inside $\boldsymbol{\Psi}(\delta)$ controls WNG (larger $\delta$ = more robust, worse frequency consistency; $\delta = 0$ gives the MMSE-optimal pattern approximation). The Jacobi-series circular-array frequency-invariant design comes with analytic relations between beampattern, DF, WNG, and the number/radius of sensors; when Bessel functions approach zeros (high frequencies) filter coefficients diverge (singularity), which concentric circular arrays and a center microphone remedy. Spherical-harmonic-decomposition beamforming (e.g., Eigenmike) requires strict sensor placement for orthogonality, whereas series-expansion designs place sensors flexibly.

### Kronecker Product Beamforming

When the geometry factorizes, the steering vector decomposes as $\mathbf{d} = \mathbf{d}_1 \otimes \mathbf{d}_2$ and the beamformer as $\mathbf{h} = \mathbf{h}_1 \otimes \mathbf{h}_2$, making the array beampattern the **product** of the two subarray beampatterns. Design strategy: one subfilter (small-aperture subarray) designs the target frequency-invariant pattern while the other is constrained flat (spatial all-pass) to exploit the remaining degrees of freedom for WNG — the flat constraint costs no degrees of freedom at low frequencies, so redundant low-frequency freedom is fully converted into robustness. Extensions surveyed: arbitrary sensor counts for uniform linear arrays, and planar arrays with flexible steering. For adaptive variants, the decomposition splits the covariance inversion into small-aperture (adaptive, exploiting noise correlation) and large-aperture (plain DSBF) pieces, drastically reducing dimensionality and improving estimation accuracy and robustness. See [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]] for the subsequent development (Cohen 2019, Wang 2021, Zhu 2025).

### Adaptive Beamforming

MVDR: $\mathbf{h}_{\mathrm{MVDR}} = \boldsymbol{\Phi}^{-1}\mathbf{d} / (\mathbf{d}^H\boldsymbol{\Phi}^{-1}\mathbf{d})$ with $\boldsymbol{\Phi}$ the observation/noise covariance. In practice the required parameters (source DOA, steering vector, interference/noise covariance) are hard to estimate in multi-source, nonstationary, reverberant, time-varying scenes; errors degrade suppression and cause target self-cancellation. The review covers: **relative transfer function (RTF)** methods (replace the modeled steering vector with the RTF vector to handle steering mismatch), **multichannel filtering** (reformulate steering-vector estimation as covariance estimation, bypassing explicit localization), LCMV (additional directional response constraints), and GSC (fixed beamformer + blocking filter + adaptive noise canceller; equivalent to MVDR at convergence but unconstrained in form, hence a robust implementation). Degenerations unify the field: white noise → MVDR reduces to DSBF; isotropic noise → superdirective; isotropic + white noise → robust superdirective; point-source interference → connections to LCMV and DMAs.

## Applications Survey

The review is methods-centric; application guidance is embedded in the motivation and the comparison of design philosophies rather than per-domain experiments:

| Application driver (Section 1) | Requirement | Best-suited families per the review's framing |
|---|---|---|
| Teleconferencing, remote collaboration, smart screens, smart home, security monitoring | Far-field pickup (meters) with SNR loss ≥ 6 dB per distance doubling | Any high-DF design; superdirective/DMA for small apertures |
| Broadband speech/audio fidelity (20 Hz–20 kHz) | Frequency-invariant beampattern | DMA, orthogonal-series (Jacobi circular), Kronecker with flat subfilter |
| Consumer electronics (space/cost limits) | Small aperture, few sensors, robustness | DSBF (max WNG); max-WNG null-constraint DMA (add sensors to raise WNG); diagonal-loaded superdirective |
| Time-varying, nonstationary environments (robots, moving sources) | Adaptivity + robust parameter estimation | Adaptive (MVDR/GSC) when estimable; fixed + robust designs otherwise |
| Duplex communication, wake-up, recognition (multi-function front-ends) | Low complexity, cascaded processing | Fixed beamformers (low run-time cost); Kronecker (low-dimensional inversions) |

## Key Contributions

1. **Design-philosophy taxonomy**: organizes the field into six families (delay-and-sum / superdirective / differential / orthogonal-series / Kronecker / adaptive), each characterized by a one-sentence design idea — coherent summation, maximum directivity, differential-field measurement, beampattern approximation, task decomposition, and optimization, respectively.
2. **Unifying performance framework**: the DF–WNG–frequency-invariance triangle as the common evaluation axes for all fixed beamforming designs, with the explicit observation that classical robustness remedies (diagonal loading etc.) purchase WNG at the price of frequency invariance.
3. **Lineage synthesis**: traces Kronecker product beamforming back to two-stage cascade superdirective/DMA designs; identifies superdirective beamforming as simultaneously a special case of differential beamforming and the isotropic-noise MVDR; and tabulates the degeneration cases of MVDR (white noise → DSBF, isotropic → superdirective, etc.).
4. **Practical robustness rules of thumb**: sensor self-noise of most microphones is 20–35 dBA, so WNG above −20 dB generally avoids white-noise amplification problems in real systems.
5. **Open-problem agenda**: (i) high gain — fixed beamformers' directivity is upper-bounded by the square of the sensor count, which small arrays cannot afford; (ii) white-noise amplification — fundamental solutions still missing; (iii) frequency invariance — lacking both a measure and a design theory; (iv) dynamic array topology optimization (exploiting platform motion online); (v) microphone sensor networks (distributed multi-channel systems whose processing theory is not yet systematized).

## Limitations and Caveats

- **Literature cutoff (2020)**: predates neural beamforming and neural directional filtering, which have since changed the order-per-sensor limits discussed here (e.g., [[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024]] realize a 3rd-order DMA pattern with 4 microphones).
- **Qualitative comparison only**: the review deliberately omits quantitative benchmark tables and algorithmic derivations, deferring to the cited primary literature.
- **Chinese-language venue**: limits international visibility relative to IEEE journal surveys; the concepts nonetheless track the international literature closely (93 references).
- **Extraction caveat**: the archived `full-text.txt` (pdftotext) has embedded-font encoding damage in the equations, English abstract, and reference list; the Chinese prose is intact. Page-level bibliographic details were cross-checked against the journal's web page.

## Related Concepts

- [[concepts/beamforming|Beamforming]]
- [[concepts/fixed-beamformer|Fixed Beamformer]]
- [[concepts/superdirective-beamforming|Superdirective Beamforming]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/frequency-invariant-beamforming|Frequency-Invariant Beamforming]]
- [[concepts/orthogonal-series-expansion-beamforming|Orthogonal Series Expansion Beamforming]]
- [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/lcmv-beamformer|LCMV Beamformer]]
- [[concepts/gsc-beamformer|GSC Beamformer]]
- [[concepts/kmvdr-beamformer|KMVDR Beamformer]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/diagonal-loading|Diagonal Loading]]
- [[concepts/relative-transfer-function|Relative Transfer Function]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]

## Related Sources

- [[sources/cohen-2019-differential-kronecker-beamforming|Cohen, Benesty & Chen 2019: Differential Kronecker Product Beamforming]] — the Kronecker line's journal formulation, generalizing the cascade designs surveyed here
- [[sources/wang-2021-kronecker-adaptive-beamforming|Wang et al. 2021: Kronecker Product Adaptive Beamforming for Microphone Arrays]] — arbitrary-geometry generalization of the Kronecker family
- [[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025: Low-Rank Robust Superdirective Beamforming Using Multidimensional Kronecker Products]] — cites this review; multidimensional N-way, rank-P continuation of the Kronecker program
- [[sources/xiang-2025-wiener-gain-reverberant|Xiang et al. 2025: Design of the Wiener Gain in Noisy and Reverberant Environments]] — same NPU/CIAC group; uses the robust superdirective design as the spatial front-end of a joint noise/reverberation Wiener post-filter
