---
type: concept
created: 2026-11-07
updated: 2026-11-07
sources:
  - raw/papers/laroche-2026-lisenet-embedded/full-text.md
tags:
  - streaming-inference
  - real-time
  - embedded-systems
  - speech-enhancement
  - npu-deployment
---

# Stateful Streaming Inference

**Stateful streaming inference** is frame-by-frame inference in which intermediate activations are kept in explicit **FIFO state buffers** between frames, so that each new output frame only requires computing on the current input frame — the temporal history lives in persistent state, not in re-read input context. It is contrasted with **stateless receptive-field recomputation**, where the full receptive field of input frames is re-fed and recomputed for every output frame.

## The Stateful vs. Stateless Gap

[[sources/laroche-2026-lisenet-embedded|Laroche & Olsson 2026]] quantify the gap on an STM32N6 NPU for a dilated-TCN speech enhancer (their Table 3):

| Variant | MACs/frame | ms/frame | Meets 16 ms deadline? |
|---|---|---|---|
| C=20 model, FIFO state | 0.92 M | 2.59 | ✅ |
| C=20 model, stateless | 66.55 M | 29.93 | ❌ |
| Deep model (RF 196), FIFO state | 1.69 M | 4.88 | ✅ |
| Deep model (RF 196), stateless | 336.31 M | 127.16 | ❌ |

Stateless recomputation is an order of magnitude (here ~72× MACs) slower at the same frame rate **despite higher accelerator utilization** — a striking demonstration that redundant arithmetic, not efficiency of each op, dominates. No stateless variant meets the 16 ms real-time deadline.

## The Cost Side: State Is Memory

Streaming moves cost from compute to memory management. The final LiSenNet-NPU stores **154 KiB across 25 FIFO tensors — more than 3× its 45 KiB of int8 weights**. This inverts the usual weights-dominate picture of model size and is the concrete meaning of "persistent streaming state" as a co-design dimension.

## Recurrent vs. Convolutional State

Two ways to carry temporal state, compared on the same board and flow (Laroche & Olsson 2026):

- **Convolutional FIFO state** (dilated TCN): fixed number of frames; any quantization error is eventually **flushed out of the receptive field**; 154 KiB / 25 tensors; 4.83 ms/frame; int8 PESQ 3.01.
- **Recurrent state** (GRU with hidden state as graph input/output): compact (17 KiB / 13 tensors), faster (2.18 ms/frame), but risks internal-state **drift** during long-duration streaming and **accumulating quantization error** in the state; int8 PESQ 2.98.

The trade-off: recurrence is efficient when state memory and latency outweigh drift/quantization risk; convolutional FIFO state buys robustness at memory cost. Related quantization evidence: [[sources/kim-2026-faster-enhancer|Kim 2026]] shows GRU state kept in fp16 quantizes cleanly — the sensitive quantity is *state precision*, not gate arithmetic.

## Related Concepts

- [[concepts/mcu-npu-deployment|MCU NPU Deployment]]
- [[concepts/lisennet-npu|LiSenNet-NPU]]
- [[concepts/post-training-quantization|Post-Training Quantization]]
- [[concepts/fifo-queue|FIFO Queue]]
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit (GRU)]]

## Related Sources

- [[sources/laroche-2026-lisenet-embedded|Laroche & Olsson 2026: Beyond Model Size — Redesigning LiSenNet for Embedded Speech Enhancement]]
- [[sources/kim-2026-faster-enhancer|Kim 2026: faster-enhancer.c]] — fp16-state GRU quantization, the complementary recurrent-side evidence
