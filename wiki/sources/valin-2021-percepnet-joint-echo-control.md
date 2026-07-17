---
type: source
created: 2026-07-17
updated: 2026-07-17
sources:
  - raw/papers/valin-2021-percepnet-joint-echo-control/full-text.md
  - https://arxiv.org/abs/2102.05245
  - zotero://select/items/0_23HVPLE8
tags:
  - acoustic-echo-cancellation
  - speech-enhancement
  - residual-echo-suppression
  - noise-suppression
  - percepnet
  - erb-scale
  - pitch-periodicity
  - low-complexity
  - hybrid-aec
  - real-time
  - deep-learning
---

# Valin, Tenneti, Helwani, Isik & Krishnaswamy 2021: Joint Neural Echo Control and Speech Enhancement Based On PercepNet

| Field | Value |
|-------|-------|
| **Authors** | [[entities/jean-marc-valin|Jean-Marc Valin]], [[entities/srikanth-tenneti|Srikanth Tenneti]], [[entities/karim-helwani|Karim Helwani]], [[entities/umut-isik|Umut Isik]], [[entities/arvindh-krishnaswamy|Arvindh Krishnaswamy]] |
| **Institution** | Amazon Web Services, Palo Alto, CA, USA |
| **Published** | arXiv:2102.05245, Feb 2021; Winner of ICASSP 2021 AEC Challenge |
| **Type** | Conference/Challenge Paper |
| **arXiv** | [2102.05245](https://arxiv.org/abs/2102.05245) |
| **Zotero** | [23HVPLE8](zotero://select/items/0_23HVPLE8) |

## Summary

This paper presents a hybrid acoustic echo control (AEC) + joint residual echo and noise suppression (RES/NS) system that combines a traditional multidelay block frequency-domain (MDF) adaptive filter with a [[concepts/percepnet|PercepNet]]-based neural post filter. It won **first place in the ICASSP 2021 AEC Challenge** out of 17 submissions while requiring only **5.5% CPU** (0.55 ms per 10-ms frame on an Intel i7-8565U). The work introduces the original PercepNet-style hybrid AEC pattern that was later refined by [[sources/seidel-2024-bark-scale-nn-residual-suppression|Bark-AEC (Seidel 2024)]] and [[sources/li-2025-echofree-neural-aec|EchoFree (Li 2025)]].

![[raw/papers/valin-2021-percepnet-joint-echo-control/figures/e5a73a91ebe8b7afb16d54d72f49917dca5f3c34c8ee04a13e93021dd0c85a2b.jpg|System overview]]
*Figure 1: Overview of the joint echo control and noise suppression system. The far-end signal f(n) is played through the loudspeaker. The microphone signal d(n) captures reverberated near-end speech plus noise v(n) and echo z(n) from the loudspeaker. The echo is partially cancelled by the adaptive filter ĥ_f to produce y(n). The RES then enhances y(n) by suppressing noise, reverberation, and the remaining echo, producing the enhanced output x̂(n).*

## Problem Formulation

Let $x(n)$ be the clean near-end speech signal. The signal captured by a hands-free microphone in a noisy room is

$$
d(n) = x(n) \star \mathbf{h}_x + v(n) + z(n), \tag{1}
$$

where $v(n)$ is additive room noise, $z(n)$ is the echo caused by a far-end signal $f(n)$, $\mathbf{h}_x$ is the impulse response from the talker to the microphone, and $\star$ denotes convolution. When ignoring non-linear effects, the echo signal can be expressed as

$$
z(n) = f(n) \star \mathbf{h}_f.
$$

Echo cancellation based on adaptive filtering consists in estimating $\mathbf{h}_f$ and subtracting the estimated echo $\hat{z}(n)$ from the microphone signal to produce the echo-cancelled signal $y(n)$. Because echo cancellation is generally imperfect, residual echo remains in $y(n)$, so a joint residual echo suppression (RES) and noise suppression (NS) stage further enhances $y(n)$ to produce $\hat{x}(n)$ that is perceptually as close as possible to the ideal clean speech $x(n)$.

## Methodology

### Adaptive Filter (MDF)

The adaptive filter is derived from the SpeexDSP implementation of the [[concepts/multidelay-block-frequency-domain-adaptive-filter|multidelay block frequency-domain (MDF) adaptive filter]] [Soo & Pang 1990]. Robustness to double-talk is achieved through a combination of:

- Learning rate control [Valin 2007]
- A two-echo-path model [Ochiai 1977]
- A block variant of the PNLMS algorithm [Duttweiler 2000] to speed up adaptation

As a compromise between complexity and convergence, the system uses a variant of AUMDF where most blocks are alternatively constrained, but the highest-energy block is constrained on each iteration.

**Delay estimation**: An unknown delay $D$ between the signal $f(n)$ sent to the loudspeaker and the corresponding echo at the microphone is estimated using a second AEC with a 400-ms filter, finding the peak in the estimated filter. This delay-estimating AEC operates on a downsampled (8 kHz) version of the signals to reduce complexity. The delayed far-end signal $f(n-D)$ is then used to perform final echo cancellation at 16 kHz.

**Filter configuration**: 150-ms filter length (good compromise between complexity, convergence, and steady-state accuracy, ensuring that echo loudness is sufficiently reduced for the RES to correctly preserve double-talk). Frame size: 10 ms (matching the RES frame size to avoid extra delay). Operating sampling rate: 16 kHz. No attempt is made to cancel non-linear distortion in the echo.

### PercepNet RES

Joint RES and NS is implemented using the [[concepts/percepnet|PercepNet]] algorithm [Valin et al. ICASSP 2020], based on two main ideas:

1. **Scaling the energy of perceptually-spaced spectral bands** to match that of the near-end speech.
2. **Using a multi-tap comb filter at the pitch frequency** to remove noise between harmonics and match the periodicity of the near-end speech.

The short-time Fourier transform (STFT) spectrum is divided into **32 triangular bands following the [[concepts/erb-scale|ERB scale]]** [Moore 2012]. Let $Y_b(\ell)$ be the magnitude of the AEC output in band $b$ for frame $\ell$ and $X_b(\ell)$ be similarly defined for the clean speech. The ideal gain that should be applied to that band is:

$$
g_b(\ell) = \frac{X_b(\ell)}{Y_b(\ell)}. \tag{2}
$$

Applying $g_b(\ell)$ to the magnitude spectrum in band $b$ results in an enhanced signal with the same spectral envelope as the clean speech. For voiced segments, a non-causal comb filter controlled by a strength/mixing parameter $r_b(\ell) \in [0, 1]$ (0 = no filtering, 1 = full comb filtering) is applied to remove noise between harmonics and increase periodicity. In cases where $r_b(\ell) = 1$ is still insufficient, a further attenuation $g_b^{\mathrm{(att)}}(\ell)$ is applied (envelope postfilter, Section 5 of [Valin 2020]).

The far-end signal $f(n)$ (rather than the delayed $f(n-D)$) is used as side information to the RES, since it does not depend on AEC behaviour and is therefore more robust to convergence problems. The output gains $\hat{g}_b(\ell)$ are further modified by an envelope postfilter that reduces the perceptual impact of remaining noise in each band.

### DNN Architecture

The model (Fig. 3) uses **2 convolutional layers** (a 1×5 layer followed by a 1×3 layer) and **5 GRU layers** [Cho et al. 2014]. The convolutional layers are aligned in time to use up to $M$ frames into the future. To achieve the 40 ms algorithmic delay allowed by the challenge (including the 10-ms frame size and 10-ms overlap), $M = 2$ frames is used.

![[raw/papers/valin-2021-percepnet-joint-echo-control/figures/f9fa37f6ad45f87bff145b9434c590cd23bf9966bea2f6fbd845b17570284d09.jpg|DNN architecture]]
*Figure 3: Overview of the DNN architecture computing the 32 gains ĝ_b and 32 strengths r̂_b from the 100-dimensional input feature vector f. The number of units on each layer is indicated above the layer type.*

**Input**: 100 features = 96 band features (3 per band) + 4 scalar features. For each of the 32 bands:

1. The energy in the band with look-ahead $Y_b(\ell + M)$
2. The [[concepts/pitch-coherence|pitch coherence]] without look-ahead $q_{y,b}(\ell)$ (the coherence estimation itself uses the full look-ahead)
3. The energy of the far-end band with look-ahead $F_b(\ell + M)$

The 4 extra scalar features are:

- The pitch period $T(\ell)$
- An estimate of the pitch correlation with look-ahead
- A non-stationarity estimate
- The ratio of the $L_1$-norm to the $L_2$-norm of the excitation computed from $y(n)$

**Output**: 64 values = 32 gains $\hat{g}_b(\ell)$ (approximating $g_b^{\mathrm{(att)}}(\ell) g_b(\ell)$) + 32 strengths $\hat{r}_b(\ell)$ (approximating $r_b(\ell)$).

**Quantization**: The 8M weights in the model are forced to a $\pm\tfrac{1}{2}$ range and quantized to 8-bit integers. This reduces total memory requirement (and cache bandwidth), while also reducing the computational complexity of inference when taking advantage of vectorization (more operations for the same register width).

### Sparse Model

For further complexity reduction, the system uses **[[concepts/structured-sparsity|structured sparsity]]** — whole sub-blocks of matrices are either zero or non-zero — implemented similarly to Kalchbrenner et al. 2018 and Valin & Skoglund 2019 (LPCNet). This is critical for SIMD vectorization on modern CPUs. The work uses **16×4 sub-blocks**.

Sparsity pattern:

- All fully-connected layers and the **first convolutional layer**: kept dense (no sparsity)
- **Second convolutional layer**: 50% dense
- **GRU new-state matrices**: 40% dense
- **GRU update gate matrices**: 20% dense
- **GRU reset gate matrices**: 10% dense

This reflects the unequal usefulness of the different gates on recurrent units.

Two sparse variants are considered:

- **Sparse (25%)**: 2.1M non-zero weights = 25% of the size of the full model
- **Ultra-low (10%)**: same density but layers limited to 256 units, giving 800k non-zero weights = 10% of the full model

When training sparse models, the sparsification schedule proposed in [Zhu & Gupta 2017] is used.

## Training

The model is trained on **synthetic mixtures** of clean speech, noise, and echo designed to recreate real-world conditions including reverberation.

- **SNR range**: −15 dB to 45 dB (with some noise-free examples)
- **Echo-to-nearend ratio**: −15 dB to 35 dB
- **Data**: 120 hours of clean speech + 80 hours of various noise types. Most data sampled at 48 kHz; some (including far-end single-talk data provided by the challenge organizers) sampled at 16 kHz. Both synthetic and real room impulse responses are used for augmentation.

**Distance / reverberation augmentation**: Although the near-end speech, echo, and noise all occur in the same room (same $RT_{60}$), they can be at different locations and distances. Therefore, only one room impulse response is picked per condition, but the **early reflections (first 20 ms) are scaled with a gain varying between 0.5 and 1.5** to simulate the distance changing. Inspired by Zhao et al. 2018, the target signal includes the early reflections plus an attenuated echo tail ($RT_{60} = 200$ ms), so that late reverberation is attenuated to match the acoustics of a small room.

**Filtering augmentation** [Valin 2018, Valin 2020]: includes applying a low-pass filter with a random cutoff frequency, making it possible to use the same model on narrowband to fullband audio.

## Loss Function

The loss function for the gain attempts to match human perception as closely as possible. It is a perceptually motivated gain loss:

$$
\mathcal{L}_g = \sum_b \mathcal{D}(g_b, \hat{g}_b) + \lambda_4 \sum_b [\mathcal{D}(g_b, \hat{g}_b)]^2, \tag{3}
$$

with the distortion function

$$
\mathcal{D}(g_b, \hat{g}_b) = \frac{\left(g_b^{2\gamma} - \hat{g}_b^{2\gamma}\right)^2}{\max\left(g_b^{2\gamma}, \hat{g}_b^{2\gamma}\right) + \epsilon}, \tag{4}
$$

where:

- $\gamma = 0.3$ is the generally agreed-upon exponent to convert acoustic power to the sone scale for perceived loudness [Moore 2012]
- $\lambda_4 = 10$ — an $L_4$ term that over-emphasizes large errors in general
- The denominator in (4) over-emphasizes the loss when completely attenuating speech or when letting through small amounts of noise/echo during silence

The same loss function as [Valin 2020] is used for $\hat{r}_b$.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Sampling rate | 16 kHz (also 48 kHz capable) |
| Frame size | 10 ms |
| AEC filter length | 150 ms |
| Delay estimation | 400-ms AEC on 8 kHz |
| ERB bands | 32 |
| Look-ahead $M$ | 2 frames (20 ms) |
| Algorithmic delay | 40 ms (challenge limit) |
| DNN | 2 conv + 5 GRU layers |
| Weights | 8M (8-bit quantized) |
| Sparse variants | 2.1M (25%) / 800k (10%) non-zero |
| Training data | 120 h speech + 80 h noise |
| Test set | ICASSP 2021 AEC Challenge blind set (1000 real recordings) |
| Metrics | P.808 MOS, P.831 Echo DMOS, ERLE* |
| Hardware | Intel i7-8565U |

Each test utterance was rated by 10 listeners, giving a 95% confidence interval of **0.01 MOS** for all algorithms. The test set comprised 600 utterances with near-end speech (excluding far-end single-talk samples) for MOS comparisons, and far-end single-talk samples for the modified ERLE* metric.

## Results

### AEC Challenge Official Results (Table 1)

P.808 MOS of near-end single-talk (STNE), P.831 Echo DMOS for far-end single-talk (STFE), P.831 Echo DMOS for double-talk (DTEcho), P.831 other-degradations DMOS of double-talk (DTOther). The baseline is provided by the challenge organizers; the second-place row is the mean of the four algorithms statistically tied for second place.

| Algorithm | STNE | STFE | DTEcho | DTOther | Mean |
|-----------|-----:|-----:|-------:|--------:|-----:|
| Baseline | 3.79 | 3.84 | 3.84 | 3.28 | 3.68 |
| 2nd place (mean of 4) | 3.80 | 4.18 | 4.25 | 3.74 | 3.99 |
| **PercepNet** | **3.85** | **4.19** | **4.34** | **4.07** | **4.11** |

PercepNet ranked **first place out of 17 submissions** to the challenge. The 95% confidence interval is 0.01 MOS for all algorithms. Although PercepNet performs well across all metrics, the improvement is particularly noticeable on **DT Other**, which measures the degradation caused to the near-end speech during double-talk conditions — a 0.33 MOS improvement over the second-place mean.

### Complexity

- **RES complexity (non-sparse)**: 800M MACs/s (dominated by the contribution of all 8M weights on 100 frames per second).
- **RES CPU**: 4.6% of an x86 mobile CPU core (Intel i7-8565U) for real-time operation.
- **Total AEC + RES** (16 kHz): 5.5% CPU (0.55 ms per 10-ms frame).
- **Fullband (48 kHz) AEC + RES**: 6.6% CPU (increase due to the higher AEC sampling rate; RES already designed to operate at 48 kHz).
- **Lower bound (sparse variants)**: quality can scale down to 1.5% CPU with graceful degradation (Section 5.1).

### Complexity Scaling (Figs. 4 & 5)

Figure 4 (P.808 MOS vs complexity) and Figure 5 (median ERLE* on far-end single-talk vs complexity) compare three PercepNet RES model sizes — each evaluated with and without a linear AEC in front — along with the AEC alone (no RES) and the AEC followed by the SpeexDSP conventional joint RES+NS. Key qualitative findings:

- The **PercepNet-based RES significantly outperforms the SpeexDSP conventional RES** at all complexity levels, even when used as a pure echo suppressor (except at the lowest complexity setting).
- All PercepNet-based algorithms **remove far more echo and noise** than the conventional approach (Fig. 5, ERLE*).
- The **linear AEC does not help attenuate isolated (far-end-only) echo** — its presence does not change ERLE* significantly on far-end single-talk.
- However, the linear AEC **greatly contributes to preserving speech during double-talk** — confirming the benefit of the adaptive filter component despite its lack of impact on isolated echo attenuation.

### Discrepancy Note

> **Note on perceptual scale used by PercepNet vs. later PercepNet-style works**: The original PercepNet (this paper) uses the **ERB scale (32 bands)**. Later works in the [[concepts/percepnet-style-neural-post-filter|PercepNet-style neural post filter]] lineage — [[sources/seidel-2024-bark-scale-nn-residual-suppression|Bark-AEC (Seidel 2024, 86 Bark bands)]] and [[sources/li-2025-echofree-neural-aec|EchoFree (Li 2025, 100 Bark bands)]] — switched to the **Bark scale**. The existing wiki's "PercepNet-style neural post filter" concept page originally characterized the entire lineage as Bark-based; this is correct for the later works but **not** for the original PercepNet, which is ERB-based. The "PercepNet-style" pattern name refers to the hybrid AEC + perceptual-band neural post filter architecture, not strictly to the Bark scale.

## Key Contributions

1. **First integrated hybrid AEC + PercepNet-based joint RES+NS system with ultra-low complexity (5.5% CPU)** — combines a classical MDF adaptive filter with a perceptually-motivated neural post filter at 800M MACs/s, demonstrating that physics/psychoacoustics priors make such low complexity feasible.
2. **Won 1st place in the ICASSP 2021 AEC Challenge (17 submissions)**, with the largest improvement on the DT Other metric (near-end preservation during double-talk) — a 0.33 MOS improvement over the second-place mean (4.07 vs. 3.74).
3. **Demonstrated that perceptually-motivated features (ERB bands + pitch coherence + comb filter) outperform conventional approaches at lower complexity.** PercepNet-based RES significantly outperforms SpeexDSP conventional RES at all complexity levels tested.
4. **Introduced structured sparsity for AEC DNNs (16×4 sub-blocks)**, scaling compute down from 4.6% CPU (full) to 1.5% CPU with graceful quality degradation; sparse variants reach 2.1M (25%) and 800k (10%) non-zero weights.
5. **Showed that the linear AEC is critical for double-talk speech preservation** despite not helping isolated (far-end-only) echo attenuation — confirming the value of the hybrid AEC + RES pattern over a pure neural suppressor.

## Related Concepts

- [[concepts/percepnet|PercepNet]]
- [[concepts/percepnet-style-neural-post-filter|PercepNet-Style Neural Post Filter]]
- [[concepts/erb-scale|ERB Scale]]
- [[concepts/pitch-coherence|Pitch Coherence]]
- [[concepts/multidelay-block-frequency-domain-adaptive-filter|Multidelay Block Frequency-Domain Adaptive Filter (MDF)]]
- [[concepts/structured-sparsity|Structured Sparsity]]
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- Residual Echo Suppression
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]

## Related Sources

- [[sources/seidel-2024-bark-scale-nn-residual-suppression|Seidel, Mowlaee & Fingscheidt 2024]] — Bark-AEC, later PercepNet-style variant using the Bark scale (86 bands) instead of ERB
- [[sources/li-2025-echofree-neural-aec|Li et al. 2025: EchoFree]] — later ultra-lightweight successor using the Bark scale (100 bands) + U-Net
- [[sources/indenbom-2023-deepvqe|Indenbom et al. 2023: DeepVQE]] — non-PercepNet SOTA comparison point
- [[sources/shetu-2024-hybrid-low-complexity-aenr|Shetu et al. 2024: Hybrid Low-Complexity AENR]] — ULCNet-AER, contemporary low-complexity baseline

## Related Synthesis

- [[synthesis/joint-multitask-ultra-low-latency-se|Joint Multi-Task SE & Ultra-Low-Latency Paradigm]] — This paper is the origin of the PercepNet-style hybrid AEC pattern, sitting at 5.5% CPU (800M MACs/s) on the efficiency frontier.
