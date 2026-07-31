---
type: concept
created: 2026-08-01
updated: 2026-08-01
sources:
  - raw/papers/liu-2025-pcen-mask-vad-speech-enhancement/full-text.md
tags:
  - audio-processing
  - signal-processing
  - feature-extraction
  - speech-enhancement
  - training-target
---

# Per-Channel Energy Normalization (PCEN)

**Per-Channel Energy Normalization (PCEN)** is a spectral-normalization technique that, for each frequency channel (band) of a spectrogram, divides the instantaneous energy by a quantity proportional to that channel's time-averaged energy, then applies a power-law nonlinearity. The result is a loudness-normalized spectrogram in which slowly varying background components are suppressed and the per-band dynamic range is compressed.

## Definition

Given a band-energy spectrogram $S(t,f)$, PCEN is computed independently per band $f$ as a function of time $t$:

$$PCEN(t,f) = \left(\frac{S(t,f)}{(\varepsilon + M(t,f))^{\alpha}} + \delta\right)^{r} - \delta^{r}$$

where the running average $M(t,f)$ follows a first-order recursion:

$$M(t,f) = (1-s)\cdot M(t-1,f) + s\cdot S(t,f)$$

The parameters are: $\varepsilon$ (stabilization, prevents division by zero), $\alpha$ (gain, exponent on the denominator), $\delta$ (bias, offset), $r$ (power, compresses dynamic range), and $s$ (smoothing factor, controls the time constant of $M$).

## Interpretation as Log-Domain High-Pass Filtering

Rewriting the core term as $\exp\!\big(\log S(t,f) - \alpha\log(\varepsilon + M(t,f))\big)$ shows that PCEN subtracts the slowly varying $M(t,f)$ from $\log S(t,f)$. Because $M(t,f)$ is a low-pass (smoothed) version of $S(t,f)$, this subtraction is a **high-pass filter in the log-energy domain**: it removes slowly varying components — which, in a "clean" speech recording, are dominated by stationary noise (recording-equipment noise, room noise) — while preserving fast speech transients.

## Effect on Dynamic Range

Raw band energies $S(t,f)$ vary widely across frequency (low-frequency bands are typically much louder than high-frequency bands), so a single global threshold on $S(t,f)$ over-suppresses high-frequency speech. Because $M(t,f)$ tracks each band's own average, the division in PCEN **normalizes each band's loudness**, yielding a much narrower dynamic range in which every band sits at a comparable level. A global constant can then serve as a valid per-band threshold.

## Parameter Values

Typical values (as used in the Liu et al. 2025 patent and consistent with librosa's `pcen` defaults):

| Parameter | Symbol | Typical value |
|---|---|---|
| Stabilization | $\varepsilon$ | $10^{-6}$ |
| Gain | $\alpha$ | 0.98 |
| Bias | $\delta$ | 2 |
| Power | $r$ | 0.5 |
| Smoothing factor | $s$ | 0.025 (conventional); 0.2 (Liu et al. 2025) |

The smoothing factor $s$ is the most application-sensitive parameter: a smaller $s$ removes more stationary noise but blurs speech harmonics. Liu et al. 2025 report that $s = 0.2$ (rather than the conventional 0.025) works better for their speech-enhancement training-target application.

## Applications

### Robust Audio Feature Front End

PCEN originated as a robust front-end feature for sound-event detection and keyword spotting, where it improves robustness to background-noise level variation across frequency channels (Lostanlen et al. 2019).

### Training-Time Mask Thresholding for Speech Enhancement (Liu et al. 2025)

A distinctive use introduced by [[sources/liu-2025-pcen-mask-vad-speech-enhancement|Liu et al. 2025 (Dolby patent)]]: PCEN is computed on the **clean training target** $S(t,f)$ and used only to decide where to zero the [[concepts/ideal-ratio-mask|ideal ratio mask]] (IRM). If $PCEN(t,f) < TH_\text{band}$ (e.g., $10^{-5}$), the IRM for that band is set to 0; otherwise the IRM is left as the standard ratio. This trains the DNN to remove stationary noise buried in the "clean" target and to ignore perceptually insignificant low-energy bands. **PCEN does not replace $S(t,f)$ inside the IRM formula** — doing so would lose speech — and it is applied **only at training time**, never at inference.

### Training-Time VAD (PCEN-VAD)

The same patent builds a frame-level [[concepts/voice-activity-detection|voice activity detector]] by summing band-level PCEN energies within a frame, $E(t) = \sum_f PCEN(t,f)$, and thresholding at $TH_\text{frame} \approx TH_\text{band}\cdot N$ (where $N$ is the number of bands). The VAD decision then gates an asymmetric loss function: non-speech frames have their IRM set to 0 and a sign-flipped error term that drives the predicted mask aggressively toward 0.

## Related Concepts

- [[concepts/ideal-ratio-mask|Ideal Ratio Mask (IRM)]] — the training target that PCEN-based thresholding modifies
- [[concepts/voice-activity-detection|Voice Activity Detection]] — PCEN-VAD is a training-time VAD used to gate a speech-enhancement loss
- [[concepts/minimum-statistics|Minimum Statistics]] — another approach to separating stationary noise from speech via spectral minima

## Related Sources

- [[sources/liu-2025-pcen-mask-vad-speech-enhancement|Liu et al. 2025: PCEN-Based Mask Thresholding and VAD for DNN Speech Enhancement Training]] — repurposes PCEN as a training-time threshold oracle and VAD
