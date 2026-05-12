---
type: source
created: 2026-05-12
updated: 2026-05-12
sources:
  - raw/papers/lee-2026-spatial-magnifier-spatial-upsampling/full-text.md
  - https://doi.org/10.48550/arXiv.2605.04749
  - zotero://select/items/0_KC7HJ7T3
tags:
  - speech-enhancement
  - virtual-microphone
  - spatial-upsampling
  - beamforming
  - gan
---

# Lee, Pandey, Parekh, Wong, Donley, Xu & Azcarreta 2026: Spatial-Magnifier

**Authors**: [[../entities/dongheon-lee|Dongheon Lee]]¹², [[../entities/ashutosh-pandey|Ashutosh Pandey]]¹, [[../entities/sanjeel-parekh|Sanjeel Parekh]]¹, [[../entities/daniel-wong|Daniel Wong]]¹, [[../entities/jacob-donley|Jacob Donley]]¹, [[../entities/buye-xu|Buye Xu]]¹, [[../entities/juan-azcarreta|Juan Azcarreta]]¹

**Affiliations**: ¹Meta Reality Labs Research, ²KAIST

**Published**: arXiv preprint, 2026-05-06

**Type**: Preprint (5 pages, 2 figures, 4 tables)

**DOI**: [10.48550/arXiv.2605.04749](https://doi.org/10.48550/arXiv.2605.04749)

**arXiv**: [2605.04749](https://arxiv.org/abs/2605.04749)

**Zotero**: [KC7HJ7T3](zotero://select/items/0_KC7HJ7T3)

## Summary

Proposes Spatial-Magnifier, a GAN-based neural network for spatial upsampling that generates virtual microphone (VM) signals from a limited set of real microphone (RM) measurements. Introduces the Spatial Audio Representation Learning (SARL) framework, which conditions downstream speech enhancement on both estimated VM signals and features. The method nearly recovers oracle performance when all microphones are available, outperforming existing Neural-VME baselines across beamforming and end-to-end enhancement tasks with lower computational cost.

## Problem Formulation

Multichannel speech enhancement (MC-SE) estimates a direct-path speech signal $\mathbf{x}_{ref} \in \mathbb{R}^{1 \times N}$ given noisy multichannel input $\mathbf{y} \in \mathbb{R}^{M \times N}$:

$$\mathbf{y} = \mathbf{x} + \mathbf{x}_{rev} + \mathbf{n}$$

where $\mathbf{x}$, $\mathbf{x}_{rev}$, and $\mathbf{n}$ denote direct-path speech, reverberation, and noise across $M$ channels. Physical constraints on consumer devices (AR glasses, earbuds, hearing aids) limit the number of microphones, reducing spatial diversity and degrading beamforming performance.

**Neural-VME task**: Given RM signals $\mathbf{r} \in \mathbb{R}^{M_r \times N}$, estimate VM signals $\hat{\mathbf{v}} \in \mathbb{R}^{M_v \times N}$:

$$\hat{\mathbf{v}} = \text{Neural-VME}(\mathbf{r})$$

The augmented signal $\bar{\mathbf{y}} = [\mathbf{r}, \hat{\mathbf{v}}]$ increases the effective array size from $M_r$ to $M = M_r + M_v$.

## Methodology

### Spatial-Magnifier Architecture

![Spatial-Magnifier generator architecture](raw/papers/lee-2026-spatial-magnifier-spatial-upsampling/figures/fig1-spatial-magnifier.png)

*Figure 1: Architecture of the Spatial-Magnifier generator. The network jointly generates VM signals and VM features.*

A GAN-based generative network inspired by the Deep Back-Projection Network (DBPN) for image super-resolution:

1. **Input**: RM signals $\mathbf{R} \in \mathbb{C}^{M_r \times T \times F}$ in the frequency domain, treating microphone indices as channel dimension with concatenated real/imaginary components
2. **Initial 2D convolution**: Expands input from $2 \times M_r$ to $D_1$ channels
3. **$N_b$ stages** of alternating up-blocks, down-blocks, and DCA modules with channel dimensions $[D_1, \ldots, D_5] = [128, 96, 64, 48, 32]$

**Key modules**:

| Module | Function | Overhead |
|:-------|:---------|:---------|
| Selection Module (SM) | Pointwise convolution + Mish activation gating before addition; extracts channel-wise adaptive features | +0.1M params, +0.1 GMAC/s |
| Dynamic Channel Allocation (DCA) | Dynamic convolutions compute channel-wise attention scores; adaptively reduces dimensionality from $D_1$ to $D_2$ for efficient compression | +0.1M params, +0.1 GMAC/s |
| Group convolution | Applied in down-blocks for additional efficiency | — |

**Discriminator**: Conformer-based MetricGAN (CMGAN) discriminator.

### SARL Framework

![SARL framework](raw/papers/lee-2026-spatial-magnifier-spatial-upsampling/figures/fig2-sarl-framework.png)

*Figure 2: Overall framework of Spatial Audio Representation Learning (SARL): (a) SARL-Signal and (b) SARL-Feature frameworks.*

Two paradigms for conditioning MC-SE on virtual spatial information:

**SARL-S (Signal-Level)**: Spatial-Magnifier estimates explicit VM signals concatenated with RM signals to form $\bar{\mathbf{y}} = [\mathbf{r}, \hat{\mathbf{v}}]$, directly processed by MC-SE model.

**SARL-F (Feature-Level)**: Spatial-Magnifier estimates VM features $f_{\hat{\mathbf{v}}} \in \mathbb{R}^{H \times T \times F}$ fused with encoded RM signals via element-wise addition:

$$\hat{\mathbf{x}}^{se_{\bar{\mathbf{y}}}} = \text{MC-SE}_{sep.+dec.}(h_\phi(\mathbf{r}) + f_{\hat{\mathbf{v}}})$$

where $h_\phi(\cdot)$ is the encoder. SARL-F acts as a high-level spatial regularizer even when raw VM waveform reconstruction is challenging.

**Training**: Pre-trained MC-SE model fine-tuned while Neural-VME trained from scratch. Same inference computational cost as base MC-SE model.

### Loss Function

Combined time-domain SNR losses for Neural-VME and VM-BF, plus adversarial losses with weights 0.3 : 0.7 : 0.01 : 0.01.

## Experimental Setup

| Parameter | Value |
|:----------|:------|
| Dataset | Interspeech 2020 DNS challenge |
| Training/Val/Test clips | 50,000 / 2,000 / 3,000 (10s each) |
| Room simulation | Pyroomacoustics, image source method (order 6) |
| Array geometry | 6-ch: 4-ch circular (r=10cm) + 2 vertical (±10cm) |
| Room dimensions | [3,10] × [3,10] × [2,5] m |
| Absorption coefficient | [0.1, 0.5] → RT60 ∈ [0.15, 1.75] s |
| SNR / SIR | [−10, 5] dB |
| Source distance | [0.5, 2.5] m from array center |
| Tasks | Omni-SE and FoV-SE (±20°) |
| STFT | 16ms window, 8ms hop, 16kHz |
| Beamformer weights | Block-wise, 25-frame window |
| Spatial-Magnifier | $N_b=5$, dims [128,96,64,48,32] |
| Optimizer | Adam, lr=0.001, 100 epochs, batch 64 |
| Hardware | 32 × H100 GPUs |
| Metrics | SI-SDR, SNR, PESQ, STOI |

## Results

### Ablation: Training Methods (2ch RM, 4ch VM, FoV-SE)

| Configuration | VM-BF SI-SDR | VM-BF SNR | VM-BF PESQ | VM-BF STOI |
|:-------------|:-------------|:----------|:-----------|:-----------|
| SpatialNet+MCWF 2ch (baseline) | 2.19 | 4.57 | 1.97 | 70.4 |
| Neural-VME (freeze) | 4.01 | 5.71 | 2.08 | 75.1 |
| Neural-VME (unfreeze) | 5.30 | 6.71 | 2.14 | 76.9 |
| **SARL-F** | **6.10** | **7.27** | **2.33** | **80.4** |
| **SARL-S** | **7.10** | **8.09** | **2.40** | **82.1** |
| SpatialNet+MCWF 6ch (oracle) | 8.35 | 9.06 | 2.41 | 84.6 |

Key findings:
- SARL-S recovers **85%** of the oracle 6ch SI-SDR gap (2ch→6ch: +6.16 dB; SARL-S: +4.91 dB)
- Removing VM loss degrades both SARL methods, confirming virtual spatial information is essential
- Even without VM signals in beamforming, SARL conditioning improves over 2ch baseline

### Ablation: Spatial-Magnifier Architecture (SARL-S, 2ch RM, 4ch VM)

| Variant | VM-BF SI-SDR | VM-BF SNR | VM-BF PESQ | VM-BF STOI |
|:--------|:-------------|:----------|:-----------|:-----------|
| Full model | 7.10 | 8.09 | 2.40 | 82.1 |
| w/o GAN | 7.06 | 8.06 | 2.39 | 81.8 |
| w/o Selection Module | 6.82 | 7.85 | 2.35 | 81.5 |
| w/o DCA | 7.01 | 8.00 | 2.38 | 81.9 |

Selection module has the largest impact on VM-BF performance; DCA more critical for SARL-F.

### Comparison with Neural-VME Baselines (Omni-SE)

| Model | Params | MAC/s | VM-BF SI-SDR (2ch/4ch) | VM-BF PESQ (2ch/4ch) |
|:------|:-------|:------|:-----------------------|:----------------------|
| MC Conv-TasNet (STL) | +13.0M | +20.5G | 3.78 / 4.89 | 2.17 / 2.24 |
| MC Conv-TasNet (MTL) | +13.0M | +20.5G | 3.78 / 4.89 | 2.17 / 2.24 |
| SpatialNet-VME | +1.2M | +19.8G | 4.80 / 4.87 | 2.17 / 2.23 |
| Spatial-Magnifier (VME) | +1.2M | +19.2G | 5.58 / 5.84 | 2.31 / 2.36 |
| **Spatial-Magnifier (SARL-S)** | **+1.5M** | **+24.4G** | **7.10 / 7.72** | **2.40 / 2.51** |

Spatial-Magnifier achieves superior VM-BF with **~10× fewer parameters** than Conv-TasNet baselines.

### Versatility Across Processing Strategies

- **2ch/8ch VM**: Near 10ch oracle performance, generating substantial spatial information from limited data
- **MVDR back-end**: Maintains competitive results when switching from MCWF to Souden MVDR
- **MC-RNN back-end**: Preserves performance gains, confirming architecture-agnostic nature
- **Smart glasses ATF**: Comparable to 7ch oracle model on measured HRTF data
- **VM-SE (end-to-end)**: SpatialNet-small + Spatial-Magnifier outperforms SpatialNet-large 2ch (2.7M/44.2G vs 6.5M/110G), proving virtual spatial information is more effective than increasing model size

## Key Contributions

1. **Spatial-Magnifier**: First specialized GAN-based network for audio spatial upsampling, incorporating Selection Module and DCA module for efficient spatial feature extraction and compression
2. **SARL framework**: Two paradigms (signal-level and feature-level) for conditioning MC-SE on virtual spatial information, decoupling spatial representation learning from spectral enhancement
3. **VM-SE task**: Novel task definition for virtual microphone-based speech enhancement, improving end-to-end models directly without beamforming back-end
4. **Architecture-agnostic**: Demonstrated robustness across MCWF, MVDR, SpatialNet, MC-RNN back-ends, and diverse array geometries including smart glasses
5. **Efficiency**: ~10× fewer parameters than Conv-TasNet baselines while achieving superior performance; virtual spatial information more effective than model scaling

## Related Concepts

- [[../concepts/virtual-microphone-estimation|Virtual Microphone Estimation]]
- [[../concepts/spatial-audio-representation-learning|Spatial Audio Representation Learning]]
- [[../concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[../concepts/beamforming|Beamforming]]
- [[../concepts/mvdr-beamformer|MVDR Beamformer]]
- [[../concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[../concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]

## Related Sources

- [[../sources/farmani-2026-virtual-mic-beamforming-hearing-aid|Farmani 2026: VM Beamforming for Hearing Aids]]
- [[../sources/oviste-2026-neural-vslf-speech-enhancement|Oviste 2026: Neural VSLF for Speech Enhancement]]
- [[../sources/liu-2026-scm-reconstruction-speech-enhancement|Liu 2026: SCM Reconstruction for Speech Enhancement]]
- [[../sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal 2026: Adaptive Diagonal Loading for Beamforming]]
