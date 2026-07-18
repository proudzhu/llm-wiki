---
type: concept
created: 2026-07-18
updated: 2026-07-18
sources:
  - raw/papers/castelli-2025-embedded-joint-aec-ns/full-text.md
tags:
  - deep-learning
  - speech-enhancement
  - acoustic-echo-cancellation
  - noise-suppression
  - neural-networks
  - embedded
  - low-complexity
---

# TinyVQE

**TinyVQE** is the final selected deployment configuration of the joint acoustic echo cancellation (AEC) and noise suppression (NS) network introduced by [[entities/francesco-castelli\|Francesco Castelli]] (NXP) at tinyML Summit 2024. It is the end point of a six-stage compression pipeline applied to the [[sources/indenbom-2023-deepvqe\|DeepVQE-s]] architecture, designed to fit a Cadence® Tensilica® HiFi 4 DSP (NXP i.MX RT600) at 600 MHz within a 16 ms real-time frame budget.

## Configuration

TinyVQE inherits the architecture of Stage 5 ("Cut MACs") and adds two further changes:

1. **Remove LayerNorm** — Castelli removes the LayerNorm layers that were introduced in the re-trained DeepVQE-s baseline (replacing the original BatchNorm, to accommodate smaller batch sizes).
2. **Longer training runs** — additional training epochs to recover quality lost to the architectural simplifications.

### Measured Performance

| Metric | Value |
|--------|-------|
| Parameters | **114k** |
| MACs / frame | **0.48 M** |
| Tensor arena | **420 KB** |
| HiFi4 DSP frame inference (FP32 @ 600 MHz) | **2.32 ms** (per 16 ms frame) |
| FST EchoMOS | 4.55 |
| DT EchoMOS | 4.41 |
| DT DegMOS | 3.81 |
| DNS-MOS Sig | 3.26 |
| DNS-MOS Bak | 3.80 |
| DNS-MOS Ovrl | 2.95 |

For comparison, the [[sources/indenbom-2023-deepvqe\|DeepVQE-s]] reference (NXP's re-trained baseline, 610k params / 10.28 MMACs) scores FST Echo 4.67, DT Echo 4.61, DT Deg 4.07, Sig 3.54, Bak 4.08, Ovrl 3.28. TinyVQE therefore achieves AEC-MOS within 0.12 (DT Echo) to 0.26 (DT Deg) of the baseline, at ≈4× fewer parameters and ≈21× fewer MACs.

### Rejected "Bonus" Variant

An aggressive 92k-parameter variant ("Bonus") was rejected because it produced **insufficient echo suppression**: DT Echo dropped to 4.24 (vs. 4.41 for TinyVQE) and DT Deg to 3.63 (vs. 3.81). The frame inference time improved only marginally (2.26 ms vs. 2.32 ms). This establishes 92k as a practical quality floor for joint AEC+NS on this architecture; TinyVQE at 114k is the selected operating point.

## Optimization Pipeline Context

TinyVQE is Stage 6 of the six-stage pipeline:

| Stage | Model | Params (k) | MACs (M) | Memory (KB) | HiFi4 (ms) | FST Echo | DT Echo | DT Deg |
|-------|-------|-----------:|---------:|------------:|-----------:|---------:|--------:|-------:|
| 0 | DeepVQE-s (ours) | 610 | 10.28 | — | — | 4.67 | 4.61 | 4.07 |
| 1 | [[concepts/mobilevqe\|MobileVQE]] | 635 | 1.34 | — | — | 4.68 | 4.49 | 3.95 |
| 2 | Cut parameters | 147 | 0.86 | 770 | 13.19 | 4.53 | 4.34 | 3.81 |
| 3 | Custom CCM impls | 147 | 0.86 | 690 | 7.19 | 4.53 | 4.34 | 3.81 |
| 4 | ELU → ReLU | 147 | 0.86 | 690 | 4.04 | 4.57 | 4.49 | 3.79 |
| 5 | Cut MACs | 139 | 0.54 | 455 | 2.99 | 4.56 | 4.45 | 3.87 |
| **6** | **TinyVQE** | **114** | **0.48** | **420** | **2.32** | **4.55** | **4.41** | **3.81** |

The cumulative effect is a ≈4× parameter reduction and ≈2× inference speed-up (relative to MobileVQE at 7.19 ms — TinyVQE at 2.32 ms is the final operating point).

## Deployment Target

| Property | Value |
|----------|-------|
| SoC | NXP i.MX RT600 (dual-core MCU) |
| Arm core | Cortex-M33 @ 300 MHz |
| DSP core | Cadence® Tensilica® HiFi 4 @ 600 MHz |
| On-chip SRAM | 4.5 MB shared |
| HiFi4 SIMD | Two 2-way VFPU (4 FP32 MACs/cycle), fixed-point 8×32×16 or 16×16×16 MACs/cycle |
| Numeric format | FP32 |
| Inference runtime | TFLite Micro + Cadence HiFi4 NN library (C/C++ intrinsics) |
| Audio pipeline | GStreamer integration on i.MX 8M Plus EVK (intermediate platform) |

The next planned step reported in the presentation is **16×8 quantization-aware training (QAT)**, which would exploit the HiFi4's fixed-point 8×32×16 / 16×16×16 MACs/cycle path for a further speed-up and memory reduction.

## Related Concepts

- [[concepts/mobilevqe\|MobileVQE]]
- [[concepts/complex-convolving-mask\|Complex Convolving Mask]]
- [[concepts/cross-attention-alignment\|Cross-Attention Alignment]]
- [[concepts/sub-pixel-convolution\|Sub-Pixel Convolution]]
- [[concepts/depthwise-separable-convolution\|Depthwise Separable Convolution]]
- [[concepts/acoustic-echo-cancellation\|Acoustic Echo Cancellation]]

## Related Sources

- [[sources/castelli-2025-embedded-joint-aec-ns\|Castelli 2024: Embedded Joint AEC and NS]] — introduces TinyVQE as the final selected configuration
- [[sources/indenbom-2023-deepvqe\|Indenbom et al. 2023: DeepVQE]] — the source architecture compressed to produce TinyVQE
- [[sources/li-2025-echofree-neural-aec\|Li et al. 2025: EchoFree]] — alternative lightweight AEC at 278k params / 30 MMACs/s; TinyVQE reaches 114k params / ≈30 MMACs/s (0.48 MMACs/frame at 16 ms hop) but performs joint AEC + NS rather than AEC only
