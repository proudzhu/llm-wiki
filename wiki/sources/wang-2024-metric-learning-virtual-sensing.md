---
type: source
created: 2026-04-18
updated: 2026-04-28
sources:
  - raw/papers/wang-2024-metric-learning-virtual-sensing/full-text.txt
  - https://doi.org/10.48550/arXiv.2409.05470
  - zotero://select/items/0_NBYTXNH4
tags:
  - active-noise-control
  - cnn
  - metric-learning
  - transfer-learning
  - virtual-sensing
aliases:
  - 'Wang 2024: Transferable Selective Virtual Sensing'
---

# Wang 2024: Transferable Selective Virtual Sensing Active Noise Control Technique Based on Metric Learning

**Authors**: Boxiang Wang, Dongyuan Shi, Zhengding Luo, Xiaoyi Shen, Junwei Ji, Woon-Seng Gan
**Institution**: Nanyang Technological University, Singapore
**Published**: arXiv (Preprint), 2024
**DOI**: [10.48550/arXiv.2409.05470](https://doi.org/10.48550/arXiv.2409.05470)
**📎 Zotero**: [zotero://select/items/0_NBYTXNH4](zotero://select/items/0_NBYTXNH4)
**Code**: [GitHub](https://github.com/WangBoxiang/Transferable-Selective-Virtual-Sensing-Active-Noise-Control)

## Summary

This paper proposes a **Transferable Selective Virtual Sensing** method that utilizes **Metric Learning** to avoid the labor-intensive retraining of CNN-based filter selectors. By using a pre-trained feature extractor and similarity matching (Cosine Similarity), the system can be deployed on new ANC platforms and handle unseen noise types with minimal effort.

## Problem Formulation

### The Scalability Gap in Neural Virtual Sensing

[[../concepts/virtual-sensing|Virtual Sensing]] (VS) using Auxiliary Filters (AF-VS) is sensitive to changes in noise characteristics. While **Cognitive Virtual Sensing (CVS)** uses CNNs to select appropriate AFs, it suffers from:
- **High Labeling Effort**: Requires retraining for every new ANC platform or noise environment
- **Generalization Failure**: Conventional classifiers cannot handle noise types or acoustic paths not seen during training
- **Resource Constraints**: Retraining deep models on embedded controllers is impractical

**Proposed Goal**: A **Transferable** system that uses a single pre-trained feature extractor across different ANC systems without retraining, even for unseen noise.

## Methodology

### 1. Metric Learning & Similarity Matching

The authors pivot from a "classification" task to a "similarity" task using **Metric Learning**.

#### 1.1 Lightweight 1D CNN Feature Extractor

A simple architecture (13K parameters) consisting of:
- One convolutional layer
- One residual block
- Max-pooling for complexity reduction
- *Discarded in target system*: The final fully connected (FC) layers used for original classification

#### 1.2 Similarity-Based Selection

Instead of predicting a class, the system calculates the **Cosine Similarity** between the embedding of the current noise ($E_x$) and the precomputed embeddings of the training noises for the available AFs ($E_q$):

```
S_q = (E_x^T · E_q) / max(||E_x||_2 · ||E_q||_2, α)
```

The filter with the highest similarity score is selected online.

#### 1.3 Transferability

Since the convolutional layers learn generic acoustic features (frequency distributions, non-stationarity), they can be "transferred" to new systems. In a new system, the user only needs to precompute embeddings for their local AF training noises using the frozen CNN.

### 2. CNN-Based Selective Virtual Sensing (Background)

The conventional AF-VS technique consists of two stages:

**Tuning stage**: Error microphone placed at desired location, optimal control filter:
```
W_opt(z) = P_v(z) / S_v(z)
```

Optimal auxiliary filter:
```
H_o(z) = P_p(z) - S_p(z) · W_opt(z)
```

**Control stage**: Virtual error microphone removed, AF helps train new control filter by minimizing:
```
E_h(z) = E_p(z) - H_o(z) · X(z) = S_p(z)[W_opt(z) - W(z)]X(z)
```

## Key Findings

### Performance vs. Complexity

| Metric | Result |
|--------|--------|
| Parameters | 13K (vs 3.9M for M34-res) |
| Accuracy on unseen classes | 92.6% (vs 36.6% for M34-res) |
| Feature extraction complexity | 6x less than full CNN |

**Simplicity Wins**: The proposed 13K-parameter network achieved **92.6% accuracy** on unseen classes, outperforming much larger models like M34-res (3.9M parameters, 36.6% accuracy) which overfitted the original training set.

### Noise Reduction

- **Broadband & Real-world**: Simulations on genset and compressor noise (unseen during training) showed performance **nearly on par with optimal control** (direct virtual mic access)
- **Superiority**: Achieved significant gains over full-band AF and standard selective VS in suddenly-varying noise scenarios

## Critical Review and Insights

- **Architectural Shift**: This represents a shift from "End-to-End Black Box" (like [[holzmueller-2026-obs-tasnet-virtual-sensing|Obs-TasNet]]) to a "Hybrid Feature-Based" approach. While Obs-TasNet estimates filter coefficients directly, Wang's method selects from a pre-trained library.
- **Deployment**: Ideal for TWS earbuds where developers want a "pre-trained acoustic brain" that works out of the box for various product SKUs without site-specific AI expertise.

## Related Concepts

- [[../concepts/virtual-sensing|Virtual Sensing]]
- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]

## Related Synthesis

- [[../synthesis/virtual-sensing-evolution|Evolution of Virtual Sensing in ANC]]
- [[../synthesis/ai-driven-anc|AI-Driven ANC]]

## Related Entities

- [[../entities/boxiang-wang|Boxiang Wang]]
- [[../entities/dongyuan-shi|Dongyuan Shi]]
- [[../entities/woon-seng-gan|Woon-Seng Gan]]
