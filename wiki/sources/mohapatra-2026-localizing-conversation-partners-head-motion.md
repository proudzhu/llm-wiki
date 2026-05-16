---
type: source
created: 2026-05-03
updated: 2026-05-03
sources:
  - raw/papers/mohapatra-2026-localizing-conversation-partners-head-motion/full-text.md
  - https://doi.org/10.48550/arXiv.2604.23927
  - zotero://select/items/0_H3IVVHDU
tags:
  - smartglasses
  - imu
  - head-orientation
  - speech-enhancement
  - conversation-partner-localization
  - behavioral-modality
---

# Mohapatra, Murdock, Aroudi, Ananthabhotla, Menon, Xu & Khaleghimeybodi 2026: Localizing Conversation Partners Using Head Motion

**Authors**: [[entities/payal-mohapatra|Payal Mohapatra]]¹, [[entities/calvin-murdock|Calvin Murdock]]², [[entities/ali-aroudi|Ali Aroudi]]², [[entities/ishwarya-ananthabhotla|Ishwarya Ananthabhotla]]², [[entities/anjali-menon|Anjali Menon]]², [[entities/buye-xu|Buye Xu]]², [[entities/morteza-khaleghimeybodi|Morteza Khaleghimeybodi]]²

**Affiliations**: ¹ Northwestern University, Evanston, IL, USA · ² Meta Reality Labs, Redmond, WA, USA

**Published**: arXiv preprint, 2026 (arXiv:2604.23927)

**Type**: Preprint

