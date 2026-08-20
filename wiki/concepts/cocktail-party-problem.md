---
type: concept
created: 2026-08-19
updated: 2026-08-20
sources:
  - raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/full-text.md
  - raw/papers/ansari-2023-ai-bss-survey/full-text.md
tags:
  - speech-processing
  - psychoacoustics
  - source-separation
  - target-speaker-extraction
---

# Cocktail-Party Problem

The **cocktail-party problem** is the task of selectively attending to and following a target speaker's voice in a noisy acoustic environment with multiple interfering speakers, named after the prototypical scenario of holding a conversation at a cocktail party. The term, popularized by Cherry (1953), describes the human ability — known as selective hearing or selective attention — to focus on a target voice while ignoring competing speech, noise, and reverberation.

## Psychoacoustic Basis

Humans use several cues to perform selective hearing, including [1]:

- **Spatial cues** — interaural time/level differences, head shadow, direction of arrival
- **Spectral (audio) cues** — voice characteristics such as pitch, formant structure, and timbre
- **Visual cues** — lip movements, facial expressions, head orientation
- **Semantic cues** — content (one's own name, a topic of interest), language

The mechanisms underlying human selective hearing are not fully understood; psychoacoustic studies suggest both bottom-up (peripheral auditory processing) and top-down (cognitive attention) processes contribute [1].

## Engineering Formulation

From a signal-processing standpoint, the cocktail-party problem motivates three classes of approaches:

1. **[[concepts/blind-source-separation|Blind source separation (BSS)]]** — estimates all sources in a mixture without auxiliary clues; suffers from global permutation ambiguity and requires the source count.
2. **Noise reduction** — assumes only background noise interferes; cannot suppress competing speakers without clues.
3. **[[concepts/target-speaker-extraction|Target speech extraction (TSE)]]** — uses an auxiliary clue (audio enrollment, visual lip movements, spatial direction) to identify and extract only the target speaker, side-stepping permutation ambiguity.

The TSE formulation is the engineering response that most directly mirrors the human cocktail-party ability: it exploits clues to identify the target and applies them to the extraction itself, rather than post-hoc source selection.

## Relation to Selective Hearing

Although TSE is engineering-motivated, it is closely connected to the cognitive cocktail-party mechanism. Both humans and TSE systems use auxiliary cues to disambiguate the target; the difference is that engineering systems are not constrained to mimic biological auditory processing. Recent extensions of TSE explore semantic and brain-signal clues (e.g., EEG-guided TSE [61]) that move closer to high-level human attention.

## Related Concepts

- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova et al. 2023: Neural Target Speech Extraction: An Overview]]
- [[sources/ansari-2023-ai-bss-survey|Ansari et al. 2023: AI Approaches in BSS Survey]] — lists the cocktail-party problem as one of the canonical BSS motivations.
