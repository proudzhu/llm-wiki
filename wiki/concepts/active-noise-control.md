---
type: concept
created: 2026-04-10
updated: 2026-04-26
sources:
aliases:
- Active Noise Control
tags:
- acoustics
- control-systems
- signal-processing
---

# Active Noise Control

## Overview

**Active Noise Control (ANC)** is a technique that cancels unwanted sound by generating an "anti-noise" signal — a secondary sound of equal amplitude but opposite phase — which combines with the primary noise to achieve destructive interference, based on the principle of superposition.

## How It Works

1. A **reference sensor** (microphone) picks up the primary noise
2. A **controller** processes this signal and generates an anti-noise signal
3. A **secondary source** (loudspeaker) emits the anti-noise
4. The anti-noise and primary noise cancel each other at the **error sensor** location

## Two System Architectures

### Feedforward ANC

- Uses a reference sensor placed **upstream** of the noise source to get a time-advanced reference signal
- Requires the noise to be measurable before it reaches the cancellation zone
- Generally better performance for predictable noise

### Feedback ANC

- No reference sensor; uses only an **error sensor** to drive the controller
- Used when the primary noise cannot be directly observed or there are too many primary noise sources
- Typical applications: headsets, headrests, headphones, double-glazed windows, ducts
- Two subtypes:
  - **Non-adaptive**: Fixed controller with high gain at frequencies of interest. Requires solving optimization problems; vulnerable to changing conditions.
  - **Adaptive**: Controller adapts automatically. Includes [[internal-model-control|Internal Model Control]] (IMC) based systems and [[adaptive-feedback-control|Adaptive Feedback Control]] systems.

## Deep Learning Approaches

Traditional ANC algorithms are limited by linear assumptions and cannot handle nonlinear acoustic paths or selectively preserve speech. Deep learning approaches address these limitations:

- **[[convolutional-recurrent-network|CRN]]-based Deep ANC**: End-to-end anti-noise generation using encoder-LSTM-decoder architecture with [[complex-spectrum-mapping|Complex Spectrum Mapping]] for precise phase control
- **[[speech-preserving-anc|Speech-Preserving ANC]]**: Uses a modified loss function that algebraically cancels speech components, training the network to cancel only noise while leaving speech transparent
- SFANC/GFANC: Selective/Generative Fixed-Filter ANC uses CNNs for filter selection or generation, enabling instant response to changing noise types
- **E2E-CFG**: End-to-End Control-Filter Generation directly generates control filters via Transformer co-processor in a differentiable ANC system, trained unsupervised on residual error

### Performance Comparison (Dai 2026, RT60=0.3s)

| Noise Type | FxLMS (dB) | Deep ANC (dB) | Improvement |
|:-----------|:-----------|:--------------|:------------|
| Engine (Periodic) | 12.22 | 22.92 | +10.70 |
| Babble (Non-stationary) | 5.28 | 18.17 | +12.89 |
| Volvo (Stationary) | 4.91 | 19.08 | +14.17 |

## Key Challenges

- **Secondary path estimation**: The path from loudspeaker to error sensor (including DAC, amplifier, speaker, acoustic path, ADC) must be estimated accurately
- **Stability**: Phase shifts in the secondary path can cause negative feedback to become positive feedback
- **Predictability**: Performance depends on how predictable the primary noise is; narrow-band noise works better than broadband noise
- **Nonlinear distortion**: Low-cost speakers and high-SPL scenarios introduce nonlinearities that linear algorithms cannot model
- **Speech cancellation**: Traditional "cancel everything" approach damages useful speech signals in mixed sound fields

## Related Concepts
- [[adaptive-algorithm-tradeoffs]]
- [[cha-2023-dnoisenet-feedback-anc]]
- [[how-to-estimate-secondary-path]]
- [[impulsive-noise-control]]
- [[jiang-2025-ai-driven-avnc-review]]
- [[luo-2026-hybrid-gfanc-fxnlms]]
- [[multichannel-anc-efficiency-and-robustness]]
- [[personal-sound-zones-evolution-and-optimization]]
- [[what-is-simplified-adaptive-feedback-anc]]

- [[adaptive-feedback-control|Adaptive Feedback Control]]
- [[internal-model-control|Internal Model Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[leaky-fxlms-algorithm|Leaky FxLMS Algorithm]]
- [[simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]]
- [[online-secondary-path-modeling|Online Secondary-Path Modeling]]
- [[convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[speech-preserving-anc|Speech-Preserving ANC]]
- [[image-source-method|Image Source Method]]
- [[uncertainty-modeling-for-anc|Uncertainty Modeling for ANC]]
- [[robust-stability-constraint|Robust Stability Constraint]]
- [[convex-hull-uncertainty-model|Convex Hull Uncertainty Model]]
- [[elliptic-uncertainty-model|Elliptic Uncertainty Model]]

## Related Sources

- [[../sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]] — Proposes a simplified adaptive feedback system using error signal directly as reference
- [[../sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Comprehensive ANC tutorial covering all major algorithms
- [[../sources/dai-2026-speech-preserving-deep-anc|Dai 2026: Speech-Preserving Deep ANC]] — CRN-based Deep ANC with speech preservation in reverberant environments
- [[../sources/hilgemann-2024-data-driven-uncertainty-anc|Hilgemann 2024: Data-Driven Uncertainty Modeling for Robust Feedback ANC]] — Elliptic and convex hull uncertainty models for robust feedback ANC
- [[../sources/wang-2026-predictive-dsfanc-crnn|Wang 2026: Predictive Directional SFANC via CRNN]] — CRNN predicts next-frame DoA for proactive filter selection in moving source ANC

## Related Entities

- [[../entities/sen-m-kuo|Sen M. Kuo]] — ANC authority, author of the definitive tutorial review
- [[../entities/dennis-r-morgan|Dennis R. Morgan]] — Co-author of the tutorial review, foundational FXLMS analysis
- [[../entities/lifu-wu|Lifu Wu]] — Proposed the simplified adaptive feedback architecture
- [[../entities/xiaojun-qiu|Xiaojun Qiu]] — Corresponding author on the SimpAFB paper
- [[../entities/shuning-dai|Shuning Dai]] — Speech-preserving Deep ANC in reverberant environments
