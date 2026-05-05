---
type: entity
created: 2026-04-25
updated: 2026-04-25
tags:
  - researcher
  - active-noise-control
  - deep-learning
---

# Shuning Dai

**Affiliation**: Nanyang Technological University, School of Electrical and Electronic Engineering
**Degree**: MSc in Signal Processing and Machine Learning (2026)
**Supervisor**: Prof. Gan Woon Seng

## Research Focus

Shuning Dai's master's dissertation addresses the intersection of deep learning and active noise control, specifically targeting the problem of speech preservation during noise cancellation in reverberant environments. His work demonstrates that a CRN-based Deep ANC system can selectively cancel noise while maintaining speech intelligibility — a capability that traditional FxLMS algorithms fundamentally lack.

## Key Contribution

- Proposed a **speech-preserving loss function** that uses algebraic cancellation to ensure the network only minimizes residual noise, never speech
- Validated Deep ANC in a physically realistic reverberant environment (RT60 = 0.3s) using the Image Source Method
- Demonstrated 10-15 dB improvement over FxLMS at nonlinear harmonic frequency points

## Related Sources

- [[../sources/dai-2026-speech-preserving-deep-anc|Dai 2026: Speech-Preserving Deep ANC]] — Master's dissertation

## Related Concepts

- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[../concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[../concepts/speech-preserving-anc|Speech-Preserving ANC]]
