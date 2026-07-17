---
type: concept
created: 2026-07-17
updated: 2026-07-17
sources:
  - raw/papers/valin-2021-percepnet-joint-echo-control/full-text.md
tags:
  - adaptive-filtering
  - acoustic-echo-cancellation
  - frequency-domain
  - signal-processing
---

# Multidelay Block Frequency-Domain Adaptive Filter (MDF)

The Multidelay Block Frequency-Domain (MDF) adaptive filter is a frequency-domain adaptive filtering algorithm for acoustic echo cancellation that partitions the echo path impulse response into multiple blocks, enabling efficient convolution and adaptation in the frequency domain via the FFT. Introduced by Soo & Pang (1990), it generalizes the block LMS frequency-domain approach to arbitrary filter lengths while maintaining computational efficiency.

## Role in PercepNet AEC

The [[concepts/percepnet|PercepNet]] AEC system (Valin et al. 2021) uses an MDF adaptive filter derived from the **SpeexDSP** implementation with several enhancements:

- **Robustness to double-talk**: combination of the learning rate control of Valin (2007) and a two-echo-path model (Ochiai, Araseki & Ogihara 1977)
- **Faster adaptation**: block variant of the PNLLS algorithm (Duttweiler 2000)
- **AUMDF variant**: alternatively constrained blocks, with the highest-energy block constrained on each iteration (compromise between complexity and convergence)
- **Filter length**: 150 ms (good compromise between complexity, convergence time, and steady-state accuracy)
- **Frame size**: 10 ms (matches the RES frame size, no extra delay)

A separate delay-estimation AEC with a 400-ms filter runs on 8 kHz downsampled signals to estimate the unknown delay D between the loudspeaker signal and the echo. The delayed far-end signal f(n−D) is then used for the main echo cancellation at 16 kHz.

## Why Traditional AEC Is Retained

Despite the neural post filter, the linear AEC is critical for double-talk performance. The PercepNet paper shows that while the linear AEC does not help attenuate isolated (far-end-only) echo, it greatly contributes to preserving near-end speech during double-talk — the neural RES alone tends to over-attenuate near-end speech when the echo path is not first removed.

## Related Concepts

- [[concepts/adaptive-filtering|Adaptive Filtering]]
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/percepnet|PercepNet]]
- [[concepts/percepnet-style-neural-post-filter|PercepNet-Style Neural Post Filter]]

## Related Sources

- [[sources/valin-2021-percepnet-joint-echo-control|Valin et al. 2021: Joint Neural Echo Control and Speech Enhancement Based On PercepNet]]
