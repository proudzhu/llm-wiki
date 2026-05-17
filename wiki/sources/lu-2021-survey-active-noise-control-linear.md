---
type: source
created: 2026-05-17
updated: 2026-05-17
sources:
  - raw/papers/lu-2021-survey-active-noise-control-linear/full-text.md
  - https://doi.org/10.48550/arXiv.2110.00531
  - zotero://select/items/0_QVJMFTWC
tags:
  - active-noise-control
  - survey
  - linear-systems
  - adaptive-filtering
  - signal-processing
---

# Lu Lu, Kai-Li Yin, Rodrigo C. de Lamare, Zongsheng Zheng, Yi Yu, Xiaomin Yang & Badong Chen 2021: A Survey on Active Noise Control Techniques — Part I: Linear Systems

| Field | Details |
|-------|---------|
| **Authors** | Lu Lu, Kai-Li Yin, Rodrigo C. de Lamare, Zongsheng Zheng, Yi Yu, Xiaomin Yang, [[entities/badong-chen\|Badong Chen]] |
| **Institutions** | Sichuan University (a,b,d), PUC-Rio (c), Southwest University of Science and Technology (e), Xi'an Jiaotong University (f) |
| **Venue** | arXiv preprint, 2021 |
| **Type** | Survey (73 pages, 17 figures) |
| **DOI** | [10.48550/arXiv.2110.00531](https://doi.org/10.48550/arXiv.2110.00531) |
| **arXiv** | [2110.00531](https://arxiv.org/abs/2110.00531) |
| **Zotero** | [Open](zotero://select/items/0_QVJMFTWC) |

## Summary

Comprehensive survey of linear active noise control (ANC) techniques developed between 2009–2020. The paper systematically reviews filtered-x, filtered-e, and filtered-u families of ANC algorithms, covering FxLMS, FxAP, FxRLS, subband, and lattice-based approaches for broadband, narrowband, and impulsive noise. Practical considerations including online secondary path estimation, acoustic feedback neutralization, error signal measurement, frequency mismatch, and analog control are examined. Novel methods emerging in the past decade — sparse ANC, convex combination schemes, fractional-order ANC, 3-D ANC, selective ANC, distributed ANC, and psychoacoustic ANC — are surveyed. Part II (companion paper) covers nonlinear ANC techniques.

## Problem Formulation

### Feedforward ANC Model

The feedforward ANC system generates an anti-noise signal $y(n)$ to cancel the primary disturbance $d(n)$ through destructive interference. The residual error is:

$$e(n) \triangleq d(n) - s(n) * y(n) \tag{1}$$

where $*$ denotes convolution, $s(n)$ is the impulse response of the secondary path $S(z)$, and $y(n) = \boldsymbol{w}^T(n)\boldsymbol{x}(n)$ is the controller output.

### Feedback ANC Model

The feedback ANC system uses only the error microphone, without a reference microphone. It suffers from the **"waterbed effect"** — suppressing noise at some frequencies increases noise at others. Feedback systems are typically limited to narrowband noise due to stability constraints.

### Hybrid ANC Model

Combines feedforward and feedback structures, where $y(n) = y_f(n) + y_b(n)$, offering high design flexibility for both correlated and uncorrelated noise.

## Methodology

### 1. Filtered-x ANC Family

**FxLMS Algorithm** (Sec. 2.1): The most widely used ANC algorithm. Weight update:

$$\boldsymbol{w}(n+1) = \boldsymbol{w}(n) + \mu e(n) \boldsymbol{X}(n) \tag{2}$$

where $\boldsymbol{X}(n) = s(n) * \boldsymbol{x}(n)$ is the reference signal filtered by the secondary path. Key to the "filtered-x" structure.

**FxLMS variants for broadband noise**:
- **Leaky FxLMS** (LFxLMS): Adds leakage factor $\gamma$ to prevent numerical instability:
  $$\boldsymbol{w}(n+1) = (1 - \mu\gamma)\boldsymbol{w}(n) + \mu e(n)\boldsymbol{X}(n) \tag{3}$$
- **HOEP-based** (e.g., FxLMK, LFxLMF): Use higher-order error moments for non-Gaussian noise
- **Frequency-domain FxLMS**: Reduces computational complexity via wavelet packet, Fourier transform, or block processing

**FxLMS variants for narrowband noise** (NANC):
- **VSS-FxLMS**: Variable step size for fast convergence and low residue trade-off
- Parallel/direct NANC implementations for faster convergence

**FxLMS variants for impulsive noise** (AINC):
- **Akhtar's algorithm**: Clips both input and error signals with thresholds $c_1, c_2$:
  $$e'(n) = \begin{cases} c_1, & e(n) \leq c_1 \\ c_2, & e(n) \geq c_2 \\ e(n), & \text{otherwise} \end{cases} \tag{4}$$
- **FxlogLMS**: Minimizes squared logarithmic transformation of error:
  $$\boldsymbol{w}(n+1) = \boldsymbol{w}(n) + \mu \operatorname{sgn}\{e(n)\} \frac{\log|e(n)|}{|e(n)|} \boldsymbol{X}(n) \tag{5}$$
- **FxLMP/FxgsnLMS**: Fractional lower-order moment (FLOM) based; M-estimator variants (Huber, Fair, Hampel)

**Secondary path modeling error effect**: FxLMS converges when $\hat{S}(z)$ and $S(z)$ have the same sign. A simple single-coefficient secondary path model can maintain performance.

**FxAP Algorithm** (Sec. 2.1.2): Affine projection update using multiple input vectors:

$$\boldsymbol{w}(n+1) = \boldsymbol{w}(n) + \mu \boldsymbol{U}(n)[\boldsymbol{U}^T(n)\boldsymbol{U}(n)]^{-1}\boldsymbol{e}(n) \tag{7}$$

where $P$ is the projection order. Faster convergence than FxLMS for correlated signals.

**FxRLS Algorithm** (Sec. 2.1.3): Fastest convergence among LMS-type algorithms, with highest complexity. Hybrid FxNLMS/FxRLS switching schemes trade off convergence vs. residual error.

**Subband ANC** (Sec. 2.1.4): Decomposes signal into subbands via analysis filter banks, enabling fast convergence for long channel responses with low complexity. Delayless SAF algorithms avoid secondary path estimation overhead.

**Lattice ANC** (Sec. 2.1.5): Gradient adaptive lattice (GAL) and RLS lattice (RLSL) algorithms with secondary path innovation (SPI) and lattice-order decision (LOD).

### 2. Filtered-e ANC Family

**FeLMS Algorithm** (Sec. 2.2): Filters the error signal through $H(z)$ instead of filtering reference through $\hat{S}(z)$. Two types:
- **ALMS** (Adjoint LMS): $H(z) = z^{-\beta} \hat{S}^*(z)$
- **SPE** (Secondary Path Equalization): $H(z) = [z^{-\beta} \hat{S}^{-1}(z)]_+$

Weight update: $\boldsymbol{w}(n+1) = \boldsymbol{w}(n) + \mu e_f(n) \boldsymbol{X}(n-\beta) \tag{10}$

**FxFeLMS**: FeLMS with secondary path filtering on both input and error paths.

### 3. Filtered-u ANC Family

**FuLMS Algorithm** (Sec. 2.3): Updates IIR filter coefficients (poles and zeros):

$$\boldsymbol{a}(n+1) = \boldsymbol{a}(n) + \mu_1 e(n) \boldsymbol{y}(n-1) \tag{11a}$$
$$\boldsymbol{b}(n+1) = \boldsymbol{b}(n) + \mu_2 e(n) \boldsymbol{X}(n) \tag{11b}$$

IIR-based ANC uses fewer coefficients than FIR, but cannot ensure global convergence due to multimodal error surface.

### 4. Computational Complexity

| Algorithm | Multiplications per iteration |
|-----------|-------------------------------|
| FxLMS | $2M + L_s + 1$ |
| FxAP | $2P^2M + 2PM + M + L_s$ |
| FxRLS | $3M^2 + 5M + L_s + 2$ |
| Subband ANC | $3M + NL_a + 2(L_a+1) + L_s$ |
| FxGAL | $21M + 2L_s$ |
| FeLMS (ALMS) | $2M + L_s + 1$ |
| FeLMS (SPE) | $2M + L_p + 1$ |
| FuLMS | $2(L_f + L_b) + L_s + 1$ |

$M$: filter length, $L_s$: secondary path model length, $P$: projection order, $N$: subband count, $L_a$: analysis filter length.

## Practical Considerations

### Online Secondary Path Estimation (Sec. 3.1)

When the secondary path is time-varying, offline estimation becomes inadequate. Auxiliary noise injection (white Gaussian noise) is the standard technique. Key methods:
- **MFxLMS** (Akhtar): Modified FxLMS with online secondary path estimation
- LMS-Newton algorithm: faster convergence for highly correlated inputs; can match RLS with $2\mu = 1-\lambda$
- Variable threshold selective updating
- **PLL-based**: Phase-locked loop for enhanced tracking (mirror-FxLMS algorithm)

### Acoustic Feedback Neutralization (Sec. 3.2)

The anti-noise output propagates upstream to the reference microphone, corrupting the reference signal. Solution: feedback path neutralization (FBPN) filter $\hat{F}(z)$, adapted offline or online with auxiliary noise injection and VSS schemes.

### Error Signal Measurement (Sec. 3.3)

- **Communication error** $e_c(n)$: accounts for sequence ordering in filter/secondary path cascade
- **Adaptive Noise Equalizer** (ANE): gain parameter $\theta$ controls attenuation/amplification:
  $$e(n) \triangleq d(n) - (1-\theta) y(n) \tag{13}$$
- **Virtual Microphone** (Remote Microphone Technique, RMT): estimates error at a location without a physical sensor using two secondary path models $\hat{S}_p(z)$ and $\hat{S}_v(z)$

### Frequency Mismatch (Sec. 3.4)

Actual vs. synthesized reference frequency mismatch in NANC can cause severe degradation even at 1%. Adaptive notch filtering (ANF) and parallel ANF are used for compensation.

### Feedback ANC Design (Sec. 3.5)

Non-adaptive vs. adaptive feedback systems. Simplified feedback ANC uses residual noise directly as reference signal.

### Analog Control (Sec. 3.6)

Analog feedback loops (negative feedback) for headphones — inexpensive, good broadband reduction, short delay. Digital-analog hybrid systems combine advantages.

### Active Structural Acoustic Control (ASAC, Sec. 3.8)

Controls vibration of casings to reduce machinery noise. Multi-channel FxLMS, iterative learning control (ILC), distributed switched-error FxLMS for active casings.

### Fuzzy Control (Sec. 3.9)

Takagi-Sugeno (TS) fuzzy models for handling nonlinear distortions and uncertainties. Combined with ANNs to form fuzzy ANNs (reviewed in Part II).

## Novel Methods (Past Decade)

### Psychoacoustic ANC (Sec. 4.1)

Weighting reference and error signals by human hearing sensitivity. Uses **loudness** (not SPL) as performance metric. Masking-based subband PANC for reduced computational cost and improved perceptual quality.

### Sparse ANC Algorithms (Sec. 4.2)

Exploit sparsity in primary/secondary paths or noise sources:
- **FxIPNLMS**: Improved proportionate NLMS
- **ZA/RZA** strategies (zero-attracting / reweighted zero-attracting)

### Convex Combination ANC (Sec. 4.3)

Two filters (fast+slow step sizes) combined via mixing parameter $\lambda(n)$:

$$e(n) = \lambda(n) e_1(n) + [1-\lambda(n)] e_2(n) \tag{15a}$$
$$y(n) = \lambda(n) y_1(n) + [1-\lambda(n)] y_2(n) \tag{15b}$$

Applied to single/multi-channel ANC and impulsive noise (convex FxLMP).

### Fractional-order ANC (Sec. 4.4)

- **GL-based**: Grünwald-Letnikov fractional calculus for online secondary path estimation
- **RL-based**: Riemann-Liouville operator for FeLMS parameter updates
- **FrFT**: Fractional Fourier transform for LFM signals

### 3-D ANC (Sec. 4.5)

Controls sound in 3D space using transfer function $\mathcal{H}(\omega)$ involving spherical Bessel functions. Creates quiet zones (ZoQ) of arbitrary shapes.

### Selective ANC (Sec. 4.6)

Selects pre-tuned control filters based on audio features instead of real-time computation. Improved robustness and reduced complexity.

### Distributed ANC (Sec. 4.7)

For WASNs over geographic regions:
- **Incremental strategy (IFxLMS)**: Cyclic path over nodes
  $$\boldsymbol{w}_k(n) = \boldsymbol{w}_{k-1}(n) + \mu_k \boldsymbol{X}_k(n) e_k(n) \tag{18}$$
- **Diffusion strategy (DFxNLMS)**: Each node communicates with neighbors
  $$\boldsymbol{\varphi}_k(n+1) = \boldsymbol{w}_k(n) + \mu_k \frac{\boldsymbol{X}_k(n)}{\|\boldsymbol{X}_k(n)\|^2} e_k(n)$$
  $$\boldsymbol{w}_k(n+1) = \sum_{l \in \mathcal{N}_k} a_{l,k} \boldsymbol{\varphi}_l(n+1) \tag{19}$$
- **DFxAP**: Diffusion FxAP with convergence analysis

## Key Contributions

1. **Comprehensive survey**: Systematic review of linear ANC algorithms from 2009–2020, covering filtered-x, filtered-e, and filtered-u families across broadband, narrowband, and impulsive noise
2. **Practical considerations** catalog: Online secondary path estimation, acoustic feedback, error signal measurement, frequency mismatch, feedback design, analog control, ASAC, fuzzy control, and computational complexity reduction methods
3. **Novel method taxonomy**: Classification of emerging approaches — sparse, convex combination, fractional-order, 3-D, selective, psychoacoustic, and distributed ANC
4. **Computational complexity comparison**: Unified table of per-iteration multiplication counts for all major algorithm families
5. **Two-part structure**: Companion Part II covers nonlinear ANC, heuristic-based ANC, and applications

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/hybrid-anc|Hybrid ANC]]
- [[concepts/narrow-band-feedforward-anc|Narrowband Feedforward ANC]]
- [[concepts/multi-channel-anc|Multi-channel ANC]]
- [[concepts/impulsive-noise|Impulsive Noise]]
- [[concepts/active-vibration-control|Active Vibration Control]]
- [[concepts/frequency-domain-anc|Frequency-domain ANC]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]
- [[concepts/adjoint-lms-algorithm|Adjoint LMS Algorithm]]
- [[concepts/internal-model-control|Internal Model Control]]
- [[concepts/maximum-correntropy-criterion|Maximum Correntropy Criterion]]
- [[concepts/information-theoretic-learning|Information Theoretic Learning]]
- [[concepts/virtual-sensing|Virtual Sensing]]
- [[concepts/online-secondary-path-estimation|Online Secondary Path Estimation]]
- [[concepts/distributed-anc|Distributed ANC]]
- [[concepts/psychoacoustic-anc|Psychoacoustic ANC]]
- [[concepts/selective-anc|Selective ANC]]
- [[concepts/active-structural-acoustic-control|Active Structural Acoustic Control (ASAC)]]
- [[concepts/convex-combination-anc|Convex Combination ANC]]
- [[concepts/sparse-anc|Sparse ANC]]
- [[concepts/subband-adaptive-filter|Subband Adaptive Filter]]
- [[concepts/acoustic-feedback|Acoustic Feedback]]

## Related Synthesis

- [[synthesis/adaptive-algorithm-tradeoffs|Adaptive Algorithm Tradeoffs]]
- [[synthesis/anc-architecture-evolution|ANC Architecture Evolution]]
- [[synthesis/feedback-anc-filter-design|Feedback ANC Filter Design]]
- [[synthesis/impulsive-noise-control|Impulsive Noise Control]]
- [[synthesis/secondary-path-modeling-evolution|Secondary Path Modeling Evolution]]
- [[synthesis/virtual-sensing-evolution|Virtual Sensing Evolution]]
- [[synthesis/multichannel-anc-efficiency-and-robustness|Multichannel ANC Efficiency and Robustness]]
- [[synthesis/nonlinear-anc-approaches|Nonlinear ANC Approaches]]
