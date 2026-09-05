---
type: concept
created: 2026-09-05
updated: 2026-09-05
sources:
  - raw/papers/he-2026-neural-projection-filter-anc/full-text.md
tags:
  - active-noise-control
  - multi-reference-anc
  - reference-projection
  - deep-learning
  - neural-filter-generation
---

# Condition-Aware Projection Filtering (CAPF)

## Overview

**Condition-aware projection filtering (CAPF)** is a neural front end for [[concepts/multi-reference-anc|multi-reference ANC]] in which a network (CAPFNet) generates **block-wise causal linear FIR projection filters** that compress high-dimensional, strongly correlated reference signals into a small number of projected references. The projected references feed a *conventional* adaptive controller (FDFxNLMS or LMS-Newton), so the neural stage only restructures the input — it never generates control signals or control filters directly.

Introduced by He, Chen, Zou, Tao & Qiu (IEEE Signal Processing Letters 2026) — [[sources/he-2026-neural-projection-filter-anc|He et al. 2026]].

## Key Formulations

The multichannel reference $\mathbf{x}(n) \in \mathbb{R}^P$ is projected block-wise:

$$\mathbf{v}(n) = \mathbf{W}_{\mathrm{proj}}(k)\,\tilde{\mathbf{x}}(n), \qquad \mathbf{W}_{\mathrm{proj}}(k) \in \mathbb{R}^{Q \times P L_p},$$

where the filter is regenerated once per block (every $N = 8$ STFT frames) but applied **sample-wise**, avoiding block-processing latency. "Condition-aware" refers to conditioning the generated filter on the vehicle operating condition (driving speed, road surface, environment): CAPFNet encodes condition features and produces softmax weights over $J = 7$ condition experts.

The generated filter is decomposed into three additive components:

$$\mathbf{W}_{\mathrm{proj}}(k) = \mathbf{W}_{base} + \mathbf{W}_{exp}(k) + \mathbf{W}_{res}(k)$$

- $\mathbf{W}_{base}$ — global learnable component capturing the common (condition-independent) projection structure;
- $\mathbf{W}_{exp}(k) = \sum_{j=1}^{J} z_{\mathrm{cond},j}(k)\,\mathbf{W}_j$ — softmax-weighted mixture of condition experts, each in low-rank form $\bar{\mathbf{A}}_j(\mathbf{I}_P \otimes \mathbf{B}_e)$ with rank $K_e = 24$;
- $\mathbf{W}_{res}(k) = \bar{\mathbf{A}}_r(k)(\mathbf{I}_P \otimes \mathbf{B}_r)$ — block-wise residual correction with rank $K_r = 12$, where $\bar{\mathbf{A}}_r(k)$ is produced from the fused encoder/condition representation by a two-linear-layer ELU mapping.

Training combines an A-weighted error loss (evaluated through an offline Wiener controller on the projected references), a whitening regularizer $\|\mathbf{R}/\rho - \mathbf{I}\|_F^2$ on the projected-reference autocorrelation, and a condition-classification cross-entropy supervising the expert weights.

## Why Block-Wise Filter Generation

The direct predecessor, NRP-FxAP (He et al., JASA 2026), performs **point-wise** neural reference projection — generating projected reference samples at the sampling rate — which incurs high online complexity (17.9 GMAC/s on the 42-channel road-noise setup). CAPF moves neural inference to **block rate**: the 500k-parameter CAPFNet costs 83.0 MMAC/s for filter generation plus 172.0 MMAC/s for the linear projection filtering, roughly **48× cheaper** online while matching NRP-FxAP's attenuation (8.52 dBA average, comparable to the offline Wiener bound). This contrasts with [[concepts/generative-fixed-filter-anc|generative fixed-filter ANC]], where the neural stage generates the *control* filter rather than a *reference projection* filter.

## Evidence

- 42-reference in-vehicle road-noise system (2 sources, 2 error mics, 4 kHz): CAPF-Newton attains −10.24/−7.46/−7.78 dBA (M1 at 50/80/100 km/h) at 374.0 MMAC/s — +2.6 dBA over FDFxNLMS, +1.19 dBA over BCD-Newton at 15% lower complexity.
- Projection dimension $Q = 4$ suffices: raising $Q$ to 6 adds only 0.07 dBA while nearly doubling complexity.
- Ablations: removing $\mathbf{W}_{base}$, $\mathbf{W}_{exp}$, or both costs 0.15, 0.29, 0.76 dBA respectively.
- Generalizes to an unseen 60 km/h condition (training only had 50/80/100 km/h), converging within ~20 s.
- Deployment: 132.2 µs per sample (delayless path, i7-10875H), 18.2 ms per asynchronous filter update, 2.65 MiB DSP memory (9.51 MiB upper bound).

## Related Concepts

- [[concepts/multi-reference-anc|Multi-Reference ANC]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/multi-channel-anc|Multi-Channel ANC]]
- [[concepts/frequency-domain-anc|Frequency-Domain ANC]]
- [[concepts/generative-fixed-filter-anc|Generative Fixed-Filter ANC]]

## Related Sources

- [[sources/he-2026-neural-projection-filter-anc|He et al. 2026: Neural Projection Filter Generation for Multi-Reference ANC]]
