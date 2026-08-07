---
type: source
created: 2026-08-07
updated: 2026-08-07
sources:
  - raw/papers/williams-2014-acoustic-feedback-elimination/full-text.md
  - https://patents.google.com/patent/US8634575B2/en
  - zotero://select/items/0_BGTSGWNK
tags:
  - acoustic-feedback
  - acoustic-howling
  - notch-filter
  - howling-detection
  - signal-processing
  - patent
  - pa-system
---

# Williams 2014: System for Elimination of Acoustic Feedback

- **Inventor**: [[entities/paul-robert-williams|Paul Robert Williams]] (Stevenage, GB)
- **Assignee**: Harman International Industries Limited (Chester, GB)
- **Type**: U.S. Patent
- **Patent No.**: US 8,634,575 B2
- **Filed**: Oct. 27, 2009 (divisional of Ser. No. 09/658,538, filed Sep. 9, 2000, now Pat. No. 7,613,529)
- **Granted**: Jan. 21, 2014
- **Prior Publication**: US 2010/0046768 A1 (Feb. 25, 2010)
- **Class.**: USPC 381/93; 381/94.3
- **Claims**: 20 (1 method, 1 system-with-instructions, 1 means-plus-function)
- **URL**: <https://patents.google.com/patent/US8634575B2/en>
- **Zotero**: [BGTSGWNK](zotero://select/items/0_BGTSGWNK)

## Summary

A patent for automatically detecting and suppressing [[concepts/acoustic-feedback|acoustic feedback]] (howling) in sound-reinforcement systems. The system runs a two-rate digital signal processor: an audio-rate path applies a bank of time-domain notch filters, while a slower frame-rate path selects candidate feedback frequencies and verifies each one by inserting a shallow trial notch and measuring the amplitude reduction. The core novelty is a **ballistics-based howling detection** front end that exploits the persistence of feedback tones versus the transience of wanted music/speech: each FFT magnitude bin is fed through an asymmetric attack/release filter whose attack builds up gradually for persistent tones and whose release tracks transients instantly. A frequency-dependent time constant (200 ms at high frequencies, 2 s at low frequencies) further discriminates fast-building high-frequency feedback from sustained bass notes. Verified feedback is suppressed by deepening the notch in 6 dB steps; unverified candidates release the notch back to bypass. This is a concrete instance of [[concepts/notch-filter-based-howling-suppression|notch-filter-based howling suppression (NHS)]] in van Waterschoot & Moonen's "gain reduction" category.

## Problem Formulation

In a PA/sound-reinforcement system the microphone, amplifier, and loudspeaker form a closed loop. When the loop gain exceeds a threshold the system oscillates ("rings") and acoustic feedback persists until the loop gain is reduced. The patent targets the operator's manual task — gain riding or hand-tuned equalization — by automating both **detection** (which frequency is feeding back?) and **suppression** (apply just enough narrowband attenuation to stop it) without an operator in the loop. The design goal is to attenuate feedback while leaving wanted pure tones (sustained musical notes, speech) intact, since both share the spectral signature of a narrow persistent peak.

The closed-loop physics is the same one formalized in [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]]: the loop is unstable when $|GF| \geq 1$ and $\angle GF = n \cdot 2\pi$. Williams' patent does not model the loop directly; it detects the *symptom* (a persistent spectral prominence that grows over time) and breaks the magnitude condition locally at that frequency via a notch.

## Methodology

### Two-Rate Architecture

![[raw/papers/williams-2014-acoustic-feedback-elimination/figures/32704d3cab8bca00d9418340285a246497a7ca72c7b9f873ff79874b8518a626.jpg|FIG. 1 — Sound system block diagram]]
*Figure 1: Sound system — microphone → ADC → digital processor → DAC → amplifier → loudspeaker, with the digital processor removing feedback components.*

The processor (FIG. 2a: DSP + non-volatile memory + RAM; or FIG. 2b: DSP + microcontroller shared with a loudspeaker controller) runs two flows at different rates (FIG. 4):

- **Audio path (flow 402)** at the sample rate (e.g. one sample every 21 μs ≈ 48 kHz): receive → circular buffer → bank of notch filters 407 → DAC.
- **Analysis path (flow 404)** at the FFT frame rate (one frame every 85 ms ≈ 11.7 Hz): copy buffer → FFT → magnitude² → ballistics → prominence search → threshold detection → assignment → state machines → notch parameter generation.

The two flows are decoupled: filtering runs continuously at audio rate, parameters are refreshed periodically at frame rate.

