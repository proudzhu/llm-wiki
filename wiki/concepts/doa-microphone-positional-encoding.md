---
type: concept
created: 2026-05-23
updated: 2026-10-27
sources:
  - raw/papers/baek-2025-geometry-invariant-doa-estimation/full-text.md
  - raw/papers/li-2026-geometry-conditioned-tse/full-text.md
tags:
  - positional-encoding
  - microphone-arrays
  - spatial-features
  - deep-learning
---

# DOA-Microphone Positional Encoding

**DOA-Microphone Positional Encoding (DOA-MPE)** is a feature representation that jointly encodes microphone array geometry and target direction-of-arrival (DOA) for neural network processing. It extends the Microphone Positional Encoding (MPE) scheme by appending a DOA-specific feature vector, enabling the network to learn spatial relationships between microphone positions and the target source.

## Origin: MPE for Geometry-Invariant DOA Estimation (Baek, Chang & Cohen 2025)

[[sources/baek-2025-geometry-invariant-doa-estimation|Baek, Chang & Cohen 2025]] introduced MPE to give a **geometry-invariant DOA network** explicit microphone coordinates without reverting to pair-wise SRP-PHAT/GCC-PHAT features. Their formulation is fully **three-dimensional and spherical** — each microphone contributes distance $r_c$, azimuth $\theta_c$ and elevation $\phi_c$ — and comes in two modulation variants, with $\mathbf{v} = \frac{4}{M}[0, 1, \ldots, \frac{M}{4}-1]^{\top} \in \mathbb{R}^{M/4}$:

$$\mathcal{P}_c^{\mathrm{PM}} = \alpha r_c \begin{bmatrix} \cos(2\pi\beta\mathbf{v} + \theta_c) \\ \sin(2\pi\beta\mathbf{v} + \theta_c) \\ \cos(2\pi\beta\mathbf{v} + \phi_c) \\ \sin(2\pi\beta\mathbf{v} + \phi_c) \end{bmatrix}, \qquad
\mathcal{P}_c^{\mathrm{FM}} = \alpha r_c \begin{bmatrix} \cos(\theta_c \beta \mathbf{v}) \\ \sin(\theta_c \beta \mathbf{v}) \\ \cos(\phi_c \beta \mathbf{v}) \\ \sin(\phi_c \beta \mathbf{v}) \end{bmatrix}$$

- **PM** shifts the phase of the sinusoid by the angle; **FM** scales its oscillation rate by the angle; the distance $r_c$ acts as amplitude scaling.
- Hyperparameters in the original system: $\alpha = 7$, $\beta = 4$, $M = 128$ (latent width), with $0 < \beta < M/8$ to avoid aliasing and keep positions distinguishable.
- The Appendix proves a **linearity + relative-position property**: MPEs of two microphones are related by a block-diagonal transform built from rotation blocks $\boldsymbol{\Omega}_m = \frac{r_q}{r_p}\begin{bmatrix}\cos\omega_m & -\sin\omega_m \\ \sin\omega_m & \cos\omega_m\end{bmatrix}$ where $\omega_m = \theta_q - \theta_p$ (PM) or $\omega_m = (\theta_q-\theta_p)\beta v_m$ (FM) — i.e. the encoding depends on **relative** azimuth difference and distance ratio, not absolute position.
- **Ablation evidence**: replacing MPE with a trainable linear encoder of the same width (MLE) diverges as soon as the array geometry becomes dynamic, and adding the raw coordinates to the first feature elements fails too — the fixed sinusoidal form, not merely the presence of coordinates, is what makes learning work.

Downstream geometry-conditioned systems (see the SE-side formulation below) reuse the scheme in a reduced form: two polar coordinates $(\varphi_m, d_m)$, only the angular part for the target DOA, and a per-microphone vector of length $K$ rather than the four-way $M$-block of the original.

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

## Comparison with Propagation-Derived Spatial Features

Li & Doclo 2026 ([[sources/li-2026-geometry-conditioned-tse|Li & Doclo 2026]]) show that MPE-style abstract encodings are not the last word in geometry conditioning: replacing $\mathbf{P}_{\text{MPE}}$ with the [[concepts/target-steering-vector|target steering vector]] (conjugate steering vectors stacked over frequency) improves the same GCSSF system from 7.77 to 9.43 dB SI-SDR (2.27 vs. 1.96 PESQ) on random arrays. The sinusoidal encoding provides coordinates but leaves the network to *implicitly learn* the phase-DOA-geometry relationship; the steering vector hands it over explicitly. The residual advantage of MPE: it degrades more gracefully under target-DOA errors beyond 20°, where propagation-derived features suffer severe phase mismatch.

## Related Concepts

- [[concepts/geometry-conditioned-ssf|Geometry-Conditioned SSF (GC-SSF)]]
- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]
- [[concepts/target-steering-vector|Target Steering Vector (TSV) Feature]] — the propagation-based alternative that empirically outperforms MPE
- [[concepts/gcc-phat-spatial-mask|GCC-PHAT Spatial Mask]] — the signal-dependent alternative
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/topology-aware-coordinate-transformer|Topology-Aware Coordinate Transformer (TACT)]] — alternative microphone-coordinate encoding for SE (no DOA, Cartesian/spherical, Transformer-driven)
- [[concepts/complexity-gradual-training|Complexity Gradual Training (CGT)]] — the training scheme that makes MPE-conditioned networks converge on mixed geometries
- [[concepts/multi-stage-geometry-learning|Multi-Stage Geometry Learning (MSGL)]] — the fixed → dynamic → variable-count array curriculum

## Related Sources

- [[sources/li-2026-geometry-conditioned-ssanc|Li 2026: Geometry-Conditioned Spatially Selective Non-Linear Filter]]
- [[sources/li-2026-geometry-conditioned-tse|Li & Doclo 2026: Geometry-Conditioned Target Speaker Extraction with Spatial Features]] — benchmarks MPE against propagation-derived spatial features
- [[sources/liu-2026-array-invariant-speech-enhancement|Liu, Zhang, Li & Qian 2026: Array-Invariant SE via Geo-DConv]]
- [[sources/baek-2025-geometry-invariant-doa-estimation|Baek, Chang & Cohen 2025: DNN-Based Geometry-Invariant DOA Estimation]] — the origin of MPE: 3-D spherical PM/FM variants, linearity/relative-position proof, and the MLE divergence ablation
