---
type: concept
created: 2026-09-03
updated: 2026-09-03
sources:
  - raw/papers/ke-2021-low-complexity-artificial-noise-suppression/full-text.md
tags:
  - speech-enhancement
  - deep-learning
  - noise-suppression
  - psychoacoustics
  - postfilter
---

# Artificial Residual Noise

**Artificial residual noise** is the residual noise left in the output of DNN-based speech enhancement whose character differs fundamentally from the background noise it replaced. Because the enhancement mapping $\mathcal{G}(\cdot)$ is nonlinear (Eq. 2 of [[sources/ke-2021-low-complexity-artificial-noise-suppression|Ke et al. 2021]]), the speech and noise components do not pass through separately: stationary input noise emerges as a **highly non-stationary** spectro-temporal structure — spectra blurred along time and frequency, energy concentrated in mid–high frequency bands where speech PSD is low, and strong energy retained during speech pauses. The name *artificial noise* marks that this noise is a product of the DNN itself, not a leftover of the original disturbance; it plays the role that musical noise played for classical spectral subtraction.

## Psychoacoustic Characterization

[[sources/ke-2021-low-complexity-artificial-noise-suppression|Ke et al. 2021]] quantified its audibility with a Virag-style psychoacoustic model applied to four identically-trained MSE front-ends (CRN, DCN, GRN, DARCN):

- Residual-noise PSD exceeds the **noise masking threshold** of the clean speech by **>10 dB** on average in low-speech-PSD bands (2–3 kHz, 4–5 kHz) during speech presence, and by **~50 dB** during speech absence (measured at 4500 Hz, averaged over time).
- Log-spectral distortion vs. clean speech: CRN 2.50, DCN 2.71, GRN 4.84, DARCN 2.86.

Because the noise is audible precisely where speech energy is low or absent, listeners perceive it as an annoying artifact even when overall attenuation looks strong — the reason subjective AB preference separates postfiltering methods far more sharply than PESQ/segSNR (see [[concepts/pesq|PESQ]]): Ke et al.'s postfilters reached >60% preference with only ~0.1–0.15 PESQ improvement.

## Root Cause and Suppression

Phase-less **MSE magnitude-mapping training** is the identified root cause: the network is driven to zero-out noise wherever the target mask is small, but blurs spectra instead of cleanly separating speech from noise, leaving the artificial structure behind. Three families of fixes appear in the wiki:

- **Classical statistical postfilter** ([[sources/ke-2021-low-complexity-artificial-noise-suppression|Ke et al. 2021]]): an MMSE noise-PSD estimator plus decision-directed Wiener gain on the DNN output, with three re-designed [[concepts/speech-presence-probability|SPP]] inputs so noise tracking does not freeze on the non-stationary residual — 0.0098–0.016 MFLOPs/frame, ~3 orders of magnitude below the front-ends.
- **Learned postfilter** ([[sources/seidel-2024-bark-scale-nn-residual-suppression|Seidel, Mowlaee & Fingscheidt 2024]]): a neural network on Bark-scale features suppressing residual echo and noise jointly.
- **Training-time noise control** ([[sources/li-2020-residual-noise-control|Li et al. 2020]]): rather than removing the residual after inference, shape it inside the loss (generalized loss / [[concepts/noise-attenuation-control|noise attenuation control]]), keeping it below the audibility threshold while retaining natural background character.

## Related Concepts

- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/speech-presence-probability|Speech Presence Probability]]
- [[concepts/noise-attenuation-control|Noise Attenuation Control]]
- [[concepts/psychoacoustic-postfilter|Psychoacoustic Postfilter]]
- [[concepts/pesq|PESQ]]

## Related Sources

- [[sources/ke-2021-low-complexity-artificial-noise-suppression|Ke, Li, Zheng, Peng & Li 2021: Low-Complexity Artificial Noise Suppression for Deep Learning-Based Speech Enhancement]] — defining source: psychoacoustic quantification + SPP-based postfilter
- [[sources/seidel-2024-bark-scale-nn-residual-suppression|Seidel, Mowlaee & Fingscheidt 2024: Bark-Scale NN for Residual Echo and Noise Suppression]] — the learned-postfilter alternative
- [[sources/li-2020-residual-noise-control|Li, Peng, Zheng & Li 2020: Supervised Speech Enhancement with Residual Noise Control]] — the training-time control alternative (same group)
