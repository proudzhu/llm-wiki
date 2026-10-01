---
type: concept
created: 2026-04-25
updated: 2026-10-01
sources:
  - raw/papers/xiao-2023-spatially-selective-anc/full-text.md
  - raw/papers/hu-2026-abse-net/full-text.md
  - raw/papers/rao-2026-keep-speech-anc/full-text.txt
aliases:
  - Keep-Speech ANC
  - KSANC
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

### Reference Enhancement (zero-delay)
- [[sources/rao-2026-keep-speech-anc|Rao et al. 2026]] (who use the term "keep-speech ANC, KSANC" for this goal) keep the control filter **conventional** and place a causal time-domain WaveNet on the **reference path** instead: the network ([[concepts/reference-signal-enhancement|RSE]]) suppresses speech in the speech-plus-noise reference, and an RLS-adapted FIR filter cancels only the noise — adding zero algorithmic delay, unlike the CRN approaches above whose frame-level latency violates headphone causality margins
- Trained with an error-domain loss $E[d + s \ast w \ast g_\phi]^2$ (Wiener-optimal control filter substituted) that jointly encodes noise suppression and speech preservation, the method improves both STOI and DNSMOS over Unprocessed / Conventional ANC / DeepANC on measured headphone IRs, and generalizes to unseen SNRs, noise types, and source directions

### Spatial Selectivity
- [[concepts/spatially-selective-anc|Spatially selective ANC]] (Xiao et al. 2023) preserves the desired sound **spatially**: a Frost-type ReIR constraint on the hybrid ANC cost function leaves the desired-direction physical wave unaltered at the error microphone while noise from other directions is minimized — SNR improved from −13.9 to 15.2 dB (NR 29.1 dB, SDI −25.1 dB) on an AR-glasses array, with ~2% of the secondary-source energy of reconstruct-based systems and natural binaural cues preserved ([[sources/xiao-2023-spatially-selective-anc|Xiao 2023]])
- The robust soft-constrained SSANC formulation in [[sources/xiao-2026-robust-spatially-selective-anc|Xiao 2026]] handles secondary-path variations across users by averaging the cost over a measured set of plant estimates
- Complementary to spectral selectivity; can be combined for enhanced separation

### Hearing-Aid Active Binaural Speech Enhancement
- [[concepts/abse-net|ABSE-NET]] (Hu et al. 2026) extends the speech-preserving idea to **open-fit hearing aids**: the loudspeaker plays both the enhanced signal and a learned anti-leakage component that destructively interferes with vent leakage, while an SI-SDR + STOI loss preserves the target speech. It needs no in-ear error microphone at inference (training-only), and its 0.112M-parameter network preserves binaural spatial cues (ILD/IPD) while cancelling leakage.

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
- [[concepts/spatially-selective-anc|Spatially Selective ANC]]
- [[concepts/soft-constrained-anc|Soft-Constrained ANC]]
- [[convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[transparency-mode|Transparency Mode]]
- [[voice-activity-detection|Voice Activity Detection]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/active-binaural-speech-enhancement|Active Binaural Speech Enhancement]]
- [[concepts/abse-net|ABSE-NET]]

## Related Sources

- [[sources/xiao-2023-spatially-selective-anc|Xiao 2023: Spatially Selective Active Noise Control Systems]]
- [[sources/dai-2026-speech-preserving-deep-anc|Dai 2026: Speech-Preserving Deep ANC]]
- [[sources/xiao-2026-robust-spatially-selective-anc|Xiao 2026: Robust Soft-Constrained SSANC for Hearables]]
- [[sources/hu-2026-abse-net|Hu et al. 2026: ABSE-NET — Active Binaural Speech Enhancement for Open-Fit Hearing Aids]]
- [[sources/rao-2026-keep-speech-anc|Rao, Rong, Sun, He, Chen, Zou & Lu 2026: Causal Reference-Enhanced Keep-Speech Active Noise Control]] — KSANC via zero-delay reference enhancement; the control filter stays conventional

## Related Synthesis

- [[synthesis/ai-driven-anc|AI-Driven ANC]]
- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]
