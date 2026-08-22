---
type: concept
created: 2026-08-22
updated: 2026-08-22
sources:
  - raw/papers/ruan-2024-speech-extraction-low-snr/full-text.md
tags:
  - blind-source-extraction
  - independent-vector-analysis
  - audio-source-separation
  - optimization-algorithms
---

# Independent Vector Extraction

**Independent Vector Extraction (IVE)** is a computationally efficient variant of [[concepts/independent-vector-analysis|Independent Vector Analysis]] for [[concepts/blind-source-extraction|blind source extraction]]: instead of estimating a full demixing matrix per frequency bin, IVE estimates only the vector related to the source of interest (SOI), modeling the SOI with a non-Gaussian inter-frequency-dependent prior and the background (BG) with a Gaussian model.

## Key Formulations

Stacking separated components along frequency gives source component vectors (SCV) $\mathbf{s}_j$, $\mathbf{z}_j$. The IVE log-likelihood (Ruan et al. 2024, Eq. 8) is:

$$\mathcal{L} = \frac{1}{J}\sum_j \log p_s(\mathbf{s}_j) + \sum_i (N-2)\log|\gamma_i|^2 - \frac{1}{J}\sum_j \sum_{i_1,i_2}\mathbf{x}_{i_1j}^{\mathrm{H}}\mathbf{B}_{i_1}^{\mathrm{H}}\mathbf{R}_{i_1i_2}\mathbf{B}_{i_2}\mathbf{x}_{i_2j} - \log|\det\mathbf{C}_{\mathbf{z}}|$$

where the BG $\mathbf{z}_j \sim \mathcal{N}_C(\mathbf{0}, \mathbf{C}_{\mathbf{z}})$ has an ML-closed-form covariance (no extra update step). A commonly used score function is the normalized tanh:

$$\varphi_i(\boldsymbol{\xi}) = \tanh(\xi_i)^* \Big/ \sqrt{\sum_{i=1}^{I}|\xi_i|^2}$$

normalized each iteration so $J^{-1}\sum_j s_{ij}\varphi_i(\mathbf{s}_j) = 1$ at the stationary point. The **orthogonal constraint** couples the mixing vector $\mathbf{a}_i$ and demixing vector $\mathbf{w}_i$ through the mixture covariance, making the cost a function of either parameterization alone — see [[concepts/ogive|OGIVE]].

## Method Families

| Family | Key idea | Representative |
|---|---|---|
| [[concepts/ogive\|OGIVE]] | Orthogonal constraint + (natural-)gradient ascent; choose $\mathbf{a}$ or $\mathbf{w}$ as optimization term | Koldovský & Tichavský 2018; Ruan et al. 2024 |
| Aux-function IVE | Majorize-minimize updates, monotonic convergence | Janský et al. 2022 (moving speaker) |
| OverIVE | Overdetermined IVE (more mics than sources) | Scheibler & Ono 2019 |
| Fast IVE | Iterative SINR maximization | Scheibler & Ono 2020 |
| Supervised IVE | Guided by speaker identification (x-vectors) | Malek et al. 2022 |

## SNR-Dependent Design Choice

IVE methods are typically formulated and evaluated at moderate SNR (−5 to 5 dB). [[sources/ruan-2024-speech-extraction-low-snr|Ruan et al. 2024]] show that at extremely low SNR (−20 dB) the choice of optimization term becomes decisive: mixing-vector ($\mathbf{a}$) optimization has a wide, flat region of convergence and extracts the *weak* source, while demixing-vector ($\mathbf{w}$) optimization drifts toward the *dominant* (noise) source and fails.

## Related Concepts

- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/blind-source-extraction|Blind Source Extraction]]
- [[concepts/ogive|OGIVE]]
- [[concepts/natural-gradient|Natural Gradient]]

## Related Sources

- [[sources/ruan-2024-speech-extraction-low-snr|Ruan, Liao, Chen & Lu 2024: Speech Extraction Under Extremely Low SNR Conditions]]
- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]]
