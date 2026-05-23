---
type: concept
created: 2026-05-23
updated: 2026-05-23
tags:
  - deep-learning
  - spatial-filtering
  - target-speaker-extraction
  - microphone-arrays
---

# Spatially Selective Non-Linear Filter

**Spatially Selective Non-Linear Filter (SSF)** is a deep-learning-based spatial filter for [[concepts/target-speaker-extraction|target speaker extraction]] that uses the target direction-of-arrival (DOA) as a spatial cue. Proposed by Tesch & Gerkmann (2024), the SSF employs LSTM layers to estimate a complex-valued mask applied to a reference microphone signal, extracting the target speaker from a multi-channel mixture.

## Signal Model

In the STFT domain, the multi-channel observed signal is:

$$\mathbf{Y}(f,t) = \mathbf{X}(f,t) + \mathbf{V}(f,t),$$

where $\mathbf{Y}(f,t) \in \mathbb{C}^M$ stacks signals from $M$ microphones, $\mathbf{X}(f,t)$ is the target speech, and $\mathbf{V}(f,t)$ is interference.

The SSF estimates a complex mask $\mathcal{M}(f,t)$ applied to the reference microphone:

$$\hat{X}_1(f,t) = \mathcal{M}(f,t) \, Y_1(f,t).$$

## Architecture

The SSF comprises two LSTM layers:

1. **Frequency-domain LSTM (F-LSTM)**: Encodes spatial and spectral information from $\mathbf{Y}(f,t)$ into high-dimensional features
2. **Time-domain LSTM (T-LSTM)**: Models temporal dependencies across time frames
3. **Linear output layer**: Produces the complex mask $\mathcal{M}(f,t)$

**DOA conditioning**: The target DOA $\theta$ is mapped to a 180-dimensional one-hot vector (2° resolution) and projected via a linear layer to initialise the F-LSTM cell state.

## Limitations

- **Geometry dependency**: Learned features are tied to the training array geometry
- **Mismatched geometry degradation**: Performance drops significantly when evaluated on different array configurations
- **No explicit geometry representation**: The network cannot adapt to unseen geometries without retraining

## Extensions

### Geometry-Conditioned SSF (GC-SSF)

The [[concepts/geometry-conditioned-ssf|GC-SSF]] addresses the geometry dependency by adding a [[concepts/film-layer|FiLM]]-based conditioning branch driven by [[concepts/doa-microphone-positional-encoding|DOA-MPE]] features. This enables a single model trained on random arrays to generalise across circular, ULA, and random geometries.

## Comparison with Related Methods

| Method | Spatial cue | Adaptation | Geometry handling |
|:-------|:------------|:-----------|:------------------|
| [[concepts/beamforming\|Beamforming]] | Array geometry | Often online | Explicit |
| SSF | Target DOA | None | Tied to training |
| [[concepts/geometry-conditioned-ssf\|GC-SSF]] | Target DOA + geometry | None | Explicit conditioning |
| [[concepts/spatially-selective-anc\|SSANC]] | Target direction (ReIRs) | Typically offline | Explicit (control-theoretic) |

## Related Concepts

- [[concepts/geometry-conditioned-ssf|Geometry-Conditioned SSF (GC-SSF)]]
- [[concepts/doa-microphone-positional-encoding|DOA-Microphone Positional Encoding (DOA-MPE)]]
- [[concepts/film-layer|FiLM Layer]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/spatially-selective-anc|Spatially Selective ANC]]

## Related Sources

- [[sources/li-2026-geometry-conditioned-ssanc|Li 2026: Geometry-Conditioned Spatially Selective Non-Linear Filter]]
