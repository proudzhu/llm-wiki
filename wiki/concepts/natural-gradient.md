---
type: concept
created: 2026-08-22
updated: 2026-08-22
sources:
  - raw/papers/ruan-2024-speech-extraction-low-snr/full-text.md
tags:
  - optimization-algorithms
  - independent-vector-analysis
  - blind-source-extraction
  - signal-processing
---

# Natural Gradient

The **natural gradient** (Amari 1998) is the direction of steepest ascent of a cost function when the parameter space is a **Riemannian manifold** rather than flat Euclidean space: it premultiplies the ordinary gradient by the inverse Riemannian metric tensor, so the update follows the manifold's geometry instead of the coordinate system's.

## Role in BSS/BSE

The set of nonsingular demixing matrices $\mathbf{W}$ (or mixing matrices $\mathbf{A}$) forms a Riemannian manifold when equipped with the appropriate metric, and the ordinary gradient is *not* the true steepest-ascent direction there. For complex-valued audio separation, the natural gradient amounts to a simple premultiplication:

$$\Delta\mathbf{W}^{\mathrm{H}} \leftarrow \mathbf{W}^{\mathrm{H}}\mathbf{W}\,\Delta\mathbf{W}^{\mathrm{H}}, \qquad \Delta\mathbf{A} \leftarrow \mathbf{A}\mathbf{A}^{\mathrm{H}}\,\Delta\mathbf{A}$$

Applied to [[concepts/ogive|OGIVE]] by [[sources/ruan-2024-speech-extraction-low-snr|Ruan et al. 2024]] (yielding OGIVEw_NG and OGIVEa_NG), the natural-gradient update for the demixing vector becomes:

$$\Delta\mathbf{w}_i = \mathbf{w}_i - \frac{1}{J}\mathbf{W}_i^{\mathrm{H}}\mathbf{W}_i \sum_{j=1}^{J}\mathbf{x}_{ij}\varphi_i(\mathbf{s}_j)$$

and symmetrically for the mixing vector with $\mathbf{A}_i\mathbf{A}_i^{\mathrm{H}}$.

## Practical Benefits (vs. ordinary gradient)

- **No matrix inversion** — the $(\hat{\mathbf{C}}_{\mathbf{x}}^i)^{-1}$ term of ordinary-gradient OGIVEa is absorbed, improving efficiency and numerical stability.
- **Stable, smooth convergence** — OGIVEa's unstable convergence and suboptimal-solution drift disappear with the natural gradient.
- **Parameterization invariance** — the update does not depend on the choice of coordinates on the manifold.

Within the IVA optimization-family taxonomy (see [[concepts/independent-vector-analysis|IVA]]), natural gradient is the step-size-based Riemannian descent route: flexible but step-size sensitive, whereas AuxIVA achieves monotonic convergence without step sizes.

## Related Concepts

- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/independent-vector-extraction|Independent Vector Extraction]]
- [[concepts/ogive|OGIVE]]

## Related Sources

- [[sources/ruan-2024-speech-extraction-low-snr|Ruan, Liao, Chen & Lu 2024: Speech Extraction Under Extremely Low SNR Conditions]]
