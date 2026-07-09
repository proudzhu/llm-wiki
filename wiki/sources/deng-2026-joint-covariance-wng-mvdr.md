---
type: source
created: 2026-07-09
updated: 2026-07-09
sources:
  - raw/papers/deng-2026-joint-covariance-wng-mvdr/full-text.md
  - https://doi.org/10.48550/arXiv.2606.24137
  - https://arxiv.org/abs/2606.24137
tags:
  - beamforming
  - speech-enhancement
  - mvdr
  - robust-beamforming
  - white-noise-gain
  - deep-learning
  - neural-beamforming
  - interspeech-2026
---

# Deng, Pei, Ma, Huang, Chen &amp; Benesty 2026: Joint Covariance and WNG Learning for Robust MVDR

**Authors**: [[entities/yongyi-deng|Yongyi Deng]]¹, [[entities/hanchen-pei|Hanchen Pei]]¹, [[entities/jianbo-ma|Jianbo Ma]]², [[entities/gongping-huang|Gongping Huang]]¹, [[entities/jingdong-chen|Jingdong Chen]]³, [[entities/jacob-benesty|Jacob Benesty]]⁴  
**Affiliations**: ¹ Wuhan University, ² Dolby Laboratories, ³ Northwestern Polytechnical University, ⁴ INRS-EMT, University of Quebec  
**Venue**: INTERSPEECH 2026  
**Year**: 2026  
**Type**: Conference Paper  
**DOI**: [10.48550/arXiv.2606.24137](https://doi.org/10.48550/arXiv.2606.24137)  
**arXiv**: [2606.24137](https://arxiv.org/abs/2606.24137)

## Summary

This paper proposes an end-to-end data-driven MVDR beamforming framework that jointly learns time-frequency noise masks for covariance matrix estimation and frequency-dependent White Noise Gain (WNG) thresholds for robustness control. Unlike conventional approaches that use fixed, manually tuned WNG constraints or diagonal loading factors, the dual-branch neural network adaptively predicts optimal WNG values per frequency bin while simultaneously estimating the noise covariance. A differentiable robust MVDR layer enables end-to-end optimization without explicit WNG supervision, achieving consistent improvements in speech quality and intelligibility over fixed-threshold baselines, particularly under array mismatch conditions.

## Problem Formulation

Consider an $M$-element microphone array in the STFT domain:

$$\mathbf{y}(n,k) = \mathbf{d}_{\theta_s}(k)X(n,k) + \mathbf{v}(n,k)$$

where $\mathbf{d}_{\theta_s}(k)$ is the steering vector for direction $\theta_s$, $X(n,k)$ is the target signal, and $\mathbf{v}(n,k)$ is the noise vector. The noise covariance matrix is:

$$\mathbf{\Phi}_\mathbf{v}(k) = E\left[\mathbf{v}(n,k)\mathbf{v}^H(n,k)\right] = \phi_V(k)\mathbf{\Gamma}_\mathbf{v}(k)$$

The conventional MVDR beamformer weights are:

$$\mathbf{h}_\text{MVDR}(k) = \frac{\mathbf{\Gamma}_\mathbf{v}^{-1}(k)\mathbf{d}_{\theta_s}(k)}{\mathbf{d}_{\theta_s}^H(k)\mathbf{\Gamma}_\mathbf{v}^{-1}(k)\mathbf{d}_{\theta_s}(k)}$$

subject to the distortionless constraint $\mathbf{h}^H(k)\mathbf{d}_{\theta_s}(k) = 1$.

The **White Noise Gain (WNG)** quantifies robustness to spatially white noise and array imperfections:

$$\mathcal{W}[\mathbf{h}(k)] = \frac{|\mathbf{h}^H(k)\mathbf{d}_{\theta_s}(k)|^2}{\mathbf{h}^H(k)\mathbf{h}(k)} = \frac{1}{\|\mathbf{h}(k)\|^2}$$

where the second equality holds under the distortionless constraint. Low WNG (negative on dB scale) indicates white noise amplification and high sensitivity to array mismatches.

Any distortionless beamformer can be orthogonally decomposed as:

$$\mathbf{h}(k) = \mathbf{h}_\text{D}(k) + \overline{\mathbf{U}}(k)\overline{\mathbf{h}}(k)$$

where $\mathbf{h}_\text{D}(k) = \mathbf{d}_{\theta_s}(k)/M$ is the delay-and-sum beamformer, and $\overline{\mathbf{U}}(k)$ is a semi-unitary basis for the subspace orthogonal to $\mathbf{d}_{\theta_s}(k)$. The WNG-constrained robust MVDR has closed-form solution via quadratic eigenvalue problem:

$$\mathbf{h}_\text{RMVDR} = \mathbf{h}_\text{D} - \overline{\mathbf{U}}\left(\overline{\mathbf{U}}^H\mathbf{\Gamma}_\mathbf{v}\overline{\mathbf{U}} - \lambda\mathbf{I}_{M-1}\right)^{-1}\overline{\mathbf{U}}^H\mathbf{\Gamma}_\mathbf{v}\mathbf{h}_\text{D}$$

where $\lambda$ is uniquely determined by the target WNG threshold $\mathcal{W}_0$. Constraining WNG is mathematically equivalent to [[concepts/diagonal-loading|diagonal loading]]: $\mathbf{\Gamma}_{\mathbf{v},\epsilon}(k) = \mathbf{\Gamma}_\mathbf{v}(k) + \epsilon\mathbf{I}_M$.

## Methodology

![[raw/papers/deng-2026-joint-covariance-wng-mvdr/figures/fig1.png|Figure 1: Dual-branch network architecture]]

*Figure 1: Overview of the proposed dual-branch network architecture for joint mask estimation and data-driven WNG prediction.*

### Dual-Branch Network Architecture

1. **Shared Feature Extractor**: Multi-clue fusion backbone (based on JNF/McNet architecture) with four parallel modules:
   - **Frequency module**: Captures inter-frequency correlations (Bi-LSTM, 128 hidden units)
   - **Narrowband temporal module**: Models short-term temporal dynamics (LSTM, 256 hidden units)
   - **Subband module**: Local frequency neighborhood expansion with reference channel (LSTM, 384 hidden units, $N_1=2$ adjacent bins)
   - **Fullband module**: Cross-band information for global context (LSTM, 128 hidden units, $N_2=5$ contextual frames)
   
   Each module uses RNN-FC architecture (LSTM/Bi-LSTM + FC + ReLU). Multi-scale features are fused and shared between output branches.

2. **WNG Prediction Branch**: Lightweight linear layer predicts **frequency-dependent WNG threshold** $\mathcal{W}_0(k)$ for each frequency bin, enabling frequency-adaptive robustness control.

3. **Complex Mask Branch**: MLP predicts real and imaginary components of complex-valued T-F mask for noise estimation. The estimated noise is:
   $$\widehat{\mathbf{v}}(k,l) = \mathbf{y}(k,l) \odot \widehat{M}(k,l)$$
   where $\widehat{M}(k,l)$ is the estimated complex mask. The noise covariance is computed via time averaging:
   $$\widehat{\mathbf{\Phi}}_\mathbf{v}(k) = \frac{1}{L}\sum_l \widehat{\mathbf{v}}(k,l)\widehat{\mathbf{v}}^H(k,l)$$

### Differentiable Robust MVDR Layer

The closed-form robust MVDR solution is embedded as a differentiable layer, enabling end-to-end backpropagation through the beamforming operation. Training uses **mean absolute error (MAE)** loss against an early-reference beamformed signal:

$$\mathcal{L}_\text{total} = \frac{1}{N}\sum_{i=1}^N \left|y_\text{early}^{(i)} - y_\text{filtered}^{(i)}\right|_1$$

No explicit WNG supervision is required — the network implicitly learns physically meaningful WNG values through the reconstruction loss, which naturally balances robustness against directivity:
- Excessively large WNG → excessive diagonal loading → reduced directivity and interference suppression
- Excessively small WNG → white noise amplification and sensitivity to array mismatches

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Dataset** | VCTK (16 kHz, 3s segments) |
| **Array** | 8-microphone ULA, 2 cm spacing (seen condition) |
| **Unseen arrays** | 1 cm and 3 cm spacing (mismatch evaluation) |
| **Room dimensions** | Random 5–10 m × 4–8 m × 2.5–4 m |
| **Reverberation ($T_{60}$)** | Uniform 0.1–0.4 s |
| **Interferers** | 1–4 sources, azimuth 90°–270° |
| **SIR** | 0–10 dB |
| **Diffuse noise SNR** | 0–10 dB |
| **White noise SNR** | 10–40 dB |
| **STFT** | 16 ms frame, 50% overlap, 256-point FFT |
| **Optimizer** | Adam, batch size 4, initial LR $10^{-4}$ |
| **LR schedule** | Halved when validation loss plateaus for 5 epochs |
| **Baselines** | FullSubNet mask estimator + fixed WNG (-6 dB optimal); fixed diagonal loading |
| **Metrics** | SNR gain, SDR, STOI, PESQ |

Array mismatch simulation: nominal spacing $\delta = d + \epsilon$, where $\epsilon \sim \mathcal{N}(0, 0.1^2 \text{ cm}^2)$.

## Results

![[raw/papers/deng-2026-joint-covariance-wng-mvdr/figures/fig2.png|Figure 2: Objective metric comparison]]

*Figure 2: Comparison of objective metrics: (a) SNR, (b) STOI, (c) SDR, and (d) PESQ. Violin plots show utterance-level score distributions for input signal, FullSubNet with optimal fixed WNG (-6 dB), and proposed methods with optimal fixed WNG (-8 dB) and adaptive WNG.*

### Quantitative Results (Table 1)

| Configuration | SNR gain (dB) | ΔSDR (dB) |
|---------------|--------------|-----------|
| **Seen array** (δ = 2.0 ± ε cm) | | |
| Proposed MVDR (adaptive WNG) | **11.94** | **11.47** |
| Conventional MVDR (optimal ε) | 10.12 | 9.28 |
| Conventional MVDR (optimal $\mathcal{W}_0$) | 10.54 | 9.51 |
| **Unseen array** (δ = 1.0 ± ε cm) | | |
| Proposed MVDR (adaptive WNG) | **10.23** | **9.93** |
| Conventional MVDR (optimal ε) | 8.88 | 8.70 |
| Conventional MVDR (optimal $\mathcal{W}_0$) | 8.68 | 8.48 |
| **Unseen array** (δ = 3.0 ± ε cm) | | |
| Proposed MVDR (adaptive WNG) | **11.59** | **10.85** |
| Conventional MVDR (optimal ε) | 9.89 | 8.65 |
| Conventional MVDR (optimal $\mathcal{W}_0$) | 9.95 | 8.79 |

### Key Findings

1. **Adaptive WNG outperforms fixed thresholds** across all array conditions, achieving +1.4–1.8 dB SNR gain and +1.9–2.2 dB SDR improvement over optimal fixed baselines.

2. **Robustness to array mismatch**: The adaptive strategy generalizes well to unseen microphone spacings (1 cm and 3 cm), maintaining performance while fixed-threshold methods degrade significantly.

3. **End-to-end optimization works** without explicit WNG labels — the reconstruction loss naturally guides the network toward appropriate frequency-dependent robustness levels.

4. The optimal fixed WNG differs between methods (-6 dB for FullSubNet baseline vs -8 dB for the proposed mask estimator), confirming that WNG tuning is mask-dependent and motivates joint learning.

## Key Contributions

1. **Data-driven WNG control**: First framework to treat WNG threshold as a learnable, frequency-dependent parameter predicted by a neural network rather than a fixed hyperparameter.

2. **Dual-branch joint learning**: Simultaneous estimation of T-F masks for covariance computation and frequency-dependent WNG constraints in a unified architecture.

3. **Differentiable robust MVDR layer**: Closed-form WNG-constrained MVDR solution integrated as a differentiable layer for end-to-end training without explicit WNG supervision.

4. **Consistent improvements**: Demonstrated 1–2 dB gains across SNR, SDR, STOI, and PESQ metrics under both matched and mismatched array conditions relative to optimally tuned fixed-WNG baselines.

## Related Concepts

- [[concepts/beamforming|Beamforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/robust-minimum-variance-beamforming|Robust Minimum Variance Beamforming]]
- [[concepts/white-noise-gain|White Noise Gain (WNG)]]
- [[concepts/diagonal-loading|Diagonal Loading]]
- [[concepts/neural-beamforming|Neural Beamforming]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/kantorovich-inequality|Kantorovich Inequality]]
- [[concepts/condition-number|Condition Number]]

## Related Synthesis

None yet.
