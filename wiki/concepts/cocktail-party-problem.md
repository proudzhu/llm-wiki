---
type: concept
created: 2026-08-19
updated: 2026-10-24
sources:
  - raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/full-text.md
  - raw/papers/ansari-2023-ai-bss-survey/full-text.md
  - raw/papers/wen-2025-neural-directed-speech-enhancement/full-text.md
  - raw/papers/veluri-2023-semantic-hearing/full-text.md
  - raw/papers/zhang-2025-mbenet/full-text.md
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
4. **Sensor-based own-voice capture** — beyond acoustic clues, bone-conduction sensors physically isolate the wearer's voice from both noise and competing speakers: [[concepts/mbenet|MBENet]] (Zhang et al. 2025) treats the BC signal itself as the TSE clue for the first time.

The TSE formulation is the engineering response that most directly mirrors the human cocktail-party ability: it exploits clues to identify the target and applies them to the extraction itself, rather than post-hoc source selection.

## Relation to Selective Hearing

Although TSE is engineering-motivated, it is closely connected to the cognitive cocktail-party mechanism. Both humans and TSE systems use auxiliary cues to disambiguate the target; the difference is that engineering systems are not constrained to mimic biological auditory processing. Recent extensions of TSE explore semantic and brain-signal clues (e.g., EEG-guided TSE [61]) that move closer to high-level human attention.

The idea extends beyond speech: [[concepts/semantic-hearing|semantic hearing]] (Veluri et al. 2023) realizes class-based selective listening on hearables — the user names a sound *class* (birds, sirens, speech) rather than a specific speaker, and a binaural network extracts it while preserving spatial cues. This is the environmental-sound analog of the TSE formulation, with speech demoted to one class among twenty.

A further non-acoustic clue class is emerging: **bone-conduction sensors**. Because the BC sensor records only skull vibrations of the speaker wearing it, it naturally implements the selective-attention filter in hardware — immune to both ambient noise and interfering talkers. MBENet (Zhang et al. 2025) demonstrates this for TSE with BC-AC fusion; see [[concepts/bone-conduction|bone conduction]].

## Related Concepts

- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/bone-conduction|Bone Conduction]]
- [[concepts/mbenet|MBENet]]

## Related Sources

- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova et al. 2023: Neural Target Speech Extraction: An Overview]]
- [[sources/ansari-2023-ai-bss-survey|Ansari et al. 2023: AI Approaches in BSS Survey]] — lists the cocktail-party problem as one of the canonical BSS motivations.
- [[sources/wen-2025-neural-directed-speech-enhancement|Wen et al. 2025: Neural Directed Speech Enhancement with Dual Microphone Array in High Noise Scenario]] — targets the cocktail-party problem with a spatial-clue approach: a dual-microphone directional enhancer steered by the target angle plus a runtime enhancement width
- [[sources/veluri-2023-semantic-hearing|Veluri et al. 2023: Semantic Hearing]] — extends selective listening from a target *speaker* to arbitrary sound *classes* on binaural hearables, preserving spatial cues in real time.
- [[sources/zhang-2025-mbenet|Zhang, Feng, Liu, Zhang & Li 2025: MBENet]] — bone-conduction sensor as a hardware-selective clue for the cocktail-party problem
