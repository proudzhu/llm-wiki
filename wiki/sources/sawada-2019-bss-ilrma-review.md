---
type: source
created: 2026-08-19
updated: 2026-08-19
sources:
  - raw/papers/sawada-2019-bss-ilrma-review/full-text.md
  - https://doi.org/10.1017/ATSIP.2019.5
  - zotero://select/items/0_AVA2LQ34
tags:
  - review-paper
  - blind-source-separation
  - independent-component-analysis
  - independent-vector-analysis
  - nonnegative-matrix-factorization
  - multichannel-nmf
  - independent-low-rank-matrix-analysis
  - audio-source-separation
  - majorization-minimization
---

# Sawada, Ono, Kameoka, Kitamura & Saruwatari 2019: A Review of Blind Source Separation Methods

- **Authors**: [[entities/hiroshi-sawada|Hiroshi Sawada]]¹, [[entities/nobutaka-ono|Nobutaka Ono]]², [[entities/hirokazu-kameoka|Hirokazu Kameoka]]¹, [[entities/daichi-kitamura|Daichi Kitamura]]³, [[entities/hiroshi-saruwatari|Hiroshi Saruwatari]]⁴
- **Affiliations**: ¹NTT Corporation, Tokyo, Japan; ²Tokyo Metropolitan University, Hino, Japan; ³National Institute of Technology, Kagawa College, Takamatsu, Japan; ⁴The University of Tokyo, Japan
- **Venue**: APSIPA Transactions on Signal and Information Processing, Vol. 8, e12
- **Year**: 2019
- **Type**: Review article
- **DOI**: [10.1017/ATSIP.2019.5](https://doi.org/10.1017/ATSIP.2019.5)
- **Zotero**: [item AVA2LQ34](zotero://select/items/0_AVA2LQ34)
- **Submitted**: 5 Feb 2019; **Revised**: 11 Apr 2019; **Published**: 14 May 2019

## Summary

This review presents a unified tutorial and survey of **determined** [[concepts/blind-source-separation|blind source separation]] (BSS) for convolutive audio mixtures, tracing two converging routes that culminate in **Independent Low-Rank Matrix Analysis (ILRMA)**: (i) the **ICA route** — frequency-domain Independent Component Analysis → Independent Vector Analysis → ILRMA, and (ii) the **NMF route** — (Itakura–Saito) Nonnegative Matrix Factorization → Multichannel NMF → ILRMA. Both routes are shown to share a common optimization engine, the **majorization-minimization (MM) algorithm with auxiliary functions**, which provides closed-form, monotonic update rules for every method in the taxonomy. The paper contains a complete rederivation of the ILRMA update rules from both the IVA side (cost-function viewpoint) and the MNMF side (Gaussian-likelihood viewpoint), and validates the methods on speech mixtures recorded in a real room.

## Taxonomy

The paper organizes determined BSS methods into two lineages whose convergence point is ILRMA:

| Route | Lineage | Source model | Spatial model | Cost / Likelihood |
|-------|---------|--------------|---------------|-------------------|
| **ICA route** | ICA → IVA → ILRMA | ICA: time-domain non-Gaussian; IVA: spherical/laplace multivariate; ILRMA: NMF spectrogram | Per-frequency mixing/unmixing matrix $\mathbf{W}^{(k)}$ | Mutual information / negentropy |
| **NMF route** | NMF → MNMF → ILRMA | NMF: $TF = \sum_l t_{in}v_{ln}$; MNMF: NMF + spatial property $\mathbf{H}^{(k)}$ | Per-cluster spatial covariance $\mathbf{H}^{(k)}$ | IS divergence (NMF); Gaussian negative log-likelihood (MNMF) |

![[raw/papers/sawada-2019-bss-ilrma-review/figures/0dcb25019e0d10991132ef7b13bd25a65b9dc4eda4b8b7fb2b36e8eb385ae925.jpg|Figure 1: Two converging routes to ILRMA, originating from ICA and NMF (Sawada et al. 2019, Fig. 1).]]

*Figure 1: The unifying taxonomy of the review — ICA and NMF routes converge at ILRMA.*

A second timeline view emphasizes the historical trajectory of each route and the emergence of the majorization-minimization optimization framework as a shared engine:

![[raw/papers/sawada-2019-bss-ilrma-review/figures/8551b3c4334d06d8b5ca38e5b40c678465f39ccfb1aa2436e9ec65e2ffb5b806.jpg|Figure 2: Historical development of the two routes (Sawada et al. 2019, Fig. 2).]]

*Figure 2: Historical development of BSS methods along the ICA and NMF routes, showing when the majorization-minimization (MM) algorithm entered each lineage.*

## Problem Formulation

For $N$ sources and $M$ microphones ($M \geq N$, the **determined** case), the convolutive mixture in the STFT domain is

$$\mathbf{x}^{(k)}[z] = \mathbf{A}^{(k)}\mathbf{s}^{(k)}[z] \in \mathbb{C}^M$$

where $k$ is the frequency-bin index, $z$ is the time-frame index, $\mathbf{A}^{(k)} \in \mathbb{C}^{M \times N}$ is the (unknown) mixing matrix and $\mathbf{s}^{(k)}[z] \in \mathbb{C}^N$ stacks the source coefficients. BSS seeks an unmixing matrix $\mathbf{W}^{(k)} \in \mathbb{C}^{N \times M}$ such that

$$\mathbf{y}^{(k)}[z] = \mathbf{W}^{(k)}\mathbf{x}^{(k)}[z] \approx \mathbf{s}^{(k)}[z] .$$

Two intrinsic ambiguities are unavoidable: (i) the **permutation ambiguity** (each $\mathbf{W}^{(k)}$ is solved independently, so source $n$ in bin $k_1$ may not equal source $n$ in bin $k_2$), and (ii) the **scaling ambiguity** (the source magnitude is identifiable only up to a complex constant). The ICA→IVA→ILRMA lineage progressively addresses (i), while projection-back handles (ii).

### Tensor view

Stacking all time-frequency bins, the observed signal is a third-order tensor $\mathbf{X} \in \mathbb{C}^{K \times Z \times M}$. ILRMA processes the tensor as a collection of **sliced matrices** $\mathbf{Y}_n \in \mathbb{C}^{K \times Z}$ (one per source), with rank $L \leq \min(K, Z)$; a rank-$L$ NMF model $\mathbf{Y}_n \approx \mathbf{T}_n\mathbf{V}_n$ captures the low-rank spectrogram structure of source $n$.

![[raw/papers/sawada-2019-bss-ilrma-review/figures/b99292d84fbd854d2d482b6731d170ec7281274047930892bde5a463dfd46e6d.jpg|Figure 3: Sliced matrices Y_n form a third-order tensor of separated signals (Sawada et al. 2019, Fig. 3).]]

*Figure 3: Sliced matrices $\mathbf{Y}_n$ form a third-order tensor of separated signals; the rank of each slice corresponds to the source-model complexity.*

## Methodology (Surveyed Methods)

The review surveys five methods along the two routes. For each, it gives the cost function / likelihood, the auxiliary function, and the resulting closed-form MM update rule.

### A. ICA route

#### A.1 Independent Component Analysis (ICA)

Frequency-domain ICA assumes the source vector elements are statistically independent and nongaussian. With a contrast function $G(\cdot)$ (e.g., $\log \cosh$ for laplacian sources), the cost is

$$\mathcal{J}_{\mathrm{ICA}} = -\sum_k \log |\det \mathbf{W}^{(k)}| - \sum_{n,k,z} G\bigl(|y_n^{(k)}[z]|\bigr) .$$

Per-bin ICA yields $\mathbf{W}^{(k)}$ that suffers from the permutation ambiguity — source labels may differ across $k$, requiring post-hoc alignment (clustering of separated-output envelopes across frequency).

#### A.2 Independent Vector Analysis (IVA)

IVA models each source as a **vector** $\mathbf{y}_n = [y_n^{(1)}, \ldots, y_n^{(K)}]^T$ spanning all frequency bins and replaces the per-bin contrast $G(|\cdot|)$ with a **spherical multivariate** contrast $G(\|\mathbf{y}_n\|)$ that is permutation-invariant with respect to the elements within $\mathbf{y}_n$. The cost becomes

$$\mathcal{J}_{\mathrm{IVA}} = -\sum_k \log |\det \mathbf{W}^{(k)}| - \sum_{n,z} G\bigl(\|\mathbf{y}_n[z]\|\bigr)$$

which makes the source labels consistent across frequency **by construction**, eliminating the permutation problem. See [[concepts/independent-vector-analysis|Independent Vector Analysis]] for the full taxonomy of update rules (natural gradient, FastIVA, AuxIVA, IP/ISS/IPA).

![[raw/papers/sawada-2019-bss-ilrma-review/figures/f65d4f531bf601eeea79b9132332b4c1fb5a117abe6d0559880fb03f6a5938bf.jpg|Figure 4: ICA vs. IVA — independence model assumptions (Sawada et al. 2019, Fig. 4).]]

*Figure 4: ICA (top) assumes independent scalar elements, whereas IVA (bottom) assumes independent vectors across frequency, with intra-vector dependencies giving permutation-robust separation.*

### B. NMF route

#### B.1 Nonnegative Matrix Factorization (NMF) with Itakura–Saito divergence

For a single-channel spectrogram $\mathbf{Y} \in \mathbb{R}_{\geq 0}^{K \times Z}$, IS-NMF decomposes

$$\mathbf{Y} \approx \mathbf{T}\mathbf{V}, \qquad \mathbf{T} \in \mathbb{R}_{\geq 0}^{K \times L},\ \mathbf{V} \in \mathbb{R}_{\geq 0}^{L \times Z}$$

by minimizing the Itakura–Saito divergence

$$\mathcal{D}_{\mathrm{IS}}(\mathbf{Y}\,\|\,\mathbf{T}\mathbf{V}) = \sum_{k,z} \left[ \frac{y_{kz}}{\hat{y}_{kz}} - \log\frac{y_{kz}}{\hat{y}_{kz}} - 1 \right], \qquad \hat{y}_{kz} = \sum_l t_{kl} v_{lz} .$$

IS-NMF is equivalent to maximum-likelihood estimation of $\mathbf{T}, \mathbf{V}$ under a Gaussian model with variance $\hat{y}_{kz}$ — a property leveraged in MNMF and ILRMA.

![[raw/papers/sawada-2019-bss-ilrma-review/figures/ae49eaa085740d9fbd2a9283f9c819f4ef3e969586e48065b3d8829f12bf57c5.jpg|Figure 5: NMF as spectrogram model fitting with IS divergence (Sawada et al. 2019, Fig. 5).]]

*Figure 5: NMF models an observed spectrogram as a low-rank product $\mathbf{T}\mathbf{V}$ optimized by minimizing the IS divergence.*

#### B.2 Multichannel NMF (MNMF)

[[concepts/multichannel-nmf|MNMF]] extends IS-NMF to the multichannel Gaussian model. The observed $\mathbf{x}^{(k)}[z] \in \mathbb{C}^M$ is modeled as circularly-symmetric complex Gaussian with zero mean and covariance

$$\mathbf{R}^{(k)}[z] = \sum_l \mathbf{H}^{(k)}_l \, \hat{y}_{lz}^{(k)}, \qquad \hat{y}_{lz}^{(k)} = \sum_n t_{ln}^{(k)} v_{nz}^{(k)}$$

where $\mathbf{H}^{(k)}_l \in \mathbb{C}^{M \times M}$ is a Hermitian positive-semidefinite **spatial property matrix** (an unconstrained spatial covariance per NMF basis $l$, not per source), and $\hat{y}_{lz}^{(k)}$ is the NMF spectrogram model. Sawada et al. (2013) introduced a **source-wise** MNMF in which each $\mathbf{H}^{(k)}_l$ is assigned to a source $n$ via a binary cluster indicator $z_{ln}$:

$$\mathbf{R}^{(k)}[z] = \sum_n \mathbf{H}^{(k)}_n \sum_{l: z_{ln}=n} t_{ln}^{(k)} v_{nz}^{(k)} = \sum_n \mathbf{H}^{(k)}_n \hat{y}_{nz}^{(k)} .$$

Source separation is recovered by the **multichannel Wiener filter** (source images $\hat{\mathbf{s}}_n^{(k)}[z] = \mathbf{H}^{(k)}_n \hat{y}_{nz}^{(k)} (\mathbf{R}^{(k)}[z])^{-1} \mathbf{x}^{(k)}[z]$). Per-source $\mathbf{H}^{(k)}_n$ gives MNMF full flexibility over spatial mixing — a more general model than IVA's rank-1 spatial structure — at higher computational cost and parameter identifiability issues.

![[raw/papers/sawada-2019-bss-ilrma-review/figures/0da2d5bdbebf4958376f9ef577061c5a983af7e15baa60c6686d47444f4d5622.jpg|Figure 6: MNMF with source-wise spatial property matrix (Sawada et al. 2019, Fig. 6).]]

*Figure 6: Source-wise MNMF — each NMF basis $l$ is assigned to a source via $z_{ln}$, and each source has its own spatial property matrix $\mathbf{H}^{(k)}_n$.*

### C. Convergence: Independent Low-Rank Matrix Analysis (ILRMA)

[[concepts/independent-low-rank-matrix-analysis|ILRMA]] is the convergence point of the two routes. ILRMA combines:

- the **per-frequency unmixing matrix** $\mathbf{W}^{(k)}$ from the ICA route (per-bin spatial model, $N \times M$ parameters per bin), and
- the **NMF source spectrogram model** $\mathbf{Y}_n \approx \mathbf{T}_n \mathbf{V}_n$ from the NMF route (per-source low-rank spectral structure, $L(K + Z)$ parameters per source).

The resulting likelihood treats the separated output $\mathbf{y}^{(k)}[z] = \mathbf{W}^{(k)}\mathbf{x}^{(k)}[z]$ as a sum of $N$ independent complex-Gaussian source vectors whose variances are $\hat{y}_{nz}^{(k)} = \sum_l t_{nl}^{(k)} v_{lz}^{(k)}$ (IS-NMF model per source $n$). Equivalently, ILRMA is rank-1 spatial MNMF where $\mathbf{H}^{(k)}_n = (\mathbf{w}_n^{(k)})^{-1}(\mathbf{w}_n^{(k)})^{-\mathrm{H}}$ — the spatial property of source $n$ is the inverse-row-inverse-conjugate-transpose of the unmixing matrix.

The negative log-likelihood (the ILRMA cost) is

$$\mathcal{J}_{\mathrm{ILRMA}} = \frac{1}{Z}\sum_k 2Z \log |\det \mathbf{W}^{(k)}| + \sum_{n,k,z} \left[ \log \hat{y}_{nz}^{(k)} + \frac{|y_n^{(k)}[z]|^2}{\hat{y}_{nz}^{(k)}} \right]$$

which inherits IVA's permutation-free property (the multivariate source model binds source $n$ across all bins) and IS-NMF's interpretability (the spectrogram is decomposed into interpretable bases $\mathbf{T}_n$ and activations $\mathbf{V}_n$).

![[raw/papers/sawada-2019-bss-ilrma-review/figures/fafbc96ff6eb89131be7e69f2b51f0b585125be148d90b11bda0b8f4b8be8997.jpg|Figure 7: ILRMA as the convergence of IVA and MNMF (Sawada et al. 2019, Fig. 7).]]

*Figure 7: ILRMA fuses the ICA-route spatial unmixing matrix $\mathbf{W}^{(k)}$ with the NMF-route spectrogram model $\mathbf{T}_n\mathbf{V}_n$ for each source.*

### D. Optimization engine: majorization-minimization with auxiliary functions

Every method in the taxonomy is optimized by a **majorization-minimization (MM) algorithm with an auxiliary function**. For a cost $\mathcal{J}(\theta)$, an auxiliary function $\mathcal{J}^{+}(\theta, \alpha)$ must (i) majorize the cost: $\mathcal{J}^{+}(\theta, \alpha) \geq \mathcal{J}(\theta)$ for all $\alpha$, and (ii) touch the cost at the current iterate: $\mathcal{J}^{+}(\theta^{(\tau)}, \alpha) = \mathcal{J}(\theta^{(\tau)})$ for some $\alpha$. Minimizing $\mathcal{J}^{+}$ with respect to $\theta$ then yields a monotonic update $\theta^{(\tau+1)} = \arg\min_\theta \mathcal{J}^{+}(\theta, \alpha)$ with closed form for the BSS family.

The review shows in detail that:

- **AuxIVA**: the auxiliary function for the IVA contrast $G(\|\mathbf{y}_n\|)$ gives the closed-form IP update of Ono (2011) for $\mathbf{W}^{(k)}$.
- **IS-NMF**: the auxiliary function for the IS divergence gives the standard multiplicative updates for $\mathbf{T}$ and $\mathbf{V}$.
- **MNMF**: the auxiliary function for the multichannel Gaussian log-likelihood gives updates for $\mathbf{H}^{(k)}_n$, $\mathbf{T}$, $\mathbf{V}$ — but the source-basis assignment $z_{ln}$ is fixed at init.
- **ILRMA**: the auxiliary function for $\mathcal{J}_{\mathrm{ILRMA}}$ yields the closed-form updates for $\mathbf{W}^{(k)}$, $\mathbf{T}_n$, $\mathbf{V}_n$ used in the original Kitamura et al. (2016) ILRMA.

![[raw/papers/sawada-2019-bss-ilrma-review/figures/828311c5ca54fe28878c36d8862589e6ee1340ff9aa2f5cd47959346b8c429fe.jpg|Figure 8: Concept of majorization-minimization with auxiliary function (Sawada et al. 2019, Fig. 8).]]

*Figure 8: The MM algorithm — auxiliary function (dashed) majorizes the true cost (solid) and is minimized in closed form, ensuring monotonic descent.*

## Experimental Setup

The methods are compared on speech mixtures recorded by a two-microphone linear array in a real reverberant room ($T_{60} \approx 130\,\mathrm{ms}$), using two- and three-source configurations at reverberant distances.

| Setup parameter | Value |
|---|---|
| Sources | 2 or 3 speech signals (male + female + female) |
| Microphones | 2-element linear array, 3-cm spacing |
| Source distance | 50 cm |
| Reverberation $T_{60}$ | ~130 ms |
| Sampling rate | 8 kHz |
| STFT window | 256-point Hann, 64-point shift |
| NMF basis $L$ | 2 sources: $L = 4$; 3 sources: $L = 6$ (ILRMA) |
| Initialization | Diagonal unmixing matrix; random NMF; H = identity (MNMF) |
| Iterations | 500 (ILRMA); 200 (MNMF) |
| Number of trials | 20 random initializations per condition |

## Results

The reported experimental outcomes support the convergence thesis:

### ICA → IVA → ILRMA progression on a 2-source mixture

![[raw/papers/sawada-2019-bss-ilrma-review/figures/65a0d3bf8ab850d396acb4f22cb0a48077302c802c2eed5fe81f6892f8e3ab8a.jpg|Figure 9: Source estimates for ICA, IVA, and ILRMA on a two-source mixture (Sawada et al. 2019, Fig. 9).]]

*Figure 9: Source estimates by ICA, IVA, and ILRMA — ILRMA produces the cleanest spectrograms with the least cross-talk.*

![[raw/papers/sawada-2019-bss-ilrma-review/figures/a1cbba2dff3f9dbf26373cadab9e833995af46d7327e281d8cbe22ca1fbcb47d.jpg|Figure 10: Auxiliary-variable view of ILRMA — separated sources and the corresponding NMF model (Sawada et al. 2019, Fig. 10).]]

*Figure 10: ILRMA auxiliary variables — the NMF activations $\mathbf{V}_n$ align with the separated-source spectrograms, validating the low-rank source-model assumption.*

### NMF → MNMF route on the same mixture

![[raw/papers/sawada-2019-bss-ilrma-review/figures/29773a5596abd403d8264e64326a3c48ea8f23154bbe0267f30970b10d68821e.jpg|Figure 11: Source estimates by NMF, MNMF, and ILRMA on a two-source mixture (Sawada et al. 2019, Fig. 11).]]

*Figure 11: NMF (single-channel) cannot separate the mixture; MNMF separates using spatial cues; ILRMA's combined spatial-spectral model gives the cleanest result.*

### Quantitative summary

The review reports SDR/SIR/SAR (BSS Eval) improvements consistent with the lineage ordering: ICA < IVA < ILRMA on the ICA route, and NMF < MNMF < ILRMA on the NMF route, with ILRMA achieving the best separation quality at lower computational cost than MNMF.

## Key Contributions

1. **Unified taxonomy**: A single figure (Fig. 1) situates ICA, IVA, NMF, MNMF, and ILRMA along two converging routes — the most-cited visualization of the determined-BSS landscape.
2. **Dual-derivation of ILRMA**: Derives the ILRMA cost and updates from **both** the IVA cost-function side (showing ILRMA = IVA with a rank-$L$ NMF source model) and the MNMF Gaussian-likelihood side (showing ILRMA = rank-1 spatial MNMF). The two derivations yield identical updates, formally demonstrating the convergence.
3. **MM-as-shared-engine**: Identifies the majorization-minimization algorithm with auxiliary functions as the common optimization engine of every method in the taxonomy; provides the auxiliary function for each.
4. **Source-wise MNMF**: Formalizes Sawada et al. (2013)'s source-cluster assignment $z_{ln}$ for MNMF, distinguishing it from the original Ozerov & Févotte (2010) full MNMF.
5. **Tensor / sliced-matrix view**: Frames the multichannel spectrogram as a third-order tensor and ILRMA's source model as a low-rank sliced-matrix factorization, motivating the name "Independent **Low-Rank Matrix** Analysis."
6. **Experimental validation**: Demonstrates the ICA < IVA < ILRMA and NMF < MNMF < ILRMA ordering of separation quality on real-room recordings.

## Limitations and Caveats

- **Determined-case only**: The review explicitly restricts to $M \geq N$. Underdetermined BSS (e.g., modeling each source with an NMF over multiple bases and using sparsity) is touched only briefly; the monophonic / underdetermined route surveyed in [[sources/richard-2023-audio-signal-processing-21st-century|Richard et al. 2023]] is not the focus.
- **Pre-deep-learning**: DNN-based source priors (MVAE, deep-cluster, mask-prediction networks) appeared the same year; the review covers only classical statistical methods.
- **Real-room experiments are small**: 2- and 3-source mixtures, single room, 2-mic array; results are illustrative rather than benchmark-grade. SDR numbers should not be compared across papers without controlling for setup.
- **MNMF computational cost**: The review notes that MNMF is markedly slower than ILRMA and prone to local optima; the "FastMNMF" of [[sources/nishikori-2026-fast-multichannel-nmf-block-diagonal-scm-bss|Nishikori et al. 2026]] (joint-diagonalizable SCMs) is the practical successor and is not yet part of this 2019 review.
- **Initialization sensitivity**: ILRMA and MNMF use random NMF initialization and 20 trials averaged; the review acknowledges high variance across runs.
- **Permutation problem in ICA**: The ICA subsection still needs post-hoc alignment; the review treats this as the historical motivation for IVA rather than as a current limitation.

## Related Concepts

- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/multichannel-nmf|Multichannel NMF (MNMF)]]
- [[concepts/independent-low-rank-matrix-analysis|Independent Low-Rank Matrix Analysis (ILRMA)]]
- [[concepts/fastmnmf|FastMNMF]] — practical successor to MNMF with joint-diagonalizable spatial covariances
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]

## Related Synthesis

(No dedicated synthesis page yet — the dual-derivation of ILRMA and the ICA/NMF route taxonomy themselves constitute the cross-source synthesis for determined BSS. See [[concepts/blind-source-separation|Blind Source Separation]] for the broader landscape.)
