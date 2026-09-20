---
type: concept
created: 2026-05-23
updated: 2026-09-20
sources:
  - raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/full-text.md
  - raw/papers/uphaus-2026-directivity-low-latency/full-text.md
tags:
  - deep-learning
  - neural-networks
  - conditioning
  - feature-modulation
---

# FiLM Layer

**Feature-wise Linear Modulation (FiLM)** is a conditioning mechanism that modulates intermediate feature maps of a neural network using learned scaling and bias parameters. Originally proposed for visual reasoning tasks (Perez et al. 2018), FiLM layers enable flexible conditioning of deep networks on auxiliary information without architectural changes to the base model.

## Formulation

Given intermediate feature maps $\mathbf{O}(t)$ at time frame $t$, a FiLM layer applies:

$$\text{FiLM}(\mathbf{O}(t)) = \mathbf{W} \odot \mathbf{O}(t) + \mathbf{B},$$

where:
- $\mathbf{W}$ is the scaling matrix (element-wise multiplication)
- $\mathbf{B}$ is the bias matrix (element-wise addition)
- $\odot$ denotes element-wise (Hadamard) product

The conditioning parameters are estimated by an encoder from the conditioning input:

$$\begin{bmatrix} \mathbf{W} \\ \mathbf{B} \end{bmatrix} = \text{Encoder}(\mathbf{P}),$$

where $\mathbf{P}$ is the conditioning feature (e.g., [[concepts/doa-microphone-positional-encoding|DOA-MPE]]).

## Key Properties

- **Feature-wise modulation**: Each feature channel is scaled and shifted independently
- **Time-invariant or time-varying**: Parameters can be static (e.g., for fixed geometry) or dynamic (e.g., for moving sources)
- **Lightweight**: Adds minimal computational overhead to the base network
- **Flexible injection**: Can be applied at multiple points in the network pipeline

## Applications in Audio Processing

### Geometry-Conditioned Spatial Filtering

In [[concepts/geometry-conditioned-ssf|GC-SSF]], FiLM layers modulate the intermediate features of a [[concepts/spatially-selective-nonlinear-filter|spatially selective filter]] based on array geometry encoded via [[concepts/doa-microphone-positional-encoding|DOA-MPE]]. This enables a single model to generalise across different microphone array configurations.

### Directivity-Pattern Conditioning (Neural Directional Filtering)

In [[concepts/film-osn|FiLM-OSN]] (Uphaus et al. 2026), FiLM is the steering mechanism of a low-latency neural directional filter for hearing aids: a 72-dimensional directivity-pattern vector (sampled at 5° intervals) is linearly mapped to the channel dimension ($C=96$), conditioning the narrow-band blocks toward the desired pattern so that the directivity can be adjusted freely at inference. The same mechanism was introduced for FT-JNF by the FiLM-JNF (Huang, Chetupalli & Habets 2025, arXiv:2510.20253), which Uphaus et al. use as their baseline.

### Visual Reasoning (Original Application)

FiLM was originally proposed for visual question answering, where image features are conditioned on natural language questions.

## Comparison with Other Conditioning Methods

| Method | Mechanism | Computational cost | Flexibility |
|:-------|:----------|:-------------------|:------------|
| Concatenation | Append conditioning to input | Low | Limited |
| Attention | Cross-attention between features | High | High |
| **FiLM** | **Element-wise scale + bias** | **Low** | **High** |
| Adaptive normalisation | Modulate normalisation statistics | Medium | Medium |

## Use in Target Speech Extraction (TSE)

Zmolikova et al. 2023 [[sources/zmolikova-2023-neural-target-speech-extraction-overview|(Zmolikova 2023)]] survey five widely used **fusion layers** for conditioning a [[concepts/target-speaker-extraction|TSE]] speech-extraction module on a clue embedding $\mathbf{E}_{s}$, with FiLM being one of them:

| Fusion type | Equation | Parameters |
|:-----------|:---------|:-----------|
| Concatenation | $\mathbf{Z}_{s} = [\mathbf{Z}_{y}, \mathbf{E}_{s}]$ | — |
| Addition | $\mathbf{Z}_{s} = \mathbf{Z}_{y} + \mathbf{L}\mathbf{E}_{s}$ | $\mathbf{L} \in \mathbb{R}^{D^{Z} \times D^{\mathrm{Emb}}}$ |
| Multiplication | $\mathbf{Z}_{s} = \mathbf{Z}_{y} \odot (\mathbf{L}\mathbf{E}_{s})$ | $\mathbf{L} \in \mathbb{R}^{D^{Z} \times D^{\mathrm{Emb}}}$ |
| **FiLM** | $\mathbf{Z}_{s} = \mathbf{Z}_{y} \odot (\mathbf{L}_{1}\mathbf{E}_{s}) + \mathbf{L}_{2}\mathbf{E}_{s}$ | $\mathbf{L}_{1}, \mathbf{L}_{2} \in \mathbb{R}^{D^{Z} \times D^{\mathrm{Emb}}}$ |
| Factorized layer | $\mathbf{Z}_{s} = \sum_{i=1}^{D^{\mathrm{Emb}}} \mathbf{L}_{i}\mathbf{Z}_{y} \mathrm{diag}(\mathbf{e}_{i})$ | $\mathbf{L}_{i} \in \mathbb{R}^{D^{Z} \times D^{Z}}$ |

The review reports that, in TSE settings, the choice of fusion layer has "rather insignificant" impact on performance, with **multiplication and FiLM generally performing well**. Best results come from placing a fusion layer in the lower part of the extraction module (shallow mixture encoder + deep extractor). Attention-based fusion [40] is an alternative that supports dynamic per-clue reliability weighting for multi-clue (e.g., audio-visual) TSE.

## Related Concepts

- [[concepts/geometry-conditioned-ssf|Geometry-Conditioned SSF (GC-SSF)]]
- [[concepts/doa-microphone-positional-encoding|DOA-Microphone Positional Encoding (DOA-MPE)]]
- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/film-osn|FiLM-OSN]]
- [[concepts/td-speakerbeam|TD-SpeakerBeam]]
- [[concepts/angle-feature|Angle Feature]]

## Related Sources

- [[sources/li-2026-geometry-conditioned-ssanc|Li 2026: Geometry-Conditioned Spatially Selective Non-Linear Filter]]
- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova et al. 2023: Neural Target Speech Extraction: An Overview]]
- [[sources/uphaus-2026-directivity-low-latency|Uphaus et al. 2026: Directivity-Conditioned Low-Latency Neural Filtering]] — FiLM steers directivity patterns in the 10 ms-latency FiLM-OSN
