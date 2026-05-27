---
type: source
created: 2026-05-27
updated: 2026-05-27
sources:
  - raw/papers/lollmann-2020-generalized-coherence-based-signal-enhancement/full-text.md
  - https://doi.org/10.1109/ICASSP40776.2020.9054470
  - zotero://select/items/0_DSYMKBRQ
tags:
  - cdr-estimation
  - generalized-coherence
  - multichannel-signal-enhancement
  - hearing-aids
  - dereverberation
  - speech-enhancement
---

# Löllmann, Brendel & Kellermann 2020: Generalized Coherence-Based Signal Enhancement

**Authors**: [[entities/heinrich-w-lollmann|Heinrich W. Löllmann]], [[entities/andreas-brendel|Andreas Brendel]], [[entities/walter-kellermann|Walter Kellermann]]
**Affiliation**: Chair of Multimedia Communications and Signal Processing, Friedrich-Alexander-Universität Erlangen-Nürnberg
**Published**: ICASSP 2020, pp. 201–205
**DOI**: [10.1109/ICASSP40776.2020.9054470](https://doi.org/10.1109/ICASSP40776.2020.9054470)
**Zotero**: [Link](zotero://select/items/0_DSYMKBRQ)
**Tags**: `cdr-estimation`, `generalized-coherence`, `multichannel-signal-enhancement`, `hearing-aids`, `dereverberation`

## Summary

This ICASSP 2020 paper presents a novel CDR-based speech enhancement approach that uses **generalized magnitude coherence (GMC)** to simultaneously exploit information from more than two microphones. Unlike conventional schemes that use a per-pair CDR estimate followed by a post-filter, this method enhances the most appropriate microphone signal — implicitly selected as a byproduct of the eigenvalue decomposition — without requiring DOA estimation. The approach is evaluated for binaural hearing aids with 4 microphones and consistently outperforms the DOA-independent CDR estimators of Schwarz et al. and Thiergart et al.

## Problem Formulation

The microphone signal model for $N$ microphones in a reverberant environment with diffuse noise:

$$x_i(k) = d_i(k) + n_i(k), \quad i \in \{1,\dots,N\}$$

where $d_i(k)$ is the early reverberant speech (desired) and $n_i(k)$ includes late reverberation and diffuse noise. The CDR at the $i$-th microphone is:

$$\Lambda_i(l,f) = \frac{\Phi_{d_i,d_i}(l,f)}{\Phi_{n_i,n_i}(l,f)}$$

For a microphone pair, the CDR can be expressed via coherence functions:

$$\Lambda_{i,j}(l,f) = \frac{\Gamma_{n_i,n_j}(l,f) - \Gamma_{x_i,x_j}(l,f)}{\Gamma_{x_i,x_j}(l,f) - \Gamma_{d_i,d_j}(l,f)}$$

## Methodology

### Generalized Magnitude Coherence (GMC)

The spectral coherence matrix $\boldsymbol{C}_x(l,f)$ is constructed from pairwise coherence estimates:

$$[\boldsymbol{C}_x(l,f)]_{ij} = \Gamma_{x_i,x_j}(l,f)$$

The GMC is defined as the magnitude-squared coherence generalized to $N$ channels via the largest eigenvalue:

$$\gamma_x(l,f) = \frac{\lambda_x^{(\max)}(l,f) - 1}{N - 1}$$

where $\lambda_x^{(\max)}(l,f)$ is the largest eigenvalue of $\boldsymbol{C}_x(l,f)$. For $N=2$, this reduces to the magnitude of the standard coherence $|\Gamma_{x_1,x_2}(l,f)|$.

### Proposed GMC-Based CDR Estimator

$$\widehat{\Lambda}_{\text{gen}}(l,f) = \frac{\gamma_n(l,f) - \gamma_x(l,f)}{\gamma_x(l,f) - 1}$$

This estimator is inherently real-valued and positive. For $N=2$, it reduces to a magnitude-based CDR estimator using the magnitudes of the coherence functions.

### Microphone Selection via Principal Eigenvector

The most appropriate microphone signal is determined by the principal eigenvector $\boldsymbol{v}_x^{(\max)}(l,f)$ of $\boldsymbol{C}_x(l,f)$:

$$i_{\text{opt}}(l) = \text{round}\{\alpha i_{\text{opt}}(l-1) + (1-\alpha)\bar{i}_{\text{opt}}(l)\}$$

$$\bar{i}_{\text{opt}}(l) = \frac{1}{M}\sum_{m=0}^{M-1} \arg\max_i \{|v_x^{(\max)}(l,f_m,i)|\}$$

The spectral weights (based on CDR estimates) are applied to this selected microphone signal rather than performing a separate post-filtering step.

### Noise Coherence Model for Binaural Hearing Aids

For a 4-microphone binaural HA setup (front+rear on each ear), the noise coherence matrix is block-structured combining intra-device diffuse coherence models and inter-device binaural coherence models:

$$\boldsymbol{C}_n(f) = \begin{bmatrix} 1 & \Gamma_n^{(I)}(f) & \Gamma_n^{(II)}(f) & \Gamma_n^{(II)}(f) \\ \Gamma_n^{(I)}(f) & 1 & \Gamma_n^{(II)}(f) & \Gamma_n^{(II)}(f) \\ \Gamma_n^{(II)}(f) & \Gamma_n^{(II)}(f) & 1 & \Gamma_n^{(I)}(f) \\ \Gamma_n^{(II)}(f) & \Gamma_n^{(II)}(f) & \Gamma_n^{(I)}(f) & 1 \end{bmatrix}$$

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Microphones | 4 (front+rear on each ear, binaural HAs) |
| Rooms | Cafeteria ($T_{60}=1.25$s), Courtyard ($T_{60}=0.9$s), Office I ($T_{60}=0.4$s), Office II ($T_{60}=0.3$s) |
| Input CDR | 5 dB at Mic 1 |
| Sampling rate | 16 kHz |
| STFT | Von Hann window, 380 samples, 190 shift, FFT 512 |
| Spectral weight | $\mu=0.8$, $W_\text{min}=0.1$ |
| Noise coherence | Cylindrically isotropic (2D) binaural model |

**Compared methods**: Thiergart et al. [22] CDR estimator, Schwarz et al. [24] CDR estimator (extended to 4 mics via coherence averaging), and coherence averaging baseline.

### Evaluation Measures
- **SRMR** (Speech-to-Reverberation Modulation Energy Ratio) — non-intrusive
- **fwSNR** (Frequency-weighted Segmental SNR) — intrusive
- **PESQ** (Perceptual Evaluation of Speech Quality) — intrusive

## Results

The proposed GMC-based method consistently achieves the best results across all environments and measures:

| Measure | Best competitor | Proposed GMC | Improvement |
|---------|----------------|--------------|-------------|
| SRMR (avg) | ~5.2 (Courtyard) | ~6.5 | +25% |
| fwSNR (avg) | ~1.7 (Courtyard) | ~1.9 | +12% |
| PESQ (avg) | ~1.5 (Courtyard) | ~1.6 | +7% |

Key observations:
- The GMC-based approach is **clearly superior** to simple averaging of coherence estimates across microphone pairs
- All four CDR estimators achieve close PESQ scores, but the proposed method shows significantly better SRMR and fwSNR
- The method is DOA-independent and requires no side information about source position
- Computational complexity is moderately higher but still significantly lower than real-time on a standard PC

## Key Contributions

1. **GMC-based CDR estimator**: First CDR estimator to exploit generalized magnitude coherence, inherently incorporating information from an arbitrary number of microphones via eigenvalue decomposition
2. **Implicit microphone selection**: The most suitable microphone signal is determined as a byproduct of the principal eigenvector, eliminating the need for DOA estimation
3. **Integration of 4-microphone binaural HA setup**: Noise coherence matrix combining intra-device diffuse and inter-device binaural models
4. **Consistent improvement**: Outperforms existing DOA-independent CDR estimators across all evaluated environments and quality measures

## Related Concepts

- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio (CDR)]]
- [[concepts/generalized-magnitude-coherence|Generalized Magnitude Coherence (GMC)]]
- [[concepts/spatial-coherence|Spatial Coherence]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/diffuse-sound-extraction|Diffuse Sound Extraction]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/beamforming|Beamforming]]

## Related Synthesis

- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]
- [[synthesis/multi-modal-speech-enhancement|Multi-Modal Speech Enhancement]]
