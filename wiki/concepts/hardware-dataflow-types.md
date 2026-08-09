---
type: concept
created: 2026-08-09
updated: 2026-08-09
sources:
  - raw/papers/liu-2024-lightweight-dl-survey/full-text.md
tags:
  - hardware-acceleration
  - dataflow
  - fpga
  - asic
  - efficient-deep-learning
  - taxonomy
---

# Hardware Dataflow Types

**Hardware Dataflow Types** is a four-way taxonomy of how data flows through Processing Elements (PEs) in hardware accelerators for deep learning, as organized by [[sources/liu-2024-lightweight-dl-survey|Liu et al. 2024]]. The taxonomy captures the design trade-off between parallelism, energy efficiency, hardware utilization, and mapping complexity — and is central to choosing the right accelerator architecture for a given DL workload.

## Background: Why Dataflow Matters

CNNs are computationally intensive and data-hungry. Three memory tiers constrain performance:

1. **Off-chip memory (DRAM)** — stores the model; high capacity, high energy per access.
2. **On-chip buffer (SRAM)** — caches weights/activations; limited capacity.
3. **PE-local register file** — fastest access; smallest capacity.

Dataflow determines **when and where** each portion of the input feature map, weights, and partial sums are accessed and stored. A well-designed dataflow maximizes data reuse and minimizes DRAM traffic — the dominant energy cost. The general flow is: model stored in DRAM → weights/activations fetched to SRAM → PEs execute MACs → partial sums accumulated.

## The Four Dataflow Types

### 1. Pipeline-Like Dataflow

- **Structure**: input pixels flow through individual PEs; weights fixed on each PE; partial sums forwarded to the subsequent PE.
- **Strengths**: substantial parallelism — multiple stages process data concurrently.
- **Limitations**: sequential execution within a single sample (each stage depends on the previous one); increased latency.

### 2. DaDianNao-Like Dataflow

- **Structure**: each PE functions like a neuron — input pixels routed to each PE, weights embedded within each PE, partial sums aggregated by an adder tree.
- **Strengths**: accommodates different kernel sizes; handles intricate/irregular model structures.
- **Limitations**: energy-intensive; demands substantial hardware resources due to model complexity.

### 3. Systolic-Array-Like Dataflow

- **Structure**: input pixels and weights cascade sequentially through PE chains; an adder tree aggregates partial sums.
- **Strengths**: optimized hardware utilization; improved overall hardware efficiency; mitigates timing issues in large designs. This is the dataflow used by Google's TPU.
- **Limitations**: finding an appropriate mapping for CNNs onto a systolic array is challenging.

### 4. Streaming-Like Dataflow

- **Structure**: input pixels continuously sent to the next PE without pausing or intermediate storage; weights fixed on each PE; adder tree accumulates partial sums.
- **Strengths**: high throughput and low latency; particularly suitable for streaming data such as audio and video processing.
- **Limitations**: applications requiring complex inter-stage operations or reliance on previous results need additional processing/design.

## Data Locality Optimization (Cross-Cutting)

Independent of the dataflow type, three loop-transformation techniques optimize data locality:

- **Loop unrolling**: expands iterations into sequential instructions → faster CNN operations, better hardware utilization, but code bloat and higher memory usage.
- **Loop tiling**: partitions input data into smaller blocks for sequential processing → mitigates buffer constraints, enhances cache locality; minimal gain on GPUs (already optimized).
- **Loop interchange**: reorders nested loops so each outer iteration reuses the same cache line → reduces memory access; risky if algorithms have intrinsic loop-order semantics.

## Practical Implications

- **Streaming data (audio, video)** → streaming-like dataflow.
- **Irregular model structures** → DaDianNao-like dataflow (at the cost of energy).
- **Maximum hardware utilization** → systolic-array-like dataflow (TPU-style).
- **Pipeline-parallel workloads** → pipeline-like dataflow.

## Limitations of the Taxonomy

The taxonomy is **CNN-centric** — it covers dataflows optimized for convolution workloads but does not address attention-specific dataflows emerging for transformer accelerators (e.g., sparse attention patterns, key-value cache reuse strategies). As noted in [[sources/liu-2024-lightweight-dl-survey|Liu et al. 2024]]'s Limitations section, hardware support for ViT-specific operators (MatMul, LayerNorm) on resource-constrained devices remains an open challenge.

## Related Concepts

- [[concepts/tinyml|TinyML]] — the extreme end of hardware-constrained deployment where dataflow choice is critical
- [[concepts/lightweight-cnn-families|Lightweight CNN Families]] — the architectures these dataflows are designed to accelerate
- [[concepts/neural-architecture-search|Neural Architecture Search]] — hardware-aware NAS variants co-optimize the architecture against the target dataflow

## Related Sources

- [[sources/liu-2024-lightweight-dl-survey|Liu et al. 2024: Lightweight Deep Learning for Resource-Constrained Environments]] — introduces the four-type dataflow taxonomy (Figure 10)
