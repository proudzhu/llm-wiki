---
type: concept
created: 2026-11-01
updated: 2026-11-01
sources:
  - raw/papers/yan-2025-lisennet/full-text.md
tags:
  - speech-enhancement
  - lightweight-model
  - dual-path
  - real-time
  - neural-network-architecture
---

# LiSenNet

**LiSenNet** (Lightweight Speech Enhancement Network) is an ultra-lightweight monaural speech enhancement model proposed by Yan et al. (ICASSP 2025). It achieves PESQ 3.07 / STOI 0.939 on VoiceBank+DEMAND with only **37k parameters and 56M MACs/s** — half the parameters and 63% of the MACs of the prior lightweight SOTA FSPEN (79k, 89M) while improving PESQ by 0.10 — making it suitable for latency-sensitive, low-resource edge devices.

## Architecture

LiSenNet follows the [[concepts/convolutional-recurrent-network|CRN]] encoder-bottleneck-decoder pattern on the STFT, with three distinctive design choices:

1. **[[concepts/sub-band-convolution|Sub-band DS-Conv / US-Conv]]** — the encoder's downsampling convolutions and decoder's upsampling convolutions treat low and high frequency bands asymmetrically: low bands use stride 1 (full resolution preserved), high bands use stride 3 with [[concepts/sub-pixel-convolution|sub-pixel convolution]] (factor 3) for upsampling, for a net ×2 frequency-axis reduction while keeping low-frequency resolution.
2. **Dual-path recurrent (DPR) bottleneck** — following the [[concepts/dprnn|DPRNN]] paradigm: a Bi-GRU models the frequency axis (causal in time, since all bins of a frame are available simultaneously) and a unidirectional GRU models the time axis, repeated N = 2 times. To afford real-time RNN sizes (hidden 24/12), a [[concepts/convglu|ConvGLU]] channel mixer compensates the lost capacity.
3. **[[concepts/noise-detector|Noise detector]]** — an optional front-end on 64-dim Mel features that makes compute proportional to the noise content (15–70M MACs/s).

## Input Features and Phase Handling

The input concatenates the power-compressed magnitude ($c = 0.3$) with [[concepts/phase-difference-feature|phase differences]] (frequency-axis and baseband temporal). The network estimates only the enhanced magnitude; the output phase is refined post-hoc with a 2-iteration [[concepts/gla-phase-refinement|Griffin–Lim refinement]] from the noisy phase — a parameter-free alternative to learned phase estimation.

The mask activation is the [[concepts/learnable-sigmoid-mask|learnable Sigmoid]] from [[concepts/pesq|MetricGAN+]] with trainable per-frequency $\alpha$ and $\beta = 2$.

## Loss

$\mathcal{L} = 0.9\,\mathcal{L}_{\mathrm{mag}} + 0.1\,\mathcal{L}_{\mathrm{comp}} + 0.05\,\mathcal{L}_{\mathrm{pesq}}$ (+ BCE for the noise detector): compressed-magnitude MSE, compressed-complex MSE, and a MetricGAN-style PESQ loss — the latter worth +0.12 PESQ in ablation, the single largest contribution.

## Results

| Model | Para. | MACs | PESQ (VBD) | STOI |
|-------|-------|------|------------|------|
| RNNoise | 0.06M | 0.04G | 2.33 | 0.922 |
| FSPEN | 79k | 89M | 2.97 | 0.942 |
| **LiSenNet** | **37k** | **56M** | **3.07** | 0.939 |
| LiSenNet+ND | 55k | 15–70M | 3.00 (WSJ0+ESC50: 3.08 for base) | — |

On WSJ0+ESC50 (instantaneous-noise dataset), LiSenNet reaches RTF 0.028 on an Intel Xeon E5-2620 v4 — 0.020 with the noise detector.

## Role in the Lightweight-SE Lineage

LiSenNet (2025) sits between GTCRN (2024, 23.7k params, 31.97M MACs/s, DNS3 PESQ 2.07) and CoFi-Lite (2026, 83.12k, 12.87M, DNS3 PESQ 2.16) on the efficiency frontier, and became a **standard baseline** for subsequent lightweight-SE work:

- [[sources/wang-2025-adaptive-convolution-cnn-speech-enhancement|Wang et al. 2025]] use it as a backbone for [[concepts/adaptive-convolution|adaptive convolution]] (+0.12 PESQ, largest on lightweight models) and as an AdaptCRN comparison point.
- [[sources/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement|Yang et al. 2026]] scale it down ("LiSenNet Small") and compare against CoFi-Lite on DNS3 (LiSenNet: 36.78k/55.77M, PESQ 2.17).
- [[sources/zhao-2026-halo-half-frame-rate-adaptive-operator|Zhao et al. 2026]] use it as a HALO backbone (55.77M MACs/s baseline, improving metrics at matched complexity via half-frame-rate processing).
- Laroche & Olsson (2026, "Beyond model size: redesigning LiSenNet for embedded speech enhancement", arXiv:2609.29866 — not yet ingested) redesign LiSenNet for embedded deployment (Arduino Nicla Voice etc.), studying what model-size reduction does and does not cost.

## Related Concepts

- [[concepts/dprnn|Dual-Path RNN (DPRNN)]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network (CRN)]]
- [[concepts/sub-band-convolution|Sub-band Convolution]]
- [[concepts/convglu|ConvGLU]]
- [[concepts/noise-detector|Noise Detector]]
- [[concepts/learnable-sigmoid-mask|Learnable Sigmoid Mask]]
- [[concepts/phase-difference-feature|Phase Difference (PD) Feature]]
- [[concepts/gla-phase-refinement|GLA Phase Refinement]]
- [[concepts/gtcrn|GTCRN]]
- [[concepts/cofi-lite|CoFi-Lite]]
- [[concepts/adaptcrn|AdaptCRN]]

## Related Sources

- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]]
- [[sources/wang-2025-adaptive-convolution-cnn-speech-enhancement|Wang et al. 2025: Adaptive Convolution for CNN-based Speech Enhancement Models]]
- [[sources/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement|Yang et al. 2026: CoFi-Lite]]
- [[sources/zhao-2026-halo-half-frame-rate-adaptive-operator|Zhao et al. 2026: HALO]]
- Laroche & Olsson 2026 ("Beyond model size", arXiv:2609.29866 — not yet ingested)
