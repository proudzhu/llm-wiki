---
type: source
created: 2026-08-20
updated: 2026-08-20
sources:
  - raw/papers/ansari-2023-ai-bss-survey/full-text.md
  - https://doi.org/10.1016/j.neucom.2023.126895
  - zotero://select/items/0_ND66R5YG
tags:
  - blind-source-separation
  - survey
  - machine-learning
  - deep-learning
  - evolutionary-algorithms
  - artificial-intelligence
  - audio-source-separation
---

# Ansari, Alatrany, Alnajjar et al. 2023: A Survey of AI Approaches in BSS

**Authors**: [[entities/sam-ansari|Sam Ansari]]<sup>a</sup>, [[entities/abbas-saad-alatrany|Abbas Saad Alatrany]]<sup>b</sup>, [[entities/khawla-a-alnajjar|Khawla A. Alnajjar]]<sup>a</sup>, [[entities/tarek-khater|Tarek Khater]]<sup>a</sup>, [[entities/soliman-mahmoud|Soliman Mahmoud]]<sup>a</sup>, [[entities/dhiya-al-jumeily|Dhiya Al-Jumeily]]<sup>b</sup>, [[entities/abir-jaafar-hussain|Abir Jaafar Hussain]]<sup>a,b,*</sup>

**Affiliations**: <sup>a</sup>Department of Electrical Engineering, University of Sharjah, UAE; <sup>b</sup>School of Computer Science and Mathematics, Liverpool John Moores University, UK

