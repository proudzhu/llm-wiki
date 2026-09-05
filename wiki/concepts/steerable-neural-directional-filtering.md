---
type: concept
created: 2026-09-05
updated: 2026-09-05
sources:
  - raw/papers/huang-2025-steerable-neural-directional-filtering/full-text.md
tags:
  - neural-directional-filtering
  - steerable-filtering
  - virtual-directional-microphone
  - directivity-pattern
  - deep-learning
---

# Steerable Neural Directional Filtering

Steerable neural directional filtering (SNDF) extends [[concepts/neural-directional-filtering|neural directional filtering (NDF)]] so that a **single trained model** can render its learned directivity pattern steered towards any direction at inference time — including switching the steering direction mid-recording. It was introduced by Huang, Halimeh, Chetupalli, Thiergart & Habets at Euronoise 2025.

Whereas the founding NDF study ([[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024]]) learns one fixed pattern with a fixed look direction per model, SNDF decouples *pattern shape* (fixed at training) from *steering direction* (a free conditioning input at inference). Pattern *shape* configurability at inference is addressed later by UNDF (FiLM-conditioned user-defined patterns) and NDF+ targets diffuse-sound control instead.

## Steering Mechanism

The steering direction $\theta_s$ is one-hot encoded (over $M = 360°/\vartheta$ classes at angular resolution $\vartheta$), passed through a linear layer, and used to initialize the forward and backward initial states of the F-BiLSTM of the FT-JNF backbone for each time frame — the conditioning scheme of the [[concepts/spatially-selective-nonlinear-filter|spatially selective filter]] (Tesch & Gerkmann 2023). No architectural changes to the mask-estimation path are required.

## Steerability-Oriented Training Strategy

1. **Scene reuse across steering targets**: each acoustic scene's microphone signals are paired with all $M$ target VDM signals (steering directions spanning 0°–360°) as separate training samples, emphasizing the steerability function.
2. **Mini-batch sampling constraint**: at least one sample per mini-batch must contain a speaker from the target steering direction or its vicinity, preventing the denominator of the batch-aggregated normalized L1 loss from collapsing and stabilizing training.
3. **Disjoint speaker grids**: training/validation/test speaker positions use interleaved angular grids (5° / 2.5°-offset / 2.5° spacing offset by 1.25°), so test DOAs are unseen.

## Key Findings (Huang et al. 2025)

- Estimated pattern shape is **steering-invariant**: main lobe well approximated, null attenuation limited, patterns frequency-invariant across $\theta_s \in \{0°, 60°, 120°\}$.
- SDR is consistent across steering directions: 25.8–26.0 dB (1st-order cardioid), 20.2–20.3 dB (3rd-order), 16.7–17.5 dB (6th-order).
- **Order beyond microphone count**: a 6th-order DMA pattern is learned with a 4-microphone array (3-mic UCA ring), where classical differential beamforming is bounded by $\lfloor Q/2 \rfloor$.
- A speech-trained model suppresses a music interferer in the null direction and supports mid-inference steering changes.

## Related Concepts

- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]
- [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering]]
- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]

## Related Sources

- [[sources/huang-2025-steerable-neural-directional-filtering|Huang et al. 2025: Steerable Neural Directional Filtering]] — the introducing paper
- [[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024: Neural Directional Filtering]] — the fixed-pattern predecessor
- [[sources/tesch-2024-spatially-selective-nonlinear-filters|Tesch & Gerkmann 2024: Spatially Selective Deep Non-linear Filters]] — origin of the conditioning mechanism
