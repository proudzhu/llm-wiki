---
type: concept
created: 2026-07-16
updated: 2026-08-09
sources:
  - raw/papers/benslimane-2026-tango-quantized-distributed/full-text.md
  - raw/papers/liu-2024-lightweight-dl-survey/full-text.md
tags:
  - neural-network
  - quantization
  - model-compression
  - speech-enhancement
  - low-precision
  - int8
---

# Quantization-Aware Training (QAT)

**Quantization-Aware Training (QAT)** is a neural-network quantization strategy in which the low-precision inference behavior is simulated during training by inserting *fake-quantization* modules in the forward pass. Weights and activations are quantized to a target bit-width (typically INT8) in the forward pass while gradients are computed in floating point and accumulated to the underlying floating-point weights. This lets the model adapt to quantization noise *before* deployment, in contrast to [[concepts/post-training-quantization|post-training quantization]] which quantizes a previously trained floating-point model without further adaptation.

## Mechanism

In uniform affine quantization, a floating-point value $x$ is mapped to an integer level $q$ via:

$$q = \mathrm{clip}\!\left( \mathrm{round}\!\left( \frac{x}{s} \right),\, n_{\min},\, n_{\max} \right), \qquad s = \frac{x_{\max} - x_{\min}}{n_{\max} - n_{\min}}$$

where $s$ is the scale, $[n_{\min}, n_{\max}]$ is the integer range determined by the bit-width, and clipping handles values outside the observed range.

Because `round` is non-differentiable, gradients are approximated using the **straight-through estimator (STE)**: the gradient of the rounding operation is treated as the identity, so gradients flow through the quantizer as if it were a linear function. This allows standard backpropagation to update the floating-point weights.

## Common Configuration: W8A8

A typical configuration is **W8A8**: weights and internal activations quantized to 8 bits. Variants include:

- **Weight-only QAT** (W8, activations FP32): Easiest to deploy; preserves most of the FP32 quality.
- **Weight + activation QAT** (W8A8): Both weights and activations are 8-bit. More aggressive; requires asymmetric activation quantization.
- **Mixed-precision I/O**: Input and output tensors kept at higher precision (e.g., INT16) to avoid accumulating quantization error at network boundaries.

In the QAT pipeline used for [[concepts/mn-tango|MN-TANGO]] ([[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026]]):

- Trainable weights use a **symmetric signed** quantizer.
- Activations use an **asymmetric affine** quantizer whose range is initialized from observed activation minima/maxima.
- Observer-based range updates are enabled during an initial warm-up phase, then frozen, after which quantization ranges are optimized by gradient descent.
- Bias terms are kept in higher precision and added in the accumulator domain before requantization.
- The main configuration is W8A8 with **16-bit I/O mask tensors**.

## QAT vs. Post-Training Quantization

| Property | [[concepts/post-training-quantization\|DPTQ]] | QAT |
|----------|------|-----|
| When quantization is applied | After FP32 training, no further optimization | During training, model adapts |
| Activation quantization | Difficult (dynamic ranges) | Trained-in, robust |
| Training cost | None | Additional fine-tuning passes |
| Quality at INT8 | Often degrades (especially for RNN/LSTM) | Typically preserves FP32 quality |

For LSTM-based mask estimators in hybrid SE systems, DPTQ causes significant quality loss because LSTM activations and internal states span different dynamic ranges. Weight-only QAT recovers FP32 performance almost exactly; W8A8 with INT16 I/O retains most perceptual metrics (STOI/PESQ) with small SI-SDR/SI-SAR degradation.

## Hybrid Neural-Spatial Robustness

A key finding for hybrid SE systems is that the **downstream spatial filter compensates for most quantization-induced mask errors**. In MN-TANGO, W8A8 degrades the intermediate MN-DNN output SI-SIR by ~1.5 dB, but the final GEVD-filtered output is within 0.1–0.6 dB of the FP32 baseline. This makes hybrid neural-spatial architectures particularly well-suited to aggressive neural quantization.

## Knowledge Distillation Companion

QAT can be combined with **knowledge distillation (KD)** using the FP32 model as teacher and the quantized model as student. The KD objective combines mask-level and enhanced-STFT matching between teacher and student outputs. In MN-TANGO, KD provided only marginal improvements, suggesting that the spatial filter already absorbs most quantization artifacts and teacher guidance adds little once QAT is in place.

## Related Concepts

- [[concepts/post-training-quantization|Post-Training Quantization (DPTQ)]]
- [[concepts/mn-tango|MN-TANGO]]
- [[concepts/tango-framework|Tango Framework]]
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]]
- [[concepts/erb-scale|ERB Scale]]

## Related Sources

- [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026: Quantized TANGO / MN-TANGO]]
- [[sources/liu-2024-lightweight-dl-survey|Liu et al. 2024: Lightweight Deep Learning for Resource-Constrained Environments]] — surveys quantization as a compression method with bit-width guidance (4-bit QAT preserves accuracy; HAWQ-V3 mixed-precision achieves 3.0% drop); recommends matching quantization precision to hardware constraints (e.g., specific MCUs/edge TPUs exclusively support integer operations, making full integer quantization essential via TF-Lite, which reduces model size by up to 4× and accelerates inference by more than 3×)
