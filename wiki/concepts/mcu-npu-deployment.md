---
type: concept
created: 2026-11-07
updated: 2026-11-07
sources:
  - raw/papers/laroche-2026-lisenet-embedded/full-text.md
tags:
  - npu-deployment
  - embedded-systems
  - int8-quantization
  - tinyml
  - streaming-inference
  - speech-enhancement
---

# MCU NPU Deployment

**MCU NPU deployment** is the practice of executing neural-network inference on the neural processing units (NPUs) integrated into microcontrollers — e.g., Arm Ethos-U, STMicroelectronics' **Neural-ART** (STM32N6). Unlike CPU/DSP targets, commercial MCU NPUs expose a **compiler-controlled set of predominantly static, integer-quantized convolutional operators** whose tensor dimensions are fixed at compile time. This operator restriction, not raw compute, is the binding constraint — a pattern instantiated for speech enhancement by [[sources/laroche-2026-lisenet-embedded|Laroche & Olsson 2026]].

## The Operator Compatibility Gap

A model compact by conventional measures (parameters, MACs) may still fail to deploy:

1. **Recurrent layers** (GRU/LSTM) — cannot be imported as supported operators; unrolling along an axis explodes the graph (LiSenNet's frequency Bi-GRU: ~850 tensor-slicing operations; the compiler stalls). The *temporal* GRU is deployable via the hidden-state-as-graph-I/O trick with dense affine transforms, but only at reduced throughput;
2. **Runtime normalization** (LayerNorm over dynamic extents) — unsupported; per-channel BatchNorm folded into the preceding convolution is the compatible substitute;
3. **Exotic activations** (PReLU, Mish) — not in the int8 operator set; ReLU6 substitutes and bounds activation ranges;
4. **Dynamic/reshaped tensors** (rank-5 reshape-based sub-pixel upsampling) — unsupported; transposed convolutions substitute.

Unsupported operations do not merely slow things down — they are **assigned to the integrated CPU host** (e.g., Cortex-M55), and for small streaming networks the host execution, data transfers, and scheduling overheads dominate the cost of the supported arithmetic.

## Co-Design Requirements

[[sources/laroche-2026-lisenet-embedded|Laroche & Olsson 2026]] distill four jointly necessary ingredients (their STM32N6 results):

1. **Supported operators** — architecture reformulation, not just compression or PTQ (their headline: model size alone does not predict deployed quality or execution time);
2. **Controlled activation ranges** — bounded activations ([[concepts/relu6-quantization-robustness|ReLU6]]) keep static int8 quantization loss small (0.01 vs. 0.08 PESQ);
3. **Explicit streaming state** — FIFO state buffers between frames ([[concepts/stateful-streaming-inference|stateful streaming inference]]); stateless receptive-field recomputation is an order of magnitude slower and misses real-time deadlines;
4. **Measurement of the complete compiled graph** — execution-epoch assignments and host–NPU partitioning taken from the compiler report and verified with the on-device per-epoch profiler.

Contrast with [[concepts/tinyml|TinyML]] on CPU-class MCUs (CMSIS-NN etc.), where memory (SRAM/Flash) is the binding constraint and any operator expressible in the library is available; and with the hardware-aware SE line (TinyLSTMs, sparsity studies, mixed-precision RNNs on programmable multicore MCUs) that targets processors explicitly supporting recurrent or sparse computation.

## Related Concepts

- [[concepts/stateful-streaming-inference|Stateful Streaming Inference]]
- [[concepts/post-training-quantization|Post-Training Quantization]]
- [[concepts/relu6-quantization-robustness|ReLU6 Quantization Robustness]]
- [[concepts/lisennet-npu|LiSenNet-NPU]]
- [[concepts/tinyml|TinyML]]

## Related Sources

- [[sources/laroche-2026-lisenet-embedded|Laroche & Olsson 2026: Beyond Model Size — Redesigning LiSenNet for Embedded Speech Enhancement]]
- [[sources/le-2026-efficient-nn-tinyml-review|Lê, Wolinski & Arbel 2026: Efficient NNs for TinyML]] — surveys the broader MCU quantization landscape
