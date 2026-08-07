---
type: concept
created: 2026-08-07
updated: 2026-08-07
sources:
  - raw/papers/williams-2014-acoustic-feedback-elimination/full-text.md
tags:
  - acoustic-howling
  - howling-detection
  - signal-processing
  - ballistics
  - fft
---

# Ballistics-Based Howling Detection

**Ballistics-based howling detection** is a [[concepts/howling-detection|howling detection]] (HD) technique that discriminates feedback tones from wanted music/speech by exploiting the *persistence* of feedback versus the *transience* of wanted signals. Each FFT magnitude-squared bin is passed through an asymmetric per-bin digital filter with a gradual attack and an instantaneous (zero) release. Persistent tones (feedback) accumulate over multiple FFT frames into a "prominence"; transient tones (music) release instantly and never build up. The technique is the candidate-selection front end of the [[concepts/notch-filter-based-howling-suppression|NHS]] patent [[sources/williams-2014-acoustic-feedback-elimination|Williams 2014]] (US 8,634,575 B2), and is a concrete instance of the "ballistics" candidate-selection step mentioned but not elaborated in [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]].

## Problem and Motivation

In a PA/sound-reinforcement system, [[concepts/acoustic-feedback|acoustic feedback]] produces a sustained pure tone that grows over time. Wanted musical signals also contain tonal components, but they are typically transient — notes come and go. A howling detector must distinguish the two. The feedback signature exploited here is **temporal persistence at a stable frequency**: a feedback tone stays in the same FFT bin at the same magnitude for many consecutive frames, whereas a musical tone migrates across bins (melody) or decays (note offsets).

A simple running average does not separate the two well, because it smooths both attack and release symmetrically — a sustained musical note would build up just like feedback. The ballistics filter breaks this symmetry by making the release instantaneous: any dip in the bin magnitude (as a musical note decays or moves) resets the stored value immediately, so only tones that stay continuously high can accumulate.

## The Asymmetric Per-Bin Filter

For each FFT magnitude-squared bin, maintain a stored value `OLD_VALUE` across frames. On each new FFT frame, with `NEW_VALUE` the current bin magnitude-squared:

$$
\text{OLD\_VALUE} \leftarrow
\begin{cases}
(\text{NEW\_VALUE} - \text{OLD\_VALUE}) \cdot K + \text{OLD\_VALUE}, & \text{NEW\_VALUE} > \text{OLD\_VALUE} \quad \text{(attack)} \\
\text{NEW\_VALUE}, & \text{NEW\_VALUE} \leq \text{OLD\_VALUE} \quad \text{(release)}
\end{cases}
$$

with the attack coefficient

$$
K = 1 - (1 - \text{Threshold})^{1/(t \cdot F_{fs})}.
$$

Here $t$ is the time to reach `Threshold` (a fractional value, e.g. 0.5) of the target, $F_{fs}$ is the FFT frame rate (e.g. 11.7 Hz for a 4096-point FFT at 48 kHz), and `Threshold` is the fraction of the target value at which the time constant is calibrated.

### Asymmetry Is the Point

- **Attack**: gradual, first-order low-pass — the stored value takes several frames to catch up to a newly loud bin. A tone must stay loud *continuously* for `OLD_VALUE` to build up.
- **Release**: instantaneous — any drop in the bin magnitude is reflected in `OLD_VALUE` on the very next frame. A transient dip (note offset, vibrato, melodic movement) resets the accumulator.

The result is that `OLD_VALUE` acts as a "how long has this bin been continuously loud" detector. Feedback (continuous) saturates it; music (intermittent) does not.

## Frequency-Dependent Time Constants

A single time constant is suboptimal across the audio band:

- **Low frequencies**: bass notes legitimately persist for seconds. A short time constant would falsely flag them as feedback. Williams uses **2 s** at the low-frequency end.
- **High frequencies**: high-frequency feedback builds faster, is more alarming to the audience, and is more likely to damage equipment (tweeters). A long time constant would delay suppression dangerously. Williams uses **200 ms** at the high-frequency end.

The time constant is defined as the time to reach 6 dB below the threshold value (i.e. 0.5 of the target), matching standard audio-dynamics conventions.

## Position in the NHS Pipeline

