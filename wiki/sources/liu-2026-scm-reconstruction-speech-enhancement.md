---
type: source
created: 2026-04-30
updated: 2026-04-30
sources:
  - raw/papers/liu-2026-scm-reconstruction-speech-enhancement/paper.pdf
  - https://doi.org/10.1109/ICASSP55912.2026.11464924
  - zotero://select/items/0_4RJXKQ8F
tags:
  - speech-enhancement
  - spatial-covariance-matrix
  - multi-source
  - reverberation
  - microphone-arrays
  - multichannel-wiener-filter
  - adaptive-algorithm
  - variance-ratio
  - coherence-matrix
  - icassp
---

# Liu, Luo, Jin, Huang, Chen, Benesty & Makino 2026: SCM Reconstruction for Speech Enhancement

> 📎 [Zotero](zotero://select/items/0_4RJXKQ8F) | [IEEE](https://ieeexplore.ieee.org/abstract/document/11464924) | DOI: 10.1109/ICASSP55912.2026.11464924

| | |
|---|---|
| **Authors** | [[../entities/wei-liu\|Wei Liu]], Xueqin Luo, Jilu Jin, [[../entities/gongping-huang\|Gongping Huang]], [[../entities/jingdong-chen\|Jingdong Chen]], [[../entities/jacob-benesty\|Jacob Benesty]], [[../entities/shoji-makino\|Shoji Makino]] |
| **Institutions** | Wuhan University; Northwestern Polytechnical University; INRS-EMT, University of Quebec; Waseda University |
| **Venue** | ICASSP 2026 |
| **Pages** | 15867–15871 |
| **Year** | 2026 |
| **Type** | Conference Paper |

## Summary

Proposes an online SCM reconstruction method for multi-source speech enhancement in reverberant environments. The normalized observation SCM is decomposed as a linear combination of predefined coherence matrices (source, diffuse, noise), and the combination weights (variance ratios) are estimated via a lightweight multiplicative update algorithm with KL-divergence regularization. The reconstructed SCMs are used in a multichannel Wiener filter (R-MWF), achieving competitive performance in both simulated and real recordings.

## Problem Formulation

Consider a compact planar microphone array with $M$ elements in a reverberant, noisy environment with $I$ acoustic point sources. In the STFT domain:

$$\mathbf{y}(k,n) = \sum_{i=1}^{I} \mathbf{x}_i(k,n) + \mathbf{r}(k,n) + \mathbf{v}(k,n)$$

where $\mathbf{x}_i = \mathbf{a}_i S_i$ is the early component of source $i$ (with RTF vector $\mathbf{a}_i$), $\mathbf{r}$ is late reverberation, and $\mathbf{v}$ is additive noise — all mutually uncorrelated.

The observation SCM is:

$$\Phi_{\mathbf{y}} = \sum_{i=1}^{I} \phi_i \Gamma_i + \phi_R \Gamma_d + \phi_V I_M$$

Normalizing by trace ($\phi_Y = \frac{1}{M}\text{tr}[\Phi_{\mathbf{y}}]$):

$$\Gamma_{\mathbf{y}}(n) = \sum_{i=1}^{I} \psi_i(n) \Gamma_i(n) + \psi_R(n) \Gamma_d + \psi_V(n) I_M$$

with variance ratios $\psi_i = \phi_i/\phi_Y$, $\psi_R = \phi_R/\phi_Y$, $\psi_V = \phi_V/\phi_Y$, subject to $\psi \geq 0$ and $\sum \psi = 1$.

The coherence matrices are:
- $\Gamma_i = \mathbf{a}_i \mathbf{a}_i^H$ — rank-one, from RTF or DOA
- $\Gamma_d$ — diffuse-field (sinc model): $[\Gamma_d]_{ij} = \text{sinc}(2\pi f_s k \delta_{ij} / Kc)$
- $I_M$ — spatially white noise

## Methodology

### Constrained Optimization for Variance Ratios

$$\min_{\psi(n)} \left\| \Gamma_{\mathbf{y}}(n) - \sum_{i=1}^{I}\psi_i(n)\Gamma_i(n) - \psi_R(n)\Gamma_d - \psi_V(n)I_M \right\|_F^2$$

$$\text{s.t.} \quad \psi \geq 0, \quad \|\psi\|_1 = 1$$

Vectorizing matrices converts this to: $\min_h \|c - \Upsilon h\|_2^2$ s.t. $h \succeq 0$, $\|h\|_1 = 1$.

### Multiplicative Update Algorithm

KL-divergence regularization between consecutive estimates controls step size. The resulting update rule:

$$h(n) = \frac{h(n-1) \circ r(n)}{h^T(n-1) r(n)}$$

where the multiplicative vector:

$$r(n) = \exp\left\{\eta \, \Re\left[\Upsilon^H(n)\varepsilon(n)\right]\right\}$$

- $\varepsilon(n) = c(n) - \Upsilon(n)h(n)$ — posterior error
- $\eta$ — step size (set to 0.1)
- Forgetting factor $\alpha = 0.5$ for recursive covariance estimation
- Complexity: $\mathcal{O}(M^2(I+2))$ per time-frequency bin

### R-MWF Formulation

$$h_{W,1}(n) = \psi_1(n) \Gamma_{\mathbf{y}}^{-1}(n) \Gamma_1(n) u$$

where $u = [1, 0, \ldots, 0]^T$ and $\Gamma_{\mathbf{y}}(n)$ is reconstructed from variance ratios.

## Experimental Setup

| Parameter | Simulation | Real Recordings |
|-----------|-----------|-----------------|
| **Array** | 4-element ULA, 2 cm spacing | 4-element UCA, 3 cm radius (from 32-ch RealMAN) |
| **Room** | 8×6×3 m³, $T_{60} \approx 300$ ms | LivingRoom6 / OfficeRoom1 / BadmintonCourt1 |
| **$T_{60}$** | 300 ms | 398 / 719 / 1577 ms |
| **Sources** | 1 target + 2 interferers (semi-circle, min 15° separation) | 1 speaker at 0.8–6 m |
| **SNR** | 0, 10, 20 dB | Real noise conditions |
| **Dataset** | TIMIT + Image Method RIRs | RealMAN dataset |
| **STFT** | 256 samples, 75% overlap, Kaiser window ($\beta=1.9\pi$) | Same |
| **Baselines** | DG-MVDR [17], MVJD-MWF-I [29], MVJD-MWF-II [29] | Same |
| **Metrics** | SNRseg, SDR, STOI | SNRseg, SDR, STOI, CD |

## Results

### Simulation Results

R-MWF consistently outperforms all baselines across SNR levels (0/10/20 dB) in SNRseg, SDR, and STOI, confirmed over 100 random configurations per SNR level.

### Real Recording Results

| Scene | $T_{60}$ | Method | SNRseg (dB) | SDR (dB) | STOI | CD |
|-------|----------|--------|-------------|----------|------|-----|
| LivingRoom6 | 398 ms | Observed | 1.16 | 6.43 | 0.68 | 4.37 |
| | | DG-MVDR | 2.66 | 7.20 | 0.71 | 3.86 |
| | | MVJD-MWF-I | 2.98 | 7.35 | 0.70 | 3.82 |
| | | MVJD-MWF-II | 3.07 | 7.20 | 0.70 | 3.93 |
| | | **R-MWF** | **4.66** | **9.15** | **0.76** | **3.51** |
| OfficeRoom1 | 719 ms | Observed | 2.11 | 0.02 | 0.75 | 4.75 |
| | | DG-MVDR | 4.15 | 6.03 | 0.80 | 4.00 |
| | | MVJD-MWF-I | 4.23 | 5.76 | 0.78 | 4.02 |
| | | MVJD-MWF-II | 4.95 | 6.12 | 0.79 | 3.94 |
| | | **R-MWF** | **5.54** | **6.83** | **0.85** | 4.11 |
| BadmintonCourt1 | 1577 ms | Observed | 0.52 | -6.00 | 0.41 | 4.73 |
| | | DG-MVDR | 1.49 | 3.40 | 0.45 | 4.50 |
| | | MVJD-MWF-I | 1.74 | 3.67 | 0.43 | 4.50 |
| | | MVJD-MWF-II | 1.83 | 3.85 | 0.44 | 4.49 |
| | | **R-MWF** | **2.87** | **4.99** | **0.49** | 4.66 |

R-MWF achieves best or near-best results across all metrics and reverberation conditions, demonstrating strong generalization to real-world recordings.

## Key Contributions

1. **Normalized SCM decomposition**: Reduces SCM reconstruction to variance ratio estimation by normalizing by trace; coherence matrices become precomputable
2. **KL-divergence regularized multiplicative update**: Naturally enforces non-negativity and unity-sum constraints; lightweight $\mathcal{O}(M^2(I+2))$ online algorithm
3. **Flexible coherence matrix input**: Supports both RTF-based and DOA-based coherence matrices
4. **Practical online MWF**: R-MWF achieves competitive speech enhancement without DNN or offline processing

## Related Concepts

- [[../concepts/spatial-covariance-matrix|Spatial Covariance Matrix]] — core concept; this paper introduces normalized decomposition and variance ratio estimation
- [[../concepts/variance-ratio-estimation|Variance Ratio Estimation]] — new concept introduced by this paper
- [[../concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]] — R-MWF is an MWF variant using reconstructed SCMs
- [[../concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — application domain
- [[../concepts/spatial-coherence|Spatial Coherence]] — diffuse-field coherence matrix $\Gamma_d$ is a key component
- [[../concepts/beamforming|Beamforming]] — SCM reconstruction can also serve MVDR beamforming
- [[../concepts/mvdr-beamformer|MVDR Beamformer]] — alternative spatial filter that also requires SCM estimation

## Related Synthesis

- [[../sources/schwarz-2019-dereverberation-spatial-coherence|Schwarz 2019]] — complementary: Schwarz uses CDR for spectral enhancement, Liu 2026 uses SCM reconstruction for MWF
- [[../sources/oviste-2026-neural-vslf-speech-enhancement|Oviste 2026]] — contrast: Oviste uses DNN to predict SCM, Liu 2026 uses analytical reconstruction
- [[../sources/farmani-2026-virtual-mic-beamforming-hearing-aid|Farmani 2026]] — related: VM beamforming also relies on RTF models

## Citation

```bibtex
@inproceedings{Liu2026SCM,
  author    = {Liu, Wei and Luo, Xueqin and Jin, Jilu and Huang, Gongping and Chen, Jingdong and Benesty, Jacob and Makino, Shoji},
  title     = {Spatial Covariance Matrix Reconstruction for Speech Enhancement in Reverberant Multi-Source Environments},
  booktitle = {ICASSP 2026 - 2026 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  pages     = {15867--15871},
  year      = {2026},
  doi       = {10.1109/ICASSP55912.2026.11464924}
}
```
