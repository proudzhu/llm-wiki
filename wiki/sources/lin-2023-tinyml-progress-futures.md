---
type: source
created: 2026-08-09
updated: 2026-08-09
sources:
  - raw/papers/lin-2023-tinyml-progress-futures/full-text.md
  - https://doi.org/10.1109/MCAS.2023.3302182
  - https://arxiv.org/abs/2403.19076
  - zotero://select/items/0_8P6FBNQD
tags:
  - tinyml
  - survey
  - review
  - deep-learning
  - efficient-deep-learning
  - microcontroller
  - edge-ai
  - on-device-training
  - neural-architecture-search
  - inference-engine
  - quantization
  - mit
---

# Lin, Zhu, Chen, Wang & Han 2023: Tiny Machine Learning — Progress and Futures

- **Authors**: [[entities/ji-lin\|Ji Lin]], [[entities/ligeng-zhu\|Ligeng Zhu]], [[entities/wei-ming-chen\|Wei-Ming Chen]], [[entities/wei-chen-wang\|Wei-Chen Wang]], [[entities/song-han\|Song Han]]
- **Institution**: Massachusetts Institute of Technology (MIT HAN Lab)
- **Venue**: IEEE Circuits and Systems Magazine, 2023
- **Type**: Review / survey article
- **DOI**: [10.1109/MCAS.2023.3302182](https://doi.org/10.1109/MCAS.2023.3302182)
- **arXiv**: [2403.19076](https://arxiv.org/abs/2403.19076)
- **Zotero**: [8P6FBNQD](zotero://select/items/0_8P6FBNQD)
- **Source**: `raw/papers/lin-2023-tinyml-progress-futures/full-text.md`

## Summary

This review surveys the [[concepts/tinyml\|TinyML]] field — running deep-learning inference *and* training on microcontrollers (MCUs) with hundreds of kilobytes of SRAM — covering the definition, challenges, recent literature, and the authors' own MCUNet family of system–algorithm co-designed solutions. Beyond inference, it extends the frontier to **on-device training** on MCUs (the MCUNetV3 contribution: Quantization-Aware Scaling + sparse update + Tiny Training Engine), and identifies four future directions: more modalities/applications, self-supervised learning, the TinyML↔LargeML relationship, and the evolving definition of "tiny".

## Taxonomy

The review organizes TinyML along three orthogonal axes:

### Axis 1 — CloudML vs EdgeML vs TinyML

![[raw/papers/lin-2023-tinyml-progress-futures/figures/fig1.jpg|Figure 1]]

*Figure 1: Efficiency frontier across CloudML (GPUs), EdgeML (mobile), and TinyML (MCUs). TinyML pushes efficiency by 3–6 orders of magnitude in memory.*

### Axis 2 — Inference vs Training

- **Inference** — running a frozen model; the binding constraint is *peak SRAM activation* + *Flash parameter size*.
- **Training** — backpropagation plus optimizer state; the binding constraint is *intermediate activations stored for the backward pass*, which is ~6.9× larger than inference memory for the same model.

### Axis 3 — Algorithm vs System

- **Algorithm solutions** — pruning, [[concepts/post-training-quantization\|quantization]], tensor decomposition, knowledge distillation, manually-designed tiny networks, [[concepts/neural-architecture-search\|NAS]].
- **System solutions** — inference libraries (CMSIS-NN, X-Cube-AI, microTVM, TF-Lite Micro, TinyEngine), operator reordering, spatial partial computation, mixed-precision kernels.

The review's central thesis is **co-design**: algorithm and system must be jointly optimized because the inference library directly affects the achievable accuracy ceiling, and the model architecture directly affects which system optimizations apply.

## Methodology

### Surveyed Inference Methods (Section II-A)

The review catalogues inference-side TinyML literature along algorithm and system axes:

- **Algorithm-side inference**: rule-based mixed-precision quantization (Rusci et al. MLSys'20); TinyNAS two-stage search-space optimization (within [[sources/lin-2020-mcunet\|MCUNet]]); MicroNets differentiated NAS (latency ≈ FLOPs proxy); [[concepts/imbalanced-memory-distribution\|imbalanced memory distribution]] identification + [[concepts/receptive-field-redistribution\|receptive field redistribution]] ([[sources/lin-2021-mcunetv2\|MCUNetV2]]); UDC compressible-NAS for NPUs (NeurIPS'22).
- **System-side inference**: CMSIS-NN optimized Cortex-M kernels; X-Cube-AI (STMicroelectronics); microTVM; operator reordering for peak-memory reduction (Liberis et al., Ahn et al.); SRAM paging (Miao et al.); spatial partial computation; CMix-NN mixed-precision kernels; [[concepts/tinyengine\|TinyEngine]] code-generation + memory scheduling; TF-Lite Micro bare-metal interpreter; [[concepts/patch-based-inference\|patch-based inference]] (MCUNetV2); TinyOps external-memory DMA; TinyMaix minimal kernel library.

### Surveyed Training Methods (Section II-B)

On-device training is harder than inference because the activations stored for backpropagation dominate memory. Surveyed approaches:

- Lightweight network design / NAS for training (same architecture-level savings).
- Recompute-on-backward (trade compute for memory) — too slow for MCUs.
- Layer-wise training — accuracy ceiling too low.
- Activation-pruning dynamic sparse training graphs.
- Quantization-aware training (reduce activation bitwidth).
- Transfer learning: freeze backbone, fine-tune last layer only — cheap but accuracy-limited under domain shift.
- **TinyTL** — freeze weights, fine-tune biases only; discards intermediate activations during backward ([Cai et al. NeurIPS'20]).
- **TinyOL** — train only the final layer weights, supporting online incremental streaming (IJCNN'21).
- **POET** — rematerialization + paging; integer-linear-program energy-optimal schedule (ICML'22).
- **MiniLearn** — int-precision weight storage with dequantize-on-training (EWSN'22).
- **MCUNetV3** — Quantization-Aware Scaling (QAS) + sparse update + Tiny Training Engine (TTE) co-design (NeurIPS'22; surveyed here as the review's own contribution).

### The MCUNet Family (Sections III–IV)

The review then presents the authors' own line of work as a coherent narrative:

- **MCUNet (V1)** = [[concepts/tinynas\|TinyNAS]] (two-stage NAS) + [[concepts/tinyengine\|TinyEngine]] (code-gen inference library) — see [[sources/lin-2020-mcunet\|Lin et al. 2020]].
- **MCUNetV2** = patch-based inference + receptive field redistribution + joint architecture-and-scheduling NAS — see [[sources/lin-2021-mcunetv2\|Lin et al. 2021]].
- **MCUNetV3** = Quantization-Aware Scaling + sparse layer/tensor update + Tiny Training Engine — the **tiny training** contribution first surveyed at length in this review.

## Applications Survey

### Hardware Constraints

![[raw/papers/lin-2023-tinyml-progress-futures/figures/hardware_stats.jpg|Table I]]

*Table I: Microcontrollers have 3–6 orders of magnitude less memory/storage than mobile/cloud hardware. ResNet-50 exceeds MCU limits by 100×, MobileNetV2 by 20×, and even int8 MobileNetV2 by 5.3× — MobileNet designs reduce *parameters* but not *activations*, which is the actual MCU bottleneck.*

![[raw/papers/lin-2023-tinyml-progress-futures/figures/fig2.jpg|Figure 2]]

*Figure 2: At equal ImageNet accuracy, MobileNetV2-1.4 has 4.2× smaller parameters than ResNet-50 yet 2.3× larger peak inference memory; training memory is 6.9× inference memory and MobileNet barely helps (1.1× only).*

### Cross-Paper Performance Comparison (Table II)

The review consolidates latency, peak memory, Flash usage, energy, and accuracy across 18 TinyML works on STM32-class MCUs, spanning both inference-only and training-capable systems. Selected rows illustrating the inference→training frontier:

| Method | Year | Type | Device | Dataset | Latency | Peak Mem | Top-1 |
|---|---|---|---|---|---|---|---|
| CMSIS-NN | 2018 | Inference | STM32H743 | ImageNet | 510 ms | < 1 MB | 59.5% |
| MicroNets | 2021 | Inference | STM32F746 | VWW | 1133 ms | 285 KB | 88.0% |
| MCUNetV1 | 2020 | Inference | STM32H743 | ImageNet | 463 ms | 416 KB | 68.0% |
| MCUNetV2 | 2021 | Inference | STM32H743 | ImageNet | 859 ms | 434 KB | 71.8% |
| TinyMaix | 2022 | Inference | STM32H750 | VWW | 64 ms | 54 KB | ~76% |
| POET | 2022 | Training | nRF52840 | CIFAR-10 | 49 ms | 271 KB | 95.5% |
| MiniLearn | 2022 | Training | nRF52840 | KWS-subset | 93 ms | 196 KB | 88.5% |
| **MCUNetV3** | 2022 | Training | STM32F746 | VWW | 546 ms | **173 KB** | 89.3% |

### Same-Hardware Framework Comparison (Table III)

A controlled head-to-head on STM32H743 (480 MHz, 512 kB SRAM, 2 MB Flash) across four frameworks — CMSIS-NN, X-Cube-AI, TinyEngine, TF-Lite Micro — running identical MCUNet/Proxyless/MobileNetV2 models. TinyEngine consistently achieves the lowest peak memory and latency; TF-Lite Micro is 20–25× slower and runs out-of-memory on the largest config. CMSIS-NN also runs out-of-memory at the largest ImageNet config (mcunet-in4), while TinyEngine completes it in 463 ms / 416 KB.

### MCUNet MCU Inference Records (Tables IV–VI)

![[raw/papers/lin-2023-tinyml-progress-futures/figures/fig4.jpg|Figure 4]]

*Figure 4: MCUNet jointly designs TinyNAS (architecture) and TinyEngine (scheduling) in the same loop.*

| Hardware | Model | Quant | MACs | SRAM | Flash | Top-1 |
|---|---|---|---|---|---|---|
| STM32F412 (256 kB / 1 MB) | MCUNet-M4 (w/ patch) | int8 | 119M | 196 kB | 1010 kB | **64.9%** |
| STM32H743 (512 kB / 2 MB) | MCUNet-H7 (w/ patch) | int8 | 256M | 465 kB | 2032 kB | **71.8%** |

Object detection on Pascal VOC (YOLOv3 backbone):

| MCU | Model | MACs | Peak SRAM | VOC mAP | Gain |
|---|---|---|---|---|---|
| H743 (~$7) | MbV2+CMSIS | 34M | 519 kB | 31.6% | — |
| H743 | MCUNet (V1) | 168M | 466 kB | 51.4% | 0% |
| H743 | MCUNet-H7 (V2) | 343M | 438 kB | **68.3%** | **+16.9%** |
| F412 (~$4) | MCUNet-M4 (V2) | 172M | 247 kB | 64.6% | +13.2% |

Memory-efficient face detection on WIDER FACE: MCUNet-L matches RNNPool-Face-C mAP at 3.4× smaller peak SRAM and 1.6× smaller compute; MCUNet-S matches RNNPool-Face-A at 1.8× smaller peak memory.

### Visual Wake Words Under 32 kB SRAM

![[raw/papers/lin-2023-tinyml-progress-futures/figures/fig14.jpg|Figure 14]]

*Figure 14: MCUNet achieves >90% VWW accuracy under <32 kB SRAM (4× smaller than V1), enabling deployment on $1.6 STM32F410-class MCUs.*

### MCUNetV3 Tiny Training

![[raw/papers/lin-2023-tinyml-progress-futures/figures/fig15.jpg|Figure 15]]

*Figure 15: Algorithm + system co-design reduces training memory from 303 MB (PyTorch) to 149 KB (MCUNetV3) for the same transfer-learning accuracy — a 2077× reduction that fits a 256 kB MCU.*

![[raw/papers/lin-2023-tinyml-progress-futures/figures/fig19.jpg|Figure 19]]

*Figure 19: Tiny Training Engine (TTE) workflow — compile-time auto-differentiation, backward-graph pruning for sparse update, operator reordering, and code generation for bare-metal deployment.*

![[raw/papers/lin-2023-tinyml-progress-futures/figures/fig21.jpg|Figure 21]]

*Figure 21: Sparse update + TTE graph optimization cuts measured peak training memory by 20–21× and accelerates training by 23–25× vs. full-update + TF-Lite Micro, making on-device training practical on 256 kB SRAM.*

## Key Contributions

1. **Three-axis taxonomy of TinyML** — CloudML/EdgeML/TinyML × inference/training × algorithm/system, framing why co-design is necessary (mobile/cloud models reduce parameters but not activations, and training is 6.9× inference memory).
2. **Literature consolidation** — Tables II and III provide the first side-by-side comparison of 18 TinyML works on identical hardware, and a controlled four-framework head-to-head (CMSIS-NN / X-Cube-AI / TinyEngine / TF-Lite Micro) on identical models, exposing framework-level efficiency differences that prior single-paper benchmarks obscured.
3. **Unified MCUNet-family narrative** — integrates V1 (TinyNAS + TinyEngine), V2 (patch-based inference + RF redistribution), and V3 (QAS + sparse update + TTE) into a single system–algorithm co-design arc spanning inference and training.
4. **MCUNetV3 on-device training** — first system to enable real quantized-graph training on a 256 kB MCU, achieving 89.3% VWW transfer-learning accuracy at 173 kB peak memory; reduces training memory 2077× (303 MB → 149 KB) vs. PyTorch at equal accuracy.
5. **Forward-looking directions** — explicitly identifies self-supervised on-device learning, the TinyML↔LargeML technique transfer (quantization and sparse learning apply to both), and the evolving "tiny" threshold as future research axes.

## Limitations and Caveats

- **CNN-and-vision focus** — the review and the MCUNet family primarily target convolutional networks for vision (classification, detection, VWW). Audio, language, time-series, and multi-sensor TinyML are surveyed as future directions rather than deeply treated.
- **Self-citation heavy** — Sections III–IV are dominated by the authors' own MCUNet V1/V2/V3 papers; readers seeking a neutral cross-group comparison should weight Table II's third-party rows accordingly.
- **V3 results not yet separately ingested** — this review is the wiki's first source for MCUNetV3's QAS, sparse update, and TTE. The original NeurIPS 2022 MCUNetV3 paper is not yet in the wiki; ingesting it would add per-experiment detail beyond what the review surveys.
- **Literature cutoff ~late 2022** — post-2022 TinyML advances (e.g., transformer-on-MCU, newer mixed-precision training schemes) are out of scope.
- **MCUNetV3 energy unreported** — Table II leaves MCUNetV3's energy consumption as "—", so direct energy-per-update comparison with POET/MiniLearn is not possible from this review alone.

## Related Concepts

- [[concepts/tinyml\|TinyML]] — the surveyed field
- [[concepts/tinynas\|TinyNAS]] — MCUNet V1's NAS component
- [[concepts/tinyengine\|TinyEngine]] — MCUNet V1/V2's inference engine
- [[concepts/patch-based-inference\|Patch-based Inference]] — MCUNetV2's memory-saving scheduling
- [[concepts/receptive-field-redistribution\|Receptive Field Redistribution]] — MCUNetV2's overhead-reduction technique
- [[concepts/imbalanced-memory-distribution\|Imbalanced Memory Distribution]] — the structural CNN pattern MCUNetV2 exploits
- [[concepts/quantization-aware-scaling\|Quantization-Aware Scaling (QAS)]] — MCUNetV3's gradient-calibration technique
- [[concepts/sparse-update\|Sparse Update]] — MCUNetV3's layer/tensor sparse backpropagation
- [[concepts/tiny-training-engine\|Tiny Training Engine (TTE)]] — MCUNetV3's compile-time training system
- [[concepts/neural-architecture-search\|Neural Architecture Search]]
- [[concepts/post-training-quantization\|Post-Training Quantization]]
- [[concepts/quantization-aware-training\|Quantization-Aware Training]]
- [[concepts/depthwise-separable-convolution\|Depthwise Separable Convolution]]

## Related Sources

- [[sources/lin-2020-mcunet\|Lin et al. 2020: MCUNet — Tiny Deep Learning on IoT Devices]] — V1 (inference)
- [[sources/lin-2021-mcunetv2\|Lin et al. 2021: MCUNetV2 — Memory-Efficient Patch-based Inference for Tiny Deep Learning]] — V2 (inference)

## Related Synthesis

(none yet — no existing synthesis page overlaps with TinyML; the wiki's synthesis pages currently focus on acoustics, speech enhancement, and LLM tooling.)
