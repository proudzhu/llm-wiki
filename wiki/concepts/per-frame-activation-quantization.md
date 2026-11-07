---
type: concept
created: 2026-11-07
updated: 2026-11-07
tags:
  - quantization
  - int8-inference
  - efficiency
  - on-device-inference
---

# Per-Frame Activation Quantization

An int8 quantization scheme for streaming inference in which activation ranges are **recomputed from each incoming frame** at runtime, rather than fixed from a calibration set at conversion time. Introduced as the load-bearing mechanism of the training-free port in [[sources/kim-2026-faster-enhancer|Kim 2026]].

## Formulation

- **Weights**: per-output-row symmetric int8, one fp32 scale per row — fixed at conversion time like any post-training scheme.
- **Activations**: per-tensor asymmetric uint8 range, **recomputed per frame**, stored shifted by −128 so signed kernels consume them directly.
- The zeropoint correction folds into the dequantization epilogue through precomputed row sums, following the integer-only formulation of Jacob et al. (2018); the hot path is an int8 dot product and one fused multiply-add.

## Why No Calibration Set

The defining property: because the range is recomputed from each frame, there is **no calibration set and no sensitivity to one**. Conventional post-training quantization must pick activation scales that generalize from a representative sample; outlier-heavy frames outside the calibration distribution get clipped. Per-frame recomputation removes that failure mode entirely, at the cost of computing the range each frame (part of the ~45%-of-peak overhead the runtime reports between its 0.033 RTF floor and 0.069 measured RTF).

## Quality Outcome

On the FastEnhancer-Medium 48 kHz port over 824 VoiceBank-DEMAND utterances: −0.006 PESQ, −0.0003 STOI, −0.079 dB SNR, −0.017 SIGMOS vs the fp32 graph — quantization costs about 1.6% of what the model itself gains, with no degradation concentrated on harder inputs (PESQ delta flat at −0.003…−0.008 across 2.5–17.5 dB input SNR buckets). For context, prior post-training quantization of comparable enhancers reported −0.06 PESQ (mixed FP16-INT8) and −0.3 (uniform int8).

Related: [[concepts/post-training-quantization|Post-Training Quantization]] — per-frame activation quantization is a PTQ variant that eliminates calibration; [[concepts/quantization-aware-training|Quantization-Aware Training]] is the alternative that folds range-awareness into training itself.

## Related Concepts

- [[concepts/post-training-quantization|Post-Training Quantization]]
- [[concepts/quantization-aware-training|Quantization-Aware Training]]
- [[concepts/faster-enhancer-c|faster-enhancer.c]]

## Related Sources

- [[sources/kim-2026-faster-enhancer|Kim 2026: faster-enhancer.c]]
- [[sources/laroche-2026-lisenet-embedded|Laroche & Olsson 2026: Beyond Model Size]] — the architectural alternative: instead of recomputing activation ranges per frame, bound the activations (ReLU6) so a *static* scale is near-optimal — necessary on MCU NPUs where the operator set expects static quantization
