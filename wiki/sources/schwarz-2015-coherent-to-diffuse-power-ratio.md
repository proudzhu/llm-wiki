---
type: source
created: 2026-05-27
updated: 2026-05-27
sources:
  - raw/papers/schwarz-2015-coherent-to-diffuse-power-ratio/full-text.md
  - https://doi.org/10.1109/TASLP.2015.2418571
  - zotero://select/items/0_AT69JCEX
tags:
  - cdr
  - dereverberation
  - spatial-coherence
  - diffuse-noise-suppression
  - speech-enhancement
  - signal-processing
---

# Schwarz & Kellermann 2015: Coherent-to-Diffuse Power Ratio Estimation for Dereverberation

**Authors**: [[entities/andreas-schwarz|Andreas Schwarz]], [[entities/walter-kellermann|Walter Kellermann]]
**Affiliation**: Chair of Multimedia Communications and Signal Processing, Friedrich-Alexander-Universität Erlangen-Nürnberg
**Published**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, Vol. 23, No. 6, June 2015, pp. 1006–1018
**DOI**: [10.1109/TASLP.2015.2418571](https://doi.org/10.1109/TASLP.2015.2418571)
**Zotero**: [Link](zotero://select/items/0_AT69JCEX)
**Tags**: `cdr`, `dereverberation`, `spatial-coherence`, `diffuse-noise-suppression`, `speech-enhancement`

## Summary

This paper presents a comprehensive theoretical and experimental investigation of coherent-to-diffuse power ratio (CDR) estimation from the spatial coherence between two omnidirectional microphones, and its application to dereverberation. Known CDR estimators are unified in a common framework with geometric interpretation in the complex plane. Several novel unbiased CDR estimators are proposed, and it is shown that knowledge of either the direction of arrival (DOA) or the noise coherence model is sufficient for unbiased CDR estimation. A CDR-based dereverberation system is evaluated using both signal-based quality measures and automatic speech recognition accuracy, demonstrating that the proposed unbiased estimators offer significant practical advantages.

## Problem Formulation

The received microphone signals in the STFT domain are modeled as:

$$X_i(l,f) = S_i(l,f) + N_i(l,f), \quad i = 1,2$$

where $S_i$ is the desired signal component (direct path + early reflections) and $N_i$ is the undesired component (late reverberation/noise). The signals are assumed short-time stationary with identical auto-power spectra at both microphones:

$$\Phi_{s_1 s_1} = \Phi_{s_2 s_2} = \Phi_s, \quad \Phi_{n_1 n_1} = \Phi_{n_2 n_2} = \Phi_n$$

The coherent-to-diffuse power ratio (CDR) is defined as:

$$\text{CDR}(l,f) = \frac{\Phi_s(l,f)}{\Phi_n(l,f)}$$

The complex spatial coherence $\Gamma_x$ of the mixed signal relates to the CDR through:

$$\Gamma_x = \frac{\text{CDR} \cdot \Gamma_s + \Gamma_n}{\text{CDR} + 1}$$

where $\Gamma_s$ is the coherence of the direct signal (determined by TDOA) and $\Gamma_n$ is the coherence of the diffuse noise field ($\Gamma_n = \sin(kd)/(kd)$ for an ideal 3D diffuse field).

## Methodology

### CDR Estimators

The paper formulates several CDR estimators in a unified mathematical framework, illustrated geometrically in the complex plane:

**DOA-dependent estimators (require $\Gamma_s$ and $\Gamma_n$):**

| Estimator | Formula | Bias | Key Property |
|-----------|---------|------|--------------|
| Jeub et al. (17) | $\widehat{CDR}_{\text{Jeub}} = \frac{|\hat\Gamma_x|^2 - \tilde\Gamma_n^2}{\tilde\Gamma_s^2 - |\hat\Gamma_x|^2}$ | Biased | Original heuristic estimator |
| Thiergart et al. (18) | $\widehat{CDR}_{\text{Thiergart1}} = \max(0, \text{Re}\{\frac{\tilde\Gamma_n - \hat\Gamma_x}{\hat\Gamma_x - \tilde\Gamma_s}\})$ | Unbiased | DOA-dependent, sensitive to phase errors |
| Proposed 1 (19) | $\widehat{CDR}_{\text{prop1}} = \max(0, \frac{\tilde\Gamma_s^*(\tilde\Gamma_n - \hat\Gamma_x)}{\text{Re}\{\tilde\Gamma_s^*\hat\Gamma_x\} - 1})$ | Unbiased | Real-part based |
| Proposed 2 (20-21) | $\widehat{CDR}_{\text{prop2}} = \left\|\frac{\tilde\Gamma_s^*(\tilde\Gamma_n - \hat\Gamma_x)}{\text{Re}\{\tilde\Gamma_s^*\hat\Gamma_x\} - 1}\right\|$ | Unbiased | Magnitude-based; best ASR performance |

**DOA-independent estimator (requires only $\Gamma_n$):**

| Proposal 3 (25) | $\widehat{CDR}_{\text{prop3}}$ derived from solving $|\Gamma_s|=1$ via quadratic equation | Unbiased | **Key contribution**: no DOA estimation needed |

**Noise-coherence-independent estimator (requires only $\Gamma_s$):**

| Proposal 4 (27) | $\widehat{CDR}_{\text{prop4}} = \frac{\text{Im}\{\hat\Gamma_x\}}{\text{Im}\{\tilde\Gamma_s\} - \text{Im}\{\hat\Gamma_x\}}$ with extensions | Unbiased | Limited to TDOA $\neq 0$ |

### Geometric Interpretation

The signal, noise, and mixed coherence lie on a straight line in the complex plane connecting $\Gamma_n$ (on the real axis) to $\Gamma_s$ (on the unit circle). The CDR determines the position of $\Gamma_x$ along this line. This geometric view enables intuitive understanding of estimator bias and robustness.

### Dereverberation System

The proposed signal enhancement system consists of:
1. **Preprocessor**: Spatial magnitude averaging of microphone signals in STFT domain to reduce variance
2. **CDR estimation**: One of the proposed estimators
3. **Postfilter**: Spectral magnitude subtraction based on CDR:

$$G(l,f) = \max\left\{G_{\min}, 1 - \sqrt{\frac{\mu}{\widehat{CDR}(l,f) + 1}}\right\}$$

## Experimental Setup

### Rooms and RIR Data

| Room | Dimensions | $T_{60}$ | Source Positions |
|------|-----------|----------|-----------------|
| Room A | 6m × 6m × 3m | ~0.4 s | 40-70 positions |
| Room B (lecture hall) | 7m × 11m × 3m | ~1 s | 40-70 positions |
| Room C (large foyer) | 54m × 7m × 3m | ~3.5 s | 40-70 positions |
| REVERB challenge RIRs | 6 rooms (SR1/2, MR1/2, LR1/2) | 0.2-0.8 s | ~0.5m and ~2m distances |

**Parameters**: Microphone spacing $d = 8$ cm, sampling rate 16 kHz, STFT: window 1024, FFT 512, downsampling 128.

### Evaluation Measures
- **Early-to-late power ratio (ELR)**: quantifying reverberation reduction
- **fwSegSDR**: frequency-weighted segmental signal-to-distortion ratio
- **PESQ**: perceptual speech quality (MOS-LQO scale)
- **ASR recognition rate**: PocketSphinx on GRID corpus

## Results

### Spatial Coherence of Reverberation

Analysis of measured and simulated RIRs confirmed that:
- Late reverberation closely matches the 3D isotropic diffuse field model for rooms with uniformly reflective surfaces
- Rooms with absorbing floor/ceilings match the 2D isotropic model
- Rooms with absorbing walls show higher-than-diffuse coherence due to dominant vertical reflections

### CDR Estimation Performance

**Mean squared error (diffuseness domain) across all rooms:**

| Estimator | Prior Info | Mean MSE |
|-----------|-----------|----------|
| Jeub | DOA, $\Gamma_n$ | 0.120 |
| Thiergart 1 | DOA, $\Gamma_n$ | 0.322 |
| Proposed 1 | DOA, $\Gamma_n$ | 0.109 |
| **Proposed 2** | **DOA, $\Gamma_n$** | **0.070** |
| Thiergart 2 (DOA-indep.) | $\Gamma_n$ | 0.075 |
| **Proposed 3 (DOA-indep.)** | $\Gamma_n$ | **0.071** |
| Proposed 4 (noise-indep.) | DOA | 0.178 |

The DOA-independent Proposed 3 estimator achieves comparable MSE to the best DOA-dependent estimators, without requiring any source direction knowledge.

### Dereverberation Performance

**Mean ASR recognition rates across all evaluated rooms:**

| Method | Required Info | Mean Recognition Rate |
|--------|--------------|---------------------|
| Unprocessed | - | 62.2% |
| Spatial averaging only | - | 63.1% |
| Lebart (oracle $T_{60}$) | $T_{60}$ | 74.7% |
| **Proposed 2 (best)** | **DOA, $\Gamma_n$** | **81.5%** |
| **Proposed 3 (DOA-indep.)** | $\Gamma_n$ | **77.6%** |

The proposed DOA-dependent estimator (Proposed 2) achieved the highest recognition rate among all methods. The DOA-independent estimator (Proposed 3) also showed significant improvement, enabling blind dereverberation without source position knowledge.

## Key Contributions

1. **Unified framework**: Known CDR estimators formulated in a common mathematical framework with geometric interpretation
2. **Novel unbiased estimators**: Multiple unbiased CDR estimators proposed, with different robustness characteristics
3. **DOA-independent CDR estimation**: First unbiased CDR estimator requiring only knowledge of the noise coherence $\Gamma_n$, enabling fully blind dereverberation
4. **Noise-coherence-independent CDR estimation**: Estimator requiring only $\Gamma_s$ (target DOA), useful when noise coherence model is uncertain
5. **Comprehensive evaluation**: Thorough validation using measured RIRs from multiple rooms, with both signal-based and ASR-based evaluation

## Related Concepts

- [[concepts/spatial-coherence|Spatial Coherence]]
- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio (CDR)]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/diffuse-sound-extraction|Diffuse Sound Extraction]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Synthesis

- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]] (background on spatial processing for audio enhancement)
