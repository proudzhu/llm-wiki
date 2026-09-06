---
type: concept
created: 2026-05-15
updated: 2026-09-06
sources:
  - raw/papers/zhang-2023-hybrid-ahs/full-text.txt
  - raw/papers/wang-2021-magnitude-phase-compensation/full-text.md
tags:
  - deep-learning
  - recurrent-neural-networks
  - training-strategy
  - speech-processing
---

# Teacher Forcing

**Teacher forcing** is a training strategy for recurrent models in which the ground-truth previous output is fed back into the model during training instead of the model's own prediction.

## Core Idea

In recursive sequence generation, training with ground-truth feedback stabilizes optimization and converts a difficult closed-loop prediction problem into a supervised learning problem. The downside is a train-test mismatch: during inference, the model must consume its own previous outputs.

## Role in Acoustic Howling Suppression

In [[acoustic-howling-suppression|Acoustic Howling Suppression]], teacher forcing is used to replace the recursively generated loudspeaker signal with the ideal target speech during offline training. This reformulates the recursive howling problem as a speech separation problem:

$$y(t) = s(t) + n(t) + h(t) * NL[s(t-\Delta t) \cdot G]$$

This makes offline training tractable while still exposing the model to playback contamination. In Hybrid AHS, the teacher-forced microphone signal is paired with a Kalman-preprocessed signal to train the neural module.

## Role in Magnitude-Domain Training Targets

[[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021]] reinterpret magnitude spectrogram approximation (MSA, loss $\|\hat{M}-|S|\|_{1}$) as teacher forcing with the **target phase**: writing $\mathcal{L}_{\text{MSA}}=\|\hat{M}e^{j\angle S}-|S|e^{j\angle S}\|_{1}$ makes explicit that MSA assumes the estimated speech has the clean phase. Since the best approximation of $S(t,f)$ along $\angle S(t,f)$ is exactly $|S(t,f)|$, the [[concepts/magnitude-phase-compensation-effect|magnitude-phase compensation]] is avoided — MSA produces the most accurate magnitudes among learned models, which is why extracting ASR features directly from estimated magnitudes outperforms re-synthesis with mixture phase.

## Benefits

- Stabilizes recurrent training
- Simplifies supervision for closed-loop systems
- Makes recursive signal processing problems trainable offline

## Limitation

Teacher forcing introduces a mismatch between offline training and streaming inference, so additional design choices are needed to improve robustness when the model is deployed recursively.

## Related Concepts

- [[neural-networks|Neural Networks]]
- [[deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[acoustic-howling-suppression|Acoustic Howling Suppression]]
- [[concepts/magnitude-phase-compensation-effect|Magnitude-Phase Compensation Effect]] — MSA's teacher forcing avoids it

## Related Sources

- [[sources/zhang-2023-hybrid-ahs|Zhang 2023: Hybrid AHS]]
- [[sources/wang-2021-magnitude-phase-compensation|Wang, Wichern & Le Roux 2021: On the Compensation Between Magnitude and Phase in Speech Separation]] — MSA as teacher forcing with target phase
