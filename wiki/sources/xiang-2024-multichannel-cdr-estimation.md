---
type: source
created: 2026-09-19
updated: 2026-09-19
sources:
  - raw/papers/xiang-2024-multichannel-cdr-estimation/full-text.md
  - https://doi.org/10.1109/JSEN.2024.3469548
  - zotero://select/items/0_HKC82V92
tags:
  - speech-enhancement
  - dereverberation
  - cdr-estimation
  - coherence
  - multichannel
  - beamforming
---

# Xiang, Lei, Pan, Chen & Benesty 2024: On Multichannel Coherent-to-Diffuse Power Ratio Estimation

**Authors**: [[entities/qian-xiang|Qian Xiang]], [[entities/tao-lei|Tao Lei]], [[entities/chao-pan|Chao Pan]], [[entities/jingdong-chen|Jingdong Chen]], [[entities/jacob-benesty|Jacob Benesty]]
**Institution**: Shaanxi University of Science and Technology, Xi'an; Northwestern Polytechnical University, Xi'an; INRS-EMT, University of Quebec, Montreal
**Venue**: IEEE Sensors Journal, 2024
**Type**: Journal article
**DOI**: [10.1109/JSEN.2024.3469548](https://doi.org/10.1109/JSEN.2024.3469548)
**Zotero**: [HKC82V92](zotero://select/items/0_HKC82V92)

## Summary

Existing coherent-to-diffuse power ratio (CDR) estimators are typically limited to two microphones. This paper investigates CDR estimation in acoustic systems with more than two microphones and proposes two DOA-free multichannel estimators: (1) **weighted-average CDR estimation**, which decomposes the array into groups of two-sensor subarrays (consistent spacing and orientation within each group), estimates a pairwise CDR per group, and fuses the group estimates through softmax-style weights; and (2) **array manifold information-based CDR estimation**, which obtains the array manifold vector via joint matrix diagonalization (GEVD) of the observation and diffuse-noise pseudo-coherence matrices and solves a closed-form CDR — eliminating subarray decomposition entirely. Integrated into a parametric Wiener-type postfilter after a delay-and-sum beamformer, both estimators outperform the two-channel Schwarz method, averaged-coherence, GMSC, and ERANK baselines in CDR accuracy (mse, kurtosis), SNR gain, LSD, and DRR, with results validated on real MARDY room impulse responses.

## Problem Formulation

An $M$-microphone, small-spacing array observes a far-field speech source in a reverberant, noisy environment. In the time-frequency domain, each sensor signal decomposes into a direct-path component and diffuse noise (all multipath components uncorrelated with the direct path):

$$\mathbf{y}(\omega, t) = \mathbf{d}(\omega, \theta) X(\omega, t) + \mathbf{v}(\omega, t)$$

where $\mathbf{d}(\omega, \theta) = [1, e^{\jmath \omega \tau_{2,1}(\theta)}, \dots, e^{\jmath \omega \tau_{M,1}(\theta)}]^{\mathrm{T}}$ is the array manifold vector. With source and diffuse noise uncorrelated, the covariance matrix decomposes as

$$\boldsymbol{\Phi}_{\mathbf{y}} = \phi_{\mathrm{cs}} \boldsymbol{\Gamma}_{\mathrm{cs}}(\theta) + \phi_{\mathrm{dn}} \boldsymbol{\Gamma}_{\mathrm{dn}}$$

where $\boldsymbol{\Gamma}_{\mathrm{cs}} = \mathbf{d}\mathbf{d}^{\mathrm{H}}$ is the source pseudo-coherence matrix and the diffuse-noise pseudo-coherence matrix has spherically isotropic elements $[\boldsymbol{\Gamma}_{\mathrm{dn}}]_{i,j} = \sin(\omega \Delta_{i,j}/c)/(\omega \Delta_{i,j}/c)$. The CDR is $\beta \triangleq \phi_{\mathrm{cs}} / \phi_{\mathrm{dn}}$. Normalizing by the observation variance gives

$$\boldsymbol{\Gamma}_{\mathbf{y}} = \frac{\beta}{\beta + 1} \boldsymbol{\Gamma}_{\mathrm{cs}}(\theta) + \frac{1}{\beta + 1} \boldsymbol{\Gamma}_{\mathrm{dn}}$$

With known DOA, $M(M-1)/2$ equations follow from the off-diagonal entries; without DOA, the pairwise Schwarz estimator solves $|[\boldsymbol{\Gamma}_{\mathrm{cs}}]_{1,2}| = 1$. The objective is to leverage the redundant and complementary information of more than two microphones for improved CDR estimation — naively averaging coherence across microphone pairs with inconsistent spacing and orientation can degrade rather than improve performance.

## Methodology

### Weighted-Average CDR Estimation (Proposed 1)

The linear array is partitioned into $N$ groups of two-sensor subarrays, such that subarrays within a group share the same sensor spacing and orientation (so the diffuse-noise coherence $\gamma_{\mathrm{dn}}^{(n)}$ is identical across the group). Estimation proceeds in three steps:

1. **Average within group** — the normalized correlation coefficients of the $J_n$ subarrays in group $n$ are averaged: $\gamma_y^{(n)} = \frac{1}{J_n} \sum_{j=1}^{J_n} \gamma_{y,j}^{(n)}$
2. **Per-group CDR** — the two-channel DOA-free Schwarz estimator $g(\gamma_y^{(n)}, \gamma_{\mathrm{dn}}^{(n)})$ is applied per group
3. **Weighted fusion** — group CDRs are merged through weights

$$\hat{\beta}_{\mathrm{prop1}} = \sum_{n=1}^{N} w_n \, g\!\left[\gamma_y^{(n)}, \gamma_{\mathrm{dn}}^{(n)}\right], \qquad w_n = \frac{e^{\zeta_0 g[\gamma_y^{(n)}, \gamma_{\mathrm{dn}}^{(n)}]}}{\sum_{i=1}^{N} e^{\zeta_0 g[\gamma_y^{(i)}, \gamma_{\mathrm{dn}}^{(i)}]}}$$

with $\zeta_0 = 0.1$ — a softmax weighting that emphasizes groups yielding larger (more reverberation-dominated) CDR estimates. Any existing two-channel CDR estimator can be plugged in, and the decomposition adapts to any array geometry.

![[raw/papers/xiang-2024-multichannel-cdr-estimation/figures/8abe29349a3421464dce9755b34d1822f822d590f8adfbed3b481af333157f20.jpg|Decomposition of a linear array with M sensors into subarrays]]
*Figure 1: Decomposition of a linear array with $M$ sensors, where $(i,j)$ denotes the subarray comprising the $i$th and $j$th sensors.*

### Array Manifold Information-Based CDR Estimation (Proposed 2)

Given an estimate $\widehat{\mathbf{d}}$ of the array manifold vector with $\|\widehat{\mathbf{d}}\|_2^2 = M$, one has $\widehat{\boldsymbol{\Gamma}}_{\mathrm{cs}} = \widehat{\mathbf{d}} \widehat{\mathbf{d}}^{\mathrm{H}}$, and pre/post-multiplying the normalized covariance model by $\widehat{\mathbf{d}}$ yields a scalar equation solved in closed form:

$$\hat{\beta}_{\mathrm{prop2}} = \frac{\widehat{\mathbf{d}}^{\mathrm{H}} \boldsymbol{\Gamma}_{\mathbf{y}} \widehat{\mathbf{d}} - \widehat{\mathbf{d}}^{\mathrm{H}} \boldsymbol{\Gamma}_{\mathrm{dn}} \widehat{\mathbf{d}}}{M^2 - \widehat{\mathbf{d}}^{\mathrm{H}} \boldsymbol{\Gamma}_{\mathbf{y}} \widehat{\mathbf{d}}}$$

The manifold vector is estimated by **joint diagonalization** of the two Hermitian matrices $\boldsymbol{\Gamma}_{\mathrm{dn}} = \mathbf{U}\mathbf{U}^{\mathrm{H}}$ and $\boldsymbol{\Gamma}_{\mathbf{y}} = \mathbf{U} \boldsymbol{\Lambda} \mathbf{U}^{\mathrm{H}}$: the columns of $\mathbf{U}$ are the eigenvectors of $\boldsymbol{\Gamma}_{\mathrm{dn}}^{-1} \boldsymbol{\Gamma}_{\mathbf{y}}$, and

$$\widehat{\mathbf{d}} = \frac{\sqrt{M}}{\|\mathbf{u}_1\|_2} \mathbf{u}_1$$

takes the principal eigenvector (largest eigenvalue). The resulting estimator is DOA-free and relies only on the diffuse noise field assumption — no subarray decomposition is needed.

### Postfilter Integration

CDR estimates drive the parametric Wiener-type postfilter (following Schwarz & Kellermann) applied after a delay-and-sum beamformer:

$$G(\omega, t) = \max\left\{G_{\min}, 1 - \sqrt{\frac{\mu}{\hat{\beta} + 1}}\right\}$$

with $\mu = 0.8$ and $G_{\min} = 0.1$.

## Experimental Setup

| Item | Value |
|------|-------|
| Source signals | 100 utterances from TIMIT, 16 kHz |
| Array | Uniform linear, 4 microphones (2–16 in scaling study), 2 cm spacing |
| Room | $6 \times 4 \times 3$ m; sensors from (3.03, 1, 1) to (2.97, 1, 1); source at 1.5 m, $30^{\circ}$ |
| RIRs | [[concepts/image-source-method\|Image-source method]]; real 4-channel RIRs from the MARDY database |
| Noise | Diffuse noise (Habets–Gannot generator) + white noise, diffuse-to-white power ratio 20 dB |
| Postfilter | $G = \max\{G_{\min}, 1 - \sqrt{\mu/(\hat{\beta}+1)}\}$, $\mu = 0.8$, $G_{\min} = 0.1$ |
| Baselines | Delay-and-sum, Schwarz (2 mics), averaged coherence, GMSC, ERANK (4 mics) |
| Metrics | Full-band SNR gain, LSD, DRR (averaged over 100 signals); CDR estimation mse and error kurtosis |
| Runtime test | 17-s signal, input SNR 5 dB, Apple M1 CPU at 3.2 GHz |

## Results

### Impact of the number of microphones (Table I; $T_{60} = 500$ ms, input SNR 5 dB)

| Method | Mics | SNR Gain | LSD | DRR |
|--------|------|----------|-----|-----|
| Weighted averaging | 2 | 7.58 | 7.90 | 6.33 |
| Weighted averaging | 4 | 11.30 | 6.72 | 7.04 |
| Weighted averaging | 8 | 13.79 | 6.25 | 8.61 |
| Weighted averaging | 16 | 15.09 | 6.40 | 14.41 |
| Diagonalization | 2 | 7.74 | 7.60 | 6.71 |
| Diagonalization | 4 | 11.69 | 7.11 | 7.08 |
| Diagonalization | 8 | 14.21 | 6.78 | 8.59 |
| Diagonalization | 16 | 14.72 | 6.67 | 14.37 |

SNR gain, DRR, and LSD all improve with more microphones; DRR jumps markedly from $M = 8$ to 16.

### CDR estimation accuracy (Fig. 2; input SNR 20 dB, $T_{60} = 500$ ms)

![[raw/papers/xiang-2024-multichannel-cdr-estimation/figures/cfcc7f7712c2132cf36ea8d9baac40d513a88d8944bc204d5123f44cd2f9044e.jpg|Absolute value of CDR estimation errors, first condition]]
![[raw/papers/xiang-2024-multichannel-cdr-estimation/figures/d6a66d81f4a4994d0d913ed093d37ec71493a4455106f4c0103729b537ecc970.jpg|Absolute value of CDR estimation errors, second condition]]
*Figure 2: Absolute value of errors between the ground truth and the CDR estimates (input SNR 20 dB, diffuse noise, $T_{60} = 500$ ms); estimation kurtosis and mse in parentheses. The proposed approaches show much smaller mse and higher kurtosis — errors concentrated near zero.*

### Performance vs. input SNR (Fig. 3; $T_{60} = 500$ ms)

![[raw/papers/xiang-2024-multichannel-cdr-estimation/figures/f2aeee6dc2d624b12b0c174efa1c47b70ac661c63ea8ad807f07adcd2ed22709.jpg|SNR gain, LSD, and DRR vs input SNR, first panel]]
![[raw/papers/xiang-2024-multichannel-cdr-estimation/figures/8ef30f8c372c9d565cf69dde89f484bd99cb2afdec97ccf02a36d22e6cd34cd7.jpg|SNR gain, LSD, and DRR vs input SNR, second panel]]
*Figure 3: SNR gains (larger is better), LSDs (smaller is better), and DRRs (larger is better) vs. input SNR (−10 to 30 dB).*

The proposed estimators outperform all compared methods in SNR gain; all multichannel estimators surpass the two-channel Schwarz method; SNR gain and LSD decrease as input SNR increases (less demanding enhancement); DRR varies minimally with input SNR — the CDR estimate, and hence the reverberation suppression, is barely influenced by the background noise level.

### Performance vs. reverberation time (Fig. 4; input SNR 5 dB, $T_{60}$ from 0.14 to 1.03 s)

![[raw/papers/xiang-2024-multichannel-cdr-estimation/figures/196a31e67eaba271081734a70f5f469b1f8fe4ba583e7eb66cb33c47c53d0408.jpg|SNR gain, LSD, and DRR vs reverberation, first panel]]
![[raw/papers/xiang-2024-multichannel-cdr-estimation/figures/8e22ed4b2c8c3cf3ceaa6b1a381d362955ac2d5245b922b05cecf63b783f97e1.jpg|SNR gain, LSD, and DRR vs reverberation, second panel]]
![[raw/papers/xiang-2024-multichannel-cdr-estimation/figures/027b7b69643bdbc1d291eb2c26a639c0e4150cf04ac383a5e094bc3f752d8f71.jpg|SNR gain, LSD, and DRR vs reverberation, third panel]]
*Figure 4: SNR gains, LSDs, and DRRs vs. reverberation condition. DRR of all methods decreases sharply with $T_{60}$; the first proposed approach is slightly inferior in DRR to the others.*

### Computational complexity (Table II; 17-s signal, Apple M1 at 3.2 GHz)

| Method | DS | Schwarz | Avg. coherence | GMSC | ERANK | Proposed 1 | Proposed 2 |
|--------|----|---------|----------------|------|-------|------------|------------|
| Runtime /s | 9.36 | 6.21 | 9.50 | 27.54 | 47.51 | 11.37 | 25.54 |

The two-channel Schwarz method is cheapest; Proposed 1 costs slightly more than averaged coherence but performs better; Proposed 2 is comparable to GMSC (similar eigenvalue decompositions); ERANK is the most expensive due to curve fitting for the inverse function coefficients.

### Performance vs. number of microphones (Fig. 5; input SNR 5 dB, $T_{60} = 500$ ms)

![[raw/papers/xiang-2024-multichannel-cdr-estimation/figures/32d9f16fbe420f3db24506ac7ce468d8ac28aa5a7211dc44c60b9c0697e2b98b.jpg|SNR gain, LSD, and DRR vs number of microphones, first panel]]
![[raw/papers/xiang-2024-multichannel-cdr-estimation/figures/81843f40ee70f47446ff6c9bbbfd6e5ae03cd2790071240429ca958c8759dce8.jpg|SNR gain, LSD, and DRR vs number of microphones, second panel]]
![[raw/papers/xiang-2024-multichannel-cdr-estimation/figures/8b69402334c0c7ac1d28a79104dbec3ad04e61b581c604ca1377419213e3837b.jpg|SNR gain, LSD, and DRR vs number of microphones, third panel]]
*Figure 5: SNR gains, LSDs, and DRRs vs. the number of microphones — the advantage of the proposed methods over the baselines grows with $M$.*

### Real-life scenarios: MARDY database (Table III; 4-channel measured RIRs, $T_{60} = 447$ ms, input SNR 20 dB)

| Method | SNR Gain | LSD | DRR |
|--------|----------|-----|-----|
| DS | 4.25 | 5.59 | 15.01 |
| Schwarz et al. | 6.22 | 4.40 | 15.32 |
| Averaged coherence | 8.65 | 4.22 | 15.82 |
| GMSC | 8.94 | 4.00 | 16.60 |
| ERANK | 8.39 | 4.01 | 16.39 |
| **Proposed 1** | **9.23** | 4.04 | 16.23 |
| **Proposed 2** | **9.37** | 4.30 | **16.71** |

The proposed methods achieve the best SNR gain and DRR on measured RIRs, consistent with the simulation results.

## Key Contributions

1. **Weighted-average multichannel CDR estimation**: decomposes the array into groups of consistent two-sensor subarrays, fusing per-group pairwise CDR estimates with softmax-style weights ($\zeta_0 = 0.1$) — a general recipe that extends *any* two-channel CDR estimator to arbitrary array geometries.
2. **Array manifold information-based CDR estimator**: a DOA-free closed-form estimator that replaces subarray decomposition with joint diagonalization (GEVD of $\boldsymbol{\Gamma}_{\mathrm{dn}}^{-1} \boldsymbol{\Gamma}_{\mathbf{y}}$), taking the principal eigenvector as the scaled manifold vector.
3. **Comprehensive multichannel comparison**: benchmarks against delay-and-sum, two-channel Schwarz, averaged coherence, GMSC, and ERANK in CDR accuracy (mse and error kurtosis), SNR gain, LSD, and DRR — showing the advantage grows with the number of microphones, and validating on the real MARDY RIR database.
4. **Complexity characterization**: Proposed 1 costs slightly above averaged coherence; Proposed 2 is comparable to GMSC; both are far cheaper than ERANK.

## Related Concepts

- [[concepts/multichannel-cdr-estimation|Multichannel CDR Estimation]] — the paper's central contribution
- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio]] — the estimated quantity
- [[concepts/spatial-coherence|Spatial Coherence]] — the pairwise coherence foundation
- [[concepts/generalized-magnitude-coherence|Generalized Magnitude Coherence]] — the GMSC baseline
- [[concepts/generalized-eigenvalue-decomposition|Generalized Eigenvalue Decomposition]] — the joint diagonalization underlying Proposed 2
- [[concepts/dereverberation|Dereverberation]] — the postfilter application
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/beamforming|Beamforming]] — the delay-and-sum spatial filter preceding the postfilter
- [[concepts/image-source-method|Image-Source Method]] — RIR simulation
- [[concepts/snr-cdr-wiener-gain|SNR–CDR Wiener Gain]] — the same group's successor postfilter consuming noise-aware CDR estimates

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — multichannel CDR estimation as the postfilter side of spatial-filter-plus-postfilter designs
