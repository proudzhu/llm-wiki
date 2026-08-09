---
type: concept
created: 2026-08-09
updated: 2026-08-09
sources:
  - raw/papers/lin-2020-mcunet/full-text.md
  - raw/papers/lin-2021-mcunetv2/full-text.md
tags:
  - tinyml
  - inference-engine
  - efficient-deep-learning
  - microcontroller
  - memory-optimization
---

# TinyEngine

**TinyEngine** is the memory-efficient inference engine component of [[sources/lin-2020-mcunet\|MCUNet (Lin et al. 2020)]], co-designed with [[concepts/tinynas\|TinyNAS]]. It replaces interpreter-based MCU inference libraries (TF-Lite Micro, CMSIS-NN, CMix-NN) with a compile-time code-generation approach, and adds model-adaptive memory scheduling, kernel specialization, and in-place depth-wise convolution. On MCUs it reduces peak memory by **3.4×** and accelerates inference by **1.7–3.3×** vs. TF-Lite Micro and CMSIS-NN.

## Motivation

On memory-starved microcontrollers the inference library is not merely a speed knob — it determines the *accuracy ceiling* of the searchable model, because a more memory-efficient library fits a larger runnable network. Interpreter-based libraries (TF-Lite Micro, CMSIS-NN) waste up to **65% of peak memory** on runtime meta-information (model-structure parameters) and add ~22% latency from runtime graph interpretation; they also optimize memory layer-by-layer, missing global reuse opportunities.

## Techniques

### 1. Code Generation instead of Interpretation

TinyEngine offloads model-structure handling from runtime to **compile time**: it generates only the specialized code that the searched TinyNAS model will execute, rather than shipping a general interpreter. This eliminates runtime meta-information memory and interpretation latency, and shrinks binary size by up to **4.5× / 5.0×** vs. TF-Lite Micro / CMSIS-NN (which must compile every operation for cross-model support).

### 2. Model-Adaptive Memory Scheduling

Instead of a per-layer buffer, TinyEngine computes a **global** maximum column memory across all layers,

$$M = \max\left(\text{kernel size}_{L_i}^2 \cdot \text{in channels}_{L_i};\ \forall L_i \in L\right),\tag{1}$$

then tiles each layer $L_j$'s feature-map width to fit as many im2col columns as possible in $M$:

$$\text{tiling size}_{L_j} = \left\lfloor M / \left(\text{kernel size}_{L_j}^2 \cdot \text{in channels}_{L_j}\right) \right\rfloor.\tag{2}$$

Two models with identical layer configurations can therefore receive different schedules, maximizing input reuse and reducing fragmentation. This yields **+13%** inference efficiency.

### 3. Computation Kernel Specialization

Per-layer loop tiling (kernel-size- and memory-dependent), inner-loop unrolling specialized per kernel size (9 segments for 3×3, 25 for 5×5) to remove branch overhead, and Conv+Padding+ReLU+BN operation fusion. Adds **+22%** efficiency.

### 4. In-Place Depth-Wise Convolution

Because [[concepts/depthwise-separable-convolution\|depth-wise convolution]] does not mix channels, once a channel's output is computed its input activation can be overwritten by another channel's output. The first channel's output is held in a temporary buffer and written back to the last channel's input at the end, reducing depth-wise-conv activation memory from $2N$ to $N+1$ — a **1.6×** measured reduction. This is the v2 (NeurIPS camera-ready) addition to TinyEngine.

> **Disambiguation**: This "in-place depth-wise convolution" (overwriting activations channel-by-channel to save SRAM) is **unrelated** to [[concepts/inplace-convolution\|inplace convolution]] in the speech-enhancement literature, which denotes stride-1 frequency-axis convolution that avoids frequency downsampling. The two concepts share a name but address different problems on different hardware.

## Empirical Impact

- **Speed**: 3× faster than TF-Lite Micro, 1.6× faster than CMSIS-NN (Figure 4a).
- **Memory**: runs model configurations (w{}-r{}) that other libraries mark out-of-memory, enlarging TinyNAS's design space (Figure 4b).
- **Co-design gain**: on STM32F746 (320 kB / 1 MB), switching the library from CMSIS-NN to TinyEngine raises ImageNet accuracy from 35.2% → 47.4% (S-MbV2) and 49.5% → 56.4% (S-Proxyless) *for the same model family* — direct evidence that library efficiency lifts the accuracy ceiling.

## MCUNetV2 Extension: Patch-based Inference Support

[[sources/lin-2021-mcunetv2\|MCUNetV2 (Lin et al. 2021)]] extends TinyEngine to support [[concepts/patch-based-inference\|patch-based inference]]. The engine now allocates the patch buffer for the memory-intensive initial stage and orchestrates the patch-by-patch execution loop, while the rest of the network continues to use the per-layer schedule with code generation, model-adaptive memory scheduling, kernel specialization, and in-place depth-wise convolution. This extension is what enables the 4–8× peak SRAM reduction on existing networks and the record MCU results (71.8% ImageNet top-1, >90% VWW under 32 kB SRAM, +16.9% mAP on Pascal VOC) reported in MCUNetV2.

## Related Concepts

- [[concepts/tinyml\|TinyML]] — problem domain
- [[concepts/tinynas\|TinyNAS]] — co-designed NAS that uses TinyEngine to measure per-candidate memory
- [[concepts/patch-based-inference\|Patch-based Inference]] — the scheduling strategy TinyEngine is extended to support in MCUNetV2
- [[concepts/receptive-field-redistribution\|Receptive Field Redistribution]] — companion technique minimizing overlapping-patch overhead
- [[concepts/imbalanced-memory-distribution\|Imbalanced Memory Distribution]] — the pattern that motivates patch-based scheduling
- [[concepts/depthwise-separable-convolution\|Depthwise Separable Convolution]] — operator optimized by in-place scheduling
- [[concepts/inplace-convolution\|Inplace Convolution]] — distinct SE concept sharing a name (see disambiguation above)

## Related Sources

- [[sources/lin-2020-mcunet\|Lin et al. 2020: MCUNet — Tiny Deep Learning on IoT Devices]]
- [[sources/lin-2021-mcunetv2\|Lin et al. 2021: MCUNetV2 — Memory-Efficient Patch-based Inference for Tiny Deep Learning]]
