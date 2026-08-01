---
type: source
created: 2026-08-01
updated: 2026-08-01
sources:
  - raw/papers/liu-2021-igcrn/full-text.md
  - https://doi.org/10.48550/arXiv.2107.11968
  - zotero://select/items/0_PR35K3UL
tags:
  - speech-enhancement
  - dual-channel
  - microphone-array
  - convolutional-recurrent-network
  - inplace-model
  - beamforming
  - complex-spectrum-mapping
  - interspeech-2021
---

# Liu & Zhang 2021: IGCRN — Inplace Gated Convolutional Recurrent Neural Network

**Authors**: [[entities/jinjiang-liu|Jinjiang Liu]], [[entities/xueliang-zhang|Xueliang Zhang]]
**Affiliation**: College of Computer Science, Inner Mongolia University, China
**Venue**: Interspeech 2021 (arXiv preprint 2107.11968, 2021-07-26)
**Year**: 2021
**Type**: Conference paper
**DOI**: [10.48550/arXiv.2107.11968](https://doi.org/10.48550/arXiv.2107.11968)
**Zotero**: [PR35K3UL](zotero://select/items/0_PR35K3UL)

## Summary

The paper proposes **IGCRN** (Inplace Gated Convolutional Recurrent Neural Network), a compact end-to-end model for dual-channel speech enhancement that mirrors the three-stage pipeline of traditional array signal processing (DOA estimation, beamforming, post-filtering) inside a single [[concepts/convolutional-recurrent-network|CRN]]-style network. The key idea is the **inplace** design: convolutional kernels use stride 1 on the frequency dimension, so each frequency bin is processed independently throughout the encoder and decoder — preserving per-bin spatial cues that downsampling convolutions would alias away. A single **channel-wise LSTM** is reused across all frequency bins (analogous to applying one beamformer per bin with shared weights), making the model extremely compact (1.4 M parameters, 19.9 G MACs). The paper also introduces a **mask + mapping + phase** training target that combines the complementary strengths of mask-based and mapping-based amplitude prediction. On simulated dual-channel mixtures (AISHELL-1 + NOISEX-92 at -3/0/3 dB SNR), IGCRN dramatically outperforms MVDR (given true DOA) and conventional GCRN, with average STOI/PESQ gains over 30 % / 2.0 vs. noisy speech. IGCRN is the predecessor of [[sources/liu-2023-iccrn|ICCRN]] and the foundation of the inplace-CRN model family.

## Problem Formulation

For a dual-channel microphone array, the received signal is modeled as

$$x_m(k) = s(k) * h_{s,m}(k) + n(k) * h_{n,m}(k)\tag{1}$$

where $m$ is the channel index, $s(k)$ and $n(k)$ are clean speech and noise, and $h_{s,m}, h_{n,m}$ are the acoustic impulse responses from speech and noise sources to the $m$-th microphone.

The authors argue that an end-to-end network should respect the **manifold space** of the multi-channel enhancement task: traditional beamforming is processed per frequency bin (a spatial filter applied to the channel dimension), so a neural architecture that aliases spatial cues with spectral patterns — as the standard CRN's frequency-downsampling convolutions do — works against this structure. IGCRN is designed to preserve that structure.

## Methodology

### Three-Stage Beamforming-Inspired Pipeline

![[raw/papers/liu-2021-igcrn/figures/f361084e4785c364f3d173182ca1574c54585b84c6fae30e595baa55115220c3.jpg|IGCRN end-to-end pipeline]]
*Figure 1: IGCRN end-to-end pipeline, compared with the traditional beamforming pipeline (DOA estimation → beamforming → post-filtering).*

IGCRN mirrors the three classical stages of beamforming inside a single [[concepts/convolutional-recurrent-network|CRN]]-style network:

| Traditional beamforming stage | IGCRN component |
|-------------------------------|------------------|
| DOA estimation / spatial cue extraction | Inplace encoder (6× inplace GLU) |
| Beamforming per frequency bin | Channel-wise LSTM (reused across bins) |
| Post-filtering / spectral reconstruction | Inplace decoder (6× inplace transpose GLU) |

The authors emphasize that, because the network is end-to-end, the three stages do **not** exactly correspond to the traditional pipeline — the network learns the appropriate intermediate representations rather than relying on hand-crafted interfaces.

### Inplace Convolution

The core architectural choice is **[[concepts/inplace-convolution|inplace convolution]]**: a convolution whose kernel stride on the frequency dimension is set to 1, so the frequency dimension is never downsampled. The encoder and decoder therefore keep the frequency axis at its original resolution throughout.

The motivation is that wideband beamforming operates per frequency bin independently — mixing spatial cues across bins (which the standard CRN's frequency-downsampling convolutions do) obscures the per-bin spatial information that the recurrent layer needs in order to act like a beamformer.

### Channel-wise LSTM with Model Reuse

A conventional CRN applies a single LSTM over the entire flattened feature (frequency × channel). IGCRN instead applies a **channel-wise LSTM** per frequency bin: the frequency dimension is folded into the batch dimension, so the LSTM only sees the channel (= multi-microphone spatial) feature at each time step.

Because the per-bin time delay for a given look direction is identical across frequencies (only the phase compensation differs, and the LSTM does not need phase compensation — it analyzes spatial cues via time delay directly), **one LSTM is reused for all frequency bins**. This *model reuse mechanism* makes the network extremely compact: the LSTM hidden size is 64 instead of the conventional 1024, while still covering all 256 frequency bins.

### Amplitude and Phase Prediction (Mask + Mapping + Phase)

IGCRN has two decoders:

- **Amplitude decoder** with two output heads: an amplitude mask $A_{msk}$ and an amplitude mapping $A_{map}$. The estimated amplitude combines them, taking the noisy amplitude $A_{nsy}$ as a residual carrier:

  $$A_{est} = A_{msk} \otimes A_{nsy} + A_{map}\tag{4}$$

- **Phase decoder** predicting real and imaginary parts, normalized to unit magnitude:

  $$P_{est} = \frac{P_{est_r} + j P_{est_i}}{\sqrt{P_{est_r}^2 + P_{est_i}^2}}\tag{5}$$

The final estimated complex spectrum is $X_{est} = A_{est} \otimes P_{est}$. This **mask + mapping + phase** target is one of the paper's contributions: masking works well at high SNR (it directly reuses input features), mapping works better at low SNR, and combining them is complementary. This generalizes the mask + phase target of Yin et al. (Phasen) and the mask + mapping ensemble of Zhang et al. (2017) into a single decoder.

### GLU Formulation

The inplace GLU (encoder) and inplace transpose GLU (decoder) are defined as

$$Y = ELU(BN(iConv(X) \otimes Sigmoid(iConv(X))))\tag{2}$$

$$Y = ELU(BN(iTConv(X) \otimes Sigmoid(iTConv(X))))\tag{3}$$

where $iConv$ and $iTConv$ are stride-1 inplace (transpose) convolutions. The decoder uses skip connections (concatenate output of $i$-th transpose GLU with input of $(i-1)$-th).

### Loss Function (Phasen Loss)

Training uses the Phasen loss (Yin et al. 2020), a compressed-amplitude RI loss that operates on the cube-root-compressed amplitude and the corresponding real/imaginary phase components:

$$\mathcal{L} = \frac{1}{F} \sum_{i=1}^{F} \big( (A_s[i])^{\frac{1}{3}} - (A_{est}[i])^{\frac{1}{3}} \big)^2 + \frac{1}{F} \sum_{i=1}^{F} \big( (A_s[i])^{\frac{1}{3}} \otimes P_{s_r}[i] - (A_{est}[i])^{\frac{1}{3}} \otimes P_{est_r}[i] \big)^2 + \frac{1}{F} \sum_{i=1}^{F} \big( (A_s[i])^{\frac{1}{3}} \otimes P_{s_i}[i] - (A_{est}[i])^{\frac{1}{3}} \otimes P_{est_i}[i] \big)^2\tag{7}$$

where $A_s, P_{s_r}, P_{s_i}$ are the clean amplitude and real/imaginary phase, and $F$ is the number of frequency bins.

### Full Architecture

![[raw/papers/liu-2021-igcrn/figures/eb310a979fe02b2cfeb0651b57a4923a89bccc13d26f03875558cfbf9d8e361e.jpg|IGCRN architecture and room simulation setup]]
*Figure 2: The proposed dual-channel speech enhancement system and the room simulation setup.*

| Layer | Input shape | Hyperparameters | Output shape |
|-------|-------------|-----------------|--------------|
| iGLU1 | $[B, 2, 256, T]$ | 5×1, stride (1,1), 64 | $[B, 64, 256, T]$ |
| iGLU2 ~ 6 | $[B, 64, 256, T]$ | 5×1, stride (1,1), 64 | $[B, 64, 256, T]$ |
| reshape | $[B, 64, 256, T]$ | — | $[B \cdot 256, T, 64]$ |
| Bi-LSTM (2 layers) | $[B \cdot 256, T, 64]$ | hidden 64 | $[B \cdot 256, T, 128]$ |
| linear | $[B \cdot 256, T, 128]$ | (128, 64) | $[B \cdot 256, T, 64]$ |
| reshape | $[B \cdot 256, T, 64]$ | — | $[B, 64, 256, T]$ |
| iTGLU6 ~ 2 | $[B, 128, 256, T]$ | 5×1, stride (1,1), 64 | $[B, 64, 256, T]$ |
| iTGLU1 | $[B, 128, 256, T]$ | 5×1, stride (1,1), 64 | $[B, 2, 256, T]$ |

Input feature is the concatenation of the real and imaginary parts of both channels' STFT (channel dim = 4 → projected to 2 by iGLU1). Two parallel decoders produce amplitude and phase outputs.

## Experimental Setup

| Item | Value |
|------|-------|
| **Speech corpus** | AISHELL-1 (29 h train, 1 h val); TIMIT (1 h, *unseen-language* generalization test) |
| **Noise** | NOISEX-92: 12 noises for training; destroyerops, white, babble for testing |
| **RIR simulation** | [[concepts/image-source-method|Image method]] (Habets); $5 \times 5 \times 3$ m room; 2 mics at 2 cm spacing |
| **Source positions (train)** | 9 positions at $\pm 1.5$ m, $-90°$ to $90°$ with $22.5°$ interval |
| **Source positions (test)** | 17 positions at $11.25°$ interval (unseen DOAs) |
| **SNRs** | -3, 0, 3 dB |
| **Sampling / STFT** | 16 kHz, 32 ms frame, 16 ms shift, sqrt-Hann window, 512-point DFT, 256 frequency bins |
| **Optimizer / LR / batch** | Adam, fixed LR $2 \times 10^{-4}$, batch size 4 |
| **Metrics** | STOI, PESQ, SDR |

### Baselines

- **MVDR** — classical [[concepts/mvdr-beamformer|MVDR beamformer]], given *true* DOA (an oracle upper bound in practice)
- **GCRN** — conventional gated CRN (Tan & Wang 2019), with frequency-downsampling convolutions and full-band LSTM

## Results

### Main Comparison (Table 2)

STOI / PESQ / SDR on TIMIT test set, three SNRs × three test noises. IGCRN outperforms MVDR (with *true* DOA) and GCRN in every condition.

| SNR | Method | STOI (white / destroyerops / babble) | PESQ (white / destroyerops / babble) | SDR (white / destroyerops / babble) |
|------|--------|--------------------------------------|-------------------------------------|-------------------------------------|
| 3 dB | noisy | 0.78 / 0.73 / 0.71 | 1.71 / 1.93 / 1.90 | 3 / 3 / 3 |
| 3 dB | MVDR (true DOA) | 0.88 / 0.87 / 0.87 | 2.63 / 2.59 / 2.65 | 11.6 / 11.1 / 11.7 |
| 3 dB | GCRN | 0.90 / 0.90 / 0.91 | 2.71 / 2.81 / 2.91 | 9.3 / 9.1 / 9.0 |
| 3 dB | **IGCRN** | **0.97 / 0.98 / 0.98** | **3.75 / 3.96 / 3.95** | **19.6 / 21.6 / 21.4** |
| 0 dB | noisy | 0.71 / 0.67 / 0.65 | 1.49 / 1.70 / 1.69 | 0 / 0 / 0 |
| 0 dB | MVDR (true DOA) | 0.87 / 0.85 / 0.85 | 2.55 / 2.51 / 2.54 | 8.6 / 7.8 / 8.4 |
| 0 dB | GCRN | 0.88 / 0.89 / 0.89 | 2.57 / 2.75 / 2.79 | 6.3 / 6.5 / 6.1 |
| 0 dB | **IGCRN** | **0.96 / 0.97 / 0.97** | **3.59 / 3.87 / 3.89** | **18.4 / 20.6 / 20.5** |
| -3 dB | noisy | 0.64 / 0.61 / 0.58 | 1.29 / 1.46 / 1.49 | -3 / -3 / -3 |
| -3 dB | MVDR (true DOA) | 0.85 / 0.84 / 0.83 | 2.49 / 2.45 / 2.46 | 5.4 / 4.4 / 5.3 |
| -3 dB | GCRN | 0.85 / 0.84 / 0.85 | 2.35 / 2.54 / 2.59 | 3.4 / 3.5 / 3.3 |
| -3 dB | **IGCRN** | **0.94 / 0.95 / 0.96** | **3.36 / 3.68 / 3.75** | **15.6 / 18.6 / 19.2** |

*Table 2: STOI / PESQ / SDR comparisons at -3, 0, 3 dB SNR for white, destroyerops, babble noise. Best result in each cell in bold. Average STOI/PESQ gains over noisy speech exceed 30 % / 2.0.*

### Training-Target Ablation (Table 3, -3 dB)

| Method | STOI (white / destroyerops / babble) | PESQ | SDR |
|--------|--------------------------------------|------|-----|
| noisy | 0.64 / 0.61 / 0.58 | 1.29 / 1.46 / 1.49 | -3 / -3 / -3 |
| GCRN(CS) — complex spectral mapping | 0.85 / 0.84 / 0.85 | 2.35 / 2.54 / 2.59 | 3.4 / 3.5 / 3.3 |
| GCRN(Msk+Ps) — amplitude mask + clean phase | 0.90 / 0.87 / 0.85 | 2.74 / 2.75 / 2.62 | 11.6 / 10.0 / 8.5 |
| GCRN(Msk+Map+Ps) — proposed target | 0.90 / 0.88 / 0.87 | 2.89 / 2.87 / 2.77 | 11.8 / 11.3 / 10.4 |
| **IGCRN** | **0.94 / 0.95 / 0.96** | **3.36 / 3.68 / 3.75** | **15.6 / 18.6 / 19.2** |

*Table 3: Ablation on training target at -3 dB SNR.* `GCRN(Msk+Ps)` beats `GCRN(CS)` because amplitude and phase are coupled in the complex spectrum — predicting them separately is more effective than mapping the complex spectrum directly. Adding the amplitude mapping term (`GCRN(Msk+Map+Ps)`) further improves performance, especially at low SNR where the mapping branch pays more attention to the amplitude. The proposed target still falls well short of the full IGCRN, confirming that the inplace architecture (not just the target) drives most of the gain.

### Direction-of-Arrival Analysis (Table 4, -3 dB babble, 11° speech-noise separation)

| DOA | STOI MVDR / GCRN(Msk+Map+Ps) / IGCRN | PESQ MVDR / GCRN / IGCRN | SDR MVDR / GCRN / IGCRN |
|------|--------------------------------------|--------------------------|--------------------------|
| $S=0°, N=11°$ | 0.87 / 0.85 / 0.95 | 2.74 / 2.64 / 3.54 | 11.6 / 9.2 / 17.5 |
| $S=23°, N=34°$ | 0.76 / 0.74 / 0.94 | 2.37 / 2.16 / 3.40 | 6.4 / 3.7 / 15.4 |
| $S=45°, N=56°$ | 0.69 / 0.66 / 0.89 | 1.80 / 1.89 / 2.86 | 0.2 / 1.3 / 9.7 |
| $S=68°, N=79°$ | 0.60 / 0.61 / 0.73 | 1.55 / 1.74 / 2.17 | -1.7 / 0.1 / 3.6 |
| $S=79°, N=90°$ | 0.54 / 0.58 / 0.57 | 1.34 / 1.69 / 1.70 | -6.4 / -0.5 / 0.4 |

*Table 4: Performance as the speech DOA moves from 0° (broadside) to 90° (endfire).* Performance decays for all methods because the time-delay difference between speech and noise shrinks as the source moves toward the array axis. MVDR wins in high-resolution (broadside) conditions because it directly exploits the true DOA. GCRN outperforms MVDR in low-resolution conditions because it uses both spectral and spatial cues. **IGCRN outperforms both MVDR and GCRN at every DOA**, including at $S=0°$ where MVDR is strongest — implying that the inplace design extracts spatial information more effectively than the conventional CRN.

### Downsampling Ablation (Table 5, -3 dB babble)

| Method | STOI | PESQ | MAC (G) | Params (M) | LSTM hidden |
|--------|------|------|---------|------------|-------------|
| noisy | 0.583 | 1.49 | — | — | — |
| GCRN | 0.847 | 2.59 | 28.8 | 71.8 | 1024 |
| **IGCRN64** (proposed) | **0.968** | **3.83** | 19.9 | 1.4 | 64 |
| IGCRN80 | 0.982 | 4.02 | 31.1 | 2.3 | 80 |
| IGCRN64-1DS | 0.982 | 3.94 | 32.1 | 3.5 | 128 |
| IGCRN64-2DS | 0.981 | 3.91 | 53.3 | 9.5 | 256 |
| IGCRN64-3DS | 0.974 | 3.73 | 85.3 | 24.1 | 512 |
| IGCRN64-4DS | 0.961 | 3.58 | 149.5 | 82.5 | 1024 |
| IGCRN64-5DS | 0.954 | 3.52 | 277.8 | 316.3 | 2048 |
| IGCRN64-6DS | 0.949 | 3.51 | 430.8 | 777.3 | 2048 |

*Table 5: Effect of frequency downsampling on performance and complexity. `IGCRN(n)-(k)DS` = IGCRN with first-GLU output channel $n$ and $k$ downsampling operations (each downsampling doubles the channel dimension).*

This is the most striking ablation in the paper: **performance degrades monotonically as downsampling is added, even though model complexity grows by orders of magnitude**. `IGCRN64-6DS` has 777 M parameters (556× more than `IGCRN64`) and 430 G MACs (22× more) but worse STOI and PESQ. The authors interpret this as direct evidence that the inplace characteristic — preserving per-bin spatial cues — is essential for multi-channel time-frequency-domain enhancement, and that downsampling aliases spatial information with spectral patterns in a way that more capacity cannot recover.

`IGCRN80` widens the channel from 64 to 80 to match `IGCRN64-1DS` in MAC count, and beats it on both STOI and PESQ — confirming that widening the inplace model is more parameter-efficient than reintroducing downsampling.

### Parameter Efficiency

The reuse mechanism of the channel-wise LSTM makes IGCRN extremely compact: **1.4 M parameters, 19.9 G MACs** — both lower than the conventional GCRN (71.8 M params, 28.8 G MACs), despite IGCRN being the larger-performing model. The parameter savings come from (a) skipping the frequency-downsampling channel expansion and (b) sharing one 64-hidden LSTM across all 256 frequency bins instead of one 1024-hidden LSTM over the flattened feature.

## Key Contributions

1. **Inplace GCRN architecture for dual-channel speech enhancement** — an end-to-end CRN-style network whose three stages (inplace encoder / channel-wise LSTM / inplace decoder) mirror the classical beamforming pipeline (DOA estimation / beamforming / post-filtering), implemented within the manifold space of multi-channel signals.
2. **[[concepts/inplace-convolution|Inplace convolution]]** — stride-1 convolution on the frequency dimension, preserving per-bin spatial cues that downsampling convolutions would alias with spectral patterns; ablation shows this is the dominant source of IGCRN's gains.
3. **[[concepts/channel-wise-lstm|Channel-wise LSTM with model reuse]]** — one LSTM applied per frequency bin and reused across all bins, motivated by the fact that per-bin time delays are frequency-independent; reduces LSTM hidden size from 1024 to 64 while still covering all 256 bins, making the model extremely compact (1.4 M params).
4. **[[concepts/mask-mapping-amplitude-prediction|Mask + mapping + phase training target]]** — combines amplitude mask, amplitude mapping, and phase prediction in a single decoder, generalizing prior mask+phase (Phasen) and mask+mapping ensemble targets; ablation shows each addition improves performance.
5. **Empirical demonstration that inplace design beats downsampling even at 500× the parameters** — the downsampling ablation (Table 5) provides direct evidence that the inplace characteristic, not capacity, drives multi-channel SE performance in the time-frequency domain.

## Related Concepts

- [[concepts/igcrn|IGCRN]] — the proposed model
- [[concepts/inplace-convolution|Inplace Convolution]] — the core architectural choice
- [[concepts/channel-wise-lstm|Channel-wise LSTM with Model Reuse]] — the compact recurrent bottleneck
- [[concepts/mask-mapping-amplitude-prediction|Mask + Mapping + Phase Target]] — the proposed training target
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — CRN family baseline
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]] — related training paradigm (IGCRN's target is a mask + mapping + phase variant rather than pure CSM)
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — broader task
- [[concepts/mvdr-beamformer|MVDR Beamformer]] — oracle baseline
- [[concepts/beamforming|Beamforming]] — traditional pipeline IGCRN mirrors
- [[concepts/image-source-method|Image Source Method]] — RIR simulation
- [[concepts/pesq|PESQ]] — quality metric

## Related Synthesis

No synthesis page currently incorporates this source. IGCRN is a single-task dual-channel SE system evaluated on simulated data (AISHELL-1 + NOISEX-92 with image-method RIRs); it does not fit into the existing joint multi-task / ultra-low-latency synthesis (which focuses on joint AEC+NS+DR at sub-10 ms latency on VoiceBank+DEMAND or DNS challenge benchmarks). Its key role in the wiki is as the **predecessor of ICCRN** in the inplace-CRN lineage — see [[concepts/iccrn|the ICCRN concept page]] for the lineage summary.
