---
type: concept
created: 2026-10-02
updated: 2026-10-02
sources:
  - raw/papers/grinstein-2024-srp-tutorial-review/full-text.md
tags:
  - steered-response-power
  - sound-source-localization
  - doa-estimation
  - audio-processing
---

# X-SRP (eXtensible Steered Response Power)

**X-SRP** is a generalized, modularized formulation of the [[concepts/steered-response-power|Steered Response Power (SRP)]] algorithm introduced by Grinstein et al. 2024 alongside their tutorial review of 200+ SRP papers. It re-expresses SRP as an algorithm built from replaceable **modules**, so that the many surveyed extensions (volumetric accumulation, iterative grid refinement, neural feature extraction, source de-emphasis, …) become instantiations of a common loop rather than ad-hoc variants. It is released as an open-source Python library ([github.com/egrinstein/xsrp](https://github.com/egrinstein/xsrp)).

## Modular Algorithm

The X-SRP loop substitutes the fixed operations of conventional SRP with generic modules:

| Module | Role | Example instantiations |
|--------|------|------------------------|
| `create_initial_candidate_grid` | Build the initial search grid $\mathbf{G}$ (Cartesian for position SSL, polar/spherical for DOA) | uniform grid, coarse grid + refinement |
| `compute_signal_features` | Compute the pairwise correlation features $\mathbf{C}$ | temporal CC, [[concepts/gcc-phat\|GCC-PHAT]], Deep-GCC |
| `create_srp_map` | Project features onto grid points → likelihood map $\mathbf{S}$ | conventional projection, V-SRP pooling |
| `grid_search` | Extract maximizing points $\hat{\mathcal{U}}$ and possibly a new grid | argmax, peak-picking, neural peak extraction |
| `update_signal_features` | Alter features between iterations (multi-source) | source de-emphasis, orthogonal-subspace projection |
| `update_grid` | Generate a new grid from current estimates | Stochastic Region Contraction, quadtree subdivision |

The framework accepts microphone signal frames, microphone positions, and (optionally, for position SSL) room dimensions; it returns a *set* of estimated positions to accommodate multi-source localization. For most single-source variants the loop executes once.

## Significance

- **Implementation-oriented literature grouping**: X-SRP offers an alternative to the review's task-oriented taxonomy — papers are grouped by *which module they replace*, facilitating combination and comparison of extensions.
- **Reproducibility**: the Python library implements selected extensions from the literature, serving as a baseline for reproducing SRP variants and exploring novel ones.

## Related Concepts

- [[concepts/steered-response-power|Steered-Response Power (SRP)]]
- [[concepts/gcc-phat|GCC-PHAT]]
- [[concepts/sound-source-localization|Sound Source Localization]]
- [[concepts/search-based-doa-estimation|Search-based DoA Estimation]]

## Related Sources

- [[sources/grinstein-2024-srp-tutorial-review|Grinstein et al. 2024: SRP for Sound Source Localization — a Tutorial Review]]
