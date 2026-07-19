---
type: source
created: 2026-07-19
updated: 2026-07-19
sources:
  - raw/papers/zheng-2023-survey-frequency-domain-speech-enhancement/full-text.md
  - https://doi.org/10.1177/23312165231209913
  - https://github.com/cszheng-ioa/Sixty-years-of-frequency-domain-monaural-speech-enhancement
tags:
  - speech-enhancement
  - survey
  - frequency-domain
  - deep-learning
  - traditional-methods
  - hearing-aids
  - audio-processing
---

# Zheng, Zhang, Liu, Luo, Li, Li & Moore 2023: Sixty Years of Frequency-Domain Monaural Speech Enhancement

**Authors**: [[entities/chengshi-zheng|Chengshi Zheng]]¹²*, [[entities/huiyong-zhang|Huiyong Zhang]]¹², Wenzhe Liu¹², Xiaoxue Luo¹², Andong Li¹², [[entities/xiaodong-li|Xiaodong Li]]¹², [[entities/brian-c-j-moore|Brian C. J. Moore]]³*
**Affiliations**: ¹Key Laboratory of Noise and Vibration Research, Institute of Acoustics, Chinese Academy of Sciences, Beijing; ²University of Chinese Academy of Sciences, Beijing; ³Cambridge Hearing Group, Department of Psychology, University of Cambridge, UK
**Venue**: Trends in Hearing, Volume 27, pp. 1–52, 2023
**DOI**: [10.1177/23312165231209913](https://doi.org/10.1177/23312165231209913)
**Code**: [cszheng-ioa/Sixty-years-of-frequency-domain-monaural-speech-enhancement](https://github.com/cszheng-ioa/Sixty-years-of-frequency-domain-monaural-speech-enhancement)
**Funding**: National Key R&D Program of China (2021YFB3201702)
**Received**: 2 Dec 2022; **Accepted**: 9 Oct 2023

## Summary

A comprehensive survey of frequency-domain monaural speech enhancement methods spanning 60 years (from Schroeder's 1965 analog noise suppressor through 2022 deep-learning architectures). The paper reviews both traditional statistical/heuristic methods (organized around five key modules: noise estimation, a priori SNR estimation, speech-presence probability, spectral gain, and phase) and deep-learning methods (organized by four training-stage modules: feature extraction, network architecture, training target, and loss function). A unified objective evaluation of 17 representative methods is conducted on the WSJ+DNS and Voice Bank+DEMAND datasets using PESQ, ESTOI, SDR, DNSMOS, and — uniquely — HASQI/HASPI metrics simulating both normal-hearing and hearing-impaired listeners (audiograms N2 mild, N3 moderate). The survey's central thesis is that the fundamental assumptions of traditional methods (independence of T-F bins, quasi-stationary noise, magnitude-only processing) explain their poor performance in nonstationary low-SNR conditions, and that deep-learning methods achieve gains precisely by implicitly relaxing these assumptions.

## Taxonomy

The survey proposes a five-group taxonomy of frequency-domain monaural speech enhancement methods, organized by the underlying estimation strategy:

| Group | Methods | Estimation Target | Phase Processed? |
|-------|---------|-------------------|------------------|
| 1. Traditional | MMSE-LSA, MMSE-STSA (β=1, 0.5), MSS, PSS, SQ-MSS | Spectral gain G(k,l) | No (noisy phase reused) |
| 2. Hybrid (DeepXi) | DeepXi-LSA, DeepXi-STSA | A priori SNR → spectral gain | No |
| 3. Magnitude-mapping DNN | LSTM, FullSubNet, CRN | |S(k,l)| via magnitude mapping | No |
| 4. Complex-spectrum DNN | GCRN, DPCRN, Uformer, DCCRN, DCCRN(SNR) | S_r(k,l), S_i(k,l) directly | Yes (implicitly) |
| 5. Decoupling-style DNN | CTSNet, G2Net (GaGNet), TaylorSENet | Magnitude + residual complex (decoupled) | Yes (explicitly) |

A secondary taxonomy classifies traditional methods by their statistical assumption: Gaussian (Ephraim & Malah 1984/1985), Gamma (Martin 2002), Laplacian (Chen & Loizou 2007), Super-Gaussian (Breithaupt & Martin 2003), and combined stochastic-deterministic (Hendriks et al. 2007; McCallum & Guillemin 2013). Spectral subtraction is treated as a separate heuristic class (Boll 1979; Berouti et al. 1979).

## Methodology (Surveyed Methods)

### Traditional Methods — Five Modules

The survey synthesizes the traditional pipeline around five inter-dependent modules, each with a clear lineage:

1. **Noise PSD Estimation** — VAD-based (Lim, Boll, McAulay & Malpass, Ephraim & Malah) → VAD-free recursive (Hirsch & Ehrlicher 1995; Doblinger 1995) → minimum statistics (Martin 1994, 2001) → minima-controlled recursive averaging / MCRA (Cohen 2003) → MMSE-based (Hendriks et al. 2010; Gerkmann & Hendriks 2012). MMSE-based methods achieved the best log-error performance among traditional estimators and became the de-facto standard.

2. **A Priori SNR Estimation** — decision-directed method (Ephraim & Malah 1984; Cappé 1994 analysis of musical-noise suppression) → two-stage SNR (Breithaupt et al. 2008) → cepstro-temporal smoothing. The decision-directed method remains the dominant approach.

3. **Speech Presence Probability (SPP)** — two-state model (McAulay & Malpass 1980) → soft-decision SPP (Malah et al. 1999) → controlled SPP (Cohen & Berdugo 2001). The combined SPP–spectral gain formulation gives the spectral gain form G(k,l) = (G_H1)^p · (G_min)^(1-p).

4. **Spectral Gain Estimation** — MMSE-STSA (Ephraim & Malah 1984), MMSE-LSA (Ephraim & Malah 1985), β-order MMSE-STSA (Breithaupt et al. 2008), spectral subtraction family (MSS, PSS, SQ-MSS), Wiener filter, log-MMSE.

5. **Phase Processing** — phase-aware mask recovery was limited in traditional methods because accurate phase requires accurate magnitude; modern phase-gradient-heap-iteration (PGHI) approaches were reviewed but concluded to be bottlenecked by magnitude-estimation accuracy.

### Deep Learning Methods — Four Training Modules

1. **Feature Extraction** — LOG-AMP, log-power spectrum, spectral amplitudes raised to power α_cp ∈ (0,1] (cube-root compression typically best), real+imaginary complex spectrum (Tan & Wang 2020), perceptually-motivated features (Bark-scale BFCCs by Valin 2018; ERB-band features by Valin et al. 2020 — 42 features → 800 MMAC/s). Compressed complex spectrum Y_cp(k,l) = |Y|^α_cp · exp(j∠Y) is the dominant modern input.

2. **Network Architecture** — DNN (Xu et al. 2014) → RNN/LSTM (Chen & Wang 2017; Sun et al. 2017; RNNoise/GRU by Valin 2018) → CRN (Tan & Wang 2018) → complex networks (complex U-Net by Choi et al. 2019; DCCRN by Hu et al. 2020, won DNS Challenge 1) → dual-path RNN (DPCRN by Le et al. 2021) → dual-branch / decoupling (CTSNet, G2Net, TaylorSENet). Progressive/task-decoupled learning reviewed (Gao et al. 2016; PHASEN by Yin et al. 2020; Uformer by Fu et al. 2022; masking-and-inpainting by Hao et al. 2020; SDDNet by Li et al. 2021b).

3. **Training Target** — masking-based (IBM Wang & Wang 2013, IRM Narayanan & Wang 2013, PSM Erdogan et al. 2015, [[concepts/complex-ratio-mask|cIRM]] Williamson et al. 2016) vs. mapping-based (magnitude, log-power spectrum, complex spectrum mapping by Tan & Wang 2019/2020, compressed complex spectrum by Li et al. 2021d).

4. **Loss Function** — frequency-domain (Mag-MSE, RI-MSE, combined RI+Mag, log-spectral, power-law-compressed), time-domain (SA, SDR, SNR), perceptually-motivated. The "compensation effect" (Wang et al. 2021; Luo et al. 2022) describes the magnitude/phase trade-off in RI-MSE. DCCRN(SNR) variant demonstrates loss choice can be more important than minor architecture changes.

### Hybrid Methods

Group 2 (DeepXi) is identified as a distinctive hybrid: deep learning estimates the a priori SNR (a traditional key parameter), and the spectral gain is then computed via the traditional formula. The framework confirms the a priori SNR is the central magnitude-estimation parameter for the speech-enhancement task.

## Applications Survey

The survey evaluates all five groups on two datasets and four listener configurations:

### Datasets

- **WSJ + DNS Challenge** — broad SNR coverage (-5, 0, 5, 10 dB); three noise types (FactoryI, Cafe, Babble).
- **Voice Bank + DEMAND** — relatively high SNR (~10 dB average), 28 speakers; the de-facto benchmark.

### Listener Models

- **Normal-hearing** — audiometric thresholds 0 dB HL at 250/500/1000/2000/4000/6000 Hz.
- **Hearing-impaired** — Bisgaard et al. (2010) standard audiograms N2 (mild sloping) and N3 (moderate sloping), with NAL-R prescribed gain (Byrne & Dillon 1986); input normalized to 65 dB SPL RMS.

### Per-Domain Findings and Best Variants

| Listener group / metric | Best deep-learning variant | Best traditional / hybrid | Key finding |
|--------------------------|---------------------------|---------------------------|-------------|
| Normal-hearing, low SNR (≤ 0 dB) | Decoupling-style (CTSNet, G2Net, TaylorSENet) | Hybrid DeepXi | DL ≫ traditional; decoupling > single-stage complex mapping |
| Normal-hearing, high SNR (≥ 10 dB) | Uformer, TaylorSENet | Hybrid DeepXi (competitive) | Marginal DL benefit; hybrid competitive |
| Hearing-impaired (HASQI / HASPI), mild loss | CTSNet, G2Net, TaylorSENet | MSS / SQ-MSS (better than MMSE-LSA) | **Compression does NOT help hearing-impaired** (opposite of normal-hearing) |
| Voice Bank + DEMAND, NB-PESQ (uncompressed) | CTSNet, TaylorSENet | Hybrid DeepXi | DL sometimes *worse* than traditional NB-PESQ when uncompressed |
| Voice Bank + DEMAND, NB-PESQ (compressed) | Uformer (3.64), TaylorSENet (3.62) | — | Compression widens DL advantage |
| Resource-constrained (smallest DL model) | DPCRN (0.72M params, 0.77 GMAC/s) | Traditional (<5K params, <10 MMAC/s) | Hybrid is 2nd smallest; better performance does *not* require more compute |

### Model Size / Complexity Comparison (Table 14)

| Model | Size (M) | MACs (G/s) |
|-------|---------:|-----------:|
| DeepXi | 1.95 | 0.12 |
| LSTM | 21.82 | 2.19 |
| FullSubNet | 5.64 | 29.83 |
| CRN | 17.58 | 2.57 |
| GCRN | 9.77 | 2.42 |
| **DPCRN** | **0.72** | **0.77** |
| Uformer | 3.34 | 5.29 |
| DCCRN | 3.67 | 11.13 |
| CTSNet | 4.35 | 5.57 |
| G2Net | 7.39 | 2.83 |
| TaylorSENet | 5.45 | 6.43 |

## Key Contributions

1. **Unified five-group taxonomy** of frequency-domain methods (traditional → hybrid → magnitude-mapping DL → complex-spectrum DL → decoupling-style DL), framed by which assumptions each group relaxes.
2. **First unified head-to-head evaluation** of 17 representative methods on the same WSJ+DNS and Voice Bank+DEMAND corpora with the same train/test pipeline and metrics — prior surveys did not provide this.
3. **Dual-listener evaluation via HASQI/HASPI** with standard audiograms (N2/N3, NAL-R gain) — quantifies the surprising finding that input-feature compression helps normal-hearing but *not* hearing-impaired listeners.
4. **Synthesis of the magnitude–phase trade-off** ("compensation effect"): single-stage complex-spectrum networks trade magnitude distortion for phase recovery; decoupling-style architectures (CTSNet, G2Net, TaylorSENet) resolve this by separately optimizing magnitude and residual complex spectrum.
5. **Complexity–performance decoupling**: documented empirically that better DL performance does not require greater storage (e.g., DPCRN at 0.72M params outperforms LSTM at 21.82M; decoupling-style methods at ~5M outperform DCCRN at 3.67M despite more parameters).
6. **Open challenges enumeration** — (a) reducing algorithmic delay below 4 ms for hearing aids (Tammen & Doclo 2021, 2022), (b) interpreting DL "black boxes" theoretically, (c) multitalker scenarios, (d) subjective validation for hearing-impaired listeners.

## Limitations and Caveats

- **Literature cutoff ~ mid-2022**: post-2022 efficient variants (e.g., NSNet2 evolution, GTCRN, PercepNet, Bark-AEC, full-band Codex/Stereo DNS systems) are not surveyed.
- **Hearing-impaired modeling limited to mild/moderate sloping losses (N2/N3)**: steeply sloping audiograms and severe/profound losses not evaluated; only two audiograms from Bisgaard et al. (2010) standard set used.
- **Objective metrics only**: no subjective listening tests with normal-hearing or hearing-impaired participants — the authors explicitly call for these.
- **Dereverberation coverage is brief**: the survey focuses on denoising; dereverberation is mentioned only as an extension under the late-reverberation-uncorrelated-with-direct assumption.
- **No binaural / multi-channel methods**: scope is strictly monaural; binaural extensions (e.g., Tammen & Doclo 2022) only briefly mentioned in future work.
- **"Best variant" recommendations are dataset- and metric-dependent**: the relative ranking of CTSNet, G2Net, TaylorSENet, Uformer shifts with input-feature compression and listener group — the survey explicitly notes (Section "Results for the WSJ + DNS Dataset") that "a more recent method did not always work better than earlier ones when the input feature changed".
- **The GaGNet/G2Net nomenclature is used interchangeably** in the source paper; the same architecture is referred to as both "G2Net" (in tables) and "GaGNet" (in description).

## Related Concepts

- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask]]
- [[concepts/frequency-domain-loss|Frequency Domain Loss for Time-Domain Networks]]
- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[concepts/nsnet2|NSNet2]]
- [[concepts/gtcrn|GTCRN]]
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]]

## Related Sources

- [[sources/seidel-2024-bark-scale-nn-residual-suppression|Seidel, Mowlaee & Fingscheidt 2024: Bark-Scale NN for Residual Echo and Noise Suppression]] — extends the survey's discussion of perceptually-motivated (Bark) features and efficient architectures.
