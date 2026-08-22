---
type: concept
created: 2026-08-22
updated: 2026-08-22
sources:
  - raw/papers/tesch-2024-spatially-selective-nonlinear-filters/full-text.md
tags:
  - direction-of-arrival
  - multi-channel
  - deep-learning
  - speech-separation
  - spatial-filtering
---

# DNN-based DoA Classifier

The **DNN-based DoA classifier** proposed by Tesch & Gerkmann (2024) is a compact neural network that, given a multi-channel mixture signal, predicts per angular bin (2° resolution, 180 bins for 360°) whether a speaker is present at that direction. It enables the blind deployment of a [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Filter (SSF)]] without the computational burden of the [[concepts/search-based-doa-estimation|search-based]] strategy.

## Architecture

- **Input**: multi-channel STFT (same form as the SSF input).
- **Front end**: one F-LSTM layer (the same F-LSTM used in the [[concepts/joint-nonlinear-filtering|JNF]] and [[concepts/mcnet|McNet]] backbones).
- **Head**: two feed-forward layers, with 256 and 180 hidden units respectively.
- **Activations**: exponential linear unit (ELU) for the first feed-forward layer, sigmoid for the second.
- **Output**: a 180-dimensional vector of per-bin speaker-presence probabilities.

## Training

- **Loss**: average binary cross-entropy over the 180 bins, computed per-utterance.
- **Training data**: 2-speaker mixture dataset (the same simulation pipeline used to train the SSF).
- **Epochs**: 100.
- **Generalization**: despite being trained only on 2-speaker mixtures, the classifier performs sufficiently well at 3- and 5-speaker mixtures — the binary per-bin detection task appears to generalize across speaker counts.

## Peak-Finding Heuristic

Because the classifier outputs continuous probabilities in [0, 1] per bin rather than a discrete set of speaker locations, the same peak-finding heuristic used for the [[concepts/search-based-doa-estimation|search-based]] strategy is applied to the classifier output to obtain a discrete set of speaker DoAs (Appendix B of the source): normalise the curve, run `scipy.signal.find_peaks` with prominence 0.009, height 0.05, width 1, and progressively relax parameters if too few peaks are found; merge peaks that are close together and have similar height; if too many peaks are found, keep the highest ones.

## Empirical Findings (Tesch & Gerkmann 2024, Table IV)

Mean angular error vs. number of speakers:

| Method | 2 spk | 3 spk | 5 spk |
|:-------|:------|:------|:------|
| search (JNF-SSF) | 1.57 ± 0.12° | 2.06 ± 0.19° | 3.54 ± 0.25° |
| search (McNet-SSF) | 2.07 ± 0.07° | 2.53 ± 0.15° | 3.99 ± 0.23° |
| **DNN classifier** | **1.06 ± 0.03°** | **1.24 ± 0.09°** | **2.13 ± 0.19°** |

- The DNN classifier is **both more efficient** (a single forward pass vs. 180 SSF evaluations per mixture) **and more accurate** (up to 1.86° lower mean angular error for 5 speakers).
- When McNet-SSF is steered with DNN-classifier DoAs (row 8 of Table II), separation performance matches the oracle-DoA case (1.42 vs. 1.43 ΔPOLQA for 5 speakers), demonstrating that the SSF approach is well applicable to fully blind separation tasks.

## Related Concepts

- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]
- [[concepts/search-based-doa-estimation|Search-based DoA Estimation]]
- [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering (JNF)]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]

## Related Sources

- [[sources/tesch-2024-spatially-selective-nonlinear-filters|Tesch & Gerkmann 2024: Multi-channel Speech Separation Using Spatially Selective Deep Non-linear Filters]]
