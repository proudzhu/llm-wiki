---
type: concept
created: 2026-08-09
updated: 2026-08-11
sources:
  - raw/papers/lin-2020-mcunet/full-text.md
  - raw/papers/lin-2021-mcunetv2/full-text.md
  - raw/papers/lin-2023-tinyml-progress-futures/full-text.md
  - raw/papers/liu-2024-lightweight-dl-survey/full-text.md
  - raw/papers/le-2026-efficient-nn-tinyml-review/full-text.md
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

MCUNetV3 (NeurIPS 2022, surveyed in [[sources/lin-2023-tinyml-progress-futures\|Lin et al. 2023: TinyML — Progress and Futures]]) extended TinyML from **inference to on-device training** by co-designing [[concepts/quantization-aware-scaling\|Quantization-Aware Scaling (QAS)]] (hyperparameter-free gradient rescaling that stabilizes real int8 quantized training), [[concepts/sparse-update\|Sparse Update]] (selective layer/tensor backpropagation via contribution analysis), and the [[concepts/tiny-training-engine\|Tiny Training Engine (TTE)]] (compile-time differentiation + backward-graph pruning + operator reordering). V3 reduced training memory from 303 MB (PyTorch) to **149 KB** at equal transfer-learning accuracy (2077×), fitting on-device training into 256 kB SRAM, and reached 89.3% VWW transfer-learning accuracy at 173 kB peak memory.

## TinyML in the Broader Lightweight-DL Pipeline

[[sources/liu-2024-lightweight-dl-survey\|Liu et al. 2024]] frames TinyML as one of two future frontiers of resource-constrained deep learning (the other being lightweight LLMs), positioned at the end of a three-stage pipeline: lightweight architecture design → model compression → hardware acceleration. The survey catalogs the **MCU inference library landscape** alongside TinyNAS/TinyEngine:

- **CMSIS-NN** (ARM Cortex-M) — pioneering library with NNfunctions (conv/pool/activation) + NNsupportfunctions (data conversion/activation tables) split.
- **CMIX-NN** — open-source mixed-precision tool supporting arbitrary 8/4/2-bit quantization of weights and activations.
- **MCUNet** / **MCUNetV2** — see Milestone above.
- **MicroNet** — differentiable NAS (DNAS) for low-operation models on TensorFlow Lite Micro (TFLM); state-of-the-art on TinyMLperf benchmarks (Visual Wake Words, Google Speech Commands, Anomaly Detection).

The survey also identifies three structural impediments to TinyML's rapid development: (1) **extreme resource constraints** (< 1 MB Flash, small SRAM); (2) **hardware/software heterogeneity** (solutions must be tweaked per device, unlike cross-platform PyTorch/TensorFlow on GPUs); (3) **lack of standard datasets** matching the data characteristics produced by edge-device external sensors.

## Related Concepts

- [[concepts/tinynas\|TinyNAS]] — resource-constrained NAS for MCUs
- [[concepts/tinyengine\|TinyEngine]] — memory-efficient MCU inference engine
- [[concepts/patch-based-inference\|Patch-based Inference]] — MCUNetV2's patch-by-patch scheduling that cuts peak SRAM 4–8×
- [[concepts/receptive-field-redistribution\|Receptive Field Redistribution]] — minimizes the overlapping-patch overhead
- [[concepts/imbalanced-memory-distribution\|Imbalanced Memory Distribution]] — the structural CNN memory pattern MCUNetV2 exploits
- [[concepts/quantization-aware-scaling\|Quantization-Aware Scaling (QAS)]] — MCUNetV3's hyperparameter-free gradient rescaling for int8 training
- [[concepts/sparse-update\|Sparse Update]] — MCUNetV3's selective layer/tensor backpropagation
- [[concepts/tiny-training-engine\|Tiny Training Engine (TTE)]] — MCUNetV3's compile-time training system (training-side sibling of TinyEngine)
- [[concepts/neural-architecture-search\|Neural Architecture Search]]
- [[concepts/post-training-quantization\|Post-Training Quantization]]
- [[concepts/quantization-aware-training\|Quantization-Aware Training]]
- [[concepts/depthwise-separable-convolution\|Depthwise Separable Convolution]]
- [[concepts/tinymlops\|TinyMLOps]] — deployment pipeline and framework taxonomy (TFLM, NNoM, Edge Impulse, CMSIS-NN)
- [[concepts/model-pruning\|Model Pruning]] — unstructured / structured / Bayesian pruning taxonomy
- [[concepts/bayesian-compression\|Bayesian Compression]] — unifying framework for pruning + quantization via spike-and-slab / horseshoe / log-uniform priors
- [[concepts/keyword-spotting\|Keyword Spotting]] — primary TinyML audio application

## Related Sources

- [[sources/lin-2020-mcunet|Lin et al. 2020: MCUNet — Tiny Deep Learning on IoT Devices]]
- [[sources/lin-2021-mcunetv2|Lin et al. 2021: MCUNetV2 — Memory-Efficient Patch-based Inference for Tiny Deep Learning]]
- [[sources/lin-2023-tinyml-progress-futures|Lin et al. 2023: TinyML — Progress and Futures]]
- [[sources/liu-2024-lightweight-dl-survey|Liu et al. 2024: Lightweight Deep Learning for Resource-Constrained Environments]] — broader survey that frames TinyML as a future frontier alongside lightweight LLMs; catalogs CMSIS-NN, CMIX-NN, MicroNet alongside the MCUNet family
- [[sources/le-2026-efficient-nn-tinyml-review|Lê, Wolinski & Arbel 2026: Efficient NNs for TinyML — A Comprehensive Review]] — bridges methodological and application TinyML surveys; introduces the runtime-vs-transcompiler framework taxonomy (TFLM vs NNoM/Edge Impulse/μTVM) covered in [[concepts/tinymlops|TinyMLOps]]; surveys the five model-compression methods with a unifying [[concepts/bayesian-compression|Bayesian compression]] synthesis; targets the extreme-low-power regime (<8 kB SRAM, Cortex-M0+/eDMPv1); provides per-dataset Flash-size-vs-accuracy landscapes overlaid with Cortex-M0+/M4/M7 memory thresholds for MNIST, ImageNet, VWW, and Google Speech Commands v2-12
