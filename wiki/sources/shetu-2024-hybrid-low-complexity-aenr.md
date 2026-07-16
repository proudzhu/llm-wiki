---
type: source
created: 2026-07-16
updated: 2026-07-16
sources:
  - raw/papers/shetu-2024-hybrid-low-complexity-aenr/full-text.md
  - https://doi.org/10.1109/IWAENC61483.2024.10694288
  - zotero://select/items/0_XIPNNJIZ
tags:
  - acoustic-echo-reduction
  - noise-reduction
  - low-complexity
  - hybrid-system
  - deep-learning
  - speech-enhancement
---

# Shetu, Desiraju, Martinez, Habets & Mabande 2024: A Hybrid Approach for Low-Complexity Joint Acoustic Echo and Noise Reduction

**Authors**: [[entities/shrishti-saha-shetu|Shrishti Saha Shetu]], [[entities/naveen-kumar-desiraju|Naveen Kumar Desiraju]], [[entities/jose-miguel-martinez-aponte|Jose Miguel Martinez Aponte]], [[entities/emanuel-habets|Emanuel A. P. Habets]], [[entities/edwin-mabande|Edwin Mabande]]

**Affiliation**: Fraunhofer IIS, Erlangen, Germany

**Venue**: IWAENC 2024 (International Workshop on Acoustic Signal Enhancement)

