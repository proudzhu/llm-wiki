---
type: concept
created: 2026-07-16
updated: 2026-07-16
sources:
  - raw/papers/benslimane-2026-tango-quantized-distributed/full-text.md
tags:
  - neural-network
  - quantization
  - model-compression
  - speech-enhancement
  - low-precision
---

# Post-Training Quantization (DPTQ)

**Post-Training Quantization (PTQ)**, and in particular **Dynamic Post-Training Quantization (DPTQ)**, applies quantization to a previously trained floating-point model without further training. Weights are statically quantized to a low-precision integer representation (typically INT8) after training, while activations are quantized dynamically at runtime according to their observed range. DPTQ is the simplest and cheapest route to a low-precision model: no labeled data and no fine-tuning are required.

## Mechanism

- **Weights**: Quantized once, after FP32 training, using the observed weight range. Stored in INT8.
- **Activations**: Quantized on-the-fly during inference, with the scale recomputed from each activation tensor's min/max. This avoids the need for calibration data but adds runtime overhead.
- **Bias**: Typically kept in higher precision (e.g., INT32 accumulator).

Because the model is not retrained, DPTQ cannot adapt to quantization noise. Layers whose activations span very different dynamic ranges — most notably **LSTM/GRU recurrent layers** — are particularly sensitive: their internal gate activations and states can vary by orders of magnitude, and a single global (or per-tensor) scale cannot represent all of them faithfully.

## When DPTQ Works

DPTQ works well for:

- **Convolutional layers** with bounded activations (e.g., after ReLU/BatchNorm).
- **Weight-only quantization** where activations remain in FP32.
- Models where the quantization-sensitive layers can be left in floating point.

## When DPTQ Fails

DPTQ degrades quality when:

- **Recurrent layers (LSTM/GRU)** are quantized, because of heterogeneous activation dynamic ranges.
- Both weights **and** activations are quantized, especially without calibration.
- The downstream task is sensitive to small mask-estimation errors (e.g., direct waveform reconstruction).

## Comparison with QAT

| Property | DPTQ | [[concepts/quantization-aware-training\|QAT]] |
|----------|------|------|
| Training required | No | Yes (fine-tuning) |
| Calibration data | Not for dynamic variant | Needed for observer initialization |
| Quality at W8A8 for LSTM | Heavy degradation | Near-FP32 |
| Best for | Quick prototyping, conv-heavy models | RNN/transformer deployment |

## Evidence in Hybrid Speech Enhancement

In [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026]], DPTQ applied to the full [[concepts/tango-framework|TANGO]] model (INT8 weights, FP32 activations) reduced memory from 4.03 MB to 1.01 MB but caused large quality drops:

| Quant. scheme | SI-SIR L/R | SI-SDR L/R | PESQ L/R |
|---------------|------------|------------|----------|
| Float32 | 22.8 / 26.2 | 4.7 / 5.0 | 1.731 / 1.770 |
| DPTQ (W8, A32) | 18.4 / 20.9 | 2.7 / 2.9 | 1.585 / 1.614 |
| QAT (W8, A32) | 22.8 / 26.2 | 4.7 / 5.0 | 1.729 / 1.765 |

Weight-only QAT recovers essentially all of the FP32 quality, confirming that the LSTM activations are the bottleneck for DPTQ.

## Related Concepts

- [[concepts/quantization-aware-training|Quantization-Aware Training (QAT)]]
- [[concepts/mn-tango|MN-TANGO]]
- [[concepts/tango-framework|Tango Framework]]
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]]

## Related Sources

- [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026: Quantized TANGO / MN-TANGO]]
