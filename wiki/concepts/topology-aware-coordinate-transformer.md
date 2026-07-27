---
type: concept
created: 2026-07-27
updated: 2026-07-27
sources:
  - raw/papers/liu-2026-array-invariant-speech-enhancement/full-text.md
tags:
  - transformer
  - microphone-arrays
  - positional-encoding
  - geometry-aware
  - deep-learning
  - speech-enhancement
---

# Topology-Aware Coordinate Transformer (TACT)

**Topology-Aware Coordinate Transformer (TACT)** is a Transformer-Encoder-based module that consumes Fourier-encoded microphone coordinates and produces a transformation coefficient matrix $\mathbf{M}$ used by [[concepts/geometry-aware-dynamic-convolution|Geo-DConv]] to generate geometry-specific dynamic convolution kernels. It is introduced by Liu, Zhang, Li & Qian (2026) as the geometry-conditioning branch of the Geo-DConv framework for [[concepts/array-invariant-speech-enhancement|array-invariant speech enhancement]].

## Motivation

To generate the transformation matrix $\mathbf{M} \in \mathbb{R}^{C \times b}$ from a coordinate matrix $\mathbf{G} \in \mathbb{R}^{C \times 3}$, two properties are essential:

1. **Global topology modeling** — each microphone's contribution must depend on the *entire* array configuration, not just its own coordinates, so that the model can capture inter-microphone spatial relationships.
2. **Permutation equivariance** — reordering the input microphones must produce a correspondingly reordered $\mathbf{M}$, so that downstream operations remain invariant under channel permutation.

TACT achieves both via Fourier Positional Encoding (PE) for fine-grained coordinate representation and a Transformer Encoder with Multi-Head Self-Attention (MHSA) for global, permutation-equivariant topology modeling.

## Architecture

### Step 1: Fourier Positional Encoding (PE)

Inspired by Implicit Neural Representations (NeRF, NAF), PE lifts each 3-D coordinate into a higher-dimensional sinusoidal feature:

$$
\gamma(\mathbf{g}_i) = \big[\mathbf{g}_i,\; \sin(2^0 \pi \mathbf{g}_i),\; \cos(2^0 \pi \mathbf{g}_i),\; \dots,\; \sin(2^{L-1} \pi \mathbf{g}_i),\; \cos(2^{L-1} \pi \mathbf{g}_i)\big]
$$

with $L$ frequency bands, giving $\mathbf{G}_{pe} \in \mathbb{R}^{C \times d_{pe}}$ where $d_{pe} = 3 + 6L$ (e.g., $d_{pe} = 39$ for $L = 6$).

### Step 2: Linear Projection to Hidden Dimension

$$
\mathbf{G}^{(0)} = \mathbf{G}_{pe} \mathbf{W}_{in}, \quad \mathbf{W}_{in} \in \mathbb{R}^{d_{pe} \times d_{\text{hidden}}}
$$

The projected matrix is treated as a sequence of $C$ tokens, one per microphone.

### Step 3: Transformer Encoder with MHSA

For each layer $l$:

$$
\mathbf{Q} = \mathbf{G}^{(l)} \mathbf{W}_Q, \quad \mathbf{K} = \mathbf{G}^{(l)} \mathbf{W}_K, \quad \mathbf{V} = \mathbf{G}^{(l)} \mathbf{W}_V
$$

$$
\mathbf{Z}^{(l+1)} = \text{LayerNorm}\big(\mathbf{Z}^{(l)} + \text{MHSA}(\mathbf{Q}, \mathbf{K}, \mathbf{V})\big)
$$

The MHSA allows every microphone token to attend to every other token, capturing global inter-microphone relationships in a single layer.

### Step 4: Linear Output Projection

After $L_{\text{layers}}$ encoding layers:

$$
\mathbf{M} = \mathbf{Z}^{(L_{\text{layers}})} \mathbf{W}_{out}, \quad \mathbf{W}_{out} \in \mathbb{R}^{d_{\text{hidden}} \times b}
$$

$\mathbf{M} \in \mathbb{R}^{C \times b}$ is the transformation matrix consumed by Geo-DConv.

## Permutation Equivariance Guarantee

Let $\mathbf{P} \in \{0,1\}^{C \times C}$ be a permutation matrix. Then:

- Fourier PE is point-wise, so $\mathbf{G}_{pe} \to \mathbf{P}\mathbf{G}_{pe}$.
- MHSA is permutation-equivariant (tokens are processed identically regardless of order), so $\mathbf{Z}^{(L_{\text{layers}})} \to \mathbf{P}\mathbf{Z}^{(L_{\text{layers}})}$.
- Therefore $\mathbf{M} \to \mathbf{P}\mathbf{M}$.

Combined with the linear combination in Geo-DConv, this yields $(\mathbf{P}\mathbf{X}) \circledast (\mathbf{P}\boldsymbol{\mathcal{W}}_{dyn}) = \mathbf{X} \circledast \boldsymbol{\mathcal{W}}_{dyn}$ — the convolution output is invariant under input permutation, a property previous array-agnostic methods achieve only empirically.

## Distinction from Related PE Schemes

| Scheme | Domain | Coordinate form | Used for |
|---|---|---|---|
| NeRF/NAF Fourier PE | 3-D vision / INR | Continuous $(x,y,z)$ | Implicit radiance / audio fields |
| [[concepts/doa-microphone-positional-encoding|MPE / DOA-MPE]] | Microphone arrays | Polar $(\varphi_m, d_m)$ + DOA | Geometry-conditioned target speaker extraction |
| **TACT Fourier PE** | Microphone arrays | Cartesian or spherical $(x,y,z)$ or $(r,\theta,\phi)$ | Array-invariant SE via dynamic convolution |

TACT's PE differs from MPE/DOA-MPE in two ways: (1) it operates directly on 3-D coordinates rather than polar angles relative to a centroid; (2) it does not encode a target DOA (the SE task has no single target direction — the target is whichever speaker is present).

## Typical Hyperparameters

| Parameter | Value | Description |
|:----------|:------|:------------|
| $L$ | 6 | PE frequency bands → $d_{pe} = 39$ |
| $d_{\text{hidden}}$ | 64 | Hidden dimension |
| Layers | 2 | Transformer encoder layers |
| Heads | 4 | MHSA heads |
| Output dim $b$ | 8 | Basis dimension of Geo-DConv |

## Related Concepts

- [[concepts/geometry-aware-dynamic-convolution|Geometry-Aware Dynamic Convolution (Geo-DConv)]]
- [[concepts/array-invariant-speech-enhancement|Array-Invariant Speech Enhancement]]
- [[concepts/attention-mechanism|Attention Mechanism]]
- [[concepts/doa-microphone-positional-encoding|DOA-Microphone Positional Encoding]] — alternative microphone PE
- [[concepts/geometry-conditioned-ssf|Geometry-Conditioned SSF]] — alternative geometry-conditioning approach

## Related Sources

- [[sources/liu-2026-array-invariant-speech-enhancement|Liu, Zhang, Li & Qian 2026: Array-Invariant SE via Geo-DConv]]
