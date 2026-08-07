---
type: concept
created: 2026-08-07
updated: 2026-08-07
sources:
  - raw/papers/williams-2014-acoustic-feedback-elimination/full-text.md
tags:
  - acoustic-howling
  - notch-filter
  - howling-detection
  - signal-processing
  - feedback-verification
---

# Trial-and-Verify Notch Insertion

**Trial-and-verify notch insertion** is a feedback-verification paradigm used in [[concepts/notch-filter-based-howling-suppression|notch-filter-based howling suppression (NHS)]] in which a candidate frequency is suppressed with a shallow *trial* notch, the post-notch amplitude is measured after a fixed test window, and the notch is *kept and deepened* only if the measured reduction confirms feedback. It is the verification half of the [[sources/williams-2014-acoustic-feedback-elimination|Williams 2014]] patent (US 8,634,575 B2), paired with [[concepts/ballistics-based-howling-detection|ballistics-based howling detection]] as the candidate-generation front end. The paradigm addresses the fundamental NHS weakness that any pure persistent tone — including wanted sustained musical notes — can masquerade as feedback to a detector that looks only at the open-loop microphone signal.

## Motivation: The Sustained-Tone Ambiguity

A howling detector that examines only the microphone signal $y(t)$ sees a narrow, persistent, high-magnitude spectral peak for both:

- **Feedback** — driven by the closed loop, the tone is self-sustaining and will grow until the loop is broken.
- **Wanted sustained tones** — a held violin note, an organ stop, a test tone, or a sung vowel. These are persistent and pure, exactly the signature that ballistics and most [[concepts/howling-detection-features|HD features]] flag as feedback.

The detector cannot tell the two apart from the open-loop signal alone, because it does not see the loop. The trial-and-verify paradigm breaks the ambiguity by *perturbing the loop*: insert a notch and observe the response. Feedback is actively sustained by the loop, so the notch produces a *continuing* reduction that tracks the notch depth; a wanted tone is not loop-driven, so the notch produces a *one-off* step that does not deepen further.

## The State Machine

Each notch filter is governed by a three-state machine:

```
       set trial notch (6 dB, candidate freq), start 500 ms timer
  Idle ───────────────────────────────────────────────────────► Testing
   ▲                                                               │
   │                                                               │ on timer expiry:
   │                                                               │  measure |X(candidate)| reduction
   │                                                               │
   │                                                               ▼
   │                                                       ┌───────┴───────┐
   │                                                       │               │
   │                                              reduction < 3 dB   reduction ≥ 3 dB
   │                                                       │               │
   │                                              bypass notch       Filtering
   │                                              (depth = 0 dB)         │
   │                                                       │               │ next candidate
   │                                                       │               │ within deadband:
   │                                                       │               │  deepen by 6 dB
   └───────────────────────────────────────────────────────┘               │
                                                                            │ next candidate
                                                                            │ different freq:
                                                                            │  exit (hand off)
```

### State: Idle

The notch filter is bypassed (depth = 0 dB). The state machine is ready to accept a new candidate frequency from the assignment process.

### State: Testing

A trial notch is inserted at the candidate frequency:

- **Trial depth**: 6 dB
- **Bandwidth**: $\max\!\big(\text{MIN\_BANDWIDTH},\ \text{WINDOW\_SMEAR} \cdot \text{SAMPLE\_RATE} / \text{FFT\_LEN} / \text{Frequency}\big)$
  - $\text{MIN\_BANDWIDTH} = 0.05$ octaves
  - $\text{WINDOW\_SMEAR} = 2.1$ (compensates the Hann-window smearing of the FFT analysis)
  - $\text{SAMPLE\_RATE} = 48000$, $\text{FFT\_LEN} = 4096$
- **Test window**: 500 ms timer

On timer expiry, retrieve the current magnitude of the candidate bin and compare the reduction to **TESTDROP = 3 dB**:

- **Reduction < 3 dB** → the candidate is *not* feedback (the loop is not sustaining it through the notch) → set notch depth to 0 dB, return to **Idle**. The filter is immediately available for reassignment to a new candidate in the same frame.
- **Reduction ≥ 3 dB** → feedback confirmed → transition to **Filtering**.

### State: Filtering

The notch remains engaged at the verified frequency. On subsequent candidate lists:

- **Same frequency** (within a 2-bin deadband) → deepen the notch by a further **6 dB**. Iterative deepening lets the system converge on the depth actually required to suppress the feedback, rather than committing a fixed deep notch up front.
- **Different frequency** → exit so another state machine can handle the new candidate; this filter continues at its current depth.

The 2-bin deadband prevents clustered false positives around a true candidate from each claiming a separate filter.

