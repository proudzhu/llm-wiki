---
type: source
created: 2026-08-03
updated: 2026-08-03
sources:
  - raw/papers/jiang-2026-lightweight-speech-enhancement-ssm-dsc/full-text.md
  - https://doi.org/10.1016/j.dsp.2026.105987
  - zotero://select/items/0_WNWMR26M
tags:
  - speech-enhancement
  - state-space-model
  - lightweight-framework
  - depthwise-separable-convolution
  - erb-scale
  - classifier-loss
  - multi-scale-feature-learning
---

# Jiang, Gao, Wang, Zou & Liu 2026: Lightweight Speech Enhancement with State-Space Model and Depthwise Separable Convolution

- **Authors**: [[entities/chen-jiang|Chen Jiang]]<sup>a,1</sup>, [[entities/dai-gao|Dai Gao]]<sup>b,1</sup>, [[entities/sirui-wang|Sirui Wang]]<sup>a</sup>, [[entities/chengxuan-zou|Chengxuan Zou]]<sup>a</sup>, [[entities/jie-liu|Jie Liu]]<sup>a,*</sup>
- **Institutions**: <sup>a</sup> School of Computer Science and Technology, Beijing Jiaotong University, Beijing, China · <sup>b</b> School of Future Science and Engineering, Soochow University, Suzhou, China
- **Venue**: *Digital Signal Processing* (Elsevier), Vol. 157, 2026
- **Published**: 2026-04-15
- **DOI**: [10.1016/j.dsp.2026.105987](https://doi.org/10.1016/j.dsp.2026.105987)
- **Zotero**: [WNWMR26M](zotero://select/items/0_WNWMR26M)
- **Type**: Journal article

## Summary

The paper proposes a lightweight monaural speech enhancement framework that pairs a **diagonal-constrained S4 state-space model (lightS4)** with **depthwise separable convolutions** and an **Auditory-Inspired Spectral Compressor (AISC)**. With only **1.65 M parameters and 0.50 G MACs** (RTF = 0.13 on an Intel Core i5-1135G7 CPU), the model reaches **PESQ 3.32 / STOI 0.96 on VoiceBank+DEMAND** and **PESQ 3.01 / STOI 0.87 on WSJ0-SI84** (SOTA among lightweight models). Relative to [[concepts/semamba|SEMamba]] (32.73 G MACs, PESQ 3.52), it cuts MACs by **≈60×** at a 0.20 PESQ cost, defining a new efficiency–quality trade-off point on the lightweight-SE Pareto frontier. A novel **Classifier Loss** with an auxiliary speaker-classification head suppresses competing human-voice interference, and a parameter-free **Griffin–Lim Algorithm** phase post-processor avoids the parameter burden of learned complex-domain decoders.

## Problem Formulation

The paper targets the fundamental trade-off in monaural speech enhancement between **perceptual quality** and **computational complexity**. High-performing SOTA architectures such as FullSubNet (~30 G MACs) and [[concepts/semamba|SEMamba]] (32.73 G MACs) are prohibitive for real-time deployment on phones and TWS earbuds, while CNN-only models have limited global context and Transformer-based models incur quadratic attention cost.

The input noisy waveform $y \in \mathbb{R}^{L}$ is transformed via STFT (400-pt Hann window, 100-pt hop, 16 kHz) into magnitude $X_m$ and phase $X_p$ spectra. After power-law compression $(X_m)^c$ ($c = 0.5$), the framework estimates an enhanced magnitude $\hat{X}_m$ and reconstructs the time-domain waveform via iSTFT using a Griffin–Lim-refined phase $\hat{X}_p$:

$$
\hat{y} = \mathrm{iSTFT}\left(\hat{X}_m \odot e^{j \cdot \hat{X}_p}\right)
$$

The mask-prediction objective is augmented with a **Classifier Loss** $\mathcal{L}_{\mathrm{Classifier}}$ that enforces feature discriminability across speakers during training, treating speakers as unseen at inference.

## Methodology

The framework is a six-stage pipeline: **STFT → power-law compression → AISC → DSConv2D encoder with ASPP → dual-path lightS4 Featuremask → DSConv2D decoder + Griffin–Lim phase refinement → iSTFT**.

![[raw/papers/jiang-2026-lightweight-speech-enhancement-ssm-dsc/figures/ff875a6867c7bf1a01fa80eee895c90cad7982890fb4c94c46a8f111e4a3ed21.jpg|Overall architecture]]
*Figure 1: Overall architecture of the proposed model. STFT magnitude is power-law compressed, ERB-compressed by AISC, encoded by a depthwise-separable-convolution + ASPP encoder, masked by a dual-path lightS4 module, and reconstructed by a depthwise-separable decoder followed by Griffin–Lim phase refinement.*

### Auditory-Inspired Spectral Compressor (AISC)

A **parameter-free** module that splits the magnitude spectrum at 1.5 kHz: the low-frequency band $X_{\mathrm{low}}$ (containing harmonics/formants) is preserved at full resolution, while the high-frequency band $X_{\mathrm{high}}$ is projected onto the [[concepts/erb-scale|ERB scale]] via a fixed triangular filter bank $W_{\mathrm{ERB}} \in \mathbb{R}^{F_{\mathrm{ERB}} \times F_H}$, reducing frequency dimension from $F$ to $F' = F_L + F_{\mathrm{ERB}}$. The decoder inverts the projection via $W_{\mathrm{ERB}}^T$. This "expert-driven" reduction directly cuts encoder MACs (which scale linearly with input size) without adding parameters.

### Depthwise Separable Convolutional Encoder with ASPP

![[raw/papers/jiang-2026-lightweight-speech-enhancement-ssm-dsc/figures/de533e055e2b152c8b04f30f9da02c1186b2db125d0494093f1812be3f749e6d.jpg|Encoder module]]
*Figure 2: Encoder module — six cascaded DSConv2D blocks with progressive channel expansion, followed by an ASPP module with dilation rates {2, 4, 8}.*

The encoder is built from [[concepts/depthwise-separable-convolution|depthwise separable convolutions (DSConv2D)]]: six cascaded blocks with progressive channel expansion. An **Atrous Spatial Pyramid Pooling (ASPP)** module uses atrous depthwise separable convolutions (ADSConv2D) with dilation rates $r \in \{2, 4, 8\}$ specifically chosen to match speech spectro-temporal structure — $r{=}2$ for fine harmonics, $r{=}4$ for formant envelopes, $r{=}8$ for syllabic-level context. Three hierarchical features (low/mid/high) are channel-aligned and concatenated, producing $X_{\mathrm{Enc}} \in \mathbb{R}^{B \times C \times F'' \times T'}$.

### Dual-Path lightS4 Featuremask

![[raw/papers/jiang-2026-lightweight-speech-enhancement-ssm-dsc/figures/7d698405444122c6f08b2a837a3b05cc8ae009af0e2fed7c68659c8f7a448038.jpg|Featuremask module]]
*Figure 3: Featuremask module — dual-path lightS4 processing along time and frequency axes, fused via cross-gating.*

![[raw/papers/jiang-2026-lightweight-speech-enhancement-ssm-dsc/figures/bd18312ebe3d148dbedc475be5801c8d64af5c7312ddad20f5e3150565720470.jpg|lightS4 module]]
*Figure 4: Internal architecture of the [[concepts/lights4|lightS4]] module.*

The Featuremask introduces **[[concepts/lights4|lightS4]]**, a diagonal-constrained variant of the structured state-space model (S4). The transition matrix is parameterized as $\mathbf{A} = -\mathrm{diag}(\exp(\mathbf{A}_{\log}))$, guaranteeing stable negative eigenvalues. This diagonal structure allows Zero-Order Hold (ZOH) discretization to simplify to element-wise operations:

$$
\overline{\mathbf{A}} = \exp(\Delta \mathbf{A}) = \mathrm{diag}\left(\exp(\Delta \mathbf{A}_{11}), \ldots, \exp(\Delta \mathbf{A}_{HH})\right)
$$

$$
\overline{\mathbf{B}} = (\overline{\mathbf{A}} - \mathbf{I}) \odot \mathbf{A}^{-1} \odot \mathbf{B}
$$

The full SSM convolution kernel $\mathbf{K} \in \mathbb{R}^{C \times L}$ is computed in a single vectorized step and applied as a global FFT convolution, avoiding iterative recurrence. The dual-path architecture processes time and frequency axes independently and fuses them via a cross-gating mechanism:

$$
G_{\mathrm{time}} = \sigma(Y_{\mathrm{time}} + b_t), \quad G_{\mathrm{freq}} = \sigma(Y_{\mathrm{freq}} + b_f)
$$

$$
Y_{\mathrm{fused}} = (Y_{\mathrm{time}} \odot G_{\mathrm{freq}}) + (Y_{\mathrm{freq}} \odot G_{\mathrm{time}})
$$

The final mask $M = \sigma(Y_{\mathrm{fused}})$ is applied element-wise: $X_{\mathrm{mask}} = X_{\mathrm{Enc}} \odot M$.

### Decoder and Griffin–Lim Phase Refinement

The decoder alternates DSConv2D with transposed convolutions (DSTransConv2D) over five layers to reconstruct $\hat{X}_m$, with a final ReLU ensuring non-negative outputs. Phase is refined by the **Griffin–Lim Algorithm (GLA)** — a parameter-free iterative algorithm — rather than a learned complex-domain decoder. GLA iterates $K = 3$ times between (i) combining $\hat{X}_m$ with the current phase estimate, (ii) iSTFT to time domain, (iii) re-deriving phase via $\angle\mathrm{STFT}$. This choice avoids the parameter and MACs surge of learned phase decoders while improving perceptual quality over noisy-phase baselines.

### Metric Discriminator

A metric discriminator inspired by MSLD-SENet learns a differentiable proxy of PESQ through adversarial training. It takes pairs of complex spectrograms (real+imag concatenated), uses spectrally-normalized DSConv2D + instance normalization + parametric activations, and maps via adaptive pooling + FC layers to a normalized quality score in $[0, 1]$.

### Loss Function

The total generator loss combines five components:

$$
\mathcal{L}_G = \lambda_1 \mathcal{L}_{\mathrm{Mag}} + \lambda_2 \mathcal{L}_{\mathrm{Con}} + \lambda_3 \mathcal{L}_{\mathrm{Com}} + \lambda_4 \mathcal{L}_{\mathrm{Metric}} + \lambda_5 \mathcal{L}_{\mathrm{Classifier}}
$$

with weights $(\lambda_1, \lambda_2, \lambda_3, \lambda_4, \lambda_5) = (0.9, 0.1, 0.1, 0.05, 0.1)$. The **[[concepts/classifier-loss|Classifier Loss]]** is a cross-entropy loss over an auxiliary speaker classifier (two FC layers + softmax) attached to the masked features; it acts as both (a) explicit speaker-discriminative guidance under vocal interference (an "acoustic anchor" grouping coherent spectral components) and (b) a structural regularizer that prioritizes reconstruction of human-speech harmonic structure over stationary environmental noise.

## Experimental Setup

| Aspect | Configuration |
|---|---|
| **Sample rate** | 16 kHz (resampled from 48 kHz) |
| **STFT** | 400-pt Hann window, 100-pt hop, 400-pt FFT |
| **Training segments** | 2-s clips (test: untruncated) |
| **Optimizer** | Adam, lr = $5 \times 10^{-4}$, exp decay ×0.99/epoch |
| **Epochs** | 150, batch size 32 |
| **Hardware** | Single NVIDIA A800 GPU |
| **Inference hardware** | Intel Core i5-1135G7 @ 2.4 GHz CPU |
| **Datasets** | VoiceBank+DEMAND (11,572 train / 824 test), WSJ0-SI84 (92 spk train, 48 spk test), LibriSpeech (1,200 train / 300 test), ICASSP SSI 2023+2024 (1,500 real recordings) |
| **Metrics** | PESQ, STOI, CSIG, CBAK, COVL, SigMOS (OVRL/SIG/BAK/COL/DISC/REVERB/LOUD), MACs, Params, RTF |
| **Baselines (VB+DEMAND)** | FullSubNet, DeepFilterNet/2/3, SSI-Net, S4NDU-Net, Dual-S4D, DPHT-ANetD, MFFR-Net, CTSE-Net, [[concepts/semamba|SEMamba]], Spiking-S4, Unet16, DeConformer-SENet |
| **Baselines (WSJ0-SI84)** | FullSubNet, CTSNet, GaGNet, MDNet, CDNN-GRU, E-CDNN-GRU, BSDB-Net |

## Results

### VoiceBank+DEMAND (Table 1, selected rows)

| Model | Year | Params (M) | MACs (G) | PESQ | STOI | CSIG | CBAK | COVL |
|---|---|---|---|---|---|---|---|---|
| Noisy | – | – | – | 1.97 | 0.91 | 3.35 | 2.44 | 2.63 |
| [[sources/schroter-2022-deepfilternet|DeepFilterNet]] | 2022 | 1.78 | 0.35 | 2.81 | 0.94 | 4.14 | 3.31 | 3.46 |
| DeepFilterNet3 | 2023 | 2.31 | 0.36 | 3.17 | 0.94 | 4.34 | 3.61 | 3.77 |
| S4NDU-Net | 2023 | 0.75 | – | 3.15 | – | 4.52 | 3.62 | 3.85 |
| Dual-S4D | 2023 | 10.8 | 18.43 | 2.55 | 0.93 | 3.94 | 3.00 | 3.23 |
| [[sources/chao-2024-mamba-speech-enhancement|SEMamba]] | 2024 | 2.25 | 32.73 | 3.52 | 0.96 | 4.75 | 3.98 | 4.26 |
| Spiking-S4 | 2024 | 0.53 | 0.75 | 3.39 | – | 4.92 | 2.64 | 4.31 |
| Unet16 | 2025 | 1.10 | 2.27 | 3.17 | 0.95 | 4.49 | 3.79 | 3.90 |
| DeConformer-SENet | 2025 | 1.57 | 3.05 | 3.24 | 0.96 | 4.51 | 3.84 | 3.92 |
| **Proposed** | **2026** | **1.65** | **0.50** | **3.32** | **0.96** | **4.70** | **3.41** | **4.10** |

### WSJ0-SI84 (Table 2, +5 dB SNR, multi-talker noise)

| Model | Year | Params (M) | MACs (G) | PESQ | STOI |
|---|---|---|---|---|---|
| FullSubNet | 2021 | 5.64 | 31.35 | 2.55 | 0.74 |
| E-CDNN-GRU | 2023 | 2.01 | 0.65 | 2.91 | 0.85 |
| BSDB-Net | 2024 | 9.78 | 1.68 | 2.92 | 0.85 |
| **Proposed** | **2026** | **1.65** | **0.50** | **3.01** | **0.87** |

### Real-Time Factor

RTF = **0.13** on Intel Core i5-1135G7 @ 2.4 GHz CPU — confirming real-time suitability on consumer-grade hardware.

### SigMOS on ICASSP SSI Test Set (Table 9)

| Method | OVERALL | OVRL | SIG | BAK | COL | DISC | REVERB | LOUD |
|---|---|---|---|---|---|---|---|---|
| Noisy | 0.411 | 2.361 | 2.927 | 3.219 | 2.728 | 3.733 | 3.652 | 2.903 |
| DeepFilterNet3 | 0.632 | 3.351 | 3.706 | 4.261 | 3.644 | 4.267 | 4.238 | 4.185 |
| SSI-Net | 0.608 | 3.231 | 3.635 | 4.577 | 3.550 | 4.140 | 4.322 | 4.060 |
| aTENNuate | 0.553 | 3.027 | 3.400 | 3.899 | 3.485 | 3.975 | 4.136 | 3.764 |
| **Proposed** | **0.657** | **3.424** | **3.775** | 3.913 | 3.618 | **4.323** | **4.336** | 4.188 |

Highest OVERALL, OVRL, SIG, DISC, and REVERB; BAK is intentionally lower than aggressive suppressors (SSI-Net 4.577, DeepFilterNet3 4.261) due to a deliberate design trade-off prioritizing speech naturalness over aggressive noise removal.

### Ablation Highlights (Table 3, selected rows)

| Variant | Params (M) | MACs (G) | PESQ | STOI |
|---|---|---|---|---|
| Full proposed | 1.65 | 0.50 | 3.32 | 0.956 |
| w/o ASPP | 1.33 | 0.47 | 3.12 | 0.948 |
| w/ Featuremask (Mamba) | 2.65 | 0.70 | 3.35 | 0.957 |
| w/ Featuremask (LSTM) | 2.60 | 0.60 | 3.02 | 0.944 |
| w/ Featuremask (Conformer) | 1.52 | 1.65 | 3.15 | 0.949 |
| w/ Featuremask (Transformer) | 1.77 | 2.51 | 3.18 | 0.950 |
| w/o GLA | 1.65 | 0.50 | 3.24 | 0.953 |
| GLA (k=4) | 1.65 | 0.50 | 3.32 | 0.956 |
| w/o AISC | 1.63 | 1.32 | 3.28 | 0.955 |
| w/ AISC (1 kHz cutoff) | 1.65 | 0.42 | 3.20 | 0.951 |
| w/o DSConv2D (standard conv) | 9.63 | 4.53 | 3.26 | 0.954 |

Key findings: (i) Mamba gives +0.03 PESQ over lightS4 but at 1.6× params and 1.4× MACs — lightS4 is the explicit efficiency-quality compromise; (ii) AISC delivers a 2.6× MACs reduction (1.32 → 0.50 G) with only 0.04 PESQ loss; (iii) DSConv2D slashes parameters ~5.8× and MACs ~9× vs. standard conv with negligible PESQ change; (iv) GLA adds +0.08 PESQ over noisy phase at zero parameter cost.

### Classifier Loss Impact (Table 4)

| Condition | w/o Classifier Loss | w/ Classifier Loss | Δ PESQ |
|---|---|---|---|
| Vocal interference | 3.02 | 3.18 | +0.16 |
| Non-vocal noise | 3.39 | 3.46 | +0.07 |

The Classifier Loss provides a larger gain under competing-voice interference (+0.16 PESQ) than under non-vocal noise (+0.07 PESQ), validating its role as both a speaker-discriminative anchor and a structural regularizer.

### Robustness

On WSJ0-SI84 and LibriSpeech at SNRs from −5 dB to +5 dB, the model shows consistent PESQ/STOI gains over noisy baselines with minimal seen-vs-unseen gap (e.g., at 5 dB Babble on WSJ0-SI84, STOI 91.4% seen vs 89.4% unseen). Average PESQ improves from 1.96 → 3.30 across a dense 2.5–17.5 dB SNR sweep on VoiceBank+DEMAND.

## Key Contributions

1. **Lightweight SSM + DSConv synergy**: First framework to combine a diagonal-constrained S4 variant ([[concepts/lights4|lightS4]]) with [[concepts/depthwise-separable-convolution|depthwise separable convolutions]] for SE, achieving 1.65 M params / 0.50 G MACs — a **~60× MACs reduction vs. [[concepts/semamba|SEMamba]]** at a 0.20 PESQ cost.
2. **Atrous Spatial Pyramid Pooling (ASPP)**: Multi-scale contextual feature extraction via atrous DSConv2D with dilation rates {2, 4, 8} matched to harmonic, formant, and syllabic speech structure.
3. **[[concepts/auditory-inspired-spectral-compressor|Auditory-Inspired Spectral Compressor (AISC)]]**: Parameter-free dimensionality-reduction module that preserves low frequencies at full resolution while projecting high frequencies onto the [[concepts/erb-scale|ERB scale]], delivering a 2.6× MACs reduction with negligible quality loss.
4. **[[concepts/classifier-loss|Classifier Loss]]**: Auxiliary speaker-classification head with cross-entropy loss that suppresses competing human-voice interference (+0.16 PESQ under vocal interference) while regularizing against non-human noise.
5. **Parameter-free phase reconstruction**: Griffin–Lim Algorithm post-processor (+0.08 PESQ over noisy phase) avoids the parameter/MACs surge of learned complex-domain decoders, achieving a high DISC score (4.323) in subjective SigMOS evaluation.
6. **Efficiency–quality Pareto point**: SOTA on WSJ0-SI84 (PESQ 3.01 / STOI 0.87) with the lowest params (1.65 M) and MACs (0.50 G) among all tested models; RTF = 0.13 on consumer CPU.

## Related Concepts

- [[concepts/state-space-model|State-Space Model]] — control-theoretic and deep-learning SSM family
- [[concepts/lights4|lightS4]] — this paper's diagonal-constrained S4 variant (novel)
- [[concepts/mamba|Mamba]] — selective SSM baseline ablated in Table 3
- [[concepts/semamba|SEMamba]] — direct SOTA comparison (32.73 G MACs vs. 0.50 G)
- [[concepts/s4nd|S4ND]] — multidimensional S4 baseline referenced in Related Work
- [[concepts/sicrn|SICRN]] — prior SSM+inplace-convolution SE baseline
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]] — encoder/decoder building block
- [[concepts/erb-scale|ERB Scale]] — psychoacoustic basis for AISC
- [[concepts/auditory-inspired-spectral-compressor|Auditory-Inspired Spectral Compressor (AISC)]] — novel module (this paper)
- [[concepts/classifier-loss|Classifier Loss]] — novel auxiliary speaker-classification loss (this paper)
- [[concepts/speech-enhancement|Speech Enhancement]] — application domain

## Related Synthesis

- [[synthesis/computational-efficiency-evolution|Computational Efficiency in ANC: From O(N²) to GPU-Accelerated DSP]] — the proposed model defines a new efficiency–quality trade-off point on the 2026 lightweight-SE Pareto frontier, complementing [[concepts/cofi-lite|CoFi-Lite]], [[concepts/adaptcrn|AdaptCRN]], [[concepts/sse-net|SSE-Net]], and [[concepts/semamba|SEMamba]] axes.