![[raw/papers/williams-2014-acoustic-feedback-elimination/figures/d2eda36219b0e9a5764981f509df7fcf27c6796b5b346d2d2af564d103118eba.jpg|FIG. 4 — Functional block diagram of the two-process architecture]]
*Figure 4: The candidate-frequency selection process 406 (FFT → magnitude² → ballistics → prominence search → threshold detection) feeds the implementation process 408 (assignment → state machines → filter parameter generation), which drives the audio-path notch filters 407.*

### Candidate Frequency Selection (Process 406)

![[raw/papers/williams-2014-acoustic-feedback-elimination/figures/ae8af623fef8d9bb9a44f0c795a112bc1b26e6e8dd84cc65fbb7f71f75b311b5.jpg|FIG. 5 — Candidate frequency selection process]]
*Figure 5: Candidate frequency selection — FFT → magnitude² → mean-square → ballistics → prominence search → threshold detection.*

1. **FFT (410).** A 4096-point FFT is run on the buffered samples once every 4096 samples, producing 4096 complex bins (2048 unique after the mirror-image discard). Frame rate $F_{fs} = 48000/4096 \approx 11.7\text{ Hz}$, i.e. one frame every ~85 ms.
2. **Magnitude Squared (412).** $|X(k)|^2$ for each of the 2048 unique bins.
3. **Mean-Square (506).** Average of the magnitude-squared bins — a per-frame energy reference used by the relative threshold.
4. **Ballistics (414).** See [[concepts/ballistics-based-howling-detection|Ballistics-Based Howling Detection]] — the core novelty. Each bin's magnitude-squared value is passed through an asymmetric per-bin digital filter:
   - *Attack* (NEW_VALUE > OLD_VALUE): $\text{OLD\_VALUE} \leftarrow (\text{NEW\_VALUE} - \text{OLD\_VALUE}) \cdot K + \text{OLD\_VALUE}$, with $K = 1 - (1 - \text{Threshold})^{1/(t \cdot F_{fs})}$. The stored value builds up gradually over multiple frames.
   - *Release* (NEW_VALUE ≤ OLD_VALUE): $\text{OLD\_VALUE} \leftarrow \text{NEW\_VALUE}$, instantaneously (zero release time).
   - Frequency-dependent time constant $t$: 2 s at low frequencies (to tolerate sustained bass notes), 200 ms at high frequencies (where feedback builds faster and is more alarming/damaging). The time constant is defined as the time to reach 6 dB below the threshold value (0.5 of target).
   - Effect: persistent tones (feedback) accumulate to a high "OLD_VALUE" over several frames; transient music causes the value to release instantly, so it never builds up.

![[raw/papers/williams-2014-acoustic-feedback-elimination/figures/8468ad0578c0602c7ef5eb6912abf28cceb04bceb9f4e838b33df75db8868fa2.jpg|FIG. 6 — Ballistics process flow]]
*Figure 6: Ballistics subroutine — attack branch applies the first-order filter with coefficient K; release branch replaces the stored value directly.*

![[raw/papers/williams-2014-acoustic-feedback-elimination/figures/cec2220a1a50085bb6454c120d94a83ff668d680452a73f35da5d69619bfd31c.jpg|FIG. 7a — Ballistics response with a music signal]]
*Figure 7a: Ballistics response for a music signal — the rapidly varying magnitudes cause the stored value to release (decrease) instantly, so no prominence builds up.*

![[raw/papers/williams-2014-acoustic-feedback-elimination/figures/936467ff026593d474c66e1f406b5da84ed5c6f918b3048d3fa6615ca06f1e8c.jpg|FIG. 7b — Ballistics response with a feedback signal]]
*Figure 7b: Ballistics response for a feedback signal — the lingering tone builds up over multiple frames until the stored value reaches the threshold, forming a "prominence."*

5. **Prominence Search (416).** Pick the $N$ highest "OLD_VALUEs" — $N=6$ in the preferred embodiment (matching the 6 notch filters).
6. **Threshold Detection (418).** Each prominence must clear *both* thresholds to become a candidate:

![[raw/papers/williams-2014-acoustic-feedback-elimination/figures/551853046132fcf80465d94c3a1783e4659bf01563a81d44c4a547668a620a58.jpg|FIG. 8 — Threshold discrimination process]]
*Figure 8: Threshold discrimination — a candidate must exceed both the ABSOLUTE_THRESHOLD (loudness floor) and the RELATIVE_THRESHOLD (prominence above the mean-square level).*

