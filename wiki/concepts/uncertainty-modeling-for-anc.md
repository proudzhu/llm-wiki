---
type: concept
created: 2026-04-26
updated: 2026-04-26
sources:
tags:
  - active-noise-control
  - feedback-anc
  - robust-control
  - uncertainty-modeling
---

# Uncertainty Modeling for ANC

**Uncertainty modeling for ANC** describes how variations in the controlled system (secondary path) $G(z)$ are abstracted into a mathematical set $\Pi$ that serves as the basis for robust controller design. The accuracy of this model directly determines the trade-off between ANC performance and stability guarantees.

## Why Uncertainty Modeling Matters

In [[concepts/feedback-anc|Feedback ANC]], the secondary path varies due to:
- Different wearers (head/ear shape)
- Fit changes (normal → loose → tight)
- Manufacturing tolerances, wear, temperature

A robust controller must guarantee stability for **all** possible plant variations. The uncertainty model $\Pi$ defines what "all possible" means — if it's too conservative (overestimates variations), the controller is unnecessarily restricted; if it's too loose, stability cannot be guaranteed.

## Requirements for a Good Uncertainty Model

1. **Minimal area**: Cover all observed variations with the smallest possible region in the complex plane, to maximize design freedom
2. **Contiguity**: The model must be a single connected region so that stability is maintained during fit transitions (e.g., normal → loose)
3. **Data-driven**: Parameters should be derived from actual measurements, not assumed a priori

## Model Hierarchy (Least to Most Conservative)

| Model | Area (relative to disk) | Constraint Type | Key Parameters |
|:------|:------------------------|:----------------|:---------------|
| [[concepts/convex-hull-uncertainty-model|Convex Hull]] | ~60% | Non-convex | Half-space weights & offsets |
| [[concepts/elliptic-uncertainty-model|Elliptic]] | ~60–70% | Non-convex | Semi-axes, rotation angle |
| Multi-Disk | ~70–80% | Convex | Multiple disk centers & radii |
| Norm-Bounded (Disk) | 100% (baseline) | Convex | Single center & radius |

## Frequency-Dependent Behavior

The shape of uncertainty varies with frequency:
- **Low frequencies** (< 200 Hz): Widely dispersed, elongated along imaginary axis — disk model severely overestimates
- **Mid frequencies** (~2.8 kHz): Elongated along a line at ~30° angle — elliptic model captures well
- **High frequencies** (~4.6 kHz): Quasi-circular distribution — disk model is already accurate

## Impact on ANC Performance

From Hilgemann et al. (2024), using more accurate models in IMC-based optimization:

| Model | Objective $J(q)$ | Peak Attenuation at 300 Hz |
|:------|:------------------|:---------------------------|
| Disk | 1.11 | ~11 dB |
| Multi-Disk | 0.66 | ~18 dB |
| Elliptic | 0.56 | ~25 dB |
| Convex Hull | 0.54 | ~29 dB |

The convex hull model achieves **18 dB more attenuation** at 300 Hz than the conventional disk model.

## Related Concepts

- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/internal-model-control|Internal Model Control]]
- [[concepts/convex-hull-uncertainty-model|Convex Hull Uncertainty Model]]
- [[concepts/elliptic-uncertainty-model|Elliptic Uncertainty Model]]
- [[concepts/robust-stability-constraint|Robust Stability Constraint]]
- [[concepts/robust-adaptive-filtering|Robust Adaptive Filtering]]

## Related Sources

- [[sources/hilgemann-2024-data-driven-uncertainty-anc|Hilgemann 2024: Data-Driven Uncertainty Modeling for Robust Feedback ANC]]
