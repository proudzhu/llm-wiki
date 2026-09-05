---
type: concept
created: 2026-05-04
updated: 2026-09-05
sources:
  - raw/papers/yang-2026-transformer-e2e-cfg-anc/full-text.md
  - raw/papers/luo-2026-hybrid-gfanc-fxnlms/full-text.md
  - raw/papers/jiang-2025-ai-driven-avnc-review/full-text.md
  - raw/papers/bai-2026-feedback-guided-anc/full-text.md
  - raw/papers/he-2026-neural-projection-filter-anc/full-text.md
tags:
  - active-noise-control
  - fixed-filter-anc
  - deep-learning
  - generative-model
---

# Generative Fixed-Filter ANC

**Generative Fixed-Filter ANC (GFANC)** is an ANC strategy that uses a neural network co-processor to generate custom control filters in real time, rather than selecting from a pre-trained discrete library as in [[selective-fixed-filter-anc|SFANC]]. The generated filter is a combination of sub-control filters weighted by the co-processor's output.

## Overview

SFANC selects one filter from a discrete library, which may be insufficient when the incoming noise differs substantially from the design conditions. GFANC addresses this by generating a more suitable control filter through **sub-filter decomposition and recombination**:

1. A wideband pre-trained control filter is partitioned into $M$ sub-filters (e.g., via uniform frequency-domain partitioning)
2. A CNN co-processor processes the reference signal and predicts $M$ combination weights
3. The final control filter is the weighted sum of sub-filters: $\mathbf{w} = \sum_{m=1}^{M} g_m \mathbf{w}_m$

This enables finer-grained adaptation than discrete selection while maintaining the instant-response advantage of fixed-filter ANC.

## Evolution of GFANC

### Supervised GFANC (Luo et al. 2024)
The original GFANC framework trains the co-processor in a **supervised** manner, requiring labeled target filters. Temporal smoothing via Bayesian or Kalman filtering enhances robustness under dynamic noise conditions.

### Unsupervised GFANC (Luo et al. 2024, ICASSP)
Integrates the co-processor and real-time controller into a **differentiable ANC system**. The accumulated squared error serves directly as the training objective, eliminating the need for labeled data while remaining aligned with the physical objective of noise cancellation.

### End-to-End CFG (E2E-CFG) (Yang et al. 2026)
Replaces the decomposition-recombination paradigm with **direct control-filter generation**. A Transformer-based co-processor outputs the full $N$-dimensional filter coefficient vector, removing dependence on intermediate sub-filter representations. Trained unsupervised using the same differentiable ANC framework.

### Feedback-Guided Fusion of Pre-Trained Experts (Bai 2026)
[[feedback-guided-controller-fusion|Bai et al. 2026]] extend the "weighted combination of pre-trained filters" idea along a different axis: rather than generating combination weights from reference-side features (GFANC) or learned sub-filter bases (E2E-CFG), they pre-train one FIR expert **per acoustic path** and fuse them with weights produced by a gating network that consumes reference + control + **delayed residual-error** signals. The feedback path closes the loop on the actual acoustic condition, addressing the path-mismatch robustness gap that reference-side-only GFANC leaves open. The result is a hybrid WaveNet + MoE controller that achieves 19.00 dB average NR (50 Hz–5 kHz) on the CCF-AATC headphone ANC dataset with negligible 1–8 kHz amplification, while being lighter (28.57k params / 672.83 MMac/s for 8 experts) than the CCF 2026 official baseline (42.76k / 2.04 GMac/s).

### Filter Generation on the Reference Path (He 2026)

[[concepts/condition-aware-projection-filtering|CAPF]] (He et al. 2026) applies the neural-filter-generation idea to a different stage: instead of generating the *control* filter, CAPFNet generates **projection filters** that compress many correlated references into a few decorrelated projected references for a conventional adaptive controller. This keeps the control loop fully adaptive (unlike fixed-filter GFANC variants) while confining neural inference to block rate — 48× cheaper online than point-wise neural reference projection.

## Comparison: SFANC vs. GFANC vs. E2E-CFG

| Aspect | SFANC | GFANC | E2E-CFG |
|--------|-------|-------|---------|
| Filter source | Pre-trained library | Generated from sub-filters | Directly generated |
| Output | Index selection | $M$ combination weights | $N$ filter coefficients |
| Adaptation granularity | Discrete | Continuous (weighted sum) | Continuous (full filter) |
| Error accumulation | No | Yes (through recombination) | No |
| Training | Classification | Supervised / Unsupervised | Unsupervised |
| Co-processor | CNN classifier | CNN weight predictor | Transformer filter generator |

## Key Formulations

### Sub-filter recombination (GFANC)
$$\mathbf{w} = \sum_{m=1}^{M} g_m \mathbf{w}_m, \quad g_m = \sigma(\text{CNN}(\mathbf{x}_f))_m$$

### Direct filter generation (E2E-CFG)
$$\mathbf{w} = \mathcal{F}_\theta(\mathbf{x}_f) \in \mathbb{R}^N$$

### Unsupervised training objective
$$\mathcal{L} = \frac{1}{T} \sum_{n=0}^{T-1} \alpha_n e^2(n)$$

where $\alpha_n$ follows a forgetting-factor scheme ($\lambda = 0.999$).

## Related Concepts

- [[concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]] — predecessor: discrete filter selection
- [[concepts/active-noise-control|Active Noise Control]] — parent domain
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — adaptive alternative
- [[concepts/end-to-end-differentiable-anc|End-to-End Differentiable ANC]] — training paradigm for unsupervised GFANC and E2E-CFG
- [[concepts/feedback-guided-controller-fusion|Feedback-guided Controller Fusion]] — extension that fuses per-path pre-trained FIR experts using residual-error feedback
- [[concepts/condition-aware-projection-filtering|Condition-Aware Projection Filtering (CAPF)]] — neural filter generation applied to the reference (projection) path rather than the control path

## Related Sources

- [[sources/yang-2026-transformer-e2e-cfg-anc|Yang 2026: Transformer-based E2E-CFG for ANC]] — direct filter generation with Transformer co-processor
- [[sources/luo-2026-hybrid-gfanc-fxnlms|Luo 2026: Hybrid GFANC-FxNLMS]] — unsupervised GFANC with CNN co-processor and hybrid stabilization
- [[sources/jiang-2025-ai-driven-avnc-review|Jiang et al. 2025: AI-Driven AVNC Review]] — reviews GFANC as a key end-to-end controller modeling approach
- [[sources/bai-2026-feedback-guided-anc|Bai 2026: Feedback-guided DNN-based Controller Fusion for Robust Fixed-Parameter ANC]] — fuses per-path pre-trained FIR experts with residual-error feedback, addressing GFANC's path-mismatch robustness gap
- [[sources/he-2026-neural-projection-filter-anc|He et al. 2026: Neural Projection Filter Generation for Multi-Reference ANC]] — block-wise neural generation of reference-projection filters (CAPF), the reference-path analog of filter generation
