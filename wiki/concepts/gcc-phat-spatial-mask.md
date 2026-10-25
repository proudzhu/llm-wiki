---
type: concept
created: 2026-10-25
updated: 2026-10-25
sources:
  - raw/papers/li-2026-geometry-conditioned-tse/full-text.md
tags:
  - gcc-phat
  - spatial-features
  - geometry-conditioning
  - microphone-arrays
  - deep-learning
---

# GCC-PHAT Spatial Mask

The **GCC-PHAT spatial mask** is a signal-dependent geometry-conditioning feature introduced by Li & Doclo (2026) for the [[concepts/geometry-conditioned-ssf|GC-SSF]]: it quantifies the **presence of the target speaker per time-frequency (TF) bin** by averaging the phase correlation (instantaneous [[concepts/gcc-phat|GCC-PHAT]]) between all pairs of TDOA-compensated microphone channels. Where the [[concepts/target-steering-vector|target steering vector]] feature is purely geometric, the spatial mask adds observed-signal evidence of target activity — conceptually related to classical spectral post-filtering.

## Formulation

First, the microphone signals are spatially aligned toward the target DOA by applying the complex conjugate of the target steering vector:

$$\mathbf{S}(k,l) = \mathbf{d}^{*}(k) \odot \mathbf{Y}(k,l),$$

where $\odot$ denotes element-wise multiplication. For any pair of TDOA-compensated channels $i, j$, the instantaneous GCC-PHAT is

$$\Psi_{ij}(k,l) = \frac{S_{i}(k,l)\, S_{j}^{*}(k,l)}{|S_{i}(k,l)|\, |S_{j}(k,l)|},$$

and the spatial mask averages the real part over all $\tfrac{M(M-1)}{2}$ unique microphone pairs:

$$I(k,l) = \frac{2}{M(M-1)}\, \text{Re}\!\left(\sum_{i=1}^{M}\sum_{j=i+1}^{M} \Psi_{ij}(k,l)\right).$$

The feature $\mathbf{P}_{\text{Mask}}$ aggregates $I(k,l)$ across the $K$ frequency bins per time step (input shape $[BL, 1, K]$, frames processed independently for online operation).

## Interpretation

- When the target speaker dominates a TF bin, the aligned channels are in phase and $I(k,l) \to 1$
- When a TF bin is dominated by interfering speakers from a different DOA, reverberation, or noise, the phase alignment degrades and $I(k,l)$ decreases
- $I(k,l)$ thus acts as a per-bin target-presence indicator, analogous to a spatial post-filter

## Properties and Limitations

- **Signal-dependent**: unlike the purely geometric [[concepts/target-steering-vector|TSV]], captures target activity per TF bin
- **Single-channel aggregation**: collapses the array into one real value per bin — does *not* preserve inter-microphone phase information across the array
- **Direct-path assumption**: the TDOA compensation assumes direct-path propagation; reverberation degrades the phase alignment, producing an inaccurate mask that suppresses valid target TF bins
- **DOA-error sensitivity**: explicitly derived from the input target DOA, so errors >20° misalign the compensation and can push performance below the abstract-encoding baseline

## Empirical Results (Li & Doclo 2026)

Used as the conditioning feature of the GCSSF (same encoder/FiLM integration as the other features), trained on random 5-microphone arrays:

| System (random arrays) | SI-SDR | PESQ | ESTOI | DNSMOS |
|:-----------------------|:-------|:-----|:------|:-------|
| GCSSF-MPE (baseline) | 7.77 | 1.96 | 0.69 | 1.95 |
| GCSSF-Mask | 8.45 | 2.10 | 0.72 | 1.99 |
| **GCSSF-TSV** | **9.43** | **2.27** | **0.75** | **2.07** |

The mask beats the abstract MPE embeddings but trails the TSV — attributed to the reverberation-induced inaccuracy above and the loss of multichannel phase information.

## Related Concepts

- [[concepts/target-steering-vector|Target Steering Vector (TSV) Feature]] — the purely geometric counterpart that outperforms it
- [[concepts/geometry-conditioned-ssf|Geometry-Conditioned SSF (GC-SSF)]]
- [[concepts/gcc-phat|GCC-PHAT]] — the underlying pairwise phase-correlation function
- [[concepts/doa-microphone-positional-encoding|DOA-Microphone Positional Encoding (MPE)]] — the abstract embedding baseline
- [[concepts/film-layer|FiLM Layer]] — integration mechanism in the GCSSF

## Related Sources

- [[sources/li-2026-geometry-conditioned-tse|Li & Doclo 2026: Geometry-Conditioned Target Speaker Extraction with Spatial Features]]
