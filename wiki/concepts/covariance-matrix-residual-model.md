---
type: concept
created: 2026-09-19
updated: 2026-09-19
sources:
  - raw/papers/pan-2026-array-self-awareness/full-text.md
tags:
  - covariance-matrix-modeling
  - array-processing
  - spatial-statistics
  - optimization-algorithms
---

# Covariance Matrix Residual Model

The **covariance matrix residual model**, introduced by Pan, Chen & Benesty (2026), is a parametric model for the *residual* of the array observation covariance matrix — the part $\phi_{\xi}(t)\Gamma_{\xi} = \Phi_{\mathbf{y}}(t) - \sum_{n=1}^{N+1}\phi_{X,n}(t)\Gamma_{\mathbf{x},n}$ left over after subtracting the contributions of the known interferences and background noise. Fitting the model recovers the coherence matrix $\Gamma_{\xi}$ of an *unknown, newly emerging* source from a single frame's covariance estimate — the technical core of [[concepts/array-self-awareness|array self-awareness]].

## Amplitude–Phase Separated Model

In the simplest case (only background noise known, with coherence matrix $\Gamma_{\mathbf{x}}$, e.g. diffuse noise with sinc elements), take the eigendecomposition $\Gamma_{\mathbf{x}} = \mathbf{Q}\boldsymbol{\Lambda}\mathbf{Q}^{H}$. The model separates the amplitude and phase of the transformed new-source coherence matrix:

$$
\mathbf{Q}^{H}\Gamma_{\xi}\mathbf{Q} = \left(\mathbf{a}\mathbf{a}^{T}\right) \odot e^{\mathcal{J}\mathbf{P}},
\qquad
\Gamma_{\xi} = \mathbf{Q}\left[\left(\mathbf{a}\mathbf{a}^{T}\right) \odot e^{\mathcal{J}\mathbf{P}}\right]\mathbf{Q}^{H},
$$

where $\mathbf{a} = [A_1 \cdots A_M]^{T}$, $A_m > 0$, $\odot$ is the Hadamard product, $\mathcal{J}$ is the imaginary unit, and $\mathbf{P}$ is a symmetric matrix with elements in $[0, 2\pi]$.

### Phase Estimation (closed form)

Left/right-multiplying the covariance model by $\mathbf{Q}^{H}$/$\mathbf{Q}$ gives $\mathbf{Q}^{H}\Phi_{\mathbf{y}}(t)\mathbf{Q} = \phi_{\xi}(t)\,\mathbf{Q}^{H}\Gamma_{\xi}\mathbf{Q} + \phi_{X}(t)\boldsymbol{\Lambda}$. Since $\phi_{\xi}, \phi_{X} \geq 0$ and $\boldsymbol{\Lambda}$ is diagonal with nonnegative real entries, the phase of the residual equals the phase of the observable transformed covariance:

$$
\mathbf{P} = \angle\left[\mathbf{Q}^{H}\Phi_{\mathbf{y}}(t)\,\mathbf{Q}\right].
$$

### Amplitude Estimation (fixed-point iteration)

The off-diagonal magnitudes satisfy $A_iA_j \propto |\mathbf{q}_i^{H}\Phi_{\mathbf{y}}(t)\mathbf{q}_j|$ for $i \neq j$. The optimal amplitudes minimize Csiszár's I-divergence between $A_iA_j$ and $|\mathbf{q}_i^{H}\Phi_{\mathbf{y}}(t)\mathbf{q}_j|$:

$$
\mathcal{I}(\mathbf{a}) = -\sum_{i=1}^{M}\sum_{j\neq i}\left[\left|\mathbf{q}_i^{H}\Phi_{\mathbf{y}}(t)\mathbf{q}_j\right|\ln(A_iA_j) - A_iA_j\right],
$$

which has no closed-form minimizer but yields, by setting $\partial\mathcal{I}/\partial A_i = 0$, the fixed-point update

$$
A_i \leftarrow \frac{B_i}{\sum_{j\neq i} A_j},
\qquad
B_i \triangleq \sum_{j\neq i}\left|\mathbf{q}_i^{H}\Phi_{\mathbf{y}}(t)\mathbf{q}_j\right|,
$$

initialized at $A_i = \sqrt{B_i/(M-1)}$. The iteration converges rapidly (verified on a toy example over 1000 random initializations, all reaching the ground truth; max 20 iterations used in practice), and its cost is negligible next to the variance update. The I-divergence minimization is inspired by NMF-style multiplicative updates (Lee & Seung) and Kameoka et al.'s spectral-envelope estimation.

### Post-Processing

The resulting $\Gamma_{\xi}$ is repaired by removing its negative eigenvalues and rescaling so that $\mathrm{tr}(\Gamma_{\xi}) = M$ (the coherence-matrix normalization). The authors note that more effective repair rules are open for future work.

## General Case

With $N$ known sources, the interference-plus-noise side is first compressed into a single term: rough variances $\phi_{X,n}(t)$ are estimated from the known coherence matrices (maximum-likelihood variance function $f_{\mathrm{V}}[\cdot]$), and the **total coherence matrix** $\Gamma_{\mathbf{x}} = \sum_{n} H_n(t)\Gamma_{\mathbf{x},n}$ (Wiener-filter-weighted) replaces the noise coherence matrix, after which the same amplitude–phase machinery applies.

## Relation to Other Covariance Decompositions

| Method | Decomposition | What is known a priori | Reference |
|--------|---------------|------------------------|-----------|
| [[concepts/variance-ratio-estimation|Variance ratio estimation]] | Normalized SCM = weighted sum of coherence matrices, weights sum to 1 | All component coherence matrices, including the target's | Liu 2026 |
| Covariance subtraction | $\Phi^{(\mathrm{Sec})} = \Phi^{(\mathrm{Tot})} - \Phi^{(\mathrm{Pri})}$ (exact differencing of two measurements) | Two measured SCMs | [[concepts/covariance-subtraction|Covariance subtraction]] |
| **Residual model** | $\Phi_{\mathbf{y}} = \phi_{\xi}\Gamma_{\xi} + \phi_X\Gamma_{\mathbf{x}}$, $\Gamma_{\xi}$ parametrized as $(\mathbf{a}\mathbf{a}^{T}) \odot e^{\mathcal{J}\mathbf{P}}$ in the eigenbasis of $\Gamma_{\mathbf{x}}$ | Only the *unwanted* components' coherence matrices — the new source's emerges from the residual | Pan, Chen & Benesty 2026 |

Unlike variance-ratio estimation, the residual model does not need the target's coherence matrix as a basis element — that is precisely what makes it usable for sources never observed before.

## Related Concepts

- [[concepts/array-self-awareness|Array Self-Awareness]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/spatial-coherence|Spatial Coherence]]
- [[concepts/variance-ratio-estimation|Variance Ratio Estimation]]
- [[concepts/covariance-subtraction|Covariance Subtraction]]
- [[concepts/wiener-filter|Wiener Filter]]

## Related Sources

- [[sources/pan-2026-array-self-awareness|Pan, Chen & Benesty 2026: Microphone Array Self-Awareness via a Residual Model of the Covariance Matrix]]
