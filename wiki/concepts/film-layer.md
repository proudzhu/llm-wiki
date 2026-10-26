---
type: concept
created: 2026-05-23
updated: 2026-10-26
sources:
  - raw/papers/perez-2018-film-visual-reasoning/full-text.md
  - raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/full-text.md
  - raw/papers/uphaus-2026-directivity-low-latency/full-text.md
  - raw/papers/yang-2026-direction-preserving-anc/full-text.txt
  - raw/papers/huang-2026-undf-configurable-directivity/full-text.md
  - raw/papers/huang-2026-neural-directional-filtering/full-text.md
  - raw/papers/yuan-2026-open-ear-anc-smart-glasses/full-text.md
  - raw/papers/li-2026-geometry-conditioned-tse/full-text.md
tags:
  - deep-learning
  - neural-networks
  - conditioning
  - feature-modulation
  - visual-reasoning
---

# FiLM Layer

**Feature-wise Linear Modulation (FiLM)** is a conditioning mechanism that modulates intermediate feature maps of a neural network using learned scaling and bias parameters. Originally proposed for visual reasoning tasks ([[sources/perez-2018-film-visual-reasoning|Perez et al. 2018]]), FiLM layers enable flexible conditioning of deep networks on auxiliary information without architectural changes to the base model.

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

In [[concepts/geometry-conditioned-ssf|GC-SSF]], FiLM layers modulate the intermediate features of a [[concepts/spatially-selective-nonlinear-filter|spatially selective filter]] based on array geometry encoded via [[concepts/doa-microphone-positional-encoding|DOA-MPE]]. This enables a single model to generalise across different microphone array configurations. The follow-up by Li & Doclo 2026 ([[sources/li-2026-geometry-conditioned-tse|Li & Doclo 2026]]) keeps the encoder + FiLM integration unchanged and swaps the conditioning feature to propagation-derived spatial features — the [[concepts/target-steering-vector|target steering vector]] or the [[concepts/gcc-phat-spatial-mask|GCC-PHAT spatial mask]] — showing that *what* is encoded (physics-based structure vs. abstract embeddings) matters more than the modulation mechanism itself: both explicit features outperform the abstract MPE embeddings on all metrics (+0.31 PESQ for TSV).

### Directivity-Pattern Conditioning (Neural Directional Filtering)

In [[concepts/film-osn|FiLM-OSN]] (Uphaus et al. 2026), FiLM is the steering mechanism of a low-latency neural directional filter for hearing aids: a 72-dimensional directivity-pattern vector (sampled at 5° intervals) is linearly mapped to the channel dimension ($C=96$), conditioning the narrow-band blocks toward the desired pattern so that the directivity can be adjusted freely at inference. The same mechanism underlies [[concepts/film-jnf|FiLM-JNF]] — introduced for FT-JNF in [[sources/huang-2026-undf-configurable-directivity|Huang, Chetupalli & Habets 2026]] and used for **continuous steering** in the journal-style NDF paper ([[sources/huang-2026-neural-directional-filtering|Huang et al. 2026]]), where a sinusoidal embedding of the steering angle ($d_{\mathrm{emb}}=72$) is mapped by two linear layers to per-feature affine parameters $\boldsymbol{\alpha},\boldsymbol{\beta}\in\mathbb{R}^{512}$. Uphaus et al. use FiLM-JNF as their baseline. Notably, the introducing study shows FiLM is what gives the pattern conditioning its generalization: an initial-state-conditioned variant (PV-JNF) collapses on unseen pattern orders, scalings, and steering directions (e.g., 8.1 vs 19.5 dB SDR on a scaled pattern), while FiLM degrades gracefully.

### Direction-Conditioned Control-Filter Estimation (ANC)

