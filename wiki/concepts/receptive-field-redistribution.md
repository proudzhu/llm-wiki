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
  - neural-architecture-search
---

# Receptive Field Redistribution

**Receptive field (RF) redistribution** is the companion technique to [[concepts/patch-based-inference\|patch-based inference]] introduced by [[sources/lin-2021-mcunetv2\|MCUNetV2 (Lin et al. 2021)]] to minimize the computation overhead caused by overlapping input patches. The idea is to **shift receptive field from the patch-based initial stage to the per-layer later stage**: smaller kernels and fewer blocks early (smaller input patches, less overlapping), compensated by more RF in the later stage (preserving task performance, especially for detecting large objects).

## Motivation

[[concepts/patch-based-inference\|Patch-based inference]] cuts peak SRAM by 4–8× but incurs computation overhead proportional to the receptive field of the patch-based stage: a larger RF means each input patch must be larger to cover the output patch's dependencies, hence more overlap and repeated computation.

For MobileNetV2 at 224×224 with 4×4 patches, the per-layer-equivalent input patch side would be $224/4 = 56$, but accounting for the actual receptive field it grows to 75, causing a 42% overhead in the patch stage (10% overall). Reducing the RF of the patch stage therefore directly shrinks the input patch size and the overlap.

## Mechanism

Manual redistribution of MobileNetV2 ("MbV2-RD"):

- **Initial patch-based stage**: use smaller kernel sizes and fewer blocks → smaller receptive field → smaller input patches.
- **Later per-layer stage**: increase the number of blocks to enlarge the RF → compensates for the performance loss on tasks sensitive to global context (e.g., detecting large objects in Pascal VOC).

The resulting network has the same overall depth/capacity but a different RF distribution.

## Empirical Impact

Applied to MobileNetV2 (MCUNetV2 Table 1, 224×224 input, 4×4 patches, int8):

| Model | Patch Size | Patch-stage overhead | Overall overhead | Peak SRAM | ImgNet Top-1 | VOC mAP |
|---|---|---|---|---|---|---|
| MbV2 (original) | 75² | +42% | +10% | 172 kB (8× ↓) | 72.2% | 75.4% |
| **MbV2-RD (redistributed)** | **63²** | **+18%** | **+3%** | 172 kB (8× ↓) | 72.1% | 75.7% |

Redistribution shrinks the input patch side from 75 to 63, cuts the overall overhead from 10% to **3%** (negligible), and *matches or slightly improves* both ImageNet top-1 and Pascal VOC mAP. On-device, MbV2-RD's latency overhead is only **4%**.

## Automation via Joint NAS

Manual redistribution is case-by-case and varies by backbone, dataset, and hardware. [[sources/lin-2021-mcunetv2\|MCUNetV2]] automates it via joint [[concepts/neural-architecture-search\|neural architecture search]] and inference-scheduling search: the search space includes per-block kernel size $k \in \{3,5,7\}$, expansion ratio $e \in \{3,4,6\}$, stage depth $d \in \{2,3,4\}$, per-block width $w \in \{0.5,0.75,1.0\}$, input resolution $r$, patch count $p$, and patch-stage depth $n$. The discovered architectures (Figure 9 of the paper) consistently show:

- Small kernels (1×1, 3×3) in the patch-based stage to reduce RF and overlapping.
- Small expansion ratios in the early per-layer stage (further reducing peak memory); larger expansion ratios later for capacity.
- Large expansion ratios and large kernels rarely co-occur (to limit computational cost).
- Larger input resolution on resolution-sensitive datasets like Visual Wake Words.

These patterns are discovered automatically, without human expertise.

## Related Concepts

- [[concepts/patch-based-inference\|Patch-based Inference]] — the scheduling technique whose overhead RF redistribution minimizes
- [[concepts/imbalanced-memory-distribution\|Imbalanced Memory Distribution]] — motivates the patch-based stage
- [[concepts/tinyml\|TinyML]] — problem domain
- [[concepts/neural-architecture-search\|Neural Architecture Search]] — automates the redistribution
- [[concepts/tinynas\|TinyNAS]] — extended in MCUNetV2 with $n$, $p$, $r$, and per-block $w$ knobs

## Related Sources

- [[sources/lin-2021-mcunetv2\|Lin et al. 2021: MCUNetV2 — Memory-Efficient Patch-based Inference for Tiny Deep Learning]]
