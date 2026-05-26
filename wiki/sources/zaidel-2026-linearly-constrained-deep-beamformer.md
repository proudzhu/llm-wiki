---
type: source
created: 2026-05-26
updated: 2026-05-26
sources:
  - raw/papers/zaidel-2026-linearly-constrained-deep-beamformer/full-text.md
  - https://doi.org/10.48550/arXiv.2605.21141
  - zotero://select/items/0_TLSRHKI7
tags:
  - deep-learning
  - beamforming
  - speech-enhancement
  - target-speaker-extraction
  - spatial-filtering
---

# Zaidel, Engel, Engel & Gannot 2026: Linearly Constrained Deep Beamformer for Multi-Speaker Scenarios

| Field | Details |
|-------|---------|
| **Authors** | [[entities/ilai-zaidel\|Ilai Zaidel]], [[entities/ori-engel\|Ori Engel]], [[entities/bar-engel\|Bar Engel]], [[entities/sharon-gannot\|Sharon Gannot]] |
| **Institution** | Faculty of Engineering, Bar-Ilan University, Ramat-Gan, Israel |
| **Venue** | arXiv preprint |
| **Year** | 2026 |
| **Type** | Preprint |
| **DOI** | [10.48550/arXiv.2605.21141](https://doi.org/10.48550/arXiv.2605.21141) |
| **Zotero** | [Open](zotero://select/items/0_TLSRHKI7) |

## Summary

This paper proposes a fully DNN-based beamforming framework for enhancing target speaker(s) in multi-speaker environments. A deep neural network is trained to estimate beamforming weights directly from noisy multichannel inputs while satisfying linear spatial constraints through an adaptive multi-term loss inspired by the augmented Lagrangian framework. The loss combines signal reconstruction (SI-SDR) with penalties that enforce a distortionless response toward the target and suppress the interference subspace. The model is guided by the estimated target relative transfer function (RTF) and interference subspace, learned via covariance whitening.

## Problem Formulation

In the STFT domain, the multichannel mixture signal is modeled as:

$$
\mathbf{y}(l,k)=\mathbf{H}(k)\mathbf{s}(l,k)+\mathbf{n}(l,k)\in\mathbb{C}^{M\times 1}
$$

where $l$ and $k$ denote time-frame and frequency-bin indices, $M$ is the number of microphones, $\mathbf{s}(l,k)\in\mathbb{C}^{J}$ contains $J$ active speakers, $\mathbf{H}(k)$ comprises the acoustic transfer functions, and $\mathbf{n}(l,k)$ is additive noise.

The time-invariant spatial filter is applied as:

$$
\hat{s}(l,k)=\mathbf{w}^{\mathrm{H}}(k)\mathbf{y}(l,k)
$$

where $\mathbf{w}(k)$ denotes the DNN-based beamformer weights. The target signal is defined as a linear combination of the sources of interest:

$$
s_{\mathrm{target}}(l,k)=\mathbf{g}^{\top}\mathbf{s}(l,k)
$$

where $\mathbf{g}\in\mathbb{R}^{J}$ is a weighting vector (1 for desired sources, 0 for interference).

## Methodology

### U-Net Architecture with Attention Fusion

The model employs a U-Net architecture with an attention-based fusion frontend that integrates spatial guidance (target RTF and interference subspace) with the multichannel mixture. The U-Net follows an encoder-decoder structure with skip connections and transposed-convolution decoder blocks, with attention also applied over the skip connections. The final layer applies a fully connected projection along the frequency dimension, followed by complex-valued normalization and learnable global gain scaling to produce the beamforming weights.

### RTF Estimation via Covariance Whitening

The covariance whitening (CW) method is used to estimate spatial signatures. The noise covariance matrix is estimated from noise-only frames:

$$
\hat{\mathbf{\Phi}}_{\mathbf{nn}}(k)=\frac{1}{|\mathcal{V}_{n}|}\sum_{l\in\mathcal{V}_{n}}\mathbf{y}(l,k)\mathbf{y}^{\mathrm{H}}(l,k)
$$

The whitening operation is:

$$
\mathbf{y_{w}}(l,k)=\hat{\mathbf{\Phi}}^{-1/2}_{\mathbf{nn}}(k)\,\mathbf{y}(l,k)
$$

The target RTF is obtained from the dominant eigenvector of the whitened covariance matrix of target-only frames, and the interference subspace from the dominant eigenvectors of the whitened covariance matrix of interference-only frames.

### Loss Function

The training objective combines SI-SDR maximization with constraint penalties:

$$
\begin{aligned}
\mathcal{L} =& -\mathrm{SI\text{-}SDR}(\hat{s},s_{\mathrm{target}}) \\
&+ \lambda_{\mathrm{pass}}\,\mathbb{E}_{k}\!\left[\left|\mathbf{w}^{\mathrm{H}}(k)\mathbf{a}_{\mathrm{target}}(k)-1\right|^{2}\right] \\
&+ \lambda_{\mathrm{null}}\,\mathbb{E}_{k}\!\left[10\log_{10}\!\left(\left\|\mathbf{w}^{\mathrm{H}}(k)\mathbf{A}_{\mathrm{interf}}(k)\right\|^{2}+\epsilon\right)\right]
\end{aligned}
$$

The loss jointly promotes target reconstruction, enforces a distortionless response toward the desired direction, and encourages null steering toward the interference subspace. The penalty weights $\lambda_{\mathrm{pass}}$ and $\lambda_{\mathrm{null}}$ are gradually increased during training following an augmented Lagrangian-inspired schedule.

## Experimental Setup

| Parameter | Setting |
|-----------|---------|
| **Microphone array** | 8-microphone linear array, height 1.3m, random tilt $[-45^\circ, 45^\circ]$ |
| **Room dimensions** | Width/length $[6,9]$ m, height 3m |
| **Speech data** | LibriSpeech |
| **Speakers** | $J\in\{2,3\}$ static speakers |
| **Noise** | Stationary babble noise |
| **Acoustic conditions** | Anechoic and reverberant target/interference |
| **Metrics** | SI-SDR, SNR, SIR, Power Ratio |
| **Baselines** | LCMV beamformer with estimated spatial signatures |

## Results

### Enhancement Performance

The proposed learned models achieve substantially higher SI-SDR and SNR than the LCMV baseline in both anechoic and reverberant scenarios, while maintaining competitive interference suppression. The "Estimated RTF" and "No RTF" models achieve similar enhancement metrics, suggesting the RTF guidance is primarily beneficial in fully overlapped conditions.

| Metric [dB] | Input | Est. RTF | No RTF | Oracle RTF | LCMV |
|-------------|-------|----------|--------|------------|------|
| **SI-SDR** | -4.65 | 0.63 | 0.62 | 1.04 | -1.94 |
| **SNR** | 1.46 | 5.74 | 6.16 | 6.02 | 2.96 |
| **SIR** | -3.39 | 4.90 | 5.15 | 5.49 | 6.70 |

*Three-speaker scenario (anechoic target/interference).*

### Importance of RTF Guidance

In fully overlapped scenarios where all speakers are active throughout the recording, the unguided model ("No RTF") fails to achieve meaningful enhancement (SI-SDR: -4.62 dB vs input -4.65 dB), whereas the "Oracle RTF" model maintains strong directional filtering (SI-SDR: 1.28 dB).

### Beampattern Analysis

![[raw/papers/zaidel-2026-linearly-constrained-deep-beamformer/figures/fig2-beampattern.png|Wideband beampower patterns]]

*Figure 1: Wideband beampower for the proposed learned beamformers vs LCMV. The learned models produce more directional and spatially selective responses with lower sidelobe levels.*

The learned beamformers produce more directional and spatially selective responses with lower sidelobe levels and improved background-noise suppression compared to the classical LCMV beamformer.

## Key Contributions

1. **Fully DNN-based beamformer with linear constraints**: A neural network trained to directly predict beamforming weights while satisfying explicit spatial constraints for target preservation and interference suppression.
2. **Adaptive multi-term loss**: A loss function combining SI-SDR reconstruction with distortionless-response and null-steering penalties, with progressive weight scheduling inspired by the augmented Lagrangian framework.
3. **Spatial guidance via estimated RTF and interference subspace**: Integration of covariance-whitening-based spatial estimates as network inputs, enabling the model to leverage spatial information without requiring oracle knowledge during inference.
4. **Superior performance over classical LCMV**: The learned beamformers substantially outperform the analytical LCMV beamformer in SI-SDR and SNR while maintaining competitive interference suppression.

## Related Concepts

- [[concepts/lcmv-beamformer|Linearly Constrained Minimum Variance (LCMV) Beamformer]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/relative-transfer-function|Relative Transfer Function (RTF)]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]

## Related Synthesis

- [[synthesis/computational-efficiency-evolution|Computational Efficiency in Multichannel Processing]]
