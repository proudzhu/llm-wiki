---
type: source
created: 2026-08-09
updated: 2026-08-09
sources:
  - raw/papers/lin-2020-mcunet/full-text.md
  - https://doi.org/10.48550/arXiv.2007.10319
  - zotero://select/items/0_T3XNP2YC
tags:
  - tinyml
  - neural-architecture-search
  - efficient-deep-learning
  - microcontroller
  - inference-engine
  - model-compression
---

# Lin, Chen, Lin, Cohn, Gan & Han 2020: MCUNet — Tiny Deep Learning on IoT Devices

| | |
|---|---|
| **Authors** | [[entities/ji-lin\|Ji Lin]], [[entities/wei-ming-chen\|Wei-Ming Chen]], [[entities/yujun-lin\|Yujun Lin]], [[entities/john-cohn\|John Cohn]], [[entities/chuang-gan\|Chuang Gan]], [[entities/song-han\|Song Han]] |
| **Institutions** | MIT; National Taiwan University; MIT-IBM Watson AI Lab |
| **Venue** | NeurIPS 2020 (preprint v2: 2020-11-19, camera ready) |
| **Type** | Conference paper (preprint on arXiv) |
| **DOI** | [10.48550/arXiv.2007.10319](https://doi.org/10.48550/arXiv.2007.10319) |
| **arXiv** | [2007.10319](http://arxiv.org/abs/2007.10319) |
| **Zotero** | [T3XNP2YC](zotero://select/items/0_T3XNP2YC) |
| **Code** | https://github.com/mit-han-lab/mcunet |

## Summary

MCUNet is a **system–algorithm co-design** framework that enables ImageNet-scale deep-learning inference on off-the-shelf microcontrollers (MCUs), whose SRAM/Flash are 3–6 orders of magnitude smaller than cloud/mobile hardware. It jointly optimizes an efficient neural architecture search method ([[concepts/tinynas\|TinyNAS]]) and a memory-efficient inference engine ([[concepts/tinyengine\|TinyEngine]]). MCUNet is the first system to exceed 70% ImageNet top-1 accuracy (70.7%) on a commercial MCU (STM32H743), using 3.5× less SRAM and 5.7× less Flash than int8 MobileNetV2/ResNet-18 at comparable accuracy.

## Problem Formulation

The core obstacle to [[concepts/tinyml\|TinyML]] is the extreme memory scarcity of microcontrollers. A representative ARM Cortex-M7 MCU (STM32F746) provides only **320 kB SRAM** (constrains activation size, read & write) and **1 MB Flash** (constrains model size, read-only). For context:

| | Cloud AI (V100) | Mobile AI (iPhone 11) | Tiny AI (STM32F746) |
|---|---|---|---|
| **Memory** | 16 GB | 4 GB | 320 kB |
| **Storage** | TB–PB | >64 GB | 1 MB |

Standard models far exceed these budgets: ResNet-50 exceeds the storage limit by ~100×; MobileNetV2 exceeds peak SRAM by ~22×; even int8 MobileNetV2 still needs 5.3× the available memory. Crucially, existing efficient architectures reduce *model size* but not *peak activation*: at ~70% ImageNet accuracy, MobileNetV2 is 4.6× smaller than ResNet-18 yet has 1.8× *larger* peak activation, making it *harder* to fit in SRAM.

![[raw/papers/lin-2020-mcunet/figures/ee70659adf8b852cb8504236591745215d25b22b5726caf79d10e34aeba0e038.jpg|Figure 1]]
*Figure 1: MobileNetV2 reduces model size but not peak memory, while MCUNet effectively reduces both parameter size and activation size.*

The goal is therefore to find an architecture $\mathcal{A}^*$ and an inference schedule that jointly maximize accuracy subject to *both* peak-SRAM and Flash constraints, rather than the FLOPs/latency targets used by mobile-grade NAS. Existing NAS search spaces (derived from MobileNetV2 at 224 resolution) do not fit MCUs, and interpreter-based inference libraries (TF-Lite Micro, CMSIS-NN) waste 65% of peak memory on runtime meta-information.

## Methodology

MCUNet couples two components in a single optimization loop: [[concepts/tinynas\|TinyNAS]] designs the network, [[concepts/tinyengine\|TinyEngine]] provides the memory schedule, and each informs the other's search space.

![[raw/papers/lin-2020-mcunet/figures/71f5367408ed4880b7f039a13bad6e63a8074446a8eaedb6ebf8cd109c964235.jpg|Figure 2]]
*Figure 2: MCUNet jointly designs the neural architecture (TinyNAS) and the inference scheduling (TinyEngine). TinyEngine makes full use of limited MCU resources, enlarging the design space for architecture search, so TinyNAS is more likely to find a high-accuracy model.*

### TinyNAS: Two-Stage NAS under Tiny Memory Constraints

TinyNAS addresses the absence of standard MCU search spaces with a two-stage approach.

**Stage 1 — Automated search-space optimization.** The mobile search space is scaled over input resolution $R = \{48, 64, 80, \ldots, 192, 208, 224\}$ (12 values) and width multiplier $W = \{0.2, 0.3, 0.4, \ldots, 1.0\}$ (9 values), giving $12 \times 9 = 108$ candidate search-space configurations $S = W \times R$, each containing $\sim 3.3 \times 10^{25}$ sub-networks. Rather than running NAS on every $S$ (astronomical cost), TinyNAS samples $m = 1000$ networks per space, uses TinyEngine to measure each one's optimal memory schedule, keeps only the networks that satisfy the memory constraint, and compares the **FLOPs cumulative distribution function (CDF)** of the satisfying networks. The insight is that, within a model family, larger FLOPs implies larger capacity and thus higher achievable accuracy; therefore the space with the largest mean FLOPs among satisfying networks is selected as $S^*$. This stage needs no training and costs ~2 CPU hours, reusable across constraints.

![[raw/papers/lin-2020-mcunet/figures/9fc2a0f63dbc195f875c4f439ea2b10eee4d808e0fd6c7c3246bcf548b265a60.jpg|Figure 3]]
*Figure 3: TinyNAS selects the best search space by analyzing the FLOPs CDF of different search spaces. The solid-red space's top-20% of models exceed 50.3M FLOPs vs. 32.3M for solid-black, and searching the red space yields 4.5% higher final accuracy.*

**Stage 2 — Resource-constrained model specialization.** Within $S^*$, TinyNAS trains one **super network** via weight sharing (initialized from the largest sub-network, channels sorted by L1-norm importance) covering variable kernel sizes (3/5/7), expansion ratios (3/4/6), and stage depths (2/3/4) — $2 \times 10^{19}$ sub-networks. It then runs **evolution search** (population 100, 30 iterations, top-20 survival, crossover + 0.1 mutation rate) to find the sub-network with the highest validation accuracy that fits the on-board resource budget, where each candidate's memory is measured by TinyEngine. This one-shot design reduces search cost to ~300 GPU hours, a 133× reduction over MnasNet's 40,000 GPU hours.

### TinyEngine: Memory-Efficient Inference Library

TinyEngine replaces the interpreter-based execution of TF-Lite Micro / CMSIS-NN with four techniques:

1. **Code generation instead of interpretation.** Model structure parameters are offloaded from runtime to compile time; only the code that the searched TinyNAS model will execute is generated. This eliminates runtime meta-information overhead (up to 65% of peak memory in interpreter-based libraries) and avoids interpretation latency. Binary size shrinks up to 4.5×/5.0× vs. TF-Lite Micro/CMSIS-NN.

2. **Model-adaptive memory scheduling.** Rather than per-layer buffers, TinyEngine computes the global maximum column memory $M$ across all layers,

$$M = \max\left(\text{kernel size}_{L_i}^2 \cdot \text{in channels}_{L_i};\ \forall L_i \in L\right),\tag{1}$$

then tiles each layer $L_j$'s feature-map width to fit as many im2col columns as possible in $M$:

$$\text{tiling size}_{L_j} = \left\lfloor M / \left(\text{kernel size}_{L_j}^2 \cdot \text{in channels}_{L_j}\right) \right\rfloor.\tag{2}$$

Two models with identical layer configs can therefore receive different schedules, maximizing input reuse and reducing fragmentation. This yields +13% inference efficiency.

3. **Computation kernel specialization.** Loop tiling is per-layer (kernel size and memory dependent); inner-loop unrolling is specialized per kernel size (9 segments for 3×3, 25 for 5×5) to remove branch overhead; Conv+Padding+ReLU+BN is fused. Adds +22% efficiency.

4. **In-place depth-wise convolution.** Because depth-wise convolution does not mix channels, once a channel's output is computed its input activation can be overwritten by another channel's output. The first channel's output is held in a temporary buffer and written back to the last channel's input at the end, reducing depth-wise-conv activation memory from $2N$ to $N+1$ (1.6× measured reduction).

![[raw/papers/lin-2020-mcunet/figures/bf7d120d4841eef4308a138ee902305ab43ddb1ab1616db3c77fe313044dd370.jpg|Figure 7]]
*Figure 7: In-place depth-wise convolution overwrites each channel's input with another channel's output, reducing the depth-wise-conv memory footprint from 2N to N+1.*

> **Note**: This "in-place depth-wise convolution" (overwriting activations channel-by-channel) is distinct from [[concepts/inplace-convolution\|inplace convolution]] in the speech-enhancement literature, which denotes stride-1 frequency-axis convolution that avoids frequency downsampling.

The combined TinyEngine improvements (code generation, model-adaptive scheduling, kernel specialization, in-place depth-wise conv) reduce peak memory by 3.4× and accelerate inference by 1.7–3.3× vs. TF-Lite Micro and CMSIS-NN, enlarging the architecture search space TinyNAS can explore.

![[raw/papers/lin-2020-mcunet/figures/44b32b3ef071a347c640efa9d7aace4d392e756bdd559cd8da892f2681f81825.jpg|Figure 4a]]
![[raw/papers/lin-2020-mcunet/figures/368a2c8ca4064d2a07dc933ec029618889104d25cea63eefed5c22495fd3f8dc.jpg|Figure 4b]]
*Figure 4: (a) TinyEngine is 3× and 1.6× faster than TF-Lite Micro and CMSIS-NN, respectively; models exceeding the memory budget are marked OOM. (b) By reducing memory usage, TinyEngine runs model designs (w{}-r{}) that other libraries cannot fit, enlarging TinyNAS's design space.*

## Experimental Setup

| Aspect | Configuration |
|---|---|
| **Datasets** | ImageNet (1000-class); Visual Wake Words (VWW, person/not-person); Google Speech Commands V2 (35-word keyword spotting); Pascal VOC (object detection) |
| **MCU targets** | STM32F412 (Cortex-M4, 256 kB SRAM / 1 MB Flash); STM32F746 (M7, 320 kB / 1 MB); STM32F765 (M7, 512 kB / 1 MB); STM32H743 (M7, 512 kB / 2 MB). Default: STM32F746 @ 216 MHz |
| **Quantization** | int8 (default, post-training, negligible loss); 4-bit linear with 25-epoch quantization-aware fine-tuning (Table 4) |
| **Baselines** | Scaled MobileNetV2 (S-MbV2), scaled ProxylessNAS (S-Proxyless), ResNet-18, CMSIS-NN, TF-Lite Micro, MicroTVM, Rusci et al. (mixed 8/4/2-bit) |
| **NAS search split** | 10,000 ImageNet / 5,000 VWW training samples held out for search-time validation; Speech Commands uses its separate validation/test split |
| **Super-net training** | SGD momentum 0.9, weight decay 5e-5, cosine-annealing LR 0.05, batch 256; largest sub-net trained 150/100/30 epochs (ImageNet/VWW/Speech), super-net trained 2× those epochs |
| **Evolution search** | Population 100, 30 iterations, top-20 survive, 50 crossover + 50 mutated (p=0.1) per generation |

## Results

**System–algorithm co-design (STM32F746, 320 kB / 1 MB, ImageNet).** Each component lifts the achievable accuracy ceiling:

| Library \ Model | S-MbV2 | S-Proxyless | TinyNAS |
|---|---|---|---|
| CMSIS-NN | 35.2% | 49.5% | 55.5% |
| TinyEngine | 47.4% | 56.4% | **61.8%** |

MCUNet (TinyNAS + TinyEngine) reaches 61.8% vs. 35.2% for the strongest baseline pairing, evidence that the inference library affects *accuracy*, not just latency, by enlarging the runnable model space.

**Record ImageNet accuracy across MCUs (4-bit quantization).** MCUNet exceeds the prior SOTA (Rusci et al., mixed-precision) *without* mixed precision:

| | Quantization | STM32F412 (256k/1M) | STM32F746 (320k/1M) | STM32F765 (512k/1M) | STM32H743 (512k/2M) |
|---|---|---|---|---|---|
| Rusci et al. | Mixed 8/4/2-bit | 60.2% | — | 62.9% | 68.0% |
| **MCUNet** | 4-bit | 62.0% | 63.5% | 65.9% | **70.7%** |

The 70.7% on STM32H743 is the first reported >70% ImageNet top-1 on an off-the-shelf commercial MCU. At comparable accuracy (69.8%) to ResNet-18 / MobileNetV2-0.75 (8-bit), MCUNet uses **3.5× less SRAM and 5.7× less Flash**.

![[raw/papers/lin-2020-mcunet/figures/25f9d531b63a716624ad4907a6ecfda5944cc4d7472a2b37908bb856a9d07a95.jpg|Figure 8]]
*Figure 8: MCUNet reduces SRAM by 3.5× and Flash by 5.7× vs. MobileNetV2 and ResNet-18 (8-bit) while achieving higher accuracy (70.7% vs. 69.8% ImageNet top-1).*

**Visual & audio wake words.** On VWW and Google Speech Commands, MCUNet advances the accuracy–latency and accuracy–memory Pareto frontier:

![[raw/papers/lin-2020-mcunet/figures/9dcd540a1ef7533cebd52b781a58e9a772ae99a419af4dcd8d1606e70ffe7c99.jpg|Figure 9a]]
![[raw/papers/lin-2020-mcunet/figures/135f290f4f2afa894eefcd62b1194a7b36fcb4dec6ef577813b541dbfcd9e370.jpg|Figure 9b]]
![[raw/papers/lin-2020-mcunet/figures/87af960d67047cb1f39953009bcafb15cfd65bf2771b4c81c811201faa8b23fc.jpg|Figure 9c]]
![[raw/papers/lin-2020-mcunet/figures/949605ab6867ddae4976198fca68d0e8383f1ba926d9f89008f022d3636a9b88.jpg|Figure 9d]]
*Figure 9: Accuracy vs. latency and vs. peak SRAM on VWW (top) and Speech Commands (bottom). MCUNet achieves higher accuracy at 2.4–3.4× faster inference and 3.7–4.1× smaller peak SRAM.*

- **VWW**: 2.4–3.4× faster, 3.7× smaller peak SRAM; 2.4× faster than the prior first-place VWW challenge solution.
- **Speech Commands**: 2.8× faster, 4.1× smaller peak SRAM; +2% over the largest MobileNetV2 and +3.3% over the largest runnable ProxylessNAS under 256 kB SRAM. Reaches 10 FPS at 91% top-1.

**Object detection (Pascal VOC, STM32H743, YOLOv2 backbone).** Under a 512 kB SRAM / 2 MB Flash budget, MCUNet improves mAP by 20 percentage points (51.4% vs. 31.6%) over MbV2+CMSIS-NN, fitting a 168M-FLOP model at 466 kB peak SRAM where the baseline could only fit 34M FLOPs and went OOM.

**Search-space optimization ablation (ImageNet-100, 320 kB/1 MB).** The TinyNAS-selected space reaches 78.7% top-1, close to ResNet-18 @ 224 (OOM, 80.3%), vs. 77.0% for a "huge" space that *contains* the best space (super-large spaces harm super-net training/evolution) and 74.7% for random spaces. Mean-FLOPs of the search space correlates positively with final accuracy (Figure 10), validating the CDF-based selection criterion.

**Per-block peak-memory balance.** Scaled MobileNetV2 (0.3×) has a single block with 2.2× the average activation, forcing other blocks to shrink drastically; TinyNAS produces a more balanced per-block activation distribution, fitting higher overall capacity at the same SRAM budget — discovered automatically without memory-distribution heuristics.

**Sensitivity of search-space configuration.** Varying SRAM (192–512 kB) and Flash (512 kB–2 MB) reveals non-trivial patterns: increasing SRAM alone raises the chosen resolution; increasing Flash alone raises the chosen width while *lowering* resolution to fit the unchanged SRAM — a trade-off hard to find manually.

**Design cost.** TinyNAS search-space optimization (~2 CPU hours, no training) plus one-shot NAS (~300 GPU hours) cut design cost 133× vs. MnasNet (40,000 GPU hours), reducing per-model CO₂ emission from 11,345 lbs to 85 lbs.

![[raw/papers/lin-2020-mcunet/figures/779dd1d0f41d2693623806d510f52ae134dfae61afa7d985564c099c32de7a98.jpg|Figure 14]]
*Figure 14: MCUNet reduces total CO₂ emission for model design by orders of magnitude (11,345 lbs → 85 lbs), enabling affordable per-device specialization.*

## Key Contributions

1. **MCUNet system–algorithm co-design framework** — jointly optimizes the neural architecture (TinyNAS) and the inference engine (TinyEngine) in a single loop, so that each enlarges the other's effective search space; demonstrates that the inference library affects achievable *accuracy*, not just latency, on memory-starved MCUs.
2. **TinyNAS** — a two-stage NAS that first auto-optimizes the search space to fit tiny, diverse MCU constraints by analyzing the FLOPs CDF of satisfying networks (no training), then specializes the architecture via one-shot super-net + evolution search; handles 108 search-space configurations and diverse device/latency/memory constraints at 133× lower design cost than MnasNet.
3. **TinyEngine** — a memory-efficient inference engine using code generation (replacing interpretation), model-adaptive global memory scheduling, per-layer kernel specialization, and in-place depth-wise convolution; reduces peak memory 3.4× and accelerates inference 1.7–3.3× vs. TF-Lite Micro / CMSIS-NN.
4. **First >70% ImageNet accuracy on a commercial MCU** — 70.7% top-1 on STM32H743 with 4-bit quantization, using 3.5× less SRAM and 5.7× less Flash than int8 MobileNetV2/ResNet-18 at comparable accuracy, beating prior mixed-precision SOTA without mixed precision.
5. **State-of-the-art wake-word inference** — 2.4–3.4× faster and 3.7–4.1× smaller peak SRAM than MobileNetV2/ProxylessNAS baselines on VWW and Speech Commands, plus a 20-mAP improvement on Pascal VOC object detection under 512 kB SRAM, demonstrating task generality.

## Related Concepts

- [[concepts/tinyml\|TinyML]] — running deep learning on microcontroller-class devices; the problem domain MCUNet addresses
- [[concepts/tinynas\|TinyNAS]] — MCUNet's two-stage, resource-constrained neural architecture search
- [[concepts/tinyengine\|TinyEngine]] — MCUNet's memory-efficient, code-generation-based inference engine
- [[concepts/neural-architecture-search\|Neural Architecture Search]] — general NAS framework that TinyNAS extends with automated search-space optimization
- [[concepts/depthwise-separable-convolution\|Depthwise Separable Convolution]] — building block of the mobile search space TinyNAS scales
- [[concepts/post-training-quantization\|Post-Training Quantization]] — int8 deployment quantization used by default
- [[concepts/quantization-aware-training\|Quantization-Aware Training]] — used for the 4-bit ImageNet results
- [[concepts/object-detection\|Object Detection]] — generalization task (Pascal VOC + YOLOv2)
- [[concepts/keyword-spotting\|Keyword Spotting]] — Speech Commands application
- [[concepts/inplace-convolution\|Inplace Convolution]] — distinct SE concept sharing a name with in-place depth-wise convolution

## Related Synthesis

_(No existing synthesis page covers TinyML or efficient on-device inference; the wiki's synthesis pages focus on acoustic/speech tasks. None are updated by this ingest.)_
