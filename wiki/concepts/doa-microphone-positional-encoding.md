---
type: concept
created: 2026-05-23
updated: 2026-07-27
tags:
  - positional-encoding
  - microphone-arrays
  - spatial-features
  - deep-learning
---

# DOA-Microphone Positional Encoding

**DOA-Microphone Positional Encoding (DOA-MPE)** is a feature representation that jointly encodes microphone array geometry and target direction-of-arrival (DOA) for neural network processing. It extends the Microphone Positional Encoding (MPE) scheme by appending a DOA-specific feature vector, enabling the network to learn spatial relationships between microphone positions and the target source.

## Microphone Positional Encoding (MPE)

The MPE encodes each microphone's position using polar coordinates $(\varphi_m, d_m)$ relative to the array centroid:

$$\mathbf{p}_m = \alpha \, d_m \begin{bmatrix} \cos(2\pi\sigma\mathbf{v} + \varphi_m) \\ \sin(2\pi\sigma\mathbf{v} + \varphi_m) \end{bmatrix} \in \mathbb{R}^K,$$

where $\mathbf{v} = \frac{2}{K}[0, 1, \ldots, \frac{K}{2}-1]^T$ is a constant vector, and $\alpha$, $\sigma$, $K$ are hyperparameters. The sinusoidal features explicitly reflect phase-related relationships between microphones critical for spatial filtering.

Stacking all $M$ microphones:

$$\mathbf{P}_{\text{MPE}} = [\mathbf{p}_1, \mathbf{p}_2, \ldots, \mathbf{p}_M] \in \mathbb{R}^{K \times M}.$$

## DOA-MPE Extension

While $\mathbf{P}_{\text{MPE}}$ characterises the array geometry, it does not explicitly capture the spatial relationship between microphone positions and the target source. DOA-MPE augments this with a DOA feature:

$$\mathbf{P}_{\text{DOA-MPE}} = [\mathbf{P}_{\text{MPE}}, \mathbf{p}_{\text{DOA}}] \in \mathbb{R}^{K \times (M+1)},$$

where

$$\mathbf{p}_{\text{DOA}} = \alpha \begin{bmatrix} \cos(2\pi\sigma\mathbf{v} + \theta) \\ \sin(2\pi\sigma\mathbf{v} + \theta) \end{bmatrix} \in \mathbb{R}^K,$$

and $\theta$ is the target DOA defined relative to the same reference axis as the microphone azimuth angles.

**Note**: The distance to the target speaker is typically unknown, so only the angular component $\theta$ is included in $\mathbf{p}_{\text{DOA}}$.

## Key Properties

- **No learnable parameters**: Sinusoidal encoding is fixed, reducing overfitting risk
- **Phase-aware**: Captures inter-microphone phase relationships critical for spatial filtering
- **Joint representation**: Explicitly models the spatial relationship between array geometry and target direction
- **Superior to coordinate concatenation**: Sinusoidal features outperform simple coordinate concatenation

## Typical Hyperparameters

| Parameter | Value | Description |
|:----------|:------|:------------|
| $\alpha$ | 7 | Scaling factor |
| $\sigma$ | 4 | Frequency scaling |
| $K$ | 514 | Feature dimension |

## Applications

- [[concepts/geometry-conditioned-ssf|Geometry-Conditioned SSF]] for [[concepts/target-speaker-extraction|target speaker extraction]]
- [[concepts/direction-of-arrival-estimation|DOA estimation]] with geometry-invariant networks
- Blind speaker separation with ad-hoc microphone arrays

## Related Concepts

- [[concepts/geometry-conditioned-ssf|Geometry-Conditioned SSF (GC-SSF)]]
- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/topology-aware-coordinate-transformer|Topology-Aware Coordinate Transformer (TACT)]] — alternative microphone-coordinate encoding for SE (no DOA, Cartesian/spherical, Transformer-driven)

## Related Sources

- [[sources/li-2026-geometry-conditioned-ssanc|Li 2026: Geometry-Conditioned Spatially Selective Non-Linear Filter]]
- [[sources/liu-2026-array-invariant-speech-enhancement|Liu, Zhang, Li & Qian 2026: Array-Invariant SE via Geo-DConv]]
