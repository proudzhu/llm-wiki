---
type: source
created: 2026-05-16
updated: 2026-05-16
sources:
  - raw/papers/wang-2022-fusing-bc-ac-complex-domain-se/full-text.md
  - https://doi.org/10.1109/TASLP.2022.3209943
  - zotero://select/items/0_K592VRRE
tags:
  - bone-conduction
  - speech-enhancement
  - complex-spectral-mapping
  - attention-mechanism
  - multimodal-fusion
  - semi-supervised-learning
  - cyclegan
---

# Wang, Zhang & Wang 2022: Fusing BC and AC Sensors for Complex-Domain Speech Enhancement

**Authors**: [[entities/heming-wang|Heming Wang]], [[entities/xueliang-zhang|Xueliang Zhang]], [[entities/deliang-wang|DeLiang Wang]]
**Institutions**: Ohio State University; Inner Mongolia University
**Published**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, Vol. 30, pp. 3134–3143, 2022
**Type**: Journal Article
**DOI**: [10.1109/TASLP.2022.3209943](https://doi.org/10.1109/TASLP.2022.3209943)
**Zotero**: [K592VRRE](zotero://select/items/0_K592VRRE)

## Summary

This paper proposes an attention-based fusion method to combine air-conduction (AC) and bone-conduction (BC) signals for complex spectral mapping-based speech enhancement. The key insight is that AC provides full-band information susceptible to noise, while BC is noise-immune but bandwidth-limited (<2 kHz). The approach additionally introduces a CycleGAN-based semi-supervised framework that leverages unpaired AC data (AISHELL-1) alongside limited parallel AC-BC data (ESMB corpus), achieving supervised-level performance with only 50% parallel data.

## Problem Formulation

Given simultaneous recordings from BC and AC sensors:

$$y[k] = s[k] + n[k]$$

where $y$ is the noisy AC signal and $s$ the clean speech. In the STFT domain:

$$\hat{S}[t,f] = g(\theta, Y[t,f], Y_{BC}[t,f])$$

The model $g$ recovers clean speech $\hat{S}$ in the complex domain using both noisy AC spectrogram $Y$ and BC spectrogram $Y_{BC}$.

## Methodology

### DC-CRN (Densely Connected CRN)

The backbone is a CRN (Convolutional Recurrent Network) with encoder–decoder + BLSTM bottleneck, where each convolution is replaced by **Densely Connected (DC) blocks**: 4 standard convolutions + 1 gated convolution, with dense skip connections across all layers:

$$x_{cat} = \text{Concat}(x_1, x_2, x_3, x_4)$$
$$x = \text{conv1}(x_{cat}) \odot \sigma(\text{conv2}(x_{cat}))$$

Pointwise convolution skip connections (replacing concatenation) reduce memory while boosting feature fusion.

### Attention-Based Fusion (AFF)

![[raw/papers/wang-2022-fusing-bc-ac-complex-domain-se/figures/469f782899b5b8c1857d6ec81a9246f10e2b66418047355996267f588a2b8dfe.jpg|Attention-based fusion strategy]]

*Figure 1: Attention-based fusion — an attention score M from local+global contexts soft-selects between AC and BC features, then concatenation with original signals feeds DC-CRN.*

The attention-fused feature is computed as:

$$Y_{AFF}[t,f] = M \cdot Y[t,f] + (1 - M) \cdot Y_{BC}[t,f]$$
$$Y_{feat}[t,f] = \text{Concat}(Y[t,f], Y_{BC}[t,f], Y_{AFF}[t,f])$$

This concatenation design preserves both cross-modal and single-modal features (addition-only loses single-modal info, ablation shows −5.3% STOI drop).

### Training Objective

Complex RI-Mag loss:

$$L_{RI-Mag}(S, \hat{S}) = L_{RI} + L_{Mag}$$

where $L_{RI}$ is MAE on real/imaginary parts and $L_{Mag}$ is MAE on magnitudes.

### Semi-Supervised CycleGAN Framework

![[raw/papers/wang-2022-fusing-bc-ac-complex-domain-se/figures/4ce32bf6001948c4874756b926f74bcaaf108d578d3482b5c517a6d1dd6ae425.jpg|CycleGAN semi-supervised framework]]

*Figure 2: CycleGAN-based semi-supervised framework — Generator A (AC-BC→Clean) and Generator B (Clean→BC) are trained with adversarial, cycle consistency, identity, and supervised losses.*

Total loss:

$$L_{total} = L_D + L_G + \alpha L_{cycle} + \beta L_{identity} + \gamma L_{sup}$$

with $\alpha=5.0$, $\beta=2.0$, $\gamma=5.0$. The cycle loss maps noisy → clean → BC → reconstructed-BC, enabling training on unpaired AC data from AISHELL-1.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Dataset (supervised) | ESMB corpus (128h, 287 speakers, Chinese, 16 kHz, Elevoc Clear earbuds) |
| Dataset (semi-supervised) | ESMB + AISHELL-1 (178h, 400 speakers, unpaired AC) |
| Noise set | DNS challenge (20000 files) + Auditec/NOISEX92 for test |
| SNR range (train) | {−5, −4, −3, −2, −1, 0} dB |
| SNR range (test) | −5, 0, 5 dB |
| Sampling rate | 8 kHz |
| STFT | 32ms window, 50% overlap, 129 freq bins |
| BC preprocessing | 8th-order Butterworth LPF + MVN |
| Optimizer | Adam, lr=6e-4 (supervised); 4e-4/2e-4 gen/disc (semi-sup) |
| Training | 30 epochs (sup); 120k iterations (semi-sup) |
| Metrics | STOI, PESQ |

## Results

### Supervised: Fusion Strategies Compared

| Method | STOI (−5 dB) | PESQ (−5 dB) |
|--------|:---:|:---:|
| FCN (EF) [Yu 2020] | — | — |
| FCN (AF) [Yu 2020] | — | — |
| DC-CRN (EF) | Baseline | Baseline |
| DC-CRN (LF) | +slight | +slight |
| **DC-CRN (AF, proposed)** | **+21.1% over FCN-AF** | **+0.83 over FCN-AF** |

Attention-based fusion consistently outperforms early-fusion and late-fusion at all SNRs.

### Single-Sensor vs. Sensor Fusion

At −5 dB SNR: AC-BC fusion → +11.6% STOI, +0.65 PESQ over AC-only DC-CRN. At 5 dB, the gap narrows to +1.7% STOI (BC advantage diminishes as AC quality improves).

BC-only (bandwidth extension) outperforms AC-only at −5 dB, demonstrating BC's noise immunity advantage in extreme conditions.

### Semi-Supervised

| Paired data | Supervised PESQ | Semi-supervised PESQ | Δ |
|:---:|:---:|:---:|:---:|
| 1% | Low | +0.38 | +8.6% STOI |
| 50% | Baseline (100% sup) | ≈100% supervised | Match |
| 100% | Best | Slightly better | Small gain |

With 50% paired data + unpaired AISHELL-1, the CycleGAN framework **matches full supervised performance** — critical for practical deployment where parallel BC data is scarce.

### Ablation

| Variant | STOI drop | PESQ drop |
|---------|:---:|:---:|
| Remove DC blocks | −5.3% | −0.29 |
| Remove gated conv | −2.2% | −0.19 |
| Concatenation skip (vs pointwise) | −small | −small |
| Addition fusion (vs concatenation) | −significant | −significant |

## Key Contributions

1. **Attention-based AC-BC fusion** in the complex domain — outperforms time-domain FCN baseline by 21.1% STOI at −5 dB
2. **DC-CRN architecture** with pointwise skip connections — lightweight variant of densely-connected CRN
3. **Semi-supervised CycleGAN framework** for AC-BC fusion when paired data is limited — 50% data matches 100% supervised
4. **Systematic comparison** of early/late/attention fusion strategies with ablation of key components
5. **ESMB corpus evaluation** establishing a benchmark for BC/AC sensor fusion SE

## Related Concepts

- [[concepts/bone-conduction|Bone Conduction]]
- [[concepts/complex-spectral-mapping|Complex Spectral Mapping]]
- [[concepts/iterative-attentional-feature-fusion|Iterative Attentional Feature Fusion (iAFF)]]
- [[concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]]
- [[concepts/sensor-failure-robust-fusion|Sensor-Failure Robust Multi-Modal Fusion]]

## Related Synthesis

- [[synthesis/multimodal-bc-speech-enhancement|Multimodal BC Speech Enhancement]]
- [[synthesis/multi-modal-speech-enhancement|Multi-Modal Speech Enhancement]]
