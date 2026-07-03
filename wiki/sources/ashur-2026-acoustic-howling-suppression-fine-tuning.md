---
type: source
created: 2026-07-03
updated: 2026-07-03
sources:
  - raw/papers/ashur-2026-acoustic-howling-suppression-fine-tuning/full-text.md
  - https://israelcohen.com/wp-content/uploads/2026/05/Enhancing_Acoustic_Howling_Suppression_Robustness_in_Deep_Speech_Enhancement_Networks.pdf
  - zotero://select/items/0_HRHUQQER
tags:
  - acoustic-howling-suppression
  - speech-enhancement
  - deep-learning
  - fine-tuning
  - demucs
  - denoiser
---

# Ashur & Cohen 2026: Acoustic Howling Suppression by Fine-Tuning Deep Speech Enhancement Networks

**Authors**: [[entities/avichay-ashur|Avichay Ashur]], [[entities/israel-cohen|Israel Cohen]]
**Institutions**: Andrew and Erna Viterbi Faculty of Electrical & Computer Engineering, Technion — Israel Institute of Technology, Haifa 3200003, Israel
**Published**: Preprint, 2026 (hosted on israelcohen.com, May 2026)
**Type**: Preprint (journalArticle in Zotero)
**URL**: [Enhancing_Acoustic_Howling_Suppression_Robustness_in_Deep_Speech_Enhancement_Networks.pdf](https://israelcohen.com/wp-content/uploads/2026/05/Enhancing_Acoustic_Howling_Suppression_Robustness_in_Deep_Speech_Enhancement_Networks.pdf)
**Zotero**: [HRHUQQER](zotero://select/items/0_HRHUQQER)

---

## Summary

Adapts a pretrained real-time **Denoiser** network (DEMUCS-based, Defossez et al. 2020) for acoustic howling suppression (AHS) by fine-tuning it on a mixture of its original noise-reduction data (Valentini-Botinhao) and offline-generated synthetic howling samples (from AISHELL-2 with image-method RIRs and hard-clipping loudspeaker nonlinearity). Systematically varying the howling/noise mixing ratio shows that the **60-40** configuration achieves strong online AHS at higher gains with only minimal degradation in speech enhancement (PESQ 2.55 at gain 2, <1% drop from the original pretrained network). The method requires no architectural modifications, no recursive training, and introduces no additional inference latency — it is a practical drop-in fine-tuning strategy for jointly addressing noise reduction and howling suppression.

---

## Problem Formulation

### Acoustic Amplification System with Feedback

![[raw/papers/ashur-2026-acoustic-howling-suppression-fine-tuning/figures/061469bcdcbf14150daefe742ec6c1599f8b71485186f9e00ed0b679adf7a437.jpg|Diagram of an acoustic amplification system]]

*Figure 1: Diagram of an acoustic amplification system. The loudspeaker output is recaptured by the microphone through the acoustic path, forming a recursive feedback loop.*

The loudspeaker signal captured by the microphone after traversing the acoustic path is:

$$d(t) = \mathrm{NL}[x(t)] * h(t) \tag{1}$$

where $h(t)$ is the room impulse response from loudspeaker to microphone, $*$ denotes linear convolution, and $\mathrm{NL}(\cdot)$ accounts for the nonlinear distortion introduced by the loudspeaker.

The microphone signal becomes a **recursive closed loop**:

$$y(t) = s(t) + n(t) + \mathrm{NL}[y(t - \Delta t) \cdot G] * h(t) \tag{2}$$

where $s(t)$ is target speech, $n(t)$ is background noise, $\Delta t$ is the system delay from microphone to loudspeaker, and $G$ is the amplifier gain. The recursive re-amplification of $y(t-\Delta t)$ produces the high-pitched tonal artifact known as acoustic howling whenever $G$ exceeds the [[concepts/maximum-stable-gain|Maximum Stable Gain]] of the loop.

### Practical Gap Addressed

Existing deep-learning AHS methods (e.g., DeepAHS, DeepMFC, HybridAHS, NKal-AHS) are designed as **dedicated suppression models** that primarily target feedback instability, without explicitly preserving general speech-enhancement (noise-reduction) capabilities. As a result, deploying them in real audio systems (hearing aids, PA systems, instrument amplifiers) that must also perform background noise reduction requires either a separate model or a compromise in speech quality. This paper investigates using offline-generated howling samples as a **complementary** training component (not the sole supervision signal) alongside the original noise-reduction data.

---

## Methodology

### A. Baseline Speech Enhancement Model — Denoiser (DEMUCS-derived)

The baseline is the real-time **Denoiser** network proposed by Defossez et al. (2020), derived from the DEMUCS (Deep Extractor for Music Sources) architecture:

- **Encoder–decoder** structure with skip connections
- Stacked **convolutional layers** in the encoder progressively downsample the input, capturing both spectral and temporal features
- **LSTM recurrent module** in the latent representation models long-range temporal dependencies
- Optimized for real-time speech enhancement: low latency, computational efficiency, preserving the encoder–decoder design
- Initially trained on the **Valentini-Botinhao** noisy-speech dataset using **time-domain loss** functions mapping noisy inputs to clean targets

### B. Fine-Tuning with Offline-Generated Howling Data

The pretrained Denoiser is fine-tuned on a joint dataset combining:

1. **Original noise-reduction data** (Valentini-Botinhao) — preserves the model's speech-enhancement capabilities
2. **Offline-generated howling samples** — exposes the network to feedback-induced distortions absent from conventional speech-enhancement datasets

The two datasets are jointly used during fine-tuning with their **relative proportions systematically varied** to study the trade-off between speech-enhancement performance and AHS robustness.

#### Howling Sample Generation Pipeline

| Component | Configuration |
|-----------|---------------|
| Clean speech source | AISHELL-2 dataset (Mandarin) |
| RIR generation | Image method (Allen & Berkley), randomized room dimensions and source–receiver configurations |
| Loudspeaker nonlinearity | Saturation-type distortion via **hard clipping** (Birkett & Goubran 1996) |
| Background noise during howling generation | **Not added** — isolates feedback-induced distortions for focused learning |
| System delay $\Delta t$ during training | 0 (randomized RIRs already introduce propagation delays) |
| Inference-time $\Delta t$ | Estimated from target platform via Denoiser repository implementation |
| Training gain $G$ | 2 (unless otherwise stated) |
| Fine-tuning epochs | 300 |

#### Mixing-Ratio Configurations

| Model label | Howling data % | Noise-reduction data % |
|-------------|---------------:|----------------------:|
| 0-100 | 0 | 100 |
| 10-90 | 10 | 90 |
| 25-75 | 25 | 75 |
| 50-50 | 50 | 50 |
| **60-40** | **60** | **40** |
| 75-25 | 75 | 25 |

### Key Design Properties

- **No architectural modifications** — same Denoiser network is fine-tuned
- **No recursive training** — no [[concepts/teacher-forcing|Teacher Forcing]] or closed-loop training (unlike DeepAHS, HybridAHS)
- **No additional inference latency** — fine-tuned model has identical forward-pass cost

---

## Experimental Setup

### Datasets

| Purpose | Dataset | Description |
|---------|---------|-------------|
| Howling sample generation | AISHELL-2 [22] | Mandarin clean speech |
| Noise reduction / speech enhancement | Valentini-Botinhao [21] | Paired clean/noisy speech, varied noise types and SNRs |
| Noise reduction evaluation | Valentini-Botinhao test set | Standard SE benchmark |

### Evaluation Metrics

- **PESQ** (Perceptual Evaluation of Speech Quality, [29]) — perceptual speech quality
- **SDR** (Signal-to-Distortion Ratio) — overall signal fidelity
- Both computed between the enhanced output and the clean target speech

### Evaluation Scenarios

1. **Speech enhancement (noise reduction)**: model evaluated offline on Valentini-Botinhao test set (no feedback loop)
2. **Online AHS**: model integrated into a streaming acoustic feedback loop with different test-time RIRs; evaluated at multiple gains $G \in \{1.5, 2, 2.5, 3\}$ and $G \in \{2, 5, 7.5\}$

### Training

- Fine-tuning: 300 epochs, gain $G = 2$
- Baseline for comparison: pretrained Denoiser (0-100 configuration, fine-tuned without any howling data)

### Comparison Baselines

| Method | Reference | Approach |
|--------|-----------|----------|
| no-AHS | — | No AHS processing (only the feedback loop) |
| DeepMFC | [18] | Deep learning solution to marginal stability; trained exclusively on offline howling data |
| DeepAHS | [12] | Teacher-forced streaming AHS network |
| HybridAHS | [25] | FDKF + SARNN cascade (see [[sources/zhang-2023-hybrid-ahs\|Zhang 2023: Hybrid AHS]]) |
| Neural-KG | [26] | Learning-based step-size control for adaptive feedback cancellation |
| NKal-AHS | [27] | NN-augmented Kalman filter (see [[sources/zhang-2024-neural-kalman-howling\|Zhang 2024: NKal-AHS]]) |
| Hybrid-NN | [28] | Recursive neural-network training for AHS |

---

## Results

### A. Online Acoustic Howling Suppression (Table I)

SDR and PESQ at gains $G \in \{2, 5, 7.5\}$ for fine-tuned models with varying mixing ratios:

| Model | SDR @ G=2 | SDR @ G=5 | SDR @ G=7.5 | PESQ @ G=2 | PESQ @ G=5 | PESQ @ G=7.5 |
|-------|----------:|----------:|------------:|-----------:|-----------:|-------------:|
| 0-100 | −0.26 | −0.54 | −1.02 | 1.95 | 1.81 | 1.66 |
| 10-90 | −0.32 | −0.20 | −0.20 | 1.93 | 1.83 | 1.71 |
| 25-75 | −0.02 | −0.11 | −0.04 | 2.19 | 2.01 | 1.86 |
| 50-50 | 0.76 | 0.62 | 0.30 | 2.46 | 2.26 | 2.06 |
| **60-40** | **2.00** | **1.65** | **1.34** | **2.55** | **2.41** | **2.22** |
| 75-25 | 1.27 | 1.06 | 0.72 | 2.19 | 2.03 | 1.86 |

**Key observation**: PESQ and SDR improve monotonically up to the 60-40 ratio, then degrade at 75-25, indicating an optimal trade-off. The 60-40 model is the recommended configuration.

### B. Comparison with Previous Works (Table II)

Online AHS at gains $G \in \{1.5, 2, 2.5, 3\}$ (mean ± std):

| Method | SDR @ G=1.5 | SDR @ G=2 | SDR @ G=2.5 | SDR @ G=3 | PESQ @ G=1.5 | PESQ @ G=2 | PESQ @ G=2.5 | PESQ @ G=3 |
|--------|------------:|----------:|------------:|----------:|-------------:|-----------:|-------------:|-----------:|
| no-AHS | −30.51 ± 7.23 | −31.86 ± 5.66 | −33.10 ± 3.96 | −33.21 ± 3.94 | — | — | — | — |
| DeepMFC [18] | −0.09 ± 6.50 | −2.78 ± 9.44 | −5.59 ± 11.40 | −7.69 ± 12.26 | 2.11 ± 0.51 | 1.88 ± 0.59 | 1.70 ± 0.62 | 1.56 ± 0.59 |
| DeepAHS [12] | 1.98 ± 6.50 | 0.04 ± 8.60 | −3.15 ± 12.01 | −6.32 ± 14.07 | 2.49 ± 0.42 | 2.42 ± 0.65 | 2.04 ± 0.79 | 1.84 ± 0.77 |
| HybridAHS [25] | 2.96 ± 3.04 | 1.25 ± 5.79 | −1.45 ± 9.60 | −3.49 ± 10.90 | 2.57 ± 0.47 | 2.33 ± 0.53 | 2.22 ± 0.59 | 1.95 ± 0.62 |
| Neural-KG [26] | 2.50 ± 2.78 | 1.63 ± 3.34 | −0.46 ± 7.46 | −2.50 ± 9.94 | 2.35 ± 0.46 | 2.14 ± 0.44 | 1.95 ± 0.48 | 1.80 ± 0.53 |
| NKal-AHS [27] | 3.65 ± 2.01 | 2.65 ± 1.70 | 1.98 ± 1.49 | 1.45 ± 1.31 | 2.55 ± 0.44 | 2.33 ± 0.41 | 2.10 ± 0.39 | 2.04 ± 0.37 |
| Hybrid-NN [28] | 3.87 ± 1.68 | 3.04 ± 1.34 | 2.49 ± 1.11 | 2.11 ± 0.98 | 2.60 ± 0.41 | 2.40 ± 0.38 | 2.25 ± 0.36 | 2.13 ± 0.34 |
| **Model 60-40 (proposed)** | 2.02 ± 4.78 | 2.00 ± 4.81 | 1.99 ± 4.82 | 1.97 ± 4.88 | 2.58 ± 0.62 | 2.55 ± 0.62 | 2.55 ± 0.61 | 2.53 ± 0.62 |

**Key observations**:

1. **PESQ stability across gains**: The proposed model's PESQ drops only ~0.05 from $G=1.5$ to $G=3$, whereas HybridAHS and NKal-AHS degrade by 0.5–0.6 over the same range. This is the proposed method's most distinctive advantage.
2. **Best PESQ at high gain ($G \geq 2$)**: The proposed model achieves the highest PESQ scores at gains 2, 2.5, and 3 among all evaluated methods (2.55, 2.55, 2.53), except for Hybrid-NN at $G=1.5$ (2.60 vs proposed 2.58, a negligible difference).
3. **Lower SDR than dedicated-feedback methods**: Hybrid-NN consistently achieves higher SDR (3.87→2.11) because it is explicitly optimized for feedback cancellation. The proposed approach prioritizes perceptual quality over raw distortion minimization, suggesting room for improvement on residual distortion.

### C. Speech Enhancement (Noise Reduction) Preservation

On the Valentini-Botinhao test set, for mixing ratios up to 60%:

- PESQ remains close to **2.56**, with **<1% reduction** versus the original pretrained Denoiser (the 0-100 configuration)
- SDR varies by **at most 2%**, indicating only minor noise-reduction degradation

At 75-25 (excessive howling data):

- PESQ drops to **2.47**
- SDR drops from **17.62 → 16.79**
- This indicates that over-emphasis on howling data biases the model to suppress narrowband feedback at the expense of broadband speech reconstruction

### D. Spectrogram Analysis

Figure 2 in the paper illustrates representative spectrograms: (a) target signal, (b) no AHS (strong narrowband high-frequency howling components dominate), (c) 0-100 model (incomplete suppression, reduced spectral clarity), (d) 60-40 model (effectively suppresses feedback while preserving both low- and high-frequency speech components). Spectrograms are illustrative and not reproduced here since the same data is summarized in the PESQ/SDR tables above.

---

## Key Contributions

1. **A practical fine-tuning strategy for joint noise reduction + AHS**: Demonstrates that a pretrained speech-enhancement network can be adapted for acoustic howling suppression simply by mixing offline-generated howling samples into the original noise-reduction training data — no architectural modification, recursive training, or additional inference latency.
2. **Systematic study of the howling/noise mixing-ratio trade-off**: Identifies the 60-40 ratio as the sweet spot that maximizes AHS robustness while preserving speech-enhancement performance (<1% PESQ loss, <2% SDR loss).
3. **State-of-the-art perceptual speech quality at high gain**: The 60-40 model achieves the highest PESQ among all evaluated methods at $G \in \{2, 2.5, 3\}$, with the most stable PESQ across gain levels (drop of only ~0.05 vs 0.5–0.6 for HybridAHS and NKal-AHS).
4. **Distinct training philosophy vs. prior AHS work**: Unlike DeepMFC (which uses offline-generated howling data in isolation) or DeepAHS/HybridAHS (which rely on teacher forcing / recursive training), this work uses howling data as a **complementary** signal alongside noise-reduction data — making it the first to explicitly trade AHS robustness against speech-enhancement preservation in a controlled manner.

---

## Related Concepts

- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — overall field this paper contributes to
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the feedback phenomenon that causes howling (Eq. 2)
- [[concepts/denoiser-network|Denoiser Network (DEMUCS)]] — the baseline architecture fine-tuned in this work
- [[concepts/speech-enhancement|Speech Enhancement]] — the original task of the pretrained Denoiser
- [[concepts/teacher-forcing|Teacher Forcing]] — explicitly *not* used here; contrasted with DeepAHS and HybridAHS
- [[concepts/image-source-method|Image Source Method]] — used for offline RIR generation
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — fundamental constraint the loop must respect to avoid howling
- [[concepts/pesq|PESQ]] — primary perceptual quality metric used in evaluation
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]] — broader methodological category

## Related Sources

- [[sources/zhang-2023-hybrid-ahs|Zhang 2023: Hybrid AHS]] — HybridAHS baseline (FDKF + SARNN with teacher forcing)
- [[sources/zhang-2024-neural-kalman-howling|Zhang 2024: NKal-AHS]] — NN-augmented Kalman filter baseline

## Related Synthesis

- (No dedicated synthesis page yet for "fine-tuning vs. dedicated-model AHS comparison" — candidate for future synthesis)
