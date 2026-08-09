---
type: concept
created: 2026-08-09
updated: 2026-08-09
sources:
  - raw/papers/lin-2020-mcunet/full-text.md
  - raw/papers/lin-2021-mcunetv2/full-text.md
tags:
  - tinyml
  - deep-learning
  - efficient-deep-learning
  - microcontroller
  - edge-ai
---

# TinyML

**TinyML** (Tiny Machine Learning) is the practice of running machine-learning inference on resource-constrained embedded devices — typically microcontroller units (MCUs) — rather than on cloud GPUs or mobile application processors. The defining challenge is that microcontrollers have 3–6 orders of magnitude less memory and storage than cloud/mobile hardware: a representative ARM Cortex-M7 MCU (STM32F746) provides only **320 kB SRAM** (constrains activation size) and **1 MB Flash** (constrains model size), versus 16 GB on an NVIDIA V100 or 4 GB on a smartphone.

## Motivation

There are an estimated 250 billion deployed MCU-based IoT devices. Running inference directly on these always-on, low-power, low-cost (≤$5) devices enables applications inaccessible to cloud AI — smart manufacturing, personalized healthcare, precision agriculture, automated retail, keyword spotting, visual wake words — while preserving privacy (sensor data never leaves the device) and operating without network connectivity.

## Why TinyML Differs from Cloud/Mobile AI

MCUs are bare-metal devices with no operating system and no DRAM. Three consequences shape TinyML system design:

1. **Memory, not FLOPs, is the binding constraint.** Efficient architectures optimized for mobile (e.g., MobileNetV2) reduce *model size* but not *peak activation*: at ~70% ImageNet accuracy, MobileNetV2 is 4.6× smaller than ResNet-18 yet has 1.8× *larger* peak activation, making it harder — not easier — to fit in SRAM.
2. **SRAM vs. Flash split.** SRAM (read & write) bounds activation size; Flash (read-only) bounds parameter size. A model must satisfy *both* budgets simultaneously, so NAS targets must be peak-SRAM and Flash, not FLOPs/latency.
3. **The inference library affects accuracy.** On memory-starved MCUs, a more memory-efficient library fits a larger runnable model, raising the achievable accuracy ceiling. Interpreter-based libraries (TF-Lite Micro, CMSIS-NN) can waste up to 65% of peak memory on runtime meta-information.

## Approaches

- **System–algorithm co-design** — jointly optimizing the network architecture and the inference engine so each enlarges the other's effective search space; exemplified by [[sources/lin-2020-mcunet\|MCUNet (Lin et al. 2020)]] = [[concepts/tinynas\|TinyNAS]] + [[concepts/tinyengine\|TinyEngine]].
- **Quantization** — int8 post-training quantization is the industrial standard with negligible loss; 4-bit and mixed-precision quantization (with quantization-aware fine-tuning) trade extra compression for accuracy recovery.
- **Pruning and compression** — removing redundant weights/channels to fit Flash budgets.
- **Memory-efficient inference** — code generation instead of interpretation, model-adaptive memory scheduling, and in-place operators (e.g., in-place depth-wise convolution).

## Milestone

MCUNet (NeurIPS 2020) was the first system to exceed **70% ImageNet top-1 accuracy (70.7%)** on an off-the-shelf commercial microcontroller (STM32H743), using 3.5× less SRAM and 5.7× less Flash than int8 MobileNetV2/ResNet-18 at comparable accuracy.

MCUNetV2 (arXiv 2021) advanced the frontier by identifying the [[concepts/imbalanced-memory-distribution\|imbalanced memory distribution]] of CNNs and introducing [[concepts/patch-based-inference\|patch-based inference]] + [[concepts/receptive-field-redistribution\|receptive field redistribution]]. It cut peak SRAM of existing networks by 4–8×, set a new record **71.8% ImageNet top-1** on STM32H743 (int8, +3.3% over V1's int8), achieved **>90% Visual Wake Words accuracy under 32 kB SRAM** (4× smaller than V1), and unlocked **object detection on MCUs** (+16.9% mAP on Pascal VOC over V1).

## Related Concepts

- [[concepts/tinynas\|TinyNAS]] — resource-constrained NAS for MCUs
- [[concepts/tinyengine\|TinyEngine]] — memory-efficient MCU inference engine
- [[concepts/patch-based-inference\|Patch-based Inference]] — MCUNetV2's patch-by-patch scheduling that cuts peak SRAM 4–8×
- [[concepts/receptive-field-redistribution\|Receptive Field Redistribution]] — minimizes the overlapping-patch overhead
- [[concepts/imbalanced-memory-distribution\|Imbalanced Memory Distribution]] — the structural CNN memory pattern MCUNetV2 exploits
- [[concepts/neural-architecture-search\|Neural Architecture Search]]
- [[concepts/post-training-quantization\|Post-Training Quantization]]
- [[concepts/quantization-aware-training\|Quantization-Aware Training]]
- [[concepts/depthwise-separable-convolution\|Depthwise Separable Convolution]]

## Related Sources

- [[sources/lin-2020-mcunet\|Lin et al. 2020: MCUNet — Tiny Deep Learning on IoT Devices]]
- [[sources/lin-2021-mcunetv2\|Lin et al. 2021: MCUNetV2 — Memory-Efficient Patch-based Inference for Tiny Deep Learning]]
