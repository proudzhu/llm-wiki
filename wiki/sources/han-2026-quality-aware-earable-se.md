---
type: source
created: 2026-06-21
updated: 2026-06-21
sources:
  - raw/papers/han-2026-quality-aware-earable-se/full-text.txt
  - https://doi.org/10.1145/3810214
  - zotero://select/items/0_92AXTWCU
tags:
  - earable-sensing
  - speech-enhancement
  - quality-aware-fusion
  - dual-microphone
  - in-ear-speech
  - ear-canal-deformation
  - data-augmentation
  - self-supervised
---

# Han, Yan, Wang, Huang, Feng & Yang 2026: QuaSE — Quality-Aware Earable Dual-Microphone Speech Enhancement

**Authors**: [[entities/feiyu-han|Feiyu Han]] (corresponding), [[entities/dawei-yan|Dawei Yan]], [[entities/shanyue-wang|Shanyue Wang]], [[entities/jinyang-huang|Jinyang Huang]], [[entities/yuanhao-feng|Yuanhao Feng]], [[entities/panlong-yang|Panlong Yang]]
**Institutions**: Nanjing University of Information Science and Technology; Hebei University; The Hong Kong Polytechnic University; Hefei University of Technology; The University of Electro-Communications
**Venue**: Proc. ACM Interact. Mob. Wearable Ubiquitous Technol. (IMWUT), Vol. 10, No. 2, Article 40
**Year**: 2026 (June)
**Type**: Journal article
**DOI**: [10.1145/3810214](https://doi.org/10.1145/3810214)
**Zotero**: [92AXTWCU](zotero://select/items/0_92AXTWCU)

## Summary

Identifies that **ear canal deformation (ECD)** induced by articulatory gestures causes air pressure imbalance inside the sealed ear canal, severely degrading in-ear speech quality and breaking the cross-channel correlation assumption underlying existing dual-microphone speech enhancement (SE) systems. Proposes **QuaSE**, a quality-aware dual-microphone SE framework that dynamically fuses quality-varying in-ear speech with noisy airborne speech by self-assessing in-ear speech quality without reference. QuaSE outperforms state-of-the-art baselines by 6.27%, 4.54%, 14.90%, and 11.93% in PESQ, STOI, SI-SDR, and SegSNR, and the quality-aware adaptation (QA) module can be modularly integrated into other systems (e.g., EarSpeech) to improve their fusion performance.

## Problem Formulation

Existing dual-microphone SE techniques (e.g., EarSpeech, ClearSpeech) assume that in-ear speech (auxiliary modality, captured via bone conduction through the sealed ear canal) maintains a highly stable correlation with airborne speech (primary modality, captured by the out-ear microphone). This assumption breaks down in practice:

**Key Observation — ECD-induced in-ear speech distortion**:
During pronunciation, articulatory gestures (mandible, lips, tongue, jaw, velum movement) stretch/compress facial muscles and soft tissues around the ear canal, causing **ear canal deformation (ECD)**. In a fully sealed ear canal (earphone eartip fits tightly), ECD alters the available air volume, creating pressure fluctuations that "clamp" the microphone diaphragm and inhibit its oscillatory response to sound waves. This induces a **stuck-at-low fault** where the microphone output remains biased at a low level, destroying the temporal and spectral structure of in-ear speech.

The microphone transducer output follows:

$$u(t) = S_e \cdot (d(t) - d_0(t))$$

where $S_e$ is electronic sensitivity, $d(t)$ is diaphragm displacement, and $d_0(t)$ is the initial displacement. ECD-induced pressure imbalance restricts $d(t)$, causing the output to remain at a constant low level.

**Impact**: The correlation between airborne and high-quality in-ear speech is ~30× greater than with low-quality in-ear speech. Low-quality in-ear speech reduces fusion gains from 0.960→0.623 (PESQ), 8.229→5.172 (SegSNR), and 10.719→7.835 (SI-SDR), a phenomenon of **modality imbalance**.

**Three challenges addressed**:
1. Fine-grained assessment of time–frequency distortion of in-ear speech **without matching references** (airborne speech is itself corrupted by noise)
2. Effective and dynamic fusion of airborne speech with **quality-varying** in-ear speech
3. Real-time and generalized SE across individuals and scenarios on resource-constrained IoT devices

## Methodology

QuaSE has four core components: multi-scale deep feature extraction, quality-aware adaptation, dual-channel speech reconstruction, and a data selection/augmentation training strategy.

### Multi-scale Audio Encoder

Dual-channel speech (in-ear + out-ear) is pre-processed with a 100 Hz high-pass filter, downsampled to 16 kHz, and transformed via STFT into time-frequency (T-F) representations. Two symmetric audio encoders process the in-ear and airborne spectrograms. Each encoder consists of multiple **ConvBlocks** interleaved with **Frequency Transformation Blocks (FTBs)**, with filter counts of 12, 24, and 48. Each ConvBlock uses:
- An initial 3×3 dilated convolution (dilation=2) to expand the receptive field
- A split into three parallel branches with dilation rates 1, 2, 3 for multi-scale spatial capture
- Concatenation and fusion via a final 3×3 dilated convolution (dilation=2)

### Quality-aware Adaptation (QA Module)

The core novelty — dynamically weighting in-ear features based on self-assessed quality.

**1. Data-level Quality Self-assessment (Self-supervised)**:
An autoencoder is trained **only on high-quality in-ear spectrograms** (selected via the spectral peak-to-valley matching strategy). At inference, the mean absolute error between input $S_{in}^{T \times F}$ and reconstruction $S_{out}^{T \times F}$ serves as the quality metric $Q_m$. Low-quality spectrograms (distorted by ECD) cannot be accurately reconstructed, yielding large errors.

**2. Quality Embedding Generation**:
The quality matrix $Q_m \in \mathbb{R}^{1 \times F \times T}$ is transformed into embeddings $Q_e \in \mathbb{R}^{C \times F \times T}$ via:
- **Frequency squeeze**: 1×1 convolution + frequency-dimensional global average pooling (GAP), reducing computation by $F$ times. Key insight: ECD-induced attenuation is frequency-independent at a given time, so squeezing along frequency is valid.
- **Quality learning block**: Two fully-connected layers with ReLU ($\psi$) and Sigmoid ($\sigma$): $U_l = \sigma(W_2 \psi(W_1 U_{squ}))$, outputting weights in [0, 1].
- **Frequency and channel unsqueeze**: Expands the quality vector back to $Q_e \in \mathbb{R}^{C \times F \times T}$.

**3. Feature-level Cross Fusion**:
The quality embedding $Q_e$ multiplies the in-ear feature map $F_{ie}$, then the weighted in-ear features are concatenated with airborne features $F_{air}$ along the channel dimension. A lightweight **Convolutional Block Attention Module (CBAM)** applies sequential channel and spatial attention to refine the fused representation.

### Speech Enhancement Decoder

- **Airborne reconstruction**: Fused features pass through four 3×3 dilated convolution blocks (48, 24, 12, 1 filters) with batch normalization + ReLU + skip connections, producing a spectrogram mask $Mask_{air}^{T \times F}$. Output: $\hat{s}_{air} = \text{iSTFT}(Mask_{air}^{T \times F} \cdot S_{air}^{T \times F})$.
- **In-ear reconstruction (auxiliary, training-only)**: Forces the model to retain in-ear branch information; frozen during inference to address modality imbalance.
- **Customized loss**: $L = L_{ie}^{tf} + L_{air}^{tf} + L_{air}^{t}$ combining in-ear T-F loss, airborne T-F loss, and airborne time-domain loss.

### High-quality Data Selection Strategy

A **spectral peak-to-valley matching algorithm** identifies high-quality in-ear speech without ground-truth references, exploiting the cross-channel correlation in the low-frequency band (100–1000 Hz, where in-ear speech retains spectral structure similar to airborne speech despite the [[concepts/ear-canal-occlusion-effect|occlusion effect]] enhancement):

1. Bandpass filter (100–1000 Hz) both channels; split into 100 ms clips (50 ms step)
2. Extract FFT magnitude spectrum envelope with Gaussian smoothing + Z-score normalization
3. Detect peaks and valleys via local extrema (min spacing = 0.1N, min prominence = 0.1·std)
4. **Greedy matching** (Alg. 1): Compute peak/valley matching rate $R$ and absolute error $Err$ within tolerance $\tau$
5. **First-order difference DTW alignment** (Alg. 2): Align interval sequences of adjacent peaks/valleys to capture rhythm; normalize DTW distance to [0, 1]
6. **Similarity score** (Alg. 3): Weighted combination of matching rates, DTW distances, and errors; threshold $\xi = 0.5$ classifies high vs. low quality. Weights $\alpha_1{=}0.4, \alpha_2{=}0.4, \alpha_3{=}0.1, \alpha_4{=}0.1$.

### Content-aware Low-quality Data Augmentation

Simulates ECD-induced distortion via **content-aware adaptive time masking** on synthesized in-ear spectrograms (generated from LibriSpeech airborne speech via a GMM). Unlike random masking, mask probability for the $m$-th time bin is conditioned on spectral energy distribution:

$$P_m = \frac{\sum_{f=f_0}^{F} S(m, f)}{\sum_{t=t_0}^{T} \sum_{f=f_0}^{F} S(t, f)}$$

This produces both high-quality and low-quality synthetic in-ear speech pairs for pre-training.

## Experimental Setup

| Aspect | Detail |
|--------|--------|
| **Participants** | 32 (20 male, 12 female), ages 18–45; 27 Mandarin, 5 English speakers |
| **Hardware** | Custom prototype with in-ear mic (AS-B6027AL30-RC1) + out-ear mic (SO-COURT-MIC-2), 3 earphone types (foam/silicone tips, vented/unvented, metal/plastic shells), connected to Raspberry Pi 5 |
| **Real dataset** | ~2800 pairs of 5-second dual-channel clips (20–30 min reading per participant) |
| **Synthetic dataset** | ~8000 pairs from LibriSpeech via GMM synthesis + content-aware masking |
| **Noise sources** | ESC-50 (environmental), LibriSpeech (competing speaker), MUSAN (music); SNR ∈ [−5, 10] dB |
| **Training** | PyTorch; 144 Xeon CPUs + 3 NVIDIA RTX A6000 GPUs; Adam (lr=0.001, weight decay=1e-5); 32 epochs, batch size 12; lr scheduler (×0.5 on plateau); gradient clipping (max norm 10) |
| **Evaluation** | Leave-one-group-out cross-validation (8 groups) |
| **Metrics** | PESQ, STOI, SI-SDR, SegSNR; real-world: WER (Whisper), MOS (10 volunteers, 0–5) |
| **Baselines** | Phasen, Inter-Subnet (single-modality); ClearSpeech, EarSpeech (dual-microphone SOTA) |

## Results

### Overall Performance (Table 1, average across noise types)

| Method | PESQ | STOI | SI-SDR (dB) | SegSNR (dB) |
|--------|------|------|-------------|-------------|
| Noisy Speech | 2.45 | 0.81 | 5.00 | 5.93 |
| Phasen | 3.11 | 0.82 | 9.81 | 10.22 |
| Inter-Subnet | 3.19 | 0.83 | 10.41 | 10.69 |
| ClearSpeech | 3.12 | 0.85 | 12.28 | 11.74 |
| EarSpeech | 3.10 | 0.88 | 11.99 | 11.64 |
| **QuaSE** | **3.39** | **0.92** | **14.11** | **13.14** |
| EarSpeech w/ QA | 3.27 | 0.88 | 13.40 | 12.84 |
| QuaSE w/o QA | 3.09 | 0.86 | 13.11 | 11.91 |

- QuaSE outperforms the best baseline by **9.35% PESQ, 4.55% STOI, 17.68% SI-SDR, 12.89% SegSNR**
- The QA module alone improves QuaSE by **6.27% PESQ, 4.54% STOI, 14.90% SI-SDR, 11.93% SegSNR**
- Integrating QA into EarSpeech yields gains up to **5.48% PESQ, 11.76% SI-SDR, 10.31% SegSNR** — demonstrating modular applicability

### Generalization and Robustness

- **Unseen sentences/languages**: Data augmentation provides ~10% SI-SDR gain; maintains competitive performance on Mandarin (untrained)
- **User groups**: Leave-one-group-out validation shows slight inter-group differences; synthetic data (60 speakers) enables user-independent features
- **Noise scope**: Effective down to −10 dB SNR (1.14 PESQ, 14.65 dB SI-SDR improvement); at −15 dB, averaged PESQ ≈ 1.8, SI-SDR ≈ 0 dB
- **Gender/age**: Consistent across genders and ages (18–45), max difference 1.82 dB
- **Earphone types**: Outperforms baseline across all 3 types; vented designs reduce but do not eliminate ECD distortion
- **Real-world**: 35% WER reduction in canteen, 30% in outdoor street; consistently higher MOS than EarSpeech

### Latency (5-second clip)

| Platform | Quality Adaptation | Encoder & Decoder | Overall |
|----------|-------------------|-------------------|---------|
| Desktop-GPU | 0.047 s | 0.073 s | 0.119 s |
| Desktop-CPU | 0.429 s | 0.561 s | 1.009 s (RTF 0.20) |
| Redmi Note 12 | 3.456 s | 5.072 s | 8.849 s (RTF 1.77) |

Real-time on desktop CPU (RTF < 1); not yet real-time on mobile, but optimizations reduced latency by ~50% (from 14 s).

## Key Contributions

1. **First identification of ECD-induced in-ear speech distortion**: Reveals that articulatory-gesture-induced ear canal deformation causes air pressure imbalance in the sealed ear canal, degrading in-ear speech quality and breaking the cross-channel correlation assumption of existing dual-microphone SE systems
2. **QuaSE framework with quality-aware fusion**: A self-supervised quality assessment module (autoencoder-based, no reference needed) generates quality embeddings that dynamically weight in-ear features before cross-modal fusion, mitigating modality imbalance
3. **Spectral peak-to-valley matching for reference-free quality selection**: Combines greedy peak/valley matching with first-order difference DTW alignment to automatically identify high-quality in-ear speech for training the quality assessor
4. **Content-aware low-quality data augmentation**: Adaptive time masking conditioned on spectral energy distribution simulates ECD-induced distortion, improving generalization to unseen sentences, languages, and users
5. **Modular QA module**: Demonstrated as a plug-in that improves EarSpeech and other sensing tasks, not limited to QuaSE
6. **Comprehensive real-world validation**: 32 participants, 3 earphone types, 3 noise types, 3 real environments; consistent gains across gender, age, language, and SNR conditions

## Related Concepts

- [[concepts/quality-aware-speech-enhancement|Quality-Aware Speech Enhancement]]
- [[concepts/ear-canal-deformation|Ear Canal Deformation]]
- [[concepts/ear-canal-occlusion-effect|Ear Canal Occlusion Effect]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/bone-conduction|Bone Conduction]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/dynamic-time-warping|Dynamic Time Warping]]
- [[concepts/pesq|PESQ]]
- [[concepts/sensor-failure-robust-fusion|Sensor-Failure Robust Fusion]]

## Related Synthesis

- [[synthesis/multimodal-bc-speech-enhancement|Multimodal BC Speech Enhancement]]
- [[synthesis/multi-modal-speech-enhancement|Multi-Modal Speech Enhancement]]
