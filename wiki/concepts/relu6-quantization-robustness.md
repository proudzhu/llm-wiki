---
type: concept
created: 2026-11-07
updated: 2026-11-07
sources:
  - raw/papers/laroche-2026-lisenet-embedded/full-text.md
tags:
  - quantization
  - neural-network
  - int8-quantization
  - activation-functions
  - speech-enhancement
---

# ReLU6 Quantization Robustness

**ReLU6** — $\mathrm{ReLU6}(x) = \min(\max(x, 0), 6)$ — is the bounded variant of ReLU that clips activations to the range $[0, 6]$. Beyond mapping directly to integer-NPU operator sets, its defining property for deployment is that **bounding the activation range makes static int8 [[concepts/post-training-quantization|post-training quantization]] robust**: a fixed, narrow dynamic range means a static activation scale represents essentially all of the distribution, with no percentile-calibration tail risk and no outliers consuming resolution.

## Evidence

[[sources/laroche-2026-lisenet-embedded|Laroche & Olsson 2026]] supply the cleanest controlled evidence (VoiceBank-DEMAND, PESQ float32 → static int8):

| Model | P-32 | P-8 | Quantization loss |
|---|---|---|---|
| LiSenNet (PReLU/Mish, recurrent) | 3.01 | 2.93 | **0.08** |
| NPU-friendly ops C=24 (ReLU6) | 3.01 | 3.00 | **0.01** |
| Deep TCN, unbounded decoder | 3.07 | 2.99 | 0.08 |
| Deep TCN + lim-ReLU6 decoder | 3.08 | 3.01 | 0.07 → final |

Two observations: (i) substituting ReLU6 (with foldable BatchNorm) for PReLU/Mish/LayerNorm cuts the quantization loss by 8× at matched float quality; (ii) bounding only the **decoder** activations ("lim-ReLU6") recovers the deep model's long-context gains after quantization (+0.029 int8 PESQ at zero parameter cost) — float32 improvements in longer receptive fields are otherwise only partly retained post-quantization.

## Mechanism

Static PTQ assigns each activation tensor one fixed scale. With unbounded activations (PReLU outputs, GRU gates/states), the scale must cover rarely-seen large values, compressing the common range into few integer levels; bounded activations concentrate the distribution within a known window, so the static scale is near-optimal. This is the architectural complement to [[concepts/per-frame-activation-quantization|per-frame activation quantization]] (which recomputes ranges dynamically — Kim 2026's approach for GRUs): instead of adapting the quantizer to the range, constrain the network so the range is fixed.

## Related Concepts

- [[concepts/post-training-quantization|Post-Training Quantization]]
- [[concepts/per-frame-activation-quantization|Per-Frame Activation Quantization]]
- [[concepts/mcu-npu-deployment|MCU NPU Deployment]]
- [[concepts/lisennet-npu|LiSenNet-NPU]]

## Related Sources

- [[sources/laroche-2026-lisenet-embedded|Laroche & Olsson 2026: Beyond Model Size — Redesigning LiSenNet for Embedded Speech Enhancement]]
