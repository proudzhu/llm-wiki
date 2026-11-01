---
type: concept
created: 2026-11-01
updated: 2026-11-01
sources:
  - raw/papers/yan-2025-lisennet/full-text.md
tags:
  - feature-engineering
  - phase
  - speech-enhancement
  - signal-processing
---

# Phase Difference (PD) Feature

The **phase difference (PD)** is an input feature for time-frequency-domain speech enhancement: instead of (or in addition to) raw phase, the network consumes the *differences* of the phase spectrum along the frequency and time axes. Used in [[concepts/lisennet|LiSenNet]] (Yan et al., ICASSP 2025), motivated by Mowlaee & Saeidi's observation that **PD exhibits similar patterns to the magnitude spectrum**, making it a useful auxiliary signal for estimating the clean magnitude.

## Definition

With $\mathbf{P}_x(t,f)$ the noisy phase spectrum, $Q$ the frame shift and $M$ the frame length:

**Frequency-axis PD** (Eq. 1):

$$\Delta_f \mathbf{P}_x(t,f) = \mathbf{P}_x(t,f) - \mathbf{P}_x(t,f-1)$$

**Temporal PD** (Eq. 2), with the baseband correction:

$$\Delta_t \mathbf{P}_x(t,f) = \mathbf{P}_x(t,f) - \mathbf{P}_x(t-1,f) - 2\pi f \frac{Q}{M}$$

The linear term $2\pi f \frac{Q}{M}$ compensates the phase offset induced by the **overlap of STFT frames**: consecutive frames analyze shifted windows of the same signal, so identical content acquires a frequency-dependent phase ramp; subtracting it yields the **baseband PD** (following Krawczyk & Gerkmann's STFT phase reconstruction work). Without the correction, the temporal PD structure would be distorted and less informative.

## Usage

LiSenNet concatenates the power-compressed magnitude $(\mathbf{A}_x)^{0.3}$ with the PDs as the model input — the network then estimates only the enhanced **magnitude**; PD serves as phase-derived evidence, not as a phase target.

Ablation (VoiceBank+DEMAND): removing PD drops PESQ 3.07 → 2.99 — **+0.08 PESQ at zero parameter cost**, since PD is only an input feature.

## Relation to Other Phase Features

- **Group delay / phase derivative**: the frequency-axis PD is related to negative group delay; the temporal PD relates to instantaneous-frequency deviation.
- **[[concepts/angle-feature|Angle feature]]** (TSE): fuses IPD/TPD via a cosine-similarity formulation against a reference — a learned combination, vs. PD's raw differences.
- **Phase-aware masks** ([[concepts/complex-ratio-mask|cIRM]] etc.): output-side phase modeling; PD is input-side only.

## Related Concepts

- [[concepts/lisennet|LiSenNet]]
- [[concepts/gla-phase-refinement|GLA Phase Refinement]]
- [[concepts/power-law-compression|Power-Law Compression]]
- [[concepts/angle-feature|Angle Feature]]
- [[concepts/spectrogram-analysis|Spectrogram Analysis]]

## Related Sources

- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]]
