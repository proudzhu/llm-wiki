---
type: source
created: 2026-08-01
updated: 2026-08-01
sources:
  - raw/papers/liu-2026-sse-net/full-text.md
  - https://doi.org/10.1109/TASLPRO.2026.3677621
  - zotero://select/items/0_DPLD7XGZ
tags:
  - speech-enhancement
  - spiking-neural-networks
  - neuromorphic-computing
  - low-power
  - monaural
  - causal
---

# Liu, Li, Fan, Zheng, Yi, Fu, Li, Zhou & Lv 2026: SSE-Net — Toward Low-Power-Consumption Spiking Neural Network for Monaural Speech Enhancement

- **Authors**: [[entities/enrui-liu|Enrui Liu]], [[entities/andong-li|Andong Li]], [[entities/cunhang-fan|Cunhang Fan]], [[entities/chengshi-zheng|Chengshi Zheng]], [[entities/jiangyan-yi|Jiangyan Yi]], [[entities/ruibo-fu|Ruibo Fu]], [[entities/xinhui-li|Xinhui Li]], [[entities/jian-zhou|Jian Zhou]], [[entities/zhao-lv|Zhao Lv]]
- **Institutions**: School of Computer Science and Technology, Anhui University; Key Laboratory of Noise and Vibration Research, Institute of Acoustics, Chinese Academy of Sciences; Institute of Automation, Chinese Academy of Sciences (CASIA)
- **Venue**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 34, 2026
- **Type**: Journal article
- **DOI**: [10.1109/TASLPRO.2026.3677621](https://doi.org/10.1109/TASLPRO.2026.3677621)
- **Zotero**: [DPLD7XGZ](zotero://select/items/0_DPLD7XGZ)

## Summary

SSE-Net (Spiking Speech Enhancement Network) is a monaural speech enhancement model whose **every block is designed natively for spike signals**, rather than converting an existing ANN architecture (the dominant prior approach for [[concepts/spiking-neural-networks|SNN]]-based SE). It couples a spiking encoder–decoder (built from residual [[concepts/spiking-feature-extraction-block|Spiking Feature Extraction Blocks]] with LIF neurons) to a continuous-domain [[concepts/information-transformation-block|Information Transformation Block]] that converts discrete spikes back to continuous features, mitigating the information loss inherent to binary activation. On WSJ0-SI84+DNS-Challenge and VoiceBank+DEMAND, SSE-Net is SOTA among SNN-based SE models (WB-PESQ 2.89 on VoiceBank+DEMAND) while reporting a **power proxy of 19.70 M Ops/s — 62% lower than Spiking-FullSubNet** (the Intel N-DNS Challenge winner) — with MACs of 0.44 G/s (≈17× lower than the average ANN baseline).

## Problem Formulation

In the STFT domain, the noisy mixture is modeled as

$$\mathrm{Y}_{(t,f)} = \mathrm{X}_{(t,f)} + \mathrm{N}_{(t,f)},$$

with $\{Y, X, N\} \in \mathbb{C}^{T \times F}$ the mixture, clean, and noise spectra. The paper targets **two intrinsic challenges of SNN-based SE**:

1. **ANN→SNN conversion breaks training**: prior SNN-SE models (Spiking-U-Net, Spiking-FullSubNet, DPSNN) convert ANN models by replacing activation functions with spiking units. This keeps redundant ANN layers, confuses the network structure, creates training difficulties, and causes information mismatch.
2. **Binary activation causes information loss**: LIF spiking neurons output 0/1 spikes; speech has complex, multi-timescale temporal patterns, so discrete activation plus simplified spatio-temporal dynamics loses information that a continuous model would preserve.

The paper also notes the motivating symmetry: the time–frequency domain is itself sparse (few T-F bins active at once), which matches SNN sparsity — an argument originally made in the context of the Intel Neuromorphic DNS Challenge.

## Methodology

![[raw/papers/liu-2026-sse-net/figures/dbb0267d7fe108291f54f93bc54e24ca0e476ec56c5f6833ec115cac13e8167c.jpg|SSE-Net architecture overview]]

*Figure 1: (a) Overall SSE-Net — encoder–decoder built from Spiking Feature Extraction Groups (SFEG, LIF-based) with skip connections, followed by an Information Transformation Block (ITB). (b) SFEB internal structure — residual three-branch design with LIFNodes. (c) ITB — converts discrete spike signals into continuous signals.*

### Input encoding

The complex spectrum $\mathbf{Y} \in \mathbb{R}^{B \times 2 \times T \times F}$ (real and imaginary parts stacked on the channel axis) is **replicated K times along a new first dimension** to form the spiking time-step sequence $\bar{\mathbf{Y}} = \{\mathbf{Y}_k\}_{k=1}^{K} \in \mathbb{R}^{K \times B \times 2 \times T \times F}$. Each $\mathbf{Y}_k$ is the same spectrum fed to the network at time step $k$ — a rate-encoding-style repetition (see ablation below for the K study).

### Encoder–Decoder (spiking)

1. A Conv2D layer (kernel 3×1, stride 1) extracts shallow features.
2. The **encoder** stacks $N$ SFEBs interleaved with DownSampling Blocks (LIF → Conv2D → GroupNorm), progressively abstracting features (channel width 24 → 48 → 96; frequency axis 161 → 81 → 41).
3. The **decoder** mirrors this with SFEBs + UpSampling Blocks, restoring original dimensions; skip connections (concatenation on the feature axis) counteract information loss and gradient vanishing.
4. A Conv2D layer estimates a mask applied to the original spectrum; ISTFT yields the enhanced waveform.

### Spiking Feature Extraction Block (SFEB)

The [[concepts/spiking-feature-extraction-block|SFEB]] is a **three-branch residual block**:

- **Branch 1 (spiking)**: LIF → Conv2D(3×1) → GroupNorm, applied twice — converts input to 0/1 spikes and re-extracts features from the spike domain.
- **Branch 2 (continuous)**: Conv2D → GroupNorm — preserves a non-spiked feature path.
- **Fusion**: element-wise addition of both branches with the original input:
$$\hat{X}_{k1} = \mathrm{GN}(\mathrm{Conv2D}(\mathrm{LIF}(\mathrm{GN}(\mathrm{Conv2D}(\mathrm{LIF}(A_k)))))), \quad \hat{X}_{k2} = \mathrm{GN}(\mathrm{Conv2D}(A_k)), \quad \hat{X}_k = A_k \oplus \hat{X}_{k1} \oplus \hat{X}_{k2}$$

The residual fusion mitigates the information loss of binary quantization — the ablation (w/o SFEB → plain LIF) drops PESQ from 2.89 to 2.70.

### LIF neuron dynamics

The leaky integrate-and-fire model used throughout is described by:

$$\mathbf{H}_k^n = \mathbf{U}_{k-1}^n + \tfrac{1}{\tau}\big(\mathbf{X}_k^n - (\mathbf{U}_{k-1}^n - V_{\text{reset}})\big), \qquad \mathbf{S}_k^n = \Theta(\mathbf{H}_k^n - V_{\text{thr}}), \qquad \mathbf{U}_k^n = (\beta \mathbf{H}_k^n) \odot (\mathbf{1} - \mathbf{S}_k^n) + V_{\text{reset}} \mathbf{S}_k^n$$

where $k$ indexes the spiking time step, $\tau$ is the membrane time constant, $V_{\text{reset}}$ the reset potential, $V_{\text{thr}}$ the firing threshold, and $\beta$ the decay factor.

### Information Transformation Block (ITB)

The [[concepts/information-transformation-block|ITB]] converts discrete spike features back to continuous values with a **two-branch gating structure** (in spirit similar to ANN gating/refinement blocks):

$$\hat{F}_1 = \phi(\mathrm{Conv2d}(\sigma(\mathrm{Conv2d}(\mathrm{Conv2d}(Z_k))))), \qquad \hat{F}_2 = \phi(\mathrm{Conv2d}(\sigma(\mathrm{Conv2d}(\mathrm{AvgPool}(Z_k))))), \qquad \hat{F} = (\hat{F}_1 \otimes Z_k) \oplus (\hat{F}_2 \otimes (1 - \hat{F}_1))$$

with $\sigma$ = Sigmoid, $\phi$ = ReLU. Branch 1 acts as a self-gate on the input; branch 2 (average-pooled context) supplies complementary information where the gate is off. A visualization study (Fig. 2) shows the ITB removes pixelation, refines feature granularity, and recovers speech information lost before the block.

![[raw/papers/liu-2026-sse-net/figures/c4fccf40c02cd12056767d0a36fbe12011834a10760852fcf1c0ab18c412af7a.jpg|ITB feature map visualization]]

*Figure 2: Feature maps before/after the ITB vs. clean and noisy speech — the ITB refines granularity and recovers lost speech information (red/yellow boxes).*

### Training

- **Gradient proxy**: because spike firing is non-differentiable, a **Sigmoid surrogate gradient** $\sigma(x) = 1/(1+e^{-\alpha x})$ with scale hyperparameter $\alpha$ is used for backpropagation (surrogate-gradient training rather than ANN-SNN conversion).
- **Loss**: RI loss + magnitude constraint, $\mathcal{L} = \beta \mathcal{L}_{RI} + (1-\beta)\mathcal{L}_{Mag}$ with $\beta = 0.5$:
$$\mathcal{L}_{RI} = \|\tilde{S}_r - S_r\|_F^2 + \|\tilde{S}_i - S_i\|_F^2, \qquad \mathcal{L}_{Mag} = \left\| \sqrt{|\tilde{S}_r|^2 + |\tilde{S}_i|^2} - \sqrt{|S_r|^2 + |S_i|^2} \right\|_F^2$$

### Power-consumption metrics (Intel N-DNS Challenge conventions)

Following the [[concepts/intel-neuromorphic-dns-challenge|Intel Neuromorphic DNS Challenge]], energy is estimated via synaptic operations (SynOPs) and neuron operations (NeuronOPs), weighted by the Intel Loihi observation that one NeuronOP ≈ 10× one SynOP:

$$P_{\text{proxy}} = \mathrm{SynOPs} + 10 \times \mathrm{NeuronOPs}, \qquad \mathrm{SynOPs} = \textstyle\sum_{l=1}^{L-1}\sum_{i=1}^{\mathcal{N}^l} \mathcal{R}_i^l (\mathcal{N}^{l+1} + \mathcal{N}^l), \qquad \mathrm{NeuronOPs} = \textstyle\sum_{l=1}^{L} \mathcal{N}^l, \qquad \mathrm{PDP}_{\text{proxy}} = P_{\text{proxy}} \times \text{Latency}$$

with $\mathcal{R}_i^l$ the firing rate of neuron $i$ in layer $l$ and $\mathcal{N}^l$ the neuron count.

## Experimental Setup

| Item | Value |
|------|-------|
| **Dataset 1** | WSJ0-SI84 + DNS-Challenge: 7,138 clean utterances (83 speakers); 5,428/957 train/validation splits; ~20,000 DNS-Challenge noise types mixed to ~55 h; causal evaluation at −5/0/5 dB SNR (Factory1, Babble noises) |
| **Dataset 2** | [[concepts/voicebank-demand\|VoiceBank+DEMAND]]: 28 train speakers / 2 test speakers, 11,572 noisy-clean pairs, 10 noise types (8 DEMAND + 2 artificial); non-causal evaluation |
| **Metrics** | NB/WB-PESQ, STOI, ESTOI, SI-SDR, MOS (CSIG, CBAK, COVL); SNN power metrics: power proxy (Ops/s), PDP proxy (Ops), energy cost (J) |
| **Network** | K time steps (K=1 chosen), B batch, 161 frequency bins, 2 RI channels; encoder 24→48→96 ch, decoder symmetric, skip connections, ITB refinement, mask estimation + ISTFT |
| **Training** | Sigmoid surrogate gradient (scale α), $\mathcal{L} = 0.5\mathcal{L}_{RI} + 0.5\mathcal{L}_{Mag}$ |
| **Baselines (WSJ0-DNS, causal)** | Time-domain: ConvTasNet, DPRNN; T-F: LSTM, CRN, GCRN, DCCRN, FullSubNet; SNN: Spiking-U-Net |
| **Baselines (VB+DEMAND, non-causal)** | SEGAN, MMSE-GAN, Wavenet, MetricGAN, DCCRN, S4DSE (ANN); Spiking-FullSubNet, Spiking-U-Net (SNN) |

## Results

### K time-step ablation (Table III)

| K | PESQ (WSJ0+DNS) | PESQ (VB+Demand) | PDP proxy (Ops) | Energy cost (J) |
|---|---|---|---|---|
| K=1 | 2.20 | **2.89** | **0.63 M** | **1.31 μ** |
| K=2 | 2.20 | 2.87 | 0.82 M | 1.71 μ |
| K=4 | 2.25 | 2.85 | 1.27 M | 2.64 μ |
| K=6 | **2.31** | 2.81 | 1.62 M | 3.37 μ |

Larger K (more temporal replication) costs energy but gains little quality — the authors conclude the current encoding "resembles rate-coding-like repetition and fails to fully leverage temporal encoding," motivating future work on frame-history-conditioned K. **K=1 is used in all main experiments.**

### Module ablation (Table IV, VB+DEMAND)

| Model | PESQ | STOI (%) |
|---|---|---|
| **SSE-Net** | **2.89** | **94.0** |
| w/o SFEB (→ plain LIF) | 2.70 | 93.5 |
| w/o ITB | 2.81 | 93.8 |
| ITB → Conv2D | 2.80 | 93.8 |

Both novel modules matter: the SFEB's residual spiking structure preserves critical info under binary input (+0.19 PESQ), and the ITB's gating refinement is worth +0.08–0.09 PESQ over removal or a plain Conv2D replacement.

### Main results — WSJ0-SI84+DNS (Table IX, causal, avg over −5/0/5 dB)

| Method | PESQ | ESTOI (%) | SI-SDR (dB) |
|---|---|---|---|
| Noisy | 1.85 | 43.30 | 0 |
| LSTM | 2.34 | 62.82 | 6.20 |
| CRN | 2.41 | 64.66 | 6.89 |
| DCCRN | 2.40 | 65.92 | 8.17 |
| GCRN | 2.50 | 70.45 | 9.25 |
| ConvTasNet | 2.52 | 72.25 | 10.21 |
| DPRNN | 2.57 | 73.34 | 10.43 |
| FullSubNet | 2.60 | 65.56 | 8.72 |
| Spiking-U-Net (SNN) | 2.44 | 61.82 | 6.69 |
| Wiener filtering | 2.03 | 52.39 | 3.09 |
| **SSE-Net** | **2.65** | 66.95 | 9.15 |

SSE-Net is the best SNN model and **exceeds every ANN baseline in this table on PESQ** (FullSubNet 2.60, DPRNN 2.57), though its ESTOI/SI-SDR lag the best time-domain ANN models (DPRNN 73.34% / 10.43 dB).

### Main results — VoiceBank+DEMAND (Table X, non-causal)

| Method | WB-PESQ | STOI (%) | CSIG | CBAK | COVL |
|---|---|---|---|---|---|
| Noisy | 1.97 | 92.1 | 3.35 | 2.44 | 2.63 |
| SEGAN | 2.16 | 92.5 | 3.48 | 2.94 | 2.80 |
| MMSE-GAN | 2.53 | 93.0 | 3.80 | 3.12 | 3.14 |
| Wavenet | — | — | 3.62 | 3.32 | 2.98 |
| MetricGAN | 2.86 | — | 3.99 | 3.18 | 3.42 |
| DCCRN | 2.68 | 93.7 | 3.88 | 3.18 | 3.27 |
| S4DSE | 2.55 | — | 3.94 | 3.00 | 3.32 |
| Spiking-U-Net (SNN) | 2.66 | 92.0 | — | — | — |
| Spiking-FullSubNet (SNN) | 2.79 | 93.7 | 3.96 | 3.26 | 3.29 |
| **SSE-Net** | **2.89** | **94.0** | **4.03** | **3.46** | **3.46** |

SSE-Net is **SOTA among SNN-SE models** and beats all listed ANN baselines on this benchmark (MetricGAN 2.86 WB-PESQ is closest). The authors note it still lags current *larger* ANN SOTA models (e.g., CMGAN-class), with the gap attributed to the inherent information capacity limit of 0/1 spike representations.

### Causal vs. non-causal (Table V)

| Model | Causal | PESQ | ESTOI (%) | SI-SDR (dB) |
|---|---|---|---|---|
| Noisy | — | 1.86 | 43.11 | 0 |
| SSE-Net | ✓ | 2.67 | 69.00 | 9.37 |
| SSE-Net | ✗ | 2.82 | 75.56 | 11.02 |

The causal version loses ~0.15 PESQ / ~6.6 pt ESTOI / ~1.7 dB SI-SDR but remains competitive — supporting real-time deployment claims.

### Complexity (Table VI, 1 s input, WSJ0)

| Model | PESQ | MACs |
|---|---|---|
| LSTM | 2.37 | 3.69 G/s |
| CRN | 2.45 | 2.54 G/s |
| GCRN | 2.55 | 2.40 G/s |
| FullSubNet | 2.64 | 29.83 G/s |
| ConvTasNet | 2.54 | 5.22 G/s |
| DPRNN | 2.60 | 8.47 G/s |
| Spiking-FullSubNet | — | 0.51 G/s |
| **SSE-Net** | **2.72** | **0.44 G/s** |

SSE-Net reports the lowest MACs of all baselines — an average **~17× reduction in computational complexity** vs. the ANN baselines.

### Energy (Table VII, Intel N-DNS metrics)

| Model | Power proxy (Ops/s) | PDP proxy (Ops) | Energy cost (J) |
|---|---|---|---|
| Microsoft NsNet2 | 136.13 M | 2.72 M | 12.51 μ |
| DCCRN | 5070 M | 100 M | 460 μ |
| FullSubNet | 3650 M | 120 M | 550 μ |
| Fast FullSubNet | 490 M | 20 M | 90 μ |
| CMGAN | 1594 M | 320 M | 1470 μ |
| CTDNN LAVADL* | 61.37 M | 1.96 M | 1.76 μ |
| PSNN* | 57.24 M | 1.83 M | 1.65 μ |
| Spiking-FullSubNet | 51.30 M | 1.64 M | 1.48 μ |
| **SSE-Net** | **19.70 M** | **0.63 M** | **1.31 μ** |

\* Intel N-DNS Challenge top-ranking systems (quoted from the official repository). SSE-Net's power proxy is **62% lower than Spiking-FullSubNet** (challenge winner) and its energy cost 11% lower; vs. ANN models it claims ~1% of their power at better performance.

### Listening test (Table VIII)

15 volunteers rated 12 real-world recorded samples (music, door opening, highway, background speech, keyboard noise, etc.) on a 1–5 MOS scale: **SSE-Net 3.78 ± 0.21** (p < 0.05) vs. Spiking-FullSubNet 3.21 ± 0.30 and Spiking-U-Net 2.49 ± 0.39.

![[raw/papers/liu-2026-sse-net/figures/bb5979219fcd97b078cd13105c722c587780f0a18f7248746d889346ab2a5abc.jpg|Spectrogram comparison]]

*Figure 3: Complex spectrograms — SSE-Net recovers more spectral detail (yellow box) than LSTM/GCRN baselines.*

![[raw/papers/liu-2026-sse-net/figures/8c739756b8d60dd35ac79ce876c82b3b5d8c78ce9603c218273829605661bbfe.jpg|Frame-wise SNR curves]]

*Figure 4: Frame-wise segmental SNR over 8 s — SSE-Net (red) never falls below 0 dB SNR and holds higher SNR density across frames than baselines.*

## Key Contributions

1. **First spike-native SNN-SE architecture**: all blocks (SFEB/SFEG/ITB) are designed from scratch for spike processing rather than reusing converted ANN modules — eliminating the structural redundancy, training difficulty, and information mismatch of ANN→SNN conversion.
2. **[[concepts/spiking-feature-extraction-block|SFEB/SFEG]]**: a residual three-branch spiking feature extraction group that converts features to spike streams while preserving a continuous residual path, alleviating information loss from discrete binary activation (+0.19 PESQ in ablation).
3. **[[concepts/information-transformation-block|Information Transformation Block]]**: a two-branch gated refinement stage converting discrete spike features back to continuous representations, recovering lost speech information (+0.08–0.09 PESQ; irreplaceable by plain Conv2D).
4. **SOTA SNN-SE performance at record-low power**: best results among all SNN-SE models on both benchmarks (WB-PESQ 2.89 on VB+DEMAND), with power proxy 19.70 M Ops/s (62% below Spiking-FullSubNet) and 0.44 G/s MACs (~17× below average ANN baseline), plus top MOS (3.78) in a real-world listening test.
5. **Surrogate-gradient training with Sigmoid proxy** for simple, efficient training (no conversion pipeline), and a clean causal/non-causal analysis supporting real-time deployment.

## Related Concepts

- [[concepts/sse-net|SSE-Net]] — main concept page for the architecture
- [[concepts/spiking-feature-extraction-block|Spiking Feature Extraction Block (SFEB/SFEG)]]
- [[concepts/information-transformation-block|Information Transformation Block (ITB)]]
- [[concepts/intel-neuromorphic-dns-challenge|Intel Neuromorphic DNS Challenge]] — source of the power-proxy / PDP evaluation metrics
- [[concepts/spiking-neural-networks|Spiking Neural Networks]] — the model family; LIF neurons and surrogate-gradient training
- [[concepts/neuromorphic-computing|Neuromorphic Computing]] — target deployment platform (Intel Loihi energy model)
- [[concepts/speech-enhancement|Speech Enhancement]] — the task
- [[concepts/voicebank-demand|VoiceBank+DEMAND]] — evaluation dataset
- [[concepts/dns-challenge|DNS Challenge]] — evaluation noise set / dataset
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]] — RI-stacked input representation
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — the ANN SE family most baselines (CRN/GCRN/DCCRN/FullSubNet) belong to
- [[concepts/dprnn|DPRNN]] — time-domain baseline

## Related Synthesis

- [[synthesis/computational-efficiency-evolution|Computational Efficiency Evolution]] — SSE-Net adds the **spiking low-power axis** (power proxy, neuromorphic deployment) to the lightweight-SE frontier alongside GTCRN/CoFi-Lite/AdaptCRN
