---
type: source
created: 2026-07-18
updated: 2026-07-18
sources:
  - raw/papers/castelli-2025-embedded-joint-aec-ns/full-text.md
  - zotero://select/items/0_MEBK2YDF
tags:
  - speech-enhancement
  - acoustic-echo-cancellation
  - noise-suppression
  - embedded
  - deep-learning
  - real-time
  - model-compression
---

# Castelli 2024: Embedded Joint AEC and Noise Suppression

| Field | Value |
|-------|-------|
| **Author** | [[entities/francesco-castelli\|Francesco Castelli]] |
| **Institution** | NXP Semiconductors, Voice & Audio Team |
| **Published** | tinyML® Summit, April 22–24, 2024 |
| **Type** | Industry presentation (public) |
| **Zotero** | [MEBK2YDF](zotero://select/items/0_MEBK2YDF) |

## Summary

This NXP tinyML Summit 2024 presentation traces the deployment path of a joint acoustic echo cancellation (AEC) and noise suppression (NS) network from the [[sources/indenbom-2023-deepvqe\|DeepVQE]] reference architecture down to a [[concepts/tinyvqe\|TinyVQE]] model that fits the resource budget of an NXP i.MX RT600 dual-core MCU with a Cadence® Tensilica® HiFi 4 DSP. Starting from a re-trained DeepVQE-s baseline (610k params, 10.28 MMACs/frame), Castelli applies a sequence of efficiency transformations — depthwise separable convolutions, parameter cutting, custom HiFi4 intrinsics for the [[concepts/complex-convolving-mask\|complex convolving mask]], ReLU replacing ELU, MACs pruning, and layer-norm removal — to arrive at TinyVQE: **114k parameters, 0.48 MMACs/frame, 420 KB tensor arena, 2.32 ms inference per 16 ms frame** on the HiFi4 DSP at 600 MHz. The presentation is a concrete industrial case study of the model-compression techniques required to port a server-grade joint AEC+NS network onto an embedded audio MCU while preserving AEC-MOS within ~0.12 of the DeepVQE-s baseline.

## Problem Formulation

Joint AEC + NS must run under hard embedded constraints:

- **Target hardware**: NXP i.MX RT600 (Arm Cortex-M33 @ 300 MHz + Cadence HiFi4 DSP @ 600 MHz, 4.5 MB on-chip SRAM)
- **HiFi4 DSP characteristics**: two 2-way SIMD VFPU (4 FP32 MACs/cycle), fixed-point 8×32×16 or 16×16×16 MACs/cycle, C/C++ intrinsics, Cadence® HiFi4 NN library
- **Latency budget**: 16 ms hop size at 16 kHz → frame inference must finish within 16 ms
- **Memory budget**: on-chip SRAM only (4.5 MB shared with other workloads)
- **Quality target**: match [[sources/indenbom-2023-deepvqe\|DeepVQE-s]] AEC-MOS as closely as possible while fitting the DSP

The presentation explicitly identifies three DSP-side challenges that distinguish embedded deployment from cloud/server deployment:

1. **Loudspeaker non-linearity, Rx-to-microphone delay, reverberation** in the echo path
2. **Strict latency requirement** (frame algorithmic delay bounded by hop size)
3. **Resource scarcity** — FP32 weights, MACs, and tensor arena memory all cost die area and power

## Methodology

### Re-Trained Baseline: DeepVQE-s @ NXP

Castelli re-implements the [[sources/indenbom-2023-deepvqe\|DeepVQE]] architecture (residual CNN autoencoder + cross-attention alignment + GRU bottleneck + [[concepts/complex-convolving-mask\|CCM]] block) on NXP data at 16 kHz (vs. the original 24 kHz) with 32 ms window and 16/8 ms hop. Two hyperparameter changes are reported:

- **BatchNorm → LayerNorm** (smaller batch sizes during training)
- **Frame delay $d = 1$ s** retained from the original DeepVQE alignment block

The re-trained DeepVQE-s reproduces the original paper's quality within noise (AEC-MOS within ±0.02, DNS-MOS within ±0.06).

### Optimization Pipeline

The optimization proceeds as a sequence of independent techniques, each reported with measured (params, MACs, memory, inference time, AEC-MOS, DNS-MOS):

| Stage | Technique | Effect |
|-------|-----------|--------|
| 0 | DeepVQE-s (ours) | 610k / 10.28 MMACs / — / — / 4.67 / 3.28 |
| 1 | [[concepts/mobilevqe\|MobileVQE]]: Conv2d → Depthwise Separable Conv2d, drop decoder residual blocks, $d=0.5$ s | 635k / **1.34 MMACs** / 4.68 / 3.11 (≈7.7× MACs reduction) |
| 2 | Cut parameters (bottleneck 598k/635k = 94% → 102k/147k = 69%); frame delay $d=250$ ms | 147k / 0.86 MMACs / 770 KB / 13.19 ms / 4.53 / 3.01 |
| 3 | Custom masking layer (HiFi4 batched complex dot product intrinsics; replace TFLM Split/Concatenation/Transposition) | 147k / 0.86 MMACs / 690 KB / **7.19 ms** / 4.53 / 3.01 |
| 4 | ELU → ReLU (HiFi4 FP32 optimized kernel) | 147k / 0.86 MMACs / 690 KB / **4.04 ms** / 4.57 / 3.00 |
| 5 | Cut MACs (symmetrical model, no skip Conv2d; masking layer 27 → 18) | 139k / 0.54 MMACs / 455 KB / 2.99 ms / 4.56 / 2.98 |
| 6 | [[concepts/tinyvqe\|TinyVQE]]: remove LayerNorm, longer training | **114k / 0.48 MMACs / 420 KB / 2.32 ms / 4.55 / 2.95** |
| Bonus | Further pruning | 92k / 0.45 MMACs / 418 KB / 2.26 ms / 4.54 / 2.92 (insufficient echo suppression — not selected) |

### Loss Function

The training loss combines complex and magnitude SDR-style terms with a near/far mixture weighting:

$$
\begin{aligned}
L_{CSDR}(A, \hat{A}) &= \frac{\sum_k \big| |A|^p e^{j\theta_A} - |\hat{A}|^p e^{j\theta_{\hat{A}}} \big|^2}{\sum_k \big| |A|^p e^{j\theta_A} \big|^2} \\
L_{MSDR}(A, \hat{A}) &= \frac{\sum_k \big| |A|^p - |\hat{A}|^p \big|^2}{\sum_k \big| |A|^p \big|^2} \\
L_{SDR}(A, \hat{A}) &= \alpha L_{CSDR}(A, \hat{A}) + (1-\alpha) L_{MSDR}(A, \hat{A}) \\
L &= \sum_n \beta L_{SDR}(S, E) + (1-\beta) L_{SDR}(M-S, M-E) \\
\beta &= \frac{\sum_k |S|^2}{\sum_k |M|^2}
\end{aligned}
$$

where $S$ is near-end speech, $M$ is the microphone mixture, $E$ is the corresponding estimate. The $\beta$ weighting adapts the loss to the energy ratio between near-end speech and the full microphone mixture per frame — an SNR-weighted combination of complex and magnitude SDR terms.

### Deployment Target

i.MX RT600 AUD-EVK board: Arm Cortex-M33 (300 MHz) + Cadence HiFi4 DSP (600 MHz) with 4.5 MB shared on-chip SRAM. The model runs FP32 inference with TFLite Micro (TFLM) wrapped in HiFi4 NN library intrinsics; earlier integration was validated on an i.MX 8M Plus EVK (Cortex-A53 + NPU) using TFLite + XNNPack with a GStreamer audio-visual pipeline.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Sampling rate | 16 kHz |
| STFT window | 32 ms (squared-root Hann) |
| Hop size | 16 ms (with 8 ms option explored) |
| Algorithmic delay | 32 ms (window-size bounded) |
| Frame delay $d_{\max}$ for alignment block | 1 s → 0.5 s → 0.25 s across stages |
| Target hardware | NXP i.MX RT600 (HiFi4 DSP @ 600 MHz) |
| Compute runtime | TFLite Micro + Cadence HiFi4 NN library (C/C++ intrinsics) |
| Numeric format | FP32 |
| Metrics | AEC-MOS (FST Echo / DT Echo / DT Deg) + DNS-MOS (Sig / Bak / Ovrl) + HiFi4 inference time |

## Results

### AEC-MOS / DNS-MOS Across Optimization Stages

| Model | Params (k) | MACs (M) | Memory (KB) | FST Echo | DT Echo | DT Deg | Sig | Bak | Ovrl | HiFi4 (ms) |
|-------|-----------:|---------:|------------:|---------:|--------:|-------:|----:|----:|-----:|-----------:|
| Unprocessed | — | — | — | 2.19 | 2.09 | 4.05 | 3.49 | 2.11 | 2.31 | — |
| DeepVQE-s (paper) | 590 | 9.64* | — | 4.61 | 4.62 | 4.02 | 3.60 | 4.10 | 3.30 | — |
| DeepVQE-s (ours) | 610 | 10.28 | — | 4.67 | 4.61 | 4.07 | 3.54 | 4.08 | 3.28 | — |
| [[concepts/mobilevqe\|MobileVQE]] | 635 | 1.34 | — | 4.68 | 4.49 | 3.95 | 3.39 | 3.95 | 3.11 | — |
| Cut parameters | 147 | 0.86 | 770 | 4.53 | 4.34 | 3.81 | 3.31 | 3.84 | 3.01 | 13.19 |
| Custom impls | 147 | 0.86 | 690 | 4.53 | 4.34 | 3.81 | 3.31 | 3.84 | 3.01 | 7.19 |
| ELU → ReLU | 147 | 0.86 | 690 | 4.57 | 4.49 | 3.79 | 3.26 | 3.93 | 3.00 | 4.04 |
| Cut MACs | 139 | 0.54 | 455 | 4.56 | 4.45 | 3.87 | 3.28 | 3.82 | 2.98 | 2.99 |
| **[[concepts/tinyvqe\|TinyVQE]]** | **114** | **0.48** | **420** | **4.55** | **4.41** | **3.81** | **3.26** | **3.80** | **2.95** | **2.32** |
| Bonus (rejected) | 92 | 0.45 | 418 | 4.54 | 4.24 | 3.63 | 3.27 | 3.79 | 2.92 | 2.26 |

### MobileVQE vs. DeepVQE Frame Inference

On a single Cortex-A53 core (i.MX 8M Plus EVK, FP32, 16 ms hop, TFLite + XNNPack), MobileVQE is reported as substantially faster than DeepVQE — the presentation shows the MobileVQE bar visually well below the DeepVQE bar; no exact millisecond figures are tabulated in the extracted text.

### Selected Configuration: TinyVQE

TinyVQE is the final selected configuration. Compared to the re-trained DeepVQE-s baseline:

- **≈4× smaller model** (610k → 114k parameters)
- **≈2× faster DSP frame inference** (the presentation cites ≈2× speed-up vs. the MobileVQE-stage measurement on the same HiFi4 DSP, with TinyVQE at 2.32 ms/frame — well within the 16 ms real-time budget on a 600 MHz HiFi4)
- AEC-MOS DT Echo drop of 0.20 (4.61 → 4.41), DNS-MOS Ovrl drop of 0.33 (3.28 → 2.95)
- Next planned step: **16×8 quantization-aware training (QAT)** to further reduce memory and accelerate fixed-point HiFi4 kernels

### Rejected Configuration: "Bonus" Pruning

The bonus stage (92k params, 0.45 MMACs) was rejected because it produced **insufficient echo suppression** (DT Echo drops to 4.24, DT Deg to 3.63), even though frame inference was the fastest measured (2.26 ms). This establishes a practical quality floor below which further parameter cutting is no longer acceptable for the embedded AEC use case.

## Key Contributions

1. **End-to-end industrial case study** of porting a server-grade joint AEC+NS network ([[sources/indenbom-2023-deepvqe\|DeepVQE-s]]) onto a 600 MHz Cadence HiFi4 DSP with 4.5 MB on-chip SRAM, achieving 2.32 ms / 16 ms frame inference at 114k parameters.
2. **Custom HiFi4 intrinsics for the CCM block** — replacing TFLM Split/Concatenation/Transposition with a batched complex dot product reduces CCM-stage inference from 13.19 ms → 7.19 ms (≈1.8× speed-up) at unchanged quality.
3. **Quantified contribution of each optimization stage** to (params, MACs, memory, inference, quality) — the only publicly available per-stage ablation of the DeepVQE → TinyVQE compression path.
4. **[[concepts/mobilevqe\|MobileVQE]] and [[concepts/tinyvqe\|TinyVQE]] as named deployment architectures** — concrete instantiations of the DeepVQE pattern optimized for embedded audio MCUs.
5. **Practical quality floor observation**: 92k parameters breaks echo suppression (DT Echo 4.24, DT Deg 3.63); 114k (TinyVQE) is the selected operating point.

## Related Concepts

- [[concepts/acoustic-echo-cancellation\|Acoustic Echo Cancellation]]
- [[concepts/complex-convolving-mask\|Complex Convolving Mask]]
- [[concepts/cross-attention-alignment\|Cross-Attention Alignment]]
- [[concepts/sub-pixel-convolution\|Sub-Pixel Convolution]]
- [[concepts/mobilevqe\|MobileVQE]]
- [[concepts/tinyvqe\|TinyVQE]]
- [[concepts/depthwise-separable-convolution\|Depthwise Separable Convolution]]

## Related Synthesis

- [[synthesis/joint-multitask-ultra-low-latency-se\|Joint Multi-Task Speech Enhancement & Ultra-Low-Latency Realtime Paradigm]] — Castelli provides the embedded-deployment case study that anchors the upper end of the latency hierarchy (16 ms hop) on a fixed-point-capable HiFi4 DSP, complementing OVC's 2 ms time-domain anchor at the lower end.

## Related Sources

- [[sources/indenbom-2023-deepvqe\|Indenbom et al. 2023: DeepVQE]] — the source architecture that Castelli re-implements and compresses; DeepVQE-s is the quality reference point throughout the optimization pipeline
- [[sources/li-2025-echofree-neural-aec\|Li et al. 2025: EchoFree]] — alternative lightweight AEC at 278k params / 30 MMACs/s; Castelli's TinyVQE reaches 114k params / 0.48 MMACs/frame (≈30 MMACs/s at 16 ms hop) but performs joint AEC + NS rather than AEC only
