---
type: concept
created: 2026-08-28
updated: 2026-08-28
sources:
  - raw/papers/kim-2014-doa-based-snr-estimation/full-text.txt
tags:
  - speech-enhancement
  - spatial-cues
  - doa
  - array-processing
---

# Target-to-Non-target Directional Signal Ratio (TNR)

The **Target-to-Non-target Directional Signal Ratio (TNR)** is the power ratio between the target-directional enhanced and rejected signals in a dual-microphone speech enhancement system — the spatial-cue analogue of the SNR, defined per time-frequency bin (Kim & Kim, Interspeech 2013; IEEE/ACM TASLP 2014).

## Definition

With $S(k,\ell)$ the target-directional source and $B(k,\ell)$ the non-target directional signal at frequency bin $k$ and frame $\ell$:

$$
\mathrm{TNR}(k,\ell) = \frac{|S(k,\ell)|^2}{|B(k,\ell)|^2}
$$

A Wiener-style spectral gain follows directly, $G = \mathrm{TNR}/(\mathrm{TNR} + \alpha)$, where the over-subtraction-style constant $\alpha$ trades off noise reduction at low TNR against target distortion at high TNR (higher $\alpha$ helps at low input TNR, hurts at high input TNR).

## Phase-Difference Estimation (Kim & Kim 2014)

After time-aligning the second microphone to the first using the known target TDOA, the frequency-normalized phase difference $\Delta\tilde\psi$ between the two channels isolates the non-target contribution. The TNR estimate is the power ratio of the delay-and-sum beamformer (DSB) and blocking-matrix (BM) transfer functions:

$$
\widehat{\mathrm{TNR}} = \frac{|H_{\mathrm{DSB}}|^2}{|H_{\mathrm{BM}}|^2} = \frac{1 + \cos\Delta\tilde\psi}{1 - \cos\Delta\tilde\psi} = \cot^2\!\left(\frac{\Delta\tilde\psi}{2}\right)
$$

- Target-dominant bin → aligned channels nearly identical → $\Delta\tilde\psi \to 0$ → TNR → ∞
- Non-target-dominant bin → large phase difference → small TNR

This exact form refines the [[concepts/phase-error-based-filter|phase-error-based filter (PEF)]] approximation $\mathrm{TNR} \approx 1/(\Delta\psi)^2$, which shares only the small-error asymptotic and distorts target-directional speech at high TNR. In Kim & Kim's SDR evaluation, the exact TNR gain beat PEF at low SNRs for *every* value of $\alpha$ (best $\alpha \approx 3$ at low SNR vs. $\approx 1$ at high SNR; PEF needs $\alpha \approx 5$).

## Role in DOA-Based SNR Estimation

The TNR estimate is the spatial-cue input to [[concepts/doa-based-snr-estimation|DOA-based SNR estimation]], which converts it into a speech-presence-uncertainty-aware SNR. The TNR-only gain is already competitive (beats SDB, GSC-PW, PEF in SDR) but is sensitive to reverberation; the full DOA-based SNR machinery restores robustness.

## Related Concepts

- [[concepts/doa-based-snr-estimation|DOA-Based SNR Estimation]] — downstream consumer of the TNR cue
- [[concepts/phase-error-based-filter|Phase-Error-Based Filter (PEF)]] — crude TNR approximation baseline
- [[concepts/beamforming|Beamforming]] — DSB/BM transfer functions provide the estimator
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — system context
- [[concepts/speech-presence-probability|Speech Presence Probability]] — uncertainty-aware successor stage

## Related Sources

- [[sources/kim-2014-doa-based-snr-estimation|Kim & Kim 2014: DOA-Based SNR Estimation for Dual-Microphone Speech Enhancement]]
