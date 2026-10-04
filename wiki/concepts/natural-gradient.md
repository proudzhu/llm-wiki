---
type: concept
created: 2026-08-22
updated: 2026-10-04
sources:
  - raw/papers/low-2004-hybrid-bss-anc/full-text.txt
  - raw/papers/ruan-2024-speech-extraction-low-snr/full-text.md
  - raw/papers/ono-2011-stable-fast-update-rules-iva/full-text.md
  - raw/papers/scheibler-2020-fast-stable-bss-rank-1-updates/full-text.md
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

The update also has a long history in subband frequency-domain ICA for speech: [[sources/low-2004-hybrid-bss-anc|Low & Nordholm 2004]] train per-subband unmixing matrices with the InfoMax natural-gradient rule $\Delta\mathbf{V}^{(m)} \propto \eta[\mathbf{I} - 2\varphi(\mathbf{y}^{(m)})(\mathbf{y}^{(m)})^{H}]\mathbf{V}^{(m)}$, where $\varphi = \tanh(\Re\,\cdot) + j\tanh(\Im\,\cdot)$ matches the supergaussian (Laplacian) distribution of subband speech.

## Practical Benefits (vs. ordinary gradient)

- **No matrix inversion** — the $(\hat{\mathbf{C}}_{\mathbf{x}}^i)^{-1}$ term of ordinary-gradient OGIVEa is absorbed, improving efficiency and numerical stability.
- **Stable, smooth convergence** — OGIVEa's unstable convergence and suboptimal-solution drift disappear with the natural gradient.
- **Parameterization invariance** — the update does not depend on the choice of coordinates on the manifold.

Within the IVA optimization-family taxonomy (see [[concepts/independent-vector-analysis|IVA]]), natural gradient is the step-size-based Riemannian descent route: flexible but step-size sensitive, whereas AuxIVA ([[sources/ono-2011-stable-fast-update-rules-iva|Ono 2011]]) achieves monotonic convergence without step sizes — the property that made auxiliary-function updates largely displace natural-gradient IVA in frequency-domain BSS.

## Related Concepts

- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/independent-vector-extraction|Independent Vector Extraction]]
- [[concepts/ogive|OGIVE]]

## Related Sources

- [[sources/low-2004-hybrid-bss-anc|Low & Nordholm 2004: A Hybrid Speech Enhancement System Employing BSS and Adaptive Noise Cancellation]] — early subband InfoMax natural-gradient ICA for speech enhancement
- [[sources/ruan-2024-speech-extraction-low-snr|Ruan, Liao, Chen & Lu 2024: Speech Extraction Under Extremely Low SNR Conditions]]
- [[sources/ono-2011-stable-fast-update-rules-iva|Ono 2011: Stable and Fast Update Rules for Independent Vector Analysis Based on Auxiliary Function Technique]] — AuxIVA's auxiliary-function updates displace step-size-based natural-gradient IVA
- [[sources/scheibler-2020-fast-stable-bss-rank-1-updates|Scheibler & Ono 2020: Fast and Stable Blind Source Separation with Rank-1 Updates]] — ISS rank-1 updates further improve on the auxiliary-function family's stability and cost without matrix inversions