**DOI**: [10.48550/arXiv.2604.23927](https://doi.org/10.48550/arXiv.2604.23927)

**Zotero**: [H3IVVHDU](zotero://select/items/0_H3IVVHDU)

## Summary

Proposes HALo (Head-orientation-based Acoustic zone Localization), a network that uses IMU-derived head orientation from smartglasses to infer a user's [[concepts/acoustic-zones-of-interest|acoustic zones of interest]] in seated conversations. By integrating an *a priori* estimate of the number of conversation partners, HALo achieves 0.78 accuracy and 0.62 macro-F1 for localization—a 24% average improvement over baselines. Complemented by CoCo (Classifying the number of Conversation partners), which achieves 0.74 accuracy for partner count estimation (35% gain over baselines), the combined HALo-CoCo system demonstrates a minimal end-to-end speech enhancement pipeline with clear advantages in noisy multiparty settings.

## Problem Formulation

The core challenge: current spatial audio-based methods for speaker localization are **agnostic to user listening preferences** and fail in noisy settings with interfering speakers. The paper proposes using **head-orienting behavior** captured by IMUs on smartglasses as a behavioral modality to infer the user's acoustic zones of interest.

**Task 1 — Localization**: Given a sequence of head orientation measurements $\mathbf{x}_t = (\phi_t, \psi_t)$ (azimuth, elevation) over a 30-second segment, predict the discrete spatial zones containing conversation partners:

$$\mathcal{Z} = \bigvee_{s=1}^{S} \mathbf{b}_s, \quad \mathbf{b}_s \in \{0,1\}^n$$

where $\mathbf{b}_s$ is the bin-vector for speaker $s$ and $\bigvee$ denotes element-wise logical OR.

**Task 2 — Classification**: Predict the number of conversation partners $K \in \{1, 2, 3, 4\}$ from IMU data alone.

**Discrete spatialization**: The azimuth plane is divided into $n=6$ bins: $[-100°, -60°]$, $[-60°, -30°]$, $[-30°, 0°]$, $[0°, 30°]$, $[30°, 60°]$, $[60°, 100°]$.

## Methodology

### Head Orientation from IMUs

Angular velocity from the IMU gyroscope is integrated using quaternion-based attitude propagation:

$$\mathbf{q}_{t+1} = \left[\cos\left(\frac{\|\boldsymbol{\omega}\|\Delta t}{2}\right)\mathbf{I}_4 + \frac{1}{\|\boldsymbol{\omega}\|}\sin\left(\frac{\|\boldsymbol{\omega}\|\Delta t}{2}\right)\boldsymbol{\Omega}(\boldsymbol{\omega})\right]\mathbf{q}_t$$

The resulting rotation matrix is transformed to spherical coordinates (azimuth, elevation) with the average front-facing direction as origin. Only gyroscope data is used (no translational motion) to avoid drift from double integration of accelerometer data. 30-second observation windows keep IMU drift acceptable.

![HALo network architecture](raw/papers/mohapatra-2026-localizing-conversation-partners-head-motion/figures/fig6-loc-arch.png)
*Figure 6: Overview of the HALo network — temporal learning module, fusion block for static features, and imbalanced predictors for acoustic zone localization.*

### HALo Network Architecture

HALo (~400k parameters) consists of four components:

1. **Feature Summarization**: 1D CNN + max pooling along temporal axis → embeddings $\mathbf{E} \in \mathbb{R}^{F \times T}$
2. **Temporal Learning**: Bidirectional LSTM + self-attention mechanism. The attention weights highlight segments with greater head-orientation dynamism (active engagement periods).
3. **Fusion of Static Features**: Late fusion of the temporal representation with the number of conversation partners (a static feature). The temporal embedding is reduced via linear layers + ReLU, then concatenated with the static feature.
4. **Imbalanced Predictors**: Per-zone binary classifiers with weighted loss to handle class imbalance:

$$\mathcal{L}_{loc} = -\frac{1}{n}\sum_{i=1}^{n} w_i \left[ y_i \log(\hat{y}_i) + (1-y_i)\log(1-\hat{y}_i) \right]$$

**Backbone comparison** (Table 2):

| Model | Macro-F1 | Hamming |
|-------|----------|---------|
| 1D CNN | 0.40 | 0.76 |
| Transformer | 0.27 | 0.82 |
| LSTM | 0.60 | 0.78 |
| **BiLSTM+Attn** | **0.63** | **0.80** |

### CoCo Network

CoCo classifies the number of conversation partners using IMU data with optional abstract audio features:

- **Input**: Same IMU features as HALo + optional self-VAD and speaker-VAD streams
- **Architecture**: Similar temporal backbone (BiLSTM + attention) with a 4-class classifier head
- **Target shaping**: Uses DBSCAN-empirically-determined 8-second cumulative voice activity threshold to qualify conversation partners, reducing noise from non-participating speakers

### HALo-CoCo Joint Training

Stage-wise training: CoCo is trained first, then its embedding replaces the ground-truth number of partners as the static feature input to HALo. This eliminates the need for *a priori* knowledge of partner count at inference time.

## Experimental Setup

| Aspect | Detail |
|--------|--------|
| **Dataset** | RLR-CHAT (Reality Labs Research Conversations for Hearing Augmentation Technology) |
| **Participants** | N > 70, aged 20–60, including mild hearing loss |
| **Group sizes** | 2–5 participants |
| **Noise conditions** | Cafeteria noise at 0, 55, 65, 75 dBA (pseudo-random 25–35s intervals) |
| **IMU** | Aria smartglasses right-leg IMU, 1000 Hz sampling |
| **Ground truth** | OptiTrack motion tracking, 120 Hz |
| **Segment length** | 30 seconds at 5 Hz → 150 frames |
| **Spatial zones** | 6 discrete azimuth bins |
| **Train/test split** | 7:3 ratio, 20% of training for validation |
| **Seeds** | 3 random seeds (2711, 2712, 2713) |
| **Optimizer** | ADAM, batch size 64 |
| **Learning rates** | Localization: 1e-5, Classification: 1e-3 |
| **Epochs** | 20, best checkpoint by lowest validation loss |

## Results

### Localization Performance (Table 3)

| Method | Macro-F1 | Hamming Score |
|--------|----------|---------------|
| Rule-based | 0.27 | 0.71 |
| Segment-based (MLP) | 0.27 ± 0.01 | 0.72 |
| Informer | 0.45 ± 0.04 | 0.76 |
| **HALo (Ours)** | **0.62** | **0.79** |
| **HALo + a priori K** | **0.78** | **0.84** |

Key findings:
- HALo outperforms all baselines by **45% in macro-F1** and **10% in Hamming score** on average
- *A priori* knowledge of partner count boosts localization by ~50% (0.62 → 0.78 macro-F1)
- Abstract audio features (self-VAD, speaker-VAD) do **not** provide significant localization benefit
- HALo outperforms Informer by **38% in F1** and **17% in Hamming score**

### Classification Performance (CoCo)

| Configuration | Accuracy | Macro-F1 |
|--------------|----------|----------|
| IMU only | 0.60 | — |
| IMU + self-VAD + speaker-VAD | 0.73 | — |
| IMU + target shaping | **0.74** | — |

### HALo-CoCo Joint Performance

HALo-CoCo (using CoCo's estimated partner count instead of ground truth) achieves performance between HALo without static features and HALo with ground-truth partner count, demonstrating practical viability.

### Minimal Speech Enhancement (EasyCom Dataset)

| Method | SNR (dB) | STOI | PESQ |
|--------|----------|------|------|
| Raw reference mic | -10.55 | 0.34 | 1.10 |
| Frontal steering (0°) | -9.30 | 0.39 | 1.16 |
| **HALo steering** | **-8.63** | **0.41** | 1.15 |
| MUSIC | -9.26 | 0.40 | 1.15 |
| GCC-PHAT | -9.11 | 0.41 | 1.16 |
| SRP-PHAT | -8.34 | 0.38 | 1.10 |

HALo-based steering provides **+1.4 dB SNR improvement** over frontal steering in multiparty settings, and remains stable under acoustically challenging conditions where audio-based methods degrade.

## Key Contributions

1. Proposes the novel task of localizing conversation partners based on listener preferences using head orientation as a behavioral modality captured from on-device IMUs in smartglasses, validated on a large-scale dataset (N > 70) with unconstrained natural conversations.

2. Introduces HALo, a head-orientation-based acoustic zone localization network that formulates conversation partner localization as a sequence-to-multilabel classification problem, achieving 0.78 accuracy and 0.62 macro-F1 with *a priori* partner count (24% average improvement over baselines). Complements with CoCo for partner count classification (0.74 accuracy, 35% gain over baselines).

3. Presents HALo-CoCo, an end-to-end training strategy that eliminates the need for *a priori* partner count knowledge, along with comprehensive evaluation including ablation studies, qualitative session-level analyses, model explainability via attention visualization, and a minimal speech-enhancement pipeline demonstrating practical advantages in noisy multiparty settings.

## Related Concepts

- [[concepts/acoustic-zones-of-interest|Acoustic Zones of Interest]]
- [[concepts/head-orientation-from-imu|Head Orientation from IMUs]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]
- [[concepts/inertial-measurement-unit|Inertial Measurement Unit]]

## Related Sources

- [[sources/miran-2026-imu-feedback-cancellation|Miran 2026: IMU-Based Acoustic Feedback Cancellation]]
- [[sources/frank-2026-low-latency-roi-beamforming|Frank & Cohen 2026: Low-latency ROI Beamforming for Smart Glasses]]
- [[sources/masilamani-2024-headphone-conversation-detect-paper-reading-note|Masilamani 2024: Headphone Conversation Detect]]
