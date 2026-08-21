---
type: concept
created: 2026-08-21
updated: 2026-08-21
sources:
  - raw/papers/bai-2026-feedback-guided-anc/full-text.md
tags:
  - active-noise-control
  - fixed-parameter-anc
  - deep-learning
  - mixture-of-experts
  - feedback-control
---

# Feedback-guided Controller Fusion

**Feedback-guided Controller Fusion** is a fixed-parameter active noise control (ANC) framework introduced by Bai et al. (2026) that dynamically fuses a causal WaveNet baseline controller with multiple pre-trained FIR filter experts according to the current acoustic condition. The distinguishing feature — vs. prior [[selective-fixed-filter-anc|SFANC]] and [[generative-fixed-filter-anc|GFANC]] frameworks — is that the gating network consumes the **control and delayed residual-error signals** in addition to the reference signal, so the fusion reflects the *actual control outcome* under the current acoustic system rather than only the input-noise characteristics.

## Overview

Conventional fixed-parameter DNN-based ANC controllers train one set of parameters shared across all conditions; their performance degrades on out-of-distribution paths. SFANC/GFANC select or generate control filters from **reference-side features** alone, which characterize input noise but not the actual control outcome — limiting their response to acoustic-path mismatch. Feedback-guided controller fusion closes this loop by:

1. Combining a feedforward WaveNet branch (a stable, condition-averaged baseline) with a feedback-guided mixture-of-experts (MoE) branch (a path-specific correction).
2. Driving the MoE gating network with $\mathbf{x}(n)$, $\mathbf{y}(n)$, and $\mathbf{e}(n-1)$ — the residual-error signal is delayed by one sample because $\mathbf{e}(n)$ becomes available only after $\mathbf{y}(n)$ propagates through the secondary path.

The final anti-noise signal is the fusion of the two branches:

$$
\mathbf{y}(n) = \alpha\, \mathbf{y}_{\mathrm{W}}(n) + (1-\alpha)\, \mathbf{y}_{\mathrm{M}}(n),
$$

where $\alpha$ is a fusion coefficient, $\mathbf{y}_{\mathrm{W}}(n)$ is the WaveNet output, and $\mathbf{y}_{\mathrm{M}}(n)$ is the MoE output. The two branches provide complementary advantages: the WaveNet branch stabilizes high-frequency behavior, while the MoE branch substantially improves low-frequency noise reduction on path outliers.

## Key Formulations

### MoE Controller

The MoE branch fuses $N$ pre-trained FIR filter experts (one per acoustic path):

$$
\mathbf{w}_{\mathrm{M}}(n) = \sum_{i=1}^{N} \beta_i(n-1)\, \mathbf{w}_i, \qquad \mathbf{y}_{\mathrm{M}}(n) = \mathbf{w}_{\mathrm{M}}(n) * \mathbf{x}(n),
$$

where $\beta_i(n-1)$ are fusion weights estimated at the previous sampling point — using the previous point's weights to generate the current control signal guarantees **causality** (no current output depends on gating weights computed from that same output).

### Gating Network

Inputs: $\mathbf{x}(n)$, $\mathbf{y}(n)$, $\mathbf{e}(n-1)$, concatenated along the channel dimension. Two parallel feature-extraction branches:

- **Temporal branch**: three cascaded Conv1d blocks (Conv1d → Layer Norm → SiLU) followed by a temporal mean for global temporal representation.
- **Statistical branch**: log-RMS features capturing amplitude statistics.

Outputs are concatenated and passed through an MLP (two linear layers + SiLU) followed by Softmax to produce fusion weights $\beta$.

The 1-sample misalignment of the error signal vs. reference/control signals has negligible impact on performance (verified experimentally by Bai 2026).

### Filter Experts

Each FIR filter expert is implemented as a Conv1d layer with kernel size 2048 — equivalent to a 2048-tap FIR filter without coefficient flipping. Coefficients are dynamically weighted by $\beta$ to form the MoE controller.

## Staged Training

1. **WaveNet pre-training** (180 epochs) on all training conditions, providing an averaged optimal baseline.
2. **FIR expert pre-training** (180 epochs per expert), one expert per acoustic path. Stages 1 and 2 can run in parallel.
3. **Gating network training** (100 epochs) with WaveNet and FIR experts frozen. The objective combines the [[frequency-aware-anc-loss|frequency-aware ANC loss]] with a cross-entropy auxiliary loss supervised by acoustic-path labels (label-smoothing 0.05):

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{ANC}} + \gamma\, \mathcal{L}_{\mathrm{cls}}.
$$

$\mathcal{L}_{\mathrm{cls}}$ establishes the correspondence between acoustic paths and their associated FIR experts, while $\mathcal{L}_{\mathrm{ANC}}$ refines the soft fusion weights according to the resulting ANC performance.

## Streaming and Peak-MAC Optimization

The model is fully causal and supports sample-wise streaming inference. A peak-MAC optimization for the 10-expert model reduces the peak MAC per sample from 34.62k to 14.15k by distributing the cost evenly across sampling points, while keeping total complexity essentially unchanged (672.93 MMac/s vs. 672.83 MMac/s for the 8-expert model).

## Empirical Behavior (Bai 2026, CCF-AATC Headphone ANC)

| Property | WaveNet-only | MoE-only | Hybrid (proposed) |
|----------|--------------|----------|-------------------|
| Low-frequency NR (path 7 outlier) | Fails (~0 dB) | Substantially improved | Substantially improved |
| High-frequency amplification (path 6) | Lower | Slightly higher | Lower (mitigated) |
| Unseen-path robustness | Limited | — | Superior on both unseen paths |

The 10-expert streaming model achieves **19.00 dB average noise reduction from 50 Hz to 5 kHz** with **negligible amplification over 1–8 kHz**, switching stable across condition changes without convergence time.

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]] — parent domain
- [[concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]] (SFANC) — predecessor; reference-side feature selection
- [[concepts/generative-fixed-filter-anc|Generative Fixed-Filter ANC]] (GFANC) — predecessor; reference-side feature generation
- [[concepts/frequency-aware-anc-loss|Frequency-aware ANC Loss]] — co-introduced training objective
- [[concepts/hybrid-anc|Hybrid ANC]] — architectural pattern (feedforward WaveNet + feedback-guided MoE)
- [[concepts/feedforward-anc|Feedforward ANC]] — branch topology
- [[concepts/feedback-anc|Feedback ANC]] — error-signal feedback principle (delayed by 1 sample here)
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — adaptive alternative (online updates vs. offline fixed-parameter)

## Related Sources

- [[sources/bai-2026-feedback-guided-anc|Bai et al. 2026: Feedback-guided DNN-based Controller Fusion for Robust Fixed-Parameter ANC]] — introduces the framework
