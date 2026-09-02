---
type: concept
created: 2026-09-02
updated: 2026-09-02
sources:
  - raw/papers/hoshuyama-2026-sound-object-echo-control/full-text.md
tags:
  - audio-fingerprinting
  - content-based-audio-retrieval
  - sound-object-identification
  - signal-processing
---

# Audio Fingerprinting

**Audio fingerprinting** extracts a compact, content-based signature (fingerprint) from an audio signal such that the *same recording* can be identified in a database or reference stream even after deformation — coding artifacts, noise, time shifting, or level changes (Cano et al. 2005 review). The canonical systems are Foote's content-based retrieval via spectrum-sequence similarity (1997), the Haitsma–Kalker robust fingerprint (2002), and Shazam's landmark/comb-hash matching (Wang 2003).

## Key Formulation (Haitsma–Kalker Style)

Fingerprints are derived from short-frame magnitude spectra, e.g., as sign bits of energy differences between adjacent frequency bands and successive frames. Matching then reduces to comparing fingerprint sequences with tolerance to bit errors and time offsets — typically via (normalized) **cross-correlation or cosine similarity** of the spectral/fingerprint sequences over a lag range.

## Use in Sound-Object Identification

Hoshuyama 2026 identifies audio fingerprinting (together with MFCCs) as the candidate feature family for the identification stage of [[concepts/sound-object-based-echo-control|sound-object-based echo control]]: the receiver/gate must decide whether a current segment is the *same sound object* as one recently buffered. The paper's verification gate implements a minimal version — cosine similarity of magnitude-spectrum sequences with a ±32 ms lag search.

Deploying fingerprinting in a call pipeline imposes constraints unlike music-identification services:

- **Ultra-low latency** — extra delay beyond a few tens of milliseconds hurts interactivity, so long-buffer high-accuracy matching is unattractive; fingerprints "need redesign under ultra-low-latency and low-compute call constraints."
- **Severe deformation** — beyond coding noise: room reverberation, noise/echo suppressors, dynamic range control, fragmentation by user mute, sampling-rate/clock mismatch, and time warping from packet-loss/jitter compensation.
- **Identity ambiguity** — rephrasing, short backchannels, and repeated music phrases can fool similarity decisions in both directions (false passes and over-muting).

## Related Concepts

- [[concepts/sound-object-based-echo-control|Sound-Object-Based Echo Control]] — the application domain re-specifying fingerprint design constraints
- [[concepts/spectrogram-analysis|Spectrogram Analysis]] — the magnitude-spectrum representation underlying the fingerprints
- [[concepts/voice-activity-detection|Voice Activity Detection]] — endpointing that delimits candidate sound objects

## Related Sources

- [[sources/hoshuyama-2026-sound-object-echo-control|Hoshuyama 2026: Sound-Object-Based Echo Control]] — fingerprinting as candidate feature for low-latency sound-object identification