**Year**: 2024 | **Type**: Conference Paper | **DOI**: [10.1109/IWAENC61483.2024.10694288](https://doi.org/10.1109/IWAENC61483.2024.10694288)

**Zotero**: [XIPNNJIZ](zotero://select/items/0_XIPNNJIZ)

## Summary

This paper proposes a low-complexity hybrid approach for joint acoustic echo and noise reduction (AENR) by integrating the ULCNet model — originally designed for ultra-low complexity noise suppression — into a hybrid system with a Kalman filter (KF) for echo estimation. The modified ULCNet takes three inputs (error signal, echo estimate, far-end signal) and achieves better echo reduction and comparable noise reduction performance than SOTA methods at a fraction of the computational cost (0.69M params, 0.10 GMACs), at the cost of slight speech quality degradation in double-talk scenarios.

## Problem Formulation

The microphone signal in a communication scenario is modeled as:

$$x(n) = s(n) + e(n) + v(n) \tag{1}$$

where $s$ is near-end speech, $e$ is acoustic echo, and $v$ is background noise.

The KF generates an echo estimate $\hat{e}(n)$, and the error signal is:

$$z(n) = x(n) - \hat{e}(n) = s(n) + r(n) + v(n) \tag{2}$$

where $r(n) = e(n) - \hat{e}(n)$ is the residual echo (composed of early residual echo from filter misalignment, late residual echo from reverberation, and nonlinear echo components).

## Methodology

### System Architecture

The proposed system is a two-stage hybrid approach:

1. **Stage 1 (KF)**: A diagonalized partitioned-block-frequency-domain adaptive Kalman filter generates the echo estimate $\hat{e}(n)$ and error signal $z(n)$
2. **Stage 2 (DNN Post-filter)**: A modified ULCNet jointly suppresses residual echo and noise in the STFT domain

![[raw/papers/shetu-2024-hybrid-low-complexity-aenr/figures/950e96f371d1a03764660d3ed4038a48a2b69380fa8e773089968befe4259f01.jpg|Figure 1: Flow-diagram of proposed method]]
*Figure 1: Flow-diagram of the proposed hybrid AENR system.*

### Three Key Modifications to ULCNet

1. **Multi-input architecture**: Takes three STFT-domain inputs $\{Z, \hat{E}, Y\}$ (error signal, echo estimate, far-end signal) instead of the single microphone input $\{X\}$ in the original ULCNet. Power-law compression with factor $\alpha$ is applied to all three.

2. **Modified channel-wise feature reorientation**: Sub-band features from the three inputs are interleaved: $[\tilde{Z}_{m,0}, \tilde{E}_{m,0}, \tilde{Y}_{m,0}, \ldots, \tilde{Z}_{m,B-1}, \tilde{E}_{m,B-1}, \tilde{Y}_{m,B-1}]$, then stacked.

![[raw/papers/shetu-2024-hybrid-low-complexity-aenr/figures/5bb4672447dea844534b764a4959183f08932411168ab94ef9ed353c3b0dafd1.jpg|Figure 2: Modified channel-wise feature reorientation]]
*Figure 2: Modified channel-wise feature reorientation and stacking for multiple inputs.*

3. **Phase input change**: The Intermediate Feature Computation block uses the phase of the error signal $\tilde{Z}_p$ (instead of the microphone signal phase $\tilde{X}_p$). The compressed near-end speech estimate is computed via complex ratio mask multiplication:

$$\tilde{S}(\ell, k) = \tilde{Z}_m(\ell, k) \cdot M_m(\ell, k) \cdot e^{(\tilde{Z}_p(\ell, k) + M_p(\ell, k))} \tag{3}$$

where $M_m$ and $M_p$ are the magnitude and phase components of the complex-valued mask $M$.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Training data | 1100 hours each for AER and AENR tasks |
| Sampling rate | 16 kHz |
| FFT order | $N_{\text{FFT}} = 512$, $K = 257$ frequency bins |
| Sub-band length | $K_B = 48$, overlap $\beta = 0.33$, $B = 8$ sub-bands |
| Compression factor | $\alpha = 0.3$ |
| Optimizer | Adam, initial LR = 0.004, decay by 10× on plateau |
| Batch size | 64, sample duration 3s, 20k steps/epoch |
| KF partitions | 10 |
| KF Kalman gain | 0.8 |
| Loss function | Frequency-domain MSE |
| SER range | [-20, 20] dB |
| SNR range | [-5, 30] dB |

| Evaluation Dataset | Task |
|--------------------|------|
| Interspeech 2021 AEC Challenge blind test set | AER |
| ICASSP 2023 AEC Challenge blind test set | AER |
| DNS Challenge 2020 synthetic non-reverb test set | NR |

## Results

### AER Performance (AECMOS)

| Method | Params [M] | GMACs | DT EMOS (IS21) | DT DMOS (IS21) | FST EMOS (IC23) | FST DMOS (IC23) |
|--------|-----------|-------|-----------------|-----------------|------------------|------------------|
| Peng et al. | 10.20 | 2.52 | 4.36 | 4.23 | — | — |
| Deep-VQE | 7.50 | 4.02 | — | — | 4.70 | 4.29 |
| Align-CRUSE | 0.74 | — | 4.45 | 4.07 | 4.60 | 3.95 |
| **Proposed ULCNet_AENR** | **0.69** | **0.10** | **4.61** | 3.79 | **4.54** | 3.58 |

- ULCNet_AENR achieves **best EMOS** in DT (Interspeech 2021) and FST (ICASSP 2023) scenarios
- Up to **10× smaller** and **4× cheaper** than SOTA methods
- DMOS in DT scenarios is lower due to aggressive suppression and modified power-law compression

### NR Performance (DNSMOS)

| Method | Params [M] | GMACs | PESQ | SI-SDR | SIGMOS | BAKMOS |
|--------|-----------|-------|------|--------|--------|--------|
| DeepFilterNet2 | 2.31 | 0.36 | 2.65 | 16.60 | 3.51 | 4.12 |
| ULCNet_MS | 0.68 | 0.09 | 2.64 | 16.34 | 3.46 | 4.06 |
| ULCNet_AER + ULCNet_Freq | 1.38 | 0.20 | 2.23 | 16.56 | 3.34 | 4.08 |
| **Proposed ULCNet_AENR** | **0.69** | **0.10** | 2.11 | 15.58 | 3.30 | 4.05 |

- NR metrics lag behind dedicated NR models, but informal listening tests show comparable perceptual quality
- ULCNet_AENR is a single model for joint AENR vs. the two-stage approach requiring double the cost

### Key Finding

The proposed method runs with a **real-time factor of 13.1%** on a Cortex-A53 1.43 GHz processor, making it suitable for embedded deployment.

## Key Contributions

1. **Hybrid AENR system**: Integrates a Kalman filter with a modified ULCNet post-filter for joint echo and noise reduction
2. **Multi-input ULCNet**: Extends single-input ULCNet to handle three inputs (error signal, echo estimate, far-end signal) via modified channel-wise feature reorientation with interleaved sub-band stacking
3. **Ultra-low complexity**: Achieves 0.69M parameters and 0.10 GMACs — up to 10× smaller and 4× cheaper than SOTA while achieving comparable or better echo reduction
4. **Single-model joint AENR**: Outperforms a two-stage dedicated AER+NR approach at half the computational cost
5. **No time-alignment required**: Unlike most SOTA approaches, no DNN-based time-alignment is needed for the far-end signal

## Related Concepts

- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation (AEC)]]
- [[concepts/ulcnet|ULCNet]]
- [[concepts/kalman-filter|Kalman Filter]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cRM)]]
- [[concepts/power-law-compression|Power-Law Compression]]
- [[concepts/channel-wise-feature-reorientation|Channel-Wise Feature Reorientation]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]

## Related Synthesis

*(None yet)*
