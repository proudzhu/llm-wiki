---
type: source
created: 2026-05-21
updated: 2026-05-21
sources:
  - raw/papers/guo-2023-iva-survey/full-text.md
  - https://doi.org/10.3390/s23010493
  - zotero://select/items/0_DA3F64K6
tags:
  - blind-source-separation
  - independent-vector-analysis
  - optimization-algorithms
  - audio-source-separation
---

# Guo, Luo & Li 2023: A Survey of Optimization Methods for Independent Vector Analysis in Audio Source Separation

**Authors**: [[entities/ruiming-guo|Ruiming Guo]], [[entities/zhongqiang-luo|Zhongqiang Luo]] & [[entities/mingchun-li|Mingchun Li]]
**Institution**: Sichuan University of Science and Engineering
**Venue**: Sensors, Vol. 23, Issue 1, Article 493
**Year**: 2023
**Type**: Survey / Journal Article
**DOI**: [10.3390/s23010493](https://doi.org/10.3390/s23010493)
**Zotero**: [DA3F64K6](zotero://select/items/0_DA3F64K6)

## Summary

This paper provides a comprehensive survey of optimization update rules used in [[concepts/independent-vector-analysis|Independent Vector Analysis]] (IVA) for frequency-domain [[concepts/blind-source-separation|blind source separation]] of convolutive audio mixtures. It categorizes six main optimization families — gradient descent, fast fixed-point (Newton), auxiliary function (AuxIVA), expectation-maximization (EM), block coordinate descent (BCD including IP/ISS), and eigenvalue decomposition (EVD) — and provides experimental comparisons under determined and overdetermined scenarios at varying SNR levels.

## Problem Formulation

A reverberant multichannel audio mixture is modeled in the STFT domain as:

$$\mathbf{x}^{(k)}[z] = \mathbf{A}^{(k)}\mathbf{s}^{(k)}[z]$$

where $\mathbf{A}^{(k)}$ is the mixing matrix at frequency bin $k$. The goal is to estimate unmixing matrices $\mathbf{W}^{(k)}$ such that:

$$\mathbf{y}^{(k)}[z] = \mathbf{W}^{(k)}\mathbf{x}^{(k)}[z]$$

recovers independent source signals. IVA minimizes the Kullback–Leibler divergence between the joint distribution and the product of marginal source distributions:

$$\mathcal{I}_{\mathrm{IVA}} = \sum_n E_{\mathbf{y}_n} \log g(\mathbf{y}_n) - 2\sum_k \log|\det \mathbf{W}^{(k)}| - \text{const.}$$

where $\mathbf{y}_n = [y_n^{(1)}, \ldots, y_n^{(K)}]^T$ is the source vector across all frequency bins. This multivariate formulation couples frequency bins for each source, inherently resolving the permutation ambiguity of per-bin ICA.

## Methodology

### Optimization Update Rules

The survey organizes IVA optimization into six families:

| Method | Principle | Step-size | Key Property |
|--------|-----------|:---------:|--------------|
| Natural Gradient (NG) | Riemannian gradient descent | ✓ | Simple but slow; step-size sensitive |
| FastIVA | Newton's fixed-point iteration | ✗ | Fast convergence; decorrelation via symmetric orthogonalization |
| AuxIVA | Majorize-minimize auxiliary function | ✗ | Monotonic convergence; stable; widely used |
| EM | Expectation-maximization | ✗ | Handles complex parameter estimation and noise |
| BCD (IP/ISS) | Block coordinate descent | ✗ | Closed-form row/column updates; low complexity variants |
| EVD | Eigenvalue decomposition | ✗ | Very fast for single-source extraction |

### Natural Gradient

The NG update multiplies a scaling matrix to the standard gradient:

$$\Delta \mathbf{W}^{(k)} = -\frac{\partial \mathcal{I}}{\partial \mathbf{W}^{(k)}} \mathbf{Q}^{(k)}, \quad \mathbf{W}^{(k)} \leftarrow \mathbf{W}^{(k)} + \eta \Delta \mathbf{W}^{(k)}$$

Convergence depends on step-size $\eta$. Various adaptive step-size schemes have been proposed (Liang et al. 2011, Fu et al. 2018).

### FastIVA (Fast Fixed Point)

Based on Newton's method applied to the IVA objective:

$$\mathbf{w}_n^{(k)} \leftarrow E\left[G'(\cdot) + |y_n^{(k)}|^2 G''(\cdot)\right]\mathbf{w}_n^{(k)} - E\left[(y_n^{(k)})^* G'(\cdot)\mathbf{x}^{(k)}\right]$$

followed by symmetric orthogonalization: $\mathbf{W}^{(k)} \leftarrow (\mathbf{W}^{(k)}(\mathbf{W}^{(k)})^H)^{-1/2}\mathbf{W}^{(k)}$. Extensions include FastDIVA for time-varying mixtures (Koldovský et al. 2021).

### Auxiliary Function (AuxIVA)

Introduced by Ono (2011), this derives from the majorize-minimize principle. Two alternating updates guarantee monotonic cost decrease:

1. Auxiliary variable (weighted covariance):
$$\mathbf{V}_n = E_n\left[\frac{U'(\|\mathbf{y}_n\|_2)}{\|\mathbf{y}_n\|_2}\mathbf{x}_n\mathbf{x}_n^H\right]$$

2. Separation vector:
$$\mathbf{w}_n^{(k)} = \frac{[\mathbf{W}\mathbf{V}_n]^{-1}\mathbf{e}_n}{\sqrt{\mathbf{e}_n^T(\mathbf{W}_n^{-H}\mathbf{V}_n^{-1}\mathbf{W}_n^{-1})\mathbf{e}_n}}$$

AuxIVA requires no step-size tuning and guarantees convergence.

### Block Coordinate Descent: IP, ISS, IPA

- **Iterative Projection (IP)**: Updates one row of $\mathbf{W}$ per iteration; requires matrix inversion at $O(M^3)$ per source per iteration.
- **Iterative Source Steering (ISS)**: Rank-1 updates to $\mathbf{W}$ at $O(M^2)$ complexity without matrix inversion:
$$\mathbf{W}^{(k)} \leftarrow \mathbf{W}^{(k)} - \mathbf{v}_n^{(k)}(\mathbf{w}_n^{(k)})^H$$
- **IP-2 / ISS-2**: Update two rows simultaneously for faster convergence.
- **IPA (IP with Adjustment)**: Combines IP and ISS jointly; updates one row and one column per iteration.

### EVD Method

For single-source extraction (FIVE algorithm), the unmixing vector is the eigenvector corresponding to the smallest eigenvalue:

$$\mathbf{w}^{(k)} = \frac{1}{\sqrt{\lambda_M^{(k)}}}\mathbf{u}_M^{(k)}$$

Achieves optimal solution in very few iterations.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Simulation | pyroomacoustics, 1000 random 3D rooms |
| Room dimensions | 6–10 m walls, 2.8–4.5 m ceiling |
| Reverberation | T60: 60–450 ms |
| Array | Circular, 3–10 mics, 10 cm radius |
| Source distance | Beyond critical distance |
| SNR levels | 5, 15, 25 dB |
| Sample rate | 16 kHz |
| STFT | 4096 Hamming window, 3/4 overlap |
| Speech corpus | CMU Arctic |
| Source prior | Multivariate Laplacian |
| Scenarios | Determined (3×3) and overdetermined (4×3) |

## Results

### Running Time Comparison (3 sources, 5 dB)

| Algorithm | IP | IP2 | ISS | ISS2 | OverIVA | FIVE | IPA | IPANCG | NG | FastIVA |
|-----------|---:|----:|----:|-----:|--------:|-----:|----:|-------:|---:|--------:|
| Time (s) | 14.46 | 14.35 | 13.29 | 13.36 | 13.91 | 7.88 | 14.48 | 13.72 | 14.66 | 13.71 |

### Key Findings

- **3×3 determined**: AuxIVA-IPA provides the most stable performance across all SNR levels. AuxIVA-IP2 and FullHEAD also perform well. FastIVA excels at 25 dB.
- **4×3 overdetermined**: AuxIVA-IPANCG is best at 5 dB; OverIVA-IP2 is optimal at 15 and 25 dB.
- **NG** cannot converge within the allocated iterations in any scenario — it requires far more iterations and is the slowest to converge.
- **ISS/ISS2** have the lowest time complexity among full-separation methods.
- **FIVE (EVD)** has minimal complexity but only extracts a single source.
- **IPA** jointly executes IP + ISS updates and re-estimates all filters, producing the best overall separation at 5 dB in the determined case.

## Key Contributions

1. Comprehensive taxonomy of six IVA optimization families with unified notation and derivation.
2. Detailed discussion of recent BCD extensions: IP-2, ISS-2, IPA, IPANCG, and FullHEAD.
3. Experimental comparison of 10+ algorithms under controlled reverberant multi-source conditions.
4. Practical guidance: AuxIVA-IPA for determined mixtures at low SNR; OverIVA-IP2 for overdetermined scenarios.
5. Discussion of source prior models (Laplacian, GMM, Student-t, deep-learning-based) and their interplay with optimization.

## Related Concepts

- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/fastmnmf|FastMNMF]] — related BSS method using NMF-based source models
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]

## Related Sources

- [[sources/nishikori-2026-fast-multichannel-nmf-block-diagonal-scm-bss|Nishikori et al. 2026: Distributed FastMNMF for BSS]]

## Related Synthesis

- None.
