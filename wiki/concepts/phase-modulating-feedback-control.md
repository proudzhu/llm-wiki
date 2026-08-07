---
type: concept
created: 2026-08-07
updated: 2026-08-07
sources:
  - raw/papers/vanwaterschoot-2011-fifty-years-afc/full-text.md
tags:
  - acoustic-feedback
  - phase-modulation
  - lptv-filter
  - sound-reinforcement
aliases:
  - PFC
  - Phase-Modulation Feedback Control
---

# Phase-Modulating Feedback Control (PFC)

**Phase-modulating feedback control (PFC)** is an [[concepts/acoustic-feedback|acoustic feedback]] control method that inserts a linear periodically time-varying (LPTV) filter in the electroacoustic forward path to smooth the loop gain and bypass the phase condition of the Nyquist stability criterion. It is one of the four categories of automatic acoustic feedback control in the [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] taxonomy.

## Principle

The Nyquist instability condition requires *both* $|GF| \geq 1$ *and* $\angle GF = n \cdot 2\pi$. PFC inserts a modulation filter $H(q,t)$ in the forward path so that the loop response becomes periodically time-varying. The LPTV frequency response decomposes into modulation sidebands whose gains are weighted by Bessel functions of the first kind $J_n(\beta)$. The design places $J_0(\beta)$ at a zero, suppressing the carrier (unshifted) component so that no single frequency simultaneously satisfies both Nyquist conditions. The loop gain is effectively smoothed: the MSG is then determined by the *average* rather than the *peak* magnitude response.

## Realizations

All of the following are special cases of the LPTV filter framework unified by Svensson and Nielsen & Svensson:

| Variant | Modulation | Typical parameter | MSG increase |
|---------|-----------|-------------------|--------------|
| **Frequency shifting (FS)** | Frequency shift by $f_m$ Hz | $f_m = 5$ Hz (Schroeder) | up to 14 dB theoretical; ≤6 dB subjectively |
| **Sinusoidal phase modulation (PM)** | $\phi(t) = \beta \sin(\omega_m t)$ | $\beta$ at a zero of $J_0$ (e.g., 3.8); $f_m = 1$ Hz | 4–8 dB |
| **Frequency modulation (FM)** | conceptually equivalent to PM | — | up to 7 dB (Nishinomiya 1968) |
| **Amplitude modulation (AM)** | — | — | (part of the LPTV framework) |
| **Delay modulation (DM)** | time-varying delay $d(t)$ | $\Delta_\tau = 32$ samples | similar to PM |

The FS variant is implemented via single-sideband modulation (analog) or a truncated FIR Hilbert filter (digital). PM and DM are realized via a Hilbert-transform phase shifter and a linear-interpolation delay line, respectively.

## Properties

- **Deterministic**: PFC behavior is independent of the instantaneous source signal and gain — no detection or adaptation is involved.
- **Smoothing, not cancellation**: PFC does not remove the acoustic coupling; it only smooths the loop gain. The theoretical MSG-increase upper bound is the peak-to-average ratio of the feedback-path magnitude response, ~10 dB (Schroeder's statistical room-acoustics result).
- **Signal distortion**: the modulation is audible for sustained tones; FS of 5 Hz is claimed inaudible for speech and music, but FS/PFC is "less appropriate for sustained tones often occurring in audio signals" (Svensson). For PFC-PM and PFC-DM, a lower modulation frequency ($f_m = 1$ Hz) is used to limit distortion.
- **Multichannel**: Poletti showed the stability improvement from FS *reduces* as the number of channels increases — a discouraging result for multichannel PFC.

## Position Among Feedback Control Methods

PFC is one of the three methods evaluated head-to-head in van Waterschoot & Moonen 2011 (the others being [[concepts/notch-filter-based-howling-suppression|NHS]] and [[concepts/adaptive-feedback-cancellation|AFC]]). In the comparative evaluation, PFC yields the lowest MSG increase (mean ΔMSG ~1 dB, max ~4 dB) but is fully deterministic and reliable on speech (0% HOP). On audio, PFC-FS catastrophically fails (52% HOP) because sustained violin tones are destabilized; PFC-PM is the preferred PFC variant overall.

PFC is also used as a **decorrelator** inside [[concepts/adaptive-feedback-cancellation|AFC]] (the AFC-FS variant), where the LPTV filter smooths the loop gain as a beneficial side effect while reducing closed-loop identification bias — see [[concepts/decorrelation-for-afc|Decorrelation for AFC]].

## Related Concepts

- [[concepts/acoustic-feedback|Acoustic Feedback]] — the problem PFC addresses
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — the metric PFC increases by loop-gain smoothing
- [[concepts/frequency-shift-feedback-cancellation|Frequency Shift Feedback Cancellation]] — FS as a PFC variant and as an AFC decorrelator
- [[concepts/adaptive-feedback-cancellation|Adaptive Feedback Cancellation (AFC)]] — the competing room-modeling method; AFC-FS reuses PFC as a decorrelator
- [[concepts/notch-filter-based-howling-suppression|Notch-Filter-Based Howling Suppression (NHS)]] — the competing gain-reduction method
- [[concepts/decorrelation-for-afc|Decorrelation for AFC]] — PFC as in-loop decorrelation

## Related Sources

- [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] — the survey formalizing PFC as a category and unifying PM/FM/AM/DM/FS as LPTV filters
