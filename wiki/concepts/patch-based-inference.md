---
type: concept
created: 2026-08-09
updated: 2026-08-09
sources:
  - raw/papers/lin-2021-mcunetv2/full-text.md
tags:
  - tinyml
  - inference-engine
  - memory-optimization
  - microcontroller
  - efficient-deep-learning
---

# Patch-based Inference

**Patch-based inference** (also called *per-patch inference*) is an inference scheduling strategy for convolutional neural networks that executes the memory-intensive initial stage **patch-by-patch** over small spatial regions of the feature map, rather than **layer-by-layer** over the entire activation. It is the core innovation of [[sources/lin-2021-mcunetv2\|MCUNetV2 (Lin et al. 2021)]] and reduces peak SRAM by 4–8× on microcontrollers, where the binding constraint is activation memory rather than FLOPs.

## Motivation

Conventional inference frameworks (TF-Lite Micro, CMSIS-NN, [[concepts/tinyengine\|TinyEngine]] v1, microTVM) allocate the full input and output activation buffer per layer in SRAM, releasing the input only after the *whole* layer finishes. This *per-layer* execution makes optimization easy (im2col, tiling, kernel fusion) but forces SRAM to hold the entire feature map, which is prohibitively large for the initial stage of CNNs.

[[sources/lin-2021-mcunetv2\|MCUNetV2]] identifies the [[concepts/imbalanced-memory-distribution\|imbalanced memory distribution]] of CNNs: the first few blocks have an order-of-magnitude larger peak memory than the rest (for MobileNetV2 at 224×224, the first 5 blocks exceed 450 kB while the remaining 13 fit comfortably in 256 kB). If one can "bypass" the initial stage's memory bottleneck, the rest of the network is already MCU-friendly.

## Mechanism

Given a sequence of convolutional layers forming the initial stage, patch-based inference:

1. Allocates a single buffer for the **final output** of the stage (small, because the stage ends at a down-sampled resolution).
2. Computes the output values **one spatial patch at a time**: for each patch, only the activations of that patch (across the staged layers) are materialized in SRAM.
3. After the patch-based stage finishes, the rest of the network runs in normal per-layer execution (its peak memory is already small).

The first input (the image) can be partially decoded from a compressed format such as JPEG, so it does not require full storage either.

## Computation Overhead

To produce the same non-overlapping output patches, the **input** image patches must *overlap*, because convolutional filters with kernel size >1 grow the receptive field: bordering pixels on output patches depend on inputs from neighboring patches. This causes repeated computation along patch borders.

For MobileNetV2 at 224×224 with 4×4 patches, the overhead is **+10% overall** (+42% for the patch-stage alone). The overhead grows with the receptive field of the initial stage and shrinks with more patches $p$ (smaller patches) — at the cost of more spatial overlapping.

## Hyper-parameters

- $n$ — number of initial blocks executed patch-by-patch (rest runs per-layer).
- $p$ — patch count; the image is split into $p \times p$ overlapping patches.

For MobileNetV2, MCUNetV2 finds $n^{*}=5$ (where the feature map is down-sampled 8×) and $p^{*}=4$ optimal. Beyond $n^{*}=5$, the patch size grows due to the increasing receptive field, raising peak memory again.

## Reducing Overhead

The companion technique [[concepts/receptive-field-redistribution\|receptive field redistribution]] cuts MobileNetV2's overhead from 10% to 3% by shrinking the initial stage's receptive field. MCUNetV2 further automates the choice of $n$, $p$, kernel sizes, expansion ratios, and stage depths via joint [[concepts/neural-architecture-search\|NAS]] + inference-scheduling search.

## Comparison to Other Memory-Saving Methods

Per MCUNetV2's Table 5 (MobileNetV2 backbone):

| Method | Inference | Invariant | Peak Mem (fp32) | Train time | ImgNet | VOC mAP |
|---|---|---|---|---|---|---|
| Per-layer (baseline) | Per-layer | ✓ | 2.29 MB | 1.0× | 72.2% | 75.4% |
| Non-overlapping patches | Per-patch | ✗ | 0.19 MB | 1.0× | 71.8% | 73.9% |
| RNNPool | Streaming | ✗ | 0.24 MB | 3.2× | 70.1% | 71.0% |
| **MCUNetV2 (MbV2-RD)** | Per-patch | ✓ | 0.19 MB | 1.0× | 72.1% | 75.7% |

Patch-based inference with overlapping patches is *numerically invariant* — it produces exactly the same output as per-layer inference — so training proceeds as a normal network (forward/backward per-layer) and only the deployment schedule changes. Non-overlapping patches break translational invariance and degrade detection mAP. RNNPool reduces memory but lowers accuracy and triples training time.

## Empirical Impact

- **Off-the-shelf** on existing backbones (no co-design): 3.7–8.0× peak memory reduction at 8–17% overhead.
- **On-device** (STM32F746, scaled to fit 320 kB / 1 MB): 4–6× measured peak SRAM reduction; MbV2-RD latency overhead only 4%.
- **Co-designed** (MCUNetV2): record 71.8% ImageNet top-1 on STM32H743 (int8); >90% VWW accuracy under 32 kB SRAM; +16.9% mAP on Pascal VOC.

## Related Concepts

- [[concepts/imbalanced-memory-distribution\|Imbalanced Memory Distribution]] — the structural CNN memory pattern that motivates patch-based inference
- [[concepts/receptive-field-redistribution\|Receptive Field Redistribution]] — companion technique that minimizes overlapping-patch overhead
- [[concepts/tinyml\|TinyML]] — problem domain
- [[concepts/tinyengine\|TinyEngine]] — extended in MCUNetV2 to support patch-based scheduling
- [[concepts/neural-architecture-search\|Neural Architecture Search]] — automates the choice of $n$, $p$, and the architecture

## Related Sources

- [[sources/lin-2021-mcunetv2\|Lin et al. 2021: MCUNetV2 — Memory-Efficient Patch-based Inference for Tiny Deep Learning]]
