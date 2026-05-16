---
type: concept
created: 2026-05-15
updated: 2026-05-15
sources:
  - raw/papers/zhang-2023-hybrid-ahs/full-text.txt
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

## Related Sources

- [[../sources/zhang-2023-hybrid-ahs|Zhang 2023: Hybrid AHS]]
