---
type: concept
created: 2026-09-27
updated: 2026-09-27
sources:
  - raw/papers/veluri-2023-semantic-hearing/full-text.md
tags:
  - target-sound-extraction
  - hearables
  - spatial-audio
  - audio-signal-processing
---

# Semantic Hearing

**Semantic hearing** is a capability for hearable devices introduced by Veluri et al. (UIST 2023): in real time, *focus on or ignore specific sound classes* from the real-world environment based on their semantic meaning, while preserving the spatial cues of the retained sounds. Example use cases: hear birds chirping in a park without nearby hikers' chatter, block street noise but keep emergency sirens, or sleep through traffic noise while still hearing an alarm clock or baby sounds.

![[raw/papers/veluri-2023-semantic-hearing/figures/93202928dfc2273e516999015504a253fe68a9c024714cf3ea37e494dd3e4884.jpg|Semantic hearing application scenarios]]
*Figure 1: Semantic hearing applications (Veluri et al. 2023).*

## Operating Principle

The system exploits modern [[concepts/active-noise-control|active noise cancellation]] as an "acoustic clean slate": the noise-canceling headset attenuates *all* external sounds, and the semantic hearing subsystem then reintroduces only the desired target sounds, extracted in real time by a neural network from the binaural microphones and played back through the headset speakers. This inverts the classical enhancement paradigm — instead of suppressing known noise, the system *selects* what to let back in based on user intent (a one-hot class query, or natural language mapped to classes via an LLM).

## Key Constraints

1. **Real-time**: end-to-end latency must stay below 20–50 ms so output stays synced with the user's visual senses; the extraction network must process ≤10 ms audio chunks in under 10 ms on a smartphone (see [[concepts/audio-latency|audio latency]]).
2. **Binaural**: the output must preserve [[concepts/interaural-time-difference|ITD]] and [[concepts/interaural-level-difference|ILD]] cues so kept sounds are perceived from their true directions.
3. **Generalization**: the network must work on unseen users, rooms, reverberation, and hardware — achieved by HRTF/BRIR-based training-data synthesis (see [[concepts/head-related-transfer-function|HRTF]]).

## Relation to Other Paradigms

- Unlike speech enhancement systems that treat all non-speech sounds as noise, semantic hearing assigns semantics to *all* sound classes; speech is just one of 20 classes.
- Unlike acoustic transparency or adaptive transparency (e.g., AirPods Pro loud-sound reduction), it lets the user pick which classes to hear, not merely reduce loudness.
- [[concepts/binaural-target-sound-extraction|Binaural target sound extraction]] is the core enabling technology.

## Open Issues

- Class imbalance and acoustically similar classes (music vs speech, hammer vs music) degrade extraction quality.
- Coexistence with adaptive ANC: playback may interact with the ANC algorithm; residual-noise-aware playback remains open.
- Wireless hearables require moving compute onto the headset (embedded GPUs or custom silicon) to meet latency.

## Related Concepts

- [[concepts/binaural-target-sound-extraction|Binaural Target Sound Extraction]]
- [[concepts/target-sound-extraction|Target Sound Extraction]]
- [[concepts/hearables|Hearables]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/cocktail-party-problem|Cocktail-Party Problem]]
- [[concepts/audio-latency|Audio Latency]]

## Related Sources

- [[sources/veluri-2023-semantic-hearing|Veluri et al. 2023: Semantic Hearing]]
