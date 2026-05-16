---
type: source
created: 2026-05-16
updated: 2026-05-16
sources:
  - raw/papers/liu-2025-robust-fusion-bc-ac-attention/full-text.md
  - https://doi.org/10.1109/ICASSP49660.2025.10888094
  - zotero://select/items/0_II6NMWAX
tags:
  - speech-enhancement
  - bone-conduction
  - multi-modal-fusion
  - attention-mechanism
  - sensor-failure-robustness
  - icassp-2025
---

# Liu, Chen & Yin 2025: Robust Fusion of Bone and Air-Conducted Sensors with Adaptive Temporal-Frequency Attention

- **Authors**: [[../entities/zhenglong-liu|Zhenglong Liu]], [[../entities/zhe-chen|Zhe Chen]] (corresponding), [[../entities/fuliang-yin|Fuliang Yin]]
- **Affiliation**: School of Information and Communication Engineering, Dalian University of Technology, China
- **Venue**: ICASSP 2025 — IEEE International Conference on Acoustics, Speech and Signal Processing, pp. 1–5
- **Year**: 2025
- **Type**: Conference Paper
- **DOI**: [10.1109/ICASSP49660.2025.10888094](https://doi.org/10.1109/ICASSP49660.2025.10888094)
- **Zotero**: [Open in Zotero](zotero://select/items/0_II6NMWAX)

## Summary

This paper proposes a complex-domain deep learning method that fuses bone-conducted (BC) and air-conducted (AC) microphone signals for speech enhancement. The architecture combines a shared-convolution **pre-fusion module**, a Dense-Net based encoder, three cascaded **Adaptive Temporal-Frequency Attention (ATFA)** modules with multi-head self-attention along both time and frequency axes, an Adaptive Hierarchical Attention (AHA) module that fuses multi-level features, and four decoders generating real masks that are applied to the original BC and AC complex spectrums and then summed. A **dual-channel mask** strategy is introduced for the first time in BC/AC fusion problems. Crucially, the authors propose a **special training (ST)** strategy that randomly disables one input channel (probability 0.2) during training, dramatically improving robustness when one sensor fails — a common failure mode of wearable BC sensors due to wearing position or body movement. With only 1.6M parameters (vs. 31.4M for the AFF baseline), the method achieves average PESQ/STOI gains of +0.2/+0.03 over the strongest baseline, and recovers PESQ from 1.45→3.39 (BC failure) and from 1.18→2.54 (AC failure) where existing methods catastrophically degrade.

## Problem Formulation

The signal model assumes complementary noise sensitivity:

- **AC microphone**: Receives clean speech with low distortion but is vulnerable to ambient noise.
- **BC microphone**: Receives speech with significant distortion (especially loss of high-frequency components > 2 kHz) but is insensitive to airborne noise.

The model takes the complex STFT spectra of both signals, generates two real masks $M_{AC}$ and $M_{BC}$, and produces:

$$
X_{\text{enhanced}} = M_{AC} \otimes X_{AC} + M_{BC} \otimes X_{BC}
$$

where $\otimes$ denotes element-wise multiplication. The final time-domain signal is reconstructed via iSTFT.

## Methodology

![Proposed architecture overview](../raw/papers/liu-2025-robust-fusion-bc-ac-attention/figures/b2b952e80b62ac570e5c8a756a61c07d43f8ef549674cd0874800236d94a9994.jpg)

*Figure 1: Overall fusion architecture — pre-fusion → DenseNet encoder → three cascaded ATFA modules → AHA → four decoders producing dual-channel masks.*

### A. Pre-Fusion via Shared Convolution

The pre-fusion module exploits the observation that BC and AC spectra share **similar local patterns at the same time-frequency positions** despite their differences. A **shared 2D convolution kernel** extracts common patterns from both modalities (parameter sharing across modalities, contrasting with the per-channel pattern extraction inside standard convolutions). Two shared convolutional layers with LN+PReLU are used; the final fused output takes the **max** between the two transformed streams (inspired by max-pooling).

The pre-fused signal $X_{\text{fused}}$ is concatenated with the original $X_{AC}$ and $X_{BC}$ in the channel axis (3-channel input to the encoder), increasing the input feature richness in a multi-view learning sense.

### B. Densely Convolutional Encoder & Decoder

The encoder uses a **dilated DenseNet** with 4 convolutional layers (kernel (2,3) in (T, F'), dilation rates {1, 2, 4, 8}) followed by two convolutional layers — kernels (1,1) and (1,3), strides (1,1) and (1,2) — that halve the frequency dimension and lift the channel count to 64.

Four parallel decoders (one per output mask channel) consist of a dilated DenseNet and a transposed 2D convolution that restores the (T, F') resolution.

### C. Adaptive Temporal-Frequency Attention (ATFA)

![ATFA module](../raw/papers/liu-2025-robust-fusion-bc-ac-attention/figures/57540c10e6535b71c541c626aed7059d67caacc1b5c617df8fb69bdd95ffd46e.jpg)

*Figure 2: ATFA — two parallel branches apply MHSA along the temporal and frequency axes, then GRU-based feed-forward, residual connections, and learnable weighting α/β.*

Each ATFA module has two parallel branches operating along **time** and **frequency** axes:

- A feature tensor $B \times T \times F' \times C$ is reshaped to $(BT) \times F' \times C$ for the frequency-axis branch and $(BF') \times T \times C$ for the temporal-axis branch.
- Each branch applies **Multi-Head Self-Attention (MHSA)** + LN, followed by a **Bi-GRU based feed-forward network** with PReLU, Linear, and residual connections.
- Branch outputs are combined with the input via summation with **learnable weights α (frequency) and β (temporal)**.

Three ATFA modules are cascaded.

### D. Adaptive Hierarchical Attention (AHA)

The outputs of the three ATFA stages are integrated by AHA: each stage output is average-pooled, then a 1×1 conv projects each to dimension $(B,1,1,1)$. The three scalars are concatenated → softmax → used as weights to sum the original three multi-level features. The fused result is multiplied by a learnable scalar γ and added to the last ATFA output.

This provides a multi-scale fusion that adaptively emphasizes the most informative attention stage per sample.

### E. Dual-Channel Mask Strategy

Inspired by adaptive filtering and beamforming intuition (MVDR, MPDR), the network outputs **four real masks** — real and imaginary masks for AC, real and imaginary masks for BC — that are multiplied with the original two complex spectra and summed. This is analogous to a learned time-varying complex filter applied to each channel followed by summation. The authors select **real masks** (over complex masks like DCCRN's) to balance performance against computation.

### F. Loss Function

A combined RI + magnitude loss (clean target $S$, estimate $\hat{S}$):

$$
L_{\text{RI}} = \frac{1}{TF} \sum_{t,f} \left( |\hat{S}_r[t,f] - S_r[t,f]| + |\hat{S}_i[t,f] - S_i[t,f]| \right)
$$
$$
L_{\text{Mag}} = \frac{1}{TF} \sum_{t,f} \left| |\hat{S}[t,f]| - |S[t,f]| \right|
$$
$$
\text{Loss} = L_{\text{RI}} + L_{\text{Mag}}
$$

The magnitude term emphasizes that magnitude matters more than phase in denoising perception.

### G. Special Training (ST) for Sensor-Failure Robustness

To address the practical problem that BC sensors may become invalid intermittently (loose contact, body movement), the authors propose a training strategy: **with probability 0.2 each, replace either the AC or BC channel with low-amplitude white noise** during training. This teaches the network to gracefully degrade when one channel is missing.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Dataset** | Elevoc Simultaneously-recorded Microphone/Bone-sensor (ESMB) corpus — 128 h speech, 287 speakers (131 M / 156 F) |
| **Hardware** | Elevoc Clear earbuds with ST25ba BC sensor + close-talk AC mic |
| **Sampling rate** | 8 kHz (downsampled) |
| **Test split** | 1 h × 4 speakers (2 M / 2 F) for testing; rest for training |
| **Training noise** | DNS Challenge noise dataset, SNR ∈ {−5, −4, −3, −2, −1, 0} dB |
| **Test noise** | NOISEX-92, SNR ∈ {−5, 0, 5, 10, 15} dB |
| **Window** | 32 ms Hanning, 50% overlap |
| **STFT** | 256-point → 129-dim spectral features |
| **Optimizer** | Adam, batch 6, 32 epochs, lr 1e-3 (halved on 4-epoch validation plateau) |
| **Sensor-failure prob.** | p = 0.2 each channel (ST variant) |
| **Metrics** | wb-PESQ, STOI |
| **Parameters** | 1.6 M |
| **Compute** | 7.3 GFLOPs / 1 s of speech |

Baselines: FCN-Fusion (Yu 2020), Aff-Fusion (Wang 2022), MMINet (Wang/Rahardja 2022), and a **Proposed AC En** ablation (proposed model with pre-fusion removed and a single-channel input — i.e., AC-only enhancement using the same backbone).

## Results

### Main Comparison (Fig. 5)

| SNR (dB) | Noisy AC | FCN | MMINet | Aff Fusion | Prop. AC En | **Proposed Fusion** |
|---:|---:|---:|---:|---:|---:|---:|
| −5 | 1.6 | 1.9 | 2.1 | 3.0 | 2.6 | **3.3** |
| 0  | 1.8 | 2.2 | 2.3 | 3.3 | 3.0 | **3.5** |
| 5  | 2.1 | 2.4 | 2.5 | 3.5 | 3.4 | **3.7** |
| 10 | 2.4 | 2.6 | 2.7 | 3.6 | 3.7 | **3.9** |
| 15 | 2.7 | 2.7 | 3.0 | 3.8 | 3.9 | **4.0** |

PESQ values; STOI follows the same trend (proposed reaches 0.82–0.95 across SNRs). Proposed Fusion is +0.2 PESQ / +0.03 STOI over Aff-Fusion on average, while having ~20× fewer parameters (1.6 M vs. 31.4 M).

### Sensor-Failure Robustness (Table I, AC under 5 dB)

| Method | Invalid BC: PESQ / STOI | Invalid AC: PESQ / STOI |
|---|---|---|
| Noisy AC | 2.16 / 0.69 | — |
| Noisy BC | — | 1.24 / 0.52 |
| FCN Fusion | 2.13 / 0.64 | 1.45 / 0.43 |
| MMINet | 1.88 / 0.63 | 1.18 / 0.46 |
| Aff Fusion | 1.98 / 0.63 | 1.22 / 0.42 |
| Proposed Fusion | 2.62 / 0.79 | 1.53 / 0.38 |
| **ST Proposed Fusion** | **3.39 / 0.84** | **2.54 / 0.73** |

**Key finding**: Existing fusion methods *worsen* the signal when one sensor is invalid (output PESQ < input PESQ). The proposed method already shows mild robustness without ST training, and ST training brings dramatic recovery — particularly for AC failure (1.18 → 2.54 PESQ, more than doubling).

### Ablation (5 dB SNR)

| Variant | PESQ | STOI |
|---|---:|---:|
| Proposed Fusion | 3.70 | 0.87 |
| (i) No Pre-fusion | 3.67 | 0.86 |
| (ii) No Mask, No Pre-fusion | 3.63 | 0.84 |
| (iii) ATFA → LSTM | 3.21 | 0.81 |

The dominant contribution is the ATFA self-attention block (replacing it with LSTM costs 0.49 PESQ). Pre-fusion and dual-mask each give modest gains. The dual-channel mask was further validated on a separate DCCRN backbone, yielding +0.2 PESQ / +0.02 STOI — showing the strategy generalizes beyond the proposed architecture.

## Key Contributions

1. **Adaptive Temporal-Frequency Attention (ATFA) for BC/AC fusion**: First adaptation of dual-axis MHSA (time + frequency) with adaptive hierarchical multi-stage fusion to the BC/AC speech enhancement problem.
2. **Shared-convolution pre-fusion module**: A shared kernel + max aggregation pre-extracts common spectral patterns across modalities before the encoder, complementing standard channel-concatenation fusion.
3. **Dual-channel mask strategy**: Generating four real masks (RI for both BC and AC) and summing the masked complex spectra — a beamforming-inspired learnable filter operation new to BC/AC fusion. Validated to also improve a DCCRN backbone, suggesting general applicability.
4. **Special Training (ST) for sensor-failure robustness**: Randomly disabling one input channel (p = 0.2 each) during training transforms the model into a graceful-degradation system — a practically important property not previously explored in BC/AC fusion literature. Recovers PESQ from 1.18 → 2.54 when the AC sensor fails.
5. **Parameter efficiency**: 1.6 M parameters (≈ 5% of Aff-Fusion's 31.4 M) while achieving better PESQ/STOI on every SNR.
6. **Empirical observation of architectural inductive bias for robustness**: The proposed model already shows better invalid-channel behavior than baselines *without* ST training, suggesting that multi-axis attention + dual-mask provide architectural robustness beyond what the training scheme alone gives.

## Related Concepts

- [[../concepts/adaptive-time-frequency-attention|Adaptive Temporal-Frequency Attention (ATFA)]]
- [[../concepts/sensor-failure-robust-fusion|Sensor-Failure Robust Multi-Modal Fusion]]
- [[../concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]]
- [[../concepts/bone-conduction|Bone Conduction]]
- [[../concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[../concepts/complex-ratio-mask|Complex Ratio Mask]]
- [[../concepts/iterative-attentional-feature-fusion|Iterative Attentional Feature Fusion (iAFF)]]
- [[../concepts/mvdr-beamformer|MVDR Beamformer]]
- [[../concepts/mpdr-beamformer|MPDR Beamformer]]
- [[../concepts/dprnn|Dual-Path RNN (DPRNN)]]

## Related Sources

- [[../sources/kuang-2024-lightweight-speech-enhancement-bone-air|Kuang, Yang & Yang 2024: Lightweight BC/AC Speech Enhancement]]
- [[../sources/he-2025-vibomni|He et al. 2025: VibOmni — IMU-based BC speech enhancement]]
- [[../sources/heitkaemper-2026-bcs-speech-enhancement-earbuds|Heitkaemper et al. 2026: BCS-Guided Speech Enhancement for Earbuds]]
- [[../sources/zhang-2022-bone-conducted-speech-dissertation|Zhang 2022: Bone-Conducted Speech Dissertation]]

## Related Synthesis

- [[../synthesis/multimodal-bc-speech-enhancement|Multimodal Smart Hearables: BC-Aided Speech Enhancement]]
- [[../synthesis/multi-modal-speech-enhancement|Multi-Modal Speech Enhancement]]
