---
type: concept
created: 2026-10-25
updated: 2026-10-25
sources:
  - raw/papers/li-2026-geometry-conditioned-tse/full-text.md
tags:
  - steering-vector
  - spatial-features
  - geometry-conditioning
  - microphone-arrays
  - deep-learning
---

# Target Steering Vector (TSV) Feature

The **target steering vector (TSV) feature** $\mathbf{P}_{\text{TSV}}$ is a geometry-conditioning feature introduced by Li & Doclo (2026) for the [[concepts/geometry-conditioned-ssf|GC-SSF]]: it stacks the complex conjugates of the far-field [[concepts/beamforming|steering vectors]] of the target speaker across all STFT frequency bins and feeds them to the conditioning branch, so that the network is explicitly handed the inter-microphone phase structure that a delay-and-sum beamformer would use to steer toward the target direction-of-arrival (DOA).

## Formulation

Assuming far-field propagation, the time difference of arrival between the $m$-th microphone and the array centroid for a target at DOA $\theta$ is

$$\tau_{m} = \frac{d_{m}\cos(\varphi_{m} - \theta)}{c},$$

with microphone polar coordinates $(d_m, \varphi_m)$ relative to the centroid and sound speed $c$. Relative to the reference microphone, the target steering vector at frequency $f_k$ is

$$\mathbf{d}(k) = \big[1,\; e^{\jmath 2\pi f_k (\tau_2 - \tau_1)}, \ldots, e^{\jmath 2\pi f_k (\tau_M - \tau_1)}\big]^{\text{T}} \in \mathbb{C}^{M}.$$

The feature stacks the **conjugate** $\mathbf{d}^{*}(k)$ across all $K$ frequency bins, giving $\mathbf{P}_{\text{TSV}}$ of shape $[B, M, K]$. The conjugate is used because $\mathbf{d}^{*}(k)$ is exactly the phase compensation applied by a delay-and-sum beamformer ($\mathbf{d}^{H}\mathbf{Y}$) — the feature therefore encodes "how to align the array toward the target" per frequency bin.

## Properties

- **Purely geometric and signal-independent**: computed only from microphone coordinates and the target DOA, independent of the observed multichannel signals — it captures where the target *is*, not whether it is active in a given TF bin
- **Multichannel**: preserves the full inter-microphone phase information across the array (unlike a single-channel aggregation such as the [[concepts/gcc-phat-spatial-mask|GCC-PHAT spatial mask]])
- **Propagation-based**: derived from acoustic propagation principles, in contrast to abstract learned embeddings such as [[concepts/doa-microphone-positional-encoding|MPE positional encodings]], which force the network to implicitly infer the phase-DOA-geometry relationship
- **DOA-error sensitivity**: because the feature is explicitly derived from the input DOA, large target-DOA errors (>20°) introduce severe phase mismatches and degrade performance below the abstract-encoding baseline

## Empirical Results (Li & Doclo 2026)

Used as the conditioning feature of the GCSSF (encoder: 3 Conv1d layers, 64/512/1024 output channels; integration via [[concepts/film-layer|FiLM]] after the F-LSTM), trained on random 5-microphone arrays (WSJ0, 2–6 speakers, Pyroomacoustics):

| System (random arrays) | SI-SDR | PESQ | ESTOI | DNSMOS |
|:-----------------------|:-------|:-----|:------|:-------|
| GCSSF-MPE (baseline) | 7.77 | 1.96 | 0.69 | 1.95 |
| **GCSSF-TSV** | **9.43** | **2.27** | **0.75** | **2.07** |

TSV is the best-performing conditioning feature in the study (+1.66 dB SI-SDR, +0.31 PESQ over MPE) and maintains its advantage for target-DOA errors up to 20°.

## Related Concepts

- [[concepts/geometry-conditioned-ssf|Geometry-Conditioned SSF (GC-SSF)]]
- [[concepts/gcc-phat-spatial-mask|GCC-PHAT Spatial Mask]] — the signal-dependent alternative feature
- [[concepts/doa-microphone-positional-encoding|DOA-Microphone Positional Encoding (MPE)]] — the abstract embedding baseline
- [[concepts/beamforming|Beamforming]] — the delay-and-sum operation whose phase compensation the TSV encodes
- [[concepts/film-layer|FiLM Layer]] — integration mechanism in the GCSSF

## Related Sources

- [[sources/li-2026-geometry-conditioned-tse|Li & Doclo 2026: Geometry-Conditioned Target Speaker Extraction with Spatial Features]]
