---
type: concept
created: 2026-11-07
updated: 2026-11-07
sources:
  - raw/papers/laroche-2026-lisenet-embedded/full-text.md
tags:
  - speech-enhancement
  - lightweight-model
  - npu-deployment
  - int8-quantization
  - real-time
  - streaming-inference
---

# LiSenNet-NPU

**LiSenNet-NPU** is the NPU-compatible redesign of [[concepts/lisennet|LiSenNet]] proposed by [[sources/laroche-2026-lisenet-embedded|Laroche & Olsson 2026]] for the STMicroelectronics STM32N6 microcontroller's Neural-ART accelerator. It preserves LiSenNet's sub-band encoder, progressive frequency reduction, U-Net skip connections, and mask decoder, while replacing every operator the restricted NPU cannot execute as a static int8 graph.

## Architecture Changes vs. LiSenNet

| Component | LiSenNet (Yan et al. 2025) | LiSenNet-NPU (Laroche & Olsson 2026) | Reason |
|---|---|---|---|
| Frequency mixer | Bi-GRU over 32 frequency bins | [[concepts/depthwise-separable-convolution\|Depthwise-separable]] conv (kernel 11) + pointwise conv | GRU unrolling needs ~850 tensor-slice ops and stalls the compiler; conv maps to NPU primitives |
| Temporal mixer | Unidirectional GRU | Causal [[concepts/stateful-streaming-inference\|dilated TCN]] with gating (3 DPC blocks, dilations up to 16, RF 196 frames) | FIFO state flushes quantization errors; avoids recurrent-state drift |
| Normalization | Multi-dim LayerNorm | Per-channel BatchNorm, folded into the preceding conv | Runtime normalization unsupported |
| Activations | PReLU / Mish | ReLU6 (incl. bounded "lim-ReLU6" decoder) | Supported int8 op; bounded range aids quantization |
| Upsampling | Reshape-based sub-pixel conv | 1×3 transposed conv, stride 3 (frequency axis) | Avoids rank-5 tensors; ~3× less decoder arithmetic |
| Bottleneck width | — | C = 24 (from {20, 24, 28}) | Non-monotonic quality/width relation |

## Performance

On VoiceBank-DEMAND: FP32 PESQ **3.08**, int8 PESQ **3.01** — versus the reproduced recurrent LiSenNet's 3.01 / 2.93. The quantization loss drops from 0.08 to 0.01 PESQ. Deployed on the STM32N6 (Neural-ART @ 1 GHz): **4.83 ms per 16 ms frame (RTF 0.30)**, 46.2k parameters, 1.66 M MACs/frame, 45 KiB int8 weights, 154 KiB FIFO state over 25 tensors. It beats both literature baselines on the same board on quality *and* speed: Conv-FSENet (1.45M params, PESQ 2.91, 4.40 ms) and dense NSNet2 (2.78M, 2.83, 22.94 ms — not real-time).

The temporal-GRU hybrid variant (conv frequency mixer + GRU temporal mixer, state as graph I/O) is even faster — 2.18 ms/frame, 17 KiB state — at int8 PESQ 2.98, making recurrence an efficient alternative when state memory and latency outweigh drift and quantization risks.

## Significance

The paper's title claim — "beyond model size" — is quantified by LiSenNet-NPU: parameter and MAC counts do not predict deployed quality or execution time on restricted NPUs. Operator compatibility, quantization range, and persistent streaming state must be co-designed with the architecture. See [[concepts/mcu-npu-deployment|MCU NPU Deployment]] for the general pattern and [[synthesis/computational-efficiency-evolution|Computational Efficiency Evolution]] for its place in the efficiency-frontier discussion.

## Related Concepts

- [[concepts/lisennet|LiSenNet]]
- [[concepts/mcu-npu-deployment|MCU NPU Deployment]]
- [[concepts/stateful-streaming-inference|Stateful Streaming Inference]]
- [[concepts/relu6-quantization-robustness|ReLU6 Quantization Robustness]]
- [[concepts/post-training-quantization|Post-Training Quantization]]
- [[concepts/depthwise-separable-convolution|Depthwise-Separable Convolution]]

## Related Sources

- [[sources/laroche-2026-lisenet-embedded|Laroche & Olsson 2026: Beyond Model Size — Redesigning LiSenNet for Embedded Speech Enhancement]]
- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]] — the original architecture
