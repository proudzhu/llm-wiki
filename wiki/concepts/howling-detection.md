---
type: concept
created: 2026-08-07
updated: 2026-08-07
sources:
  - raw/papers/vanwaterschoot-2011-fifty-years-afc/full-text.md
  - raw/papers/mounir-2025-robust-early-howling-detection-sparsity/full-text.md
tags:
  - acoustic-howling
  - howling-detection
  - signal-processing
  - detection-theory
  - precision-recall
---

# Howling Detection

**Howling detection (HD)** is the problem of identifying the frequencies and time intervals at which an acoustic feedback artifact (howling or ringing) occurs in a sound reinforcement system, typically as the front-end stage of [[concepts/notch-filter-based-howling-suppression|notch-filter-based howling suppression (NHS)]].

## Problem Formulation

Cast as a **binary hypothesis testing** problem: for each time-frequency bin of the microphone signal STFT, decide between *howling* and *no howling* by comparing a signal feature to a detection threshold. The microphone signal is framed and transformed via the STFT:

$$Y(\omega_k, t) = \sum_{n=0}^{M-1} w(t_n) y(t_n) e^{-j \omega_k t_n}, \quad k = 0, \ldots, M-1$$

### Two Solution Paradigms

1. **Candidate-based HD (state-of-the-art)** — magnitude-spectrum peak-picking selects a few candidate howling frequencies $\mathcal{D}_{\breve{\omega}}(t)$; discriminating features are then computed only for those candidates. This excludes low-energy howling and ringing from detection.
2. **Full-grid HD (proposed in Mounir et al. 2025)** — features are computed over *all* STFT frequency bins, treating every bin as a candidate. This enables **early howling and ringing detection** since no minimum energy is required to enter the candidate set.

### Howling Properties Exploited for Detection

- **Narrowband and persisting** — a horizontal line in the spectrogram, high power relative to neighbours.
- **Purely sinusoidal** — no harmonics (unless loudspeaker clipping/saturation occurs).
- **High power** relative to a reference (absolute threshold, frame average, neighbours, or harmonics).

## Early Howling and Ringing Detection

**Early howling** refers to howling components that have not yet built up significant energy — too small to be peak-picked, yet already audible and detrimental. **Ringing** is a non-persisting feedback artifact that occurs when the loop phase condition is met but the loop gain is below unity (typically a few dB below the MSG). Detecting these requires abandoning the candidate-selection paradigm, since they exhibit too little energy to be peak-picked. Mounir et al. (2025) introduce an **early HD evaluation** scenario in which performance is measured only up to 5 s after the theoretical howling start.

## Evaluation

### The Class-Imbalance Problem

Howling occurs in only $\sim 10^{-3}$ of time-frequency bins. The traditional **ROC curve and ROC-AUC** perform poorly on such imbalanced datasets and fail to visually differentiate features. Mounir et al. (2025) advocate **precision-recall (PR) curves, PR-AUC, and $F_1$-score**, which are better suited to skewed datasets. The PR baseline (random guessing) is a near-zero constant line, making feature separation visible.

### Automatic Annotation

When the feedback path $F$ and forward path $G$ are known (e.g., in simulated datasets), the binary annotation can be generated automatically from the **Nyquist stability criterion**: a bin is labelled howling if it straddles the predicted howling frequency $\tilde{\omega}_h$ from the gain-rise midpoint onwards. This avoids subjective manual annotation and the implicit train/test dependencies it introduces.

## Challenges

- **Detection speed vs. precision** — reactive NHS methods require howling to be detected before it can be suppressed; both speed and audibility-before-detection matter.
- **Music vs. speech** — HD is harder for music, whose tonal components resemble howling; all features perform poorly on early music HD.
- **Threshold sensitivity** — some features (e.g., IMSD) are extremely sensitive to the detection threshold, making deployment fragile. Normalized features (IPMP, NINOS²-T) with $[0,1]$ ranges facilitate signal-independent thresholding.

## Related Concepts

- [[concepts/notch-filter-based-howling-suppression|Notch-Filter-Based Howling Suppression (NHS)]] — the solution scheme HD serves
- [[concepts/howling-detection-features|Howling Detection Features]] — the spectral and temporal features used for HD
- [[concepts/ninosp2-transposed|NINOS²-T]] — a sparsity-based HD feature enabling early-howling detection
- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — broader AHS context
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the closed-loop instability producing howling
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — bounds the gain before howling onset

## Related Sources

- [[sources/vanwaterschoot-2011-fifty-years-afc|van Waterschoot & Moonen 2011]] — surveys HD as the front-end stage of two-stage NHS and formalizes the six classical HD features
- [[sources/mounir-2025-robust-early-howling-detection-sparsity|Mounir, Bernardi & van Waterschoot 2025]] — proposes NINOS²-T, the full-grid PR-based evaluation, and an automatically annotated dataset
