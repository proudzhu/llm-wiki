---
type: source
created: 2026-08-22
updated: 2026-08-22
sources:
  - raw/papers/tesch-2023-insights-deep-nonlinear-filters/full-text.md
  - https://doi.org/10.1109/TASLP.2022.3221046
  - zotero://select/items/0_QZMBNBLN
tags:
  - speech-enhancement
  - multi-channel
  - spatial-filtering
  - deep-learning
  - microphone-arrays
  - nonlinear-filtering
  - joint-nonlinear-filtering
  - target-speaker-extraction
---

# Tesch & Gerkmann 2023: Insights Into Deep Non-linear Filters for Improved Multi-channel Speech Enhancement

**Authors**: [[entities/kristina-tesch|Kristina Tesch]] (Student Member, IEEE), [[entities/timo-gerkmann|Timo Gerkmann]] (Senior Member, IEEE)
**Affiliation**: Signal Processing Group, Universität Hamburg, Germany
**Venue**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 71, 2023
**Type**: Journal Article
**DOI**: [10.1109/TASLP.2022.3221046](https://doi.org/10.1109/TASLP.2022.3221046)
**Zotero**: [QZMBNBLN](zotero://select/items/0_QZMBNBLN)
**Predecessor**: Tesch, Mohrmann & Gerkmann, Interspeech 2022 — "On the role of spatial, spectral, and temporal processing for DNN-based non-linear multi-channel speech enhancement" [21]

## Summary

This paper presents a systematic analysis of the internal mechanisms of DNN-based joint non-linear spatial and tempo-spectral filters (JNF) for multi-channel speech enhancement. By carefully controlling the information sources (spatial, spectral, temporal) available to a simple two-LSTM + feed-forward network, the authors show that (i) a non-linear spatial filter outperforms an **oracle** MVDR plus post-filter at low microphone counts, (ii) spectral information processed jointly with spatial information increases spatial selectivity far more than temporal information does, and (iii) the resulting **FT-JNF** architecture — using all three information sources — outperforms state-of-the-art baselines (FaSNet+TAC, EaBNet, COSPA, CRNN, T-JNF) by at least 0.22 POLQA on a speaker-extraction task and 0.32 POLQA on CHiME3, despite having the fewest parameters (1.2 M). The FT-JNF is the architectural basis for the [[concepts/spatially-selective-nonlinear-filter|SSF]] and for [[concepts/mcnet|McNet]].

## Problem Formulation

The paper considers extracting a single target speaker from a noisy, reverberant mixture captured by a $C$-microphone array. In the STFT domain the additive signal model is:

$$Y_{\ell}(k, i) = X_{\ell}(k, i) + V_{\ell}(k, i),$$

stacked as $\mathbf{Y}(k, i) \in \mathbb{C}^{C}$ across channels. A traditional linear **filter-and-sum** spatial filter computes

$$\hat{S}(k, i) = \mathbf{h}(k, i)^{H}\, \mathbf{Y}(k, i),$$

e.g., the **MVDR** beamformer

$$\mathbf{h}_{\mathrm{MVDR}}(k, i) = \frac{\boldsymbol{\Phi}_{V}^{-1}(k, i)\, \mathbf{d}(k, i)}{\mathbf{d}^{H}(k, i)\, \boldsymbol{\Phi}_{V}^{-1}(k, i)\, \mathbf{d}(k, i)},$$

which is the MMSE-optimal spatial filter under a Gaussian noise assumption [10], [25]. However, the authors' prior statistical analysis [10], [27] shows that for non-Gaussian noise the MMSE-optimal filter is **non-linear and non-separable** — it cannot be decomposed into a spatial filter followed by a single-channel post-filter. This motivates the central research questions:

1. Is non-linear (vs linear) spatial filtering the main factor for good performance?
2. Or is it the *interdependency* between spatial and tempo-spectral processing?
3. Do temporal and spectral information have the same impact on spatial filtering performance?

![[raw/papers/tesch-2023-insights-deep-nonlinear-filters/figures/f013212dee5dae4c3c4fc216a9645a625bcce00cddc414a5434b29f648cf3b9e.jpg|Three processing schemes considered in the analysis]]
*Figure 1: Three processing schemes compared in the analysis. (a) Traditional two-step: linear spatial filter (beamformer) + single-channel post-filter. (b) Joint spatial and tempo-spectral non-linear filter (the JNF family). (c) Two-step with a non-linear spatial filter followed by a post-filter (the NSF + PF family).*

## Methodology

### Base Architecture (T-JNF / F-JNF / FT-JNF)

The base network (Figure 2) is adapted from Li & Horaud's narrow-band filtering [15], [39] and consists of **two bi-directional LSTM layers followed by a feed-forward (FF) layer with tanh activation**. The feature dimension carries (real, imaginary) parts of the multi-channel STFT; the sequence dimension is chosen to expose a second information source:

| Variant | Sequence dim | Available information |
|:--------|:-------------|:----------------------|
| **T-JNF** ([15]) | Time (narrow-band) | Spatial + fine-grained temporal + global spectral |
| **F-JNF** | Frequency (wide-band) | Spatial + fine-grained spectral + global temporal |
| **FT-JNF** (proposed) | Freq → Time (switched between LSTM1 and LSTM2) | Spatial + fine-grained spectral + fine-grained temporal |

FT-JNF feeds wide-band data into the first LSTM and switches to narrow-band arrangement before the second LSTM, ensuring **all three** information sources (spatial, spectral, temporal) can be exploited while keeping the parameter count identical to T-JNF/F-JNF.

### Non-linear Spatial Filter Variants (NSF)

To isolate spatial processing from tempo-spectral post-filtering, three **NSF** variants are defined (T-NSF, F-NSF, FT-NSF). The trick: **randomly permute the data along the sequence dimension** before the LSTM and apply the inverse permutation before the FF layer. This destroys fine-grained temporal/spectral correlations while preserving global statistics, so the network can only do non-linear spatial filtering using coarse per-frequency or per-time averages. The frequency-bin index is appended to the feature dimension so the network still knows which bin it is processing (without this, F-NSF performs poorly because spatial characteristics depend strongly on frequency).

### Single-Channel Post-Filter (PF)

A separate single-channel PF uses the same base architecture with real/imaginary parts stacked along the frequency dimension (feature) and time as the sequence. It is trained on the output of a given spatial filter (MVDR or FT-NSF) to study separability (Figure 1c).

### Mask, Loss, and Training

The network estimates a **complex ideal ratio mask** (cIRM) [41], compressed by a tanh with $K=C=1$ [41]:

$$\hat{S}(k, i) = \mathcal{M}_{\mathrm{S}}(k, i) \cdot Y_{0}(k, i), \qquad \mathcal{M}_{\mathrm{V}} = 1 - \mathcal{M}_{\mathrm{S}} \;(\text{real}), \; -\mathcal{M}_{\mathrm{S}} \;(\text{imag}).$$

The loss is the time+frequency $\ell_{1}$ formulation of Tolooshams et al. [17]:

$$L(s, \hat{s}) = \sum_{u \in \{s, v\}} \alpha \|u - \hat{u}\|_{1} + \big\| |U| - |\hat{U}| \big\|_{1},$$

with $\alpha = 10$ to equalize time/frequency domain contributions.

![[raw/papers/tesch-2023-insights-deep-nonlinear-filters/figures/fd64afc8656f525218233e5246b50a1614fbab41b62dafb0be4a7372dfadff71.jpg|Base system architecture]]
*Figure 2: Base system architecture. Input data is arranged wide-band or narrow-band and passed through two bi-directional LSTM layers, an FF layer, and a tanh activation to obtain a cIRM estimate that is multiplied by the reference-channel noisy STFT.*

## Experimental Setup

| Aspect | Configuration |
|:-------|:--------------|
| **Simulated dataset** (speaker extraction) | `pyroomacoustics` [43], source-image method [44]; 6000 / 1000 / 600 train / val / test samples; WSJ0 clean speech [45]; 16 kHz |
| **Rooms** | W 2.5–5 m, L 3–9 m, H 2.2–3.5 m, $T_{60}$ 0.2–0.5 s (uniformly sampled) |
| **Microphone array** | Circular, 2–5 channels, 10 cm diameter, random rotation $\varphi \in [0, 2\pi)$, height 1.5 m, ≥1 m from walls |
| **Speakers** | 1 target + 5 interfering; target on blue axis 0.3–1 m from array; interferers in gray area ≥1 m away, one per angular segment; 20° exclusion zone around target |
| **Average SNR** | −4 dB (95% of samples in [−9, 2] dB) |
| **CHiME3 dataset** [53] | 2400 / 476 / 3251 train / val / test utterances; last 4 channels; SNR {−4, 0, 4, 8} dB; cafeteria, bus, pedestrian, street |
| **STFT** | 32 ms window, 50% overlap, Hann analysis + synthesis |
| **Optimizer** | Adam [42], lr 0.001; batch size 6; max 250 epochs; best-by-validation-loss model selection |
| **LSTM hidden units** | 256 (layer 1), 128 (layer 2); PF uses 256 in both |
| **Metrics** | ΔPOLQA [46], ESTOI [49], MUSHRA CQS [51], [52] |
| **Baselines** (Section V) | T-JNF [15] (cIRM variant), CRNN [16], FaSNet+TAC [50], [35], EaBNet [19], COSPA [20] |

## Results

### Separability of Spatial and Tempo-Spectral Processing (Figure 4)

The key separability experiment (Section IV-B) compares three configurations on the speaker-extraction dataset (3 mics):

- **LSF (oracle MVDR) + PF** (Figure 1a, solid red): 0.18–0.5 POLQA gain over LSF alone, with larger gains at higher mic counts.
- **FT-NSF + PF** (Figure 1c, solid purple): post-filter adds *no* improvement — the purple line runs on top of the dashed blue FT-NSF line. Once a non-linear spatial filter has distorted speech, the post-filter cannot recover it.
- **FT-JNF** (Figure 1b, solid orange): **outperforms** oracle MVDR + PF at low microphone counts by up to **0.44 POLQA at 2 mics**. The gap closes/inverts at higher mic counts because each additional mic lets the oracle MVDR null one more interferer.

![[raw/papers/tesch-2023-insights-deep-nonlinear-filters/figures/1c1c9cccd1deeba0e11d1822da933437367bd14b1618a9dea8dbc8e13f808ece.jpg|POLQA and ESTOI vs microphone count for separability comparison]]
*Figure 4: Mean POLQA and ESTOI vs number of microphones for the separability comparison. Joint spatial + tempo-spectral filtering (FT-JNF, orange) outperforms a non-linear spatial filter + post-filter (FT-NSF+PF, purple) and the oracle MVDR + post-filter (red) at low microphone counts.*

### Interdependency: Spectral vs Temporal Information (Table II)

At 3 microphones, ΔPOLQA and ESTOI improvements:

| Variant | ΔPOLQA | ESTOI |
|:--------|:-------|:------|
| F-NSF (spatial + global spectral) | 0.78 ± 0.03 | 0.62 ± 0.012 |
| T-NSF (spatial + global temporal) | 0.46 ± 0.03 | 0.54 ± 0.013 |
| FT-NSF (spatial + global both) | 0.87 ± 0.03 | 0.64 ± 0.011 |
| F-JNF (spatial + fine spectral) | 1.15 ± 0.04 | 0.70 ± 0.011 |
| T-JNF [15] (spatial + fine temporal) | 0.74 ± 0.03 | 0.63 ± 0.012 |
| **FT-JNF (proposed)** | **1.43 ± 0.04** | **0.76 ± 0.009** |

**Spectral information contributes 0.32 POLQA more than temporal information** when added to spatial processing (F-NSF vs T-NSF), and this gap is preserved in the joint case (F-JNF vs T-JNF: 0.41 POLQA). This is explained by Fig. 6: spectral information narrows the spatial selectivity pattern more sharply than temporal information does.

### State-of-the-Art Comparison (Figure 7, Table III)

On the speaker-extraction dataset, FT-JNF outperforms all five baselines by at least **0.22 POLQA** and **0.04 ESTOI**, despite having the **fewest parameters (1.2 M)**. A MUSHRA listening test (12 examples, 11 participants) ranks FT-JNF first with CQS 67.9, vs. EaBNet second at 53.1 — an audible quality difference. The best-performing baseline (EaBNet [19]) uses a filter-and-sum architecture explicitly inspired by traditional beamforming, but the mask-based FT-JNF beats it, contradicting the common belief that beamformer-inspired designs have superior spatial filtering.

| Method | LR | STFT [ms] | #Param. [M] | POLQA | MUSHRA CQS |
|:-------|:---|:----------|:------------|:------|:-----------|
| **FT-JNF (proposed)** | 0.001 | 32 | **1.2** | **1.43** | **67.9** |
| T-JNF [15] | 0.001 | 32 | 1.2 | 0.74 | — |
| CRNN [16] | 0.0001 | 32 | 17.4 | — | — |
| FaSNet+TAC [50], [35] | 0.0001 | — | 4.1 | — | — |
| EaBNet [19] | 0.001 | 20 | 2.8 | — | 53.1 |
| COSPA [20] | 0.0001 | 64 | 2.1 | — | — |

![[raw/papers/tesch-2023-insights-deep-nonlinear-filters/figures/1e143b7fa5fc33fb5c31e53f8e34f8e6453736ce2e6ae37aaf3412b7785bb0ec.jpg|SOTA comparison POLQA, ESTOI, and MUSHRA CQS]]
*Figure 7: Performance comparison of FT-JNF and five baselines on the speaker-extraction dataset. Top: mean ESTOI; middle: mean POLQA with 95% CI; bottom: MUSHRA CQS over 12 randomly selected examples. FT-JNF consistently ranks first despite having the fewest learnable parameters.*

### Spatial Selectivity of FT-JNF vs EaBNet (Figures 8, 9)

To investigate *why* FT-JNF beats the filter-and-sum-style EaBNet, the authors present the trained networks with white-noise signals from variable incidence angles in an anechoic room (out-of-distribution, but spatially consistent with training). The resulting response patterns (Figure 8) resemble traditional directivity patterns but, because the DNN filters are non-linear, cannot be interpreted exactly like classical beampatterns.

![[raw/papers/tesch-2023-insights-deep-nonlinear-filters/figures/a2deeea5aacc166dbd27aa97599db183e3005539ce41f414fc5edfd9fb63ce7c.jpg|White-noise response pattern for FT-JNF]]
![[raw/papers/tesch-2023-insights-deep-nonlinear-filters/figures/6bc9a861b0b9261f1531168d6a75b9be767e98a281dec66747047ed76bb81851.jpg|White-noise response pattern for EaBNet]]
*Figure 8: White-noise response patterns of FT-JNF (top) and EaBNet (bottom) for variable incidence angle (x-axis) and frequency (y-axis). FT-JNF shows a sharp, well-localized beam aligned with the 0° target direction and matching the ±20° noise-free section of the training setup; EaBNet's beam is wider and suppresses non-target directions poorly at high frequencies.*

![[raw/papers/tesch-2023-insights-deep-nonlinear-filters/figures/000c535fa97bbd02e05503653510692933760c6969ba8b2a08147de23d51896f.jpg|Spatial selectivity of FT-JNF vs EaBNet on clean speech]]
*Figure 9: Mean POLQA score and 95% CI for a clean/anechoic speech signal arriving from variable incidence angle. FT-JNF (blue) passes signals from the target direction unaltered; EaBNet (orange) degrades the clean target speech even when it arrives from the target direction — explaining the performance gap in Figure 7.*

### CHiME3 Results (Table IV)

POLQA improvement by noise type on CHiME3:

| Method | BUS | CAF | PED | STR |
|:-------|:----|:----|:----|:----|
| F-JNF | 1.16 ± 0.05 | 1.17 ± 0.05 | 1.08 ± 0.04 | 1.35 ± 0.03 |
| T-JNF [15] | 1.30 ± 0.03 | 1.23 ± 0.03 | 1.11 ± 0.03 | 1.45 ± 0.03 |
| **FT-JNF (proposed)** | **1.53 ± 0.04** | **1.56 ± 0.04** | **1.45 ± 0.04** | **1.76 ± 0.03** |
| CRNN [16] | 0.89 ± 0.04 | 0.90 ± 0.04 | 0.83 ± 0.04 | 1.02 ± 0.03 |
| FaSNet+TAC | 0.61 ± 0.03 | 0.53 ± 0.03 | 0.51 ± 0.02 | 0.61 ± 0.02 |
| EaBNet [19] | 1.19 ± 0.04 | 1.18 ± 0.04 | 1.08 ± 0.04 | 1.31 ± 0.03 |
| COSPA [20] | 0.60 ± 0.03 | 0.61 ± 0.03 | 0.56 ± 0.03 | 0.65 ± 0.03 |

**Notable dataset reversal**: on CHiME3, **T-JNF outperforms F-JNF** — the opposite of the speaker-extraction dataset. The authors attribute this to the noise characteristics: CHiME3 noise is more stationary and tempo-spectrally distinct from speech, so single-channel tempo-spectral processing carries most of the gain and the spatial component is less decisive. The spatial selectivity plots of Fig. 10 confirm that F-JNF's spatial pattern is much narrower than T-JNF's, but T-JNF still wins on CHiME3 because temporal information (not reflected in the spatial plot) compensates. FT-JNF — by using all three information sources — wins on both datasets, gaining 0.23 POLQA over F-JNF on CHiME3.

The spatial selectivity maps of Fig. 10 also reveal that CHiME3 effectively has a fixed (only slightly variable) target speaker position relative to the microphone-array orientation — a fact "easily forgotten as the target speaker positions in the CHiME3 dataset are unknown". Performance improvements on CHiME3 therefore cannot be blindly attributed to better spatial filtering without further analysis.

## Key Contributions

1. **Conceptual superiority of joint non-linear filtering over oracle linear filtering**: Demonstrates that a DNN-based joint non-linear spatial + tempo-spectral filter (FT-JNF) outperforms an **oracle** MVDR beamformer + post-filter at low microphone counts (up to 0.44 POLQA at 2 mics) — empirically validating the theoretical MMSE non-separability result of [10], [27] for non-Gaussian noise.
2. **Spectral > temporal information for spatial filtering**: A controlled ablation (F-NSF vs T-NSF, F-JNF vs T-JNF) shows that fine-grained spectral information contributes 0.32–0.41 POLQA more to spatial-filtering performance than temporal information, and Fig. 6 traces the cause to spectral information narrowing the spatial selectivity pattern more sharply.
3. **NSF variant family as a methodological tool**: Introduces the permutation-trick (randomly permute the sequence dimension before the LSTM, undo before the FF) to construct non-linear spatial filters that have only *global* tempo-spectral statistics — enabling clean isolation of spatial processing from tempo-spectral post-filtering.
4. **FT-JNF architecture**: A two-LSTM + FF architecture that switches from wide-band (frequency-as-sequence) to narrow-band (time-as-sequence) arrangement between the two LSTM layers, exploiting all three information sources without changing the parameter count vs T-JNF. Outperforms five SOTA baselines (T-JNF, CRNN, FaSNet+TAC, EaBNet, COSPA) by ≥0.22 POLQA on speaker extraction and ≥0.32 POLQA on CHiME3, with the **fewest parameters (1.2 M)**.
5. **Dataset-characteristic-aware analysis**: Reveals that the spectral-vs-temporal ranking **reverses** between the speaker-extraction dataset (F-JNF > T-JNF) and CHiME3 (T-JNF > F-JNF), tracing the cause to noise stationarity and tempo-spectral distinctness — a cautionary finding that improvements on CHiME3 cannot be attributed to spatial filtering without further analysis.
6. **Spatial selectivity forensics**: Develops two visualization techniques — (i) clean/anechoic speech from variable incidence angle measured by POLQA, (ii) white-noise response patterns in dB per angle and frequency — that explain *why* FT-JNF beats the beamformer-inspired EaBNet baseline (sharper beam, no clean-speech distortion at 0°).

## Related Concepts

- [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering (JNF / FT-JNF)]]
- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]
- [[concepts/mcnet|McNet (Multi-Cue Network)]]
- [[concepts/neural-directional-filtering|Neural Directional Filtering (NDF)]]
- [[concepts/beamforming|Beamforming]] (MVDR baseline, oracle MVDR)
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]
- [[concepts/complex-ratio-mask|Complex Ratio Masking (cIRM)]]
- [[concepts/neural-beamforming|Neural Beamforming]] (DNN-driven linear spatial filters, e.g. Heymann et al. [11], FaSNet, EaBNet, COSPA)

## Related Sources

- [[sources/tesch-2024-spatially-selective-nonlinear-filters|Tesch & Gerkmann 2024: Multi-channel Speech Separation Using Spatially Selective Deep Non-linear Filters]] — 2024 journal extension introducing the DOA-steered SSF built on FT-JNF
- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]] — extends FT-JNF with dual coherent/diffuse masks for virtual directional microphone reconstruction
- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova 2023: Neural Target Speech Extraction Overview]] — surveys TSE including DOA-based spatial-clue variants that overlap with the speaker-extraction task here
- [[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng 2023: Survey of Frequency-Domain Speech Enhancement]] — surveys the broader DNN-based multi-channel speech enhancement landscape that this paper analyzes

## Related Synthesis

- [[synthesis/deep-speech-enhancement|Deep Speech Enhancement]] — multi-channel DNN filtering frontier, where FT-JNF's (params, MACs, quality) tuple is a new data point
