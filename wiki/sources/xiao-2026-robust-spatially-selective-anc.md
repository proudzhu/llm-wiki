---
type: source
created: 2026-05-23
updated: 2026-05-23
sources:
  - raw/papers/xiao-2026-robust-spatially-selective-anc/full-text.txt
  - http://arxiv.org/abs/2605.17407
  - zotero://select/items/0_33LYSUKU
tags:
  - active-noise-control
  - spatially-selective-anc
  - hearables
  - secondary-path-modeling
  - robust-control
  - soft-constrained-optimization
  - speech-preserving-anc
---

# Xiao, Roden, Blau & Doclo 2026: Robust Soft-Constrained Spatially Selective ANC for Hearables under Secondary Path Variations

**Authors**: [[entities/tong-xiao|Tong Xiao]], [[entities/reinhild-roden|Reinhild Roden]], [[entities/matthias-blau|Matthias Blau]], [[entities/simon-doclo|Simon Doclo]]
**Institutions**: Carl von Ossietzky Universität Oldenburg & Jade-Hochschule, Oldenburg, Germany; Cluster of Excellence "Hearing4all.connects"
**Type**: Preprint (arXiv)
**Published**: arXiv:2605.17407 [eess.AS], May 2026
**DOI**: [10.48550/arXiv.2605.17407](https://doi.org/10.48550/arXiv.2605.17407)
**Zotero**: [33LYSUKU](zotero://select/items/0_33LYSUKU)

---

## Summary

Spatially selective active noise control (SSANC) hearables aim to suppress noise from undesired directions at the eardrum while preserving speech from a chosen direction. Existing soft-constrained SSANC formulations assume an accurate model of the secondary path from the loudspeaker to the inner error microphone — an assumption that fails in practice because the path varies across users and device fits. This paper proposes a **robust soft-constrained optimization** that computes a single control filter by minimizing the average cost over a set of $J=44$ measured secondary path estimates. Both simulations and a real-time dSPACE implementation show that the robust filter trades a small drop in mean performance for a substantial reduction of the 5th–95th percentile spread under secondary path mismatch, providing a practical design strategy when an exact secondary path is unavailable.

## Problem Formulation

### Signal Model

The hearable has $K$ outer microphones, one inner error microphone, and one loudspeaker (secondary source). The inner error microphone signal is

$$e(n) = p(n) + (\mathbf{Gw})^T \mathbf{x}(n), \tag{1}$$

where $p(n)$ is the leakage at the eardrum (noise + desired speech), $\mathbf{w} \in \mathbb{R}^{(K+1) L_w}$ is the stacked control filter (per-channel length $L_w$), and $\mathbf{G}$ is the block-diagonal convolution matrix of the secondary path $\mathbf{g}$ of length $L_g$. The stacked input vector $\mathbf{x}(n)$ contains the $K$ outer-microphone signals plus an estimate $\hat{p}(n)$ of the leakage.

The estimated leakage is computed via an estimate $\hat{\mathbf{g}}$ of the secondary path:

$$\hat{p}(n) = e(n) - \hat{\mathbf{g}}^T \mathbf{y}(n). \tag{6}$$

When the estimate is exact ($\hat{\mathbf{g}} = \mathbf{g}$), $\hat{p}(n) = p(n) = \mathbf{q}^T \mathbf{x}(n)$, with $\mathbf{q} = [\mathbf{0}^T \dots \mathbf{0}^T \, \boldsymbol{\delta}^T]^T$ a leakage-selection vector.

### Soft-Constrained Cost Function

Building on the soft-constrained SSANC formulation in earlier work (Xiao et al., WASPAA 2025), the cost balances noise reduction against speech distortion via a positive scalar $\beta$:

$$\min_{\mathbf{w}} \;\; \mathbb{E}\{e^2(n)\} + \mathbf{w}^T \mathbf{B} \mathbf{w} + \beta \, \| \mathbf{H}(\mathbf{q} + \mathbf{Gw}) - \boldsymbol{\delta}_\Delta \|^2. \tag{9}$$

- $\mathbf{B} = \mathrm{blkdiag}(\eta_{FF} \mathbf{I}, \dots, \eta_{FF} \mathbf{I}, \eta_{FB} \mathbf{I})$ is the regularisation matrix with separate feedforward and feedback weights.
- $\mathbf{H}$ contains the **acausal relative impulse responses (ReIRs)** of the desired speech direction at each outer microphone with respect to a chosen reference microphone; $\boldsymbol{\delta}_\Delta$ is the delayed unit impulse with delay $\Delta$ and amplification $\alpha$.
- A larger $\beta$ favours speech preservation; a smaller $\beta$ favours noise reduction at the cost of speech distortion.

The matched-case closed-form solution is

$$\mathbf{w}_{\mathrm{soft}} = -\big(\boldsymbol{\Phi}_{rr} + \beta \mathbf{G}^T \mathbf{H}^T \mathbf{H} \mathbf{G}\big)^{-1} \big(\boldsymbol{\phi} - \beta \mathbf{G}^T \mathbf{H}^T (\boldsymbol{\delta}_\Delta - \mathbf{H q})\big), \tag{12}$$

with $\boldsymbol{\Phi}_{rr} = \mathbf{G}^T \mathbb{E}\{\mathbf{x}(n)\mathbf{x}^T(n)\} \mathbf{G} + \mathbf{B}$ and $\boldsymbol{\phi} = \mathbf{G}^T \mathbb{E}\{\mathbf{x}(n)\mathbf{x}^T(n)\} \mathbf{q}$.

## Methodology

### Three Evaluation Cases

| Case | Optimisation path | Evaluation path | Purpose |
|:-----|:------------------|:----------------|:--------|
| 1. Matched (oracle) | $\mathbf{G}$ | Same $\mathbf{G}$ | Upper bound for the formulation |
| 2. Mismatched | One $\mathbf{G}_j$ from the set | The remaining $J-1$ paths | Sensitivity to single-path error |
| 3. Robust (proposed) | Average over $\{\mathbf{G}_j\}_{j=1}^{J}$ | All paths in the set | Robust design across variations |

### Case 3: Robust Optimisation

The robust filter minimises the **average cost across the $J$ secondary path estimates**:

$$\min_{\mathbf{w}} \;\; \frac{1}{J} \sum_{j=1}^{J} \Big[ \mathbb{E}\{e_j^2(n)\} + \beta \, \| \mathbf{H}(\mathbf{q} + \mathbf{G}_j \mathbf{w}) - \boldsymbol{\delta}_\Delta \|^2 \Big] + \mathbf{w}^T \mathbf{B} \mathbf{w}. \tag{15}$$

The closed-form solution averages the secondary-path-dependent matrices and vectors:

$$\mathbf{w}_{\mathrm{robust}} = -\Big(\boldsymbol{\Phi}_{rr} + \beta \, \tfrac{1}{J} \sum_{j=1}^{J} \mathbf{G}_j^T \mathbf{H}^T \mathbf{H} \mathbf{G}_j \Big)^{-1} \big(\bar{\boldsymbol{\phi}} - \beta \, \tfrac{1}{J} \sum_j \mathbf{G}_j^T \mathbf{H}^T (\boldsymbol{\delta}_\Delta - \mathbf{H q})\big). \tag{16}$$

This formulation is conceptually identical to robust min-mean-of-cost designs used for sound pressure equalisation (Schepker et al., EURASIP JASMP 2022).

### Generation of the Secondary Path Set

- **Reference paths** identified by least-squares estimation on a GRAS 45BB-12 KEMAR head with closed-fitting hearables under white-noise excitation.
- **$J=44$ variations** generated by perturbing the KEMAR-identified paths to model fit and anatomy variability (the paper draws on individual transfer-function databases such as the [Hearpiece database](https://doi.org/10.5281/zenodo.5886987) — Denk & Kollmeier 2021).

## Experimental Setup

| Parameter | Value |
|:----------|:------|
| Outer microphones | 4 (entrance + concha at L/R) |
| Inner error mics | 2 (one per ear, #5 and #6) |
| Reference microphones | Entrance microphones #1 (L) and #3 (R) |
| Sampling rate | 40 kHz (dSPACE SCALEXIO LabBox + FPGA) |
| Control filter length $L_w$ | 1800 |
| Secondary path length $L_g$ | 1800 |
| ReIR causal/anticausal length $L_a = L_h$ | 4500 |
| Desired speech delay $\Delta$ | 240 samples (6 ms) |
| Speech amplification $\alpha$ | 2.0 |
| FF regularisation $\eta_{FF}$ | $\lambda_{\max} / 10^4$ |
| FB regularisation $\eta_{FB}$ | $30 \, \eta_{FF}$ |
| Trade-off $\beta$ | 1 to 3000 ($\log_{10}\beta \in [0, 3.48]$) |
| Number of secondary paths $J$ | 44 |
| Acoustic scene | $7 \times 6 \times 2.7$ m, $T_{60} \approx 370$ ms |
| Desired speech | VCTK speaker p361 at $0°$, 0.7 m |
| Noise sources | Two airplane-cabin sources at $60°$ (0.7 m) and $245°$ (0.9 m); 12-loudspeaker pub-scene diffuse noise via TASCAR |
| Mean leakage SNR | $-7.0$ dB ($-6.6$ dB left, $-7.2$ dB right) |
| Real-time platform | dSPACE SCALEXIO LabBox with FPGA |

### Metrics

- **Noise Reduction (NR)** in dB — reduction of leakage noise component at the inner error mic.
- **Intelligibility-weighted Spectral Distortion** $SD_{\text{intellig}}$ — band-importance-weighted spectral distortion of the speech component, following [25,26] and ANSI S3.5.
- **Narrowband PESQ improvement**.
- **ESTOI improvement**.

## Results

For the right inner error microphone (#6):

- **Case 1 (Matched / Oracle)**: best mean performance across all metrics with the **narrowest spread** — establishes an effective upper bound for the formulation.
- **Case 2 (Mismatched)**: mean performance comparable to Case 1 but with a **substantially wider 5th–95th percentile**: up to ~6 dB spread for noise reduction and a noticeably wider PESQ-improvement band. Speech distortion and ESTOI are less affected.
- **Case 3 (Robust, proposed)**: mean **slightly below** Case 1, comparable to Case 2, but the percentile range is **significantly narrowed** across the entire $\beta$ sweep. Performance becomes consistent across all 44 secondary path estimates.

### Real-Time Validation

Filters from Cases 1 and 3 were deployed on the dSPACE platform in the same scene with $\beta = 150$ ($\log_{10}\beta \approx 2.18$). Spectra of the speech and noise components at the inner error microphones (#5, #6) closely match the simulation predictions for both the matched and the robust cases, confirming the simulation findings under real acoustic conditions.

## Key Contributions

1. **Robust soft-constrained SSANC formulation**: A min-mean-of-cost criterion (Eq. 15) over a measured set of secondary paths yields a single robust control filter (Eq. 16) without requiring online identification.
2. **Quantitative characterisation of secondary-path mismatch in SSANC**: Demonstrates that single-path optimisation produces a ~6 dB NR percentile spread under variations, motivating the robust design.
3. **Insight on which metrics are sensitive to mismatch**: Noise reduction and PESQ improvement are most affected by secondary path variations, while speech distortion ($SD_{\text{intellig}}$) and ESTOI improvement are comparatively robust.
4. **Real-time validation**: Implementation on a dSPACE SCALEXIO LabBox + FPGA with closed-fitting KEMAR hearables confirms the simulation results, narrowing the gap between offline analysis and practical deployment.

## Important Distinctions

- **Different from selective fixed-filter ANC (SFANC)**: SFANC switches between pre-trained controllers based on noise classification; here a **single robust filter** is computed offline to handle plant uncertainty rather than disturbance variability.
- **Different from data-driven uncertainty modelling for headphones** ([[sources/hilgemann-2024-data-driven-uncertainty-anc|Hilgemann 2024]]): Hilgemann captures plant uncertainty as a frequency-dependent geometric set $\Pi_\mu$ for IMC robust stability; this paper averages a discrete sample of measured plants in a soft-constrained SSANC cost. Both target secondary path variations but at different levels of abstraction.
- **Different from spectral speech-preserving ANC** ([[sources/dai-2026-speech-preserving-deep-anc|Dai 2026]]): selectivity here is **spatial** (ReIRs encode direction) rather than spectral.

## Future Work Directions

- Extending the robust criterion beyond uniform averaging (e.g., min-max or worst-case weighting over the path set).
- Online refinement of the path set or hybrid robust + adaptive-update schemes.
- Generalisation to open-fitting hearables (where ReIRs are acausal in different ways) and to multi-loudspeaker secondary sources.
- Coupling the robust filter with online leakage estimation under mismatched $\hat{\mathbf{g}}$.

## Related Concepts

- [[concepts/spatially-selective-anc|Spatially Selective ANC]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/uncertainty-modeling-for-anc|Uncertainty Modeling for ANC]]
- [[concepts/robust-control|Robust Control]]
- [[concepts/speech-preserving-anc|Speech-Preserving ANC]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/hybrid-anc|Hybrid ANC]]

## Related Sources

- [[sources/hilgemann-2024-data-driven-uncertainty-anc|Hilgemann 2024: Data-Driven Uncertainty Modeling for Robust Feedback ANC]]
- [[sources/dai-2026-speech-preserving-deep-anc|Dai 2026: Speech-Preserving Deep ANC]]
- [[sources/liebich-2018-doa-dependency-anc-headphones|Liebich 2018: DOA Dependency of ANC Headphones]]
- [[sources/yin-2023-selective-fixed-filter-anc-headphones|Yin 2023: Selective Fixed-Filter ANC for Headphones]]

## Related Synthesis

- [[synthesis/ai-driven-anc|AI-Driven ANC]]
- [[synthesis/anc-architecture-evolution|ANC Architecture Evolution]]
- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]
