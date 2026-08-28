---
type: source
created: 2026-08-28
updated: 2026-08-28
sources:
  - raw/papers/kim-2014-doa-based-snr-estimation/full-text.txt
  - https://doi.org/10.1109/TASLP.2014.2360646
  - zotero://select/items/0_UY66URYH
tags:
  - speech-enhancement
  - multi-channel
  - array-processing
  - doa
  - snr-estimation
  - spatial-cues
  - dual-microphone
---

# Kim & Kim 2014: DOA-Based SNR Estimation for Dual-Microphone Speech Enhancement

**Authors**: [[entities/seon-man-kim|Seon Man Kim]] (ISVR, University of Southampton), [[entities/hong-kook-kim|Hong Kook Kim]] (GIST)
**Venue**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 22, no. 12, pp. 2207–2217, December 2014
**Type**: Journal article
**DOI**: [10.1109/TASLP.2014.2360646](https://doi.org/10.1109/TASLP.2014.2360646)
**Zotero**: [UY66URYH](zotero://select/items/0_UY66URYH)

> **Extraction note**: MinerU was unavailable and pdftotext is not installed on this machine, so the text was extracted with PyMuPDF (text mode). Inline equation contents and figure graphics were lost in extraction; equations below are reconstructed from the surrounding prose at a descriptive level.

## Summary

This paper proposes estimating the a priori SNR for a Wiener-filter speech enhancer not from a noise-variance estimate (unreliable in adverse noise) but from **spatial cues**: the phase difference between dual-microphone signals is first converted into a target-to-non-target directional signal ratio (TNR), and the TNR is then turned into a **DOA-based SNR** via a statistical model-based log-likelihood ratio test (LRT) for target speech activity followed by a decision-directed (DD) update. The resulting dual-microphone system outperforms single-microphone Wiener filtering and conventional dual-microphone methods (super-directive beamformer, GSC + post-filter, phase-error-based filter, and angular-spectrum-based masking) in SDR and PESQ at SNRs from 0 to 20 dB, including reverberant conditions up to RT60 = 300 ms.

## Problem Formulation

Reliable SNR estimation is the crux of short-term spectral amplitude (STSA) speech enhancement. Conventional estimation chains a noise-variance estimate to an a posteriori SNR and a DD a priori SNR update; when the noise variance estimate is unreliable in adverse noise, the estimated clean speech is distorted. Dual-microphone alternatives exploit the phase difference between channels, but each has a failure mode:

- **Binary masking** (dominant-source-per-T-F-bin assumption) suffers from musical noise due to discontinuous zero-padding, and the sparseness assumption breaks in real environments.
- **Beamformers** (super-directive beamformer, SDB; generalized sidelobe canceller, GSC) have spatial directivity patterns (SDPs) constrained by the number of microphones — a dual-microphone SDB underperforms masking-based methods. Post-filtering on the beamformer output behaves similarly to phase-error-based filtering (PEF).
- **ICA-based BSS** requires the number of sources ≤ number of microphones, which is impractical.
- **PEF** (Aarabi & Shi 2004) reduces non-target directional noise well at low SNR but distorts target-directional speech at high SNR, because it uses only the DOA cue and approximates TNR crudely by the inverse squared phase difference.

The signal model assumes a far-field target-directional source (direct path only) plus non-target directional sources; after time-aligning the second microphone to the first via the known target TDOA, the phase difference between the two channels reflects the non-target content. The target DOA is assumed known a priori (e.g., interlocutor-facing hearing-aid wearer, driver in car telematics), or estimable beforehand via GCC-PHAT / SRP-PHAT localization.

## Methodology

The proposed pipeline (Fig. 2 of the paper): phase difference → TNR estimate → DOA-based SNR → final SNR estimate → Wiener spectral gain.

### TNR Estimation from Phase Differences

Using the delay-and-sum beamformer (DSB) transfer function $H_{\mathrm{DSB}} = \tfrac{1}{2}(1 + e^{j\Delta\tilde\psi})$ (target-enhancing) and the blocking matrix (BM) transfer function $H_{\mathrm{BM}} = \tfrac{1}{2}(1 - e^{j\Delta\tilde\psi})$ (target-rejecting), both computed from the **frequency-normalized** phase difference $\Delta\tilde\psi$ of the time-aligned dual-microphone signals, the TNR estimate is the power ratio of the two:

$$
\widehat{\mathrm{TNR}} = \frac{|H_{\mathrm{DSB}}|^2}{|H_{\mathrm{BM}}|^2} = \frac{1 + \cos\Delta\tilde\psi}{1 - \cos\Delta\tilde\psi} = \cot^2\!\left(\frac{\Delta\tilde\psi}{2}\right)
$$

When the target dominates a T-F bin, the aligned channels are nearly identical ($\Delta\tilde\psi \to 0$) and TNR → ∞; non-target dominance gives a large phase difference and small TNR. A TNR-based Wiener-style gain $G = \mathrm{TNR}/(\mathrm{TNR} + \alpha)$ (with over-subtraction factor $\alpha$) already outperforms PEF, which approximates TNR by $1/(\Delta\psi)^2$ — the same small-error asymptotic but crude away from it. This TNR estimator extends the authors' Interspeech 2013 work.

### DOA-Based SNR Estimation

Each directional component is decomposed into target speech plus directional noise, yielding two hypotheses ($H_0$: speech absent, $H_1$: speech present) on the T-F bin. The **DOA-based SNR** is defined as the ratio of expected target-directional speech power to expected noise power under speech presence. Its estimation combines:

1. **Speech activity decision** — a statistical model-based log-likelihood ratio test (Sohn et al. 1999) decides $H_1$ vs. $H_0$ per T-F bin.
2. **Noise-side power** — recursively smoothed (only when $H_0$ holds).
3. **Speech-side power** — Wiener filtering with a DD-estimated a priori SNR.
4. **Final SNR update** — a second DD step blends the DOA-based SNR with an a posteriori SNR computed from a speech-absence-gated noise variance estimate, making the final estimate robust even when the DOA cue is weak.

### Target Speech Reconstruction

The estimated SNR feeds a Wiener spectral-gain attenuator $G = \hat{\xi}/(1+\hat{\xi})$, applied to the first microphone's noisy spectrum and inverse-transformed to the time domain.

## Experimental Setup

| Item | Detail |
|:-----|:-------|
| Room simulation | Image source method (ISM) with diffused decay model; RT60 ∈ {0, 100, 200, 300} ms |
| Array | Dual microphones, 4 cm spacing, height 1.5 m |
| Targets | 10 TIMIT utterances (5 male, 5 female); 2 target azimuths on a 1 m-radius circle (S1, S2) |
| Interferers | 4 TIMIT speech sources at 2 m radius (N1–N4); also factory, vacuum cleaner, white noise (NOISEX-92) |
| Scenarios | 6 cases: S2-N1/N2/N3 (Cases 1–3, easy), S1-N3 (Case 4, hardest — near-identical DOAs), S1-N4-N1 and S2-N3-N1 (Cases 5–6, two-noise mixtures) |
| SNRs | 0, 5, 10, 15, 20 dB; 50 test signals per scenario per RT60 |
| Signal processing | 8 kHz sampling, 32 ms cosine windows, half-overlapped; TDOAs known a priori |
| Metrics | SDR, SIR, SAR (least-square projection decomposition); PESQ (ITU-T P.862) |
| Baselines | No processing, single-channel Wiener (DD), SDB, GSC + post Wiener filter (GSC-PW), PEF, ASBM |
| Tuning | Smoothing/over-subtraction parameters fixed per SDR maximization; e.g., TNR gain best at $\alpha \approx 1$ (high SNR) / $\approx 3$ (low SNR) vs. PEF at $\alpha \approx 5$ |

## Results

- **TNR vs. PEF (Fig. 4)**: at low SNRs the proposed TNR gain gives higher SDR than PEF for *all* values of $\alpha$; at high SNRs both peak (TNR at $\alpha \approx 1$, PEF at $\alpha \approx 5$), confirming PEF's high-SNR target distortion.
- **SNR estimation accuracy (Fig. 6, Table II)**: at 1/2/3 kHz the proposed SNR track follows the true SNR far more closely than the conventional single-microphone DD estimate; RMS errors from 500 Hz to 3 kHz are much smaller throughout.
- **SDR/SIR/SAR across scenarios (Fig. 7)**: the proposed DOA-based SNR method achieves the highest SDR (the global measure) in essentially all scenarios; in Cases 1–2 some conventional methods edge it out on SIR alone. In Case 4 (target and noise from nearly the same direction) all DOA-cue methods collapse to similar SDR — DOA ambiguity is a fundamental limitation. The TNR-only variant already beats SDB, GSC-PW, and PEF everywhere except Case 4, but not ASBM.
- **DOA error robustness (Figs. 8–9)**: performance is best near zero DOA error; SDB is nearly DOA-error-invariant (broadside dual-mic directivity is flat), while GSC-PW, PEF, ASBM, and the proposed methods degrade with DOA error. Since GCC/SRP localization is reliable within the small error range where the proposed method dominates, the method is judged practical.
- **Reverberation (Table III)**: all methods degrade with RT60, but the proposed DOA-based SNR method yields the highest SDR improvement for all SNRs when RT60 < 300 ms; SDB is consistently worst; ASBM is the best conventional method. Notably, the full DOA-based SNR method outperforms the TNR-only method — the DD/LRT machinery makes the estimate robust to reverberation, which the raw TNR cue is sensitive to.
- **Noise types (Table IV)** and **PESQ (Table V)**: the proposed method gives the highest improved SDR under factory, vacuum-cleaner, and white noise at both low and high SNRs, and the highest PESQ scores across all noise conditions, beating ASBM (the strongest conventional competitor).

## Key Contributions

1. **TNR estimator from phase differences** — a closed-form target-to-non-target directional signal ratio obtained as the DSB/BM transfer-function power ratio (equivalently $\cot^2(\Delta\tilde\psi/2)$) of the time-aligned dual-microphone signals, generalizing the authors' Interspeech 2013 estimator.
2. **DOA-based SNR** — a new SNR definition and estimator that converts the spatial TNR cue into a speech-presence-uncertainty-aware SNR via a statistical model-based LRT decision and two decision-directed updates, replacing unreliable noise-variance-driven a priori SNR estimation.
3. **Wiener integration** — the DOA-based SNR slots directly into a Wiener spectral-gain attenuator, combining temporal and DOA cues rather than either alone.
4. **Comprehensive dual-microphone benchmark** — SDR/SIR/SAR + PESQ comparison against SDB, GSC-PW, PEF, and ASBM across 6 scenarios, 5 SNRs, 4 RT60s, and 4 noise types, with DOA-error sensitivity analysis.

## Limitations and Caveats

- Target DOA (TDOA) assumed known a priori; performance degrades outside a small DOA-error window, and Case 4 (co-located target and noise) defeats all DOA-cue methods.
- Far-field, direct-path modeling of the target; the TNR-only variant is sensitive to reverberation (mitigated, not eliminated, by the full DOA-based SNR machinery).
- Known-DOA simulation setup (no end-to-end localization); evaluation on simulated reverberant mixtures only.

## Related Concepts

- [[concepts/doa-based-snr-estimation|DOA-Based SNR Estimation]] — the paper's core contribution
- [[concepts/target-to-non-target-directional-signal-ratio|Target-to-Non-target Directional Signal Ratio (TNR)]] — spatial cue precursor
- [[concepts/phase-error-based-filter|Phase-Error-Based Filter (PEF)]] — closest baseline, distinctively formulated here via the TNR connection
- [[concepts/wiener-filter|Wiener Filter]] — spectral-gain stage consuming the estimated SNR
- [[concepts/beamforming|Beamforming]] — SDB baseline; DSB/BM transfer functions used as TNR machinery
- [[concepts/gsc-beamformer|GSC Beamformer]] — GSC-PW baseline
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]] — DOA cue and error sensitivity
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — system context
- [[concepts/voice-activity-detection|Voice Activity Detection]] — LRT-based speech activity decision inside the estimator
- [[concepts/speech-presence-probability|Speech Presence Probability]] — related soft-decision machinery
- [[concepts/image-source-method|Image Source Method]] — reverberant room simulation
- [[concepts/pesq|PESQ]] — perceptual quality metric
- [[concepts/ideal-binary-mask|Ideal Binary Mask]] — musical-noise failure mode of binary masking
- [[concepts/cocktail-party-problem|Cocktail-Party Problem]] — motivating problem

## Related Synthesis

- [[synthesis/deep-speech-enhancement|Deep Speech Enhancement]] — spatial-cue SNR estimation as a classical counterpart to learned multi-channel enhancement
- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — classical statistical-model branch of the MCSE family tree
