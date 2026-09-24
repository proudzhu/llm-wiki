---
type: concept
created: 2026-09-14
updated: 2026-09-24
sources:
  - raw/papers/pan-2020-microphone-array-beamforming/full-text.txt
  - raw/papers/zhu-2025-kronecker-superdirective-beamforming/full-text.txt
  - raw/papers/xiang-2025-wiener-gain-reverberant/full-text.md
  - raw/papers/cohen-2019-differential-kronecker-beamforming/full-text.txt
  - raw/papers/desena-2012-higher-order-differential/full-text.md
tags:
  - beamforming
  - microphone-arrays
  - robustness
  - fixed-beamformer
---

# Superdirective Beamforming

**Category**: Fixed Beamforming / Array Signal Processing

## Definition

Superdirective (SD) beamforming designs a fixed beamformer that **maximizes the directivity factor (DF)** under a distortionless constraint in the look direction — providing high spatial selectivity that effectively suppresses spatially isotropic (diffuse) noise in speech communication and far-field pickup. For a filter $\mathbf{h}(\omega)$ applied to an $M$-microphone array with steering vector $\mathbf{d}_{\theta_s}(\omega)$:

$$\mathcal{D}[\mathbf{h}] = \frac{|\mathbf{h}^H \mathbf{d}_{\theta_s}|^2}{\mathbf{h}^H \boldsymbol{\Gamma} \mathbf{h}}, \qquad \mathbf{h}^H \mathbf{d}_{\theta_s} = 1$$

where $\boldsymbol{\Gamma}(\omega)$ is the normalized isotropic noise covariance matrix, $[\boldsymbol{\Gamma}]_{ij} = \sin(\omega\delta_{ij}/c)/(\omega\delta_{ij}/c)$.

## Optimal Solution

The superdirective beamformer is the MVDR-type solution against the diffuse noise field:

$$\mathbf{h}_{\mathrm{SD}} = \frac{\boldsymbol{\Gamma}^{-1}\mathbf{d}_{\theta_s}}{\mathbf{d}_{\theta_s}^H \boldsymbol{\Gamma}^{-1}\mathbf{d}_{\theta_s}}$$

with directivity factor $\mathcal{D} = \mathbf{d}_{\theta_s}^H \boldsymbol{\Gamma}^{-1}\mathbf{d}_{\theta_s}$, which approaches $M^2$ as the inter-element spacing $\delta$ becomes small (Lotter & Vary 2006).

## The Robustness Problem

Superdirective beamformers are **highly sensitive to array imperfections** — sensor gain/phase mismatch and self-noise — because maximizing DF drives the [[concepts/white-noise-gain|white noise gain (WNG)]] strongly negative, especially at low frequencies where the array is acoustically small. This limits practical application.

### Robust Superdirective (RSD) via Diagonal Loading

The most widely used remedy applies [[concepts/diagonal-loading|diagonal loading]] to $\boldsymbol{\Gamma}$:

$$\mathbf{h}_{\mathrm{RSD}} = \frac{[\boldsymbol{\Gamma} + \epsilon \mathbf{I}_M]^{-1}\mathbf{d}_{\theta_s}}{\mathbf{d}_{\theta_s}^H [\boldsymbol{\Gamma} + \epsilon \mathbf{I}_M]^{-1}\mathbf{d}_{\theta_s}}$$

The loading factor $\epsilon \geq 0$ trades DF against WNG: larger $\epsilon$ raises WNG (more robust) but lowers DF. $\epsilon$ can be fixed per design, or found per frequency bin by bisection to meet a target WNG.

Other robust design families include subspace-based designs, Krylov-subspace formulations, quadratic-eigenvalue approaches, and combined beamforming + post-filtering (see Zhu et al. 2025 for a survey in the introduction).

The RSD beamformer also serves as the fixed spatial front-end of post-filter pipelines: [[sources/xiang-2025-wiener-gain-reverberant|Xiang et al. 2025]] adopt exactly this $\epsilon = 10^{-3}$ loaded design (against the diffuse-field sinc coherence model of reverberation) on a 4-mic, 2 cm ULA, and follow it with a [[concepts/snr-cdr-wiener-gain|joint SNR–CDR Wiener gain]] for simultaneous noise and reverberation suppression — the beamformer contributes the interferer-leakage weights $\alpha_R, \alpha_V$ that scale each ratio in the gain. Notably, the SD beamformer's SNR gain is nearly constant across input SNRs because it depends on the noise *coherence matrix*, not the covariance.

