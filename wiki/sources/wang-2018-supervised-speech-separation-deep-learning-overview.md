---
type: source
created: 2026-06-01
updated: 2026-06-01
sources:
  - raw/papers/wang-2018-supervised-speech-separation-deep-learning-overview/full-text.md
  - https://doi.org/10.1109/TASLP.2018.2842159
  - zotero://select/items/0_D79MZFJA
tags:
  - speech-separation
  - deep-learning
  - supervised-learning
  - speech-enhancement
  - speaker-separation
  - time-frequency-masking
  - survey
---

# DeLiang Wang & Jitong Chen 2018: Supervised Speech Separation Based on Deep Learning: An Overview

**Authors**: [[entities/deliang-wang|DeLiang Wang]], [[entities/jitong-chen|Jitong Chen]]
**Affiliation**: Ohio State University
**Venue**: IEEE/ACM Transactions on Audio, Speech, and Language Processing
**Year**: 2018
**Type**: Journal Article (Survey)
**Volume**: 26, Issue 10, pp. 1702-1726
**DOI**: [10.1109/TASLP.2018.2842159](https://doi.org/10.1109/TASLP.2018.2842159)
**IEEE Link**: [8369155](https://ieeexplore.ieee.org/document/8369155/)
**Zotero**: [D79MZFJA](zotero://select/items/0_D79MZFJA)

---

## Summary

This comprehensive survey reviews deep-learning-based supervised speech separation, covering the three main components -- learning machines, training targets, and acoustic features -- along with monaural and array-based separation algorithms. It traces the evolution from traditional signal-processing approaches (spectral subtraction, CASA, beamforming) through the formulation of speech separation as a supervised learning problem, to modern deep neural network methods. The paper systematically compares training targets (masking-based vs. mapping-based), evaluates acoustic features for their discriminative power, and discusses critical generalization issues for noise-, speaker-, and condition-independent separation. It also proposes a concrete definition of a solution to the cocktail party problem: a system that elevates hearing-impaired speech intelligibility to normal-hearing levels in all conditions.


## Problem Formulation

Speech separation is framed as the task of extracting target speech from background interference (nonspeech noise, competing speakers, or reverberation). The supervised learning formulation treats separation as a **classification** (binary mask estimation) or **regression** (spectral mapping) problem.

---

## Methodology

### Learning Machines

The paper reviews four DNN families: Feedforward MLPs, CNNs, RNNs with LSTM, and GANs. LSTM is essential for speaker generalization.

### Training Targets

**Masking-based targets**: [[concepts/ideal-binary-mask|Ideal Binary Mask (IBM)]], Ideal Ratio Mask (IRM), Spectral Magnitude Mask (SMM), Phase-Sensitive Mask (PSM), Complex Ideal Ratio Mask (cIRM), Signal Approximation (SA).

**Mapping-based targets**: Target Magnitude Spectrum (TMS), Gammatone Frequency Target Power Spectrum (GF-TPS).

Masking-based targets outperform mapping-based targets for intelligibility.

### Acoustic Features

**Multi-Resolution Cochleagram (MRCG)** is the best-performing feature. Recommended combination: PNCC + GF + LOG-MEL (enhancement) or PNCC + GFCC + LOG-MEL (speaker separation).

---

## Key Contributions

1. Comprehensive survey organizing supervised speech separation into three pillars.
2. Training target systematization with quantitative comparison.
3. Multi-Resolution Cochleagram (MRCG) feature.
4. Large-scale training with 10,000 noises for noise-independent models.
5. LSTM for speaker generalization.
6. Cocktail party solution definition: HI intelligibility matching NH in all conditions.
7. Feature importance quantification across multiple conditions.
8. DNN-based beamforming integration.

---

## Related Concepts

- [[concepts/ideal-binary-mask|Ideal Binary Mask (IBM)]]
- [[concepts/ideal-ratio-mask|Ideal Ratio Mask (IRM)]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cIRM)]]
- [[concepts/permutation-invariant-training|Permutation Invariant Training (PIT)]]
- [[concepts/deep-clustering-speech-separation|Deep Clustering for Speech Separation]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/neural-beamforming|Neural Beamforming]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/complex-spectral-mapping|Complex Spectral Mapping]]
- [[concepts/self-supervised-speech-representation|Self-Supervised Speech Representation]]
- [[concepts/diffusion-models-for-speech|Diffusion Models for Speech]]

## Related Synthesis

- [[synthesis/multi-modal-speech-enhancement|Multi-Modal Speech Enhancement]]
- [[synthesis/multimodal-bc-speech-enhancement|Multimodal BC Speech Enhancement]]

## Related Sources

- [[sources/tan-2018-convolutional-recurrent-network-speech-enhancement|Tan & Wang 2018: CRN for Real-Time Speech Enhancement]]
- [[sources/wang-2022-fusing-bc-ac-complex-domain-se|Wang, Zhang & Wang 2022: Fusing BC and AC for Complex-Domain SE]]
- [[sources/wang-2026-cross-talk-speech-reduction-separation|Wang & Cornell 2026: Cross-Talk Speech Reduction]]


