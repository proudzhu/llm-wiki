---
type: concept
created: 2026-05-15
updated: 2026-09-13
sources:
  - raw/papers/zhang-2023-hybrid-ahs/full-text.txt
  - raw/papers/zhang-2024-enhanced-hybrid-ahs/full-text.md
tags:
  - deep-learning
  - recurrent-neural-networks
  - attention
  - speech-processing
---

# Self-Attentive Recurrent Neural Network

A **Self-Attentive Recurrent Neural Network (SARNN)** combines recurrent sequence modeling with self-attention so that a model can capture both local temporal evolution and longer-range dependencies across frames.

## Core Idea

Recurrent layers such as GRU or LSTM summarize sequential context through hidden states, while self-attention explicitly reweights information from different time-frequency positions. The combination is useful in speech and audio tasks where both short-term continuity and longer-range structure matter.

## Role in Hybrid AHS

In [[acoustic-howling-suppression|Acoustic Howling Suppression]], Hybrid AHS uses a SARNN after Kalman pre-processing. The network consumes spectral and correlation features derived from the microphone signal and Kalman output, then estimates enhancement filters that suppress howling while preserving target speech.

The final SARNN stage in the paper contains:

- two linear layers
- two multi-head self-attention layers
- one GRU layer
- residual connections

This architecture estimates a three-channel enhancement filter that is applied through deep filtering.

The TASLP journal version ([[sources/zhang-2024-enhanced-hybrid-ahs|Zhang et al. 2024]]) replaces the SARNN with a 2-layer LSTM (300 units, 8 ms frames, magnitude-only features) to keep latency deployment-feasible, with [[concepts/recursive-training|recursive training]] compensating for the smaller model — suggesting the SARNN's capacity was not the decisive factor in the hybrid design.

## Why It Helps

- Recurrent layers track frame-to-frame evolution of feedback and speech
- Self-attention improves modeling of longer-range dependencies and structured tonal artifacts
- The hybrid design complements adaptive filtering by handling nonlinear residual distortion

## Related Concepts

- [[neural-networks|Neural Networks]]
- [[deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[teacher-forcing|Teacher Forcing]]
- [[convolutional-recurrent-network|Convolutional Recurrent Network]]

## Related Sources

- [[sources/zhang-2023-hybrid-ahs|Zhang 2023: Hybrid AHS]]
- [[sources/zhang-2024-enhanced-hybrid-ahs|Zhang, Zhang, Yu & Yu 2024: Enhanced Acoustic Howling Suppression]] — journal version swaps SARNN for a 2-layer LSTM with recursive training