![[raw/papers/williams-2014-acoustic-feedback-elimination/figures/e72209f6a7cf2b1a19d97fcd1e2ec5abb3a819c922fe887bb8c195283c703415.jpg|FIG. 9 — Frequency spectrum with absolute and relative thresholds]]
*Figure 9: Prominence 908 clears both thresholds (absolute 902, relative 904) and is admitted as a candidate; prominence 910 fails the absolute threshold and is rejected. The mean-square level 906 sets the relative threshold 904.*

- **ABSOLUTE_THRESHOLD**: +85 dB SPL at 1 m from the loudspeaker — inaudible feedback is not worth filtering.
- **RELATIVE_THRESHOLD**: $\text{MEAN\_SQUARE} \cdot (L/150)^2$ with $L = 4096$ — the prominence must stick out above the broadband average, which favours pure tones and avoids attenuating feedback already masked by wideband signal.

### Implementation Process (408) — Trial-and-Verify Notch Insertion

![[raw/papers/williams-2014-acoustic-feedback-elimination/figures/2a5dadd27b56115a5b591c7403af0197338201a51ed0e5946b495bf9ebe6d444.jpg|FIG. 10 — Assignment process]]
*Figure 10: Assignment process — for each candidate frequency, scan the N state machines; reuse the same one if the frequency is already in use (within a 2-bin deadband), otherwise assign the first free state machine.*

![[raw/papers/williams-2014-acoustic-feedback-elimination/figures/ff43c829b70913a0a0691f275a0648b24afbdbfa1dddd33ba82e44263815854a.jpg|FIG. 11 — State machine process]]
*Figure 11: State machine — Idle → Testing (set trial notch, start 500 ms timer) → check magnitude reduction vs TESTDROP (3 dB): if not met, bypass and return to Idle; if met, transition to Filtering. In Filtering, a same-frequency candidate deepens the notch by 6 dB; a different-frequency candidate is handed off to another state machine.*

See [[concepts/trial-and-verify-notch-insertion|Trial-and-Verify Notch Insertion]] for the dedicated concept page. The mechanism:

- **Assignment (420).** $N=6$ state machines, one per notch filter. For each candidate: if already in use (same frequency or within a 2-bin deadband) → reuse the same state machine; otherwise assign the first free one. The 2-bin deadband prevents clustered false positives around a true candidate.
- **State machine (422).** Three states per filter: **Idle**, **Testing**, **Filtering**.
  - *Idle → Testing*: set the notch to the candidate frequency, trial depth **6 dB**, bandwidth $= \max(\text{MIN\_BANDWIDTH}=0.05,\ \text{WINDOW\_SMEAR} \cdot \text{SAMPLE\_RATE}/\text{FFT\_LEN}/\text{Frequency})$ with WINDOW_SMEAR = 2.1 for a Hann window, SAMPLE_RATE = 48000, FFT_LEN = 4096. Start a 500 ms timer.
  - *Testing*: on timer expiry, retrieve the current bin magnitude. If the reduction is less than **TESTDROP = 3 dB**, the candidate is not feedback → set notch depth to 0 dB (bypass), return to Idle. If the reduction is ≥ 3 dB → feedback confirmed, transition to Filtering.
  - *Filtering*: if the next candidate is at the same frequency (or within deadband), increase the notch depth by a further 6 dB; otherwise exit so another state machine can handle the new candidate.
- **Verification principle.** A wanted pure tone (e.g. a sustained musical note) will *also* be reduced by the trial notch, but unlike feedback it is *not* sustained by the closed loop — the reduction is therefore a one-off step rather than a continuing decrease. The patent uses the post-notch magnitude reduction as the feedback signature: only feedback is actively driven by the loop and so produces a sustained reduction correlated with the notch depth change.

### Parameter Summary

