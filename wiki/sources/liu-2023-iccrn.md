---
type: source
created: 2026-08-01
updated: 2026-08-01
sources:
  - raw/papers/liu-2023-iccrn/full-text.md
  - https://doi.org/10.1109/ICASSP49357.2023.10096918
  - zotero://select/items/0_S3KNZA83
tags:
  - speech-enhancement
  - cepstral-analysis
  - convolutional-recurrent-network
  - inplace-model
  - complex-spectrum-mapping
  - icassp-2023
---

# Liu & Zhang 2023: ICCRN — Inplace Cepstral Convolutional Recurrent Neural Network

**Authors**: [[entities/jinjiang-liu|Jinjiang Liu]], [[entities/xueliang-zhang|Xueliang Zhang]]
**Affiliation**: College of Computer Science, Inner Mongolia University, China
**Venue**: ICASSP 2023, pp. 1–5
**Year**: 2023
**Type**: Conference paper
**DOI**: [10.1109/ICASSP49357.2023.10096918](https://doi.org/10.1109/ICASSP49357.2023.10096918)
**Zotero**: [S3KNZA83](zotero://select/items/0_S3KNZA83)

## Summary

The paper proposes **ICCRN** (Inplace Cepstral Convolutional Recurrent Neural Network), a monaural speech enhancement model that augments the authors' earlier inplace CRN (IGCRN) with a novel **Cepstral Frequency Block (CFB)**. The CFB performs neural processing in a *cepstral space* obtained by applying a real-valued FFT to the time-frequency (TF) feature map inside the network. Because speech harmonics are sparsely represented by a few pitch peaks in the cepstral domain, the cepstral branch can recover harmonic structure that is hard to model directly in the frequency domain. Trained and evaluated at low SNRs (-5 dB to 0 dB) on WSJ0 SI-84 with 10000 kinds of training noise, ICCRN outperforms strong baselines (GCRN, DCCRN, DPCRN, DCCRN-CSM, DPCRN-CSM) on STOI and PESQ in babble and cafeteria noise, especially at -5 dB — while being the most compact model (0.46 M params, 2.09 G MACs).

## Problem Formulation

Noisy speech in the TF domain is modeled as additive:

$$X[k] = S[k] + N[k]$$

where $S$ and $N$ are the spectra of clean speech and noise, and $k$ is the frame index. ICCRN directly maps the real and imaginary parts of the noisy spectrum $X$ to those of the clean spectrum $S$ (i.e., [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]). The training loss is a weighted L1 combination of real, imaginary, and magnitude errors:

$$\mathcal{L} = \left\| \mathcal{R}(\hat{S}) - \mathcal{R}(S) \right\|_1 + \left\| \mathcal{I}(\hat{S}) - \mathcal{I}(S) \right\|_1 + \alpha \left\| |\hat{S}| - |S| \right\|_1$$

with $\alpha = 2$ to emphasize amplitude. The estimated spectrum is first inverted to the time domain and re-transformed back to the TF domain before computing the loss, which alleviates the [[concepts/stft-consistency|STFT consistency]] problem.

## Methodology

### Motivation: Sparsity of Speech in the Cepstral Space

Speech production decomposes into **excitation** (vocal cords) and **vocal tract** (filter). In the cepstral domain, the slowly varying spectral envelope — carrying timbre and semantic content — concentrates in the narrow low-quefrency band, while the densely periodic harmonics collapse to a few sparsely distributed pitch peaks in the higher-quefrency band. Because most noises do not share this envelope/harmonic structure, speech components are distinguishable from noise cepstrally even at low SNR.

![[raw/papers/liu-2023-iccrn/figures/acf30afb626deabce1db58b6a943f76a6a8e651abff168daca2cad4f1f05f569.jpg|(a) Noisy spectrum]]
![[raw/papers/liu-2023-iccrn/figures/d3f5dc251edbce021ab9910ab93b00dfaddca05fa19a38a88dd31806caa0a8d4.jpg|(b) Corresponding cepstrum]]
*Figure 1: Harmonics in the frequency domain are sparsely represented by a few pitch peaks in the cepstrum domain. Noise barely perturbs those peaks.*

### Cepstral Frequency Block (CFB)

The CFB is the core novel module replacing the Gated Linear Units (GLUs) of IGCRN. It jointly processes the feature map in the TF domain and in the cepstral space, then fuses the two branches.

![[raw/papers/liu-2023-iccrn/figures/3e6ba05bde3daf360d53cc18c4ec6214b4b956971227ab629b14c74049135d2a.jpg|Cepstral frequency block (CFB) and cepstral unit]]
*Figure 2: The proposed Cepstral Frequency Block (CFB) and the cepstral unit. Conv F×T = 2D convolution over frequency×time; Ceps-chBLSTM(c)×n = BLSTM processing on the cepstral-bin sequence within a frame (c = hidden size per direction, n = number of layers); Sig = sigmoid; LN = LayerNorm on channel and frequency dimensions; [b, c, f, t] = dimension sizes (batch, channel, frequency, time).*

The CFB has three sub-modules:

1. **Task-split gate**. A `LN → Conv1×1 → Sigmoid` module produces a gate; the input TF feature is projected by a `Conv1×1` and multiplied by the gate to split the task into a cepstral-branch input and a TF-branch residual.

2. **Cepstral unit (Ceps Unit)**. The gated feature is transformed into the cepstral space by a real-valued FFT applied per channel per frame. The cepstral feature is processed by:
    - **Cepstral LayerNorm**. Statistics $E_{c,f}$ and $\mathrm{Var}_{c,f}$ are computed jointly over channel and cepstral dimensions to stabilize the very different energy distributions across quefrency bands. A learned affine $\gamma \in \mathbb{R}^{c \times f}$ and $\beta \in \mathbb{R}^{c \times f}$ then individually rescale each cepstral bin in each channel:

      $$\mathrm{LN}(\mathbf{x}) = \frac{\mathbf{x} - E_{c,f}[\mathbf{x}]}{\sqrt{\mathrm{Var}_{c,f}[\mathbf{x}] + \epsilon}} \odot \gamma + \beta$$

      Multiplication in the cepstral domain is equivalent to circular convolution in the frequency domain, so the learned $\gamma$ acts as a bank of full-size (160-tap) frequency-domain filters — even before any densely connected neural layers. The paper highlights this as the reason the ablation `ICCRN(cepsLN)` (cepstral LN alone, no Ceps-chBLSTM) already yields large gains over the no-ceps ablation.
    - **Cepstral channel-wise BLSTM (Ceps-chBLSTM)**. Treats cepstral bins as a time series and processes them with a BLSTM, so the network knows which quefrency band it is filtering and can apply different patterns to different bands. This replaces the alternative of splitting the cepstrum into ≥10 sub-bands with separate $3 \times 1$ convolutions, at much lower complexity.

3. **TF-domain residual branch**. A `LN → Conv3×1` module processes the residual of the gated feature directly in the TF domain. Speech energy is sparse cepstrally; some noise (e.g., tonal or narrowband) is sparser in the frequency domain, so cross-domain modeling is complementary.

The outputs of the cepstral unit and the TF branch are added to produce the CFB output.

### Why FFT for the Space Transformation?

The cepstral transform uses the classical FFT rather than a learnable transform, for three reasons: (1) the DFT is orthogonal — its coefficients are independent and introduce no information loss or dataset bias, unlike data-driven transforms; (2) the DFT spectrum has a clear physical ordering (low- to high-quefrency bins), enabling analysis and tuning; (3) the FFT is parameterless and has linearithmic complexity. In this work, the FFT costs only **0.15 G MACs**, whereas a DFT or neural transform would cost ~0.95 G MACs.

### ICCRN Architecture

The ICCRN follows a U-Net structure with skip connections.

![[raw/papers/liu-2023-iccrn/figures/b78acf3d0bc11bceeff9039178d18aaf8bd657e876b235079d7ee227ec209696.jpg|ICCRN architecture]]
*Figure 3: Implemented ICCRN architecture.*

- **Input**: real and imaginary parts of the complex STFT spectrum stacked along the channel dimension, with shape `[Batch, 2, F=160, Time]`.
- **Encoder projection**: a channel-wise BLSTM (F-chBLSTM) projects the 2-channel input to a higher-dimensional feature (channel size $c = 20$).
- **Encoder**: 5 sequential Cepstral Frequency Blocks process the feature. No frequency downsampling is performed — the frequency dimension stays at $f = 160$ throughout, and all convolutions share output channel size $c = 20$.
- **Bottleneck**: a 2-layer channel-wise LSTM (T-chLSTM×2, hidden size $2c$) computes a mask multiplied with the encoder output.
- **Decoder**: 5 cascaded CFBs process the masked feature stacked with skip-connection features; a final T-chLSTM refines the time dimension.
- **Output**: a $1 \times 1$ convolution compresses the channel dimension back to 2, producing the estimated real and imaginary parts of the STFT.

The system is **causal** (no reference to future frames) and uses 50%-overlap STFT (20 ms Hamming window, 160 frequency bins).

### Inplace Design Choice

ICCRN inherits the *inplace* design from IGCRN (Liu & Zhang 2021): no frequency downsampling, channel-wise LSTM processes each frequency bin independently. IGCRN was originally designed for multi-channel speech enhancement, where preserving per-bin spatial cues matters; its monaural performance was weak because discarding frequency downsampling also discards full-band modeling capacity. ICCRN recovers that capacity by replacing GLUs with CFBs that model speech in the cepstral space.

## Experimental Setup

| Item | Value |
|------|-------|
| **Speech corpus** | WSJ0 SI-84 (77 speakers for training, 6 for unseen-speaker generalization test) |
| **Training noise** | ~126 h / 10 000 kinds of high-quality non-speech sounds (sound-ideas.com) |
| **Validation noise** | -5 dB NOISEX-92 (except babble) |
| **Training SNRs** | Uniformly sampled from {-5, -4, -3, -2, -1, 0} dB |
| **Test noise** | Babble and cafeteria from Auditec CD |
| **Test SNRs** | -5 dB, 0 dB, and unseen 5 dB |
| **Sampling / STFT** | 16 kHz, 20 ms Hamming window, 50% frame shift, 160 frequency bins |
| **Optimizer / LR** | AdamW, fixed LR 0.001 |
| **Batch size / Framework** | 24 / DDP with PyTorch |
| **Loss weight** | $\alpha = 2$ on amplitude error |
| **Causality** | All systems causal; no future-frame reference |

### Baselines and Ablations

- **Baselines**: IGCRN (authors' previous model), IGCRN(DIL) (dilated-conv variant of IGCRN), GCRN (Tan & Wang 2019), DCCRN (Hu et al. 2020), DPCRN (Le et al. 2021). For fair comparison, DCCRN(CSM) and DPCRN(CSM) use the same complex-spectrum-mapping loss as ICCRN.
- **Ablations**:
    - `ICCRN` — proposed model, CFB channel size $c = 20$.
    - `ICCRN(-freq)` — TF-domain `LN → Conv3×1` branch short-circuited.
    - `ICCRN(-ceps)` — cepstral unit short-circuited.
    - `ICCRN(cepsLN)` — cepstral-chBLSTM removed; cepstral feature processed only by the cepstral LayerNorm.

## Results

### STOI / PESQ on WSJ0 SI-84 (Auditec babble & cafeteria noise)

| Noise | Babble STOI (%) / PESQ | Cafeteria STOI (%) / PESQ |
|---|---|---|
| **SNR** | -5 / 0 / 5 dB | -5 / 0 / 5 dB |
| Mixture | 58.50 / 70.35 / 81.18 — 1.537 / 1.819 / 2.119 | 57.52 / 69.86 / 81.06 — 1.464 / 1.767 / 2.122 |
| IGCRN | 77.38 / 88.98 / 94.25 — 1.953 / 2.612 / 3.067 | 75.73 / 88.32 / 93.84 — 1.984 / 2.609 / 3.054 |
| IGCRN(DIL) | 78.88 / 89.80 / 94.66 — 1.992 / 2.629 / 3.088 | 77.07 / 89.29 / 94.23 — 2.048 / 2.658 / 3.085 |
| GCRN | 80.98 / 90.74 / 94.64 — 2.014 / 2.594 / 3.059 | 77.95 / 89.17 / 94.08 — 1.936 / 2.557 / 3.015 |
| DCCRN | 80.52 / 89.82 / 94.12 — 2.177 / 2.747 / 3.084 | 79.25 / 89.14 / 93.66 — 2.221 / 2.732 / 3.072 |
| DPCRN | 80.30 / 90.42 / 94.80 — 2.174 / 2.816 / 3.199 | 75.87 / 88.80 / 94.07 — 2.013 / 2.680 / 3.139 |
| DCCRN(CSM) | 81.72 / 91.03 / 94.93 — 2.216 / 2.827 / 3.265 | 80.30 / 90.39 / 94.57 — 2.241 / 2.857 / 3.235 |
| DPCRN(CSM) | 83.21 / 91.76 / 95.39 — 2.212 / 2.814 / 3.212 | 80.03 / 90.36 / 94.68 — 2.226 / 2.759 / 3.164 |
| **ICCRN** | **84.48 / 92.36 / 95.81** — **2.231 / 2.818 / 3.242** | **80.73 / 90.84 / 94.95** — **2.257 / 2.737 / 3.172** |
| ICCRN(-freq) | 83.21 / 91.91 / 95.62 — 2.134 / 2.752 / 3.217 | 80.14 / 90.54 / 94.83 — 2.085 / 2.689 / 3.126 |
| ICCRN(-ceps) | 74.12 / 86.82 / 93.19 — 1.793 / 2.455 / 2.973 | 72.76 / 86.25 / 92.72 — 1.900 / 2.491 / 2.949 |
| ICCRN(cepsLN) | 78.35 / 89.57 / 94.45 — 1.947 / 2.625 / 3.079 | 76.17 / 88.52 / 93.73 — 1.961 / 2.578 / 3.017 |

*Table 1: STOI (%) and PESQ comparisons at -5 dB, 0 dB, 5 dB SNR (auditec babble & cafeteria). Best STOI in each column in bold.*

### Key Findings

- ICCRN is the **best STOI** model in every test condition, with the largest gap at -5 dB: in babble -5 dB, +1.27 pp STOI over DPCRN(CSM) and +3.50 pp over GCRN.
- The **+7.1 pp STOI** and **+0.278 PESQ** improvement of ICCRN over the original IGCRN at -5 dB babble is the largest single-model gain reported in the paper.
- **Ablation `ICCRN(-ceps)` is the worst** by a wide margin (e.g., 74.12 vs 84.48 STOI at -5 dB babble), confirming that the cepstral branch contributes far more than the TF-domain `Conv3×1` branch. Removing the TF branch (`ICCRN(-freq)`) still beats all baselines on STOI.
- **`ICCRN(cepsLN)` surprises**: a single cepstral LayerNorm — with no LSTM or CNN in the cepstral branch — already lifts `ICCRN(-ceps)` by +4.23 pp STOI and +0.154 PESQ at -5 dB babble. The authors attribute this to the equivalent full-size frequency-domain circular-convolution bank realized by the learned affine $\gamma$.

### Recovering a Destroyed Spectrum

To visualize the cepstral branch's effect, the authors delete the 1–3 kHz band of clean speech and replace it with -5 dB white noise, then ask each model to recover the missing band from spectral context.

![[raw/papers/liu-2023-iccrn/figures/69baaf97db6d652af0a738c49c8959b13cae3b273213eae0cf040ca760ffbfa8.jpg|Spectrum recovery test]]
*Figure 4: Recovering a destroyed spectrum. The 1–3 kHz speech band is removed and replaced with -5 dB white noise; models must synthesize the missing speech from spectral context.*

All complex-mapping baselines can synthesize speech in frames with strong spectral context, but frequency-domain models fail in faint areas. ICCRN produces more precise fine-structure estimates, attributed to the sparsity and distinctness of pitch peaks in the cepstral domain.

### Model Complexity

| Model | GCRN | DPCRN | DCCRN | **ICCRN** |
|-------|------|-------|-------|-----------|
| MAC (G) | 2.42 | 3.18 | 5.59 | **2.09** |
| Param (M) | 9.77 | 0.81 | 3.67 | **0.46** |

*Table 2: MACs and parameters. ICCRN's neural part costs 1.94 G MAC; the FFT transform costs only 0.15 G MAC.*

ICCRN is the most compact model — about half the parameters of DPCRN and one-eighth of DCCRN, with the lowest MAC count. The inplace design (no frequency downsampling) avoids the channel expansion that downsampling-based CRNs require, which is the main source of the parameter savings.

### Comparison with FFC-SE

The authors contrast ICCRN with the contemporaneous FFC-SE (Shchekotov et al., Interspeech 2022), which also uses FFT-domain processing but is inspired by Fast Fourier Convolution from computer vision:

- FFC-SE uses $1 \times 1$ convolutions in the FFT domain, which is suitable for image content with little shared pattern but inadequate for speech spectra that share a fairly fixed cepstral pattern. ICCRN instead uses a cepstral BLSTM that models the cepstral-bin sequence with both short- and long-term patterns.
- FFC-SE uses batch normalization; ICCRN argues layer normalization is better suited to cepstral-feature distributions.
- ICCRN is causal, uses short windows, and uses channel-wise LSTM for the time dimension; FFC-SE differs on these aspects.

## Key Contributions

1. **Cepstral Frequency Block (CFB)** — a novel in-place block that augments a TF-domain `LN → Conv3×1` residual with a cepstral-space branch (FFT → cepstral LN → cepstral channel-wise BLSTM → iFFT), enabling joint cross-domain speech-enhancement modeling.
2. **Cepstral-space LayerNorm as an implicit full-size frequency filter bank** — the learned per-bin affine parameters $\gamma \in \mathbb{R}^{c \times f}$ are mathematically equivalent to a bank of full-size (160-tap) circular-convolution kernels in the frequency domain. The `ICCRN(cepsLN)` ablation shows this single normalization layer (no LSTM/CNN in the cepstral branch) already yields large gains over the no-ceps baseline.
3. **Channel-wise BLSTM over cepstral bins** — treats cepstral bins as a sequence so the LSTM can apply band-specific filtering patterns, replacing a costly multi-sub-band CNN alternative.
4. **FFT as a parameterless, low-cost space transform** — uses classical FFT (0.15 G MAC) instead of a learnable transform (0.95 G MAC), avoiding dataset bias and ensuring physically interpretable cepstral-bin ordering.
5. **State-of-the-art low-SNR performance at minimum complexity** — ICCRN achieves the best STOI across all test conditions on WSJ0 SI-84 with Auditec babble/cafeteria noise, especially at -5 dB, while being the smallest model (0.46 M params, 2.09 G MACs).

## Related Concepts

- [[concepts/iccrn|ICCRN]] — the proposed model
- [[concepts/cepstral-frequency-block|Cepstral Frequency Block (CFB)]] — the core novel module
- [[concepts/cepstral-space-speech-enhancement|Cepstral-Space Speech Enhancement]] — the broader paradigm
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — CRN family baseline
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]] — training paradigm
- [[concepts/stft-consistency|STFT Consistency]] — loss-construction technique used in training
- [[concepts/speech-enhancement|Speech Enhancement]] — broader task
- [[concepts/pesq|PESQ]] — quality metric

## Related Sources

- [[sources/liu-2021-igcrn|Liu & Zhang 2021: IGCRN]] — predecessor; introduces the inplace CRN design (inplace convolutions + channel-wise LSTM with model reuse) for dual-channel SE. ICCRN inherits the inplace design and replaces the GLU blocks with the Cepstral Frequency Block to recover the full-band modeling capacity that IGCRN sacrificed by discarding frequency downsampling.

## Related Synthesis

No synthesis page currently incorporates this source. ICCRN is a single-task monaural speech-enhancement system evaluated on WSJ0 SI-84 with Auditec noise; it does not fit cleanly into the existing multi-task / low-latency synthesis (which focuses on joint AEC+NS+DR at sub-10 ms latency on VoiceBank+DEMAND or DNS challenge benchmarks). Its cepstral-domain processing axis is a new dimension not represented in any current synthesis page; should a future synthesis on cross-domain speech enhancement (TF vs. cepstral vs. time-domain) emerge, this paper would be a foundational reference.
