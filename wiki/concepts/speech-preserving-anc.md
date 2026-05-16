---
type: concept
created: 2026-04-25
updated: 2026-04-25
sources:
tags:
  - active-noise-control
  - speech-processing
  - deep-learning
  - selective-noise-control
---

# Speech-Preserving ANC

**Speech-Preserving ANC** is a variant of [[active-noise-control|Active Noise Control]] that selectively cancels environmental noise while retaining target speech signals. Unlike traditional ANC which minimizes total error energy (eliminating all sound), speech-preserving ANC acts as a spectral filter that distinguishes noise from speech based on their time-frequency characteristics.

## The Problem with Traditional ANC

Traditional ANC algorithms (e.g., [[filtered-x-lms-algorithm|FxLMS]]) minimize $E[e^2(n)] \to 0$, treating all sound at the error microphone as noise to be eliminated. In mixed sound fields where both noise and speech are present, this "one-size-fits-all" approach accidentally cancels desired speech, hindering communication and potentially masking safety-critical audio cues.

## The Speech-Preserving Loss Function

The key innovation (formalized by Dai 2026) is a loss function that targets acoustic transparency for speech:

$$\mathcal{L}_{speech} = \frac{1}{L} \sum_{n=1}^{L} (e(n) - d_{speech}(n))^2$$

Where $e(n) = d_{noise}(n) + d_{speech}(n) + a(n)$ is the residual error signal. After algebraic simplification, the speech components cancel:

$$\mathcal{L}_{speech} = \frac{1}{L} \sum_{n=1}^{L} (d_{noise}(n) + a(n))^2$$

This means the network is trained to minimize only residual noise ($a(n) \approx -d_{noise}(n)$), with no incentive to cancel the speech component. The loss function implicitly enforces spectral selectivity.

## ANC vs. Speech Enhancement

Speech-preserving ANC is fundamentally different from traditional Speech Enhancement (SE):

| Aspect | Speech-Preserving ANC | Speech Enhancement |
|--------|----------------------|--------------------|
| Domain | Physical (wave interference in air) | Digital (signal filtering) |
| Latency | <10 ms (sound propagation delay) | Can be offline or high-latency |
| Secondary path | Must compensate for $S(z)$ | Not applicable |
| Output | Anti-noise signal for speaker | Enhanced audio signal |
| Phase accuracy | Critical (determines cancellation) | Important but less critical |

## Implementation Approaches

### Deep Learning (CRN-based)
- Uses [[convolutional-recurrent-network|CRN]] with [[complex-spectrum-mapping|CSM]] for precise phase control
- Secondary path modeled as frozen convolutional layer during training
- Speech-preserving loss function drives selective cancellation
- Validated in reverberant environments (Dai 2026)

### Spatial Selectivity
- Xiao et al. (2023) proposed spatially selective ANC using beamforming to create quiet zones while allowing sound in other areas
- Complementary to spectral selectivity; can be combined for enhanced separation

## Performance Characteristics

From Dai 2026 (SNR = 5 dB, RT60 = 0.3s):

| Noise Type | NR (dB) | PESQ Δ | STOI Δ |
|:-----------|:--------|:-------|:-------|
| Engine (Periodic) | 8.88 | +0.686 | +0.101 |
| Babble (Non-stationary) | 5.30 | +0.359 | +0.066 |
| Volvo (Stationary) | 13.70 | +0.464 | +0.001 |
| F16 (Broadband) | 8.19 | +0.632 | +0.100 |

The system conservatively reduces noise for Babble (5.30 dB) to protect speech, while aggressively canceling stationary noise (Volvo: 13.70 dB) where speech is clearly distinguishable.

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[transparency-mode|Transparency Mode]]
- [[voice-activity-detection|Voice Activity Detection]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]

## Related Sources

- [[sources/dai-2026-speech-preserving-deep-anc|Dai 2026: Speech-Preserving Deep ANC]]

## Related Synthesis

- [[synthesis/ai-driven-anc|AI-Driven ANC]]
- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]
