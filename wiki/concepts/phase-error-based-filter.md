---
type: concept
created: 2026-08-28
updated: 2026-08-28
sources:
  - raw/papers/kim-2014-doa-based-snr-estimation/full-text.txt
tags:
  - speech-enhancement
  - spatial-cues
  - dual-microphone
  - array-processing
---

# Phase-Error-Based Filter (PEF)

The **Phase-Error-Based Filter (PEF)** (Aarabi & Shi 2004) is a soft-masking dual-microphone speech enhancement method whose spectral gain is driven by the **phase-difference error** between the two channels, motivated by the observation that phase errors relate to the SNR of the observed noisy signal.

## Mechanism

PEF exploits the link between phase difference and the [[concepts/target-to-non-target-directional-signal-ratio|target-to-non-target directional signal ratio (TNR)]]: it approximates the TNR by the inverse of the squared phase difference,

$$
\widehat{\mathrm{TNR}}_{\mathrm{PEF}} \approx \frac{1}{(\Delta\psi)^2}
$$

and substitutes this into the Wiener-style TNR gain $G = \mathrm{TNR}/(\mathrm{TNR}+\alpha)$. Unlike binary masking on the dominant source per T-F bin, PEF is a soft mask, avoiding the musical noise caused by discontinuous zero-padding.

## Strengths and Weaknesses

- **Effective at low SNR / low TNR** for reducing non-target directional noise; PEF reported higher digit recognition accuracy than dual-microphone SDB and beamformer + post-filter (Aarabi & Shi 2004).
- **Distorts target-directional speech at high SNR / high TNR** — the $1/(\Delta\psi)^2$ approximation matches the exact $\cot^2(\Delta\tilde\psi/2)$ TNR only in the small-error asymptotic.
- **Single-cue dependence**: PEF works only on the DOA cue represented by phase differences, so when the target DOA is uncertain it can underperform even single-microphone techniques using temporal cues (Kim & Kim 2014).

In Kim & Kim's (2014) benchmark, PEF required a larger over-subtraction factor ($\alpha \approx 5$) than the exact TNR gain ($\alpha \approx 1$–$3$) and was outperformed in SDR by the exact TNR gain at low SNRs for every $\alpha$, and by [[concepts/doa-based-snr-estimation|DOA-based SNR estimation]] throughout.

## Related Concepts

- [[concepts/target-to-non-target-directional-signal-ratio|Target-to-Non-target Directional Signal Ratio (TNR)]] — quantity PEF approximates
- [[concepts/doa-based-snr-estimation|DOA-Based SNR Estimation]] — successor that fixes PEF's high-SNR distortion
- [[concepts/ideal-binary-mask|Ideal Binary Mask]] — hard-decision alternative with musical-noise artifacts
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — system context

## Related Sources

- [[sources/kim-2014-doa-based-snr-estimation|Kim & Kim 2014: DOA-Based SNR Estimation for Dual-Microphone Speech Enhancement]] — distinctively formulates PEF's relation to TNR and benchmarks against it