The ballistics filter sits between the magnitude-squared stage and the prominence search in the candidate-frequency selection process:

1. FFT (4096-point, ~85 ms frame rate)
2. Magnitude-squared per bin
3. Mean-square (per-frame energy reference)
4. **Ballistics** ← this concept
5. Prominence search (top-N `OLD_VALUE`s)
6. Threshold detection (absolute SPL + relative-to-mean)
7. → Implementation: [[concepts/trial-and-verify-notch-insertion|trial-and-verify notch insertion]]

The output of the ballistics stage is what the patent calls "prominences" — bins whose `OLD_VALUE` has accumulated to a high level because the underlying tone has been persistent.

## Discrimination Behavior

![[raw/papers/williams-2014-acoustic-feedback-elimination/figures/cec2220a1a50085bb6454c120d94a83ff668d680452a73f35da5d69619bfd31c.jpg|FIG. 7a — Ballistics response with a music signal]]
*Figure 7a: Ballistics response for a music signal — rapidly varying magnitudes cause the stored value to release instantly, so no prominence builds up.*

![[raw/papers/williams-2014-acoustic-feedback-elimination/figures/936467ff026593d474c66e1f406b5da84ed5c6f918b3048d3fa6615ca06f1e8c.jpg|FIG. 7b — Ballistics response with a feedback signal]]
*Figure 7b: Ballistics response for a feedback signal — the lingering tone builds up over multiple frames until the stored value reaches the threshold, forming a "prominence."*

![[raw/papers/williams-2014-acoustic-feedback-elimination/figures/8468ad0578c0602c7ef5eb6912abf28cceb04bceb9f4e838b33df75db8868fa2.jpg|FIG. 6 — Ballistics process flow]]
*Figure 6: Ballistics subroutine — attack branch applies the first-order filter with coefficient K; release branch replaces the stored value directly.*

## Properties

- **Amplitude-dependent attack rate**: the per-frame increment $(\text{NEW} - \text{OLD}) \cdot K$ is larger for louder tones, so high-level feedback reaches the threshold faster than low-level feedback. This matches the operational priority — louder feedback is more urgent.
- **Pure-tone bias**: because the filter operates per-bin, only tones that stay in the *same* bin accumulate. Moving tones (melody, vibrato spanning multiple bins) release. This reinforces the relative threshold's pure-tone bias.
- **No explicit statistical model**: unlike [[concepts/howling-detection-features|HD features]] such as NINOS² or IPMP, ballistics does not model the signal statistics; it is a purely temporal persistence filter.

## Limitations

- **Sustained musical notes**: a held pure tone (e.g. a long violin sustain, or a test tone) will accumulate just like feedback and clear the ballistics stage. The patent relies on the downstream [[concepts/trial-and-verify-notch-insertion|trial-and-verify]] step to reject these false candidates.
- **No early-howling detection**: a feedback tone must build up in `OLD_VALUE` over several frames before it becomes a candidate, so very early/low-energy howling (the regime targeted by [[concepts/ninosp2-transposed|NINOS²-T]] in [[sources/mounir-2025-robust-early-howling-detection-sparsity|Mounir et al. 2025]]) is structurally excluded — the same limitation as all candidate-based HD.
- **Single-bin assumption**: very loud feedback that splatters across adjacent bins (e.g. due to loudspeaker clipping) may not accumulate efficiently in any single bin.

## Related Concepts

- [[concepts/howling-detection|Howling Detection]] — the broader problem this technique solves
- [[concepts/howling-detection-features|Howling Detection Features]] — spectral/statistical HD features (a different family of approaches)
- [[concepts/notch-filter-based-howling-suppression|Notch-Filter-Based Howling Suppression (NHS)]] — the solution scheme this front end feeds
- [[concepts/trial-and-verify-notch-insertion|Trial-and-Verify Notch Insertion]] — the downstream verification step that rejects false candidates from the ballistics front end
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the problem being detected
- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — broader AHS context

## Related Sources

- [[sources/williams-2014-acoustic-feedback-elimination|Williams 2014]] — introduces the ballistics-based HD front end (US 8,634,575 B2)
- [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] — surveys NHS and mentions ballistics as an optional candidate-selection preprocessing step (§3.2)
