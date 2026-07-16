---
type: source
created: 2026-07-17
updated: 2026-07-17
sources:
  - raw/papers/li-2025-echofree-neural-aec/full-text.md
  - https://doi.org/10.48550/arXiv.2508.06271
  - zotero://select/items/0_RPUN2SVZ
tags:
  - acoustic-echo-cancellation
  - speech-enhancement
  - low-complexity
  - deep-learning
  - self-supervised-learning
  - bark-scale
  - hybrid-aec
---

# Li, Kang, Wang, Zhang, Liu, Fu & Xie 2025: EchoFree — Ultra Lightweight Neural AEC

| Field | Value |
|-------|-------|
| **Authors** | [[entities/xingchen-li\|Xingchen Li]]<sup>†</sup>, [[entities/boyi-kang\|Boyi Kang]]<sup>†</sup>, [[entities/ziqian-wang\|Ziqian Wang]], [[entities/zihan-zhang\|Zihan Zhang]], [[entities/mingshuai-liu\|Mingshuai Liu]], [[entities/zhonghua-fu\|Zhonghua Fu]]<sup>*</sup>, [[entities/lei-xie\|Lei Xie]] |
| **Institution** | Audio, Speech and Language Processing Group (ASLP@NPU), School of Computer Science, Northwestern Polytechnical University, Xi'an, China |
| **Published** | arXiv preprint, 8 Aug 2025 |
| **Type** | Preprint |
| **DOI** | [10.48550/arXiv.2508.06271](https://doi.org/10.48550/arXiv.2508.06271) |
| **arXiv** | [2508.06271](https://arxiv.org/abs/2508.06271) |
| **Zotero** | [RPUN2SVZ](zotero://select/items/0_RPUN2SVZ) |

<sup>†</sup> Equal contribution. <sup>*</sup> Corresponding author.

## Summary

**EchoFree** is an ultra-lightweight neural acoustic echo cancellation (AEC) framework that cascades a partitioned-block frequency-domain adaptive Kalman filter (linear AEC) with a U-Net-style neural post filter operating on Bark-scale spectral features. With only **278K parameters** and **30 MMACs/s** of compute, it matches or exceeds the performance of state-of-the-art lightweight model DeepVQE-S (0.82M params, 315 MMACs/s) on the ICASSP 2023 AEC Challenge blind test set. A two-stage training strategy based on WavLM-Large self-supervised (SSL) embeddings is introduced: stage 1 uses only SSL loss to learn coarse spectral representations; stage 2 combines a perceptually motivated Bark-scale gain loss with SSL loss for fine-grained refinement.

![[raw/papers/li-2025-echofree-neural-aec/figures/8573cf52d1668f2e976a690b336b433d020544162e23d61fa94fe79faf9e30bc.jpg|EchoFree hybrid AEC system overview]]
*Figure 1: EchoFree hybrid approach combining a linear acoustic echo canceller with a neural post filter for residual echo suppression.*

## Problem Formulation

Full-duplex communication scenario: the far-end signal $x(n)$ is played through a loudspeaker, undergoes room reflections and hardware nonlinearities, and is recaptured by the near-end microphone together with the near-end speech $s(n)$:

$$
y(n) = s(n) + e(n) \tag{1}
$$

where $e(n)$ is the acoustic echo. The objective is to recover $s(n)$ given $y(n)$ and $x(n)$. EchoFree uses a cascaded linear filter + neural post filter:

$$
\begin{aligned}
z(n) &= y(n) - \hat{e}(n) \\
     &= s(n) + \underbrace{\{e(n) - \hat{e}(n)\}}_{r(n)}
\end{aligned} \tag{2}
$$

The linear filter estimates the echo $\hat{e}(n)$, producing residual signal $z(n)$ that still contains residual echo $r(n)$. The neural post filter takes $\{y(n), \hat{e}(n)\}$ and predicts a Bark-scale gain mask to suppress $r(n)$.

## Methodology

### Linear Filtering Front-end

EchoFree uses the **partitioned-block frequency-domain adaptive Kalman filter** of Kuech, Mabande & Enzner (ICASSP 2014) — the same family of [[concepts/frequency-domain-kalman-filter\|frequency-domain Kalman filters]] used in hybrid AEC pipelines. Configuration: 10 partitions, FFT length 256.

### Neural Post Filter Architecture

The neural post filter (Fig. 2) has three components:

**1. Bark-scale Feature Extractor** — STFT (window 512, hop 256, FFT 512 → 257 bins) is computed for $y(n)$ and $\hat{e}(n)$. The magnitude spectrum is multiplied by a mapping matrix $\mathbf{B}$ mapping 257 linear bins to **100 Bark-scale bands**, then log-compressed. Following Ma et al. (2020), first- and second-order derivatives of the first 6 features are concatenated, giving a final input dimension of $D = 112$.

![[raw/papers/li-2025-echofree-neural-aec/figures/b6324b6c8293570da7e81f812f8384d1f1659efbaa127521b28ba7c463742fbd.jpg|Neural post filter overall architecture]]
![[raw/papers/li-2025-echofree-neural-aec/figures/8b8930707d3046e87f06645f46c04886757eef4957f8073387c11145d4b84612.jpg|Bark-scale feature extractor and decoder layer]]
*Figure 2: Neural post filter architecture. (a) Overall pipeline with two encoder branches (mic + echo), bottleneck GRU, and 4-stage decoder. (b) Bark-scale feature extractor. (c) Decoder layer with skip block, sub-pixel convolution, and optional residual block.*

**2. U-Net Backbone** — A two-branch encoder + bottleneck + decoder:
- **Mic branch encoder**: 4 [[concepts/depthwise-separable-convolution\|depthwise separable convolution]] layers, filter sizes (8, 16, 24, 32), kernel (4, 3), stride (4, 3).
- **Echo branch encoder**: single depthwise separable conv layer, 8 filters. Its output is concatenated with mic-branch features.
- **Bottleneck**: unidirectional [[concepts/gtcrn\|GRU]] (192 units) + linear layer (192 units). Chosen over LSTM for efficiency.
- **Decoder**: 4 decoder modules (filter sizes 24, 16, 8, 1), each using [[concepts/sub-pixel-convolution\|SubPixelConv]] for upsampling and skip-block mechanism (point-wise $1{\times}1$ conv) for skip connections. The last module additionally includes a residual block.
- **Output head**: final linear layer + sigmoid → Bark-scale gain $\hat{\mathbf{g}} \in [0, 1]^{100}$.

BatchNorm + ELU activations are applied throughout.

**3. Post-processing** — The predicted Bark gain $\hat{\mathbf{g}}$ is multiplied by $\mathbf{B}^\top$ to expand back to 257-bin magnitude mask, which is then multiplied by $|Y|$ to obtain the estimated near-end magnitude spectrum.

### Two-Stage Training Strategy with SSL Loss

The key training innovation is a **two-stage optimization** leveraging WavLM-Large [[concepts/self-supervised-speech-representation\|self-supervised speech representations]] (frozen during training).

![[raw/papers/li-2025-echofree-neural-aec/figures/8337a47c39c70c0f4ddbe1d0cdd5213c4f08c95b92ead6a664f46ca01cf211f3.jpg|Two-stage training strategy]]
*Figure 3: Stage 1 uses only SSL loss; stage 2 combines Bark-scale gain loss with SSL loss. WavLM parameters are frozen.*

**SSL loss** (stage 1): MSE between WavLM embeddings of estimated and ground-truth signals, averaged over all $L$ layers:

$$
\mathcal{L}_{SSL} = \frac{1}{L} \sum_{l=1}^{L} \| \mathbf{e}_l - \hat{\mathbf{e}}_l \|^2 \tag{3}
$$

**Bark-scale gain loss** (stage 2): penalizes both squared and quartic root-mean discrepancies between predicted gain $\hat{\mathbf{g}}$ and target gain $\mathbf{g}$, plus a small cross-entropy regularization:

$$
\begin{aligned}
\mathcal{L}_{Bark} = &\, 10(|\hat{\mathbf{g}}|^c - |\mathbf{g}|^c)^4 + (|\hat{\mathbf{g}}|^c - |\mathbf{g}|^c)^2 \\
                    &+ 0.01 \cdot \mathrm{CrossEntropy}(\hat{\mathbf{g}}, \mathbf{g})
\end{aligned} \tag{4}
$$

with compression coefficient $c = 0.5$. The fourth-order term emphasizes large perceptual errors; the second-order term provides general stability; cross-entropy adds distributional regularization.

**Stage objectives**:

$$
\mathcal{L}_{\text{stage-1}} = \mathcal{L}_{SSL} \tag{5}
$$

$$
\mathcal{L}_{\text{stage-2}} = 10 \cdot \mathcal{L}_{Bark} + 0.5 \cdot \mathcal{L}_{SSL} \tag{6}
$$

In stage 2 the SSL loss acts as a regularization term preserving representation fidelity while the model is fine-tuned toward better Bark-scale gain prediction.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Sampling rate** | 16 kHz |
| **STFT window / hop / FFT** | 512 / 256 / 512 (257 bins) |
| **Bark-scale bands** | 100 |
| **Input feature dim** | 112 (100 Bark + 6×2 derivatives) |
| **Linear filter** | Partitioned-block frequency-domain adaptive KF, 10 partitions, FFT 256 |
| **Encoder kernels / strides** | (4, 3) / (4, 3) |
| **Mic encoder filters** | 8, 16, 24, 32 |
| **Echo encoder filters** | 8 |
| **GRU units** | 192 |
| **Decoder filters** | 24, 16, 8, 1 |
| **Parameters** | **0.28M (278K)** |
| **Compute** | **30 MMACs/s** |
| **Optimizer** | Adam, lr $10^{-3}$ → $10^{-5}$ (×0.5 on plateau, patience 5) |
| **Batch size / segment** | 128 / 10 s |
| **Early stop patience** | 10 epochs (each stage) |

### Training Data

Synthesized dynamically from clean speech of [[concepts/dns-challenge\|ICASSP 2021 DNS Challenge]]: ~90K samples / 573 h total, split 80K (506 h) train + 10K (67 h) val. Per-instance random parameters:

- Near-end: convolved with randomly selected RIR
- Far-end: nonlinear distortion → RIR convolution → time delay 10–512 ms
- Signal-to-echo ratio (SER): −15 to +15 dB
- Near-end speech zeroed with 10% probability (simulates far-end single talk)

### Evaluation

**Test set**: ICASSP 2023 AEC Challenge blind test set — 800 samples (300 double-talk, 300 far-end single-talk, 200 near-end single-talk). Audio resampled to 16 kHz for inference, then upsampled to 48 kHz for scoring.

**Metric**: [[sources/indenbom-2023-deepvqe\|AECMOS]] (Purin et al., ICASSP 2022) — two scores:
- **EchoMOS**: echo cancellation quality
- **DegMOS**: near-end speech preservation quality
- Reported separately for single-talk far-end (ST FE), single-talk near-end (ST NE), and double-talk (DT)

## Results

### Comparison with State-of-the-Art Low-Complexity AEC (Table I)

| Method | # Param. | MACs/s | ST FE EchoMOS | ST NE DegMOS | DT EchoMOS | DT DegMOS |
|--------|---------:|-------:|--------------:|-------------:|-----------:|----------:|
| ULCNet-AER [[sources/shetu-2024-hybrid-low-complexity-aenr\|Shetu 2024]] | 1.12M | 173M | 2.89 | 3.04 | 2.68 | 3.77 |
| Bark-AEC (Seidel et al. ICASSP 2024) | 1.62M | 107M | 3.16 | 2.83 | 2.96 | 3.27 |
| DeepVQE-S [[sources/indenbom-2023-deepvqe\|Indenbom 2023]] | 0.82M | 315M | 4.13 | 3.24 | 3.96 | 3.69 |
| Linear AEC only | — | — | 2.91 | 3.02 | 2.68 | 3.76 |
| EchoFree — cost loss only | **0.28M** | **30M** | 4.15 | 3.13 | 3.74 | 3.52 |
| EchoFree — SSL loss only | **0.28M** | **30M** | 4.15 | 3.18 | 3.91 | 3.46 |
| **EchoFree — proposed (two-stage)** | **0.28M** | **30M** | **4.20** | **3.27** | **3.88** | **3.53** |

### Key Findings

1. **EchoFree-proposed outperforms ULCNet-AER and Bark-AEC** by a wide margin across all four metrics, at **4× fewer parameters** and **3.6–5.8× less compute**.
2. **Matches or surpasses DeepVQE-S**: EchoFree wins on ST FE EchoMOS (4.20 vs 4.13) and ST NE DegMOS (3.27 vs 3.24), with small trade-offs in DT metrics — while using **2.9× fewer parameters** and **10.5× less compute**.
3. **SSL loss alone beats conventional gain loss** on DT EchoMOS (3.91 vs 3.74), confirming that SSL embeddings carry rich acoustic/semantic information beneficial for residual echo suppression.
4. **Two-stage training is the best overall**: stage-2 fine-tuning improves ST FE EchoMOS (4.20), ST NE DegMOS (3.27), and DT DegMOS (3.53) over SSL-only, at a small cost in DT EchoMOS (3.88 vs 3.91).
5. **All NN configurations beat linear AEC only**, confirming the value of the neural post filter even at ultra-low complexity.

### Two-Stage Visualization (Fig. 4)

Stage-1 output (SSL-only) suppresses echo but introduces spectral distortions, particularly in high-frequency regions. Stage-2 fine-tuning substantially mitigates these distortions, validating the progressive coarse-to-fine learning hypothesis.

## Key Contributions

1. **Ultra-lightweight hybrid AEC architecture**: 278K params / 30 MMACs/s — to our knowledge the smallest model achieving DeepVQE-S-comparable AEC performance on ICASSP 2023 AEC Challenge blind set.
2. **U-Net neural post filter on Bark-scale features**: replaces the FC+GRU baseline of prior Bark-AEC (Ma 2020 / Seidel 2024) with a two-branch encoder + GRU bottleneck + sub-pixel-conv decoder, achieving better performance at smaller compute.
3. **Two-stage SSL training strategy**: stage-1 WavLM-Large embedding loss for coarse spectral learning, stage-2 weighted combination of perceptual Bark-scale gain loss + SSL loss for fine-grained refinement. WavLM remains frozen throughout.
4. **Comprehensive ablation** isolating the contributions of (a) the neural post filter, (b) conventional gain loss vs SSL loss, and (c) the two-stage combination — showing each component adds measurable benefit.

## Related Concepts

- [[concepts/acoustic-echo-cancellation\|Acoustic Echo Cancellation]]
- [[concepts/bark-scale-spectral-features\|Bark-Scale Spectral Features]]
- [[concepts/u-net-post-filter\|U-Net Post Filter]]
- [[concepts/self-supervised-speech-representation\|Self-Supervised Speech Representation]]
- [[concepts/percepnet-style-neural-post-filter\|PercepNet-Style Neural Post Filter]]
- [[concepts/frequency-domain-kalman-filter\|Frequency-Domain Kalman Filter]]
- [[concepts/depthwise-separable-convolution\|Depthwise Separable Convolution]]
- [[concepts/sub-pixel-convolution\|Sub-Pixel Convolution]]
- [[concepts/ulcnet\|ULCNet]]
- [[concepts/dns-challenge\|DNS Challenge]]
- [[concepts/speech-enhancement\|Speech Enhancement]]
- [[concepts/adaptive-filtering\|Adaptive Filtering]]

## Related Sources

- [[sources/indenbom-2023-deepvqe\|Indenbom et al. 2023: DeepVQE]] — primary SOTA comparison (DeepVQE-S)
- [[sources/shetu-2024-hybrid-low-complexity-aenr\|Shetu et al. 2024: Hybrid Low-Complexity AENR]] — ULCNet-AER baseline for low-complexity AEC
- [[sources/enzner-2006-fdakf-echo-control\|Enzner 2006: FDAKF Echo Control]] — foundational work on frequency-domain adaptive Kalman filtering for AEC

## Related Synthesis

- [[synthesis/joint-multitask-ultra-low-latency-se\|Joint Multi-Task SE & Ultra-Low-Latency Paradigm]] — EchoFree extends the low-complexity AEC frontier at 30 MMACs/s, sitting below DeepVQE-S (315 MMACs/s) and ULCNet-AER (173 MMACs/s) on the efficiency axis.
