---
type: source
created: 2026-08-07
updated: 2026-08-07
sources:
  - raw/papers/mounir-2025-robust-early-howling-detection-sparsity/full-text.md
  - https://doi.org/10.1186/s13636-025-00399-1
  - zotero://select/items/0_UNDKU7LR
tags:
  - acoustic-howling
  - howling-detection
  - spectral-sparsity
  - notch-filter
  - signal-processing
  - precision-recall
---

# Mounir, Bernardi & van Waterschoot 2025: Robust and Early Howling Detection

**Authors**: [[entities/mina-mounir|Mina Mounir]], [[entities/giuliano-bernardi|Giuliano Bernardi]], [[entities/toon-van-waterschoot|Toon van Waterschoot]]
**Institutions**: KU Leuven, Leuven, Belgium
**Published**: EURASIP Journal on Audio, Speech, and Music Processing, 2025-03-27
**Type**: Journal article (Open Access)
**DOI**: [10.1186/s13636-025-00399-1](https://doi.org/10.1186/s13636-025-00399-1)
**Zotero**: [UNDKU7LR](zotero://select/items/0_UNDKU7LR)
**Code**: https://github.com/maganino/Howling-Detection-NINOS2T
**Dataset**: https://doi.org/10.48804/EOW7OF

---

## Summary

This paper proposes **NINOS²-T** (Normalized Identification of Note Onset based on Spectral Sparsity — Transposed), a novel [[concepts/howling-detection|howling detection]] feature derived from a spectral sparsity measure originally developed for musical note onset detection. Unlike state-of-the-art HD features that rely on a preselection of candidate howling frequencies via magnitude-spectrum peak-picking, NINOS²-T is computed over all STFT frequency bins, enabling detection of **early howling and ringing** that exhibit too little energy to be peak-picked. The paper additionally introduces a larger and more diverse automatically annotated HD dataset and a precision-recall (PR) based evaluation procedure that handles the high class imbalance inherent in the HD problem and supports early-howling evaluation. NINOS²-T consistently yields the best average and worst-case PR-AUC across speech and music datasets and is the only feature for which the single largest feature value per frame reliably points to howling.

---

## Problem Formulation

### Acoustic Feedback and Howling

A single-channel sound reinforcement system forms a closed loop with forward path $G(q)$ and feedback path $F(q)$. The closed-loop frequency response is:

$$\frac{U(\omega, t)}{V(\omega, t)} = \frac{G(\omega, t)}{1 - G(\omega, t) F(\omega, t)} \tag{1}$$

Howling occurs when the **Nyquist stability criterion** is satisfied at some frequency:

$$|G(\omega, t) F(\omega, t)| \geq 1, \quad \angle G(\omega, t) F(\omega, t) = n 2\pi, \quad n \in \mathbb{Z} \tag{2-3}$$

The [[concepts/maximum-stable-gain|Maximum Stable Gain (MSG)]] bounds the broadband gain before instability:

$$\mathrm{MSG}(t) [\mathrm{dB}] = -20 \log_{10}\left(\max_{\omega \in \mathcal{W}} |F(\omega, t)|\right) \tag{4}$$

where $\mathcal{W}$ is the set of frequencies satisfying the loop phase condition. A frequency satisfying the phase condition but not the gain condition may still produce **ringing** — a non-persisting but equally detrimental artifact.

![[raw/papers/mounir-2025-robust-early-howling-detection-sparsity/figures/6dbc43d441f7787acf37dc7f1ba1a816f263809d1c80e16f14d5b6e70b7f0803.jpg|Closed-loop system model]]
*Figure 1: Closed-loop system model — the microphone signal y(t) is processed and amplified in the forward path G, resulting in the loudspeaker signal u(t) which is fed back to the microphone through the acoustic feedback path F.*

![[raw/papers/mounir-2025-robust-early-howling-detection-sparsity/figures/2a9323340dac5ff159365c81055e20affcca6c4a2e0d2f50e79ed8e4f616430c.jpg|Nyquist stability criterion example]]
*Figure 2: Nyquist stability criterion example — only the frequency around 1.6 kHz (red) satisfies both gain and phase conditions (howling); the frequency around 2.6 kHz (orange) satisfies the phase condition with gain near 3 dB (ringing).*

### The Candidate-Selection Limitation

Existing [[concepts/notch-filter-based-howling-suppression|NHS]] methods detect howling by first peak-picking the microphone signal magnitude spectrum to obtain a small set of candidate howling frequencies $\mathcal{D}_{\breve{\omega}}(t)$, then computing discriminating features only for those candidates. This implicitly **rules out early howling and ringing**, since such artifacts exhibit too little energy to be peak-picked. The paper challenges this presumption by computing HD features directly on the full STFT (i.e., treating all frequency bins as candidates).

![[raw/papers/mounir-2025-robust-early-howling-detection-sparsity/figures/6e64bb94a9075cdd2b9438a15848630ae31431d4f491b9098a310a865d96b5ff.jpg|NHS solution scheme]]
*Figure 3: NHS solution scheme — a howling detection (HD) block analyses y(t) and produces notch filter design parameters $\mathcal{D}_H(t)$ for a bank of adjustable notch filters $H(\omega,t)$.*

![[raw/papers/mounir-2025-robust-early-howling-detection-sparsity/figures/fce88e18fb8d1904ffa3bd5e68ba7f5afa8dbfe06fdc8c9cf1430eea92f1ec30.jpg|State-of-the-art HD solution scheme]]
*Figure 4: State-of-the-art HD solution scheme — candidate howling frequencies are first peak-picked, then discriminating features are computed only for those candidates. The proposed approach omits the candidate selection (lower arrow only), enabling early-howling and ringing detection.*

---

## Methodology

### From Note Onsets to Howling: The Sparsity Analogy

The key insight is an analogy between **musical note onsets** (vertical lines in a spectrogram — broadband, short energy bursts) and **howling** (horizontal lines — narrowband, persisting components). Both problems amount to detecting lines in a spectrogram. The previously proposed NINOS² feature for note onset detection exploits *spectral sparsity* across the M frequency bins of a single time frame. The proposed NINOS²-T feature transposes this idea to operate across $\mathcal{Q}_M$ time frames of a single frequency bin (a row rather than a column of the STFT matrix).

### NINOS²-T Derivation

An inverse sparsity measure based on the ratio of two vector norms, for an arbitrary length-$M$ vector $\mathbf{x}$:

$$\mathcal{S} = \frac{\|\mathbf{x}\|_p}{\|\mathbf{x}\|_q} = \frac{\left(\sum_{m=0}^{M-1} |x_m|^p\right)^{1/p}}{\left(\sum_{m=0}^{M-1} |x_m|^q\right)^{1/q}}, \quad p < q \tag{15}$$

For HD, this is applied to the time-vector of STFT coefficients in a single frequency bin over $\mathcal{Q}_M$ past frames:

$$\mathbf{Y}_T(\omega_i, t) = \left[Y(\omega_i, t-\mathcal{Q}_M+1) \dots Y(\omega_i, t)\right]^T \tag{17}$$

Using $p=2, q=4$ and normalizing to $[0,1]$ (where 0 = most sparse, 1 = least sparse), the proposed **NINOS²-T** feature is:

$$\mathcal{N}(\omega_i, t) = \frac{1}{\sqrt[4]{\mathcal{Q}_M} - 1}\left(\frac{\|\mathbf{Y}_T(\omega_i, t)\|_2}{\|\mathbf{Y}_T(\omega_i, t)\|_4} - 1\right) \tag{20-21}$$

Crucially, the **energy measure is removed** (unlike the NINOS² variant that retains it): the high-energy property is only discriminative for howling that has already built up significant energy and is clearly audible, which conflicts with the goal of detecting early howling. Retaining only the inverse sparsity measure expresses the fact that howling persists over time, without requiring it to be loud.

The howling detection function (HDF) $\mathcal{N}(\omega_i, t)$ is a function of time and frequency that can be compared to a detection threshold $\theta \in [0,1]$. Because the feature is normalized, the threshold choice is facilitated and largely signal-independent.

### Computational Complexity

| Feature | Complexity | Notes |
|---------|-----------|-------|
| PTPR, PAPR, PNPR, PHPR (spectral) | $O(M)$ | Linear in frame size |
| IPMP (temporal) | $O(M \mathcal{Q}_M)$ | Plus peak tracking |
| IMSD (temporal) | $O(M \mathcal{Q}_M^2)$ | Long- + short-term slope averages |
| **NINOS²-T** (temporal) | $O(M \mathcal{Q}_M)$ | $\ell_2$ + $\ell_4$ norms per bin |

NINOS²-T is more efficient than IMSD ($O(M\mathcal{Q}_M)$ vs. $O(M\mathcal{Q}_M^2)$) while matching the linear-in-$M$ scaling of the spectral features.

### Performance Evaluation Procedure

Three novelties over prior HD evaluation:

1. **All frequency bins as candidates** — removes the candidate-selection step that artificially excluded low-energy howling from evaluation.
2. **Precision-Recall (PR) curves and PR-AUC** instead of ROC curves — the HD problem is highly class-imbalanced (howling occurs in $\sim 10^{-3}$ of time-frequency bins), and ROC curves fail to differentiate features under such imbalance. The PR baseline (random guessing) is near zero.
3. **Early HD evaluation** — performance is computed only up to 5 s after the theoretical howling start (i.e., up to 13.5 s of a 20-s excerpt), assessing early-howling and ringing detection capability.

Annotations are generated **automatically** using the known feedback path $F$ and forward path $G$: a time-frequency bin is labelled as howling if it is one of the two bins straddling the Nyquist-predicted howling frequency $\tilde{\omega}_h$, from time $T_s + T_r/2$ onwards.

---

## Experimental Setup

| Parameter | Value |
|:----------|:------|
| Source signals | 30 speech (8 files, 4 languages: Chinese, English, Dutch, Russian) + 28 music (7 pieces, jazz/opera/etc.) excerpts, 20 s each |
| Sampling rate | 16 kHz |
| SNR (added noise) | 40 dB Gaussian white noise |
| Feedback paths | 8 acoustic impulse responses from Openair database, truncated/padded to 1 s |
| MSG normalization | Forward path gain of 10 dB → MSG condition |
| Gain profile | $K_i = \mathrm{MSG}-6$ dB for 0–8 s; linear ramp to $K_f = \mathrm{MSG}$ over 8–9 s; held at $K_f$ for 9–20 s |
| STFT frame sizes | $M \in \{512, 1024, 2048, 4096\}$ |
| Hop size | 50 frames/s (20 ms) |
| Temporal window | $\mathcal{Q}_M \in \{4, 8, 16, 32, 64, 96\}$ |
| Thresholding | $S_c \in \{1, 3, M\}$ largest feature values per frame |
| Cross-validation | 5-fold, separate for speech and music |
| Threshold grid | $\theta \in [0,1]$, resolution 0.05, plus $\pm\infty$ |
| Baselines | PTPR, PAPR, PNPR, PHPR, IPMP, IMSD, NINOS² (with energy) |
| Metrics | Best $F_1$-score, PR-AUC, ROC-AUC (full and early evaluation) |

---

## Results

### Cross-Validation PR-AUC (5-fold)

![[raw/papers/mounir-2025-robust-early-howling-detection-sparsity/figures/db0e1abd066b576ce7e1b960c6e0661b2447d7e4b15d17123cdeafaeaf43f3da.jpg|Speech cross-validation PR-AUC box plots]]

![[raw/papers/mounir-2025-robust-early-howling-detection-sparsity/figures/124fa04569f326b6da4d31f3594e93edb83acd40fc31da10752524d2af2186d9.jpg|Music cross-validation PR-AUC box plots]]
*Figure 6: Cross-validation PR-AUC results for full and early HD evaluation on speech (top) and music (bottom) datasets. NINOS²-T consistently yields the highest average PR-AUC across all datasets and scenarios; IMSD consistently performs worst.*

### Speech Dataset (Best Parametrization per Feature)

| Feature | $F_1$ (Full) | PR-AUC (Full) | ROC-AUC (Full) | $F_1$ (Early) | PR-AUC (Early) | ROC-AUC (Early) |
|:--------|:---:|:---:|:---:|:---:|:---:|:---:|
| **NINOS²-T** | **0.88** | **0.82** | 0.93 | **0.74** | **0.63** | 0.86 |
| NINOS² | 0.77 | 0.65 | 0.90 | 0.58 | 0.40 | 0.82 |
| IPMP | 0.68 | 0.69 | 0.95 | 0.50 | 0.47 | 0.91 |
| PAPR | 0.63 | 0.56 | 0.99 | 0.45 | 0.31 | 0.98 |
| PTPR | 0.60 | 0.49 | 0.83 | 0.41 | 0.25 | 0.76 |
| PHPR | 0.59 | 0.47 | 0.76 | 0.46 | 0.31 | 0.68 |
| PNPR | 0.55 | 0.44 | 0.94 | 0.41 | 0.27 | 0.88 |
| IMSD | 0.13 | 0.03 | 0.66 | 0.07 | 0.01 | 0.60 |

### Music Dataset (Best Parametrization per Feature)

| Feature | $F_1$ (Full) | PR-AUC (Full) | ROC-AUC (Full) | $F_1$ (Early) | PR-AUC (Early) | ROC-AUC (Early) |
|:--------|:---:|:---:|:---:|:---:|:---:|:---:|
| **NINOS²-T** | **0.70** | **0.53** | 0.83 | **0.42** | **0.21** | 0.69 |
| IPMP | 0.47 | 0.36 | 0.71 | 0.23 | 0.15 | 0.61 |
| NINOS² | 0.36 | 0.19 | 0.95 | 0.27 | 0.13 | 0.94 |
| PTPR | 0.33 | 0.17 | 0.96 | 0.19 | 0.08 | 0.95 |
| PAPR | 0.33 | 0.16 | 0.96 | 0.17 | 0.05 | 0.94 |
| PHPR | 0.18 | 0.07 | 0.95 | 0.09 | 0.03 | 0.93 |
| PNPR | 0.16 | 0.05 | 0.87 | 0.08 | 0.02 | 0.80 |
| IMSD | 0.05 | 0.01 | 0.56 | 0.03 | 0.00 | 0.54 |

### ROC vs PR Curves

![[raw/papers/mounir-2025-robust-early-howling-detection-sparsity/figures/5a019741b68bc7ec0ffb2b20c58d0b1108f7fc93f805f9c497dd55fabe1cd8ff.jpg|ROC and PR curves for speech dataset]]
*Figure 7: ROC and PR curves for full and early HD evaluation with the speech dataset. The ROC curves fail to differentiate the features due to class imbalance, while the PR curves clearly separate NINOS²-T from the baselines.*

![[raw/papers/mounir-2025-robust-early-howling-detection-sparsity/figures/6de6f756d101356663ab7dbe92db4b8d39bc23180887b2fa494cc0cdb090c45e.jpg|ROC and PR curves for music dataset]]
*Figure 8: ROC and PR curves for the music dataset. NINOS²-T and NINOS² yield PR curves closer to the top-right corner than IPMP, indicating a better precision–recall compromise.*

### Howling Detection Function Spectrograms

![[raw/papers/mounir-2025-robust-early-howling-detection-sparsity/figures/da51ae7d5aa86d34dba5885921d5b4e809f372c5e3ddd6ebea6e79132e4c72ca.jpg|HDF spectrogram comparison]]
*Figure 10: Comparison of HDFs for (left) a speech example exhibiting a ringing artifact around 800 Hz and (right) a music excerpt exhibiting a low-power howling around 260 Hz. Only NINOS²-T captures the howling close to its starting point. Spectral features have a "vertical" granular structure; temporal features have a "horizontal" smoother structure.*

### Key Findings

- **NINOS²-T is the only feature crossing 50% PR-AUC** in full HD evaluation for both speech and music; for early HD, it only crosses 50% for speech (all features perform poorly on early music HD).
- **NINOS²-T is the only feature for which $S_c=1$ is optimal** in all scenarios — its single largest feature value per frame reliably points to the most probable howling occurrence.
- **HD is harder for music than speech**, particularly for early howling, due to music's tonal components resembling howling.
- **IMSD consistently performs worst**, presumably due to high sensitivity to the detection threshold.
- **PR-AUC correlates strongly with $F_1$-score**, confirming PR is more suitable than ROC for the imbalanced HD problem.
- **ROC curves fail to differentiate features** under the high class imbalance — only points on the vertical TPR axis are practically usable.

---

## Key Contributions

1. **NINOS²-T feature** — a novel HD feature based on a transposed spectral sparsity measure, computed over all STFT bins without candidate preselection, enabling early-howling and ringing detection. Normalized to $[0,1]$ for signal-independent thresholding and more robust to threshold variations than baselines.
2. **Larger and more diverse HD dataset** — 58 automatically annotated speech/music excerpts with simulated howling across 8 acoustic impulse responses and 4 languages, with a documented pruning procedure (majority vote across three authors). Publicly available.
3. **PR-based evaluation procedure** — replaces the candidate-based, ROC-based evaluation with a procedure using all time-frequency bins as candidates and PR curves / PR-AUC / $F_1$-score, suitable for the highly class-imbalanced HD problem and supporting early-howling and ringing detection evaluation.

---

## Related Concepts

- [[concepts/howling-detection|Howling Detection]] — the core problem addressed; this paper provides the NINOS²-T feature and the PR-based evaluation framework
- [[concepts/notch-filter-based-howling-suppression|Notch-Filter-Based Howling Suppression (NHS)]] — the solution scheme in which NINOS²-T serves as the HD component
- [[concepts/howling-detection-features|Howling Detection Features]] — the six baseline features (PTPR, PAPR, PNPR, PHPR, IPMP, IMSD) surveyed and compared
- [[concepts/ninosp2-transposed|NINOS²-T]] — the proposed feature, derived from the NINOS² note-onset feature
- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — broader AHS context
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the closed-loop instability that produces howling
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — used in dataset generation and gain profiling
- [[concepts/spectrogram-analysis|Spectrogram Analysis]] — howling manifests as horizontal lines; note onsets as vertical lines

## Related Synthesis

- None — this paper is a classical signal-processing contribution to howling detection and does not intersect the existing synthesis pages (which focus on ANC/SE neural-network efficiency frontiers and Kalman-filter theory). It may warrant a future synthesis page on HD feature evolution if additional HD papers are ingested.
