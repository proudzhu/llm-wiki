---
type: concept
created: 2026-08-19
updated: 2026-08-19
sources:
  - raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/full-text.md
tags:
  - speech-processing
  - voice-activity-detection
  - diarization
  - target-speaker-extraction
  - deep-learning
---

# Target-Speaker Voice Activity Detection (TS-VAD)

**Target-Speaker Voice Activity Detection (TS-VAD)** is the task of predicting when a specific target speaker is actively speaking in a multi-speaker recording, given a clue (typically an enrollment utterance or pre-extracted [[concepts/speaker-embedding|speaker embedding]]) that identifies that speaker. It is the activity-detection analog of [[concepts/target-speaker-extraction|target speech extraction (TSE)]]: rather than estimating the target's speech signal, TS-VAD estimates a binary activity mask indicating "target speaking" vs. "target silent" for each time frame.

## Relation to Standard VAD

Standard [[concepts/voice-activity-detection|voice activity detection (VAD)]] predicts whether *any* speech is present. TS-VAD is **speaker-conditioned**: it predicts whether *the target speaker* is present. This requires the model to internally solve the same identification sub-task as TSE but with a simpler (binary) output, which permits lighter-weight network architectures and faster inference.

## Architecture

A TS-VAD system reuses the general TSE framework (clue encoder + mixture encoder + fusion layer) but replaces the mask estimator with a binary classifier:

$$
a_{s}[n] = \mathrm{TS\text{-}VAD}(\mathbf{y}, \mathbf{C}_{s}; \theta^{\mathrm{TS\text{-}VAD}}), \quad a_{s}[n] \in [0, 1],
$$

where $a_{s}[n]$ is the activity probability of the target speaker at frame $n$, $\mathbf{y}$ the mixture, and $\mathbf{C}_{s}$ the enrollment clue (audio embedding or visual features). Personalized VAD [27] is a representative single-target instantiation; audio-visual VAD [56] uses video clues analogously.

## Multi-Target Extension for Diarization

Extending TS-VAD to simultaneously output the activity of multiple target speakers ($a_{s_{1}}, \dots, a_{s_{K}}$) yields a powerful diarization system [28]:

- Each speaker is associated with a pre-extracted embedding.
- A shared network predicts per-speaker activity masks.
- Overlapping speech is naturally handled because the masks are independent rather than exclusive.

The resulting TS-VAD diarization system achieved the top diarization performance in the CHiME-6 evaluation campaign, outperforming conventional clustering-based approaches in challenging dinner-party scenarios with frequent overlaps.

## Why TS-VAD Is Easier Than TSE

Estimating a binary activity mask is strictly simpler than estimating the target speech waveform: the model needs only to identify *when* the target speaks, not *what* they say. This has two practical consequences:

1. **Lighter architectures** suffice — useful for hearing aids, hearables, and edge deployment.
2. **Higher robustness** to identification errors — small confusions produce frame-level mistakes rather than full waveform corruption.

## Limitations and Open Issues

- **Inactive target speaker**: TS-VAD must reliably output "silent" when the target is absent from the mixture, which most TSE systems are not explicitly trained to do [57].
- **Multi-target scaling**: the standard TS-VAD diarization scheme requires pre-enrolling every speaker of interest, which limits its use to scenarios with a known speaker inventory (e.g., a meeting).
- **Clue corruption**: like all enrollment-conditioned systems, performance degrades when the enrollment embedding is noisy or out-of-domain.

## Related Concepts

- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/voice-activity-detection|Voice Activity Detection (VAD)]]
- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/target-speaker-asr|Target-Speaker ASR (TS-ASR)]]

## Related Sources

- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova et al. 2023: Neural Target Speech Extraction: An Overview]]