| Parameter | Value | Meaning |
|-----------|-------|---------|
| Sample rate | 48 kHz | Audio path rate |
| FFT length $L$ | 4096 | Frame size |
| Frame rate $F_{fs}$ | 11.7 Hz | One FFT every 4096 samples (~85 ms) |
| Number of notch filters $N$ | 6 | One state machine per filter |
| Prominences selected | 6 (top-N) | Per frame |
| Ballistics attack time $t$ | 200 ms (high freq) – 2 s (low freq) | Frequency-dependent; time to 6 dB below threshold |
| Ballistics release | 0 (instantaneous) | Tracks transients instantly |
| ABSOLUTE_THRESHOLD | +85 dB SPL @ 1 m | Loudness floor for candidature |
| RELATIVE_THRESHOLD | $\text{MEAN\_SQUARE} \cdot (L/150)^2$ | Prominence over broadband average |
| Trial notch depth | 6 dB | Initial test attenuation |
| TESTDROP | 3 dB | Minimum reduction to confirm feedback |
| Test duration | 500 ms | Timer for the Testing state |
| Notch deepening step | 6 dB | Per same-frequency hit while Filtering |
| Deadband | 2 bins | Around each candidate frequency |
| MIN_BANDWIDTH | 0.05 octaves | Floor on notch bandwidth |
| WINDOW_SMEAR | 2.1 (Hann) | FFT window smearing compensation |

## Experimental Setup

No formal experiments are reported — this is a patent disclosure, not a research paper. The "Results" are the design itself: the parameter table above is the preferred embodiment, and the figures illustrate the expected behavior (FIG. 7a vs 7b for the ballistics discrimination, FIG. 9 for the threshold geometry).

## Results

The patent argues qualitative correctness rather than reporting metrics:

- The ballistics front end "is very effective at picking lingering tones out of a noisy (music) background" — frequencies that are not continuous (and thus probably music) never accumulate enough to become candidates.
- The attack rate is amplitude-dependent: a high-level feedback tone is acted on more urgently than a low-level one, because the per-frame increment $(\text{NEW}-\text{OLD}) \cdot K$ is larger.
- The trial-and-verify step prevents wanted sustained tones (e.g. sustained musical notes that *do* persist long enough to clear the ballistics stage) from being permanently notched, because their post-notch magnitude behavior differs from feedback.
- The system "dynamically guards against feedback in applications where the conditions are continuously changing, such as where a microphone is mobile."

No ΔMSG, SD, HOP, or TRI figures are reported — the patent predates the standardized NHS evaluation framework used in [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]].

## Key Contributions

1. **Asymmetric per-bin ballistics** for feedback-vs-music discrimination — a bank of digital filters (one per FFT bin) with gradual attack and zero release, turning persistent tones into "prominences" while letting transient music fall through. This is the patent's central novelty and a concrete instance of the "ballistics" candidate-selection step mentioned (but not elaborated) in the van Waterschoot & Moonen NHS survey.
2. **Frequency-dependent attack time constants** (200 ms high / 2 s low) — adapts the persistence criterion to the different physics of low- vs high-frequency feedback while explicitly discriminating sustained bass notes.
3. **Trial-and-verify notch insertion** — rather than committing a notch on detection, insert a shallow 6 dB trial notch, wait 500 ms, and confirm feedback by measuring ≥ 3 dB reduction. This separates feedback (driven by the loop, so the reduction holds) from wanted sustained tones (not loop-driven, so the reduction is a one-off step). Verified feedback is deepened in 6 dB steps; unverified candidates return to bypass.
4. **Two-threshold candidate admission** (absolute SPL + relative-to-mean) — prevents filtering inaudible feedback and feedback already masked by broadband signal, and biases selection toward pure tones.
5. **Two-rate DSP architecture** — audio-rate filtering decoupled from frame-rate analysis, with a circular buffer bridging the rates.
6. **Per-filter state machine with deadband** — six independent Idle/Testing/Filtering state machines with a 2-bin deadband prevent clustered false positives and allow concurrent verification of multiple candidates.

## Related Concepts

- [[concepts/acoustic-feedback|Acoustic Feedback]] — the closed-loop instability this patent suppresses
- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — the broader problem category
- [[concepts/notch-filter-based-howling-suppression|Notch-Filter-Based Howling Suppression (NHS)]] — the gain-reduction sub-category this patent instantiates
- [[concepts/howling-detection|Howling Detection]] — the front-end problem; this patent's ballistics stage is a candidate-based HD method
- [[concepts/ballistics-based-howling-detection|Ballistics-Based Howling Detection]] — the patent's core HD novelty (introduced by this source)
- [[concepts/trial-and-verify-notch-insertion|Trial-and-Verify Notch Insertion]] — the patent's verification paradigm (introduced by this source)
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — NHS effectively raises the operable gain above the passive MSG

## Related Synthesis

- (No dedicated synthesis page on PA-system acoustic-feedback control exists yet; the cross-source comparison of NHS/PFC/AFC lives inside [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] and the [[concepts/notch-filter-based-howling-suppression|NHS]] concept page. This patent is a single concrete instance of NHS and does not by itself change the cross-source comparison.)
