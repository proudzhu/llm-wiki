---
type: concept
created: 2026-10-03
updated: 2026-10-03
sources:
  - raw/papers/huang-2026-neural-directional-filtering/full-text.md
tags:
  - directivity-pattern
  - neural-directional-filtering
  - performance-evaluation
  - microphone-array
---

# Data-Dependent Directivity Metrics

Classical directivity evaluation — the [[concepts/directivity-pattern|directivity pattern]], white noise gain, and directivity factor (DF) — is defined for **fixed linear** beamformers via their weight vector $\mathbf{w}$ (e.g., $\mathcal{DF}=|\mathbf{w}^H\mathbf{d}|^2 / \mathbf{w}^H\boldsymbol{\Gamma}\mathbf{w}$). Masking-based neural spatial filters are data-dependent and non-linear, so no fixed $\mathbf{w}$ exists. Huang et al. (arXiv 2026) proposed estimation methods applicable to **any masking-based method**, separating the analysis of direct and reverberant components.

## Power Pattern Estimation

The estimated mask $\mathcal{M}^{(k)}[f,t]$ for test sample $k$ is applied **separately to the direct-path component of each source** as received by the reference microphone. The narrowband power ratio

$$
\xi_{n}^{(k)}[f]=\frac{\sum_{t}\left|\mathcal{M}^{(k)}[f,t]\,X^{(k)}_{1,n,\textrm{dir}}[f,t]\right|^{2}}{\sum_{t}\left|X^{(k)}_{1,n,\textrm{dir}}[f,t]\right|^{2}}
$$

(and its wideband analogue $\bar{\xi}_n^{(k)}$) is averaged over all test sources located at each candidate direction $\theta_p$ to obtain the estimated narrowband/wideband power pattern $\widehat{\mathcal{P}}[\theta_p,f]$. The mask is computed from the full (reverberant) microphone signals but applied only to the direct sound, so the estimate is **more accurate at high direct-to-reverberation ratio**.

## Directivity Factor Estimation

Assuming the filter is distortionless, the DF is estimated as the ratio of reverberant-component power at the input to that at the output:

$$
\widehat{\mathcal{DF}}[f]=\frac{\sum_{k,t}\left|Y^{(k)}_{1,\textrm{rvb}}[f,t]\right|^{2}}{\sum_{k,t}\left|\mathcal{M}^{(k)}[f,t]\,Y^{(k)}_{1,\textrm{rvb}}[f,t]\right|^{2}},
$$

reflecting the mask's suppression of late reverberation (modelled as diffuse). A target-VDM variant $\widehat{\mathcal{DF}}_{\textrm{target}}$ (with the ideal VDM signal in the denominator) validates the computation: it closely matches the theoretical DF of the target patterns, particularly for 1st-order patterns or high reverberation. The DF estimate is **more accurate at low DRR**, complementing the power-pattern estimate.

## Usage

Applied in [[sources/huang-2026-neural-directional-filtering|Huang et al. 2026]] to compare anechoic-trained (A-Model) and reverberant-trained (R-Model) NDF: the R-Model's DF approaches or exceeds the target VDM's DF at RT60 = 0.6 s — revealing slight over-suppression of reverberation beyond the training range (max RT60 = 0.5 s). The power-pattern method generalizes the per-direction masked/unmasked power-ratio estimation already used for steerable NDF evaluation.

## Related Concepts

- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]
- [[concepts/fixed-beamformer|Fixed Beamformer]]

## Related Sources

- [[sources/huang-2026-neural-directional-filtering|Huang et al. 2026: Neural Directional Filtering with a Compact Microphone Array]] — the introducing paper
