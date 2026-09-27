---
type: concept
created: 2026-09-27
updated: 2026-09-27
sources:
  - raw/papers/veluri-2023-semantic-hearing/full-text.md
tags:
  - target-sound-extraction
  - neural-network
  - audio-signal-processing
---

# Target Sound Extraction

**Target sound extraction** (TSE) is the task of separating one or a limited number of *target* sounds from an acoustic mixture, using clues that identify the target. It generalizes target *speech* extraction to arbitrary sound classes (sirens, bird chirps, music, door knocks, ...), in contrast to speech-centric systems that treat every non-speech sound as noise.

## Clue Types

Prior neural TSE systems condition extraction on:

- **Audio** clues (e.g., enrollment recordings — SoundBeam)
- **Images** (visual co-separation)
- **Text** descriptions (language-queried separation)
- **Onomatopoeic words**
- **One-hot class vectors** (universal sound selector; the query form used by Waveformer and semantic hearing)

## Real-Time Constraint

Most prior TSE models are designed for offline processing of clips ≥1 s (full-file access). Real-time hearable applications instead require causal, streaming models that operate on ~10 ms blocks with a past-only receptive field — the setting addressed by [[concepts/waveformer|Waveformer]] (single-channel) and [[concepts/binaural-target-sound-extraction|binaural target sound extraction]] (Veluri et al. 2023).

## Relation to Neighboring Tasks

- [[concepts/cocktail-party-problem|Cocktail-party problem]]: TSE is the machine-learning response to human selective listening; class-based TSE extends it beyond speech.
- [[concepts/blind-source-separation|Blind source separation]] separates all sources without a target notion; TSE extracts only the cued target(s), which is cheaper and sufficient when the user picks one class.
- [[concepts/sound-event-detection|Sound event detection]] classifies *when* sounds occur; TSE additionally produces the isolated waveform.
- An inverse operation is also useful: extract a class and *subtract* it to attenuate a known annoyance (e.g., remove keyboard typing, keep everything else).

## Related Concepts

- [[concepts/binaural-target-sound-extraction|Binaural Target Sound Extraction]]
- [[concepts/waveformer|Waveformer]]
- [[concepts/semantic-hearing|Semantic Hearing]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/music-source-separation|Music Source Separation]]
- [[concepts/sound-event-detection|Sound Event Detection]]

## Related Sources

- [[sources/veluri-2023-semantic-hearing|Veluri et al. 2023: Semantic Hearing]]
