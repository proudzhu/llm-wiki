---
type: concept
created: 2026-08-09
updated: 2026-08-09
sources:
  - raw/papers/lin-2023-tinyml-progress-futures/full-text.md
tags:
  - tinyml
  - on-device-training
  - inference-engine
  - efficient-deep-learning
  - microcontroller
  - memory-optimization
---

# Tiny Training Engine (TTE)

**Tiny Training Engine (TTE)** is the compile-time training system component of MCUNetV3 that transforms the algorithm-side savings of [[concepts/quantization-aware-scaling\|Quantization-Aware Scaling (QAS)]] and [[concepts/sparse-update\|Sparse Update]] into measured memory and latency reductions on bare-metal microcontrollers. TTE offloads auto-differentiation from runtime to compile time, prunes the backward graph for frozen tensors, reorders gradient operators for in-place updates, and generates specialized binary code — the training analogue of [[concepts/tinyengine\|TinyEngine]]'s code-generation approach to inference. It is surveyed in [[sources/lin-2023-tinyml-progress-futures\|Lin et al. 2023: TinyML — Progress and Futures]] as the system-side half of MCUNetV3.

## Motivation

Existing deep-learning training frameworks (PyTorch, TensorFlow, JAX, MXNet) target cloud servers and consume >300 MB even when training a small MobileNetV2-w0.35 at batch size 1 — a >1000× gap versus a 256 kB MCU SRAM budget. Edge inference frameworks (TVM, TF-Lite, NCNN) provide slim runtimes but lack back-propagation support. Without a training system co-designed for MCUs, the theoretical memory savings of QAS and sparse update do not translate into measured savings: a generic runtime still pays for unused gradient nodes, intermediate activation buffers, and Python host-language overhead.

## Core Techniques

### 1. Compile-Time Differentiation + Code Generation

TTE traces the forward graph for a given model and *derives the corresponding backward graph at compile time*, rather than at runtime. The static backward graph can then be pruned and reordered (below) and compiled to specialized bare-metal binaries — eliminating the Python host language and runtime auto-differentiation overhead.

### 2. Backward Graph Pruning for Sparse Update

For [[concepts/sparse-update\|sparse layer update]], TTE prunes the gradient nodes of frozen weights, keeping only the bias-update nodes. It then traverses the graph to find intermediate nodes (e.g., saved input activations) made dead by pruning and applies **dead-code elimination (DCE)**.

For **sparse tensor update**, TTE introduces a *sub-operator slicing* mechanism: a layer's weights are split into trainable and frozen subsets, and only the backward graph of the trainable subset is compiled. This is what turns "update 1/8 of the channels of layer $i$" from a runtime check into a compile-time constant.

Backward graph pruning alone reduces training memory by 7–9×.

### 3. Operator Reordering for In-Place Updates

Traditional training frameworks compute all gradients first, then apply all updates — requiring enough memory to hold every gradient simultaneously. TTE traces tensor dependencies (weights, gradients, activations) and **reorders operators** so the gradient of a tensor can be applied *in-place* immediately after it is computed, then released before backpropagating to earlier layers. Operator fusion further eliminates large intermediate tensors.

Operator reordering contributes an additional 2.4–3.2× memory reduction.

## Empirical Impact (STM32F746 MCU)

- **Peak memory**: sparse update + TTE graph optimization reduces measured peak training memory by **20–21×** across three MCUNet models, fitting all three into 256 kB SRAM.
- **Training speed**: 23–25× faster than full-update + TF-Lite Micro kernels (loop unrolling, tiling, and other compiler optimizations on top of graph-level savings), reducing energy per update and making on-device training practical.
- **Combined with QAS + sparse update algorithm**: MCUNetV3 reaches **89.3% VWW transfer-learning accuracy at 173 kB peak memory** — first system to enable real quantized-graph training on a 256 kB MCU.

## Relation to TinyEngine

TTE is the training-side counterpart of [[concepts/tinyengine\|TinyEngine]] (the inference engine of MCUNet V1/V2). Both share the code-generation philosophy — offload graph handling to compile time, ship only the specialized code that will actually execute. TTE extends this to the backward graph, adding the auto-differentiation trace, backward-graph pruning, and gradient-operator reordering that inference engines do not need.

## Related Concepts

- [[concepts/quantization-aware-scaling\|Quantization-Aware Scaling (QAS)]] — algorithm-side fix that TTE compiles
- [[concepts/sparse-update\|Sparse Update]] — algorithm-side selection that TTE compiles via backward-graph pruning
- [[concepts/tinyengine\|TinyEngine]] — inference-side sibling; same code-generation philosophy
- [[concepts/tinyml\|TinyML]] — problem domain
- [[concepts/online-learning\|Online Learning]]
- [[concepts/continuous-learning\|Continuous Learning]]

## Related Sources

- [[sources/lin-2023-tinyml-progress-futures\|Lin et al. 2023: TinyML — Progress and Futures]] — surveys TTE as part of the MCUNetV3 on-device-training contribution
