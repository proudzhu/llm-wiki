---
type: source
created: 2026-04-29
updated: 2026-04-29
sources:
  - raw/papers/oviste-2026-neural-vslf-speech-enhancement/full-text.txt
  - https://ieeexplore.ieee.org/abstract/document/11464002
  - zotero://select/items/0_K2TY3FFD
tags:
  - multi-channel-speech-enhancement
  - variable-span-linear-filter
  - hybrid-method
  - beamforming
  - spatial-covariance-matrix
  - icassp
---

# Oviste, Mowlaee, Badajoz-Davila, Jensen & Christensen 2026: Neural Variable Span Filters for Interpretable Multi-Channel Speech Enhancement

**Authors**: [[../entities/tom-oviste|Tom Oviste]], [[../entities/pejman-mowlaee|Pejman Mowlaee]], [[../entities/javier-badajoz-davila|Javier Badajoz-Davila]], [[../entities/jesper-rindom-jensen|Jesper Rindom Jensen]], [[../entities/mads-graesboell-christensen|Mads Græsbøll Christensen]]
**Institutions**: GN Group, Ballerup, Denmark; Audio Analysis Lab, Aalborg University, Denmark
**Published**: ICASSP 2026, pp. 20996–21000
**Type**: Conference Paper
**DOI**: [10.1109/ICASSP55912.2026.11464002](https://doi.org/10.1109/ICASSP55912.2026.11464002)
**Zotero**: [K2TY3FFD](zotero://select/items/0_K2TY3FFD)

---

## Summary

Proposes the **Hybrid Variable Span Filter (HVSF)** architecture that integrates the Variable Span Linear Filter (VSLF) framework into a DNN-guided multi-channel speech enhancement system. The DNN predicts three intermediate quantities — clean-speech SCM, overall-noise SCM, and speech-distortion tradeoff parameter — to compute complex VSLF weights. The method improves speech intelligibility and quality over end-to-end baselines while enabling explicit control over the tradeoff between speech distortion and noise reduction.

---

## Problem Formulation

### Signal Model

Noisy mixture at M microphones in time-frequency domain:

$$y[t,f] = x[t,f] + r[t,f] + d[t,f] + v[t,f] \in \mathbb{C}^M$$

where $x$ = target dry speech, $r$ = speech reverberation, $d$ = interfering speech, $v$ = ambient noise. Simplified as:

$$y[t,f] = x[t,f] + n[t,f]$$

Goal: recover reference-channel clean speech $X_1[t,f]$ via complex filter $h[t,f]$:

$$\hat{X}_1[t,f] = h[t,f]^H y[t,f]$$

### Three Categories of Multi-Channel Speech Enhancement

| Category | Examples | Characteristics |
|:---------|:---------|:----------------|
| Linear filtering (probabilistic) | MWF, MVDR, GEV beamformer | Interpretable, controllable tradeoff |
| End-to-end data-driven | [8]–[11] | Black box, implicit tradeoff |
| Hybrid methods | [12]–[14] | DNN guides linear filter, explainable |

---

## Methodology

### Variable Span Linear Filter (VSLF) Framework

The VSLF framework derives optimal linear filters with controllable tradeoff between speech distortion and noise reduction. It generalizes MWF, MVDR, and GEV beamformers as special cases.

**Key quantities**:
- Clean-speech SCM: $\Phi_x = \mathbb{E}[xx^H]$
- Overall-noise SCM: $\Phi_n = \mathbb{E}[nn^H]$
- Joint diagonalization: $B^H \Phi_x B = \Lambda$, $B^H \Phi_n B = I_M$
- Generalized eigenvalues $\Lambda$ ordered decreasingly
- Span dimension $Q \in \{1, \ldots, M\}$ partitions eigenvalues

**Optimal VSLF weights**:

$$h_Q^{(\mu)} = B_{:Q} (\Lambda_{:Q} + \mu I_Q)^{-1} B_{:Q}^H \Phi_x i_1$$

where $\mu \geq 0$ controls speech distortion vs noise reduction tradeoff, and $Q$ controls the subspace span.

**Special cases**:
- $\mu=1, Q=M$ → Multi-Channel Wiener Filter (MWF)
- $\mu=0, Q=P$ (true rank of $\Phi_x$) → MVDR beamformer

### Hybrid Variable Span Filter (HVSF) Architecture

The HVSF uses a DNN to estimate the necessary quantities from noisy spectrogram $y$:

1. **Feature extraction**: Stack of 6M features — log-spectral, cosine, sine, and their time-deltas
2. **DNN prediction**: Real-valued array $z = [z_x, z_n, z_\mu] \in \mathbb{R}^{M^2 + M^2 + 1}$
3. **SCM construction**:
   - Clean-speech SCM: $\hat{\Phi}_x = L_x L_x^H$ via Cholesky decomposition from $z_x$
   - Overall-noise SCM: $\hat{\Phi}_n = L_n L_n^H$ via Cholesky from $z_n$
4. **GEVD computation**: $\Psi = L_n^{-1} \hat{\Phi}_x L_n^{-H}$, eigendecomposition yields $(\hat{\Lambda}, \hat{B})$
5. **Span dimension estimation**: $Q = |\{\Lambda_{m,m} > \tau\}|$ (eigenvalues above threshold $\tau$)
6. **Tradeoff parameter**: $\hat{\mu} = 10^{z_\mu} \in \mathbb{R}_{>0}$
7. **VSLF weights**: $\hat{h}_Q$ computed per Eq. (12)
8. **Reconstruction**: Inverse STFT to time domain

### Loss Function

Combined time-domain and TF-domain magnitude loss:

$$\mathcal{L} = \alpha \|\hat{x}_1 - x_1\|_1 + \|\hat{X}_1 - X_1\|_1$$

---

## Experimental Setup

| Parameter | Value |
|:----------|:------|
| Microphones | M = 4 (simulating true-wireless earbuds) |
| Room size | 4–10m × 4–10m × 3–5m |
| Reverberation time | 0–1 second |
| SNR | Uniform [0, 30] dB |
| SIR | Uniform [−5, 15] dB |
| Speech corpora | VCTK (target), LibriSpeech (interferer) |
| Noise corpus | DEMAND |
| STFT | Hamming window 512, hop 256 |
| Sample rate | 16 kHz |
| Training data | 60k pairs (80 hours) |
| Validation data | 6k pairs |
| Test data | 6k pairs |

---

## Results

HVSF improves speech intelligibility and quality over end-to-end baselines while enabling explicit control of the tradeoff between speech distortion and noise reduction. The method offers interpretability of the rank of the clean-speech SCM and control over the filter's performance in noise attenuation and speech preservation.

---

## Key Contributions

1. **First integration of VSLF into DNN-guided architecture**: HVSF generalizes beyond MWF/MVDR to the full VSLF framework
2. **Interpretable intermediate parameters**: DNN predicts SCMs and tradeoff parameter, enabling analysis of estimated rank and filter behavior
3. **Explicit tradeoff control**: Unlike end-to-end methods, HVSF allows explicit control over speech distortion vs noise reduction
4. **Span dimension estimation**: Threshold-based eigenvalue analysis provides adaptive filter span at every TF bin

---

## Related Concepts

- [[../concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[../concepts/variable-span-linear-filter|Variable Span Linear Filter]]
- [[../concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[../concepts/mvdr-beamformer|MVDR Beamformer]]
- [[../concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[../concepts/generalized-eigenvalue-decomposition|Generalized Eigenvalue Decomposition]]

## Related Synthesis

- [[../synthesis/multimodal-bc-speech-enhancement|Multimodal BC Speech Enhancement]]
