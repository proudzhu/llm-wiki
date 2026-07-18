---
type: source
created: 2026-06-06
updated: 2026-06-06
sources:
  - raw/papers/indenbom-2023-deepvqe/full-text.md
  - https://doi.org/10.48550/arXiv.2306.03177
  - zotero://select/items/0_WV7YKFHR
tags:
  - speech-enhancement
  - acoustic-echo-cancellation
  - noise-suppression
  - dereverberation
  - deep-learning
  - real-time
---

# Indenbom, Ristea, Saabas, Parnamaa, Guzvin & Cutler 2023: DeepVQE

| Field | Value |
|-------|-------|
| **Authors** | [[entities/evgenii-indenbom\|Evgenii Indenbom]], [[entities/nicolae-catalin-ristea\|Nicolae-Catalin Ristea]], [[entities/ando-saabas\|Ando Saabas]], [[entities/tanel-parnamaa\|Tanel Parnamaa]], [[entities/jegor-guzvin\|Jegor Guzvin]], [[entities/ross-cutler\|Ross Cutler]] |
| **Institution** | Microsoft Corp. |
| **Published** | arXiv preprint, 2023 |
| **Type** | Preprint |
| **DOI** | [10.48550/arXiv.2306.03177](https://doi.org/10.48550/arXiv.2306.03177) |
| **arXiv** | [2306.03177](https://arxiv.org/abs/2306.03177) |
| **Zotero** | [WV7YKFHR](zotero://select/items/0_WV7YKFHR) |

## Summary

DeepVQE is a real-time cross-attention deep model based on residual CNNs and GRUs that simultaneously performs acoustic echo cancellation (AEC), noise suppression (NS), and dereverberation (DR). It achieves state-of-the-art performance on both the ICASSP 2023 AEC Challenge and DNS Challenge non-personalized tracks with a single unified model, and has been deployed in Microsoft Teams.

![[raw/papers/indenbom-2023-deepvqe/figures/4263d5e9506cd39f591699d03ea5567267a2043f797c93ee92f572de72be0d5d.jpg|DeepVQE architecture overview]]
*Figure 1: DeepVQE architecture overview. The mic and far-end signals are processed through encoder branches, cross-attention alignment, GRU bottleneck, decoder with sub-pixel convolutions, and CCM block.*

## Problem Formulation

The system addresses joint AEC, NS, and DR in full-duplex communication:

- **Far-end reference** signal is played through a loudspeaker and picked up by the microphone via an acoustic echo path
- **Microphone signal** contains near-end speech, background noise, reverberations, and echoes
- **Goal**: A single model removes echoes, noise, and reverberation from the microphone signal

Input features are power-law compressed complex spectra computed with a squared-root Hann window at 24 kHz sampling rate.

## Methodology

### Overall Architecture

DeepVQE is a residual CNN autoencoder with a GRU bottleneck, consisting of:

1. **Encoder** — mic branch (5 blocks) and far-end branch (2 blocks + alignment block)
2. **Alignment block** — cross-attention soft alignment of mic and far-end features
3. **GRU bottleneck** — recurrent layer + linear projection
4. **Decoder** — 5 decoding blocks with sub-pixel convolutions
5. **CCM block** — complex convolving mask for output reconstruction

### Cross-Attention Alignment Block

Addresses the delay between microphone and far-end reference signals:

- Point-wise convolutions produce queries $\mathbf{Q} \in \mathbb{R}^{h \times t \times f}$ and keys $\mathbf{K} \in \mathbb{R}^{h \times t \times f}$
- Key is unfolded along time axis creating delay dimension: $\mathbf{K}_u \in \mathbb{R}^{h \times t \times d_{\max} \times f}$
- Dot product on frequency axis yields $\mathbf{Z} \in \mathbb{R}^{h \times t \times d_{\max}}$
- Convolutional layer ($5 \times 3$ kernel) combines $h$ similarity channels into single attention head
- Softmax on delay axis produces delay probability distribution $\mathbf{D} \in \mathbb{R}^{t \times d_{\max}}$
- Aligned far-end features computed as weighted sum with delay probabilities

Key innovation: convolutional layer in the time-delay map stabilizes the delay distribution and enhances AEC performance.

### Residual Block

$$\mathbf{Y} = \mathbf{X} + \text{ELU}(\text{BatchNorm}(\text{Conv2D}(\mathbf{X})))$$

where $\mathbf{X}, \mathbf{Y} \in \mathbb{R}^{c \times t \times f}$. Kernel size $4 \times 3$, stride 1, causal padding.

### Sub-Pixel Convolution

Replaces transposed convolution for upsampling in the decoder. Input $\mathbf{X} \in \mathbb{R}^{c_i \times t \times f}$ is transformed by convolution with $2c$ filters into $\mathbf{X}' \in \mathbb{R}^{2c \times t \times f}$, then transposed and reshaped into $\mathbf{Y} \in \mathbb{R}^{c \times t \times 2f}$. Each upscaling is by factor 2 on the frequency axis.

### Complex Convolving Mask (CCM) Block

Two-stage process:

**Stage 1** — Complex mask construction using three weight components at 120° in the complex plane:

$$\mathbf{v} = (v_1, v_2, v_3) = \left(1, -\frac{1}{2} + j\frac{\sqrt{3}}{2}, -\frac{1}{2} - j\frac{\sqrt{3}}{2}\right)$$

$$\mathbf{H} = \mathbf{v} \cdot \mathbf{X}'$$

**Stage 2** — Time-frequency varying convolution:

$$\hat{\mathbf{X}}(t, f) = \sum_{i=-m}^{0} \sum_{j=-n}^{n} \mathbf{X}(t+i, f+j) \cdot \mathbf{M}(i, j, t, f)$$

The CCM enables the network to estimate each T-F bin by mixing multiple neighbor bins in a learnable fashion. The three-vector component (vs. two-vector) provides more stable output, preventing low noise and echo leakage.

### Skip Block

Replaces classical skip connections with point-wise convolution ($1 \times 1$ kernel), decoupling encoder and decoder feature spaces and allowing independent channel counts.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Sampling rate | 24 kHz |
| Window | Squared-root Hann, 20 ms |
| Hop length | 10 ms |
| DFT length | 480 |
| Algorithmic delay | 20 ms |
| Max delay $d_{\max}$ | 100 frames (1 second) |
| Optimizer | AdamW |
| Learning rate | $1.2 \times 10^{-3}$ |
| Weight decay | $5 \times 10^{-7}$ |
| Batch size | 400 |
| Epochs | 250 |
| DeepVQE parameters | 7.5M |
| DeepVQE-S parameters | 0.59M |
| DeepVQE inference | 3.66 ms/frame (i7-11370H) |
| DeepVQE-S inference | 0.14 ms/frame (RTF 0.014) |

Training data synthesized online from clean/noisy speech with random parameters (SNR, RIR, distortion, gain, SER, etc.) from ICASSP 2022 AEC and DNS challenges.

## Results

### ICASSP 2023 DNS Challenge (Non-Personalized)

| Method | SIG | BAK | OVRL | WAcc | Final |
|--------|-----|-----|------|------|-------|
| DNS Baseline | 3.14 | 2.60 | 2.34 | 70.7% | 0.521 |
| DNS Winner | 3.58 | 2.82 | 2.65 | 72.5% | 0.569 |
| **DeepVQE** | **3.47** | **2.94** | **2.73** | **73.4%** | **0.582** |

### ICASSP 2023 AEC Challenge (Non-Personalized)

| Method | ST FE Echo | DT Echo | DT Other | ST NE | SIG | BAK | WAcc | Final |
|--------|-----------|--------|----------|-------|-----|-----|------|-------|
| AEC Baseline | 4.53 | 4.28 | 3.47 | 3.88 | 3.88 | — | 64.9% | 0.736 |
| AEC Winner | 4.70 | 4.77 | 4.31 | 3.99 | 4.38 | — | 82.3% | 0.852 |
| DeepVQE-S | 4.66 | 4.63 | 4.00 | 4.04 | 4.33 | — | 75.7% | 0.821 |
| **DeepVQE** | **4.69** | **4.70** | **4.29** | **4.15** | **4.41** | — | **80.7%** | **0.854** |

### Key Ablation Findings

- **Alignment block**: Surpasses both DSP-based alignment and prior cross-attention method across all metrics, especially WER
- **CCM block**: Provides the largest improvement for NS task; leverages magnitude and phase from neighboring T-F bins
- **Dereverberation**: Over 10 dB SRR improvement on both AEC-NEST and DNS data
- **Same model** handles both AEC and DNS challenges — winners use separate task-specific models

## Key Contributions

1. New cross-attention mechanism for microphone/far-end soft alignment in feature space with convolutional stabilization of the delay distribution
2. Architecture efficiently combining alignment block, residual blocks, CCM, and sub-pixel convolution for joint AEC, NS, and DR
3. State-of-the-art on both ICASSP 2023 AEC Challenge (final score 0.854, rank 1) and DNS Challenge (final score 0.582) with a single unified model
4. DeepVQE-S (0.59M params, RTF 0.014) deployed in Microsoft Teams for hundreds of millions of users

## Related Concepts

- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/cross-attention-alignment|Cross-Attention Alignment]]
- [[concepts/complex-convolving-mask|Complex Convolving Mask]]
- [[concepts/sub-pixel-convolution|Sub-Pixel Convolution]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask]]

## Related Sources

- [[sources/tan-2018-convolutional-recurrent-network-speech-enhancement|Tan & Wang 2018: CRN for Speech Enhancement]]
- [[sources/wang-2018-supervised-speech-separation-deep-learning-overview|Wang & Chen 2018: Supervised Speech Separation Survey]]
- [[sources/li-2025-echofree-neural-aec|Li et al. 2025: EchoFree]] — DeepVQE-S serves as the upper-bound SOTA comparison for this 278K-parameter PercepNet-style AEC model
- [[sources/castelli-2025-embedded-joint-aec-ns|Castelli 2024: Embedded Joint AEC and NS]] — NXP industrial deployment that re-implements DeepVQE-s at 16 kHz and compresses it through a six-stage pipeline to [[concepts/tinyvqe|TinyVQE]] (114k params, 0.48 MMACs/frame, 2.32 ms / 16 ms on a Cadence HiFi4 DSP)