In [[concepts/direction-preserving-anc|DP-ANC]] (Yang et al. 2026), FiLM steers a control-filter **estimation** network rather than a signal filter: a periodic code $[\cos\theta_d, \sin\theta_d]^T$ of the user-specified desired direction is embedded by a small MLP, and a per-block FiLM head maps that embedding to channel-wise $(\gamma_\ell, \beta_\ell)$ that modulate each of three Conv–BN blocks of the acoustic encoder — $h_\ell = \mathrm{ReLU}[(1+\gamma_\ell)\odot u_\ell + \beta_\ell]$ — before the decoder emits the full multichannel FIR ANC control-filter bank. Zero-initializing the FiLM heads makes the initial modulation an identity mapping. This extends FiLM's steering role from neural directional filtering (FiLM-OSN) into active noise control, where the conditioned output is a filter bank rather than an audio signal.

### Secondary-Path Conditioning (Open-Ear ANC)

In [[concepts/virtual-in-ear-sensing|virtual in-ear sensing]] ([[sources/yuan-2026-open-ear-anc-smart-glasses|Yuan, Liu & Xiao 2026]]), FiLM makes the filter-estimation network user-adaptive without retraining: the wearer's 1024-tap secondary-path estimate (from an ESS sweep) is FFT-transformed and compressed by a small MLP into a 128-d embedding, from which a FiLM head produces the scale/bias pair $(\gamma, \beta)$ modulating the U-Net's LSTM bottleneck — the shared network weights stay fixed while the modulation tailors the estimated 2048-tap ANC control filters to each wearer's acoustic anatomy. The entire user-specific state is the ~512-byte secondary-path estimate, versus the ~16 MB of network weights that per-user retraining would require. With calibrated secondary paths the open-ear system gains +1.6 dB mean reduction and inter-user variability shrinks from 1.5 dB to 0.4 dB std.

### Visual Reasoning (Original Application)

FiLM was introduced by [[sources/perez-2018-film-visual-reasoning|Perez et al. 2018 (AAAI)]] for visual reasoning — answering multi-step questions about images. A [[concepts/gated-recurrent-unit|GRU]] question encoder (4096 hidden units) forms the FiLM generator: its final hidden state is projected to $(\boldsymbol{\gamma}, \boldsymbol{\beta})$ pairs, one per residual block of a CNN visual pipeline that classifies an answer over 28 candidates. In the paper's original notation:

$$\mathrm{FiLM}(\mathbf{F}_{i,c} \mid \gamma_{i,c}, \beta_{i,c}) = \gamma_{i,c}\,\mathbf{F}_{i,c} + \beta_{i,c},$$

with $\gamma_{i,c}, \beta_{i,c}$ predicted per feature map $c$ from the conditioning input $\mathbf{x}_i$. This roughly **halved the state-of-the-art error on the CLEVR benchmark** (4.5% → 2.3%, 97.7% accuracy, above human 92.6%) without program supervision or reasoning-specific architectures, beating modular networks (PG+EE) and Relation Networks.

Key findings about the mechanism itself:
- **γ dominates β**: replacing γ with training-mean values at test time costs 65.4% accuracy, β only 1.0%; unrestricted scaling (large magnitudes, negation, zeroing) is essential — bounding γ to (0,1) or (−1,1) hurts as much as removing conditioning.
- **Selective feature-map gating**: γ histograms peak sharply at 0 (feature maps shut off), with a selective set of high-|γ| upregulated maps; 36% of γ and 76% of β values are negative, giving selective thresholding against the following ReLU.
- **Emergent modularity**: t-SNE of (γ, β) clusters by reasoning function — low-level functions in the first FiLM layer, high-level in the last — a function-based modularity learned without any architectural prior.
- **Implicit spatial attention**: globally-pooled classifier features localize on question-relevant objects; feature modulation indirectly yields spatial modulation (a plausible reason FiLM beats Stacked Attention by 21%).
- **Decoupled from normalization**: FiLM works at many positions inside a residual block, not only right after a normalization layer — generalizing and relaxing Conditional Normalization (Conditional Instance Norm, Conditional Batch Norm, Adaptive Instance Norm), whose affine parameters are exactly FiLM with fixed placement.
- **Resolution-independent cost**: two parameters per feature map, independent of image resolution — unlike attention or Relation Networks (quadratic in spatial resolution).
- **Analogy-making in parameter space**: linear combinations of questions' (γ, β) vectors ("cyan spheres" + "brown cubes" − "brown spheres" ≈ "cyan cubes") enable zero-shot generalization to unseen attribute combinations.

