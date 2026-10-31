---
type: source
created: 2026-10-31
updated: 2026-10-31
sources:
  - raw/papers/kuo-2006-anc-headphones/full-text.txt
  - https://doi.org/10.1109/TCST.2005.863667
  - zotero://select/items/0_HFSVG5EP
tags:
  - active-noise-control
  - adaptive-feedback
  - headphones
  - secondary-path-modeling
  - signal-processing
---

# Kuo, Mitra & Gan 2006: Active Noise Control System for Headphone Applications

**Authors**: [[entities/sen-m-kuo|Sen M. Kuo]], [[entities/sohini-mitra|Sohini Mitra]], [[entities/woon-seng-gan|Woon-Seng Gan]]
**Institutions**: Center for Acoustics and Vibration, Northern Illinois University, DeKalb, IL (Kuo, Mitra); School of Electrical and Electronics Engineering, Nanyang Technological University, Singapore (Gan)
**Venue**: IEEE Transactions on Control Systems Technology, Vol. 14, No. 2, pp. 331–335, March 2006
**Type**: journalArticle
**DOI**: [10.1109/TCST.2005.863667](https://doi.org/10.1109/TCST.2005.863667)
**Zotero**: [HFSVG5EP](zotero://select/items/0_HFSVG5EP)

## Summary

This paper presents the design and real-time implementation of an adaptive feedback ANC (AFANC) headphone, addressing the two practical barriers of the architecture — the correct placement of the error microphone and the intrusiveness of conventional secondary-path identification excitation. The optimal error-microphone location (of eight candidates) is found experimentally by minimizing dips and peaks in the measured secondary-path magnitude response, and is explained by the spectral filtering of the pinna. Music signals are shown to be viable excitation for adaptive secondary-path identification, achieving similar modeling quality to white noise and chirp. Implemented in assembly on a TMS320C32 DSP (8 kHz, 16-bit), the prototype cancels 50+ dB of sinusoidal noise up to 2 kHz and beats a high-end commercial ANC headphone (Bose QuietComfort 2) on real engine noise, especially at low-frequency harmonics.

## Problem Formulation

In feedback ANC headphones, only the error microphone is available — no reference microphone captures the primary noise $d(n)$ upstream. The AFANC algorithm must therefore estimate the primary noise and use it as the reference signal $x(n)$ for the control filter $W(z)$. Three coupled design problems arise:

1. **Reference synthesis**: the secondary-path estimate $\hat{S}(z)$ is used to reconstruct the reference: $\hat{x}(n) = e(n) + \hat{s}(n) * y(n)$, i.e. the internal-model-control route — the estimated primary noise equals the residual error plus the estimated anti-noise contribution.
2. **Stability constraint**: for perfect cancellation the adaptive filter converges to the optimum transfer function $W^{\mathrm{opt}}(z) = P(z)/S(z)$, so the system is unstable at any frequency $\omega_0$ where $|S(e^{j\omega_0})| \approx 0$ — FxLMS works properly at all frequencies only when the secondary-path magnitude response is flat. The secondary path is thus the optimization target.
3. **Modeling intrusiveness**: standard adaptive system identification of $S(z)$ uses white noise as excitation, which is annoying for headphone users — motivating a perceptually acceptable excitation signal.

## Methodology

### AFANC Algorithm

The AFANC system is the standard feedback-ANC instantiation of the FxLMS algorithm: the control signal is $y(n) = \mathbf{w}^{T}(n)\,\hat{\mathbf{x}}(n)$ over an $L$-tap filter, updated with the FxLMS rule $w(n+1) = w(n) + \mu\, e(n)\, \mathbf{x}'(n)$, where $\mathbf{x}'(n) = \hat{s}(n) * \hat{x}(n)$ is the filtered reference. The reference is synthesized internally (Problem 1 above), using the same $\hat{S}(z)$ model that pre-filters the weight update. The $M$-tap FIR secondary-path model $\hat{S}(z)$ is estimated by adaptive system identification.

### Error-Microphone Placement Optimization

The secondary-path transfer function $S(z)$ is dominated by acoustic propagation from the ear-cup loudspeaker to the error microphone, and is shaped by the spectral filtering of the outer ear (pinna): its asymmetrical cartilaginous structure imposes a unique set of delays, resonances, and diffractions per microphone position. Eight candidate error-microphone locations on the median plane around the ear-pad were measured (8 kHz sampling, 0–3.38 kHz band) with an HP3563A control-systems analyzer on a KEMAR mannequin:

- Locations #1–#4 (posterior ear) and #5–#8 (frontal ear) showed markedly dissimilar responses, consistent with the different cartilage/skin structure of the two regions; responses within #5–#8 were similar.
- **Position #8** (near the external auditory meatus, fitting naturally into the hollow) showed the flattest magnitude response with the fewest dips and peaks — the worst was position #2.
- The response measured at #8 matches the response measured by the KEMAR's ear-canal microphone, confirming that minimizing at #8 also minimizes noise at the hearing position — the actual perceptual target.

### Music as Identification Excitation

Instead of white noise or chirp, music is used as the excitation signal for adaptive system identification of $S(z)$. Analyzed music pieces show a systematic trade-off: those rich in frequency content span a narrower frequency range, and those spanning a wider range have lower frequency density. Frames of "O Fortuna" (Carmina Burana) are nearly flat over 0–4 kHz, making it a suitable excitation. The magnitude response of $\hat{S}(z)$ estimated with music closely matches the measured system, performing comparably to white noise and chirp.

## Experimental Setup

**Hardware**:

| Component | Detail |
|-----------|--------|
| Base headphone | Sennheiser HD 565 Ovation (modified: error mic added inside each ear-cup) |
| Error microphone | Omni-directional Realistic tie-pin microphone, embedded in ear-pad at position #8 |
| Pre-amplifier | Symetrix SX202 dual preamp |
| Loudspeaker amplifier | ONKYO stereo amplifier |
| DSP | TMS320C32 (Spectrum Signal Processing board), assembly-coded AFANC |
| ADC/DAC | 16-bit, 4-channel analog I/O board, third-order Butterworth anti-aliasing filters, 3.38 kHz cutoff |
| Sampling rate | 8 kHz |
| Mannequin | KEMAR with 1/2-inch Falcon-range B&K 4189 microphone inside ear cavity |
| Analyzer | HP3563A Control Systems Analyzer (spectra + $S(z)$ measurement) |
| Noise source | Primary loudspeaker 27 cm in front / 24 cm below KEMAR; Sony DAT deck for recorded engine noises |
| Comparison device | Bose QuietComfort 2 (high-end commercial ANC headphone) |

**Algorithm parameters**:

| Parameter | Value |
|-----------|-------|
| Secondary-path model $\hat{S}(z)$ length $M$ | 65 taps |
| Secondary-path modeling step size | 0.05 |
| Control filter $W(z)$ length $L$ | 110 taps |
| Control step size $\mu$ | 0.3 |

Primary noises: sinusoids 0–2 kHz in 100 Hz steps (HP 33120A generator), and real engine noise recorded at 2200 rpm and 3700 rpm. All performance numbers are measured by the microphone inside the KEMAR's ear canal (proxy for human perception), comparing ANC OFF vs ON.

## Results

**Sinusoidal noise**: net noise cancellation decreases with frequency but remains **more than 50 dB** up to 2 kHz.

**Engine noise at 3700 rpm** (first three harmonics; NIU prototype vs Bose QC2):

| Harmonic | NIU AFANC | Bose QC2 |
|----------|-----------|----------|
| 61 Hz | **20.906 dB** | 0.685 dB |
| 122 Hz | **18.387 dB** | 8.284 dB |
| 183 Hz | **16.293 dB** | 14.575 dB |

**Engine noise at 2200 rpm** (four harmonics):

| Harmonic | NIU AFANC | Bose QC2 |
|----------|-----------|----------|
| 76 Hz | **14.371 dB** | 0.919 dB |
| 116 Hz | **25.627 dB** | 6.955 dB |
| 156 Hz | **26.767 dB** | 12.25 dB |
| 196 Hz | 13.197 dB | 13.409 dB |

The designed headphone achieves marked improvement over the commercial headphone at all harmonics, especially at low frequencies (e.g., 61 Hz: 20.9 dB vs 0.7 dB).

## Key Contributions

1. **Error-microphone placement rule**: experimentally identifies the optimal error-microphone location inside an ear-cup as the position with the flattest secondary-path magnitude response (position #8, near the external auditory meatus), and validates that this location also correlates with the response at the ear-canal hearing position — making flatness of $S(z)$ a practical placement criterion for feedback ANC headphones.
2. **Pinna spectral-filtering explanation**: attributes the position-dependence of $S(z)$ to the cartilage structure of the outer ear (anterior folds vs posterior rim), grounding the placement rule acoustically.
3. **Music as secondary-path identification excitation**: demonstrates that music (specifically spectrally dense frames, e.g. "O Fortuna") can replace white noise/chirp for adaptive system identification of $S(z)$ with comparable accuracy — removing the annoyance of conventional training signals for headphone users.
4. **Complete real-time prototype**: a single-error-microphone-per-ear-cup, low-cost, compact AFANC headphone on a TMS320C32 DSP that outperforms a leading commercial ANC headphone on real engine noise, especially at low-frequency harmonics.

## Related Concepts

- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/adaptive-feedback-control|Adaptive Feedback Control]]
- [[concepts/internal-model-control|Internal Model Control]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/system-identification|System Identification]]
- [[concepts/head-related-transfer-function|Head-Related Transfer Function]]
- [[concepts/active-noise-control|Active Noise Control]]

## Related Synthesis

- [[synthesis/anc-architecture-evolution|ANC Architecture Evolution]]
- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]
- [[synthesis/secondary-path-modeling-evolution|Secondary Path Modeling Evolution]]