## Assignment Process

With $N=6$ notch filters and 6 state machines, the assignment process assigns each candidate to a state machine:

1. For each candidate, scan all state machines.
2. If the candidate frequency is already in use by some state machine (within the deadband) → assign to that same machine (so it deepens the existing notch).
3. Otherwise → assign to the first free (Idle) state machine.

This ensures a feedback frequency that survives the trial is deepened on subsequent frames rather than re-tested from scratch.

## Verification Principle

The trial-and-verify step is a *closed-loop probe*. The key insight is:

- A **feedback** tone is an instability of the closed loop. The notch reduces the loop gain at the feedback frequency, which reduces the feedback component at the microphone, which reduces the input to the notch, and so on — the system settles at a lower equilibrium. The reduction is sustained and matches (or exceeds) the trial depth.
- A **wanted sustained tone** is an exogenous input. The notch attenuates it by exactly the trial depth, but the source is unaffected — the tone keeps arriving at the microphone at its original level. The reduction is a single step equal to the trial depth, not a continuing decrease.

The TESTDROP threshold (3 dB) is set below the trial depth (6 dB) to allow for measurement noise and partial overlap between the notch and the tone, while still requiring a clear reduction. A wanted tone that happens to be reduced by exactly the trial depth would be on the boundary; in practice, feedback reductions tend to exceed the trial depth because of the loop interaction, while wanted-tone reductions saturate at the trial depth.

## Comparison with Open-Loop HD Features

| Aspect | Trial-and-Verify | Open-loop HD features (e.g. [[concepts/howling-detection-features|HD features]]) |
|--------|------------------|--------------------------------------------------------------|
| Signal observed | Closed-loop response to a probe | Open-loop microphone signal only |
| Sustained-tone ambiguity | Resolved by perturbing the loop | Persists — sustained wanted tones mimic feedback |
| Detection latency | ≥ test window (500 ms) per candidate | One frame (~85 ms) |
| Audio intrusion | Trial notch briefly attenuates wanted tones during test | No intrusion (detection only) |
| Computational cost | N notch filters + N state machines | Feature computation per candidate |
| Per-candidate cost | 500 ms of notch + magnitude check | One-shot feature evaluation |

The trade-off is latency and transient audio intrusion versus robustness against the sustained-tone ambiguity. Williams' patent accepts the latency because the ballistics front end already requires the tone to persist for ~200 ms–2 s before candidature, so the additional 500 ms is a marginal increment.

## Position in the NHS Pipeline

The trial-and-verify state machine is the *implementation* half of the Williams NHS system, downstream of [[concepts/ballistics-based-howling-detection|ballistics-based howling detection]]:

1. [[concepts/ballistics-based-howling-detection|Ballistics]] → candidate frequencies (top-6 prominences above absolute + relative thresholds)
2. **Assignment** to one of 6 state machines
3. **Trial-and-verify state machine** (this concept) → confirmed feedback frequencies with deepening notches
4. Time-domain notch filter bank at audio rate

## Limitations

- **Latency**: 500 ms per candidate test adds to the ballistics accumulation time. By the time a feedback tone is verified, it has been audible for at least the ballistics attack time plus 500 ms.
- **Trial-notch intrusion**: the 6 dB trial notch briefly attenuates a wanted tone that happens to be a candidate, before being released on test failure. The patent argues this is acceptable because the test is short and the trial depth is shallow.
- **No early-howling detection**: like all candidate-based NHS, the system reacts only after howling has built up. It cannot suppress the early/ringing regime targeted by [[concepts/ninosp2-transposed|NINOS²-T]].
- **Single-frequency probe**: the state machine tests one frequency at a time. Multiple simultaneous feedback tones require multiple state machines, and the patent caps this at 6.

## Related Concepts

- [[concepts/notch-filter-based-howling-suppression|Notch-Filter-Based Howling Suppression (NHS)]] — the solution scheme this paradigm belongs to
- [[concepts/ballistics-based-howling-detection|Ballistics-Based Howling Detection]] — the upstream candidate-generation front end in the same patent
- [[concepts/howling-detection|Howling Detection]] — the open-loop detection problem this paradigm sidesteps by probing the loop
- [[concepts/howling-detection-features|Howling Detection Features]] — the open-loop feature-based alternative
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the closed-loop instability being verified
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — the notch effectively raises the operable MSG by reducing loop gain at the critical frequency

## Related Sources

- [[sources/williams-2014-acoustic-feedback-elimination|Williams 2014]] — introduces the trial-and-verify state machine (US 8,634,575 B2)
- [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] — surveys NHS as a category; Williams' trial-and-verify is a concrete instance of the notch-insertion step with a closed-loop verification twist
