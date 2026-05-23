---
type: concept
created: 2026-05-23
updated: 2026-05-23
tags:
  - active-noise-control
  - hearables
  - beamforming
  - speech-preserving-anc
  - spatial-filtering
---

# Spatially Selective ANC

**Spatially Selective Active Noise Control (SSANC)** is an ANC variant for hearables (headphones, earbuds, hearing aids) that **suppresses noise from undesired directions while preserving sound from a chosen target direction** at the eardrum. It combines the closed-loop noise reduction of conventional ANC with the spatial discrimination of [[concepts/beamforming|beamforming]].

## Motivation

Conventional [[concepts/feedback-anc|feedback]] and [[concepts/feedforward-anc|feedforward]] ANC reduce all leakage at the inner error microphone uniformly, which also attenuates the talker the user wants to hear (e.g., during a face-to-face conversation while wearing closed-fitting earbuds). SSANC introduces a **directional preference**: noise from the side and back is cancelled, while a target-direction signal (typically frontal speech) reaches the ear with controlled distortion.

## Signal Model

A hearable with $K$ outer microphones, one inner error microphone, and one loudspeaker captures both the leakage at the eardrum $p(n)$ (noise + desired speech) and the secondary-source contribution. The inner-error signal is

$$e(n) = p(n) + (\mathbf{Gw})^T \mathbf{x}(n),$$

where $\mathbf{w}$ is the stacked control filter, $\mathbf{G}$ is the convolution matrix of the secondary path $\mathbf{g}$, and $\mathbf{x}(n)$ stacks the outer-microphone signals (and a leakage estimate when the architecture is hybrid).

## Design Principle: Relative Impulse Responses

Spatial selectivity is encoded in the **acausal relative impulse responses (ReIRs)** $\mathbf{H}$ from the desired direction at each outer microphone with respect to a chosen reference microphone, together with a delayed unit impulse $\boldsymbol{\delta}_\Delta$ as the desired post-filter response. A typical SSANC design solves a [[concepts/soft-constrained-anc|soft-constrained]] cost

$$\min_{\mathbf{w}} \;\; \mathbb{E}\{e^2(n)\} + \mathbf{w}^T \mathbf{B} \mathbf{w} + \beta \, \| \mathbf{H}(\mathbf{q} + \mathbf{Gw}) - \boldsymbol{\delta}_\Delta \|^2,$$

balancing noise reduction against speech distortion via a positive scalar $\beta$. The leakage-selection vector $\mathbf{q}$ extracts the desired (e.g., last) channel of $\mathbf{x}(n)$.

## Key Differences from Related Concepts

| Concept | Selectivity dimension | Online adaptation | Goal |
|:--------|:----------------------|:------------------|:-----|
| Conventional ANC | None | Often yes | Cancel all leakage |
| [[concepts/beamforming|Beamforming]] | Spatial | Sometimes | Spatial filtering at outer mics |
| [[concepts/selective-anc|Selective ANC (SFANC)]] | Spectral / scenario | No (filter switching) | Choose pre-trained controller |
| **Spatially Selective ANC** | **Spatial** | Typically no (offline) | **Cancel non-target directions while preserving target direction at eardrum** |
| [[concepts/speech-preserving-anc|Speech-Preserving ANC]] | Spectral / source | Often yes (deep model) | Preserve speech component |

SSANC is closer in spirit to combining beamforming and ANC than to spectral methods: the **objective itself** encodes the desired spatial response.

## Practical Challenges

- **Secondary path variability**: $\mathbf{g}$ depends strongly on user, fit, and ear-canal geometry. Designing for a single nominal $\mathbf{g}$ leads to large performance spread across users (see [[sources/xiao-2026-robust-spatially-selective-anc|Xiao 2026]]).
- **ReIR direction selection**: The target direction must be specified or estimated; head/torso orientation and movement can violate the assumed ReIRs.
- **Speech-noise trade-off**: The trade-off parameter $\beta$ controls the balance between noise reduction and speech distortion; tuning depends on application (conversation vs. announcement listening).
- **Causality**: ReIRs may include acausal taps; sufficient control filter length and processing delay are required.

## Robustness Strategies

- **Robust soft-constrained design**: Average the cost over a measured set of secondary paths to obtain a single, plant-uncertainty-aware control filter ([[sources/xiao-2026-robust-spatially-selective-anc|Xiao 2026]]).
- **Uncertainty-set design**: Couple SSANC with [[concepts/uncertainty-modeling-for-anc|uncertainty modelling]] strategies developed for feedback ANC ([[sources/hilgemann-2024-data-driven-uncertainty-anc|Hilgemann 2024]]).

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/hybrid-anc|Hybrid ANC]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/soft-constrained-anc|Soft-Constrained ANC]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/speech-preserving-anc|Speech-Preserving ANC]]
- [[concepts/uncertainty-modeling-for-anc|Uncertainty Modeling for ANC]]
- [[concepts/selective-anc|Selective ANC (filter selection)]]

## Related Sources

- [[sources/xiao-2026-robust-spatially-selective-anc|Xiao 2026: Robust Soft-Constrained SSANC for Hearables]]
