---
type: source
created: 2026-05-01
updated: 2026-05-01
sources:
  - raw/papers/yin-2023-selective-fixed-filter-anc-headphones/full-text.md
  - https://doi.org/10.1016/j.apacoust.2023.109505
  - zotero://select/items/0_4MBBAJXH
tags:
  - active-noise-control
  - fixed-filter-anc
  - frequency-response-matching
  - headphones
  - online-modelling
---

# Yin, Zhang, Wu, Zhou, Guo, Yang & Zhang 2023: Selective Fixed-Filter ANC Based on Frequency Response Matching in Headphones

**Authors**: [[entities/lan-yin|Lan Yin]], [[entities/zeqiang-zhang|Zeqiang Zhang]], [[entities/ming-wu|Ming Wu]], [[entities/shuang-zhou|Shuang Zhou]], [[entities/jianfeng-guo|Jianfeng Guo]], [[entities/jun-yang|Jun Yang]], [[entities/jianing-zhang|Jianing Zhang]]

**Institution**: Key Laboratory of Noise and Vibration Research, Institute of Acoustics, Chinese Academy of Sciences; University of Chinese Academy of Sciences

**Venue**: Applied Acoustics, Volume 211, August 2023, Pages 109505

**Year**: 2023 | **Type**: Journal Article | **DOI**: [10.1016/j.apacoust.2023.109505](https://doi.org/10.1016/j.apacoust.2023.109505) | [Zotero](zotero://select/items/0_4MBBAJXH)

## Summary

Proposes FRM-SFANC, a selective fixed-filter ANC algorithm for headphones that uses **online frequency response matching** to select the most appropriate pre-trained control filter for variable primary noise. Unlike CNN-based SFANC methods that rely on deep learning classifiers, FRM-SFANC uses a computationally lightweight online modelling approach to compare the estimated primary path frequency response against pre-trained filter profiles, achieving robust filter selection without training data or neural network inference.

## Problem Formulation

Most ANC headphones use fixed-filter methods optimized for specific noise conditions. When the primary noise's spectral characteristics or direction changes significantly, the fixed filter delivers unsatisfactory performance. The core problem is: **how to select the best pre-trained control filter in real time without adaptive algorithms' convergence delays?**

The paper models the ANC process as a **hidden Markov model (HMM)**, where:
- The optimal control filter $\mathbf{w}_o$ is the hidden state
- The reference signal $\mathbf{x}(n)$ is the observation
- The predicted probability of the next-step optimal filter is proportional to the current likelihood: $P[\mathbf{w}_o(n+1) = \mathbf{w}_i | \mathbf{x}(0), \ldots, \mathbf{x}(n)] \propto P[\mathbf{x}(n) | \mathbf{w}_o(n) = \mathbf{w}_j]$

This converts the ANC problem into a **control filter selection problem**:

$$\mathbf{w}_o(n+1) = \underset{\mathbf{w} \in \{\mathbf{w}_i\}_{i=1}^{M}}{\arg\max} \{P[\mathbf{x}(n) | \mathbf{w}]\}$$

## Methodology

### FRM-SFANC Algorithm

The FRM-SFANC method consists of three stages:

1. **Pre-training control filters**: Use FxLMS to derive $M$ optimal control filters for $M$ broadband white noises with different frequency ranges. Store in a filter database.

2. **Online frequency response matching**: An online modelling approach estimates the primary path frequency response in real time. The estimated response is compared against the frequency response profiles associated with each pre-trained filter. The filter whose profile best matches the estimated response is selected.

3. **Real-time noise cancellation**: The selected filter is applied immediately for noise control. Since the matching process runs in parallel with the real-time controller, there is no processing delay.

### Key Equations

The noise label assignment (which filter is best for a given noise):

$$l_i = \underset{j \in \{1, 2, \ldots, M\}}{\arg\min} \mathbb{E}\{[e_i(n)]^2\}$$

Noise reduction level (NR) metric:

$$\text{NR} = 10\log_{10}\frac{\sum_{n=1}^{L} d^2(n)}{\sum_{n=1}^{L} e^2(n)}$$

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Platform | Headphone ANC system |
| Sampling rate | 16 kHz (simulation); real-time hardware |
| Control filter length | 1024 taps (simulation), 512 taps (real-time) |
| Pre-trained filters | 7 ($B_0$ to $B_6$) |
| Primary/secondary paths | Synthetic bandpass filters (simulation); real acoustic paths (experiment) |
| Noise types | 7 broadband white noises with different frequency ranges |
| Comparison algorithms | FxLMS (step size = 0.0001) |

## Results

### Simulation Results (Real-Recorded Noises)

| Noise Type | CNN-SFANC NR | FxLMS NR |
|------------|-------------|----------|
| Aircraft noise | 16.82 dB | 4.15 dB |
| Compressor noise | 15.39 dB | 7.29 dB |

- SFANC responds much faster: achieves >10 dB NR after the first second vs. FxLMS taking >40 seconds
- SFANC effectively attenuates 200–700 Hz frequency components

### Real-Time Experiment Results (4-Channel ANC Window)

**Broadband noise cancellation** (Table 5):

| Broadband Noise | ANC Off | ANC On | NR | Selected Filter |
|----------------|---------|--------|-----|----------------|
| 200–700 Hz | 73.61 dBA | 55.79 dBA | 17.82 dB | $B_0$ |
| 200–450 Hz | 74.17 dBA | 53.43 dBA | 20.74 dB | $B_1$ |
| 450–700 Hz | 70.42 dBA | 54.70 dBA | 15.72 dB | $B_2$ |
| 200–325 Hz | 75.10 dBA | 56.62 dBA | 18.48 dB | $B_3$ |
| 325–450 Hz | 68.44 dBA | 56.06 dBA | 12.38 dB | $B_4$ |
| 450–575 Hz | 70.33 dBA | 57.57 dBA | 12.76 dB | $B_5$ |
| 575–700 Hz | 68.48 dBA | 52.26 dBA | 16.22 dB | $B_6$ |

**Real noise cancellation** (Table 6):

| Real Noise | ANC Off | ANC On | NR |
|-----------|---------|--------|-----|
| Aircraft | 72.36 dBA | 60.07 dBA | 12.29 dB |
| Compressor | 73.90 dBA | 61.47 dBA | 12.43 dB |

### Transferability

The 2D CNN model trained on **synthetic acoustic paths** was directly applied to **real acoustic paths** without retraining, and still correctly classified all broadband noises. This demonstrates good transferability across diverse acoustic scenarios.

## Key Contributions

1. **FRM-SFANC algorithm**: Proposes a frequency response matching mechanism for selective fixed-filter ANC, providing a computationally efficient alternative to CNN-based selection
2. **HMM theoretical framework**: Formally derives the SFANC problem as a hidden Markov model, providing theoretical justification for filter selection based on reference signal likelihood
3. **Real-time implementation**: Demonstrates the method in a 4-channel ANC window with co-processor + real-time controller architecture, achieving delayless noise control
4. **Transferability validation**: Shows that the 2D CNN trained on synthetic paths transfers to real acoustic environments without retraining
5. **Explainability via LayerCAM**: Uses LayerCAM to reveal that the CNN's filter selection is primarily based on noise frequency band information — the network focuses on high-intensity spectral content

## Related Concepts

- [[concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]] — the broader framework this paper contributes to
- [[concepts/active-noise-control|Active Noise Control]] — parent domain
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — used to pre-train control filters
- [[concepts/feedforward-anc|Feedforward ANC]] — system architecture used
- [[concepts/frequency-response-matching|Frequency Response Matching]] — core mechanism of FRM-SFANC

## Related Sources

- [[sources/wang-2026-predictive-dsfanc-crnn|Wang 2026: Predictive Directional SFANC via CRNN]] — extends SFANC with DoA prediction
- [[sources/wang-2026-directional-sfanc-reverberant|Wang 2026: Directional SFANC in Reverberant Environments]] — CNN-based directional SFANC
- [[sources/luo-2026-hybrid-gfanc-fxnlms|Luo 2026: Hybrid GFANC-FxNLMS]] — generative filter selection with adaptive refinement
