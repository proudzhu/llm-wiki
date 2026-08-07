---
type: concept
created: 2026-08-07
updated: 2026-08-07
sources:
  - raw/papers/mounir-2025-robust-early-howling-detection-sparsity/full-text.md
tags:
  - acoustic-howling
  - howling-detection
  - spectral-sparsity
  - signal-processing
---

# NINOS²-T (Normalized Identification of Note Onset based on Spectral Sparsity — Transposed)

**NINOS²-T** is a [[concepts/howling-detection|howling detection]] feature based on a transposed spectral sparsity measure, introduced by Mounir et al. (2025). It is derived from the NINOS² feature previously developed for musical note onset detection, but operates along the time axis of a single frequency bin (a row of the STFT matrix) rather than along the frequency axis of a single time frame (a column). It is the first HD feature designed to detect **early howling and ringing** without relying on candidate howling frequency preselection.

## Motivation: The Onset–Howling Analogy

The key insight is an analogy between two spectrogram-line detection problems:

| Problem | Spectrogram pattern | Axis of sparsity |
|---------|---------------------|-------------------|
| Note onset detection | Vertical line (broadband, short burst) | Frequency — a single time frame is *less sparse* across frequencies during an onset |
| Howling detection | Horizontal line (narrowband, persisting) | Time — a single frequency bin is *more sparse* across time during howling |

Both amount to detecting lines in a spectrogram. NINOS² exploits spectral sparsity across frequency for onsets; NINOS²-T transposes this to exploit temporal sparsity within a frequency bin for howling.

## Derivation

### Inverse Sparsity Measure

For an arbitrary vector $\mathbf{x}$, an inverse sparsity measure based on the ratio of two norms ($p < q$):

$$\mathcal{S} = \frac{\|\mathbf{x}\|_p}{\|\mathbf{x}\|_q} = \frac{\left(\sum |x_m|^p\right)^{1/p}}{\left(\sum |x_m|^q\right)^{1/q}}$$

The most sparse vector (all energy in one coefficient) gives $\mathcal{S}=1$; the least sparse vector (all coefficients equal) gives $\mathcal{S} = \sqrt[4]{\mathcal{Q}_M}$ for $p=2, q=4$.

### Application to Howling

Define the time-vector of STFT coefficients in frequency bin $\omega_i$ over the past $\mathcal{Q}_M$ frames:

$$\mathbf{Y}_T(\omega_i, t) = \left[Y(\omega_i, t-\mathcal{Q}_M+1) \dots Y(\omega_i, t)\right]^T$$

A howling component persists over time, so this vector is *sparse* (energy concentrated in few large coefficients) — howling does not vary much frame-to-frame. Applying the $p=2, q=4$ inverse sparsity measure and normalizing to $[0,1]$:

$$\mathcal{N}(\omega_i, t) = \frac{1}{\sqrt[4]{\mathcal{Q}_M} - 1}\left(\frac{\|\mathbf{Y}_T(\omega_i, t)\|_2}{\|\mathbf{Y}_T(\omega_i, t)\|_4} - 1\right)$$

- **0** = most sparse (persistent howling)
- **1** = least sparse (time-varying speech/music)

The howling detection function (HDF) $\mathcal{N}(\omega_i, t)$ is compared to a threshold $\theta \in [0,1]$.

### Why the Energy Measure Is Removed

The NINOS² variant retains a joint energy measure ($\|\mathbf{x}\|_2 \cdot \mathcal{S}$), expressing that howling is both high-energy and persistent. NINOS²-T **explicitly removes the energy measure** because high energy is only discriminative for howling that has already built up and is clearly audible — contradicting the goal of detecting early howling. Retaining only the inverse sparsity measure captures temporal persistence without requiring loudness.

## Properties

- **Normalized to $[0,1]$** — facilitates signal-independent threshold choice, unlike PTPR/PAPR/PNPR/PHPR/IMSD which require signal-dependent normalization.
- **No candidate selection required** — computed over all STFT bins, enabling early-howling and ringing detection.
- **$S_c=1$ optimal** — in all evaluation scenarios, the single largest NINOS²-T value per frame reliably points to the most probable howling occurrence, a unique property among HD features.
- **Complexity** $O(M\mathcal{Q}_M)$ — more efficient than IMSD ($O(M\mathcal{Q}_M^2)$).
- **Robust to threshold variation** — PR-curve marked points are clustered closer together than for IPMP, indicating stability.

## Performance (Mounir et al. 2025)

NINOS²-T consistently achieves the best average and worst-case PR-AUC across speech and music datasets, for both full and early HD evaluation. It is the only feature crossing 50% PR-AUC in full HD for both datasets, and the only one crossing 50% for early speech HD. Key numbers (best parametrization):

| Dataset | $F_1$ (Full) | PR-AUC (Full) | $F_1$ (Early) | PR-AUC (Early) |
|---------|:---:|:---:|:---:|:---:|
| Speech | 0.88 | 0.82 | 0.74 | 0.63 |
| Music | 0.70 | 0.53 | 0.42 | 0.21 |

## Related Concepts

- [[concepts/howling-detection|Howling Detection]] — the problem NINOS²-T solves
- [[concepts/howling-detection-features|Howling Detection Features]] — the six baseline features NINOS²-T is compared against
- [[concepts/notch-filter-based-howling-suppression|Notch-Filter-Based Howling Suppression (NHS)]] — the solution scheme in which NINOS²-T serves as the HD component
- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — broader AHS context
- [[concepts/spectrogram-analysis|Spectrogram Analysis]] — the onset–howling line-detection analogy

## Related Sources

- [[sources/mounir-2025-robust-early-howling-detection-sparsity|Mounir, Bernardi & van Waterschoot 2025]] — introduces NINOS²-T, dataset, and PR-based evaluation
- Mounir, Karsmakers & Waterschoot 2016, "Guitar note onset detection based on a spectral sparsity measure" (EUSIPCO) — the NINOS² feature for note onset detection, from which NINOS²-T is transposed
