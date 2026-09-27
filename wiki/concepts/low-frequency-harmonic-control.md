---
type: concept
created: 2026-09-27
updated: 2026-09-27
sources:
  - raw/papers/watanabe-2026-low-frequency-harmonic-control/full-text.md
tags:
  - post-filter
  - harmonic-emphasis
  - low-complexity
  - intelligibility
  - open-ear-headphones
---

# Low-Frequency Harmonic Control (LFHC)

**Low-Frequency Harmonic Control (LFHC)** is a low-complexity post-filter, introduced by [[entities/yuki-watanabe|Watanabe]] et al. (NTT, ICASSP 2026), that improves the intelligibility of speech played back through [[concepts/open-ear-headphones|open-ear headphones]] in noisy environments **without amplifying volume**. It suppresses the fundamental frequency $f_0$ and reinforces the second and third harmonics, reallocating speech energy into bands that are (i) less masked by low-frequency environmental noise and (ii) less constrained by the weak low-frequency output of the small loudspeaker units in open-ear designs.

## Principle

Enhancing the fundamental of open-ear playback contributes little to intelligibility: the fundamental falls in the frequency range where urban/bustle noise has large components (masking) and where the speaker's output is limited (high lowest resonant frequency). LFHC instead emphasizes the low-order harmonics, which previous research (Hu & Loizou 2010) shows contribute to intelligibility.

## Key Formulations

LFHC adapts the conventional pitch-enhancement post-filter from speech coding. The pitch period $\tau_0$ is estimated per frame (several tens of ms) via autocorrelation. A single-tap FIR comb filter produces the delayed signal

$$r[n] = \alpha\, s[n - \tau], \qquad 0 < \alpha < 1$$

with the delay set to $\tau = \tau_0 / 2.5$ — **not** $\tau_0$ as in conventional pitch enhancement:

- $\tau \approx \tau_0/2$ would align the comb nulls with $f_0$ *and its odd-order harmonics*, suppressing too much.
- $\tau \approx \tau_0/3$ would emphasize the third harmonic, which has less energy than the second due to the average spectral tilt of speech.

A moving-average FIR low-pass filter with cutoff $F_C = 5 f_0$ (filter length $N \approx F_S / (2F_C)$) confines emphasis to at most the third harmonic, minimizing influence on formant frequencies. Its group delay $\tau_g = (N-1)/2$ samples is compensated in the comb delay:

$$\tau = \frac{\tau_0}{2.5} - \frac{N-1}{2}$$

The output is $s_{\mathrm{out}}[n] = s[n] + r_{\mathrm{LP}}[n]$.

## Empirical Findings

In a MUSHRA-like subjective evaluation under Brown noise at 69 dB SPL (SNR ≈ −5 dB(A)):

- **$\alpha = 0.6$**: significantly improved intelligibility for 3 of 6 utterances, degraded none.
- **$\alpha = 0.9$**: significantly degraded 2 of 6 — excessive suppression/enhancement, or pitch-estimation-error artifacts becoming prominent at high $\alpha$.
- The Intelligibility Score correlates **−0.93** with the pre-processing mean energy ratio of the 2nd/3rd harmonics to the fundamental: LFHC helps most for speech whose low-order harmonics are weak relative to $f_0$, motivating per-signal adaptation based on this energy ratio.

## Relation to Other Post-Filters

Unlike the [[concepts/psychoacoustic-postfilter|psychoacoustic postfilter]] (which *suppresses* noise/echo up to the masking threshold of the desired signal), LFHC *rearranges* the desired signal's own harmonic energy to fall into less-masked, better-reproduced bands — the masking-aware counterpart for playback intelligibility rather than residual-noise suppression. Like the speech-coding post-filters it descends from (ITU-T G.718, 3GPP EVS; Chiba et al.'s pitch-adaptive post-filter), it achieves this with a handful of filter taps, suitable for small in-device DSPs.

## Related Concepts

- [[concepts/open-ear-headphones|Open-Ear Headphones]]
- [[concepts/hearables|Hearables]]
- [[concepts/psychoacoustic-postfilter|Psychoacoustic Postfilter]]

## Related Sources

- [[sources/watanabe-2026-low-frequency-harmonic-control|Watanabe et al. 2026: Low-Frequency Harmonic Control for Speech Intelligibility in Open-Ear Headphones]]
