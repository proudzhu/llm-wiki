---
type: concept
created: 2026-08-09
updated: 2026-08-09
sources:
  - raw/papers/lin-2020-mcunet/full-text.md
  - raw/papers/lin-2021-mcunetv2/full-text.md
  - raw/papers/lin-2023-tinyml-progress-futures/full-text.md
tags:
  - neural-architecture-search
  - tinyml
  - efficient-deep-learning
  - microcontroller
---

# TinyNAS

**TinyNAS** is the neural-architecture-search (NAS) component of [[sources/lin-2020-mcunet\|MCUNet (Lin et al. 2020)]]. It is a **two-stage NAS** that first *automatically optimizes the search space* to fit tiny and diverse MCU memory constraints, then *specializes the network architecture* within that optimized space. Its distinguishing contribution over prior mobile-grade NAS (MnasNet, ProxylessNAS, FBNet) is handling peak-SRAM and Flash constraints — rather than FLOPs/latency — at low search cost.

## Motivation

The performance of [[concepts/neural-architecture-search\|NAS]] depends heavily on the search space, yet there are no standard MCU model designs and hence no standard MCU search spaces. Manual per-device tuning is labor-intensive given the diversity of MCU constraints (SRAM from 256 kB to 512 kB, Flash from 1 MB to 2 MB, latency targets from 5 to 10 FPS). Naively using a mobile search space (224 resolution, MobileNetV2-derived) yields models that exceed MCU memory by 5×.

## Stage 1: Automated Search-Space Optimization

The mobile search space is scaled over input resolution $R = \{48, 64, 80, \ldots, 192, 208, 224\}$ (12 values) and width multiplier $W = \{0.2, 0.3, 0.4, \ldots, 1.0\}$ (9 values), giving $12 \times 9 = 108$ candidate configurations $S = W \times R$. Each configuration contains $\sim 3.3 \times 10^{25}$ sub-networks.

Selecting the best $S^*$ by running NAS on every configuration is intractable. Instead TinyNAS:

1. Samples $m = 1000$ networks from each configuration.
2. Uses [[concepts/tinyengine\|TinyEngine]] to measure each network's optimal memory schedule and discards those that violate the SRAM/Flash budget.
3. Builds the **FLOPs cumulative distribution function (CDF)** of the *satisfying* networks.
4. Selects the configuration with the **largest mean FLOPs** among satisfying networks.

The insight is that within a model family, larger FLOPs implies larger capacity and thus higher achievable accuracy; the configuration whose satisfying models have the highest mean FLOPs is therefore the best bet. This stage requires **no training** (~2 CPU hours) and is reusable across constraints.

## Stage 2: Resource-Constrained Model Specialization

Within the selected $S^*$, TinyNAS trains one **super network** via weight sharing (initialized from the largest sub-network, channels sorted by L1-norm importance) covering variable kernel sizes (3/5/7), expansion ratios (3/4/6), and stage depths (2/3/4) — $2 \times 10^{19}$ sub-networks. It then runs **evolution search** (population 100, 30 iterations, top-20 survive, 50 crossover + 50 mutated candidates at $p=0.1$ per generation), evaluating each candidate's accuracy on a held-out training split and measuring its memory with TinyEngine to enforce the resource budget.

## Key Results

- On ImageNet-100 (320 kB/1 MB), the TinyNAS-selected space reaches 78.7% top-1, vs. 77.0% for a "huge" space that *contains* the best space (overly large spaces harm super-net training/evolution) and 74.7% for random spaces — validating the CDF selection criterion.
- The selected architecture has a **more balanced per-block peak activation** than scaled MobileNetV2 (0.3×), which has one block with 2.2× the average activation; balance lets TinyNAS fit higher overall capacity at the same SRAM, discovered automatically without memory-distribution heuristics.
- Search-space optimization reveals non-trivial patterns: increasing SRAM alone raises chosen resolution; increasing Flash alone raises chosen width while *lowering* resolution to fit unchanged SRAM.
- Design cost is ~300 GPU hours (one-shot NAS) + ~2 CPU hours (space optimization), a **133× reduction** over MnasNet's 40,000 GPU hours, cutting per-model CO₂ emission from 11,345 lbs to 85 lbs.

## Relation to General NAS

TinyNAS extends general [[concepts/neural-architecture-search\|Neural Architecture Search]] with two MCU-specific ideas: (1) *search-space optimization as a first-class stage* (prior NAS assumes a fixed mobile space), and (2) *co-design with the inference engine* so that the memory schedule, not just FLOPs, is the constraint measured during search.

## MCUNetV2 Extension: Joint Architecture + Inference-Scheduling Search

[[sources/lin-2021-mcunetv2\|MCUNetV2 (Lin et al. 2021)]] extends TinyNAS with two changes that merge V1's two-stage search-space optimization into a single stage:

1. **Per-block width multiplier** $w_{[\,]} \in \{0.5, 0.75, 1.0\}$ and **input resolution** $r \in \{96, 128, 160, 192, 224, 256\}$ are added *directly to the search space*, rather than being optimized in a separate pre-NAS stage. The same super network can therefore span tight resource budgets (ablation: Table 6 of the paper shows this beats V1's two-stage method and prior NAS+scale approaches at 25/50/100M MACs budgets, with the gain largest at ≤25M).
2. **Inference-scheduling knobs** — patch count $p \in \{1, 2, 3, 4\}$ (image split into $p \times p$ overlapping patches) and patch-stage depth $n$ (number of initial blocks executed patch-by-patch) — are co-optimized with the architecture, enabling [[concepts/patch-based-inference\|patch-based inference]] and [[concepts/receptive-field-redistribution\|receptive field redistribution]] to be discovered automatically rather than tuned case-by-case.

The discovered architectures consistently show small kernels (1×1, 3×3) in the patch stage, small expansion ratios early in the per-layer stage, and avoid combining large expansion ratios with large kernels — patterns discovered without human expertise.

## Related Concepts

- [[concepts/tinyml\|TinyML]] — problem domain
- [[concepts/tinyengine\|TinyEngine]] — co-designed inference engine that measures per-candidate memory
- [[concepts/neural-architecture-search\|Neural Architecture Search]] — general framework
- [[concepts/patch-based-inference\|Patch-based Inference]] — the scheduling strategy co-optimized by MCUNetV2's NAS
- [[concepts/receptive-field-redistribution\|Receptive Field Redistribution]] — automated by MCUNetV2's joint search
- [[concepts/imbalanced-memory-distribution\|Imbalanced Memory Distribution]] — motivates patch-based inference
- [[concepts/depthwise-separable-convolution\|Depthwise Separable Convolution]] — building block of the scaled mobile search space

## Related Sources

- [[sources/lin-2020-mcunet\|Lin et al. 2020: MCUNet — Tiny Deep Learning on IoT Devices]]
- [[sources/lin-2021-mcunetv2\|Lin et al. 2021: MCUNetV2 — Memory-Efficient Patch-based Inference for Tiny Deep Learning]]
- [[sources/lin-2023-tinyml-progress-futures\|Lin et al. 2023: TinyML — Progress and Futures]] — surveys TinyNAS within the MCUNet V1/V2/V3 co-design arc
