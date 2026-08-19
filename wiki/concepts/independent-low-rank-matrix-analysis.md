---
type: concept
created: 2026-08-19
updated: 2026-08-19
sources:
  - raw/papers/sawada-2019-bss-ilrma-review/full-text.md
tags:
  - blind-source-separation
  - independent-vector-analysis
  - nonnegative-matrix-factorization
  - audio-source-separation
  - optimization-algorithms
---

# Independent Low-Rank Matrix Analysis

**Independent Low-Rank Matrix Analysis (ILRMA)** is a determined [[concepts/blind-source-separation|blind source separation]] method that combines the spatial unmixing-matrix model of [[concepts/independent-vector-analysis|Independent Vector Analysis]] with the Itakura–Saito [[concepts/multichannel-nmf|Multichannel NMF]] source-spectrogram model, inheriting the permutation-free property of IVA and the interpretable low-rank spectral structure of NMF. ILRMA is the convergence point of the two routes through determined BSS surveyed in [[sources/sawada-2019-bss-ilrma-review|Sawada et al. 2019]].

## Problem Setting

Given $M$ microphone observations in the STFT domain with $N \leq M$ sources,

$$\mathbf{x}^{(k)}[z] = \mathbf{A}^{(k)}\mathbf{s}^{(k)}[z] \in \mathbb{C}^M,$$

ILRMA seeks a per-frequency unmixing matrix $\mathbf{W}^{(k)} \in \mathbb{C}^{N \times M}$ such that $\mathbf{y}^{(k)}[z] = \mathbf{W}^{(k)}\mathbf{x}^{(k)}[z]$ are the separated sources, while modeling each source's spectrogram $\mathbf{Y}_n \in \mathbb{C}^{K \times Z}$ (stacking $y_n^{(k)}[z]$ over frequency $k$ and time $z$) as a rank-$L$ NMF:

$$\mathbf{Y}_n \approx \mathbf{T}_n\mathbf{V}_n, \qquad \mathbf{T}_n \in \mathbb{R}_{\geq 0}^{K \times L},\ \mathbf{V}_n \in \mathbb{R}_{\geq 0}^{L \times Z}.$$

The "low-rank matrix" in the name refers to the source-wise spectrogram slice $\mathbf{Y}_n$ being approximately rank-$L$ — the third-order tensor of separated outputs $\mathbf{Y} \in \mathbb{C}^{N \times K \times Z}$ is decomposed into $N$ sliced low-rank matrices, one per source.

## Dual Derivation

ILRMA admits two equivalent derivations, which is what makes it the convergence point of the ICA and NMF routes:

### From the IVA side (cost-function viewpoint)

Start from the IVA cost with a spherical multivariate source contrast $G(\|\mathbf{y}_n\|)$:

$$\mathcal{J}_{\mathrm{IVA}} = -\sum_k \log|\det\mathbf{W}^{(k)}| - \sum_{n,z} G\bigl(\|\mathbf{y}_n[z]\|\bigr).$$

Replace $G(\|\mathbf{y}_n\|)$ with a per-source IS-NMF likelihood $-\sum_{k,z}\bigl(\log\hat{y}_{nz}^{(k)} + |y_n^{(k)}[z]|^2/\hat{y}_{nz}^{(k)}\bigr)$, where $\hat{y}_{nz}^{(k)} = \sum_l t_{nl}^{(k)} v_{lz}^{(k)}$. The result is the ILRMA cost.

### From the MNMF side (Gaussian-likelihood viewpoint)

Start from the [[concepts/multichannel-nmf|MNMF]] multichannel Gaussian negative log-likelihood with per-source spatial property matrix $\mathbf{H}^{(k)}_n$ and NMF spectrogram $\hat{y}_{nz}^{(k)}$:

$$\mathcal{J}_{\mathrm{MNMF}} = \sum_{k,z}\left[ \log\det\mathbf{R}^{(k)}[z] + \mathbf{x}^{(k)\mathrm{H}}[z]\,(\mathbf{R}^{(k)}[z])^{-1}\,\mathbf{x}^{(k)}[z] \right],$$

with $\mathbf{R}^{(k)}[z] = \sum_n \mathbf{H}^{(k)}_n \hat{y}_{nz}^{(k)}$. Imposing the **rank-1 spatial constraint** $\mathbf{H}^{(k)}_n = (\mathbf{w}_n^{(k)})^{-1}(\mathbf{w}_n^{(k)})^{-\mathrm{H}}$ (where $\mathbf{w}_n^{(k)}$ is the $n$-th row of $\mathbf{W}^{(k)}$) yields

$$\mathbf{R}^{(k)}[z] = (\mathbf{W}^{(k)})^{-1}\mathrm{diag}(\hat{y}_{1z}^{(k)},\ldots,\hat{y}_{Nz}^{(k)})(\mathbf{W}^{(k)})^{-\mathrm{H}},$$

and substituting plus change of variables $\mathbf{y} = \mathbf{W}\mathbf{x}$ gives exactly the ILRMA cost from the IVA side. The two derivations yield identical update rules.

## Cost Function and Updates

The ILRMA cost (negative log-likelihood, up to constants) is

$$\mathcal{J}_{\mathrm{ILRMA}} = 2Z\sum_k \log|\det\mathbf{W}^{(k)}| + \sum_{n,k,z}\left[\log\hat{y}_{nz}^{(k)} + \frac{|y_n^{(k)}[z]|^2}{\hat{y}_{nz}^{(k)}}\right].$$