**Venue**: Neurocomputing, Vol. 552, 2023, pp. 126895 (article number)
**Published**: 2023-12-07
**DOI**: [10.1016/j.neucom.2023.126895](https://doi.org/10.1016/j.neucom.2023.126895)
**Zotero**: [ND66R5YG](zotero://select/items/0_ND66R5YG)
**Type**: Survey / Systematic literature review

## Summary

This paper presents a systematic literature survey of **blind source separation (BSS)** with a particular focus on **artificial-intelligence-based frameworks**. The authors review ~60 state-of-the-art BSS studies spanning 2003–2023 and propose a **three-way taxonomy** of AI-based BSS approaches: (i) **classical machine-learning methods** (FNN, MLP, SVM, clustering, fuzzy logic, BNN, ANN, KAM, RF, etc.), (ii) **deep-learning methods** (DNN, RNN, CNN, BLSTM, DRNN, GAN, DAN, deep clustering, CDAE, VAE, Transformer-based networks such as Conv-TasNet/SepFormer/Demucs), and (iii) **evolutionary/swarm-intelligence methods** (PSO, GA, ABC, BCO, ACO, DE, FPA, BCC, cat swarm, DNPSO, quantum GA, etc.). The survey benchmarks these methods across audio, speech, music, voice, and source separation applications, and identifies research gaps in speed/accuracy trade-off, robustness, scalability, underdetermined convolutive cases, nonlinear mixing, and edge/mobile deployment.

## Taxonomy

The survey's distinctive contribution is its **three-way classification of AI-based BSS techniques**. This taxonomy is depicted in Fig. 3 ("existing BSS techniques"), Fig. 10 (tree chart of surveyed approaches), and consolidated in Table 9 of the paper.

![[raw/papers/ansari-2023-ai-bss-survey/figures/a91e24bf7fcff31c7f6ee0fcbdd753ffc19f99539b988c8d982c6f4e3fee7b44.jpg|Figure 3: The existing BSS techniques.]]

*Figure 3: The existing BSS techniques.*

![[raw/papers/ansari-2023-ai-bss-survey/figures/0d97ecb6305fbc5d4dc11790f41c4ff805d2166a4a16fff227eab047ead1754b.jpg|Figure 10: Tree chart of surveyed BSS approaches.]]  
*Figure 10: Tree chart of the surveyed BSS approaches.*

| Approach | Representative algorithms | References surveyed |
|----------|---------------------------|---------------------|
| **Classical machine learning** | FNN, variational Bayes, variational Bayes EM, customized EM, MLP, WMM-MAP, MAP, DBSCAN, K-means, AP, SVM, fuzzy c-means, NN, RBF, CSKC, BNN, ANN, KAM, RF, IBM, K-hyperline clustering, CFSFDP, bigradient neural network | [89, 102–109, 111–113, 115–123, 135, 149–161, 174] |
| **Deep learning** | DNN, RNN, CNN, Conv-TasNet, BLSTM, DRNN, GAN, DAN, deep clustering, GRU, LSTM, deep fully CDAE, BRNN, mixed-type detection hierarchical DNN, VAE, GAN+VAEM, Transformer-based networks (SepFormer, Demucs) | [86, 97, 124–126, 129–137, 162–172] |
| **Evolutionary / swarm intelligence** | PSO, GA, CGA, BCO, ACO, DE, ABC, HEPSO, QPSO, BCC, BCA, DNPSO, quantum GA, FPA, cat swarm | [138–140, 142–148, 173–182] |

## Problem Formulation

The survey adopts the standard linear instantaneous BSS model. With $M$ sources $\mathbf{S} = [S_1, S_2, \dots, S_M]^T$ mixed by an unknown $N \times M$ matrix $A$, the observed signals are:

$$\mathbf{X} = A\,\mathbf{S} \tag{1}$$

The BSS goal is to recover a separating matrix $B$ such that the estimated signals $\mathbf{Y} = B\,\mathbf{X}$ are statistically independent and equal (up to permutation and scaling) to the original sources:

$$\mathbf{Y} = B\,\mathbf{X} \tag{2}$$

The survey notes that the term "blind" reflects two unknowns: (i) the source signals are not directly observable, and (ii) the mixing system is unknown. The complexity of the BSS problem depends on whether the mixture is **determined** ($M = N$), **over-determined** ($M < N$), or **underdetermined** ($M > N$); the latter is the hardest and requires sparsity or learned priors.

![[raw/papers/ansari-2023-ai-bss-survey/figures/ab4816fe753c17c138079a27639c681035765dd13c8775da77fb2229990da910.jpg|Figure 1: Schematic diagram of BSS in linear space.]]
*Figure 1: Schematic diagram of BSS in linear space.*

## Methodology (Surveyed Methods)

### 3.1 Sparse Approximation Foundation

Sparse representation underpins many BSS methods. The survey introduces the (P0) problem:

$$(P_0):\ \min_{x}\ \lVert x \rVert_0\quad \text{s.t.}\quad y = Dx \tag{3}$$

where $D$ is a dictionary of atoms and $\lVert\cdot\rVert_0$ is the $\ell_0$ pseudo-norm. Because (P0) is NP-hard, convex relaxations (e.g., $\ell_1$) or greedy algorithms are used in practice. **Sparse component analysis (SCA)** and **sparse coding** are listed as the prominent BSS techniques that exploit sparsity. Sparse representations also enable underdetermined separation by exploiting the low probability that two sources are simultaneously active at the same sparse-space point.

### 3.2 Classical vs. Deep Learning

The survey distinguishes ML from DL along three axes:

- **Linearity**: classical ML is largely linear; DL models are hierarchical.
- **Feature extraction**: classical ML requires a separate feature-extraction step; DL embeds it inside the model via end-to-end learning.
- **Data scaling**: classical ML plateaus as data grows; DL improves with more data.

![[raw/papers/ansari-2023-ai-bss-survey/figures/2860fc45d5193b4f86f7d39aa9c0c9915230c44498f04c388022d83560124fbc.jpg|Figure 9: Overall structure and difference between ML and DL.]]
*Figure 9: Overall structure and difference between ML and DL.*

### 3.3 Research Protocol

The survey follows a systematic-literature-review protocol with explicit selection steps (Figs. 4–8): define essentials → design review protocol → search digital libraries → filter by criteria → categorize by type/year/library → analyze. The final pool contains ~60 papers, with the largest contributions in 2014–2017 and 2021.

![[raw/papers/ansari-2023-ai-bss-survey/figures/8e86a2f3fd2205ec7b5832e586d52666f232e5445419471609dd86257996604d.jpg|Figure 4: Main steps of the research protocol.]]
*Figure 4: Main steps of the research protocol.*

![[raw/papers/ansari-2023-ai-bss-survey/figures/463e01401a9f8cd489f6024e71419e58fd559440a7611b99ccd6ec1c22a9f258.jpg|Figure 5: Procedure followed to analyze the developed systems and studies.]]
*Figure 5: Procedure followed to analyze the developed systems and studies.*

![[raw/papers/ansari-2023-ai-bss-survey/figures/dbdc79a9d9ac4a6d50d32be3bc8c9f8bbcfa807f5311af7683ddc209c1c71939.jpg|Figure 6: Annual trend of selected research articles.]]
*Figure 6: Annual trend of selected research articles.*

![[raw/papers/ansari-2023-ai-bss-survey/figures/5ec12967a9d52626cad206509241a12231bcdeb36ec685b0589cc44231a3320b.jpg|Figure 7: Annual contribution of selected papers in the final pool.]]
*Figure 7: Annual contribution of selected papers in the final pool.*

![[raw/papers/ansari-2023-ai-bss-survey/figures/881a100515d51100b508942b2463cd494552871f9fffaa644f1960050251db83.jpg|Figure 8: Final pool of relevant studies.]]
*Figure 8: Final pool of relevant studies providing complete information about the selected papers.*

## Applications Survey

The selected studies are split into audio, speech, music, sound, voice, and source separation categories. Per-method performance is heterogeneous because different studies use different metrics (SAR/SDR/SIR/SNR/PI/AVCC/MSE/PESQ/accuracy), datasets, and signal types — making fair cross-study comparison difficult.

### Classical Machine Learning Methods (Section 4.1.1)

The survey benchmarks classical-ML BSS methods in Table 1. Notable findings:

- **FCRNN with self-feedback** [102] avoids local minima and suits nonlinear mixing.
- **Variational Bayes** [103, 104] models underdetermined mixtures frequency-bin-wise and can determine the actual source count automatically.
- **WMM-MAP** [108] reaches SDR 5.80 dB / SIR 13.00 dB on audio.
- **K-means + AP clustering** [112] achieves SIR 14.43 dB / SDR 8.09 dB.
- **Gaussianity + Sparsity** [113] reaches SIR 38.93 dB on audio (the strongest classical-ML SIR).
- **FastICA contrast functions** [122]: ML outperforms Kurtosis and Negentropy in noisy environments; the contrast function reaches SDR 49.70 dB / SIR 51.33 dB / SAR 54.76 dB on synthetic data.
- **NN + ML with dual acceleration** [123] quadruples convergence speed and improves steady-state performance by up to 96% relative to prior methods.

### Deep Learning Methods (Section 4.1.2)

Table 5 compares DL-based methods. Notable findings:

- **DNN for noise-robust ASR** [124]: DNN estimates a clean target-sound feature vector and outperforms ICA / nonlinear PCA, especially in low-SNR directional noise.
- **Hybrid DNN + multi-channel Gaussian model** [86, 125]: each DNN enhances spectra from the prior EM iteration; outperforms single-channel DNN and multichannel NMF baselines.
- **Multi-DNN TF-mask ensemble** [126]: four DNNs with different cost functions (softmax, IBM, direct source, discriminative constraint) jointly predict masks; ensemble beats single DNNs.
- **CNN pixel-wise classifier** [133] converts BSS into pixel-wise spectrogram classification, eliminating pre/post-processing; up to +5.96 dB improvement.
- **DAN+BLSTM** [168]: SDR 17.4 / 16.5 / 14.0 dB on speech — the strongest DL SDR in the survey.
- **GAN+VAEM** [172]: SAR 18.20 / SDR 17.10 / SIR 29.55 dB on handwritten and spectrogram sources — strongest combined metrics in the DL pool.
- **CNN+RNN+LSTM+GRU** [161] for voice-operated IoT: 98% accuracy.
- **Hierarchical DNN with mixed-type detection** [171]: SDR 7.74 dB / SIR 14.02 dB / PESQ-improved on speech.

### Evolutionary Algorithms (Section 4.1.3 / 4.2.3)

Table 6 benchmarks evolutionary methods. Notable findings:

- **MABC with covariance ratio** [177]: AVCC 0.99857, MSE 1.983e-4, SNR 25.84 dB on speech/music — strongest evolutionary SNR.
- **BCA** [176]: SNR 22.75 / 19.44 dB on speech/images.
- **DNPSO** [178]: correlation coefficient 0.9989 on speech.
- **FPA** [181]: correlation coefficient 0.9568 on speech.
- **Quantum GA + RBF** [179]: accuracy 0.8898 on nonlinear signals.
- **ABC permutation alignment** [173]: SDR 1.85 / SIR 5.67 / SAR 8.04 dB on speech — weakest evolutionary result.
- **Cat swarm + phase-space reconstruction** [182]: faster convergence via orthogonal-matrix parametrization.

### Computational Complexity Comparison (Tables 7 & 8)

| Method class | Complexity range | Notes |
|--------------|------------------|-------|
| Classical ICA / FastICA / NMF / SCA / JADE / SOBI / JD / CCA / SVD | $O(p^3)$ to $O(n^4)$ — low to moderate | Closed-form or fixed-point iterations |
| Evolutionary (PSO/GA/DE) | Moderate–high, problem-dependent | Iterative global search; convergence varies |
| DL (DNN/RNN/CNN/VAE/GAN/Transformer/Deep clustering) | High — depends on architecture and data size | Trades compute for accuracy |

The survey stresses that DL models consistently outperform other classes when large labeled datasets are available, but at the cost of substantially higher computational complexity.

## Key Contributions

1. **Three-way taxonomy of AI-based BSS** — introduces a unified classification (Classical ML / DL / Evolutionary) covering ~60 surveyed papers; this taxonomy is the survey's distinctive synthesis contribution.
2. **Cross-method benchmarking** — Tables 1, 5, 6 consolidate heterogeneous metrics (SAR/SDR/SIR/SNR/PESQ/AVCC/MSE/accuracy) across classical-ML, DL, and evolutionary methods in a single comparative view, despite acknowledging that direct cross-study comparison is methodologically difficult.
3. **Complexity comparison** — Tables 7 & 8 explicitly contrast Big-O complexity across classical statistical methods (ICA, FastICA, NMF, SCA, JADE, SOBI, JD, CCA, SVD, sparse coding) and AI-based methods (PSO, GA, DE, DNN, RNN, CNN, VAE, GAN, Transformer, deep clustering), making the compute/accuracy trade-off explicit.
4. **Research-gap analysis** — identifies specific open challenges in: speed/accuracy trade-off; multipurpose BSS models; robustness and scalability; underdetermined convolutive cases; non-harmonic-instrument separation; nonlinear mixing; hybrid ML models; standardized perceptual evaluation metrics; and edge/mobile/on-device deployment (privacy, bandwidth efficiency, IoT applications).
5. **Edge/mobile deployment roadmap** — articulates a forward-looking research direction for BSS on resource-constrained devices, calling for hardware-efficient architectures and algorithm optimizations for real-time processing.

## Limitations and Caveats

- **Heterogeneous metrics across studies**: the survey repeatedly notes that different papers use different benchmark criteria, datasets, and signal types, making fair cross-study comparison difficult; the consolidated tables should be read as a coarse map rather than a strict ranking.
- **Many surveyed works do not report numerical results**: several entries in Tables 1, 5, 6 are blank ("—"), limiting quantitative comparison.
- **Time/computational complexity is not always reported**: the survey calls for explicit Big-O analysis and runtime measurement, which most surveyed papers lack.
- **Coverage cutoff**: the survey's literature search appears to favor the 2014–2017 and 2021 vintages; very recent (2022–2023) transformer-based and self-supervised BSS models are mentioned but not deeply analyzed.
- **Numbering inconsistency in the paper**: Table 5 references "Section 4.2.2" and Table 6 references "Section 4.2.3" while the body text labels the corresponding subsections as 4.1.2 and 4.1.3 — a typographical inconsistency that does not affect the substantive content.
- **Stricter-concept-threshold note for wiki ingest**: the survey surveys many named methods (Conv-TasNet, SepFormer, Demucs, deep clustering, VAE, GAN, BNN, etc.) but does not contribute a distinctive synthesis of each — only its three-way AI-based-BSS taxonomy warrants updating the existing [[concepts/blind-source-separation|Blind Source Separation]] concept page. Named methods are linked to existing wiki pages where available and left as plain text otherwise.

## Related Concepts

- [[concepts/blind-source-separation|Blind Source Separation]] — the survey's main subject; the three-way AI-based-BSS taxonomy extends the existing concept page.
- [[concepts/cocktail-party-problem|Cocktail-Party Problem]] — one of the named motivations for BSS in the survey's introduction.
- [[concepts/tf-mask-estimation|TF Mask Estimation]] — DNN-based mask prediction is covered as a deep-learning BSS sub-area (Refs. [124, 126, 133, 160, 167]).
- [[concepts/deep-clustering-speech-separation|Deep Clustering for Speech Separation]] — listed among the DL-based BSS methods surveyed (Refs. [97, 137, 160]).
- [[concepts/independent-vector-analysis|Independent Vector Analysis]] — mentioned as an emerging BSS direction extending beyond linear mixtures to nonlinear dependencies among sources.
- [[concepts/cocktail-party-problem|Cocktail-Party Problem]] — among the canonical BSS applications listed in the survey's introduction.
- [[concepts/sparsity-based-source-tracking|Sparsity-Based Source Tracking]] — sparse approximation is the survey's foundational technique for underdetermined BSS.

## Related Sources

- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova et al. 2023: Neural Target Speech Extraction: An Overview]] — companion neural-BSS survey focusing on target speech extraction with auxiliary clues.
- [[sources/sawada-2019-bss-ilrma-review|Sawada et al. 2019: BSS/ILRMA Review]] — tutorial of the ICA → IVA → ILRMA lineage; complements this survey's statistical-BSS foundation.
- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]] — narrower IVA-focused survey; complements the AI-based-BSS perspective here.
- [[sources/wang-2018-supervised-speech-separation-deep-learning-overview|Wang & Chen 2018: Supervised Speech Separation Based on Deep Learning: An Overview]] — earlier DL-for-speech-separation overview covering deep clustering and mask-prediction networks that this survey references.
- [[sources/richard-2023-audio-signal-processing-21st-century|Richard et al. 2023: Audio Signal Processing in the 21st Century]] — 25-year retrospective that traces the determined and monophonic BSS lineages this survey builds on.
