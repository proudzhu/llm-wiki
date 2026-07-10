---
type: concept
created: 2026-06-19
updated: 2026-07-10
sources:
  - raw/papers/ostergaard-2026-own-voice-cancellation/full-text.md
tags:
  - speech-enhancement
  - speaker-adaptation
---

# Personalized Speech Enhancement (PSE)

Personalized speech enhancement (PSE) uses speaker representations to guide the enhancement process, preserving the target speaker's characteristics while suppressing interference and noise. Methods typically condition the enhancement model on speaker embeddings extracted from enrollment audio (clean or noisy). G-MaP-SE addresses the key limitation of noisy-conditioning PSE by refining noisy embeddings via GMM prior matching.

## Related Tasks

[[concepts/own-voice-cancellation|Own-Voice Cancellation (OVC)]] is a related enrollment-conditioned task that inverts the PSE objective: instead of preserving the enrolled speaker, OVC removes the enrolled speaker from the mixture while preserving all other speech. Both PSE and OVC share the same conditioning machinery (e.g., [[concepts/td-speakerbeam|TD-SpeakerBeam]], [[concepts/mamba-mingru|Mamba-MinGRU]]).

## Related Concepts

- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/prior-matching|Prior Matching]]
- [[concepts/own-voice-cancellation|Own-Voice Cancellation (OVC)]]
- [[concepts/td-speakerbeam|TD-SpeakerBeam]]
- [[concepts/mamba-mingru|Mamba-MinGRU]]

## Related Sources

- [[sources/ostergaard-2026-own-voice-cancellation|Østergaard et al. 2026: Don't Listen to Me — Own-Voice Cancellation]]
- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]