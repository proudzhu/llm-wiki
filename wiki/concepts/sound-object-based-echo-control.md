---
type: concept
created: 2026-09-02
updated: 2026-09-02
sources:
  - raw/papers/hoshuyama-2026-sound-object-echo-control/full-text.md
tags:
  - acoustic-howling
  - echo-cancellation
  - sound-object-identification
  - voice-switching
  - signal-processing
---

# Sound-Object-Based Echo Control

**Sound-object-based echo control** is an acoustic echo and howling suppression paradigm (Hoshuyama 2026) that replaces echo **path estimation** with **sound object identification**: it identifies whether sound objects (speech segments of tens to hundreds of milliseconds) reappear, and gates their pass/playback accordingly, rather than estimating the acoustic feedback path and subtracting echo.

## Basic Policy: Default Mute with Conditional Pass

Channels are **muted by default** and unmuted for pass/playback only when a signal is judged **not identical** to sound objects recently observed at the same terminal:

- **Transmit side**: a signal is sent to the server only when identification against stored receive-side objects indicates it is unlikely to stem from the same utterance.
- **Receive side**: playback is allowed only when the receive object is judged different from microphone-side objects.

Because only sound objects are used — no path information — echo loops can in principle be broken **even for unintended paths** that include network delay and nonlinear in-device processing (codecs, noise/echo suppressors, dynamic range control, user mute fragmentation, clock mismatch). The policy is an extension of classical [[concepts/voice-switched-half-duplex|voice-switched half-duplex]] toward *conditional* half-duplex: not permanent half-duplex, but gating that closes locally when object identity is detected.

## Processing Blocks

1. **Extraction and buffering of sound objects** — extract objects from the microphone or receive signal; retain for a duration on the order of the network delay and room reverberation.
2. **Sound object identification** — compute a similarity or identity probability between the current transmit/receive object and the buffered set; [[concepts/audio-fingerprinting|audio fingerprinting]] and MFCC features are candidates.
3. **Playback control** — mute when identity is likely; pass otherwise; **safe-side mute** when comparison candidates are insufficient.

## Error Behavior and Trade-off

A **non-persistent** identification error causes only a brief echo rather than sustained howling, since the loop is broken on the next correct decision. Two error types define the fundamental trade-off:

- **False passes** (same object judged different) — seed momentary echo;
- **Over-muting** (different objects judged the same) — fragments desired speech and reduces intelligibility.

## Verification Simulation (Hoshuyama 2026)

A two-room, three-terminal setup (hands-free A1 + microphone-only A2 in Room A, hands-free B1 in Room B; $T_{60}=500$ ms, 200 ms inter-room delay) with a full call chain (partitioned AEC → nonlinear residual echo suppression → spectral subtraction → codec distortion). The initial gate implementation uses cosine similarity of magnitude-spectrum sequences with ±32 ms lag search; receive side passes only at similarity ≤ 0.66, transmit side mutes at similarity ≥ 0.68, with per-hop exponential gain smoothing.

Results: howling arises ~2–3 s after call start without control; with control, sustained howling is suppressed even under double- and triple-talk, but over-muting thins the spectrograms — mute-only control is insufficient under double-talk.

## Related Concepts

- [[concepts/voice-switched-half-duplex|Voice-Switched Half-Duplex]] — the classical technique extended into conditional half-duplex
- [[concepts/audio-fingerprinting|Audio Fingerprinting]] — candidate identification feature
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]] — the path-estimation paradigm this replaces for complicated paths
- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — the broader problem domain
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the closed-loop instability the default-mute policy breaks
- [[concepts/residual-echo-suppression|Residual Echo Suppression]] — coexists in the call chain of the verification simulation

## Related Sources

- [[sources/hoshuyama-2026-sound-object-echo-control|Hoshuyama 2026: Sound-Object-Based Echo Control]] — introduces the paradigm
