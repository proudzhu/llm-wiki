---
type: concept
created: 2026-07-27
updated: 2026-07-27
sources:
  - raw/papers/liu-2026-array-invariant-speech-enhancement/full-text.md
tags:
  - speech-enhancement
  - multi-channel
  - microphone-arrays
  - array-invariant
  - dynamic-convolution
  - geometry-aware
  - deep-learning
---

# Geometry-Aware Dynamic Convolution (Geo-DConv)

**Geometry-Aware Dynamic Convolution (Geo-DConv)** is a dynamic convolution layer that generates geometry-specific convolution kernels by linearly combining a small bank of basis kernels, where the combination weights are produced from explicit microphone array coordinates by a [[concepts/topology-aware-coordinate-transformer|Topology-Aware Coordinate Transformer (TACT)]]. It is the core module of the array-invariant speech enhancement framework introduced by Liu, Zhang, Li & Qian (2026), and serves as a **universal adapter** that converts any fixed-array SE backbone (e.g., SpatialNet, TF-GridNet) into an array-invariant system supporting arbitrary microphone counts and channel permutations.

## Motivation

Conventional convolutional layers require a **fixed input channel dimension**, blocking their use in [[concepts/array-invariant-speech-enhancement|array-invariant SE]] settings where the microphone count and ordering vary across deployments. Existing array-agnostic methods (TAC, USES2, FOA, UniArray) handle variable channel counts via batch operations or fixed-dimensional transformations but **fail to exploit explicit array geometry priors** — even though such priors are well-established in classical MVDR beamforming and modern geometry-invariant DOA estimation, and require no extra annotation effort (array coordinates are typically specified in multi-channel datasets).

Geo-DConv closes this gap by making the convolution kernel a function of microphone coordinates, allowing a single learned basis to be reshaped into geometry-specific weights at inference time.

## Formulation

Given multi-channel features $\mathbf{X} \in \mathbb{R}^{C \times F \times T}$ and coordinates $\mathbf{G} \in \mathbb{R}^{C \times 3}$, Geo-DConv maintains a basis kernel bank $\boldsymbol{\mathcal{K}} \in \mathbb{R}^{b \times O \times K_f \times K_t}$ (with $b$ basis kernels, $O$ output channels, kernel sizes $K_f, K_t$). A transformation coefficient matrix $\mathbf{M} \in \mathbb{R}^{C \times b}$ — produced by [[concepts/topology-aware-coordinate-transformer|TACT]] from $\mathbf{G}$ — linearly combines the basis kernels to yield the dynamic weight:

$$
\mathcal{W}_{dyn}^{(c,o,:,:)} = \sum_{j=1}^{b} M_{c,j} \cdot \mathcal{K}^{(j,o,:,:)}
$$

giving $\boldsymbol{\mathcal{W}}_{dyn} \in \mathbb{R}^{C \times O \times K_f \times K_t}$. After convolution, LayerNorm and PReLU produce the fixed-dimensional output consumed by the downstream fixed-array backend:

$$
\mathbf{Y} = \text{PReLU}\big(\text{LayerNorm}(\text{Geo-DyncConv}(\mathbf{G}, \mathbf{X}))\big)
$$

## Key Properties

- **Variable channel count**: The same learned basis serves any $C$ — the matrix $\mathbf{M}$ adapts the input-channel dimension dynamically.
- **Permutation equivariance**: If $\mathbf{G} \to \mathbf{P}\mathbf{G}$ for a permutation matrix $\mathbf{P}$, then $\mathbf{M} \to \mathbf{P}\mathbf{M}$ (guaranteed by TACT), so $\boldsymbol{\mathcal{W}}_{dyn} \to \mathbf{P}\boldsymbol{\mathcal{W}}_{dyn}$ and the convolution $(\mathbf{P}\mathbf{X}) \circledast (\mathbf{P}\boldsymbol{\mathcal{W}}_{dyn}) = \mathbf{X} \circledast \boldsymbol{\mathcal{W}}_{dyn}$ is invariant. Channel ordering at inference is irrelevant.
- **Universal adapter**: Adding Geo-DConv as a front-end converts a fixed-array backbone into an array-invariant system with negligible overhead (+0.1 M params, +0.09 G/s MACs for SpatialNet).
- **Coordinate system agnostic**: Works with either Cartesian $(x,y,z)$ or spherical $(r,\theta,\phi)$ coordinates; spherical is used by default.
- **Basis dimension controls expressiveness**: $b$ (default 8) regulates how many distinct spatial patterns the kernel bank can express; small $b$ keeps compute low while still outperforming heavier array-agnostic baselines.

## Distinction from Prior Dynamic Convolutions

| Aspect | CV Dynamic Convolution | Adaptive Convolution (Wang 2025) | **Geo-DConv** |
|---|---|---|---|
| Conditioning input | Image features (semantic) | Acoustic features (per-frame) | **Microphone coordinates (geometry)** |
| Temporal scope | Per-image | Per-frame (causal streaming) | **Per-array (time-invariant)** |
| Purpose | Increase kernel expressiveness | Causal frame-wise kernel mixing | **Generalize across array geometries** |
| Domain | Computer vision | Speech enhancement | Multi-channel speech enhancement |

See [[concepts/dynamic-convolution|Dynamic Convolution]] for the CV ancestor and [[concepts/adaptive-convolution|Adaptive Convolution]] for the per-frame SE variant.

## Distinction from Related Array-Agnostic Approaches

| Method | Geometry used? | Channel-count handling | Permutation handling |
|---|---|---|---|
| TAC / TA-C | No | Batch ops + reference/avg | Implicit (batch ops) |
| FOA (First-Order Ambisonics) | No | Fixed 4-channel transform | Requires ≥4 mics |
| UniArray (VME-based) | No | Virtual mic estimation | Requires input-order preprocessing |
| **Geo-DConv** | **Yes (explicit coordinates)** | **Dynamic basis combination** | **Mathematically guaranteed** |

## Typical Hyperparameters

| Parameter | Value | Description |
|:----------|:------|:------------|
| $b$ | 8 | Basis dimension |
| $O$ | 16 | Output channel size |
| $L$ | 6 | Fourier PE frequency bands |
| $d_{\text{hidden}}$ | 64 | TACT hidden dimension |
| TACT layers | 2 | Transformer encoder layers |
| TACT heads | 4 | MHSA heads |
| Coordinate system | Spherical | $(r, \theta, \phi)$ |

## Related Concepts

- [[concepts/topology-aware-coordinate-transformer|Topology-Aware Coordinate Transformer (TACT)]] — produces the transformation matrix $\mathbf{M}$
- [[concepts/array-invariant-speech-enhancement|Array-Invariant Speech Enhancement]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/dynamic-convolution|Dynamic Convolution]] — CV ancestor
- [[concepts/adaptive-convolution|Adaptive Convolution]] — per-frame SE variant
- [[concepts/virtual-microphone-estimation|Virtual Microphone Estimation]] — UniArray alternative
- [[concepts/geometry-conditioned-ssf|Geometry-Conditioned SSF]] — FiLM-based geometry conditioning for target speaker extraction
- [[concepts/mvdr-beamformer|MVDR Beamformer]] — classical geometry-explicit baseline

## Related Sources

- [[sources/liu-2026-array-invariant-speech-enhancement|Liu, Zhang, Li & Qian 2026: Array-Invariant SE via Geo-DConv]]
