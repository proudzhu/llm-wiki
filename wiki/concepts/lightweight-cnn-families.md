---
type: concept
created: 2026-08-09
updated: 2026-08-09
sources:
  - raw/papers/liu-2024-lightweight-dl-survey/full-text.md
tags:
  - lightweight-deep-learning
  - cnn
  - architecture
  - efficient-deep-learning
  - taxonomy
---

# Lightweight CNN Families

**Lightweight CNN Families** is a taxonomy introduced by [[sources/liu-2024-lightweight-dl-survey|Liu et al. 2024]] that organizes efficient CNN architectures into chronological **"series"** reflecting the evolution of lightweight design. Unlike flat lists of architectures, the series view exposes how each family addressed the limitation of its predecessor — typically the tension between reducing FLOPs/parameters and the resulting increase in Memory Access Cost (MAC), which dominates inference time on real hardware.

## Motivation: Why FLOPs ≠ Inference Speed

Early lightweight architectures (SqueezeNet, MobileNet) reduced parameters and FLOPs but often **increased** MAC, leading to slower inference. This is because element-wise operations, depthwise convolutions, and 1×1 convolutions have low FLOPs but high memory traffic per FLOP. The series taxonomy tracks the design responses to this insight.

## The Six Series

### 1. SqueezeNet Series

- **Fire module** (SqueezeNet, 2016): squeeze layer (1×1 conv) compresses channels, expand layer (1×1 + 3×3 conv) separates the operation. Achieves AlexNet-level accuracy with 50× fewer parameters.
- **SqueezeNext**: decomposes 3×3 kernel into 3×1 + 1×3 (parameters $k^2 \to 2k$), adds ResNet-style shortcuts. 112× parameter reduction vs. AlexNet.

### 2. ShuffleNet Series

- **ShuffleNet** (2017): channel shuffle after 1×1 group convolution enables cross-group information exchange — addressing the blocked information flow in standard group convolution.
- **ShuffleNetV2** (2018): four practical guidelines for memory-efficient design:
  1. Equal input/output channel dimensions → smaller MAC.
  2. Large groups → large MAC (especially for depthwise separable convs).
  3. Avoid wide/fragmented networks (e.g., Inception) → large MAC.
  4. Avoid element-wise operations → low FLOPs but high MAC.

### 3. CondenseNet Series

- **CondenseNet** (2017): Learned Group Convolutions (LGCs) progressively prune unimportant connections during training.
- **CondenseNetV2** (2021): sparse feature reactivation module reactivates outdated features by relearning connection weights during training (CondenseNet fixes them after pruning). See [[sources/liu-2024-lightweight-dl-survey|Liu et al. 2024]] Figure 1 for the visual comparison with DenseNet.

### 4. MobileNet Series

- **MobileNet** (V1, 2017): depthwise separable convolutions for efficient mobile inference (see [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]).
- **MobileNetV2** (2018): inverted residual block + linear bottleneck — expands channels inside the residual, projects back down at the output, replacing ReLU with linear combination in the last layer to mitigate low-dimensional information loss.
- **MobileNetV3** (2019): platform-aware NAS + SENet (channel attention) in bottleneck + H-swish activation (quantization-friendly, lower MAC than ReLU6).
- **MobileNeXt** (2020): Sandglass block — flips the inverted residual to enhance gradient transmission in wider architectures.

### 5. Shift-Based Series

Replaces multiplications with shift operations (zero parameters, zero FLOPs in the shift itself):
- **ShiftNet** (2018): Group Shift convolution replacing spatial convolutions.
- **Active Shift Layer** (Jeon et al.): learnable shifts instead of heuristic assignments.
- **Sparse Shift Layer** (Chen et al.): eliminates meaningless memory movement; non-shift channels unchanged.
- **AddressNet**: channel shift instead of channel shuffle (avoids permutation overhead) for GPU speed.
- **DeepShift**: bit-wise shifts + sign flips replacing all multiplications.

### 6. Add-Based Series

Replaces multiplications with additions (lower energy):
- **AdderNet** (2020): L1-norm distance as filter-response criterion (Absolute-difference-accumulation).
- **ShiftAddNet** (2021): combines bit-wise shifts (hardware efficiency) with additive networks (expressive capacity) — proposes "expressive capacity" as a metric comparing accuracy under similar hardware conditions.

## Cross-Family Insights

- **MAC, not FLOPs, drives real inference time** — this unifying insight motivates the design rules of ShuffleNetV2 and the architecture choices of MobileNetV3.
- **Multiplication-free operations** (shift, add) achieve extreme FLOPs reduction but trade off against expressive capacity and hardware-specific deployment concerns.
- **Hybrid shift+add** approaches (ShiftAddNet) attempt to recover the lost accuracy while preserving hardware efficiency.

## Related Concepts

- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]] — foundational operation underlying MobileNet and several other series
- [[concepts/attention-mechanism|Attention Mechanism]] — the basis for SENet channel attention integrated into MobileNetV3
- [[concepts/neural-architecture-search|Neural Architecture Search]] — used by MobileNetV3's platform-aware NAS
- [[concepts/tinyml|TinyML]] — the deployment target where these families' memory footprint matters most

## Related Sources

- [[sources/liu-2024-lightweight-dl-survey|Liu et al. 2024: Lightweight Deep Learning for Resource-Constrained Environments]] — introduces the six-series taxonomy
