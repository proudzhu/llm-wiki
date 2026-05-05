---
type: source
created: 2026-04-30
updated: 2026-04-30
sources:
  - raw/papers/wang-2026-predictive-dsfanc-crnn/full-text.md
  - raw/papers/wang-2026-predictive-dsfanc-crnn/paper.pdf
  - https://arxiv.org/abs/2604.23144
  - zotero://select/items/0_I6FHS99P
tags:
  - active-noise-control
  - selective-fixed-filter-anc
  - moving-source
  - direction-of-arrival
  - crnn
  - deep-learning
  - sound-source-localization
  - predictive-control
  - feedforward-anc
---

# Wang, Luo, Shi, Ji, Su & Gan 2026: Predictive Directional SFANC via CRNN

> 📎 [Zotero](zotero://select/items/0_I6FHS99P) | [arXiv](https://arxiv.org/abs/2604.23144) | [HTML](https://arxiv.org/html/2604.23144)

| | |
|---|---|
| **Authors** | [[../entities/boxiang-wang\|Boxiang Wang]], [[../entities/zhengding-luo\|Zhengding Luo]], [[../entities/dongyuan-shi\|Dongyuan Shi]], [[../entities/junwei-ji\|Junwei Ji]], [[../entities/xiruo-su\|Xiruo Su]], [[../entities/woon-seng-gan\|Woon-Seng Gan]] |
| **Institutions** | Nanyang Technological University, Singapore; Northwestern Polytechnical University, China |
| **Venue** | Preprint (arXiv:2604.23144) |
| **Year** | 2026 |
| **Type** | Preprint / Conference Paper |

## Summary

Proposes a Predictive Directional Selective Fixed-Filter ANC (PD-SFANC) method that uses a CRNN to predict the next-frame Direction-of-Arrival (DoA) of a moving noise source and proactively select the most suitable pre-trained control filter. Unlike D-SFANC which reacts to the current DoA with a one-frame lag, PD-SFANC exploits multi-frame temporal context to forecast source movement, achieving delayless filter switching and superior noise reduction under both constant-rate and time-varying-rate source motion.

## Problem Formulation

D-SFANC selects the control filter based on the **current** DoA estimate, but by the time the filter is applied, the source has already moved. This one-frame lag causes:
- Degraded noise reduction during directional transitions
- High-amplitude fluctuations in the residual error
- Inability to track rapidly accelerating sources

The goal is to **predict** the DoA for the upcoming frame and pre-select the corresponding control filter, eliminating the reactive lag.

![D-SFANC vs PD-SFANC comparison](raw/papers/wang-2026-predictive-dsfanc-crnn/figures/fig1-intro.png)
*Figure 1: D-SFANC reacts to the current DoA with a one-frame lag; PD-SFANC predicts the next-frame DoA for proactive filter selection.*

## Methodology

### Pre-trained Control Filter Library

A discrete DoA grid $\theta_v \in \{\theta_1, \ldots, \theta_V\}$ is defined with $V$ candidate angles. At each $\theta_v$, a control filter $\mathbf{w}^{[\theta_v]}$ is pre-trained via FxLMS:

$$\mathbf{w}^{[\theta_v]}(n+1) = \mathbf{w}^{[\theta_v]}(n) + \mu [\mathbf{r}^{[\theta_v]}(n)]' e^{[\theta_v]}(n)$$

where $[\mathbf{r}^{[\theta_v]}(n)]' = \hat{s}(n) * \mathbf{r}^{[\theta_v]}(n)$ is the filtered reference signal.

### CRNN for Next-Frame DoA Prediction

**Input**: $K$ consecutive frames of $J$-channel reference signals, preprocessed via STFT into magnitude + phase spectrograms → tensor $\mathbf{R} \in \mathbb{R}^{2J \times F \times TK}$.

**Architecture**:

![CRNN architecture for DoA prediction](raw/papers/wang-2026-predictive-dsfanc-crnn/figures/fig3-crnn-architecture.png)
*Figure 3: CRNN architecture — 3 conv blocks extract spatial features, GRU fuses temporal dynamics, FC+Softmax outputs DoA class probabilities.*

1. **3 Convolutional Blocks**: 2D conv + group norm + ReLU + max pooling → spatial feature extraction
2. **Adaptive Average Pooling** along frequency → $\mathbf{z} = \text{Avg}[\text{CNN}(\mathbf{R})] \in \mathbb{R}^{T' \times 64}$
3. **GRU Layer**: $\mathbf{h}_t = \text{GRU}(\mathbf{z}_t, \mathbf{h}_{t-1}) \in \mathbb{R}^{64}$ — temporal dynamics fusion
4. **FC + Softmax**: $\hat{\mathbf{p}} = \text{Softmax}[\text{FC}(\mathbf{h}_{T'})] \in \mathbb{R}^{V}$ — DoA class probabilities

**Prediction**: $\hat{v} = \arg\max_{v} \hat{p}_v$

**Loss**: Cross-entropy $\mathcal{L} = -\sum_{v=1}^{V} y_v \log(\hat{p}_v)$

### Proactive Noise Control (Dual-Module Architecture)

![PD-SFANC system block diagram](raw/papers/wang-2026-predictive-dsfanc-crnn/figures/fig2-block-diagram.jpg)
*Figure 2: PD-SFANC dual-module architecture — co-processor runs CRNN for DoA prediction and filter pre-selection; real-time controller performs noise cancellation at sampling rate.*

| Module | Rate | Function |
|--------|------|----------|
| **Co-processor** (e.g., phone) | Frame rate | CRNN inference → DoA prediction → filter pre-selection |
| **Real-time controller** | Sampling rate | Noise cancellation using selected filter |

The co-processor predicts the next-frame DoA and pre-selects $\mathbf{w}^{[\theta_{\hat{v}}]}$; the real-time controller applies it without buffering delay. After a $K$-frame cold-start, the filter updates every frame.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Sampling rate | 16000 Hz |
| Reference microphones ($J$) | 4 (tetrahedral cardioid, 0.025 m) |
| Secondary sources | 1 |
| Error microphones | 1 |
| Control filter length | 1024 |
| STFT bins ($F$) | 513 |
| STFT frames ($T$) | 64 |
| DoA categories ($V$) | 36 (10° resolution) |
| Context frames ($K$) | 4 |
| Frame length | 0.5 s |
| Network input length | 2 s |
| CRNN parameters | 0.05 M |
| CRNN MACs | 480.08 M |

| Dataset | Noise | Rooms | RT60 (s) | SNR (dB) | Samples |
|---------|-------|-------|----------|----------|---------|
| Train+Val | Synth + UrbanSound8K | R1, R2, R3 | 0.1–0.6 | 10–50 | 86400 + 9600 |
| Test | Unseen noises | R1', R2', R3' | 0.3–0.6 | 10–50 | 9600/room-SNR |

Motion modes: **static**, **constant-rate** (±12°/frame), **time-varying-rate** (periodic modulation, amplitude 5–55°).

## Results

### CRNN DoA Classification Accuracy

| Room | 10 dB | 20 dB | 30 dB | 40 dB | 50 dB |
|------|-------|-------|-------|-------|-------|
| R1' | 87.9% | 90.3% | 91.3% | 91.7% | 91.2% |
| R2' | 86.8% | 89.9% | 90.0% | 90.4% | 90.2% |
| R3' | 86.9% | 90.1% | 90.3% | 90.3% | 90.1% |

- >90% accuracy at SNR ≥ 20 dB; generalizes to unseen noise types and rooms

### Noise Reduction (Vacuum Cleaner, RT60 = 0.48 s, SNR = 30 dB)

**Constant-rate motion** (10°/s linear):
- PD-SFANC and DFG-SFANC maintain NRL > 15 dB for most of the duration
- D-SFANC shows one-frame lag with high-amplitude fluctuations
- FxLMS has limited performance due to slow convergence

**Time-varying-rate motion** (sinusoidal 50°–150°):
- PD-SFANC achieves stable, high noise reduction throughout
- DFG-SFANC exhibits significant drops at rapid-acceleration intervals (~7 s, ~15 s)
- FxLMS and D-SFANC show lower NRLs with greater fluctuations

### Key Comparison

| Method | Predictive? | Auto-tuned? | Moving source tracking |
|--------|-------------|-------------|----------------------|
| FxLMS | No | Step-size | Slow convergence, divergence risk |
| D-SFANC | No | N/A | One-frame lag |
| DFG-SFANC | Partial (pre-selection) | Manual tuning | Struggles with rapid acceleration |
| **PD-SFANC** | **Yes (CRNN)** | **Fully learned** | **Robust across motion patterns** |

## Key Contributions

1. **Predictive DoA estimation**: CRNN exploits multi-frame temporal context to forecast next-frame DoA, eliminating the reactive lag of D-SFANC
2. **Proactive filter selection**: Pre-selects the control filter for the upcoming frame, achieving delayless noise control during source transitions
3. **Fully learned parameters**: All CRNN parameters are trained end-to-end, removing the need for manual parameter tuning required by DFG-SFANC
4. **Lightweight architecture**: Only 0.05M parameters and 480M MACs, suitable for resource-constrained co-processors
5. **Robust generalization**: Validated on unseen noise types, rooms, and reverberation conditions with >90% DoA accuracy at SNR ≥ 20 dB

## Related Concepts

- [[../concepts/active-noise-control|Active Noise Control]] — core domain; this paper extends SFANC with predictive capability
- [[../concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]] — foundation; PD-SFANC adds DoA prediction to directional SFANC
- [[../concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — CRNN architecture used for DoA prediction (note: different from CRN encoder-decoder; this is CNN+GRU for classification)
- [[../concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]] — CRNN predicts next-frame DoA for proactive filter selection
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — used to pre-train the control filter library
- [[../concepts/moving-source-tracking|Moving Source Tracking]] — core problem addressed by this paper

## Related Synthesis

- [[../synthesis/ai-driven-anc|AI-Driven Active Noise Control]] — PD-SFANC is a neural selection method extending the SFANC paradigm
