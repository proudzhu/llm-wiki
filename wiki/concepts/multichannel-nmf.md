---
type: concept
created: 2026-08-19
updated: 2026-08-19
sources:
  - raw/papers/sawada-2019-bss-ilrma-review/full-text.md
tags:
  - blind-source-separation
  - nonnegative-matrix-factorization
  - spatial-covariance-matrix
  - audio-source-separation
---

# Multichannel NMF (MNMF)

**Multichannel NMF (MNMF)** is a determined [[concepts/blind-source-separation|blind source separation]] method that extends single-channel Itakura–Saito NMF to the multichannel case by adding a per-source **spatial property matrix** $\mathbf{H}^{(k)}_n$ to the NMF spectrogram model, treating the observed multichannel STFT coefficients as circularly-symmetric complex Gaussian with covariance $\sum_n \mathbf{H}^{(k)}_n \hat{y}_{nz}^{(k)}$. MNMF is one of the two converging routes to [[concepts/independent-low-rank-matrix-analysis|ILRMA]] surveyed in [[sources/sawada-2019-bss-ilrma-review|Sawada et al. 2019]].

## Problem Setting

Given $M$ microphone observations in the STFT domain and $N \leq M$ sources, MNMF models the observed vector $\mathbf{x}^{(k)}[z] \in \mathbb{C}^M$ as zero-mean circularly-symmetric complex Gaussian with covariance

$$\mathbf{R}^{(k)}[z] = \sum_n \mathbf{H}^{(k)}_n\, \hat{y}_{nz}^{(k)} \in \mathbb{C}^{M \times M},$$

where:

- $\mathbf{H}^{(k)}_n \in \mathbb{C}^{M \times M}$ is the **spatial property matrix** of source $n$ at frequency $k$ — a Hermitian positive-semidefinite matrix that encodes the spatial mixing (direction-of-arrival, reverberation) of source $n$,
- $\hat{y}_{nz}^{(k)} = \sum_l t_{nl}^{(k)} v_{lz}^{(k)}$ is the NMF spectrogram model for source $n$ at frequency $k$ and time $z$, with $\mathbf{T}_n \in \mathbb{R}_{\geq 0}^{K \times L}$ (bases) and $\mathbf{V}_n \in \mathbb{R}_{\geq 0}^{L \times Z}$ (activations).

The likelihood is

$$\mathcal{L}_{\mathrm{MNMF}} \propto \prod_{k,z}\frac{1}{\det\mathbf{R}^{(k)}[z]}\exp\bigl(-\mathbf{x}^{(k)\mathrm{H}}[z]\,(\mathbf{R}^{(k)}[z])^{-1}\,\mathbf{x}^{(k)}[z]\bigr).$$

## Source-Wise vs. Full MNMF

Two formulations exist in the literature, both surveyed in [[sources/sawada-2019-bss-ilrma-review|Sawada et al. 2019]]:

| Variant | Spatial property structure | Cluster assignment | Identifiability |
|---|---|---|---|
| **Full MNMF** (Ozerov & Févotte 2010) | Per-basis $\mathbf{H}^{(k)}_l$, basis $l$ not bound to a source | None — needs explicit source-basis clustering after fit | Poor; basis-spatial pairs are interchangeable |
| **Source-wise MNMF** (Sawada et al. 2013) | Per-source $\mathbf{H}^{(k)}_n$, with binary cluster assignment $z_{ln}$ s.t. each basis $l$ belongs to one source $n$ | Fixed at init — basis $l$ is bound to source $z_{ln} = n$ | Better; source structure is enforced |

The source-wise form is what bridges MNMF to ILRMA: by replacing the per-source $\mathbf{H}^{(k)}_n$ with the rank-1 form $(\mathbf{w}_n^{(k)})^{-1}(\mathbf{w}_n^{(k)})^{-\mathrm{H}}$, MNMF reduces exactly to [[concepts/independent-low-rank-matrix-analysis|ILRMA]].

## Update Rules (MM Algorithm)

MNMF is optimized by the majorization-minimization algorithm with auxiliary functions, giving multiplicative closed-form updates for $\mathbf{H}^{(k)}_n$, $\mathbf{T}_n$, $\mathbf{V}_n$. The per-frequency $M \times M$ matrix inversion $\mathbf{R}^{(k)}[z]$ at every $(k,z)$ — $\mathcal{O}(I J M^3)$ per iteration — is the dominant cost and makes MNMF markedly slower than ILRMA.

- $\mathbf{H}^{(k)}_n$: multiplicative update derived from the MM auxiliary function of the Gaussian log-likelihood (Sawada et al. 2013, Eq. 17-19).
- $t_{nl}^{(k)}$, $v_{lz}^{(k)}$: standard IS-NMF multiplicative updates, augmented with the spatial weighting.

Source images are recovered by the **multichannel Wiener filter**:

$$\hat{\mathbf{s}}_n^{(k)}[z] = \mathbf{H}^{(k)}_n \hat{y}_{nz}^{(k)} \,(\mathbf{R}^{(k)}[z])^{-1}\,\mathbf{x}^{(k)}[z].$$

## Relationship to ILRMA and FastMNMF

- Imposing **rank-1 spatial constraint** on $\mathbf{H}^{(k)}_n$ (i.e., $\mathbf{H}^{(k)}_n = (\mathbf{w}_n^{(k)})^{-1}(\mathbf{w}_n^{(k)})^{-\mathrm{H}}$) reduces MNMF to [[concepts/independent-low-rank-matrix-analysis|ILRMA]] — this is the "NMF route" to ILRMA in Sawada et al. 2019.
- [[concepts/fastmnmf|FastMNMF]] makes the **joint diagonalizability** assumption $\mathbf{R}^{(k)}[z] = \mathbf{W}_k^{\mathrm{H}}\mathrm{diag}(\ldots)\mathbf{W}_k$ across sources, avoiding the $\mathcal{O}(M^3)$ per-$(k,z)$ inversion at the cost of $\mathcal{O}(M^4)$ per-frequency diagonalization. This is the practical successor to full MNMF.

## Key Properties

- **Permutation-free**: by binding each NMF basis to a source via $z_{ln}$ and using a per-source spatial property $\mathbf{H}^{(k)}_n$, the source labels are consistent across frequency (in source-wise MNMF).
- **More general spatial model than ILRMA**: full-rank $\mathbf{H}^{(k)}_n$ can model reverberant / diffuse sources that the rank-1 ILRMA spatial model cannot.
- **Initialization-sensitive**: random NMF initialization combined with full-rank $\mathbf{H}^{(k)}_n$ makes MNMF prone to local optima; multiple restarts are typical.
- **Cluster assignment $z_{ln}$ is fixed**: not optimized jointly with the other parameters — a limitation that drives the move to FastMNMF / ILRMA in practice.

## Related Concepts

- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/independent-low-rank-matrix-analysis|Independent Low-Rank Matrix Analysis]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/fastmnmf|FastMNMF]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]

## Related Sources

- [[sources/sawada-2019-bss-ilrma-review|Sawada et al. 2019: BSS/ILRMA Review]]
- [[sources/nishikori-2026-fast-multichannel-nmf-block-diagonal-scm-bss|Nishikori et al. 2026: Distributed FastMNMF for BSS]]
