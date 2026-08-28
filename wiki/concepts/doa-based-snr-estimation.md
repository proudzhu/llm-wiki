---
type: concept
created: 2026-08-28
updated: 2026-08-28
sources:
  - raw/papers/kim-2014-doa-based-snr-estimation/full-text.txt
tags:
  - speech-enhancement
  - snr-estimation
  - doa
  - spatial-cues
  - multi-channel
---

# DOA-Based SNR Estimation

**DOA-Based SNR Estimation** (Kim & Kim 2014) estimates the a priori SNR for spectral-gain speech enhancement from **spatial (phase-difference) cues** instead of from a noise-variance estimate, which is unreliable in adverse noise environments.

## Motivation

Classical a priori SNR estimation chains a recursively tracked noise variance to a decision-directed (DD) update. In adverse noise the noise-variance estimate itself becomes unreliable, distorting the estimated clean speech. Dual-microphone spatial cues offer an alternative SNR information source: the phase difference between time-aligned channels reflects how much non-target-directional energy contaminates each time-frequency bin.

## Pipeline

The method (proposed for dual microphones with known target TDOA) proceeds in four stages:

1. **TNR estimation** — the frequency-normalized phase difference $\Delta\tilde\psi$ of the time-aligned dual-microphone signals is converted into a [[concepts/target-to-non-target-directional-signal-ratio|target-to-non-target directional signal ratio (TNR)]] estimate via the closed form $\widehat{\mathrm{TNR}} = (1+\cos\Delta\tilde\psi)/(1-\cos\Delta\tilde\psi) = \cot^2(\Delta\tilde\psi/2)$, derived as the power ratio of delay-and-sum-beamformer and blocking-matrix transfer functions.
2. **Speech activity decision** — a statistical model-based log-likelihood ratio test (LRT; Sohn et al. 1999) decides target-speech presence per T-F bin under uncertainty, replacing binary masking's discontinuous hard decisions (the source of musical noise).
3. **DOA-based SNR** — defined as the ratio of expected target-directional speech power to expected noise power; the speech-side power comes from Wiener filtering with a DD-estimated a priori SNR, the noise-side power from speech-absence-gated recursive smoothing.
4. **Final SNR update** — a second DD step blends the DOA-based SNR with an a posteriori SNR from a speech-absence-gated noise variance estimate, combining the DOA cue with the temporal cue so that neither is a single point of failure.

The estimated SNR feeds a [[concepts/wiener-filter|Wiener filter]] spectral gain $G = \hat{\xi}/(1+\hat{\xi})$ applied to the reference microphone.

## Empirical Findings (Kim & Kim 2014)

- Much lower RMS error against true SNR than single-microphone DD estimation (500 Hz – 3 kHz).
- Highest SDR among {no processing, single-channel Wiener, SDB, GSC-PW, [[concepts/phase-error-based-filter|PEF]], ASBM, TNR-only} across 6 scenarios, SNRs 0–20 dB, RT60 up to 300 ms, and interference-speech/factory/vacuum-cleaner/white noise; also highest PESQ.
- The full LRT+DD machinery outperforms the TNR-only gain especially under reverberation — the raw phase-difference cue is reverberation-sensitive, the SNR machinery is not.
- Fails when target and noise share a DOA (Case 4: near-identical directions) — a fundamental limit of DOA cues; also degrades with target-DOA error outside a small window around zero.

## Related Concepts

- [[concepts/target-to-non-target-directional-signal-ratio|Target-to-Non-target Directional Signal Ratio (TNR)]] — spatial-cue precursor
- [[concepts/phase-error-based-filter|Phase-Error-Based Filter (PEF)]] — closest baseline
- [[concepts/wiener-filter|Wiener Filter]] — downstream spectral gain
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]] — source of the spatial cue
- [[concepts/voice-activity-detection|Voice Activity Detection]] — LRT-based activity decision inside the estimator
- [[concepts/speech-presence-probability|Speech Presence Probability]] — related soft-decision machinery
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — system context

## Related Sources

- [[sources/kim-2014-doa-based-snr-estimation|Kim & Kim 2014: DOA-Based SNR Estimation for Dual-Microphone Speech Enhancement]]
