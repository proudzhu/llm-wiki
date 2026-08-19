---
type: concept
created: 2026-08-19
updated: 2026-08-19
sources:
  - raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/full-text.md
tags:
  - speech-recognition
  - target-speaker-extraction
  - end-to-end
  - multi-modal
---

# Target-Speaker ASR (TS-ASR)

**Target-Speaker ASR (TS-ASR)** is the task of transcribing the speech of a target speaker in a multi-speaker mixture while ignoring interfering speakers, given a clue (audio enrollment, visual lip video, or anchor keyword) that identifies the target. It is the recognition-side counterpart of [[concepts/target-speaker-extraction|target speech extraction (TSE)]], and motivates many TSE deployments where ASR — rather than listening — is the downstream application.

## Architectures

Three architectural patterns have been explored:

### 1. Cascade: TSE front-end + ASR back-end

The simplest TS-ASR pipeline runs a TSE system as a front-end and feeds the extracted signal to a standard ASR back-end. This is modular, interpretable, and supports independent development of the two stages. However, the TSE system is typically optimized with a signal-level loss (e.g., SI-SNR or SDR), so the cascade suffers from **artifacts** caused by residual interferers, over-suppression, and non-linear processing distortions, which limit the downstream ASR gains.

### 2. Joint training: differentiable TSE + ASR

The TSE front-end and ASR back-end are interconnected by differentiable operations (e.g., [[concepts/beamforming|beamforming]], feature extraction) and trained end-to-end with an ASR loss [10], [42], [43]. This lets the front-end learn representations that are *useful for ASR* rather than purely for signal-level fidelity, often yielding substantial TS-ASR improvements over the cascade baseline.

### 3. Integrated: clue fusion inside ASR

A fusion layer is inserted directly into the ASR network to condition decoding on the clue, skipping the explicit signal-extraction step entirely [26], [45]. This is computationally cheaper than the cascade/joint variants and avoids the artifact problem, but is less interpretable because no extracted waveform is produced.

## Clue Types

| Clue | Source | Notes |
|:-----|:-------|:------|
| **Audio enrollment** | pre-recorded utterance of the target | most common [10], [26], [45] |
| **Anchor keyword** | a wake-word captured at deployment time | suitable for smart-device scenarios [54] |
| **Visual** | video of the speaker's face/lips | also enables audio-visual ASR back-end [55] |

## Why TS-ASR Is Not Just ASR + TSE

TS-ASR is more than running a TSE front-end followed by ASR — it explicitly targets *recognition of a specific speaker* and exploits the clue *for that purpose*. The signal-level optimum for TSE is not the ASR-level optimum: a clean-sounding extraction may still discard phonetically useful cues if the TSE loss does not know which features the ASR cares about. Joint and integrated TS-ASR designs exist precisely to align the front-end's objective with the downstream task.

## Limitations and Open Issues

- **Clue corruption**: enrollment noise, mismatched recording conditions, or wrong anchor keywords degrade identification.
- **Inactive target speaker**: like TSE, TS-ASR systems are not always trained to abstain when the target is silent.
- **Visual synchronization**: integrated audio-visual TS-ASR requires well-synchronized video; computational cost of visual processing limits low-latency deployment.
- **Open-set speakers**: most TS-ASR work assumes speaker-open training but enrollment-conditioned inference, leaving fully speaker-closed scenarios underexplored.

## Related Concepts

- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/target-speaker-vad|Target-Speaker VAD (TS-VAD)]]
- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/beamforming|Beamforming]]
- ASR back-ends (general automatic speech recognition, not separately surveyed)

## Related Sources

- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova et al. 2023: Neural Target Speech Extraction: An Overview]]
