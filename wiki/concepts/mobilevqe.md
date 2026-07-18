---
type: concept
created: 2026-07-18
updated: 2026-07-18
sources:
  - raw/papers/castelli-2025-embedded-joint-aec-ns/full-text.md
tags:
  - deep-learning
  - speech-enhancement
  - acoustic-echo-cancellation
  - neural-networks
  - embedded
  - low-complexity
---

# MobileVQE

**MobileVQE** is an intermediate deployment-stage variant of the [[sources/indenbom-2023-deepvqe\|DeepVQE]] joint AEC+NS architecture, introduced by [[entities/francesco-castelli\|Francesco Castelli]] (NXP) at tinyML Summit 2024 as the first step in compressing DeepVQE-s onto an NXP i.MX 8M Plus / i.MX RT600 embedded target. MobileVQE trades negligible AEC-MOS for a roughly 7.7× reduction in MACs/frame by replacing standard 2-D convolutions with depthwise separable convolutions and removing the decoder's residual blocks.

## Architecture Changes vs. DeepVQE-s

1. **Conv2d → Depthwise Separable Conv2d** throughout the encoder/decoder — the standard efficiency substitution that factorizes a $c_{out} \times c_{in} \times k_t \times k_f$ convolution into a depthwise $c_{in} \times 1 \times k_t \times k_f$ followed by a pointwise $c_{out} \times c_{in} \times 1 \times 1$.
2. **No decoder residual blocks** — Castelli drops the residual blocks in the decoder, simplifying the upsampling path.
3. **Cross-attention frame delay reduced** from $d = 1$ s (DeepVQE-s) to $d = 0.5$ s.

The [[concepts/cross-attention-alignment\|alignment block]], GRU bottleneck, [[concepts/complex-convolving-mask\|CCM]] output block, and the overall encoder-decoder topology are preserved.

## Performance

On NXP's re-trained AEC-MOS / DNS-MOS evaluation:

| Model | Params (k) | MACs (M) | FST Echo | DT Echo | DT Deg | Sig | Bak | Ovrl |
|-------|-----------:|---------:|---------:|--------:|-------:|----:|----:|-----:|
| DeepVQE-s (ours) | 610 | 10.28 | 4.67 | 4.61 | 4.07 | 3.54 | 4.08 | 3.28 |
| **MobileVQE** | **635** | **1.34** | 4.68 | 4.49 | 3.95 | 3.39 | 3.95 | 3.11 |

MobileVQE preserves FST echo cancellation (4.68, marginally better than DeepVQE-s) at the cost of small losses in DT echo (−0.12), DNS-MOS Sig (−0.15), and DNS-MOS Bak (−0.13). The MACs reduction (10.28 → 1.34 MMACs) is the largest single-stage reduction in the [[sources/castelli-2025-embedded-joint-aec-ns\|Castelli 2024]] optimization pipeline.

## Position in the Optimization Pipeline

MobileVQE is Stage 1 of a six-stage compression pipeline that culminates in [[concepts/tinyvqe\|TinyVQE]]:

| Stage | Model | Params | MACs |
|-------|-------|-------:|-----:|
| 0 | DeepVQE-s (ours) | 610k | 10.28 M |
| **1** | **MobileVQE** | **635k** | **1.34 M** |
| 2 | Cut parameters | 147k | 0.86 M |
| 3 | Custom CCM impls | 147k | 0.86 M |
| 4 | ELU → ReLU | 147k | 0.86 M |
| 5 | Cut MACs | 139k | 0.54 M |
| 6 | [[concepts/tinyvqe\|TinyVQE]] | 114k | 0.48 M |

Notably MobileVQE has **more** parameters than DeepVQE-s (635k vs. 610k) — the depthwise-separable substitution does not produce a smaller model in absolute terms at this width, but it produces a much smaller MAC count, which is the binding constraint for HiFi4 DSP real-time execution.

## Related Concepts

- [[concepts/tinyvqe\|TinyVQE]]
- [[concepts/complex-convolving-mask\|Complex Convolving Mask]]
- [[concepts/cross-attention-alignment\|Cross-Attention Alignment]]
- [[concepts/depthwise-separable-convolution\|Depthwise Separable Convolution]]
- [[concepts/acoustic-echo-cancellation\|Acoustic Echo Cancellation]]

## Related Sources

- [[sources/castelli-2025-embedded-joint-aec-ns\|Castelli 2024: Embedded Joint AEC and NS]] — introduces MobileVQE as Stage 1
- [[sources/indenbom-2023-deepvqe\|Indenbom et al. 2023: DeepVQE]] — MobileVQE is a depthwise-separable-conv + no-decoder-residual variant of DeepVQE-s
