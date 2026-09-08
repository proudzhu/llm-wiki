---
type: concept
created: 2026-05-23
updated: 2026-09-08
sources:
  - raw/papers/xiao-2023-spatially-selective-anc/full-text.md
  - raw/papers/hu-2026-abse-net/full-text.md
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

## Original Formulation (Xiao 2023): Hard Frost Constraint

The foundational paper ([[sources/xiao-2023-spatially-selective-anc|Xiao, Xu & Zhao 2023]], JASA) derives SSANC on a **hybrid ANC** architecture: a Frost-type linear spatial constraint is imposed as a **hard equality** on the hybrid ANC cost function,

$$\min_{\mathbf{w}} \; \mathbb{E}\{e^2(n)\} \quad \text{such that} \quad \mathbf{H}^T(\tilde{\mathbf{d}} + \mathbf{Gw}) = \mathbf{f},$$

where $\mathbf{H}$ stacks the Toeplitz matrices of the **relative impulse responses (ReIRs)** between each microphone and a reference microphone closest to the desired source, and the constraint vector $\mathbf{f} = \mathbf{h}_K$ fixes the response of the desired-direction signal at the error microphone — so the residual desired component equals the original physical sound, $e_s(n) = s(n)$ (**preserved, not reconstructed**). The closed-form solution decomposes into a Wiener hybrid-ANC term + a Frost-beamformer term (with the secondary-path matrix $\mathbf{G}$ folded in) + a coupling term, and a coupled adaptive (LMS-type) algorithm with projection $\mathbf{P}$ and offset $\mathbf{q}$ handles time-varying environments. Because $\mathbf{G}$ is rank-deficient (secondary-path delays), Tikhonov regularization is required; choosing the regularization factors by the **largest eigenvalue** of the matrices to invert (ratio 5 000–50 000) rather than the sensor-noise-power rule $10\sigma_n^2$ keeps NR at 24.3 dB / SDI at −22.5 dB even under 30 dB sensor-noise perturbation.

Demonstrated on a six-microphone AR-glasses array on KEMAR (desired speech at 0°, babble noise at 60°, a priori SNR −13.2 dB): SNR improved from −13.9 to 15.2 dB (NR 29.1 dB, SDI −25.1 dB), with ~2% of the secondary-source energy of reconstruct-based systems and natural binaural cues preserved. Directivity is bound by ANC causality: directions where noise reaches the error microphone before the reference microphones can only be controlled by the feedback subsystem.

![[raw/papers/xiao-2023-spatially-selective-anc/figures/fig02.png|Block diagram of the original spatially selective ANC system]]

*Figure 2 from Xiao 2023: the adaptive hybrid ANC algorithm is spatially constrained (Frost constraint via ReIRs).*

## Later Evolution: Soft Constraint (Xiao 2025–2026)

Later formulations replace the hard equality with a penalty: spatial selectivity is encoded in the **acausal relative impulse responses (ReIRs)** $\mathbf{H}$ from the desired direction at each outer microphone with respect to a chosen reference microphone, together with a delayed unit impulse $\boldsymbol{\delta}_\Delta$ as the desired post-filter response. The soft-constrained cost (Xiao et al., WASPAA 2025; [[sources/xiao-2026-robust-spatially-selective-anc|Xiao 2026]]) solves

$$\min_{\mathbf{w}} \;\; \mathbb{E}\{e^2(n)\} + \mathbf{w}^T \mathbf{B} \mathbf{w} + \beta \, \| \mathbf{H}(\mathbf{q} + \mathbf{Gw}) - \boldsymbol{\delta}_\Delta \|^2,$$

balancing noise reduction against speech distortion via a positive scalar $\beta$. The leakage-selection vector $\mathbf{q}$ extracts the desired (e.g., last) channel of $\mathbf{x}(n)$. See [[concepts/soft-constrained-anc|Soft-Constrained ANC]] for the trade-offs between hard and soft formulations.

## Key Differences from Related Concepts

| Concept | Selectivity dimension | Online adaptation | Goal |
|:--------|:----------------------|:------------------|:-----|
| Conventional ANC | None | Often yes | Cancel all leakage |
| [[concepts/beamforming|Beamforming]] | Spatial | Sometimes | Spatial filtering at outer mics |
| [[concepts/selective-anc|Selective ANC (SFANC)]] | Spectral / scenario | No (filter switching) | Choose pre-trained controller |
| **Spatially Selective ANC** | **Spatial** | Yes (coupled adaptive) or offline optimal | **Cancel non-target directions while preserving target direction at eardrum** |
| [[concepts/speech-preserving-anc|Speech-Preserving ANC]] | Spectral / source | Often yes (deep model) | Preserve speech component |

SSANC is closer in spirit to combining beamforming and ANC than to spectral methods: the **objective itself** encodes the desired spatial response.

## Relation to Active Binaural Speech Enhancement

A closely related but distinct line targets **open-fit hearing aids**, where the vent that relieves the [[concepts/ear-canal-occlusion-effect|occlusion effect]] also lets noise leak into the ear canal. There the enemy is not non-target *directions* but the leakage component $d_L$ itself, and the objective is to preserve the target's binaural cues (ILD/IPD) while cancelling leakage. [[concepts/abse-net|ABSE-NET]] (Hu et al. 2026) represents the neural, error-microphone-free variant of this idea: a binaural MVDR front-end followed by a lightweight network that synthesizes the anti-leakage signal, achieving the best spatial-cue preservation ($\Delta$ILD 3.047) among compared methods while remaining robust to 15° DOA/ATF mismatch.

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
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]
- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]
- [[concepts/active-binaural-speech-enhancement|Active Binaural Speech Enhancement]]
- [[concepts/abse-net|ABSE-NET]]

## Related Sources

- [[sources/xiao-2026-robust-spatially-selective-anc|Xiao 2026: Robust Soft-Constrained SSANC for Hearables]]
- [[sources/li-2026-geometry-conditioned-ssanc|Li 2026: Geometry-Conditioned Spatially Selective Non-Linear Filter]]
- [[sources/hu-2026-abse-net|Hu et al. 2026: ABSE-NET — Active Binaural Speech Enhancement for Open-Fit Hearing Aids]]
