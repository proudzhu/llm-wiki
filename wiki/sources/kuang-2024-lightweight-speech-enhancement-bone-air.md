---
type: source
created: 2026-05-16
updated: 2026-05-16
sources:
  - raw/papers/kuang-2024-lightweight-speech-enhancement-bone-air/full-text.md
  - https://doi.org/10.1121/10.0028339
  - zotero://select/items/0_VBVTU72Z
tags:
  - speech-enhancement
  - bone-conduction
  - multi-modal-fusion
  - lightweight-network
  - dengcan
  - jasa-2024
---

# Kuang, Yang & Yang 2024: A Lightweight Speech Enhancement Network Fusing Bone- and Air-Conducted Speech

- **Authors**: [[entities/kelan-kuang|Kelan Kuang]], [[entities/feiran-yang|Feiran Yang]], [[entities/jun-yang|Jun Yang]]
- **Affiliations**: Key Laboratory of Noise and Vibration Research, Institute of Acoustics, Chinese Academy of Sciences; University of Chinese Academy of Sciences; State Key Laboratory of Acoustics
- **Venue**: The Journal of the Acoustical Society of America (JASA), Vol. 156, Issue 2, pp. 1355–1366
- **Year**: 2024
- **Type**: Journal Article
- **DOI**: [10.1121/10.0028339](https://doi.org/10.1121/10.0028339)
- **Zotero**: [Open in Zotero](zotero://select/items/0_VBVTU72Z)

## Summary

This paper proposes a lightweight speech enhancement model that fuses bone-conducted (BC) and air-conducted (AC) speech to improve speech quality in noisy environments. The model uses an iterative attention-based feature fusion (iAFF) module to fuse BC and AC spectrograms, followed by a densely gated convolutional attention network (DenGCAN) backbone that estimates a complex ratio mask (cRM). The DenGCAN architecture features dense blocks in encoder/decoder, a squeezed Conformer (sConformer) bottleneck for long-term dependency modeling, and improved attention gates (AG) in skip-connections. On the authors' A4BS dataset (109 speakers, 4 BC positions), the model achieves an average 1.870 wideband-PESQ improvement over noisy AC speech, with only 1.03M parameters and 0.859 GMACs — making it suitable for real-time wearable applications.

## Problem Formulation

Let $\mathbf{y}_{AC}(t) = [Y_{AC}(t,1), \ldots, Y_{AC}(t,F)]^T \in \mathbb{C}^{F \times 1}$ and $\mathbf{y}_{BC}(t) = [Y_{BC}(t,1), \ldots, Y_{BC}(t,F)]^T \in \mathbb{C}^{F \times 1}$ denote the STFT coefficients of the speech signals received by the ACM and BCM at time frame $t$ and frequency bin $f$.

The signal model assumes:
- BC speech is not affected by ambient noise (only self-noise $V_s$ due to resonance/friction)
- AC speech is susceptible to ambient noise $V_b$
- $\phi(\cdot)$ is a nonlinear mapping from AC speech to BC speech

$$
Y_{AC}(t,f) = S(t,f) + V_b(t,f)
$$
$$
Y_{BC}(t,f) = \phi(S(t,f)) + V_s(t,f)
$$

The model estimates a complex ratio mask (cRM) $\mathbf{m}(t) \in \mathbb{C}^{F \times 1}$, applied element-wise to noisy AC speech:

$$
\hat{\mathbf{s}}(t) = \mathbf{m}(t) \otimes \mathbf{y}_{AC}(t)
$$

## Methodology

### Feature Fusion (iAFF)

An iterative attentional feature fusion module generates attention coefficients in two stages:

1. **Coarse fusion**: BC and AC signals are summed, passed through a channel attention module to obtain $\alpha'$
2. **Refined fusion**: The coarsely fused signal is passed through another channel attention module to obtain $\alpha$

$$
\mathbf{y}_{AF}' = \alpha' \otimes \mathbf{y}_{AC} + (1 - \alpha') \otimes \mathbf{y}_{BC}
$$
$$
\mathbf{y}_{AF} = \alpha \otimes \mathbf{y}_{AC} + (1 - \alpha) \otimes \mathbf{y}_{BC}
$$

The fused signal $\mathbf{y}_{AF}$ is concatenated with original $\mathbf{y}_{AC}$ and $\mathbf{y}_{BC}$ as input to the backbone.

### DenGCAN Backbone

The [[concepts/densely-gated-convolutional-attention-network|DenGCAN]] backbone uses a convolutional encoder-decoder structure with:

- **5 dense blocks** in encoder (channel progression: 6→16→32→48→64→64) and 5 in decoder
- **2-layer grouped sConformer** as bottleneck for temporal dependency modeling
- **Attention Gate (AG) skip-connections** between encoder and decoder dense blocks
- **Dense layers**: Each convolution layer takes all preceding feature maps as input (feature reuse); 4 conv layers per dense block, each (1,3) kernel, (1,1) stride, 8 channels
- **Gated layers**: Conv with (1,4) kernel, (1,2) stride to halve frequency dimension; sigmoid gate

The encoder reduces dimensionality progressively (161→79→38→18→8→3 frequency bins), and the decoder restores it.

### Output Mapping

The feature map from the backbone $\tilde{\mathbf{x}} \in \mathbb{C}^{F \times 1}$ is split into real and imaginary components, each passed through a fully connected layer:

$$
\mathbf{m} = \mathbf{W}_r \tilde{\mathbf{x}}_r + j \mathbf{W}_i \tilde{\mathbf{x}}_i
$$

### Training Objective

Combined loss weighting real/imaginary components and magnitude:

$$
\mathcal{L}_{RI} = ||\hat{\mathbf{S}}_r - \mathbf{S}_r||_F + ||\hat{\mathbf{S}}_i - \mathbf{S}_i||_F
$$
$$
\mathcal{L}_{Mag} = ||\hat{\mathbf{S}}| - |\mathbf{S}||_F
$$
$$
\mathcal{L}_{RI-Mag} = 0.5\mathcal{L}_{RI} + 0.5\mathcal{L}_{Mag}
$$

Adam optimizer with linear warmup (2e-5→2e-4) over 10 epochs, then cosine decay to 2e-5. Trained for 250 epochs with early stopping (patience 20).

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Dataset** | A4BS — 109 speakers, 107 h, Mandarin Chinese, 4 BC positions |
| **Training/Validation/Test** | 87 / 11 / 11 speakers |
| **Synthetic noise sources** | ICASSP2022 DNS, QUT Noise, Environmental Background, MUSAN (train); Non-speech-115, NOISEX-92, CHiME-3, MUSAN (test) |
| **SNR range** | [−15 dB, 10 dB] |
| **Window** | 20 ms Hanning, 50% overlap |
| **FFT** | 320-point → 161-dim spectral features |
| **Sampling rate** | 16 kHz, 4-second clips |
| **Metrics** | wb-PESQ, eSTOI |

## Results

### Objective Metrics

Across the test set, the proposed model achieves:
- **Average wb-PESQ: 3.036** (1.870 improvement over noisy AC speech)
- **Average eSTOI: 86.74%** (31.66% improvement over noisy AC speech)

### Comparison with State-of-the-Art

| Model | Domain | Parameters (M) | MACs (G) | Avg wb-PESQ | RTF (ARM) |
|-------|--------|---------------|----------|-------------|-----------|
| GaGNet (Li 2022) | T-F | 5.95 | 1.652 | — | 0.740 |
| DPT-EGNet (Zheng 2022) | T | 0.52 | 13.876 | — | 15.260 |
| MMINet (Wang 2022b) | T | 1.49 | 3.055 | — | 1.802 |
| DC-CRN (Wang 2022a) | T-F | 1.34 | 1.119 | — | 0.865 |
| **DenGCAN (proposed)** | **T-F** | **1.03** | **0.859** | **3.036** | **0.649** |

DenGCAN achieves the lowest RTF (0.649 on ARM Cortex-A53, 0.068 on x86 Kaby Lake) among all models, making it suitable for real-time wearable applications.

### Ablation Study

- **AG skip-connection**: +0.053 wb-PESQ over concatenation-based skip
- **iAFF fusion**: Removing iAFF causes noticeable wb-PESQ decrease at low SNRs
- **sConformer**: Removing sConformer → −0.114 avg wb-PESQ versus LSTM replacement
- **Algorithmic latency**: wb-PESQ improves from 2.98 (0 ms) to 3.11 (160 ms additional latency)

### Subjective Test

Absolute Category Rating with 30 listeners: the proposed model achieves the highest mean opinion scores among all competitive models.

## Key Contributions

1. **DenGCAN backbone**: A lightweight encoder-decoder architecture with densely connected layers enabling feature reuse and significant parameter reduction (1.03M params, 0.859 GMACs).
2. **Attention Gate (AG) skip-connections**: An improved AG that considers both local and global features for selective feature propagation in skip-connections, outperforming both concatenation-based and PWConv-based alternatives.
3. **iAFF-based multi-modal fusion**: Iterative attentional feature fusion that performs coarse-then-refined fusion of BC and AC speech, alleviating the bottleneck of low-quality initial fusion.
4. **sConformer bottleneck**: Lightweight self-attention bottleneck enabling flexible use of future context (0–160 ms additional latency) for improved denoising at the cost of slightly increased latency.
5. **A4BS dataset**: A large-scale 4-position bone-conducted speech dataset with 109 speakers and ~107 hours, enabling research on BC speech characteristics across different sensor placements (throat, overhead, temporal bone, external auditory canal).
6. **Real-time viability**: Lowest RTF among all tested models on both ARM (0.649) and x86 (0.068) platforms.

## Related Concepts

- [[concepts/densely-gated-convolutional-attention-network|DenGCAN (Densely Gated Convolutional Attention Network)]]
- [[concepts/iterative-attentional-feature-fusion|Iterative Attentional Feature Fusion (iAFF)]]
- [[concepts/attention-gate|Attention Gate (AG)]]
- [[concepts/bone-conduction|Bone Conduction]]
- [[concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cRM)]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]

## Related Synthesis

- [[synthesis/multimodal-bc-speech-enhancement|Multimodal Smart Hearables: Bone-Conduction Aided Speech Enhancement]]
