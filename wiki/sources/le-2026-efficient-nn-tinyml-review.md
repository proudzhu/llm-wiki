---
type: source
created: 2026-08-11
updated: 2026-08-11
sources:
  - raw/papers/le-2026-efficient-nn-tinyml-review/full-text.md
  - https://doi.org/10.1145/3798276
  - https://arxiv.org/abs/2311.11883
  - zotero://select/items/0_QDFZSG5A
tags:
  - tinyml
  - survey
  - review
  - deep-learning
  - efficient-deep-learning
  - microcontroller
  - edge-ai
  - model-compression
  - pruning
  - quantization
  - knowledge-distillation
  - weight-sharing
  - low-rank-decomposition
  - bayesian-compression
  - tinymlops
  - arm-cortex-m
  - risc-v
  - fixed-point
  - mems
---

# Lê, Wolinski & Arbel 2026: Efficient Neural Networks for Tiny Machine Learning — A Comprehensive Review

- **Authors**: [[entities/minh-tri-le|Minh Tri Lê]], [[entities/pierre-wolinski|Pierre Wolinski]], [[entities/julyan-arbel|Julyan Arbel]]
- **Institutions**: Université Grenoble Alpes, Inria, CNRS, Grenoble INP, LJK (Grenoble, France); LAMSADE, Paris-Dauphine University, PSL University, CNRS (Paris, France)
- **Venue**: ACM Transactions on Intelligent Systems and Technology (TIST), Vol. 17, No. 4, Article 86 (April 2026), 41 pages
- **Type**: Review / survey article
- **DOI**: [10.1145/3798276](https://doi.org/10.1145/3798276)
- **arXiv**: [2311.11883](https://arxiv.org/abs/2311.11883)
- **Zotero**: [QDFZSG5A](zotero://select/items/0_QDFZSG5A)
- **Source**: `raw/papers/le-2026-efficient-nn-tinyml-review/full-text.md`

## Summary

This review provides an end-to-end treatment of [[concepts/tinyml|TinyML]] — running deep-learning inference on ultra-low-power microcontrollers (MCUs) with as little as 8 kB SRAM and 10 MHz clock — unifying four perspectives that prior surveys covered only in isolation: (1) NN fundamentals and why TinyML falls outside the regime where standard DL theory guarantees good generalization, (2) MEMS-based application scope and the extreme hardware constraints of Cortex-M0+/M4 MCUs, (3) the five model-compression methods (knowledge distillation, pruning, quantization, weight-sharing, low-rank decomposition) with explicit attention to their [[concepts/bayesian-compression|Bayesian-compression]] variants, and (4) the [[concepts/tinymlops|TinyMLOps]] pipeline and the four main TinyML frameworks (CMSIS-NN, TFLM, NNoM, Edge Impulse). The review's distinctive contributions are: a Bayesian synthesis that unifies pruning and quantization under spike-and-slab / horseshoe / log-uniform priors; a runtime-vs-transcompiler taxonomy of TinyML frameworks; and a per-dataset Flash-size-vs-accuracy analysis that overlays Cortex-M0+/M4/M7 memory thresholds on MNIST, ImageNet, Visual Wake Word, and Google Speech Commands v2-12 model landscapes.

![[raw/papers/le-2026-efficient-nn-tinyml-review/figures/0e790a48f27fb36f257a3be7432342984ec2483c8b71096c1f8279ca366afb5b.jpg|Figure 1]]

*Figure 1: TinyML as the intersection of AI and embedded systems.*

## Taxonomy

The review organizes TinyML along four axes, mirroring its four body sections:

| Axis | Section | Coverage |
|------|---------|----------|
| 1. NN fundamentals | §2 | Feedforward NNs, universal approximation, double descent, why TinyML falls outside the well-studied regime |
| 2. MEMS + MCU hardware | §3 | MEMS sensors, MCU heterogeneity (ARM Cortex-M0+/M4/M7, RISC-V), fixed-point arithmetic, 8 kB–512 kB SRAM regimes |
| 3. Efficient-NN methods | §4 | Five model-compression families: KD, pruning (unstructured/structured/Bayesian), quantization (QAT/PTQ, uniform/non-uniform, sym/asym, Bayesian), weight-sharing, low-rank decomposition |
| 4. TinyMLOps deployment | §5 | Framework taxonomy (runtime vs transcompiler), CMSIS-NN, TFLM, NNoM, Edge Impulse, algorithm-hardware co-design (RISC-V ISA extension), MLPerf Tiny benchmark |

A distinctive feature is that the review explicitly positions itself *between* two prior survey families: methodological surveys (Guo 2018 on quantization; Gholami 2022 on quantization; Gou 2021 on KD; Hoefler 2021 on sparsity; Alqahtani 2021 on compression) that "do not address the TinyML context or constraints," and application-focused surveys (Han & Siebert 2022; Ray et al.; Schizas et al.) that "offer little insight into NN architectures, optimization methods, or tradeoffs at the algorithmic level." This review bridges the two by combining NN fundamentals + MCU hardware + compression methods + deployment tools in a single narrative.

## Methodology

### Section 2 — NN Fundamentals and Why TinyML Is Hard

The review opens with the standard feedforward NN formulation $h^{(l)} = \phi^{(l)}(W^{(l)} h^{(l-1)} + B^{(l)})$ and reviews universal approximation (Cybenko 1989; Hornik 1989; Lin & Jegelka for ResNets), overparameterization, and double descent. The key TinyML-relevant point: expressiveness and generalization guarantees "are mainly verified for large NNs," so obtaining good training and generalization on sub-megabyte models is "very challenging" — a regime where standard DL theory offers little guidance.

### Section 3 — MEMS-Based Applications on Ultra-Low-Power MCUs

![[raw/papers/le-2026-efficient-nn-tinyml-review/figures/e3b4d3f534f2b523fff6bccaba6385360a9af44d05a4f81108384665cecf108e.jpg|Figure 3a]]

![[raw/papers/le-2026-efficient-nn-tinyml-review/figures/71cfffec82e2f0704e2a4380d798160560dfcea8f8806add2568637bad8d5068.jpg|Figure 3b]]

*Figure 3: Memory hierarchies for (a) a mobile processor with off-chip DRAM and (b) an ARM Cortex-M7 microcontroller where all computation and data transfer happen on-chip.*

The review targets the "extreme low-end range of MCUs, with less than 8 kB of RAM and 10 MHz processing speed." Key hardware comparisons (Table 4):

| Platform | Architecture | Memory (SRAM) | Storage | Frequency | Power | Price |
|----------|-------------|---------------|---------|-----------|-------|-------|
| Cloud (Nvidia V100S) | GPU Volta | 32 GB HBM | TB–PB | 1.2–1.3 GHz | 250 W | $14,500 |
| Mobile (Galaxy Note 20) | Kryo 585 | 8 GB DRAM | 128 GB | 1.8–3.1 GHz | ~8 W | $550 |
| TinyML — Cortex-M7 | ARM Cortex-M7 | 384 kB | 2,048 kB | 300 MHz | 0.3 W | $5 |
| TinyML — SAMG55J19 | ARM Cortex-M4 | 160 kB | 512 kB | 120 MHz | 0.1 W | $3 |
| TinyML — Newport | ARM Cortex-M0+ | **8 kB** | 16 kB | 6.14 MHz | **70 μW** | $1 |
| TinyML — Newport | eDMPv1 | 4 kB | 16 kB | 6.14 MHz | 66 μW | $1 |
| TinyML — HiFive1 Rev B | RISC-V RV32IMAC | 16 kB | 512 kB | 320 MHz | 0.14 W | $50 |
| TinyML — VEGAboard | RISC-V RV32IMC | 8 kB | 64 kB | 100 MHz | 0.1 W | $20 |

The review emphasizes that even within TinyML, "Cortex-M4 only consumes 0.1 W, yet it still represents a target that is 1,500 times more power-hungry and 20 times more memory capacity compared to the Cortex-M0+." The industrial incentive is concrete: "a 2$ difference observed between the low-end of MCUs... magnifies when considering the billions of annual unit market sales."

**Fixed-point arithmetic**: Because the Cortex-M0+ lacks an FPU, the review restricts to fixed-point Qm.n representation (Figure 4) and the conversion $Q(F, n) = \lfloor F \cdot 2^n \rceil$, $F(Q, n) = Q \cdot 2^{-n}$. Dynamic range drops from $\sim 10^{38}$ (FP32) to $\approx [-2^{15}, 2^{16}]$ (Q16.16), and only "primitive operations like bit-manipulation, Boolean operators, and basic additions or multiplications" are supported — explicit division and exponentiation must be avoided. See [[concepts/ieee-754|IEEE 754]] for the floating-point representation baseline.

**ARM vs RISC-V**: ARM dominates TinyML deployments via mature toolchain and CMSIS-NN. RISC-V is "emerging as an attractive alternative due to its open, extensible ISA that allows hardware customization," but its software ecosystem is comparatively immature — TFLM and TVM "have recently begun adding native RISC-V back-ends, yet their coverage of instruction extensions (DSP, vector, bit-manipulation) is partial."

### Section 4 — Efficient NNs for TinyML

The review frames model compression as "a set of methods aiming to address the growing power footprint and costs... on resource-constrained devices, such as MCUs," and identifies five families: **KD, pruning, quantization, weight-sharing, low-rank decomposition**. Quantization is singled out as "the most critical method since it is a mandatory step in deploying models on MCUs."

#### 4.1 Knowledge Distillation

Standard KD loss combining student task loss and KL divergence between softened teacher/student distributions:

$$L_{\mathrm{KD}}(x, y) = \alpha L_{\mathrm{S}}(x, y) + (1 - \alpha) \mathrm{D}_{\mathrm{KL}}\!\left(\mathrm{softmax}\!\left(\tfrac{T(x,y)}{\text{temp}}\right), \mathrm{softmax}\!\left(\tfrac{S(x,y)}{\text{temp}}\right)\right)$$

The review notes that "there is limited use of KD for deployment on MCUs in the existing literature," attributable to "the simplicity of pruning and quantization methods and the more stringent size constraints compared to mobile-sized models." See [[concepts/knowledge-distillation-paradigms|Knowledge Distillation Paradigms]] for the broader offline/online/self-distillation taxonomy.

#### 4.2 Model Pruning

The review distinguishes **unstructured** (fine-grained weight removal) from **structured** (block-level: neurons, filters, channels, rows/columns) pruning, and introduces **Bayesian pruning** as a third category that subsumes both via prior selection. See [[concepts/model-pruning|Model Pruning]] for the full taxonomy.

![[raw/papers/le-2026-efficient-nn-tinyml-review/figures/49e350408e3eb9a52c796b7971170db24435334d15b37cbecdce0c4ba537bd3f.jpg|Figure 5]]

*Figure 5: Unstructured pruning (left) versus structured pruning (middle, right).*

The polynomial gradual-sparsity schedule of Zhu & Gupta (2017):

$$s_t = s_f + (s_0 - s_f) \left(1 - \tfrac{t - t_0}{n \Delta t}\right)^3$$

prunes "quickly and early when there is the most redundancy, and then slow down... as there is little remaining redundancy." Magnitude-based pruning is highlighted as "model- and task-agnostic, can seamlessly incorporate within training, and is easy to implement," achieving 90% sparsity with acceptable accuracy loss on large networks. Structured pruning's advantage is hardware efficiency: "it may allow skipping entire filters or rows during a matrix multiplication," but it "has strict compression rules that make them more difficult to achieve without degrading performance."

The [[concepts/bayesian-compression|Bayesian compression]] synthesis (covered in detail in §4.3 of this page below) treats pruning as a spike-and-slab / horseshoe / log-uniform prior selection problem and is presented as the review's distinctive unifying framework for both pruning and quantization.

#### 4.3 Quantization

The review organizes quantization along three orthogonal axes, all of which are surveyed for the TinyML regime:

| Axis | Options | TinyML preference |
|------|---------|-------------------|
| Stage | QAT vs PTQ | PTQ for simplicity; QAT for <8-bit |
| Step type | Uniform vs Non-uniform | **Uniform** (mandatory for hardware support) |
| Zero-point | Symmetric ($Z=0$) vs Asymmetric ($Z \neq 0$) | Symmetric simpler; Asymmetric uses full `[-128, +127]` range |

Quantization function and scaling (Equations 7–8):

$$Q(r) = \mathrm{int}(r/S) - Z, \quad S_{\mathrm{sym}} = \tfrac{\max(|\alpha|, |\beta|)}{2^{b-1}-1}, \quad S_{\mathrm{asym}} = \tfrac{\max(|\alpha|, |\beta|)}{(2^b - 1)/2}$$

Key TinyML-specific finding: "very small models, that can be found in TinyML, should be more sensitive to quantization" than overparameterized cloud models — the redundancy that "allows for some leniency in quantization errors" is precisely what TinyML lacks. See [[concepts/quantization-aware-training|Quantization-Aware Training]] and [[concepts/post-training-quantization|Post-Training Quantization]] for the standard treatment; [[concepts/quantization-aware-scaling|Quantization-Aware Scaling (QAS)]] for the MCUNetV3-specific int8 training stabilizer.

The review's conclusion: "we would favor uniform 8-bit PTQ due to its simplicity and acceptable results until we need lower-bit precision for more power footprint reduction."

#### 4.4 Weight-Sharing

"Weight-sharing is the simplest form of model compression, involving sharing weights values in different parts of the model." K-means clustering of weights (Han et al. 2016) compressed a CNN by 3× without significant loss. The review notes that "quantization is a form of weight-sharing because lowering the bit-precision of parameters forces them to be aggregated into a common set of values" — an explicit unification of the two methods. Weight-sharing "has not been widely adopted for TinyML models."

#### 4.5 Low-Rank Matrix and Tensor Decompositions

Weight matrices are replaced by products of lower-rank matrices (SVD or tensor decomposition). Alvarez & Salzmann (2017) obtained up to 96% compression. Caveats: "additional hyperparameter tuning" and "trial and error to find the optimal rank, which may not generalize between applications," plus the concern that "the incorporation of additional products from the lower-rank matrix may not always lead to increased efficiency and reduced power consumption" on MCUs.

### Section 5 — Deploying DL Models on Ultra-Low-Power MCUs

#### 5.1 TinyMLOps Definition

![[raw/papers/le-2026-efficient-nn-tinyml-review/figures/09c1f50e8c97623021555e8980155b8dac92d1aa12f6a956332f18898251c3f8.jpg|Figure 8]]

*Figure 8: The TinyMLOps pipeline — extending MLOps to embedded-device deployment.*

The review defines [[concepts/tinymlops|TinyMLOps]] as the subset of MLOps focused on "the process of taking a trained model and enabling it to run on an embedded system, such as compiling the model, firmware integration, and verification of the solution on the target device." It notes TFLM (2019) was "the first dedicated DL framework for MCUs," and that "the TinyMLOps ecosystem is still in an earlier stage than MLOps, with challenges yet to be fully addressed." The fundamental challenge: "the tight dependency between software and hardware components... failure to adapt the delivered ML software to the constraints of particular hardware renders it unusable."

#### 5.2 TinyML Framework Taxonomy

The review introduces a distinctive **runtime vs transcompiler** taxonomy of TinyML frameworks:

| Approach | Description | Examples |
|----------|-------------|----------|
| Runtime | Loads model from read-only device memory at runtime; interpreter-based | TFLM |
| Transcompiler | Converts and compiles models to C/C++ code built into the project | NNoM, Edge Impulse, μTVM |

**CMSIS-NN** (low-level library): ARM's optimized NN kernel library for Cortex-M, providing FC, convolution, and activation (ReLU, sigmoid, tanh) functions. Reported 4.6× speedup and 4.9× energy savings over non-optimized convolutional models.

**TFLM** (runtime): TensorFlow Lite Micro converts and quantizes a 32-bit floating-point TensorFlow model to a compressed flatbuffer `.tflite` using 8-bit integer weights and 32-bit integer activations/data. Three components: operator resolver, memory stack pre-allocation, interpreter. Limitations: missing GRU, Conv1D, some activations; no arbitrary bit-widths; no target-specific optimizations; no built-in power-footprint measurement; interpreter-based approach "makes it difficult to debug and extend." Despite these, "TFLM remains the most popular choice."

**NNoM** (transcompiler): Open-source C code generation with CMSIS-NN support for ARM Cortex-M. Supports all RNN layers including GRU (unlike TFLM). Limitations: no lower-bit-width quantization, smaller community.

**Edge Impulse** (transcompiler): Closed-source cloud service with no-code GUI. Uses the EON (Edge Optimized Neural) compiler, which "can run the same model with 25%–55% less SRAM and 35% less flash memory than TFLM." Provides end-to-end pipeline (data collection, feature extraction, training, deployment).

#### 5.3 Algorithm-Hardware Co-Design

Verma et al.'s RISC-V co-design workflow: compiler translates ML library functions to C, then generates a custom processor with SDK and specialized instructions. Achieved 17.63× speedup for vector–matrix multiplication via a 16×16 custom Vector–Matrix Multiply instruction.

#### 5.4 MLPerf Tiny Benchmark

The benchmark evaluates latency and energy per single-input inference on five task/model combinations: Keyword Spotting (Speech Commands, Depth-Separable CNN), Anomaly Detection (ADMOS Toy Car, FC AutoEncoder), Person Detection (COCO Visual Wakeword, MobileNetV1 0.25×), Image Classification (CIFAR-10, ResNet-V1, ≥85% accuracy required). See [[concepts/keyword-spotting|Keyword Spotting]] for the application context.

## Results

### Per-Dataset Flash-Size-vs-Accuracy Analysis (Section 6)

The review's central experimental contribution is a per-dataset scatter analysis of Flash model size vs. accuracy, overlaid with vertical lines for Cortex-M0+ (16 kB), Cortex-M4 (512 kB), and Cortex-M7 (2,048 kB) Flash limits. The analysis covers four standard TinyML benchmarks:

![[raw/papers/le-2026-efficient-nn-tinyml-review/figures/5a64749b6f5f709cbdde3ade5a1f78a8e2be562d3fb2b7a43064641570e8afed.jpg|Figure 9a]]

![[raw/papers/le-2026-efficient-nn-tinyml-review/figures/32aff91a2c4128d9c53c518f439ea00ec979d988863cd9f57d6258e96a8aa8db.jpg|Figure 9b]]

![[raw/papers/le-2026-efficient-nn-tinyml-review/figures/6ba6bde68dab41183ee7dc3dc30d5f94ab8f81df3784ad26766c605e50442d91.jpg|Figure 9c]]

![[raw/papers/le-2026-efficient-nn-tinyml-review/figures/79899ccd91e39457f2a99b01c73e0519082ff49e01ff6569cfc08724e59af8f6.jpg|Figure 9d]]

*Figure 9: Flash model size versus accuracy on (a) MNIST, (b) ImageNet, (c) Visual Wake Word, (d) Google Speech Commands v2-12. Vertical grey dashed lines indicate Cortex-M0+, M4, and M7 storage limits.*

Key per-dataset findings:

| Dataset | Best size-accuracy tradeoff | Cortex-M0+ feasibility |
|---------|----------------------------|------------------------|
| MNIST | μNAS (below Cortex-M0+ threshold); LeNet slightly better accuracy but over threshold | Yes (μNAS, Sparse CNN, ProtoNN) |
| ImageNet | MCUNet (large) — "right below the Cortex-M7 memory threshold"; SqueezeNet/MNasNet unsuitable | No — most models above M4/M7 threshold |
| Visual Wake Word | MSNet (optimal in ultra-low-power range); RaScaNet for lower power | No model below Cortex-M0+ threshold yet; "reachable with further research" |
| Google Speech Commands v2-12 | FastGRNN (extreme-low-power range); μNAS (ultra-low-power range) | Yes (FastGRNN) |

Cross-dataset conclusion: "TinyML models are able to comply with extreme-low power constraints as low as 8 kB for a speech recognition task and a simple image classification dataset, with a given tradeoff on accuracy. In this regard, further research efforts are required for an image recognition task and a more complex image classification problem. Otherwise, Cortex M4 is sufficient to run most models for all tasks with the best accuracy."

### Compression-in-Practice Results (Section 5.1)

| Method combination | Dataset | Accuracy | Model size | Notes |
|--------------------|---------|----------|------------|-------|
| Bayesian structured pruning (Fedorov et al. 2019) | MNIST | 98.64% | 2.77 kB (1.96 kB RAM) | 80× parameter reduction |
| Structured pruning (Liberis & Lane) | CIFAR-10 | 91.98% | 256 kB | — |
| Structured pruning (Liberis & Lane) | Google Speech Commands v2-12 | 96.03% | 115 kB | — |
| KD (Polino et al.) — small student | CIFAR-10 | 77.92% | 450 kB | 46× smaller than teacher |
| KD (Polino et al.) — medium student | CIFAR-10 | 84.22% | ~1,350 kB | ~3× small student |
| KD + PTQ (Zein et al.) | CIFAR-10 | 69.5% | 81 kB | — |
| KD (TinyBERT) | GLUE | — | 14.5M params | 7.5× smaller, 9.4× faster; still too large for MCU |
| Pruning + weight-sharing + quantization (Han et al. 2016) | MNIST | 98.42% | 27 kB | 1,070 kB → 27 kB (~40×) |
| Sparse decomposition + quantization (Kusupati et al.) | Google Speech Commands v2-12 | 92.21% | 57 kB | — |

### MLPerf Tiny Latency/Energy (Table 6)

On Cortex-M4 vs Cortex-M7, the M4 has lower energy consumption but higher latency than the M7 — consistent with the M7's higher frequency and higher power draw. The review notes that "latency is considered as secondary and is less frequently reported in the literature" than memory size, because "memory size is the primary constraint to overcome for deploying TinyML models."

## Key Contributions

1. **Bridging survey gap**: First review to combine NN fundamentals + MCU hardware characteristics + compression methods + deployment tools in a single narrative, explicitly positioned between methodological-only surveys (Guo, Gholami, Gou, Hoefler, Alqahtani) and application-only surveys (Han & Siebert, Ray, Schizas).
2. **Bayesian compression synthesis**: Unifies pruning and quantization under a single Bayesian framework via spike-and-slab, horseshoe, and log-uniform priors — see [[concepts/bayesian-compression|Bayesian Compression]].
3. **TinyMLOps framework taxonomy**: Introduces the runtime-vs-transcompiler classification of TinyML frameworks (TFLM vs NNoM/Edge Impulse/μTVM).
4. **Per-dataset Flash-size-vs-accuracy landscape**: Overlays Cortex-M0+/M4/M7 memory thresholds on MNIST, ImageNet, VWW, and Google Speech Commands v2-12 model-scatter plots — letting practitioners directly read off which models deploy on which MCU class. See Figure 9.
5. **Extreme-low-power regime emphasis**: Targets the <8 kB SRAM / 10 MHz regime (Cortex-M0+, eDMPv1) that the literature typically treats as out of reach, and identifies the $2 MCU price difference as a billion-dollar industrial incentive.
6. **ARM-vs-RISC-V analysis**: Surveys recent RISC-V TinyML efforts (Lite-QAIRISC, Cheshire, Extrem-Edge, RIOT-ML) and characterizes the tradeoff between ARM's ecosystem maturity and RISC-V's ISA extensibility.
7. **Open challenges catalog**: Identifies adversarial robustness on MCUs, adaptive resource management (dynamic quantization, early-exit networks), standardized benchmarking beyond accuracy (latency, memory, energy), and hardware-algorithm co-design beyond ARM as concrete research directions.

## Limitations and Caveats

- **No novel algorithms**: This is a review; all surveyed methods (KD, pruning, quantization, etc.) are previously published. The contributions are the synthesis, taxonomy, and per-dataset landscape analysis.
- **Memory-size focus**: The experimental analysis emphasizes Flash model size over latency/energy because "memory size is the primary constraint" and "latency is considered as secondary and is less frequently reported in the literature." Practitioners needing latency/energy numbers should consult MLPerf Tiny directly.
- **TensorFlow-only framework scope**: The TinyML-framework comparison is explicitly restricted to "frameworks that support TensorFlow models as input... and that also target Arm Cortex-M MCUs for inference," excluding PyTorch-native workflows and non-ARM targets.
- **Uniform-quantization-only scope**: Non-uniform quantization is excluded because "non-uniform quantization schemes are challenging to deploy on embedded hardware because they require a custom implementation," so the quantization survey focuses on uniform schemes.
- **KD underused for MCUs**: The review explicitly notes "limited use of KD for deployment on MCUs in the existing literature," attributing this to the simplicity of pruning/quantization and stricter size constraints.
- **RISC-V software ecosystem immaturity**: While RISC-V's openness is highlighted as an opportunity, the review acknowledges that "efficient TinyML deployment on RISC-V currently requires low-level toolchain customization or hardware-software co-design."

## Related Concepts

- [[concepts/tinyml|TinyML]] — the field this review surveys; updated with this source
- [[concepts/model-pruning|Model Pruning]] — unstructured / structured / Bayesian taxonomy, central to §4.2
- [[concepts/bayesian-compression|Bayesian Compression]] — spike-and-slab, horseshoe, log-uniform priors unifying pruning and quantization (§4.2, §4.3)
- [[concepts/tinymlops|TinyMLOps]] — the deployment pipeline and framework taxonomy introduced in §5
- [[concepts/knowledge-distillation-paradigms|Knowledge Distillation Paradigms]] — broader offline/online/self-distillation taxonomy
- [[concepts/quantization-aware-training|Quantization-Aware Training]] — QAT survey in §4.3
- [[concepts/post-training-quantization|Post-Training Quantization]] — PTQ survey in §4.3
- [[concepts/quantization-aware-scaling|Quantization-Aware Scaling (QAS)]] — MCUNetV3's int8 training stabilizer
- [[concepts/keyword-spotting|Keyword Spotting]] — primary TinyML audio application
- [[concepts/neural-architecture-search|Neural Architecture Search]] — μNAS, MSNet, MCUNet surveyed in §6
- [[concepts/ieee-754|IEEE 754]] — floating-point baseline for the fixed-point discussion in §3.3

## Related Sources

- [[sources/lin-2023-tinyml-progress-futures|Lin et al. 2023: TinyML — Progress and Futures]] — the MIT HAN Lab review covering the MCUNet family (V1/V2/V3) and on-device training; complementary focus on system–algorithm co-design
- [[sources/liu-2024-lightweight-dl-survey|Liu et al. 2024: Lightweight Deep Learning for Resource-Constrained Environments]] — broader survey framing TinyML as a future frontier alongside lightweight LLMs; catalogs CMSIS-NN, CMIX-NN, MicroNet
- [[sources/lin-2020-mcunet|Lin et al. 2020: MCUNet]] — first 70% ImageNet top-1 on a commercial MCU; surveyed here as a key ImageNet frontier
- [[sources/lin-2021-mcunetv2|Lin et al. 2021: MCUNetV2]] — patch-based inference and receptive field redistribution
