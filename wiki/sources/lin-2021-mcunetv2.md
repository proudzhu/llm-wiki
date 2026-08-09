---
type: source
created: 2026-08-09
updated: 2026-08-09
sources:
  - raw/papers/lin-2021-mcunetv2/full-text.md
  - https://doi.org/10.48550/arXiv.2110.15352
  - zotero://select/items/0_W65ANM64
tags:
  - tinyml
  - neural-architecture-search
  - efficient-deep-learning
  - microcontroller
  - inference-engine
  - memory-optimization
  - patch-based-inference
---

# Lin, Chen, Cai, Gan & Han 2021: MCUNetV2 — Memory-Efficient Patch-based Inference for Tiny Deep Learning

| | |
|---|---|
| **Authors** | [[entities/ji-lin\|Ji Lin]], [[entities/wei-ming-chen\|Wei-Ming Chen]], [[entities/han-cai\|Han Cai]], [[entities/chuang-gan\|Chuang Gan]], [[entities/song-han\|Song Han]] |
| **Institutions** | MIT; MIT-IBM Watson AI Lab |
| **Venue** | arXiv preprint (v1: 2021-10-28; v2: camera-ready, project/demo links updated) |
| **Type** | Preprint (arXiv) |
| **DOI** | [10.48550/arXiv.2110.15352](https://doi.org/10.48550/arXiv.2110.15352) |
| **arXiv** | [2110.15352](http://arxiv.org/abs/2110.15352) |
| **Zotero** | [W65ANM64](zotero://select/items/0_W65ANM64) |
| **Project** | https://tinyml.mit.edu/ |

## Summary

MCUNetV2 is the successor to [[sources/lin-2020-mcunet\|MCUNet (Lin et al. 2020)]] that targets a previously unaddressed bottleneck of [[concepts/tinyml\|TinyML]]: the *imbalanced memory distribution* of CNNs, where the first few blocks consume an order of magnitude more SRAM than the rest of the network. It introduces three contributions — (1) [[concepts/patch-based-inference\|patch-based inference]] that runs the memory-intensive initial stage patch-by-patch instead of layer-by-layer, (2) [[concepts/receptive-field-redistribution\|receptive field redistribution]] that shifts receptive field to the later stage to minimize overlapping-patch computation overhead, and (3) joint NAS + inference-scheduling search that automates the architecture/schedule co-design. MCUNetV2 cuts peak SRAM of existing networks by 4–8×, sets a record 71.8% ImageNet top-1 on MCU, achieves >90% Visual Wake Words accuracy under 32 kB SRAM, and unlocks object detection on MCUs with +16.9% mAP on Pascal VOC over the prior SOTA.

## Problem Formulation

While [[sources/lin-2020-mcunet\|MCUNet V1]] reduced model size and peak activation via NAS + an efficient inference engine, it still used *per-layer* execution: each convolutional layer allocates the full input and output activation buffer in SRAM, releases the input only after the whole layer finishes. MCUNetV2 identifies that this per-layer model exposes a structural memory bottleneck that prior work (pruning, quantization, NAS) does not address.

### Imbalanced Memory Distribution

Profiling MobileNetV2 (int8, 224×224 input) reveals that the **first 5 blocks** have peak memory >450 kB (exceeding typical MCU budgets), while the remaining 13 blocks easily fit 256 kB. The peak memory of the initial memory-intensive stage is **8× higher** than the rest of the network. This pattern is generic across efficient CNN backbones (MnasNet, FBNet, even MCUNet-320kB), as shown in Figure 11 of the paper.

The root cause is the **hierarchical structure** of single-branch / residual CNNs: after each stage the spatial resolution is down-sampled by 2× (4× fewer pixels), while the channel count typically increases only 2× (or less), so activation size decreases through the network. Consequently the memory bottleneck is concentrated at the early stage.

Concretely, the first convolution of MobileNetV2 (3→32 channels, stride 2) on a 224×224 image requires

$$3 \times 224^{2} + 32 \times 112^{2} = 539\ \text{kB}\quad(\text{int8}),$$

which already exceeds a typical MCU's SRAM. Yet if one could "bypass" the initial memory-intensive stage, the rest of the network would fit comfortably — leaving a large optimization headroom.

### Goal

Find a network architecture $\mathcal{A}^*$ and an *inference schedule* $\mathcal{S}^*$ that jointly maximize accuracy subject to peak-SRAM and Flash constraints, where the schedule is no longer constrained to per-layer execution.

## Methodology

### Patch-based Inference

[[concepts/patch-based-inference\|Patch-based inference]] (Section 3.1) breaks the memory bottleneck of the initial layers. Instead of computing the whole feature map for each layer, the initial memory-intensive stage is executed **patch-by-patch**: a buffer is allocated for the *final* output of the stage, and its values are computed one small spatial patch at a time. Only the activation of *one patch* needs to be stored, rather than the entire feature map. The first input (the image) can be partially decoded from a compressed format like JPEG, so it does not require full storage either. The rest of the network (with small per-block memory) continues to use normal layer-by-layer execution.

The trade-off is **computation overhead**: to produce the same non-overlapping output patches, the input image patches must *overlap* (because convolutional filters with kernel size >1 grow the receptive field), causing repeated computation along patch borders. For MobileNetV2 with 4×4 patches, the overhead is 10% overall (42% for the patch-stage alone).

### Receptive Field Redistribution

[[concepts/receptive-field-redistribution\|Receptive field redistribution]] (Section 3.2) reduces the computation overhead. The overhead is positively related to the receptive field (RF) of the patch-based stage: a larger RF means a larger input patch is needed, hence more overlapping. The remedy is to *(1) reduce the RF of the initial patch-based stage* (smaller kernels, fewer blocks) and *(2) increase the RF of the later per-layer stage* to compensate for the performance loss (important for tasks like detecting large objects).

Applied manually to MobileNetV2 ("MbV2-RD"), this shrinks the input patch side from 75 to 63, cuts the patch-stage overhead from 42% to 18% and the overall overhead from 10% to **3%**, while preserving ImageNet top-1 (72.1% vs. 72.2%) and improving Pascal VOC mAP (75.7% vs. 75.4%). The peak SRAM remains 172 kB (8× reduction). However, manual redistribution is case-by-case; the next step automates it.

### Joint Neural Architecture and Inference Scheduling Search

MCUNetV2 jointly optimizes the backbone and the inference schedule in a single NAS loop (Section 3.3), extending [[concepts/tinynas\|TinyNAS]] with new search knobs:

| Knob | Symbol | Choices | Note |
|---|---|---|---|
| Kernel size per block | $k_{[\,]}$ | {3, 5, 7} | MnasNet-alike space |
| Expansion ratio per block | $e_{[\,]}$ | {3, 4, 6} | |
| Stage depth | $d_{[\,]}$ | {2, 3, 4} | |
| **Per-block width multiplier** | $w_{[\,]}$ | {0.5, 0.75, 1.0} | **New** — extends V1's global $w$ to per-block, merges V1's two-stage search-space optimization into one stage |
| **Input resolution** | $r$ | {96, 128, 160, 192, 224, 256} | **New** — added directly to the search space (V1 optimized it separately) |
| **# patches** | $p$ | {1, 2, 3, 4} | **New** — image split into $p \times p$ overlapping patches |
| **# patch-based layers** | $n$ | $<N$ (total layers) | **New** — rest of network runs per-layer |

Including $r$ and $w_{[\,]}$ in the search space (rather than as a separate pre-NAS optimization stage as in V1) allows the same super network to span tight resource budgets. MobileNetV3-style search spaces are avoided because Swish activation is hard to quantize for MCU deployment.

[[concepts/tinyengine\|TinyEngine]] is extended to support patch-based inference (allocating the patch buffer and orchestrating the patch-by-patch loop). Models are quantized to int8 (with 10-epoch quantization-aware training following the format of Jacob et al. 2018).

## Experimental Setup

| Aspect | Configuration |
|---|---|
| **Datasets** | ImageNet (1000-class classification); Visual Wake Words (VWW, person/not-person); Pascal VOC (object detection, YOLOv3 backbone); WIDER FACE (face detection, S3FD backbone) |
| **MCU targets** | STM32F412 (Cortex-M4, 256 kB SRAM / 1 MB Flash); STM32F746 (M7, 320 kB / 1 MB); STM32H743 (M7, 512 kB / 2 MB) |
| **Quantization** | int8 (10-epoch quantization-aware training, Jacob et al. 2018 format) |
| **Baselines (existing networks)** | MobileNetV2 (MbV2), redistributed MobileNetV2 (MbV2-RD), OFA-CPU, MnasNet, FBNet-A; per-layer vs. per-patch execution |
| **Baselines (SOTA tinyML)** | MCUNet V1 (TinyNAS / TinyEngine), Rusci et al. (mixed-precision), ProxylessNAS, scaled MobileNetV1/V2, RNNPool-Face, LFFD, EXTD, EagleEye |
| **Super-net training** | SGD batch 1024, LR 0.2, weight decay 4e-5, cosine decay, 150 epochs (ImageNet) / 30 (VWW); channels sorted by L1-norm importance for super-net init; 4 architectures sampled per iteration |
| **Evolution search** | Population 100, 30 iterations, top-20 survive, 50 crossover + 50 mutated (rate 0.1) per generation |
| **Sub-network fine-tuning** | 1/10 of initial LR for 10 epochs |
| **Search validation split** | 10,000 ImageNet / 5,000 VWW samples held out (BN re-calibration: 20 batches × 64) |

## Results

### Reducing Peak Memory of Existing Networks (Section 4.1)

Patch-based inference is first applied *off-the-shelf* to existing backbones (no co-design), at 224×224 input and 4×4 patches, profiled in int8:

| Network | Memory reduction | Computation overhead |
|---|---|---|
| MobileNetV2 | 8.0× | +10% |
| MbV2-RD | 8.0× | **+3%** (after RF redistribution) |
| OFA-CPU | 3.7–8.0× | +8–17% |
| MnasNet | ~5× | larger overhead (large initial kernels) |
| FBNet-A | ~5× | +8–17% |

On-device measurement on STM32F746 (with width/resolution scaled to fit 320 kB / 1 MB) confirms **4–6× peak SRAM reduction**, with MbV2-RD achieving only **4% latency overhead**.

### ImageNet Classification on MCUs (Section 4.2, Table 2)

| MCU | Method | Quant. | MACs | SRAM | Flash | Top-1 | Top-5 |
|---|---|---|---|---|---|---|---|
| STM32F412 (256k/1M) | MCUNet V1 | int8 | 68M | 238 kB | 1007 kB | 60.3% | — |
| STM32F412 (256k/1M) | MCUNet V1 | int4 | 134M | 233 kB | 1008 kB | 62.0% | — |
| STM32F412 (256k/1M) | **MCUNetV2-M4** | int8 | 119M | 196 kB | 1010 kB | **64.9%** | 86.2% |
| STM32H743 (512k/2M) | MCUNet V1 | int8 | 126M | 452 kB | 2014 kB | 68.5% | — |
| STM32H743 (512k/2M) | MCUNet V1 | int4 | 474M | 498 kB | 2000 kB | 70.7% | — |
| STM32H743 (512k/2M) | **MCUNetV2-H7** | int8 | 256M | 465 kB | 2032 kB | **71.8%** | 90.7% |

MCUNetV2-M4 outperforms V1 (int8) by **+4.6%** at 18% lower peak SRAM. MCUNetV2-H7 sets a new **record ImageNet accuracy of 71.8%** on a commercial MCU — **+3.3%** over V1 under the same int8 quantization policy (V1's 70.7% required int4).

### Visual Wake Words under 32 kB SRAM (Section 4.2)

MCUNetV2 achieves **>90% accuracy under 32 kB SRAM**, a **4.0× reduction** in peak memory vs. MCUNet V1, enabling deployment on a $1.6 STM32F410-class MCU. Per-patch inference also expands the search space, improving the accuracy-vs-latency Pareto frontier.

### Object Detection on Pascal VOC (Section 4.3, Table 3)

| MCU | Constraint | Model | #Param | MACs | Peak SRAM | VOC mAP | Gain |
|---|---|---|---|---|---|---|---|
| H743 (~$7) | SRAM <512 kB | MbV2+CMSIS | 0.87M | 34M | 519 kB | 31.6% | — |
| H743 | SRAM <512 kB | MCUNet V1 | 1.20M | 168M | 466 kB | 51.4% | 0% |
| H743 | SRAM <512 kB | **MCUNetV2-H7** | 0.67M | 343M | 438 kB | **68.3%** | **+16.9%** |
| F412 (~$4) | <256 kB | **MCUNetV2-M4** | 0.47M | 172M | 247 kB | **64.6%** | **+13.2%** |

Object detection — previously impractical on MCUs due to the resolution bottleneck (Figure 2: detection accuracy degrades far faster than classification as input resolution drops) — is made practical. MCUNetV2-M4 attains similar MACs to V1 (172M vs. 168M) but +13.2% higher mAP at 1.9× smaller peak SRAM, because patch-based inference allows a larger input resolution.

### Memory-efficient Face Detection (Section 4.3, Table 4, WIDER FACE)

| Method | MACs | Peak Mem (fp32) | Easy | Med | Hard |
|---|---|---|---|---|---|
| LFFD | 9.25G | 18.8 MB (9.9×) | 0.91 | 0.88 | 0.77 |
| RNNPool-Face-C | 1.80G | 6.44 MB (3.4×) | 0.92 | 0.89 | 0.70 |
| **MCUNetV2-L** | **1.10G** | **1.89 MB (1.0×)** | 0.92 | 0.90 | 0.70 |

MCUNetV2-L matches RNNPool-Face-C accuracy at **3.4× smaller peak memory and 1.6× smaller computation**, and beats LFFD by 9.9× in memory. MCUNetV2-S outperforms RNNPool-Face-A and EagleEye at 1.8× smaller memory.

### Ablation and Analysis (Section 4.4)

- **Hyper-parameters** ($n$ patch-stage blocks, $p$ patch count): for MobileNetV2, $n^{*}=5$ (where feature map is down-sampled 8×) and $p^{*}=4$ minimize peak memory with smallest overhead. Larger $p$ shrinks each patch but increases overlapping; RF redistribution significantly reduces overhead (MbV2-RD).
- **Comparison to other memory-saving methods** (Table 5): non-overlapping patches break translational invariance and degrade detection mAP (73.9% vs. 75.4%); RNNPool reduces memory but lowers accuracy and triples training time. MbV2-RD (MCUNetV2) matches per-layer accuracy (72.1% ImageNet, 75.7% VOC) at the same 0.19 MB peak memory and 1.0× training cost — and acts identically to a normal network during training.
- **Discovered architecture patterns** (Figure 9): NAS automatically chooses small kernels (1×1, 3×3) in the patch stage; small expansion ratios in the early per-layer stage; avoids combining large expansion with large kernels; uses larger input resolution on resolution-sensitive datasets like VWW.
- **NAS search-space ablation** (Table 6, Appendix D): merging $r$ and $w$ into the search space beats V1's two-stage approach and prior NAS+scale methods (TinyNet, EfficientNet, MobileNetV3) at 25/50/100M MACs budgets, with the gain largest at tiny budgets (≤25M).

## Key Contributions

1. **Imbalanced memory distribution analysis** — systematically profiles efficient CNN backbones and identifies that the first few blocks consume an order of magnitude more SRAM than the rest (root cause: hierarchical structure with 2× resolution downsampling vs. 2× channel growth), exposing a large optimization headroom ignored by pruning/quantization/NAS.
2. **Patch-based inference scheduling** — runs the initial memory-intensive stage patch-by-patch, storing only one patch's activation rather than the whole feature map, reducing peak SRAM of existing networks by **4–8×** (analytic) and **4–6×** (on-device) at 8–17% computation overhead.
3. **Receptive field redistribution** — shifts RF from the patch-based initial stage to the per-layer later stage, cutting MobileNetV2's computation overhead from 10% to **3%** without hurting accuracy; jointly searched with the architecture to remove case-by-case manual tuning.
4. **Joint architecture + inference-scheduling NAS** — extends TinyNAS with per-block width multiplier $w_{[\,]}$, input resolution $r$, patch count $p$, and patch-stage depth $n$ as search knobs, merging V1's two-stage search-space optimization into one stage.
5. **Record tiny-ML results across tasks** — 71.8% ImageNet top-1 on STM32H743 (int8, +3.3% over V1's int8); >90% VWW accuracy under 32 kB SRAM (4× smaller than V1); 68.3% Pascal VOC mAP on H743 (+16.9% over V1) and 64.6% on F412 (+13.2%), unlocking object detection on MCUs; 3.4× smaller peak memory than RNNPool-Face-C at matching face-detection accuracy.

## Related Concepts

- [[concepts/patch-based-inference\|Patch-based Inference]] — MCUNetV2's core execution-order innovation
- [[concepts/receptive-field-redistribution\|Receptive Field Redistribution]] — companion technique minimizing the overlapping-patch computation overhead
- [[concepts/imbalanced-memory-distribution\|Imbalanced Memory Distribution]] — the structural CNN memory pattern MCUNetV2 identifies and exploits
- [[concepts/tinyml\|TinyML]] — problem domain
- [[concepts/tinynas\|TinyNAS]] — extended with inference-scheduling knobs
- [[concepts/tinyengine\|TinyEngine]] — extended to support patch-based inference
- [[concepts/neural-architecture-search\|Neural Architecture Search]] — general framework
- [[concepts/depthwise-separable-convolution\|Depthwise Separable Convolution]] — building block of the mobile search space

## Related Synthesis

_(No existing synthesis page covers TinyML, patch-based inference, or efficient on-device vision; the wiki's synthesis pages focus on acoustic/speech tasks. The only tag-overlap candidate (`computational-efficiency-evolution.md`, shared `memory-optimization`/`model-compression`) is an ANC/SE efficiency synthesis — MCUNetV2 is a vision/TinyML paper, so a cross-source addition would be thin and off-topic. None are updated by this ingest.)_
