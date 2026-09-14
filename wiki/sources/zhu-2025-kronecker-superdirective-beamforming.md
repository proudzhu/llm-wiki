---
type: source
created: 2026-09-14
updated: 2026-09-14
sources:
  - raw/papers/zhu-2025-kronecker-superdirective-beamforming/full-text.txt
  - https://doi.org/10.12466/xhcl.2025.09.003
  - zotero://select/items/0_3FFIXGTS
tags:
  - beamforming
  - microphone-arrays
  - superdirective-beamforming
  - kronecker-product
  - low-rank
  - robustness
  - white-noise-gain
  - fixed-beamformer
---

# Zhu, Zhao, Luo, Jin, Huang & Chen 2025: Low-Rank Robust Superdirective Beamforming Using Multidimensional Kronecker Products

**Authors**: [[entities/yujie-zhu|Yujie Zhu]], [[entities/kunlong-zhao|Kunlong Zhao]], [[entities/xueqin-luo|Xueqin Luo]], [[entities/jilu-jin|Jilu Jin]], [[entities/gongping-huang|Gongping Huang]] (corresponding), [[entities/jingdong-chen|Jingdong Chen]]
**Affiliations**: School of Electronic Information, Wuhan University; Center of Intelligent Acoustics and Immersive Communications, Northwestern Polytechnical University; Shenzhen Research Institute, Wuhan University
**Venue**: Journal of Signal Processing (信号处理), Vol. 41, No. 9, pp. 1478–1493, Sep. 2025 (in Chinese)
**Type**: Journal article
**DOI**: [10.12466/xhcl.2025.09.003](https://doi.org/10.12466/xhcl.2025.09.003)
**Zotero**: [3FFIXGTS](zotero://select/items/0_3FFIXGTS)
**Funding**: NSFC 62471340; Guangdong Basic and Applied Basic Research Foundation 2025A1515010226

## Summary

This paper proposes the **low-rank robust superdirective (LR-RSD) beamformer**, which extends the existing two-dimensional [[concepts/kronecker-product-beamforming|Kronecker product beamforming]] framework to a *multidimensional* (N-way, rank-P) decomposition. The length-$M$ superdirective filter is written as a sum of $P$ Kronecker products of $N$ short filters (with $M = \prod_{n=1}^{N} L_n$), and the short filters are solved by an alternating-iteration algorithm that maximizes the directivity factor under a distortionless constraint, with diagonal loading applied inside every subproblem for robustness. For an $M = 64$ array with $K = 256$, rank $P = 2$ cuts the stored complex parameters by 62.5% and the largest matrix-inversion dimension by 87.5% versus the conventional robust superdirective (RSD) beamformer, while matching (or slightly exceeding) its SNR/SIR/STOI performance across uniform linear and concentric circular arrays — validated further by anechoic-chamber measurements.

## Problem Formulation

A planar array of $M$ microphones receives a far-field source from direction $\theta_s$:

$$\mathbf{y}(\omega) = \mathbf{d}_{\theta_s}(\omega) X(\omega) + \mathbf{v}(\omega)$$

with steering vector $[\mathbf{d}_\theta(\omega)]_m = e^{j\omega r_m \cos(\theta - \psi_m)/c}$. The beamformer output is $Z(\omega) = \mathbf{h}^H(\omega)\,\mathbf{y}(\omega)$ subject to the distortionless constraint $\mathbf{h}^H \mathbf{d}_{\theta_s} = 1$. Three performance metrics:

- **Beampattern**: $B[\mathbf{h}(\omega), \theta] = \mathbf{h}^H(\omega)\mathbf{d}_\theta(\omega)$
- **[[concepts/white-noise-gain|White noise gain]] (WNG)**: $\mathcal{W}[\mathbf{h}] = |\mathbf{h}^H \mathbf{d}_{\theta_s}|^2 / \mathbf{h}^H \mathbf{h}$ — robustness to spatially white sensor self-noise
- **Directivity factor (DF)**: $\mathcal{D}[\mathbf{h}] = |\mathbf{h}^H \mathbf{d}_{\theta_s}|^2 / \mathbf{h}^H \boldsymbol{\Gamma} \mathbf{h}$, where $\boldsymbol{\Gamma}$ is the $M \times M$ normalized isotropic (diffuse) noise covariance matrix with $[\boldsymbol{\Gamma}(\omega)]_{ij} = \sin(\omega \delta_{ij}/c) / (\omega \delta_{ij}/c)$

The superdirective (SD) beamformer $\mathbf{h}_{\mathrm{SD}} = \boldsymbol{\Gamma}^{-1}\mathbf{d}_{\theta_s} / (\mathbf{d}_{\theta_s}^H \boldsymbol{\Gamma}^{-1} \mathbf{d}_{\theta_s})$ maximizes DF (approaching $M^2$ for small inter-element spacing $\delta$) but suffers severe white-noise amplification, especially at low frequencies. The widely used robust superdirective (RSD) beamformer applies [[concepts/diagonal-loading|diagonal loading]]:

$$\mathbf{h}_{\mathrm{RSD}} = [\boldsymbol{\Gamma} + \epsilon \mathbf{I}_M]^{-1}\mathbf{d}_{\theta_s} / \left(\mathbf{d}_{\theta_s}^H [\boldsymbol{\Gamma} + \epsilon \mathbf{I}_M]^{-1} \mathbf{d}_{\theta_s}\right)$$

trading DF against WNG via $\epsilon \geq 0$. The remaining problem: as $M$ grows, the RSD beamformer stores $(K/2{+}1)M$ complex parameters in the STFT domain and inverts $M \times M$ matrices — parameter redundancy and computational cost that limit embedded/large-array deployments.

## Methodology

### Multidimensional Kronecker product decomposition

From a tensor-decomposition perspective, the length-$M$ filter is written as a **rank-$P$ sum of $N$-way Kronecker products of short filters**:

$$\mathbf{h}_{\mathrm{P}} = \sum_{p=1}^{P} \mathbf{h}_{N,p} \otimes \mathbf{h}_{N-1,p} \otimes \cdots \otimes \mathbf{h}_{1,p}, \qquad M = \prod_{n=1}^{N} L_n$$

where $\mathbf{h}_{n,p}$ has length $L_n$. Prior Kronecker beamforming work was mostly limited to $N = 2$ (e.g., rectangular/specific geometries); this paper allows arbitrary $N \geq 2$, arbitrary decomposition modes, and rank $P > 1$, applicable to arbitrary array geometries.

### Alternating-iteration solution

The design problem is $\min_{\mathbf{h}_{\mathrm{P}}} \mathbf{h}_{\mathrm{P}}^H \boldsymbol{\Gamma} \mathbf{h}_{\mathrm{P}}$ (i.e., DF maximization) subject to $\mathbf{h}_{\mathrm{P}}^H \mathbf{d}_{\theta_s} = 1$ with the Kronecker structure. Using the property $\bigotimes_{n=N}^{1} \mathbf{h}_{n,p} = \mathbf{H}_{n,p}\,\mathbf{h}_{n,p}$ (with $\mathbf{H}_{n,p}$ an $M \times L_n$ matrix built from the *other* short filters and identity blocks), each filter group is stacked as $\bar{\mathbf{h}}_n = [\mathbf{h}_{n,1}^T, \dots, \mathbf{h}_{n,P}^T]^T$ (length $P L_n$), giving

$$\mathbf{h}_{\mathrm{P}} = \sum_{p=1}^{P} \mathbf{H}_{n,p}\,\mathbf{h}_{n,p} = \bar{\mathbf{H}}_n \bar{\mathbf{h}}_n$$

so the objective becomes $\bar{\mathbf{h}}_n^H \bar{\boldsymbol{\Gamma}}_n \bar{\mathbf{h}}_n$ with the $PL_n \times PL_n$ block matrix $[\bar{\boldsymbol{\Gamma}}_n]_{ij} = \mathbf{H}_{n,i}^H \boldsymbol{\Gamma} \mathbf{H}_{n,j}$, and the constraint becomes $\bar{\mathbf{h}}_n^H \bar{\mathbf{d}}_n = 1$ with $\bar{\mathbf{d}}_n = [\mathbf{d}_{\theta_s}^H \mathbf{H}_{n,1}, \dots, \mathbf{d}_{\theta_s}^H \mathbf{H}_{n,P}]^T$. With all other filter groups fixed, the Lagrangian solution is MVDR-like:

$$\bar{\mathbf{h}}_n = \frac{\bar{\boldsymbol{\Gamma}}_n^{-1} \bar{\mathbf{d}}_n}{\bar{\mathbf{d}}_n^H \bar{\boldsymbol{\Gamma}}_n^{-1} \bar{\mathbf{d}}_n}$$

The algorithm **initializes** all groups, then cycles through $n = 1, \dots, N$ updating each $\bar{\mathbf{h}}_n$ in closed form (recomputing $\bar{\mathbf{d}}_n, \bar{\boldsymbol{\Gamma}}_n$ from the current estimates), iterating until convergence. **Robustness**: each subproblem inverts the diagonally loaded matrix $\bar{\boldsymbol{\Gamma}}_n + \epsilon \mathbf{I}_{PL_n}$, so the WNG–DF trade-off is controlled *inside* the iteration rather than only at the end.

### Complexity and storage

Per frequency bin, the conventional RSD stores $M$ complex parameters and inverts an $M \times M$ matrix; LR-RSD stores $P \sum_{n=1}^{N} L_n$ parameters and the largest inversion is only $P L_1 \times P L_1$ (with $L_1 \geq L_2 \geq \cdots \geq L_N$). With $K$-point STFT, totals are $(K/2{+}1)M$ vs. $(K/2{+}1) P \sum_n L_n$.

## Experimental Setup

| Item | Value |
|:-----|:------|
| Arrays | (i) ULA $M = 8$, 1.0 cm spacing; (ii) ULA $M = 64$, 1.0 cm; (iii) concentric circular $M = 64$ (rings at radii 15/12/8/5/2/0 cm with 24/15/12/8/4/1 mics) |
| Look direction | $\theta_s = 0°$ |
| Decomposition | 3-way tensor decomposition; $L_1{=}L_2{=}L_3{=}2$ ($M{=}8$), $L_1{=}L_2{=}L_3{=}4$ ($M{=}64$); rank $P \in \{1,2,3,4\}$ |
| Loading | fixed $\epsilon = 10^{-6}$ (ULA-8), $\epsilon = 5 \times 10^{-10}$ (concentric); per-frequency bisection on $\epsilon$ to enforce a WNG target in the comparison/speech experiments |
| Speech data | TIMIT, 200 random trials; target at $\theta_s = 0°$, 1–2 m; 1–2 interferers at 135°–225°, 1–2 m, same power as target |
| Acoustics | Image-source RIRs, room $8 \times 5 \times 3$ m, $T_{60}$ 200–800 ms; diffuse noise SNR 10–20 dB, white noise SNR 20–30 dB |
| STFT | Frame 256 (simulations) / 512 (measurements), 75% overlap / 128 hop, Kaiser window $\beta = 1.9\pi$; 16 kHz (measurements) |
| WNG constraint (speech) | $\geq -10$ dB via per-frequency bisection on $\epsilon$ |
| Metrics | DF, WNG, beampatterns; SNR, SIR, STOI |
| Real test | Anechoic chamber ($11.8 \times 4.2 \times 3.8$ m), 8-mic ULA at 3 cm spacing on rotating platform (360 × 1°, 6 s holds), narrowband source at 2 m, $f = 1$ and 2 kHz |

## Results

**Rank trade-off.** Across all three arrays, increasing $P$ narrows the main lobe, lowers sidelobes, raises DF, and lowers WNG — $P$ acts as a continuous DF-vs-robustness knob, reproducing the RSD trade-off within the low-rank family. The low-frequency WNG amplification of superdirective designs persists; it is mitigated by smaller $P$ or larger $\epsilon$.

*Table 1: Complexity for $M = 64$, $K = 256$, $N = 3$, $L_1{=}L_2{=}L_3{=}4$.*

| Method | Params/bin | Total params | Max inversion dim |
|:-------|:-----------|:-------------|:------------------|
| RSD | 64 | 8256 | 64 |
| LR-RSD ($P{=}1$) | 12 | 1548 | 4 |
| LR-RSD ($P{=}2$) | 24 | 3096 | 8 |
| LR-RSD ($P{=}4$) | 48 | 6192 | 16 |

At $P = 2$: **−62.5% parameters and −87.5% max inversion dimension** versus RSD.

**Convergence.** DF and WNG stabilize after ~18 alternating iterations (e.g., DF = 30.546 dB, WNG = 0.236 dB for the $M = 64$ ULA, essentially independent of $P$ at convergence).

**Decomposition-mode comparison** ($M = 64$ ULA, $P = 2$, WNG pinned to 0 dB by per-frequency bisection on $\epsilon$):

- With $N = 3$ fixed, the three modes LR-RSD-I ($L = 4,4,4$ uniform), II ($8,4,2$), III ($16,4,4$) perform nearly identically and all approach the conventional RSD with far fewer parameters — the **uniform** mode is the most practical (lowest params and inversion dimension).
- With uniform modes and $P = 2$, varying $N = 2$ ($8,8$), 3 ($4,4,4$), 4 ($4,4,2,2$), 5 ($4,2,2,2,2$), 6 ($2,2,2,2,2,2$): performance differences are minor, but **larger $N$ monotonically reduces parameters and inversion dimension** — decomposing into more, shorter filter groups is the cheaper axis.

*Table 6: Speech enhancement (TIMIT, WNG ≥ −10 dB). LR-RSD uses $N = 3$.*

| Array | Method | SNR /dB | SIR /dB | STOI |
|:------|:-------|:--------|:--------|:-----|
| ULA $M{=}8$ | Observation | −0.661 | −7.265 | 0.447 |
| | RSD | 5.582 | 2.916 | 0.642 |
| | LR-RSD ($P{=}1$) | 5.560 | 3.073 | 0.624 |
| | LR-RSD ($P{=}2$) | 5.508 | 2.780 | 0.638 |
| | LR-RSD ($P{=}4$) | 5.456 | 2.761 | 0.638 |
| ULA $M{=}64$ | Observation | 1.097 | −6.647 | 0.469 |
| | RSD | 11.183 | 10.897 | 0.826 |
| | LR-RSD ($P{=}1$) | 11.484 | 10.336 | 0.823 |
| | LR-RSD ($P{=}2$) | 11.441 | 10.841 | 0.825 |
| | LR-RSD ($P{=}4$) | 11.321 | 10.935 | 0.827 |
| Concentric $M{=}64$ | Observation | 0.433 | −5.440 | 0.461 |
| | RSD | 9.450 | 8.117 | 0.759 |
| | LR-RSD ($P{=}1$) | 9.258 | 6.077 | 0.724 |
| | LR-RSD ($P{=}2$) | 9.744 | 7.371 | 0.745 |
| | LR-RSD ($P{=}4$) | 9.937 | 7.751 | 0.758 |

With 12–48 instead of 64 parameters per bin, LR-RSD matches or exceeds RSD on SNR (ULA-64: 11.48 vs. 11.18 dB at $P{=}1$; concentric: 9.94 vs. 9.45 dB at $P{=}4$) and STOI, with SIR within ~0.6 dB (concentric $P{=}1$ is the weakest at 6.08 vs. 8.12 dB but recovers with $P{=}4$).

**Real-world validation.** Measured narrowband beampatterns (anechoic chamber, $f = 1$ and 2 kHz, $M = 8$ ULA) closely match the theoretical patterns, especially in the main-lobe region, confirming practical deployability.

## Key Contributions

1. **Multidimensional Kronecker product beamforming** — generalizes the existing 2-D Kronecker product beamforming to an $N$-way, rank-$P$ decomposition applicable to arbitrary array geometries, with a systematic study of how decomposition mode ($L_n$ distribution, number of groups $N$, rank $P$) affects performance.
2. **LR-RSD alternating algorithm** — closed-form per-group updates (MVDR-like solutions on $PL_n$-dimensional stacked problems) with diagonal loading embedded in every subproblem, converting the optimization of one long filter into that of several short filters.
3. **Parameter and complexity reduction** — $P\sum_n L_n$ stored parameters per bin and $PL_1$-dimensional inversions instead of $M$ and $M$; e.g., −62.5% parameters and −87.5% inversion size at $P = 2$, $M = 64$.
4. **Rank-$P$ robustness knob** — $P$ continuously trades directivity factor against white noise gain, reproducing and refining the classical RSD trade-off inside a low-rank family; convergence in ~18 iterations.
5. **Comprehensive validation** — simulations on ULA and concentric circular arrays (up to $M = 64$), TIMIT-based speech enhancement with reverberation and interference (SNR/SIR/STOI), and anechoic-chamber measurements matching theoretical beampatterns.

## Related Concepts

- [[concepts/superdirective-beamforming|Superdirective Beamforming]]
- [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/diagonal-loading|Diagonal Loading]]
- [[concepts/fixed-beamformer|Fixed Beamformer]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
