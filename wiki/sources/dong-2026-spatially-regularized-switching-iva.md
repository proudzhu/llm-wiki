---
type: source
created: 2026-06-04
updated: 2026-10-04
sources:
  - raw/papers/dong-2026-spatially-regularized-switching-iva/full-text.md
  - zotero://select/items/0_GMZWLILS
tags:
  - blind-source-separation
  - independent-vector-analysis
  - switching-iva
  - iterative-source-steering
  - spatial-regularization
  - speech-separation
---

# Dong, Liu, Xie & Makino 2026: Spatially-Regularized Switching IVA with ISS

**Authors**: [[entities/haonan-dong|Haonan Dong]], [[entities/wei-liu|Wei Liu]], [[entities/xuemai-xie|Xuemai Xie]] & [[entities/shoji-makino|Shoji Makino]]
**Institutions**: Waseda University, Japan; Wuhan University, China
**Type**: Journal Article
**Venue**: Journal of Signal Processing, vol. 30, no. 4, 2026 (published 2026-07-01)
**DOI**: [10.2299/jsp.30.123](https://doi.org/10.2299/jsp.30.123)
**Year**: 2026
**Zotero**: [GMZWLILS](zotero://select/items/0_GMZWLILS)

## Summary

This paper proposes SR-SwIVA-ISS, a computationally efficient variant of Spatially Regularized Switching Independent Vector Analysis that replaces the matrix-inversion-based Iterative Projection (IP) update with an Iterative Source Steering (ISS) rank-one update. The method maintains separation performance while reducing per-iteration computational cost from ~14 ms to ~2 ms, making it suitable for practical scenarios with limited microphone arrays.

## Problem Formulation

### Signal Model

In the STFT domain, the observed multichannel signal is modeled as:

$$\mathbf{x}(f, t) = \mathbf{A}(f)\mathbf{s}(f, t)$$

where $\mathbf{x}(f, t) \in \mathbb{C}^M$ is the observed signal, $\mathbf{s}(f, t) \in \mathbb{C}^N$ is the source signal vector, and $\mathbf{A}(f) \in \mathbb{C}^{M \times N}$ is the unknown mixing matrix.

### Switching Demixing Model

To handle time-varying acoustic conditions, multiple demixing matrices $\mathbf{W}_j(f)$ are maintained for switching states $j = 1, \ldots, J$. The separated signals under state $j$ are:

$$\hat{\mathbf{s}}_j(f, t) = \mathbf{W}_j^{\mathsf{H}}(f)\mathbf{x}(f, t)$$

A binary switching variable $\delta_j(f, t) \in \{0, 1\}$ selects the most appropriate demixing matrix at each time-frequency bin.

## Methodology

### SR-SwIVA Cost Function

The Spatially Regularized Switching IVA cost function is:

$$\mathcal{L}(\Theta) = \sum_{j, f, t} \delta_j(f, t) \left[ \sum_n \left(\log v_n(f, t) + \frac{|\hat{\mathbf{s}}_{j, n}(f, t)|^2}{v_n(f, t)}\right) - 2\log|\det\mathbf{W}_j(f)| \right] + \sum_{f, j, n} \lambda_{\text{reg}} \|\mathbf{w}_{j, n}(f) - \mathbf{a}_n(f)\|_2^2$$

where $\lambda_{\text{reg}}$ controls spatial regularization strength toward steering vectors $\mathbf{a}_n(f)$ estimated from DOA information.

### ISS Rank-One Update

Instead of matrix inversion, ISS performs rank-one updates:

$$\mathbf{W}_f \leftarrow \mathbf{W}_f - \mathbf{v}_{n, f}\mathbf{w}_{n, f}^{\mathsf{H}}$$

The update vector $\mathbf{v}_{j, n}(f)$ is optimized by minimizing a sub-objective. For off-diagonal elements ($i \neq n$), closed-form solutions are obtained. For the diagonal element $v_{j, nn}(f)$, the solution depends on whether $\beta_{j, n}(f) = 0$:

$$v_{j, n}(f) = \begin{cases} 1 - \alpha_{j, n}(f)^{-1/2}, & \beta_{j, n}(f) = 0 \\ \gamma_{j, n}(f), & \beta_{j, n}(f) \neq 0 \end{cases}$$

where:

$$\alpha_{j, n}(f) = \sum_t \delta_j(f, t) \frac{|\hat{s}_{j, n}(f, t)|^2}{v_n(f, t)} + 2\lambda_{\text{reg}}\|\mathbf{w}_{j, n}(f)\|^2$$

$$\beta_{j, n}(f) = \lambda_{\text{reg}}\mathbf{w}_{j, n}^{\mathsf{H}}(f)(\mathbf{w}_{j, n}(f) - \mathbf{a}_n(f))$$

### Demixing Matrix Update

Once $v_{j, n}(f)$ is obtained, the demixing matrix rows are updated:

$$\mathbf{w}_{j, i}^{\mathsf{H}}(f) \leftarrow \mathbf{w}_{j, i}^{\mathsf{H}}(f) - v_{j, n}(f)\mathbf{w}_{j, n}^{\mathsf{H}}(f)$$

and the separated signals are updated:

$$\mathbf{y}(f, t) \leftarrow \mathbf{y}(f, t) - \mathbf{v}_j(f)y_j(f, t)$$

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Dataset | TIMIT-ConvMix (simulated noisy reverberant mixtures) |
| Reverberation time | 300 ms |
| Microphone array | 3-element ULA, 3 cm spacing |
| Sources | 3 speech + 5 noise sources |
| SNR | 10 dB |
| STFT window | 64 ms Hann, 32 ms shift |
| Sampling rate | 16 kHz |
| Metrics | SDRi, SIRi, computational time per iteration |

![[raw/papers/dong-2026-spatially-regularized-switching-iva/figures/65ada77175146477e2bcebc9ae34ccd2814d8c1aa6f7591b5683e7eabfa73772.jpg|Figure 1: Spatial configuration of the microphone array and sound sources]]

*Figure 1: Spatial configuration of the microphone array (3-element ULA, $M_1$–$M_3$) and the three speech sources; DOAs were drawn from $\{10°, 30°, 50°, \ldots, 170°\}$ with a minimum angular separation of $40°$.*

### Initialization Strategies

1. **Simple-init**: Identity matrix initialization
2. **SPG-init**: Spatially-guided initialization using MPDR beamformer
3. **SRSS-init**: Spatially-Regularized Single-State initialization using DOA-based spatial regularization

## Results

### Separation Performance

| Initialization | Method | SDRi [dB] | SIRi [dB] |
|----------------|--------|-----------|-----------|
| Simple-init | SR-SwIVA | 7.28 | 18.70 |
| Simple-init | SR-SwIVA-ISS | 7.05 | 18.39 |
| SPG-init | SR-SwIVA | 7.14 | 18.47 |
| SPG-init | SR-SwIVA-ISS | 7.36 | 19.04 |
| SRSS-init | SR-SwIVA | 8.45 | 22.16 |
| SRSS-init | SR-SwIVA-ISS | 8.45 | 22.34 |

### Computational Efficiency

Average computational time per iteration for updating demixing matrix $\mathbf{W}_f$:

| Initialization | SR-SwIVA | SR-SwIVA-ISS | Speedup |
|----------------|----------|--------------|---------|
| Simple-init | 14.0 ms | 2.0 ms | 7.0× |
| SPG-init | 14.0 ms | 2.0 ms | 7.0× |
| SRSS-init | 11.0 ms | 2.0 ms | 5.5× |

![[raw/papers/dong-2026-spatially-regularized-switching-iva/figures/f254c17424dd23eee7738b90342a0819d8b1c7ea5317003a744b70c7dabdbd75.jpg|Figure 2: Average run time under different initialization setups]]

*Figure 2: Average run time per iteration under different initialization setups — SR-SwIVA-ISS consistently requires less computation time than SR-SwIVA for all initialization conditions.*

### Key Findings

1. SR-SwIVA-ISS achieves comparable or slightly better separation performance than SR-SwIVA across all initialization strategies
2. Computational cost is reduced by 5.5–7× per iteration
3. SRSS-init provides the best separation performance for both methods
4. The ISS update maintains numerical stability without matrix inversion

## Key Contributions

1. Integration of Iterative Source Steering (ISS) into Spatially Regularized Switching IVA framework
2. Derivation of closed-form ISS update rules with spatial regularization terms
3. Demonstration of 5.5–7× computational speedup while maintaining separation quality
4. Experimental validation on noisy reverberant scenarios with limited microphone arrays

## Related Concepts

- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/switching-independent-vector-analysis|Switching Independent Vector Analysis]]
- [[concepts/iterative-source-steering|Iterative Source Steering]]
- [[concepts/spatial-regularization|Spatial Regularization]]

## Related Sources

- [[sources/nakatani-2022-switching-iva|Nakatani et al. 2022: Switching IVA and Its Extension to Blind and Spatially Guided Convolutional Beamforming]] — the swIVA framework and initialization strategies this paper builds on (ref. [6])
- [[sources/goto-2022-offline-iss-gciva|Goto et al. 2022: GC-IVA with Auxiliary Function Approach and Iterative Source Steering]] — prior work folding geometric constraints into closed-form ISS coefficients (ref. [11])
- [[sources/li-2020-geometrically-constrained-iva|Li & Koishida 2020: Geometrically Constrained IVA for Directional Speech Enhancement]] — spatial-regularization origins in IVA (ref. [10])
- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]]

## Related Synthesis

- None.
