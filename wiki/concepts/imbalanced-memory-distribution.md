---
type: concept
created: 2026-08-09
updated: 2026-08-09
sources:
  - raw/papers/lin-2021-mcunetv2/full-text.md
tags:
  - tinyml
  - memory-optimization
  - efficient-deep-learning
  - microcontroller
  - convolutional-neural-network
---

# Imbalanced Memory Distribution

**Imbalanced memory distribution** is a structural pattern of convolutional neural networks identified and named by [[sources/lin-2021-mcunetv2\|MCUNetV2 (Lin et al. 2021)]]: in typical efficient CNN backbones, the **first few blocks** consume an order of magnitude more SRAM than the rest of the network, becoming the memory bottleneck. The rest of the network already fits comfortably within MCU memory budgets, leaving a large optimization headroom if the initial stage can be "bypassed."

## The Pattern

Profiling MobileNetV2 (int8, 224×224 input) per-block:

- The **first 5 blocks** have peak memory >450 kB — exceeding typical MCU SRAM budgets (256–512 kB).
- The **remaining 13 blocks** easily fit 256 kB.
- The peak memory of the initial memory-intensive stage is **8× higher** than the rest of the network.

The pattern is generic across efficient CNN backbones. MCUNetV2's Appendix C confirms it for MnasNet, FBNet, and even MCUNet-320kB (a model specialized for memory-constrained settings) — patch-based inference can cut their peak memory by 3.5–6.1×.

## Root Cause: Hierarchical Structure

The imbalance arises from the **hierarchical design** of single-branch and residual CNNs:

- After each stage, the spatial resolution is down-sampled by 2×, reducing the number of pixels by **4×**.
- The channel count typically increases by only **2×** (VGG, ResNet) or by an even smaller ratio (MobileNetV2, ShuffleNet, EfficientNet).

The net effect is that activation size $H \times W \times C$ **decreases** through the network: halving each dimension reduces area by 4×, while doubling channels only adds 2×, so the product shrinks by 2× per stage. The early-stage activations are therefore the largest, dominating peak memory.

Concretely, the first convolution of MobileNetV2 (3 → 32 channels, stride 2) on a 224×224 image requires

$$3 \times 224^{2} + 32 \times 112^{2} = 539\ \text{kB}\quad(\text{int8}),$$

which already exceeds a typical MCU's SRAM — before any subsequent layer is even considered.

## Implications

The imbalance has two consequences exploited by MCUNetV2:

1. **Bypassing the initial stage yields disproportionate gains.** If one can execute the initial memory-intensive stage without holding its full activation, the rest of the network is already MCU-friendly — cutting overall peak memory by up to 8×.
2. **Resolution-sensitive tasks are most affected.** Because the initial-stage memory scales with input resolution $r^{2}$, tasks that need high resolution (e.g., object detection, whose accuracy degrades much faster than classification as $r$ drops) are disproportionately constrained by the initial-stage bottleneck. This is why MCUNet V1 could not achieve decent detection mAP on MCUs, and why MCUNetV2's [[concepts/patch-based-inference\|patch-based inference]] — by breaking the initial-stage bottleneck — unlocks object detection on MCUs.

## Remedy

[[sources/lin-2021-mcunetv2\|MCUNetV2]] addresses the imbalance with [[concepts/patch-based-inference\|patch-based inference]], which runs the initial stage patch-by-patch so that only one small patch's activation is held in SRAM at a time, rather than the full feature map. The rest of the network (already small in memory) continues with per-layer execution. [[concepts/receptive-field-redistribution\|Receptive field redistribution]] then minimizes the computation overhead introduced by overlapping patches.

## Related Concepts

- [[concepts/patch-based-inference\|Patch-based Inference]] — the scheduling technique that bypasses the initial-stage bottleneck
- [[concepts/receptive-field-redistribution\|Receptive Field Redistribution]] — minimizes the resulting overlapping-patch overhead
- [[concepts/tinyml\|TinyML]] — the problem domain where the imbalance is most binding
- [[concepts/depthwise-separable-convolution\|Depthwise Separable Convolution]] — building block of the efficient backbones exhibiting the imbalance

## Related Sources

- [[sources/lin-2021-mcunetv2\|Lin et al. 2021: MCUNetV2 — Memory-Efficient Patch-based Inference for Tiny Deep Learning]]
