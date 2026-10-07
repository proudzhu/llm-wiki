---
type: concept
created: 2026-06-19
updated: 2026-10-07
sources:
  - raw/papers/ostergaard-2026-own-voice-cancellation/full-text.md
  - raw/papers/ohlenbusch-2026-pas-se/full-text.md
tags:
  - speech-enhancement
  - speaker-adaptation
---

# Personalized Speech Enhancement (PSE)

Personalized speech enhancement (PSE) uses speaker representations to guide the enhancement process, preserving the target speaker's characteristics while suppressing interference and noise. Methods typically condition the enhancement model on speaker embeddings extracted from enrollment audio (clean or noisy). G-MaP-SE addresses the key limitation of noisy-conditioning PSE by refining noisy embeddings via GMM prior matching.

## Related Tasks

[[concepts/own-voice-cancellation|Own-Voice Cancellation (OVC)]] is a related enrollment-conditioned task that inverts the PSE objective: instead of preserving the enrolled speaker, OVC removes the enrolled speaker from the mixture while preserving all other speech. Both PSE and OVC share the same conditioning machinery (e.g., [[concepts/td-speakerbeam|TD-SpeakerBeam]], [[concepts/mamba-mingru|Mamba-MinGRU]]).

## PSE vs. Auxiliary-Sensor Speech Enhancement

Ohlenbusch et al. 2026 [[sources/ohlenbusch-2026-pas-se|(Ohlenbusch 2026)]] provide the first systematic comparison of PSE with [[concepts/as-se|auxiliary-sensor speech enhancement (AS-SE)]] — two complementary answers to the target/interferer ambiguity in hearable voice pickup: PSE requires an enrollment procedure but is device-agnostic, while AS-SE is user-agnostic but array-dependent. Key findings:

- An FT-JNF-based PSE (1.4M params + 1.8M speaker encoder) slightly outperforms the 4.985M-parameter [[concepts/td-speakerbeam|TD-SpeakerBeam]] baseline in-domain, and — unlike SpeakerBeam — generalizes across datasets (magnitude-STFT features vs. time-domain learnable filterbanks).
- Combining both ([[concepts/pas-se|PAS-SE]]) systematically improves interferer suppression; with **in-ear enrollment**, the combined system outperforms even in-domain-trained AS-SE baselines across datasets.
- In-ear-microphone enrollments retain personalization benefits down to −10 dB enrollment SNR, whereas outer-microphone enrollments provide no benefit below 0 dB.

## Related Concepts

- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/prior-matching|Prior Matching]]
- [[concepts/own-voice-cancellation|Own-Voice Cancellation (OVC)]]
- [[concepts/td-speakerbeam|TD-SpeakerBeam]]
- [[concepts/mamba-mingru|Mamba-MinGRU]]
- [[concepts/as-se|Auxiliary-Sensor Speech Enhancement (AS-SE)]]
- [[concepts/pas-se|PAS-SE]]

## Related Sources

- [[sources/ostergaard-2026-own-voice-cancellation|Østergaard et al. 2026: Don't Listen to Me — Own-Voice Cancellation]]
- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]
- [[sources/ohlenbusch-2026-pas-se|Ohlenbusch, Kegler & Stamenovic 2026: PAS-SE]] — first systematic PSE vs. AS-SE benchmark; PAS-SE combination