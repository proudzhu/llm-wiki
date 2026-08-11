---
type: concept
created: 2026-08-11
updated: 2026-08-11
sources:
  - raw/papers/fang-2020-robust-residual-echo-suppression/full-text.md
tags:
  - evaluation-metric
  - acoustic-echo-cancellation
  - residual-echo-suppression
---

# Echo Return Loss Enhancement (ERLE)

Echo Return Loss Enhancement (ERLE) is the standard objective metric for evaluating acoustic echo cancellation (AEC) and residual echo suppression (RES) performance during **single talk** (far-end only, no near-end speech). It measures the attenuation of the echo achieved by the AEC/RES system relative to the unprocessed microphone signal.

## Key Formulations

$$\mathrm{ERLE} = 10\log_{10}\frac{\mathcal{E}\{|e[n]|^2\}}{\mathcal{E}\{|y[n]|^2\}},$$

where $y[n]$ is the original microphone signal (containing echo) and $e[n]$ is the output signal after echo cancellation / suppression. Higher ERLE (in dB) means more echo has been removed.

### Variants

- **True ERLE (tERLE)**: computed using the error signal with the near-end component removed, isolating the echo attenuation from near-end speech corruption. Used in [[sources/wung-2011-residual-echo-suppression-system|Wung et al. 2011]] to avoid the metric being inflated or depressed by near-end speech.
- **Segmental ERLE**: computed frame-by-frame to track convergence over time, as plotted in [[sources/fang-2020-robust-residual-echo-suppression|Fang 2020]].

### When ERLE Is Meaningful

ERLE is only well-defined when the near-end signal is absent (single talk). During double talk, $e[n]$ contains near-end speech whose energy inflates the numerator, making ERLE a misleading indicator of echo suppression. For double-talk evaluation, [[concepts/speech-to-speech-distortion-ratio|SSDR]] is preferred.

### Typical Targets

- ITU-T G.167 recommends **>45 dB ERLE** during single talk and **~30 dB** during double talk for hands-free teleconferencing systems (cited in [[sources/wung-2011-residual-echo-suppression-system|Wung et al. 2011]]).

## Related Concepts

- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]] — the system ERLE evaluates.
- [[concepts/residual-echo-suppression|Residual Echo Suppression]] — the post-AEC stage that further increases ERLE.
- [[concepts/speech-to-speech-distortion-ratio|Speech-to-Speech-Distortion power Ratio (SSDR)]] — the complementary metric for double-talk evaluation.

## Related Sources

- [[sources/fang-2020-robust-residual-echo-suppression|Fang 2020]] — uses segmental ERLE to compare AEC-only, baseline RES, and proposed RES.
- [[sources/wung-2011-residual-echo-suppression-system|Wung et al. 2011]] — uses tERLE to evaluate a system-level RES approach.
