---
type: concept
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/nakatani-2022-switching-iva/full-text.md
tags:
  - blind-source-separation
  - dereverberation
  - convolutional-beamforming
  - switching-system
  - independent-vector-analysis
---

# Switching CIVA (swCIVA)

**Switching CIVA (swCIVA)** is a blind Convolutional beamforming algorithm with IVA that integrates [[concepts/switching-independent-vector-analysis|Switching IVA (swIVA)]] and switching WPE (swWPE) in a jointly optimal way, adding a switching mechanism to CIVA so that denoising, dereverberation, and source separation remain accurate with only 2–3 microphones (small $M - N$).

## Formulation

A **switching CBF (swCBF)** in its expanded form dereverberates the observed signal $\mathbf{x}_{t,f}$ with $I$ time-invariant MCLP filters and separates the result with $J$ time-invariant separation matrices, then selects one of the $IJ$ outputs per TF point:

$$
\mathbf{z}_{t,f}^{(i)} = \mathbf{x}_{t,f} - (\mathbf{G}_{f}^{(i)})^{\mathsf{H}} \bar{\mathbf{x}}_{t,f}, \qquad
\mathbf{y}_{t,f}^{(i,j)} = (\mathbf{W}_{f}^{(j)})^{\mathsf{H}} \mathbf{z}_{t,f}^{(i)}, \qquad
\mathbf{y}_{t,f} = \sum_{i=1}^{I}\sum_{j=1}^{J} \beta_{t,f}^{(i,j)} \mathbf{y}_{t,f}^{(i,j)}
$$

with hard binary switching weights $\beta_{t,f}^{(i,j)} \in \{0,1\}$, $\sum_{i,j}\beta_{t,f}^{(i,j)}=1$. All parameters are jointly optimized by maximum-likelihood (coordinate ascent):

- **G update**: closed-form per state via source-wise covariance decomposition (extension of swWPE with the spatial model fixed by $\mathbf{W}$);
- **W update**: iterative projection as in AuxIVA, per state, using state-weighted covariances — enabled by separation matrix-wise switching;
- **$\Lambda$ / $\mathbf{B}$ updates**: variance by source power; switch picks the state pair maximizing the local likelihood.

## Factorized vs direct switching model

Two structures for combining the switches (Fig. 1 of the source paper):

| Model | Structure | Assessment |
|-------|-----------|------------|
| **Factorized** | Separate switches for MCLP filters ($I$ states) and separation matrices ($J$ states) | **Adopted** — captures two *different* time-varying characteristics; substantially better accuracy |
| **Direct** | One switch selecting among $J$ complete CBFs | Sub-optimal — cannot decouple dereverberation/separation dynamics; gains saturate beyond $J{=}2$ |

Experiments show the two switch types learn clearly different TF patterns: the separation-matrix switch tracks the observed spectrogram's structure, while the MCLP-filter switch follows the time-varying noise influence instead.

## Key enabling techniques

- [[concepts/coarse-fine-source-model|Coarse-fine source model]] — frequency-independent model for separation-matrix updates, frequency-dependent for MCLP filters and switches;
- Initialization solving the inter-state permutation problem: **blind single-state initialization** (optimize with $J{=}1$, then clone) or **spatially guided initialization** (NN-mask GEVD ATF estimates initialize MPDR beamformers per state);
- [[concepts/weighted-prediction-error|WPE]]-style prediction delay $D$ and CBF length $L$ as in CIVA.

## Complexity and results

Dominant covariance cost stays $O(M^3L^2TF)$ as in CIVA, with extra terms growing in $I$ and $J$ (e.g., $O(IJM^5L^2F)$ from source-wise covariance decomposition). On REVERB-2MIX and TIMIT-ConvMix, swCIVA $(I,J){=}(2,2)$ substantially outperformed CIVA in FWSSNR, WER, and SDR with 2–4 microphones; joint optimization beat cascaded swWPE→swIVA; SIR/denoising/dereverberation all improve individually as states increase from 1 to 3.

## Related Concepts

- [[concepts/switching-independent-vector-analysis|Switching Independent Vector Analysis]]
- [[concepts/coarse-fine-source-model|Coarse-Fine Source Model]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/weighted-prediction-error|Weighted Prediction Error (WPE)]]
- [[concepts/mclp|MCLP]]
- [[concepts/blind-source-separation|Blind Source Separation]]

## Related Sources

- [[sources/nakatani-2022-switching-iva|Nakatani et al. 2022: Switching IVA and Its Extension to Blind and Spatially Guided Convolutional Beamforming]]