## Alternative Interpretations and Lineage (Pan, Huang & Chen 2020)

[[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020]] give the superdirective beamformer two additional readings: it is a **special case of differential beamforming** (both respond to the differential sound field — DMAs measure the differential field, superdirective arrays effectively do the same), and it is the **MVDR beamformer specialized to isotropic noise** (constrained-distortionless minimization of output power with $\boldsymbol{\Gamma}$ as the noise covariance). The review also documents the robustness/frequency-invariance tension explicitly: with $\epsilon = 10^{-3}$ diagonal loading on an $M=8$, 1 cm-spacing ULA, the loaded design's beampattern loses frequency consistency — WNG is purchased at the price of frequency invariance. A **two-stage cascade** design (beamformer = convolution of two subfilters; beampattern = product of sub-patterns; one stage maximizes DF, the other improves WNG) preserves frequency consistency while boosting WNG — this cascade is the direct ancestor of [[concepts/kronecker-product-beamforming|Kronecker product beamforming]].

[[sources/desena-2012-higher-order-differential|De Sena, Hacihabiboglu & Cvetkovic 2012]] place the two classical optimality targets in one family: their [[concepts/sector-directivity-design|(α, λ) directivity design framework]] has the max-DF hypercardioid at $(\lambda, \alpha) = (1, \alpha \to 0)$ and the max-FBR supercardioid at $(1, \pi/2)$ as corner solutions, with intermediate pairs trading directivity against in-sector uniformity — a design-space view of the same DF-vs-rejection tension that superdirective design navigates via the loading factor.

## Efficiency Problem at Scale

As $M$ grows, an RSD beamformer stores $M$ complex parameters per frequency bin ($(K/2{+}1)M$ for a $K$-point STFT) and requires $M \times M$ matrix inversions — parameter redundancy that limits embedded and large-array deployments. Low-rank approaches such as [[concepts/kronecker-product-beamforming|Kronecker product beamforming]] address this by decomposing the long filter into short filters. The line began with differential Kronecker product beamforming ([[sources/cohen-2019-differential-kronecker-beamforming|Cohen, Benesty & Chen 2019]]), whose alternating maximization of the (non-factorizable) directivity factor over two virtual-array subfilters is the precursor of later alternating-iteration Kronecker superdirective algorithms (Zhu et al. 2025).

## Relation to Other Fixed Beamformers

Superdirective designs belong to the [[concepts/fixed-beamformer|fixed beamformer]] family: coefficients are precomputed and stored, giving stable performance and low run-time cost. They generalize [[concepts/differential-microphone-array|differential microphone arrays]] (DMAs give frequency-invariant patterns with the same low-frequency WNG amplification issue) and relate to the WNG–DF trade-off faced by compact arrays (see the [[concepts/fixed-beamformer|fixed beamformer]] page).

## Related Concepts

- [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/diagonal-loading|Diagonal Loading]]
- [[concepts/fixed-beamformer|Fixed Beamformer]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/snr-cdr-wiener-gain|SNR–CDR Wiener Gain]] — post-filter that consumes the RSD's interferer-leakage weights
- [[concepts/frequency-invariant-beamforming|Frequency-Invariant Beamforming]] — the third axis of the DF–WNG–frequency-invariance trade-off triangle

## Related Sources

- [[sources/cohen-2019-differential-kronecker-beamforming|Cohen, Benesty & Chen 2019: Differential Kronecker Product Beamforming]] — alternating DF/FBR maximization over Kronecker subfilters
- [[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020: Microphone Array Beamforming Methods for Speech Communication and Interaction]] — superdirective as special case of both DMA and isotropic-noise MVDR; robustness-vs-frequency-invariance tension; two-stage cascade ancestor of Kronecker beamforming
- [[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025: Low-Rank Robust Superdirective Beamforming Using Multidimensional Kronecker Products]]
- [[sources/xiang-2025-wiener-gain-reverberant|Xiang, Chen, Benesty, Lei & Pan 2025: Design of the Wiener Gain in Noisy and Reverberant Environments]] — RSD ($\epsilon = 10^{-3}$) as the spatial front-end of a joint SNR–CDR Wiener post-filter
- [[sources/desena-2012-higher-order-differential|De Sena, Hacihabiboglu & Cvetkovic 2012: On the Design and Implementation of Higher Order Differential Microphones]] — (α, λ) framework with max-DF hypercardioid and max-FBR supercardioid as corner solutions
