---
type: source
created: 2026-08-09
updated: 2026-08-09
sources:
  - raw/papers/liu-2024-lightweight-dl-survey/full-text.md
  - https://arxiv.org/abs/2404.07236
  - zotero://select/items/0_FFWWNXQT
tags:
  - survey
  - review
  - lightweight-deep-learning
  - model-compression
  - pruning
  - quantization
  - knowledge-distillation
  - neural-architecture-search
  - hardware-acceleration
  - tinyml
  - efficient-transformer
  - llm
  - edge-ai
  - green-ai
---

# Liu, Galindo, Xie, Wong, Shuai, Li & Cheng 2024: Lightweight Deep Learning for Resource-Constrained Environments

- **Authors**: [[entities/hou-i-liu|Hou-I. Liu]], [[entities/marco-galindo|Marco Galindo]], [[entities/hongxia-xie|Hongxia Xie]], [[entities/lai-kuan-wong|Lai-Kuan Wong]], [[entities/hong-han-shuai|Hong-Han Shuai]], [[entities/yung-hui-li|Yung-Hui Li]], [[entities/wen-huang-cheng|Wen-Huang Cheng]]
- **Institutions**: National Yang Ming Chiao Tung University (NYCU); Jilin University; Multimedia University; Hon Hai Research Institute (Foxconn); National Taiwan University (NTU)
- **Venue**: arXiv preprint, 2024 (Computer Science — CV and ML)
- **Type**: Review / survey article
- **DOI**: [10.48550/arXiv.2404.07236](https://doi.org/10.48550/arXiv.2404.07236)
- **arXiv**: [2404.07236](https://arxiv.org/abs/2404.07236)
- **Zotero**: [FFWWNXQT](zotero://select/items/0_FFWWNXQT)
- **Source**: `raw/papers/liu-2024-lightweight-dl-survey/full-text.md`

## Summary

This survey provides a comprehensive end-to-end pipeline view of lightweight deep learning for resource-constrained devices (mobile phones, MCUs, IoT), unifying three pillars that prior surveys treated in isolation: (1) lightweight **architecture design** (CNN families and efficient transformers), (2) model **compression methods** (pruning, quantization, knowledge distillation, NAS), and (3) **hardware acceleration** (GPU/FPGA/ASIC/TPU architectures, dataflows, DL libraries, software-hardware co-design). It closes with two forward-looking directions — [[concepts/tinyml|TinyML]] on sub-1 mW MCUs, and lightweight Large Language Models (LLMs) on edge devices — framing both as the next frontier of resource-constrained DL.

## Taxonomy

The survey's central organizational contribution is a **three-stage pipeline** for lightweight DL deployment, explicitly connecting stages that prior surveys covered only in isolation:

| Stage | Pillar | Survey Section | Representative Methods |
|-------|--------|---------------|----------------------|
| 1 | Architecture Design | §2 | MobileNet family, ShuffleNet, CondenseNet, SqueezeNet, Shift-based, AdderNet, Efficient Transformers (ViT, DeiT, MobileViT, EViT, T2T-ViT) |
| 2 | Model Compression | §3 | Pruning (unstructured / structured), Quantization (1–16 bit), Knowledge Distillation (offline / online / self), NAS (RL / EA / gradient / hardware-aware) |
| 3 | Hardware Acceleration | §4 | GPUs, FPGAs, ASICs/TPUs, dataflow types, data locality optimization, DL libraries (TF-Lite, PyTorch, MXNet, cuDNN, TensorRT), co-design |
| 4 | Future Frontier | §5 | TinyML (CMSIS-NN, TinyEngine, MCUNet family), Lightweight LLMs (SparseGPT, Wanda, prompt tuning, lightweight diffusion) |

The survey emphasizes that **parameters and FLOPs do not consistently correlate with inference time** — early architectures (SqueezeNet, MobileNet) reduced FLOPs but increased Memory Access Cost (MAC), causing slower inference. This motivates the joint architecture–compression–hardware view.

## Methodology

### Section 2 — Lightweight Architecture Design

#### 2.1 Prior Knowledge

- **Evaluation metrics**: FLOPs (arithmetic ops), MACs (multiply-accumulate ops, FLOPs ≈ 2 × MACs), Memory Access Cost (MAC = $H \cdot W(C_{in}+C_{out})+k \cdot k(C_{in}\times C_{out})$ for a conv layer), throughput (inferences/sec), latency (seconds/inference).
- **Pointwise convolution** ($1\times 1$ conv): introduced by the Inception module for channel-dimension modification at low FLOPs.
- **Group convolution**: from AlexNet; divides channels into groups and convolves separately, reducing complexity by $N$× ($N$ = group count) but blocking cross-group information flow.
- **Depthwise separable convolution**: from Xception; depthwise conv followed by pointwise conv — computation-saving but time-consuming due to high MAC.

#### 2.2 Lightweight CNN Architecture Families

The survey organizes lightweight CNNs into **chronological "series"** reflecting the evolution of efficient design — see [[concepts/lightweight-cnn-families|Lightweight CNN Families]] for the full taxonomy. Series covered:

1. **SqueezeNet series** — fire module (squeeze + expand layers); SqueezeNext decomposes 3×3 into 3×1 + 1×3, reducing $k^2$ params to $2k$; 50× and 112× parameter reduction vs. AlexNet.
2. **ShuffleNet series** — channel shuffle after group conv for cross-group information exchange; ShuffleNetV2's four practical guidelines for memory-efficient design (equal channel dims, small groups, avoid fragmentation, avoid element-wise ops).
3. **CondenseNet series** — Learned Group Convolutions (LGCs) that prune unimportant connections during training; CondenseNetV2 adds sparse feature reactivation to dynamically relearn connections.

![[raw/papers/liu-2024-lightweight-dl-survey/figures/fig1.png|Figure 1]]

*Figure 1: Comparison of DenseNet, CondenseNet, and CondenseNetV2. Active weight connections are solid arrows; pruned connections are gray dashed arrows. CondenseNet fixes pruned connections after training; CondenseNetV2 reactivates them dynamically.*

4. **MobileNet series** — depthwise separable convs (V1); inverted residual + linear bottleneck (V2); platform-aware NAS + SENet + H-swish (V3); Sandglass block flipping the inverted residual (MobileNeXt).
5. **Shift-based series** — ShiftNet replaces spatial conv with zero-FLOP Group Shift; Active Shift Layer (learnable shifts); Sparse Shift Layer; AddressNet (channel shift instead of shuffle); DeepShift (bit-wise shifts + sign flips).
6. **Add-based series** — AdderNet replaces multiplications with L1-norm distance (Absolute-difference-accumulation); ShiftAddNet combines bit-wise shifts with additive networks for hardware efficiency.

#### 2.3 Efficient Transformers

Self-attention has $O(N^2)$ complexity in sequence length. The survey covers three efficiency directions:

- **Efficient self-attention** — Sparse Transformer ($O(N\sqrt{N})$), Linformer ($O(N)$), Reformer ($O(N\log N)$).
- **Token sparsing** — T2T-ViT (soft unfolding), DynamicViT (binary mask prediction), EViT (top-K tokens by attentiveness), A-ViT (adaptive token count by depth).
- **Lightweight hybrid models** — DeiT (KD from CNN teacher), MobileViT (MobileNetV2 backbone + MobileViT block), MobileFormer (parallel CNN+transformer with two-way cross-attention).

**Key observation**: hybrid models achieve the lowest FLOPs (Mobile-Former-96M: 0.096 G) and lowest parameters (MobileViT-XS: 2.3 M), but lower FLOPs has greater accuracy impact than lower parameters — challenging the assumption that FLOPs and parameters correlate.

### Section 3 — Model Compression

#### 3.1 Pruning

![[raw/papers/liu-2024-lightweight-dl-survey/figures/fig4.png|Figure 4]]

*Figure 4: Unstructured pruning (left) zeros individual weights irregularly; structured pruning (right) removes entire filters/channels, preserving regular structure for hardware compatibility.*

- **Unstructured pruning** — Optimal Brain Damage / Surgeon (Hessian-based), lottery ticket hypothesis, network slimming. Produces irregular sparsity incompatible with dense hardware.
- **Structured pruning** — filter pruning (Geometric Median, learnable thresholds, adaptive sensitivity-based thresholds), channel pruning (L1 norm, Hessian-based, layer grouping, CATRO). Regular structure compatible with PyTorch/TensorFlow built-in primitives.

#### 3.2 Quantization

- **Symmetric vs. asymmetric** quantization representations.
- **Bit-width trade-offs** (Table 5): 4-bit quantization preserves accuracy (LLT: +0.6% / −0.3%); 2-bit causes 3–4% loss; 1-bit (XNOR-Net) causes 18% loss.
- **Practical guidance**: match quantization precision to hardware (MCUs/edge TPUs often require full integer); 8-bit int recommended for low-power CPUs; 16-bit float as a starting point when hardware permits; TF-Lite achieves 4× size reduction and 3×+ inference speedup.

#### 3.3 Knowledge Distillation (KD)

![[raw/papers/liu-2024-lightweight-dl-survey/figures/fig6.png|Figure 6]]

*Figure 6: Three KD paradigms — (a) Offline Distillation (pre-trained teacher, sequential), (b) Online Distillation (concurrent teacher-student training, e.g., Deep Mutual Learning), (c) Self-Distillation (model teaches itself across depths or epochs). Orange lines denote gradient updates.*

See [[concepts/knowledge-distillation-paradigms|Knowledge Distillation Paradigms]] for the survey's three-paradigm taxonomy. **Practical guidance**:
- **Offline KD** — viable when training a large teacher is feasible (vanilla KD, SimKD, SemCKD).
- **Online KD** — Deep Mutual Learning (DML) needs no pre-trained teacher, suits multi-GPU training of small models; mean-teacher framework is valuable for scarce/noisy labels (pseudo-label generation).
- **Self-distillation** — single-model, but weaker gains (PS-KD: +3.36%); pair with other methods.

#### 3.4 Neural Architecture Search (NAS)

The survey organizes NAS by search algorithm — see [[concepts/neural-architecture-search|Neural Architecture Search]] for the cross-reference:

- **RL-based NAS** — Zoph et al.'s RNN controller; MnasNet's factorized hierarchical search with latency-aware Pareto optimization.
- **EA-based NAS** — AmoebaNet-style population evolution with mutation; encoding mechanisms to accelerate evolution.
- **Gradient-based NAS** — DARTS (differentiable architecture search); FBNet's DNAS pipeline with layer-wise latency lookup table and latency-aware loss $L(a,w_a) = CE(a,w_a) \cdot \alpha \log(LAT(a))^\beta$.

![[raw/papers/liu-2024-lightweight-dl-survey/figures/fig7.png|Figure 7]]

*Figure 7: NAS with reinforcement learning. An RNN controller generates candidate architectures; the child network's accuracy becomes the reward signal that updates the controller.*

![[raw/papers/liu-2024-lightweight-dl-survey/figures/fig8.png|Figure 8]]

*Figure 8: The DNAS pipeline in FBNet — a stochastic supernetwork is optimized with SGD over a layer-wise search space, with latency injected via a lookup table.*

- **Other NAS** — NetAdapt's layer-wise lookup table (energy/memory-aware), NetAdaptV2's Channel-Level Bypass Connections, zero-cost proxies for single-forward-pass NAS scoring.

![[raw/papers/liu-2024-lightweight-dl-survey/figures/fig9.png|Figure 9]]

*Figure 9: Layer-wise lookup table used by NetAdapt — per-layer latency is pre-measured so total latency is a sum over layers, simplifying the search for pre-trained networks.*

### Section 4 — Hardware Acceleration

#### 4.1 Hardware Architectures

| Architecture | Type | Strengths | Limitations |
|-------------|------|-----------|-------------|
| **CPU** | Temporal | SLIDE shows CPU can beat NVIDIA-V100 with smart randomized algorithms | Low FLOPs; serial; poorly suited for typical DL training |
| **GPU** | Temporal | Thousands of cores; matrix-ops; primary DL accelerator | High power consumption; unsuitable for edge/IoT |
| **FPGA** | Spatial | Reprogrammable; low power; supports pruning & DSP algorithms well | Slower than ASICs; smaller batch throughput |
| **ASIC (TPU)** | Spatial | Highest speed, lowest power, highest throughput at scale | High NRE cost; inflexible; TPU-v4 = 4096 chips, 2.7× perf/watt and 10× speed vs. TPU-v3 |

**Selection rule**: GPUs for training/cloud; FPGAs for rapid-development or small-batch edge AI; ASICs for mass-produced mature products; TPUs for budget-rich large-model training (GPT-4, LLaMA).

#### 4.2 Dataflow and Data Locality Optimization

The survey contributes a **four-type dataflow taxonomy** — see [[concepts/hardware-dataflow-types|Hardware Dataflow Types]] for details:

![[raw/papers/liu-2024-lightweight-dl-survey/figures/fig10.png|Figure 10]]

*Figure 10: Comparison of dataflow types — pipeline-like, DaDianNao-like, systolic-array-like, streaming-like. PE = processing element.*

- **Pipeline-like** — input pixels flow through PEs with fixed weights; high parallelism but sequential stages.
- **DaDianNao-like** — each PE acts as a neuron with embedded weights; adder tree aggregates partial sums; handles irregular kernels but energy-intensive.
- **Systolic-array-like** — pixels and weights cascade through PEs; high hardware utilization; mapping challenge.
- **Streaming-like** — continuous data flow without intermediate storage; ideal for audio/video; limited to simple stage-wise operations.

**Data locality optimization**: loop unrolling (parallelism but code bloat), loop tiling (block-level parallelism for limited SRAM), loop interchange (cache-line reuse via loop reordering).

#### 4.3 DL Libraries

TensorFlow / TF-Lite (mobile/edge), PyTorch (research, with deployment limitations), MXNet (Intel-optimized, multi-language), cuDNN / CUDA-X / TensorRT (NVIDIA GPU optimization), ONNX (cross-library interoperability).

#### 4.4 Co-Design of Hardware Architecture

The survey synthesizes **hardware-software co-design** as a holistic strategy addressing the limitations of software-only or hardware-only solutions. Three directions:

1. **Sparse weight access** — Cambricon-X (sparse indices, but PE imbalance), Cambricon-S (regular filter sparsity enforced), Sparse-YOLO (dedicated sparse conv unit), SCNN (compressed-format convolution with input-stationary dataflow). Han et al. show 20–30% memory bandwidth reduction from sparse weight compression.
2. **NAS + hardware co-search** — joint optimization of CNN and accelerator (Chen et al.'s supernet approach); hardware optimization first, then network training only if viable (Lin et al.).

![[raw/papers/liu-2024-lightweight-dl-survey/figures/fig11.png|Figure 11]]

*Figure 11: Two approaches for NAS + hardware co-design — (a) co-search by evaluating CNN–accelerator pairs (supernet can skip per-pair training), (b) hardware-first optimization that gates whether the network is trained at all.*

## Applications Survey

### Per-Pillar Practical Recommendations

| Method | When to Use | When to Avoid |
|--------|-------------|---------------|
| **Structured pruning** | Modern frameworks have built-in support; regular structure suits hardware accelerators | When fine-grained sparsity is needed (use unstructured, but expect hardware incompatibility) |
| **Quantization (16-bit float)** | Initial step when hardware permits floating point | When MCU/edge TPU requires full integer (use int8) |
| **Quantization (8-bit int)** | Low-power CPUs; MCUs/edge TPUs supporting only integer ops | When accuracy is highly sensitive to quantization noise |
| **Offline KD** | When a large teacher can be trained first | When teacher training is infeasible |
| **Online KD (DML)** | Multi-GPU training of several small models; no pre-trained teacher available | Single-device training |
| **Mean-teacher KD** | Scarce/noisy labels (pseudo-label generation) | Abundant labeled data |
| **Self-distillation** | Single-model constraint | When maximum compression is needed (pair with other methods) |
| **RL/EA NAS** | Ample compute (hundreds of GPUs, days/weeks) | GPU-limited research (use gradient-based NAS) |
| **Gradient-based NAS (DARTS, FBNet)** | Limited compute; hardware-aware NAS | When maximum accuracy matters more than search cost |
| **Hardware-aware NAS (FBNet, NetAdapt)** | Memory/energy/latency are key constraints | When FLOPs/accuracy is the only target |
| **FPGA** | Rapid edge AI development; small-batch products | Mass-produced mature products (use ASIC) |
| **ASIC/TPU** | Mass production; budget-rich large-model training | Rapid prototyping; small batches |
| **Co-design** | Holistic optimization needed; sparse/compressed models on hardware | Simple deployment; isolated software or hardware optimization |

### Section 5 — Future Frontier

#### 5.1 TinyML

TinyML runs DL on ultra-low-power IoT devices (< 1 mW), predominantly on MCUs. MCU libraries (CMSIS-NN, TinyEngine) are platform-dependent, unlike GPU libraries. See [[concepts/tinyml|TinyML]] for the cross-source synthesis with the MCUNet family.

Surveyed MCU libraries:
- **CMSIS-NN** (ARM Cortex-M) — pioneering; NNfunctions + NNsupportfunctions split.
- **CMIX-NN** — mixed-precision (8/4/2-bit) quantization tool.
- **MCUNet** — TinyNAS + TinyEngine co-design; first >70% ImageNet on commercial MCU.
- **MCUNetV2** — patch-based inference for peak memory reduction.
- **MicroNet** — DNAS over low-operation models; state-of-the-art on TinyMLperf benchmarks (Visual Wake Words, Google Speech Commands, Anomaly Detection).

**What hinders TinyML**: (1) extreme resource constraints (< 1 MB Flash, small SRAM); (2) hardware/software heterogeneity (solutions tweaked per device); (3) lack of standard datasets matching edge-sensor data characteristics.

#### 5.2 Lightweight LLMs

LLMs at billion-parameter scale demand GPU-level hardware and tens of GB of memory. Key initiatives for edge deployment:

- **Pruning without retraining** — SparseGPT (single-step 50% sparsity, no retraining), Wanda (prune by weight × activation magnitude, no retraining, no weight updates). These set a milestone for retraining-free LLM pruning.
- **Model design** — Visual Prompt Tuning (VPT, < 1% trainable parameters), CALIP (parameter-free attention for vision-language), adaptive fine-tuning strategies.
- **Lightweight diffusion models** — post-training quantization for the denoising process (Shang et al.); trade-off between image quality and model size under compression.
- **ViT deployment** — ViT inference on mobile is up to 40× slower than CNN; bottlenecks are MatMul (attention) and FFN layers. DeiT-Tiny removes redundant heads/FFN layers for 23.2% latency reduction with 0.75% accuracy loss. DiVIT and VAQF propose FPGA co-designed ViT solutions. Two future directions: (1) algorithm optimization (accelerate/reduce MatMul, integer quantization, operator fusion); (2) hardware accessibility (ViT-specific operator support on mobile GPU/VPU, e.g., LayerNorm unsupported on Intel NCS2 VPU).

## Key Contributions

1. **Three-stage pipeline unification** — explicitly connects architecture design, compression, and hardware acceleration as a single end-to-end pipeline, unlike prior surveys that covered only one stage.
2. **"Series" taxonomy of lightweight CNNs** — groups architectures chronologically by family (SqueezeNet, ShuffleNet, CondenseNet, MobileNet, Shift-based, Add-based), reflecting design evolution rather than listing methods in isolation.
3. **Efficient-transformer categorization** — three directions: ViT & KD, ViT & CNN hybrid, ViT & Token sparsing, with quantitative comparison on ImageNet.
4. **Practical per-method guidance** — actionable "when to use" recommendations for pruning, quantization, KD, and NAS, grounded in hardware constraints (e.g., match quantization precision to MCU integer-only support).
5. **Hardware-software co-design synthesis** — integrates sparse weight access, NAS + hardware co-search, and accelerator–CNN joint optimization into a holistic co-design framework.
6. **Future frontier framing** — positions TinyML (< 1 mW MCUs) and lightweight LLMs (sub-1 GB memory target) as the two open frontiers of resource-constrained DL, with specific challenges (retraining-free pruning, ViT hardware support, diffusion-model compression).

## Limitations and Caveats

- **Primarily vision-focused** — the survey is anchored in computer vision (ImageNet, ViT, MobileNet). Speech/audio/NLP applications appear only via TinyML benchmarks (Google Speech Commands) and LLMs; acoustic-domain lightweight architectures (e.g., [[concepts/bc-resnet|BC-ResNet]], [[sources/cai-2024-tf-sepnet|TF-SepNet]]) are not surveyed.
- **Literature cutoff ~2023** — does not cover post-2023 developments in efficient LLMs (e.g., SSMs/Mamba, quantization schemes like AWQ/GPTQ adoption at scale, mobile LLM runtimes like MediaPipe LLM Inference API).
- **Hardware dataflow taxonomy is CNN-centric** — covers systolic arrays for convolutions but not attention-specific dataflows emerging for transformer accelerators.
- **Co-design section is conceptual** — cites specific accelerators (Cambricon-X/S, SCNN, Sparse-YOLO) but does not provide a unified benchmark or quantitative comparison across co-designed systems.
- **Quantization table (Table 5) is ResNet18-only** — does not cover transformer quantization, which has distinct challenges (homogeneous word embedding, varied weight distribution per Tao et al.).
- **No experimental validation** — as a survey, all recommendations are synthesized from cited works; the survey itself does not run new experiments to verify cross-method guidance.

## Related Concepts

- [[concepts/tinyml|TinyML]] — the sub-1 mW MCU frontier this survey frames as Future Direction 1
- [[concepts/neural-architecture-search|Neural Architecture Search]] — covered as a compression method with RL/EA/gradient/hardware-aware taxonomy
- [[concepts/lightweight-cnn-families|Lightweight CNN Families]] — the survey's "series" taxonomy (SqueezeNet/ShuffleNet/CondenseNet/MobileNet/Shift/Add)
- [[concepts/knowledge-distillation-paradigms|Knowledge Distillation Paradigms]] — the survey's offline/online/self-distillation taxonomy
- [[concepts/hardware-dataflow-types|Hardware Dataflow Types]] — the survey's four-type dataflow taxonomy (pipeline / DaDianNao / systolic-array / streaming)
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]] — foundational lightweight conv operation used by MobileNet/Xception
- [[concepts/post-training-quantization|Post-Training Quantization]] — covered in the quantization section
- [[concepts/quantization-aware-training|Quantization-Aware Training]] — covered in the quantization section
- [[concepts/attention-mechanism|Attention Mechanism]] — the basis for efficient transformers surveyed in §2.3
- [[concepts/patch-based-inference|Patch-based Inference]] — MCUNetV2's memory-saving strategy mentioned in the TinyML section
- [[concepts/keyword-spotting|Keyword Spotting]] — one of the TinyML benchmark tasks (Google Speech Commands)
- [[concepts/acoustic-scene-classification|Acoustic Scene Classification]] — relevant edge-AI audio task within TinyML scope

## Related Sources

- [[sources/lin-2023-tinyml-progress-futures|Lin et al. 2023: TinyML — Progress and Futures]] — complementary TinyML-focused survey; this Liu et al. 2024 survey cites MCUNet/MCUNetV2/MCUNetV3 and frames TinyML as a future direction, while Lin et al. 2023 provides the deeper TinyML system co-design treatment
- [[sources/lin-2020-mcunet|Lin et al. 2020: MCUNet]] — cited as a TinyML milestone (first > 70% ImageNet on commercial MCU)
- [[sources/lin-2021-mcunetv2|Lin et al. 2021: MCUNetV2]] — cited for patch-based inference

## Related Synthesis

- [[synthesis/computational-efficiency-evolution|Computational Efficiency in ANC: From O(N²) to GPU-Accelerated DSP]] — adjacent synthesis on efficiency evolution; this survey broadens the lens beyond ANC/speech to general DL deployment
