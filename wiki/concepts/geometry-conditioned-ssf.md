---
type: concept
created: 2026-05-23
updated: 2026-07-27
tags:
  - deep-learning
  - spatial-filtering
  - microphone-arrays
  - target-speaker-extraction
  - geometry-conditioning
---

# Geometry-Conditioned Spatially Selective Non-Linear Filter

**Geometry-Conditioned SSF (GC-SSF)** extends the baseline [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]] by incorporating explicit array geometry information via a [[concepts/film-layer|FiLM]]-based conditioning branch. This enables robust [[concepts/target-speaker-extraction|target speaker extraction]] across different microphone array geometries without retraining.

## Motivation

The baseline SSF learns intermediate features tied to the training array geometry. When evaluated on mismatched geometries, performance degrades significantly. GC-SSF addresses this by conditioning the filter on the array geometry, allowing a single model trained on random arrays to generalise across circular, ULA, and random configurations.

## Architecture

The GC-SSF comprises two main components:

1. **Baseline SSF**: Two LSTM layers (F-LSTM for spectral-spatial encoding, T-LSTM for temporal modelling) that estimate a complex-valued mask conditioned on the target DOA
2. **Geometry-conditioning branch**: A Conv1d encoder that processes [[concepts/doa-microphone-positional-encoding|DOA-MPE]] features and modulates the SSF's intermediate feature maps via [[concepts/film-layer|FiLM layers]]

The conditioning parameters (scaling matrix $\mathbf{W}$ and bias matrix $\mathbf{B}$) are time-invariant, as the array geometry and target DOA are assumed static:

$$\text{FiLM}(\mathbf{O}(t)) = \mathbf{W} \odot \mathbf{O}(t) + \mathbf{B},$$

where $\mathbf{O}(t)$ is the intermediate feature map at time frame $t$.

## Points of Injection

The conditioning can be applied at three locations in the SSF pipeline:

| POI | Location | Effect |
|:----|:---------|:-------|
| 1 | After F-LSTM | Modulates spectral-spatial features |
| 2 | After T-LSTM input | Modulates temporal features (best performance) |
| 3 | After T-LSTM output | Late-stage injection (lower performance) |

**Optimal configuration**: DOA-MPE at POI 2 achieves the highest PESQ scores.

## Key Properties

- **Geometry generalisation**: Trained on random arrays, GC-SSF achieves competitive performance on circular, ULA, and random geometries
- **Spatial selectivity**: Maintains high sensitivity to target DOA errors, comparable to geometry-specific baselines
- **No fine-tuning required**: Single model works across geometries without per-array adaptation

## Comparison with Related Approaches

| Approach | Geometry handling | Adaptation | Target extraction |
|:---------|:------------------|:-----------|:------------------|
| Baseline SSF (fixed geometry) | Tied to training geometry | None | DOA-based |
| Meta-learning SSF | Per-geometry fine-tuning | Few-shot | DOA-based |
| Geometry-agnostic systems | Geometry-invariant by design | None | Blind separation |
| **GC-SSF** | **Explicit conditioning** | **None** | **DOA-based** |

## Related Concepts

- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]
- [[concepts/doa-microphone-positional-encoding|DOA-Microphone Positional Encoding (DOA-MPE)]]
- [[concepts/film-layer|FiLM Layer]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/geometry-aware-dynamic-convolution|Geometry-Aware Dynamic Convolution (Geo-DConv)]] — sibling geometry-conditioning approach for SE (vs. GC-SSF for target-speaker extraction); uses [[concepts/topology-aware-coordinate-transformer|TACT]] + dynamic-kernel basis instead of FiLM, and is permutation-equivariant

## Related Sources

- [[sources/li-2026-geometry-conditioned-ssanc|Li 2026: Geometry-Conditioned Spatially Selective Non-Linear Filter]]
- [[sources/liu-2026-array-invariant-speech-enhancement|Liu, Zhang, Li & Qian 2026: Array-Invariant SE via Geo-DConv]]
