---
type: source
created: 2026-07-27
updated: 2026-07-27
sources:
  - raw/papers/liu-2026-array-invariant-speech-enhancement/full-text.md
  - https://doi.org/10.48550/arXiv.2607.18658
  - zotero://select/items/0_REFWW6J4
tags:
  - speech-enhancement
  - multi-channel
  - microphone-arrays
  - array-invariant
  - dynamic-convolution
  - geometry-aware
  - transformer
  - positional-encoding
  - preprint
---

# Liu, Zhang, Li & Qian 2026: Towards Array-Invariant Speech Enhancement via Geometry-Aware Dynamic Convolution

- **Authors**: [[entities/zhenglong-liu|Zhenglong Liu]], [[entities/wangyou-zhang|Wangyou Zhang]], [[entities/chenda-li|Chenda Li]], [[entities/yanmin-qian|Yanmin Qian]]
- **Affiliation**: Auditory Cognition and Computational Acoustics Lab, Shanghai Jiao Tong University; VUI Labs
- **Venue**: arXiv preprint
- **Year**: 2026
- **Type**: Preprint
- **DOI**: [10.48550/arXiv.2607.18658](https://doi.org/10.48550/arXiv.2607.18658)
- **Zotero**: [Open in Zotero](zotero://select/items/0_REFWW6J4)

## Summary

Multi-channel speech enhancement (SE) systems are conventionally tied to a fixed microphone array geometry, blocking cross-device deployment and dataset merging. Existing array-agnostic methods (TAC, USES2, FOA, UniArray) handle variable microphone counts and permutations but **fail to exploit explicit array geometry priors**, leaving a well-known spatial cue on the table. This paper proposes **Geometry-Aware Dynamic Convolution (Geo-DConv)**, a universal front-end that converts any fixed-array SE model into an array-invariant one: microphone coordinates are encoded by Fourier positional encoding, processed by a **Topology-Aware Coordinate Transformer (TACT)** into a transformation matrix, and used to linearly combine a small bank of basis convolution kernels into geometry-specific dynamic weights. The resulting SpatialNet-Geo-DConv and TF-GridNet-Geo-DConv outperform FaSNet-TAC and USES2-comp on RealMAN while using 10× less compute than USES2-comp, and generalize zero-shot to a 6-microphone CHiME-4 array (trained on ≤4 mics), improving DNSMOS OVRL from 1.42 → 2.73.

## Problem Formulation

The signal model operates in the STFT domain. Let $\mathbf{X} \in \mathbb{R}^{C \times F \times T}$ denote the multi-channel acoustic feature (real and imaginary parts of the complex spectrogram concatenated along frequency), where $C$ is the (variable) number of microphones and $F, T$ are frequency and time dimensions. Each microphone $i$ has relative coordinates $\mathbf{g}_i \in \mathbb{R}^3$ (Cartesian $(x,y,z)$ or spherical $(r,\theta,\phi)$), stacked into a coordinate matrix $\mathbf{G} = [\mathbf{g}_1, \dots, \mathbf{g}_C]^\top \in \mathbb{R}^{C \times 3}$. A Geo-DConv layer maps this pair to a fixed-dimensional output:

$$
\text{Out} = \operatorname{Geo-DyncConv}(\mathbf{G}, \mathbf{X})
$$

The core requirement is **permutation equivariance**: if the input channels are permuted as $\mathbf{P}\mathbf{X}$ with corresponding permuted coordinates $\mathbf{P}\mathbf{G}$, the output must be the permuted version of the original output, so the model is insensitive to microphone ordering at inference.

## Methodology

![[raw/papers/liu-2026-array-invariant-speech-enhancement/figures/c82a207e32d645f4b7e2d0af7e70a913d88a8eeca0398c8a6b1a7a73f2e23d40.jpg|Geo-DConv architecture]]

*Figure 1: Architecture of Geo-DConv. Left — Topology-Aware Coordinate Transformer (TACT) consumes Fourier-encoded microphone coordinates and produces a transformation matrix M. Right — dynamic convolution combines basis kernels K via M to produce geometry-specific weights applied to acoustic features.*

### A. Geometry-Aware Dynamic Convolution (Geo-DConv)

A typical convolution kernel is $\boldsymbol{\mathcal{K}} \in \mathbb{R}^{b \times O \times K_f \times K_t}$, where $b$ is the basis dimension, $O$ the fixed output channel size, and $K_f, K_t$ the frequency/time kernel sizes. The dynamic weight for a specific array geometry is a linear combination of the basis kernels guided by a transformation coefficient matrix $\mathbf{M} \in \mathbb{R}^{C \times b}$:

$$
\mathcal{W}_{dyn}^{(c,o,:,:)} = \sum_{j=1}^{b} M_{c,j} \cdot \mathcal{K}^{(j,o,:,:)}
$$

yielding $\boldsymbol{\mathcal{W}}_{dyn} \in \mathbb{R}^{C \times O \times K_f \times K_t}$. The remaining challenge is generating $\mathbf{M}$ from $\mathbf{G}$ in a way that captures global spatial interactions while remaining permutation-equivariant.

### B. Topology-Aware Coordinate Transformer (TACT)

Inspired by Implicit Neural Representations (NeRF, NAF), Fourier Positional Encoding (PE) is applied to each coordinate:

$$
\gamma(\mathbf{g}_i) = \big[\mathbf{g}_i,\; \sin(2^0 \pi \mathbf{g}_i),\; \cos(2^0 \pi \mathbf{g}_i),\; \dots,\; \sin(2^{L-1} \pi \mathbf{g}_i),\; \cos(2^{L-1} \pi \mathbf{g}_i)\big]
$$

with $L$ frequency bands, yielding an encoded matrix $\mathbf{G}_{pe} \in \mathbb{R}^{C \times d_{pe}}$ where $d_{pe} = 3 + 6L$.

The encoded matrix is projected to the hidden dimension $d$ and treated as a sequence of $C$ tokens fed into a Transformer Encoder with Multi-Head Self-Attention (MHSA):

$$
\mathbf{G}^{(0)} = \mathbf{G}_{pe} \mathbf{W}_{in}, \quad \mathbf{W}_{in} \in \mathbb{R}^{d_{pe} \times d_{\text{hidden}}}
$$

$$
\mathbf{Q} = \mathbf{G}^{(l)} \mathbf{W}_Q, \quad \mathbf{K} = \mathbf{G}^{(l)} \mathbf{W}_K, \quad \mathbf{V} = \mathbf{G}^{(l)} \mathbf{W}_V
$$

$$
\mathbf{Z}^{(l+1)} = \text{LayerNorm}\big(\mathbf{Z}^{(l)} + \text{MHSA}(\mathbf{Q}, \mathbf{K}, \mathbf{V})\big)
$$

After $L_{\text{layers}}$ encoding layers, a linear output projection produces the transformation matrix:

$$
\mathbf{M} = \mathbf{Z}^{(L_{\text{layers}})} \mathbf{W}_{out}, \quad \mathbf{W}_{out} \in \mathbb{R}^{d_{\text{hidden}} \times b}
$$

**Permutation Equivariance guarantee**: The point-wise Fourier PE and the permutation-equivariant MHSA together ensure that permuted input coordinates $\mathbf{P}\mathbf{G}$ produce a permuted transformation matrix $\mathbf{P}\mathbf{M}$. The dynamic kernel is correspondingly permuted along its input channel dimension, and the convolution $(\mathbf{P}\mathbf{X}) \circledast (\mathbf{P}\boldsymbol{\mathcal{W}}_{dyn}) = \mathbf{X} \circledast \boldsymbol{\mathcal{W}}_{dyn}$ is mathematically invariant — so the extracted features are stable regardless of input channel ordering.

### C. Overall Architecture and Integration

For compatibility with downstream fixed-array algorithms, Layer Normalization (LN) and PReLU activation are applied:

$$
\mathbf{Y} = \text{PReLU}\big(\text{LayerNorm}(\text{Geo-DyncConv}(\mathbf{G}, \mathbf{X}))\big)
$$

This maps variable-dimensional inputs to a fixed-dimensional output that any conventional fixed-array SE backend (e.g., SpatialNet, TF-GridNet) can consume, transforming it into an array-invariant system.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Dataset** | RealMAN (real-recorded 32-channel microphone array) — 83.7 h speech (64.0/8.1/11.6 train/val/test) + 144.5 h noise (106.3/16.0/22.2 train/val/test); 32 scenes for speech, 31 for noise; indoor/outdoor/semi-outdoor/transportation |
| **Sample rate** | 8 kHz |
| **STFT** | 256-pt window, 128-sample frame shift |
| **Segment length** | 4 s utterances (identical boundaries across all models at test) |
| **Basis dimension $b$** | 8 |
| **Output channels $O$** | 16 |
| **Coordinate system** | Spherical $(r, \theta, \phi)$ |
| **PE frequency bands $L$** | 6 (so $d_{pe} = 3 + 36 = 39$) |
| **TACT hidden dim** | 64 |
| **TACT layers / heads** | 2 layers, 4 heads |
| **Activation / norm** | PReLU + LayerNorm |
| **Single-channel baseline** | BSRNN |
| **Array-agnostic baselines** | FaSNet-TAC, USES2-comp |
| **Fixed-array baselines** | SpatialNet, TF-GridNet |
| **Metrics** | SDR, SI-SDR, PESQ, STOI, DNSMOS (P808, SIG, BAK, OVRL) |
| **Cross-dataset eval** | CHiME-4 (6-mic real-world, never seen during training) |

RealMAN is used specifically to avoid the sim-to-real domain mismatch that plagues simulated multi-channel datasets; the direct-path signal (source filtered through an estimated direct-path propagation filter) serves as the clean target.

## Results

### Table 1 — Performance and efficiency on RealMAN

| No. | Model | Params (M) | MACs (G/s) | SDR | SI-SDR | PESQ | STOI | P808 | SIG | BAK | OVRL |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | No processing | – | – | -2.11 | -9.47 | 1.54 | 0.72 | 2.39 | 1.99 | 1.84 | 1.49 |
| 2 | BSRNN (single-channel) | 16.9 | 21.15 | 5.31 | -1.38 | 1.94 | 0.79 | 2.62 | 2.61 | 3.29 | 2.18 |
| | **Fixed-Array (geometry-specific upper bound)** | | | | | | | | | | |
| 3 | FaSNet-TAC | 2.7 | 9.76 | 5.13 | -1.03 | 1.69 | 0.72 | 2.46 | 2.36 | 3.14 | 1.95 |
| 4 | USES2-comp | 2.5 | 70.26 | 9.36 | 4.78 | 2.56 | 0.87 | 2.77 | 3.14 | 3.49 | 2.65 |
| 5 | SpatialNet | 1.2 | 5.99 | 10.06 | 5.23 | 2.56 | 0.87 | 2.75 | 3.11 | 3.58 | 2.67 |
| 6 | TF-GridNet | 8.2 | 73.03 | 9.77 | 5.29 | 2.72 | 0.88 | 2.84 | 3.13 | 3.63 | 2.71 |
| | **Random 4-Mics Array (training)** | | | | | | | | | | |
| 7 | FaSNet-TAC | 2.7 | 9.76 | 5.82 | -1.09 | 1.72 | 0.73 | 2.46 | 2.41 | 3.04 | 1.95 |
| 8 | USES2-comp | 2.5 | 70.26 | 9.56 | 4.86 | 2.66 | 0.87 | 2.79 | 2.99 | 3.67 | 2.62 |
| 9 | SpatialNet | 1.2 | 5.99 | 9.41 | 3.77 | 2.55 | 0.87 | 2.76 | 3.13 | 3.50 | 2.64 |
| 10 | TF-GridNet | 8.2 | 73.03 | 9.00 | 3.78 | 2.57 | 0.87 | 2.79 | 3.06 | 3.55 | 2.63 |
| 11 | SpatialNet-Geo-DConv (Ours) | 1.3 | 6.08 | 9.77 | 3.92 | 2.46 | 0.87 | 2.73 | 3.19 | 3.28 | 2.59 |
| 12 | TF-GridNet-Geo-DConv (Ours) | 8.3 | 73.12 | 8.83 | 3.56 | 2.46 | 0.87 | 2.77 | 3.03 | 3.50 | 2.59 |
| | **Geometry-Invariant (primary comparison)** | | | | | | | | | | |
| 13 | FaSNet-TAC | 2.7 | 9.76 | 5.76 | -0.81 | 1.74 | 0.73 | 2.48 | 2.48 | 3.18 | 2.05 |
| 14 | USES2-comp | 2.5 | 70.26 | 8.62 | 4.17 | 2.52 | 0.86 | 2.76 | 3.02 | 3.50 | 2.56 |
| 15 | **SpatialNet-Geo-DConv (Ours)** | 1.3 | 6.08 | **9.72** | 4.22 | 2.48 | 0.86 | 2.77 | 3.16 | 3.51 | 2.68 |
| 16 | **TF-GridNet-Geo-DConv (Ours)** | 8.3 | 73.12 | 9.05 | 3.90 | **2.59** | **0.87** | **2.83** | **3.21** | **3.62** | **2.77** |

**Key findings from Table 1**:

- **Fixed vs. random array training (Nos. 3–10)**: Fixed-array methods (SpatialNet, TF-GridNet) lose 1–1.5 dB SDR when trained on random arrays, because they cannot reliably leverage array structure. Array-agnostic methods (FaSNet-TAC, USES2-comp) slightly *benefit* from random-array training as a form of data regularization.
- **Geo-DConv revives fixed-array methods in array-invariant settings (Nos. 13–16)**: SpatialNet-Geo-DConv achieves 9.72 dB SDR vs. USES2-comp's 8.62 dB (+1.10 dB), and TF-GridNet-Geo-DConv achieves the best PESQ (2.59), STOI (0.87), and DNSMOS OVRL (2.77) overall.
- **Efficiency**: SpatialNet-Geo-DConv is essentially tied with USES2-comp on quality while using ~10× fewer MACs (6.08 vs 70.26 G/s).
- **Random mic count training helps (Nos. 11–12 vs 15–16)**: Training with a variable number of microphones further improves performance, suggesting the model learns to generate better dynamic convolution weights when exposed to diverse array sizes.

### Table 2 — Generalization across array topologies and cross-dataset

| Array Config | SI-SDR (dB) | PESQ | OVRL |
|---|---:|---:|---:|
| **USES2-comp** | | | |
| 1 mic: {0} | -4.16 | 1.81 | 1.90 |
| 2 mics: {0,1} | 3.55 | 2.46 | 2.54 |
| 5 mics: {0,1,3,5,7} | 4.91 | 2.60 | 2.59 |
| CHiME-4 (cross-dataset, 6 mics) | – | – | 2.55 |
| **SpatialNet-Geo-DConv (Ours)** | | | |
| 1 mic: {0} | 2.30 | 2.15 | 2.57 |
| 2 mics: {0,1} | 3.97 | 2.45 | 2.66 |
| 5 mics: {0,1,3,5,7} | 4.65 | 2.53 | 2.69 |
| CHiME-4 (cross-dataset, 6 mics) | – | – | 2.64 |
| **TF-GridNet-Geo-DConv (Ours)** | | | |
| 1 mic: {0} | 2.76 | 2.37 | 2.70 |
| 2 mics: {0,1} | 4.12 | 2.62 | 2.77 |
| 5 mics: {0,1,3,5,7} | 4.54 | 2.67 | 2.79 |
| CHiME-4 (cross-dataset, 6 mics) | – | – | 2.73 |

(Unprocessed CHiME-4 OVRL = 1.42; models trained with max 4 mics on RealMAN.)

**Key findings from Table 2**:

- Geo-DConv methods generalize from ≤4-mic training to 5-mic and 6-mic (CHiME-4) arrays without fine-tuning, confirming that the model learns general geometry-aware spatial patterns rather than overfitting to a specific topology.
- At the single-mic extreme, the proposed methods degrade far more gracefully than USES2-comp (SI-SDR of +2.30 / +2.76 vs -4.16 dB), because the underlying fixed-array backbones (SpatialNet, TF-GridNet) are strong single-channel enhancers.
- Cross-dataset transfer to real-recorded CHiME-4 raises DNSMOS OVRL from 1.42 → 2.64 (SpatialNet-Geo-DConv) and 2.73 (TF-GridNet-Geo-DConv), closing most of the gap to the in-domain RealMAN result (2.68 / 2.77).

## Key Contributions

1. **Geo-DConv — explicit array-geometry conditioning via dynamic convolution**: A novel dynamic convolution layer that uses microphone coordinates to generate geometry-specific weights via a linear combination of basis kernels. Unlike prior array-agnostic methods (TAC, USES2, FOA, UniArray), it explicitly injects geometric priors while supporting arbitrary microphone counts and permutations.
2. **TACT — Topology-Aware Coordinate Transformer**: A Transformer-Encoder-based module that consumes Fourier-encoded microphone coordinates and produces the transformation matrix $\mathbf{M}$. Its point-wise PE + permutation-equivariant MHSA design provides a mathematical guarantee of permutation equivariance, ensuring stable outputs under arbitrary input channel ordering — a property previous array-agnostic methods achieve only empirically.
3. **Universal adapter for fixed-array → array-invariant conversion**: Geo-DConv front-ends convert conventional fixed-array models (SpatialNet, TF-GridNet) into array-invariant systems with minimal parameter overhead (+0.1 M params, +0.09 G/s MACs), preserving the strong inductive biases of fixed-array backbones.
4. **Empirical case for explicit geometry in array-invariant SE**: First systematic demonstration that explicit array geometry cues — long exploited in MVDR beamforming and DOA estimation — substantially benefit array-invariant SE when properly injected, closing most of the gap to fixed-array upper bounds.
5. **Real-data training + cross-dataset generalization**: By training on the real-recorded RealMAN corpus (avoiding sim-to-real mismatch) and evaluating zero-shot on CHiME-4 (6-mic, never seen), the paper demonstrates practical deployability across devices — the DNSMOS OVRL on CHiME-4 improves from 1.42 → 2.73.
6. **Efficiency advantage over array-agnostic baselines**: SpatialNet-Geo-DConv matches or exceeds USES2-comp quality at ~10× lower MACs (6.08 vs 70.26 G/s), a significant practical win for resource-constrained deployment.

## Related Concepts

- [[concepts/geometry-aware-dynamic-convolution|Geometry-Aware Dynamic Convolution (Geo-DConv)]]
- [[concepts/topology-aware-coordinate-transformer|Topology-Aware Coordinate Transformer (TACT)]]
- [[concepts/array-invariant-speech-enhancement|Array-Invariant Speech Enhancement]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/dynamic-convolution|Dynamic Convolution]]
- [[concepts/virtual-microphone-estimation|Virtual Microphone Estimation]] — UniArray (a related array-agnostic approach)
- [[concepts/doa-microphone-positional-encoding|DOA-Microphone Positional Encoding]] — related but distinct PE scheme
- [[concepts/geometry-conditioned-ssf|Geometry-Conditioned SSF]] — concurrent geometry-conditioning approach for target speaker extraction
- [[concepts/mvdr-beamformer|MVDR Beamformer]] — traditional geometry-explicit baseline
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]

## Related Synthesis

_No synthesis pages yet — consider creating `synthesis/geometry-aware-multichannel-speech-processing.md` to compare Geo-DConv, GC-SSF, DOA-MPE, and MVDR as geometry-explicit approaches to multi-channel SE / target extraction._

