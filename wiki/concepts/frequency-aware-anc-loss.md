---
type: concept
created: 2026-08-21
updated: 2026-08-21
sources:
  - raw/papers/bai-2026-feedback-guided-anc/full-text.md
tags:
  - active-noise-control
  - loss-function
  - deep-learning
  - frequency-domain
---

# Frequency-aware ANC Loss

The **frequency-aware ANC loss** is a training objective for deep-learning-based active noise control (ANC) introduced by Bai et al. (2026). It combines three terms computed via one-third-octave-band analysis to jointly promote low-frequency noise reduction and suppress high-frequency amplification ("rebound"), while constraining overall residual energy.

## Definition

The frequency-aware ANC objective is

$$
\mathcal{L}_{\mathrm{ANC}} = \mathcal{L}_{\mathrm{NR}} + \lambda\, \mathcal{L}_{\mathrm{RB}} + \mathcal{L}_{\mathrm{NMSE}},
$$

where:

- **$\mathcal{L}_{\mathrm{NR}}$** — the negative of the equally-weighted mean noise reduction over **50 Hz–5 kHz**. Promotes broadband low/mid-frequency attenuation.
- **$\mathcal{L}_{\mathrm{RB}}$** — the **rebound** metric: the largest noise amplification over **1 kHz–8 kHz**, set to zero when no band is amplified. For a more conservative constraint, the upper frequency is extended to **16 kHz**. Suppresses waterbed-type amplification at high frequencies where ANC performance is fundamentally limited.
- **$\mathcal{L}_{\mathrm{NMSE}}$** — broadband normalized mean-square error:

$$
\mathcal{L}_{\mathrm{NMSE}} = 10 \log_{10}\!\left( \frac{\sum_n e^2(n)}{\sum_n d^2(n)} \right),
$$

constraining the overall residual energy.

$\lambda$ is a weighting coefficient that balances noise reduction against rebound suppression.

## Spectral Computation

All spectral terms use an **8192-point STFT with a Hann window and a hop size of 2048**. The disturbance $\mathbf{d}$ and residual $\mathbf{e}$ are converted to one-third-octave bands for $\mathcal{L}_{\mathrm{NR}}$ and $\mathcal{L}_{\mathrm{RB}}$.

## Role in the Feedback-guided Controller Fusion Pipeline

The loss is used in stages 1 and 3 of the [[feedback-guided-controller-fusion|feedback-guided controller fusion]] training:

1. **WaveNet pre-training** (180 epochs) — uses $\mathcal{L}_{\mathrm{ANC}}$ alone.
3. **Gating network training** (100 epochs) — combines $\mathcal{L}_{\mathrm{ANC}}$ with a cross-entropy path-classification auxiliary loss:

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{ANC}} + \gamma\, \mathcal{L}_{\mathrm{cls}}.
$$

$\mathcal{L}_{\mathrm{cls}}$ (label-smoothing 0.05) establishes the path-expert correspondence; $\mathcal{L}_{\mathrm{ANC}}$ refines soft fusion weights by the resulting ANC performance.

## Design Rationale

A naive MSE/NMSE-only objective (as used by the CCF 2026 official baseline) tends to over-attenuate easy low-frequency bands while leaving perceptually important high-frequency rebound uncontrolled. The frequency-aware formulation makes the trade-off explicit and tunable through $\lambda$, allowing the model to push low-frequency attenuation without sacrificing high-frequency neutrality. In Bai (2026), this loss (combined with the staged training) lets a WaveNet-only branch (10.08k params, 483.84 MMac/s) outperform the official baseline (42.76k params, 2.04 GMac/s) on seen paths.

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]] — parent domain
- [[concepts/feedback-guided-controller-fusion|Feedback-guided Controller Fusion]] — co-introduced framework that uses this loss
- [[concepts/waterbed-effect|Waterbed Effect]] — physical principle motivating the rebound term
- [[concepts/frequency-domain-loss|Frequency-Domain Loss]] — generic spectral loss family

## Related Sources

- [[sources/bai-2026-feedback-guided-anc|Bai et al. 2026: Feedback-guided DNN-based Controller Fusion for Robust Fixed-Parameter ANC]] — introduces the loss
