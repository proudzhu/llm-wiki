---
type: source
created: 2026-04-30
updated: 2026-05-02
sources:
  - raw/papers/wang-2026-directional-sfanc-reverberant/full-text.md
  - https://arxiv.org/abs/2601.06981
  - zotero://select/items/0_4V3ESJXQ
tags:
  - active-noise-control
  - selective-fixed-filter-anc
  - direction-of-arrival
  - convolutional-neural-network
  - multi-task-learning
  - reverberant-environments
---

# Wang, Luo, Li, Shi, Ji, Yang & Gan 2026: Directional Selective Fixed-Filter ANC Based on CNN in Reverberant Environments

**Authors**: [[../entities/boxiang-wang|Boxiang Wang]], [[../entities/zhengding-luo|Zhengding Luo]], [[../entities/haowen-li|Haowen Li]], [[../entities/dongyuan-shi|Dongyuan Shi]], [[../entities/junwei-ji|Junwei Ji]], [[../entities/ziyi-yang|Ziyi Yang]], [[../entities/woon-seng-gan|Woon-Seng Gan]]
**Institutions**: School of Electrical and Electronic Engineering, Nanyang Technological University, Singapore; Center of Intelligent Acoustics and Immersive Communications, Northwestern Polytechnical University, China
**Published**: arXiv preprint, 2026-01-11
**Type**: Preprint
**DOI**: [10.48550/arXiv.2601.06981](https://doi.org/10.48550/arXiv.2601.06981)
**Zotero**: [4V3ESJXQ](zotero://select/items/0_4V3ESJXQ)

---

## Summary

Proposes a CNN-based directional SFANC method that incorporates DoA estimation in reverberant environments. A multi-task learning CNN estimates azimuth and elevation angles from multi-reference signals and selects the most appropriate pre-trained control filter at the frame level. Achieves ~96% azimuth and ~91% elevation classification accuracy with only 0.03M parameters, enabling delayless noise control with superior performance over FxLMS, SFANC, and GFANC in reverberant conditions.

---

## Problem Formulation

### Multi-Reference ANC Signal Model

In reverberant environments, the signal at the j-th microphone:

$$r_j(n) = q_j(n) * x(n)$$

where $q_j(n)$ is the room impulse response (RIR) between source and microphone j, $x(n)$ is the source signal.

Control signal driving the secondary source:

$$y(n) = \sum_{j=1}^{J} \mathbf{r}_j^T(n) \mathbf{w}_j(n)$$

Error signal at the error microphone:

$$e(n) = d(n) - \mathbf{y}^T(n) \mathbf{s}(n)$$

where $d(n)$ is the disturbance, $\mathbf{s}(n)$ is the secondary path impulse response.

### Key Gap

Existing SFANC methods focus on frequency content but overlook spatial information (DoA). Prior DoA-aware ANC methods are limited to free-field conditions and rely on traditional signal processing for DoA estimation, which fails in complex reverberant environments.

---

## Methodology

### Directional SFANC Architecture

Two-component system:
1. **Real-time controller**: Operates at sampling rate for noise cancellation
2. **Co-processor**: Frame-level DoA estimation and filter selection

![Figure 2: Block diagram of the proposed directional SFANC method.](raw/papers/wang-2026-directional-sfanc-reverberant/figures/control.png)
*Figure 2: The co-processor estimates DoA from reference signals via CNN and selects the corresponding pre-trained control filter at the frame level, while the controller applies the filter sample-by-sample for delayless noise cancellation.*

CNN output:

$$(\hat{\mathbf{p}}_{\text{azim}}, \hat{\mathbf{p}}_{\text{elev}}) = CNN(\mathbf{R}; \Theta^*)$$

where $\mathbf{R}$ is STFT spectrograms of J-channel reference signals, $\Theta^*$ is trained CNN parameters.

Estimated azimuth and elevation indices:

$$\hat{a} = \arg\max_{i} \hat{p}_{\text{azim},i}, \quad \hat{b} = \arg\max_{k} \hat{p}_{\text{elev},k}$$

### Pre-trained Control Filter Library

![Figure 4: Pre-trained control filter library spatial grid.](raw/papers/wang-2026-directional-sfanc-reverberant/figures/cflibrary.png)
*Figure 4: (a) Six azimuth classes in the horizontal plane (0°, 60°, 120°, 180°, 240°, 300°) and (b) three elevation classes in the vertical plane (90°, 30°, -30°), yielding 13 unique control filters.*

- Horizontal plane: 6 azimuth classes (0°, 60°, 120°, 180°, 240°, 300°)
- Vertical plane: 3 elevation classes (90°, 30°, -30°)
- Total: 13 control filters pre-trained with FxLMS for broadband noise (20–2020 Hz)

### CNN Architecture

![Figure 3: Architecture of the proposed CNN.](raw/papers/wang-2026-directional-sfanc-reverberant/figures/cnn.png)
*Figure 3: The CNN takes J-channel magnitude + phase spectrograms as input, processes them through three convolutional modules, and outputs azimuth and elevation class probabilities via two separate FC heads.*

| Layer | Configuration |
|-------|--------------|
| Input | J-channel magnitude + phase spectrograms (STFT) |
| Conv Module 1-3 | Conv → GroupNorm → ReLU → MaxPool |
| Pooling | Adaptive average pooling (frequency + time) |
| FC Layers | Two fully connected layers for azimuth and elevation |
| Output | Softmax probability distributions |

### Multi-Task Learning

Joint loss function:

$$Loss = Loss_{\text{azim}} + Loss_{\text{elev}}$$

Both tasks use cross-entropy loss. Shared representations enable efficient learning of both azimuth and elevation simultaneously.

---

## Experimental Setup

| Parameter | Value |
|:----------|:------|
| ANC System | 4×1×1 multi-reference (4 ref mics, 1 secondary, 1 error mic) |
| Reference Array | Tetrahedral, 2.5 cm diameter |
| Azimuth Classes | 6 (0°, 60°, 120°, 180°, 240°, 300°) |
| Elevation Classes | 3 (90°, 30°, -30°) |
| STFT | Hann window 1024, hop 64, 16 kHz |
| Training Samples | 46,080 (38,400 synthetic + 7,680 real) |
| Validation Samples | 5,760 |
| Test Samples | 4,800 (unseen noise types + environments) |
| RIR Generation | gpuRIR (image method) |
| Noise Sources | Bandlimited white noise + UrbanSound8K |
| Room Conditions | Varying sizes, RT60, array positions, SNR levels |

---

## Results

### DoA Estimation Accuracy

| Metric | Value |
|:-------|:------|
| Azimuth Accuracy | ~96% |
| Elevation Accuracy | ~91% |
| CNN Parameters | 0.03M |
| CPU Runtime | 7.83 ms |
| MACs | 119.86M |

Results obtained on unseen noise types and acoustic environments, demonstrating strong generalization.

### Noise Cancellation Performance

| Method | Relative Performance |
|:-------|:---------------------|
| FxLMS | Baseline (slow convergence) |
| SFANC | Better than FxLMS but ignores DoA |
| GFANC | Better than SFANC but no spatial awareness |
| **Directional SFANC** | **Best across all conditions** |

- Superior noise reduction across entire frequency band (100–700 Hz)
- Robust performance across all tested noise types (air conditioner, street traffic, etc.)
- Effective in reverberant environments where traditional DoA estimation fails

---

## Key Contributions

1. **First directional SFANC for reverberant environments**: Extends DoA-aware ANC beyond free-field assumptions
2. **CNN-based multi-task DoA estimation**: Simultaneous azimuth + elevation classification from multi-reference signals
3. **Low-complexity design**: 0.03M parameters, 7.83 ms CPU runtime, suitable for embedded deployment
4. **Frame-level filter selection**: Delayless noise control via real-time controller + co-processor architecture
5. **Strong generalization**: ~96% azimuth / ~91% elevation accuracy on unseen noise types and acoustic environments

---

## Related Concepts

- [[../concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]]
- [[../concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[../concepts/multi-channel-anc|Multi-Channel ANC]]

## Related Synthesis

- [[../synthesis/ai-driven-anc|AI-Driven ANC]]
- [[../synthesis/secondary-path-modeling-evolution|Secondary Path Modeling Evolution]]
