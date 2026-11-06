---
type: entity
created: 2026-11-07
updated: 2026-11-07
tags:
  - researcher
  - speech-enhancement
  - efficiency
  - quantization
---

# Gyeongmin Kim

**Affiliation**: Department of Computer Science, Hanyang University, Seoul, Korea
**Role**: Researcher (sole author)
**Research Focus**: Deployment efficiency for streaming speech enhancement — int8 quantization, SIMD kernel specialization, and energy-aware benchmarking of neural speech enhancers on commodity CPUs.

## Key Contributions

- Sole author of "faster-enhancer.c: A Dependency-Free int8 Runtime for Streaming Speech Enhancement on Commodity CPUs" (arXiv 2026) — [[sources/kim-2026-faster-enhancer|Kim 2026]] — ported FastEnhancer-Medium at 48 kHz to a dependency-free C runtime with six int8 GEMM tiers (3.3× faster than the fp32 ONNX graph on an Apple M2, tracking it to −0.006 PESQ), and introduced the racing-vs-pacing benchmarking protocol showing deadline pacing saves 49% of the energy at 4.2× per-frame cost.

## Related Sources

- [[sources/kim-2026-faster-enhancer|Kim 2026: faster-enhancer.c — A Dependency-Free int8 Runtime for Streaming Speech Enhancement on Commodity CPUs]]