FiLM was later adopted as the standard conditioning mechanism in audio and speech processing — steering directivity patterns ([[concepts/film-osn|FiLM-OSN]], [[concepts/film-jnf|FiLM-JNF]]), conditioning extraction networks on speaker clues ([[concepts/target-speaker-extraction|TSE]] fusion layers), and adapting filter-estimation networks to users and directions ([[concepts/direction-preserving-anc|DP-ANC]], [[concepts/virtual-in-ear-sensing|virtual in-ear sensing]]).

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
- [[concepts/target-steering-vector|Target Steering Vector (TSV) Feature]] — propagation-based conditioning input to a FiLM geometry-conditioning branch
- [[concepts/gcc-phat-spatial-mask|GCC-PHAT Spatial Mask]] — signal-dependent conditioning input to a FiLM geometry-conditioning branch
- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/film-osn|FiLM-OSN]]
- [[concepts/film-jnf|FiLM-JNF]]
- [[concepts/undf|UNDF]] — the user-defined-pattern conditioning task introduced by the FiLM-JNF study
- [[concepts/td-speakerbeam|TD-SpeakerBeam]]
- [[concepts/angle-feature|Angle Feature]]
- [[concepts/virtual-in-ear-sensing|Virtual In-Ear Sensing]] — FiLM conditions filter estimation on the wearer's secondary-path embedding (~512 bytes/user instead of retraining)

## Related Sources

- [[sources/perez-2018-film-visual-reasoning|Perez, Strub, de Vries, Dumoulin & Courville 2018: FiLM: Visual Reasoning with a General Conditioning Layer]] — the original paper introducing FiLM: formulation, CLEVR results (97.7%, halving SOTA error), γ/β analysis, ablations, and the zero-shot linear-combination method
- [[sources/li-2026-geometry-conditioned-ssanc|Li 2026: Geometry-Conditioned Spatially Selective Non-Linear Filter]]
- [[sources/li-2026-geometry-conditioned-tse|Li & Doclo 2026: Geometry-Conditioned Target Speaker Extraction with Spatial Features]] — swaps the FiLM conditioning input from MPE embeddings to propagation-derived spatial features
- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova et al. 2023: Neural Target Speech Extraction: An Overview]]
- [[sources/uphaus-2026-directivity-low-latency|Uphaus et al. 2026: Directivity-Conditioned Low-Latency Neural Filtering]] — FiLM steers directivity patterns in the 10 ms-latency FiLM-OSN
- [[sources/huang-2026-undf-configurable-directivity|Huang, Chetupalli & Habets 2026: UNDF]] — the introducing study of FiLM-JNF pattern conditioning; FiLM vs initial-state conditioning generalization comparison
- [[sources/huang-2026-neural-directional-filtering|Huang et al. 2026: Neural Directional Filtering with a Compact Microphone Array]] — FiLM-JNF: sinusoidal angle embedding mapped to per-feature affine parameters for continuous steering
- [[sources/yang-2026-direction-preserving-anc|Yang et al. 2026: Direction-Preserving ANC]] — FiLM conditions control-filter estimation on the desired direction
- [[sources/yuan-2026-open-ear-anc-smart-glasses|Yuan, Liu & Xiao 2026: Active Noise Cancellation on Open-Ear Smart Glasses]] — FiLM secondary-path conditioning: 1024-tap ESS estimate → MLP embedding → (γ, β) modulating the LSTM bottleneck, ~512 bytes/user vs ~16 MB retraining
