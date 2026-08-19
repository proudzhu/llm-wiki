---
type: concept
created: 2026-08-19
updated: 2026-08-19
sources:
  - raw/papers/ishikawa-2025-real-time-speech-extraction/full-text.md
tags:
  - blind-source-separation
  - spatial-covariance-matrix
  - diffuse-noise
  - speech-extraction
  - rank-constrained
---

# Rank-Constrained Spatial Covariance Matrix Estimation

**Rank-Constrained Spatial Covariance Matrix Estimation (RCSCME)** is a blind speech-extraction method that models the observed multichannel covariance as a time-varying weighted sum of a **rank-1 target-speech** spatial covariance matrix (SCM) and a **full-rank diffuse-noise** SCM, then estimates both the time-varying weights and the diffuse-noise SCM jointly via a majorization-equalization algorithm with a sparsity-inducing inverse-gamma prior.

## Motivation

[[concepts/independent-low-rank-matrix-analysis|ILRMA]] assumes a **determined** mixture ($M = N$) and is permutation-free, but it cannot model diffuse noise directly — it forces every output channel to be a point source. RCSCME instead assumes $N = 1$ point target plus diffuse noise, so it can explicitly separate the target from isotropic background noise using only a single prior steering direction.

## Observed-SCM Model

For frequency bin $i$ and time frame $j$:

$$\mathcal{R}_{ij}^{(\mathrm{x})} = r_{ij}^{(\mathrm{t})}\,\mathbf{a}_i^{(\mathrm{t})}(\mathbf{a}_i^{(\mathrm{t})})^{\mathsf{H}} + r_{ij}^{(\mathrm{n})}\,\mathcal{R}_i^{(\mathrm{n})}, \tag{18}$$

where

- $\mathbf{a}_i^{(\mathrm{t})}$ is the target-speech steering vector (rank-1 spatial model),
- $r_{ij}^{(\mathrm{t})}, r_{ij}^{(\mathrm{n})}$ are the time-varying target and noise powers,
- $\mathcal{R}_i^{(\mathrm{n})}$ is the **full-rank diffuse-noise SCM**, estimated from the non-target ILRMA channels.

The rank constraint on the target SCM is the key feature: it makes the target spatially **point-like** while leaving the noise SCM **full-rank**, exactly matching the diffuse-noise physical scenario.

## Diffuse-Noise SCM Estimation

RCSCME constructs $\mathcal{R}_i^{(\mathrm{n})}$ from the $M-1$ non-target output channels of ILRMA (the "null space" of the target):

$$\mathcal{R}_i^{(\mathrm{n})} = \mathcal{R}_i^{\prime(\mathrm{n})} + \lambda_i\,\mathbf{z}_i\mathbf{z}_i^{\mathsf{H}}, \tag{20}$$

$$\mathcal{R}_i^{\prime(\mathrm{n})} = \frac{1}{J}\sum_j \hat{\mathbf{u}}_{ij}\hat{\mathbf{u}}_{ij}^{\mathsf{H}},\quad \hat{\mathbf{u}}_{ij} = (\mathbf{W}_i)^{-1}\tilde{\mathbf{y}}_{ij}^{(\mathrm{n})}, \tag{21}$$

where $\tilde{\mathbf{y}}_{ij}^{(\mathrm{n})}$ stacks the $M-1$ non-target separated outputs, $\mathbf{W}_i$ is the ILRMA demixing matrix, and $\lambda_i$ is a frequency-dependent scaling parameter that controls the noise SCM's contribution along the target direction $\mathbf{z}_i$.

## Cost Function with Sparsity-Inducing Prior

To handle intermittent target speech (silences), an inverse-gamma prior is placed on $r_{ij}^{(\mathrm{t})}$ with shape $\alpha > 0$ and scale $\beta > 0$. The resulting MAP cost is:

$$\mathcal{T}_{\mathrm{RCSCME}} = \sum_{i,j}\!\left[\mathbf{x}_{ij}^{\mathsf{H}}(\mathcal{R}_{ij}^{(\mathrm{x})})^{-1}\mathbf{x}_{ij} + \log\det\mathcal{R}_{ij}^{(\mathrm{x})} + (\alpha+1)\log r_{ij}^{(\mathrm{t})} + \frac{\beta}{r_{ij}^{(\mathrm{t})}}\right] + \text{const.} \tag{23}$$

The $(\alpha+1)\log r_{ij}^{(\mathrm{t})} + \beta/r_{ij}^{(\mathrm{t})}$ term acts as a **sparsity prior**: it shrinks $r_{ij}^{(\mathrm{t})}$ toward zero during silent target frames, properly separating the target's quiet periods from sustained diffuse noise.

## Majorization-Equalization Updates

RCSCME updates $r_{ij}^{(\mathrm{t})}, r_{ij}^{(\mathrm{n})}, \lambda_i$ using a **majorization-equalization algorithm** (a variant of MM that tightens the auxiliary upper bound at each step). Closed-form multiplicative updates exist for all parameters; see Eqs. (25)–(29) of [[sources/ishikawa-2025-real-time-speech-extraction|Ishikawa et al. 2025]] for the full update equations.

## Target-Image Extraction (MWF)

After convergence, the target image is extracted using the [[concepts/multi-channel-wiener-filter|multichannel Wiener filter]] derived from the estimated SCMs:

$$\hat{\mathbf{s}}_{ij} = \frac{r_{ij}^{(\mathrm{t})}}{r_{ij}^{(\mathrm{t})} + \lambda_i r_{ij}^{(\mathrm{n})}}\,\mathbf{a}_i^{(\mathrm{t})}\mathbf{w}_{in^{(\mathrm{t})}}^{\mathsf{H}}\mathbf{x}_{ij}, \tag{33}$$

where $\mathbf{w}_{in^{(\mathrm{t})}}$ is the ILRMA demixing row for the target channel. Note that $\mathbf{a}_i^{(\mathrm{t})} = (\mathbf{W}_i)^{-1}\mathbf{e}_{n^{(\mathrm{t})}}$, i.e. the target column of the ILRMA-estimated mixing matrix.

## Role in the Real-Time Framework

In the real-time blockwise batch framework, RCSCME runs **every STFT shift** (e.g. 32 ms) using the most recent $\mathbf{W}_i$ and $n^{(\mathrm{t})}$ from ILRMA, then outputs the target estimate. The rank-constrained model and sparsity prior are what allow the method to suppress diffuse noise in real time without explicit noise-only detection.

## Key Properties

- **Target rank-1 + noise full-rank**: matches the diffuse-noise physical scenario directly, unlike ILRMA (which assumes all sources are point-like).
- **Sparsity-inducing prior** on $r_{ij}^{(\mathrm{t})}$ properly handles intermittent speech.
- **Closed-form multiplicative updates** via majorization-equalization, suitable for real-time operation.
- **Coupled with ILRMA**: borrows ILRMA's demixing matrix $\mathbf{W}_i$ to construct the diffuse-noise SCM, so the two methods are designed to be used together.

## Related Concepts

- [[concepts/independent-low-rank-matrix-analysis|Independent Low-Rank Matrix Analysis (ILRMA)]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/spatial-regularization|Spatial Regularization]]
- [[concepts/fast-demixing-matrix-estimation|Fast Demixing Matrix Estimation]] (used in the real-time RCSCME framework)

## Related Sources

- [[sources/ishikawa-2025-real-time-speech-extraction|Ishikawa et al. 2025: Real-Time RCSCME-based Speech Extraction]]
