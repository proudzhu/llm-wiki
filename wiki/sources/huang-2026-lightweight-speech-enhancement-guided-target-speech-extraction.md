---
type: source
created: 2026-07-25
updated: 2026-07-25
sources:
  - raw/papers/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction/full-text.md
  - https://arxiv.org/abs/2508.19583
  - zotero://select/items/0_UJMWF4E2
tags:
  - target-speech-extraction
  - speech-enhancement
  - noisy-multi-speaker
  - enrollment-guidance
  - distortion-aware-training
  - lightweight-model
  - embedding-free
---

# Huang, Wu & Fan 2026: Lightweight Speech Enhancement Guided Target Speech Extraction in Noisy Multi-Speaker Scenarios

- **Authors**: [[entities/ziling-huang|Ziling Huang]]<sup>1,2†</sup>, Junnan Wu<sup>2</sup>, Lichun Fan<sup>2</sup>, Zhenbo Luo<sup>2</sup>, Jian Luan<sup>2</sup>, Haixin Guan<sup>3</sup>, [[entities/yanhua-long|Yanhua Long]]<sup>1,3∗</sup>
- **Affiliations**: <sup>1</sup>Shanghai Normal University, Shanghai, China; <sup>2</sup>MiLM Plus, Xiaomi Inc., Beijing, China; <sup>3</sup>Unisound AI Technology Co., Ltd., Beijing, China
- **Venue**: arXiv preprint (2508.19583), 2026-03-13
- **Type**: Preprint (eess.AS)
- **DOI**: [10.48550/arXiv.2508.19583](https://doi.org/10.48550/arXiv.2508.19583)
- **Code**: [github.com/isHuangZiling/D-LGTSE](https://github.com/isHuangZiling/D-LGTSE)
- **Zotero**: [UJMWF4E2](zotero://select/items/0_UJMWF4E2)

## Summary

Target speech extraction (TSE) performs poorly in noisy multi-speaker scenarios because noise in the mixture corrupts the enrollment-guided representation. Building on the embedding-free [[concepts/sef-pnet|SEF-PNet]] backbone, this paper proposes **LGTSE** and **D-LGTSE**: two frameworks that integrate a lightweight [[concepts/gtcrn|GTCRN]] denoiser (0.05 M params, 0.03 GMACs/s) to (1) produce **noise-agnostic enrollment guidance** by denoising the mixture before context interaction with enrollment speech, and (2) provide **distortion-aware training data** by using the mildly distorted denoised output as an additional training input. A two-stage pretrain + joint fine-tune strategy yields +0.89 dB SI-SDR, +0.16 PESQ, and +1.97% STOI over SEF-PNet on Libri2Mix (2-speaker + noise), and the approach generalizes to the stronger [[concepts/cie-mdptnet|CIE-mDPTNet]] backbone (+0.83 dB SI-SDR).

## Problem Formulation

Given enrollment speech $\mathbf{E} \in \mathbb{R}^{2F \times T_e}$ and noisy mixture $\mathbf{Y} \in \mathbb{R}^{2F \times T_y}$ (complex STFT with concatenated real/imaginary parts, dynamic-range compressed with $\beta = 0.5$), the baseline [[concepts/sef-pnet|SEF-PNet]] computes enrollment guidance via context interaction:

$$
\mathbf{E}_Y = \mathbf{E} \times \mathrm{softmax}\left(\mathbf{E}^{\mathrm{T}} \times \mathbf{Y}\right)
$$

The softmax is applied along the enrollment timeframe dimension. Because $\mathbf{Y}$ contains noise, the resulting guidance $\mathbf{E}_Y$ is **noise-contaminated**, which misleads the backbone in identifying the target speaker — especially under noisy multi-speaker conditions. Prior remedies (jointly trained enhancers, multi-stage coarse-to-fine extraction) either leave the guidance contaminated or nearly double the parameter count.

## Methodology

### Noise-agnostic Enrollment Guidance (LGTSE)

LGTSE inserts a lightweight [[concepts/gtcrn|GTCRN]] denoiser before context interaction. The noisy mixture $\mathbf{Y}$ is first denoised to $\mathbf{Y}_d$, then the guidance is computed against the denoised feature:

$$
\mathbf{Y}_d = \mathrm{GTCRN}(\mathbf{Y}), \qquad \mathbf{E}_{Y_d} = \mathbf{E} \times \mathrm{softmax}\left(\mathbf{E}^{\mathrm{T}} \times \mathbf{Y}_d\right)
$$

This yields a **noise-agnostic** target-speaker representation. The concatenated feature $[\mathbf{Y}; \mathbf{E}_{Y_d}]$ is passed to the backbone (base concatenation).

### Distortion-aware LGTSE (D-LGTSE)

D-LGTSE additionally exploits the fact that $\mathbf{Y}_d$ is not perfectly clean but mildly distorted, using it as a distortion-aware training signal. Three data-usage strategies are investigated (see [[concepts/distortion-aware-training|Distortion-aware Training]]):

1. **Distortion-aware concatenation** — concatenate $[\mathbf{Y}; \mathbf{Y}_d; \mathbf{E}_{Y_d}]$ along the channel dimension (single forward pass).
2. **On-the-fly** — enlarge each mini-batch with both original noisy and denoised pairs:
   $$\mathcal{B} = \{(\mathbf{Y}_i, \mathbf{E}_{Y_d}^i), \mathbf{Y}_{\text{target}}^i\}_{i=1}^N \cup \{(\mathbf{Y}_d^i, \mathbf{E}_{Y_d}^i), \mathbf{Y}_{\text{target}}^i\}_{i=1}^N$$
3. **Offline** — pre-process the entire dataset to form $\mathcal{D}_d$, then merge and shuffle:
   $$\mathcal{D}_{\text{mix}} = \mathrm{shuffle}(\mathcal{D} \cup \mathcal{D}_d)$$

The offline strategy stores distorted speech in advance, so the distortion signal persists throughout training (whereas concatenation/on-the-fly denoisers sharpen during joint fine-tuning, reducing residual distortion and limiting exposure to challenging conditions). Offline also reduces inference latency vs. concatenation.

### Two-stage Training

- **Stage 1 (pretraining)**: GTCRN is trained for SE on noisy 2-speaker+noise mixtures (ground-truth: clean 2-speaker mixture $\mathbf{y}_{\text{clean}}$); the backbone is trained from scratch for TSE using GTCRN's denoised output + enrollment.
- **Stage 2 (joint fine-tuning)**: GTCRN is unfrozen and the entire system is fine-tuned end-to-end.

Joint loss combining denoising and TSE objectives:

$$
\mathcal{L} = -\mathrm{SI\text{-}SDR}(\mathbf{y}_d, \mathbf{y}_{\text{clean}}) - \mathrm{SI\text{-}SDR}(\hat{\mathbf{y}}_{\text{target}}, \mathbf{y}_{\text{target}})
$$

### Architecture

![[raw/papers/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction/figures/e10a721e96b6d90252f27d4db2d53d65e7615e1e9c5c5b274c96f4946db93ede.jpg|LGTSE and D-LGTSE architecture (upper) and simplified SEF-PNet baseline (lower)]]

*Figure 1: Architecture of the proposed LGTSE (a, base concatenation) and D-LGTSE (b, distortion-aware concatenation), and the simplified SEF-PNet baseline. GTCRN denoises the noisy speech before context interaction with enrollment.*

The backbone [[concepts/sef-pnet|SEF-PNet]] (simplified: the iterative feature integration block is removed for fair comparison) consists of an encoder, decoder, Temporal Convolutional Network (TCN), PyramidBlock, and Deconv2d. [[concepts/gtcrn|GTCRN]] consists of an encoder (two Conv blocks + three GT-Conv blocks), a grouped dual-path RNN (G-DPRNN) bottleneck, and a symmetric decoder, operating in the ERB domain. [[concepts/cie-mdptnet|CIE-mDPTNet]] is also evaluated as a stronger SOTA backbone.

## Experimental Setup

| Aspect | Configuration |
|:-------|:--------------|
| **Dataset** | Libri2Mix "mix both" (2-speaker + noise), 8 kHz, "minimum" mode |
| **Train set** | 13,900 utterances, 251 speakers |
| **Dev / Test set** | 3,000 utterances, 40 speakers each |
| **Target speaker** | First speaker only |
| **STFT** | Hanning window, 32 ms length, 8 ms shift |
| **Optimizer** | Adam, initial lr $5 \times 10^{-4}$ |
| **LR schedule** | $\times 0.98$ every 2 epochs (first 100 epochs); $\times 0.9$ (last 20 epochs) |
| **Gradient clipping** | Max L2-norm = 1 |
| **Epochs** | 150 |
| **Metrics** | SI-SDR (dB), PESQ, STOI (%) |
| **Backbones** | SEF-PNet (simplified, embedding-free); CIE-mDPTNet (SOTA) |

## Results

### Overall Results (Table 1)

| ID | Method | SI-SDR (dB) | PESQ | STOI (%) |
|:---|:-------|:-----------:|:----:|:--------:|
| E0 | Unprocessed | -2.03 | 1.43 | 64.65 |
| E1 | [[concepts/sef-pnet\|SEF-PNet]] [baseline] | 7.43 | 2.14 | 80.31 |
| E2 | LGTSE | 7.88 | 2.21 | 81.27 |
| E3 | D-LGTSE (Concat) | 7.96 | 2.24 | 81.37 |
| E4 | D-LGTSE (On-the-fly) | 8.10 | 2.28 | 81.80 |
| E5 | **D-LGTSE (Offline)** | **8.32** | **2.30** | **82.28** |
| F0 | [[concepts/cie-mdptnet\|CIE-mDPTNet]] [SOTA baseline] | 10.87 | 2.73 | 87.26 |
| F1 | **D-LGTSE-mDPTNet (Offline)** | **11.70** | **2.86** | **88.83** |

- LGTSE improves over SEF-PNet by **+0.45 dB SI-SDR**, validating noise-agnostic guidance alone.
- D-LGTSE (Offline) achieves the best overall result: **+0.89 dB SI-SDR, +0.16 PESQ, +1.97% STOI** over SEF-PNet.
- On the stronger CIE-mDPTNet backbone, D-LGTSE-mDPTSE adds **+0.83 dB SI-SDR, +0.13 PESQ, +1.57% STOI**, demonstrating generalizability across backbones. Absolute metrics under CIE-mDPTNet exceed SEF-PNet mainly because CIE-mDPTNet incurs ~3× higher computational cost (Table 2).

### Model Size and Complexity (Table 2)

| Model | Params (M) | MACs (G/s) |
|:------|:----------:|:----------:|
| GTCRN (denoiser only) | 0.05 | 0.03 |
| SEF-PNet | 6.08 | 8.50 |
| D-LGTSE | 6.13 | 8.53 |
| CIE-mDPTNet | 2.87 | 22.25 |
| D-LGTSE-mDPTNet | 2.92 | 22.28 |

Adding GTCRN to either backbone costs only **+0.05 M params and +0.03 GMACs/s** — a negligible overhead for the measured gains, justifying the "lightweight" claim.

### Ablation: Training Strategy (Table 3)

| ID | Training Method | SI-SDR (dB) | PESQ | STOI (%) |
|:---|:----------------|:-----------:|:----:|:--------:|
| S0 | GTCRN* + backbone* (separately pretrained, stacked) | 7.60 | 2.15 | 80.64 |
| S1 | GTCRN* + backbone (GTCRN frozen, backbone trained) | 8.02 | 2.26 | 81.41 |
| E5 | **Two-stage Training (joint fine-tune)** | **8.32** | **2.30** | **82.28** |

Simple stacking (S0) yields limited gains; tighter integration (S1) helps; end-to-end joint fine-tuning (E5) is crucial for fully exploiting distortion-aware learning.

### Visualization of Noise-agnostic Enrollment Guidance

![[raw/papers/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction/figures/6539eba53bb36574e7ffde0073cd95084da70e098b96298e688f6bc68022a004.jpg|Enrollment guidance spectrogram comparison]]

*Figure 2: Noise-agnostic enrollment guidance analysis. Top row: guidance from direct context interaction between enrollment and noisy speech. Bottom row: guidance produced with the proposed noise-agnostic (denoised) interaction. Denoising via GTCRN visibly suppresses noise components in the guidance.*

## Key Contributions

1. **LGTSE** — introduces a lightweight noise-agnostic enrollment guidance scheme where context interaction is performed between GTCRN-denoised speech and clean enrollment, avoiding direct interaction with noisy mixtures. The new concept is documented at [[concepts/noise-agnostic-enrollment-guidance|Noise-agnostic Enrollment Guidance]].
2. **D-LGTSE** — extends LGTSE by using the mildly distorted denoised output as additional training data, exposing the model to distortion and enhancing robustness. Three distortion-aware data strategies (concatenation, on-the-fly, offline) are investigated, with offline performing best. See [[concepts/distortion-aware-training|Distortion-aware Training]].
3. **Two-stage training** — a progressive strategy (GTCRN pretrain + backbone pretrain → end-to-end joint fine-tune) that yields consistent gains over frozen or separately-trained stacking.
4. **Generalizability** — the framework improves both the CNN-based SEF-PNet backbone and the SOTA CIE-mDPTNet backbone, at negligible parameter/MAC overhead (+0.05 M, +0.03 GMACs/s).

## Related Concepts

- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/noise-agnostic-enrollment-guidance|Noise-agnostic Enrollment Guidance]]
- [[concepts/distortion-aware-training|Distortion-aware Training]]
- [[concepts/sef-pnet|SEF-PNet]]
- [[concepts/cie-mdptnet|CIE-mDPTNet]]
- [[concepts/gtcrn|GTCRN]]
- [[concepts/personalized-speech-enhancement|Personalized Speech Enhancement]]
- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/erb-scale|ERB Scale]]

## Related Synthesis

- (None — the paper does not cross-reference existing synthesis pages; its efficiency data point for GTCRN reuse as a TSE front-end is noted on [[concepts/gtcrn|GTCRN]] rather than on the ANC-focused efficiency synthesis.)