It is minimized by the **majorization-minimization (MM) algorithm with auxiliary functions** (Ono 2011; Kitamura et al. 2016). The closed-form updates are:

- **Unmixing matrix** $\mathbf{W}^{(k)}$ (per source row $\mathbf{w}_n^{(k)}$, Iterative Projection):

  $$\mathbf{w}_n^{(k)} \leftarrow \left(\mathbf{X}^{(k)}(\mathbf{U}_n^{(k)})^{\mathrm{H}}\mathbf{X}^{(k)\mathrm{H}}\right)^{-1}\mathbf{u}_n^{(k)}, \quad \text{then normalize},$$

  where $\mathbf{U}_n^{(k)}$ is the auxiliary variable $u_{nz}^{(k)} = |y_n^{(k)}[z]|^2 / (\hat{y}_{nz}^{(k)})^2$ and $\mathbf{u}_n^{(k)}$ is the corresponding row of the auxiliary matrix.

- **NMF basis** $t_{nl}^{(k)}$ and **activation** $v_{lz}^{(k)}$ (multiplicative updates):

  $$t_{nl}^{(k)} \leftarrow t_{nl}^{(k)} \cdot \frac{\sum_z |y_n^{(k)}[z]|^2 v_{lz}^{(k)} / (\hat{y}_{nz}^{(k)})^2}{\sum_z v_{lz}^{(k)} / \hat{y}_{nz}^{(k)}},$$

  $$v_{lz}^{(k)} \leftarrow v_{lz}^{(k)} \cdot \frac{\sum_k |y_n^{(k)}[z]|^2 t_{nl}^{(k)} / (\hat{y}_{nz}^{(k)})^2}{\sum_k t_{nl}^{(k)} / \hat{y}_{nz}^{(k)}}.$$

All updates are multiplicative and monotonic — they never increase $\mathcal{J}_{\mathrm{ILRMA}}$.

## Key Properties

- **Permutation-free**: by binding source $n$ across all frequency bins through the NMF model $\mathbf{T}_n\mathbf{V}_n$, the source labels are inherently consistent (no post-hoc alignment needed, unlike frequency-domain ICA).
- **Scaling ambiguity**: a complex scaling per source per frequency remains; resolved by the **projection back** post-processing $\hat{\mathbf{s}}_n^{(k)}[z] = (\mathbf{w}_n^{(k)})^{-1} y_n^{(k)}[z]$ using the reference microphone.
- **Identifiability**: ILRMA is identifiable when each source's spectrogram is sufficiently low-rank and the mixing matrices are sufficiently different across sources.
- **Computational cost**: lower than MNMF (no per-bin $M \times M$ matrix inversions of $\mathbf{R}^{(k)}[z]$); the dominant cost is the IP update of $\mathbf{W}^{(k)}$, $\mathcal{O}(N^3 K Z)$ per iteration.
- **Initialization sensitivity**: random NMF initialization can lead to different local optima; multiple restarts are recommended.

## Variants and Successors

- **Determined ILRMA** (original Kitamura et al. 2016) — the form surveyed in [[sources/sawada-2019-bss-ilrma-review|Sawada et al. 2019]].
- **FastMNMF / FastMNMF2** — [[concepts/fastmnmf|FastMNMF]] generalizes the rank-1 spatial constraint of ILRMA to a jointly-diagonalizable full-rank spatial model.
- **MVAE** — replaces the IS-NMF source model with a deep variational autoencoder prior, integrating ILRMA's spatial model with learned spectral priors (Sekiya et al. 2019).
- **Subspace ILRMA / t-ILRMA / GGD-ILRMA** — extensions using richer source priors (Student-t, generalized Gaussian) that retain the MM framework.

## Relationship to IVA and MNMF

| Aspect | [[concepts/independent-vector-analysis\|IVA]] | [[concepts/multichannel-nmf\|MNMF]] | **ILRMA** |
|---|---|---|---|
| Spatial model | Rank-1 unmixing $\mathbf{W}^{(k)}$ | Full-rank $\mathbf{H}^{(k)}_n$ per source | Rank-1 $\mathbf{W}^{(k)}$ (= constrained MNMF) |
| Source spectrogram model | Spherical / laplacian contrast (single variance per source per bin) | Per-source IS-NMF $\mathbf{T}_n\mathbf{V}_n$ | Per-source IS-NMF $\mathbf{T}_n\mathbf{V}_n$ |
| Permutation-free | Yes (built into cost) | Yes (per-source spatial model) | Yes |
| Free parameter count | Lower | Higher | Moderate |

ILRMA sits at the intersection: IVA's spatial model + MNMF's spectrogram model, with the spatial model constrained to rank 1 to inherit IVA's permutation-free property and computational efficiency.

## Related Concepts

- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/multichannel-nmf|Multichannel NMF]]
- [[concepts/fastmnmf|FastMNMF]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]

## Related Sources

- [[sources/sawada-2019-bss-ilrma-review|Sawada et al. 2019: BSS/ILRMA Review]]
- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]]
- [[sources/nishikori-2026-fast-multichannel-nmf-block-diagonal-scm-bss|Nishikori et al. 2026: Distributed FastMNMF for BSS]]
