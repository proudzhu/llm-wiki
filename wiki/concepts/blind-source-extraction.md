---
type: concept
created: 2026-08-22
updated: 2026-08-22
sources:
  - raw/papers/ruan-2024-speech-extraction-low-snr/full-text.md
tags:
  - blind-source-extraction
  - audio-source-separation
  - speech-enhancement
  - signal-processing
---

# Blind Source Extraction

**Blind Source Extraction (BSE)** extracts a single source of interest (SOI) directly from a noisy mixture while deliberately *disregarding* the estimation of the background (BG) components (environmental noise, competing sources). It contrasts with [[concepts/blind-source-separation|Blind Source Separation]] (BSS), which estimates *all* sources simultaneously — BSE trades completeness for lower cost and the ability to target a specific source.

## Key Formulations

In the STFT domain, the per-frequency-bin instantaneous model $\mathbf{x}_{ij} = \mathbf{A}_i\mathbf{v}_{ij}$ is partitioned around the SOI:

$$\mathbf{A}_i = [\mathbf{a}_i\ \ \mathbf{Q}_i], \qquad \mathbf{W}_i = \begin{bmatrix}\mathbf{w}_i^{\mathrm{H}}\\ \mathbf{B}_i\end{bmatrix}, \qquad s_{ij} = \mathbf{w}_i^{\mathrm{H}}\mathbf{x}_{ij}$$

Since identifying the BG $\mathbf{z}_{ij} = \mathbf{B}_i\mathbf{x}_{ij}$ is not the goal, $\mathbf{Q}_i$/$\mathbf{B}_i$ can be arbitrary — only the SOI-related column $\mathbf{a}_i$ / row $\mathbf{w}_i^{\mathrm{H}}$ matters. The distortionless-response constraint $\mathbf{w}_i^{\mathrm{H}}\mathbf{a}_i = 1$ ties the two, and a compact parameterization in $(\beta_i, \gamma_i, \mathbf{g}_i, \mathbf{h}_i)$ reduces the free parameters (Ruan et al. 2024, Eq. 4).

## Method Families

- **[[concepts/independent-vector-extraction|Independent Vector Extraction (IVE)]]** — computationally efficient, extraction-targeted variant of IVA; includes [[concepts/ogive|OGIVE]] (orthogonal constraint, gradient-based), auxiliary-function-based IVE, and OverIVE (overdetermined formulation).
- **Neural target-speaker extraction** — clue-driven deep-learning extraction ([[concepts/target-speaker-extraction|Target Speaker Extraction]]); requires a speaker/enrollment clue rather than relying on statistical independence alone.

## Why Extraction (Not Separation) at Low SNR

At extremely low SNR (e.g., −20 dB), separation algorithms that model *all* sources can waste capacity modeling the dominant noise, while BSE methods that model only the SOI (with a simple Gaussian BG model) and choose the right optimization parameter stay robust — the central finding of [[sources/ruan-2024-speech-extraction-low-snr|Ruan et al. 2024]].

## Related Concepts

- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/independent-vector-extraction|Independent Vector Extraction]]
- [[concepts/ogive|OGIVE]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]

## Related Sources

- [[sources/ruan-2024-speech-extraction-low-snr|Ruan, Liao, Chen & Lu 2024: Speech Extraction Under Extremely Low SNR Conditions]]
- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova et al. 2023: Neural Target Speech Extraction Overview]]
