---
type: concept
created: 2026-07-17
updated: 2026-07-17
sources:
  - raw/papers/valin-2021-percepnet-joint-echo-control/full-text.md
  - raw/papers/li-2025-echofree-neural-aec/full-text.md
  - raw/papers/seidel-2024-bark-scale-nn-residual-suppression/full-text.md
tags:
  - speech-enhancement
  - acoustic-echo-cancellation
  - low-complexity
  - hybrid-aec
  - real-time
---

# PercepNet-Style Neural Post Filter

A **PercepNet-style neural post filter** is a hybrid AEC / speech-enhancement architecture in which a traditional linear adaptive filter first removes the bulk of the (linear) echo, and a lightweight neural network operating on a **perceptually-spaced spectral representation** predicts a gain mask that suppresses residual echo and noise. The design originated with [[concepts/percepnet|PercepNet]] (Valin et al. ICASSP 2020, extended to joint echo control in 2021) for joint echo control and speech enhancement, and has since been refined by Bark-AEC (Seidel et al. ICASSP 2024) and EchoFree (Li et al. 2025).

> **Note on perceptual scale**: The original PercepNet uses the [[concepts/erb-scale|ERB scale]] (32 bands), **not** the Bark scale. Later "PercepNet-style" works — Bark-AEC and EchoFree — switched to the [[concepts/bark-scale-spectral-features|Bark scale]] (86 and 100 bands respectively). The "PercepNet-style" pattern name refers to the hybrid AEC + perceptual-band neural post filter architecture, not strictly to the Bark scale.

## Design Pattern

All PercepNet-style post filters share four ingredients:

1. **Linear front-end** — adaptive filter (MDF, NLMS, RLS, or [[concepts/frequency-domain-kalman-filter|frequency-domain Kalman filter]]) estimates the linear echo $\hat{e}(n)$ and produces a residual signal $z(n) = y(n) - \hat{e}(n)$.
2. **Perceptual feature extraction** — STFT magnitude is projected onto a perceptually-spaced filterbank (ERB for the original PercepNet, Bark for Bark-AEC / EchoFree), log-compressed, optionally augmented with first/second-order derivatives.
3. **Lightweight neural masker** — small DNN (conv + GRU, FC + GRU, or more recently a [[concepts/u-net-post-filter|U-Net post filter]]) takes perceptual features of $\{y, \hat{e}\}$ and predicts a bounded gain $\hat{\mathbf{g}} \in [0, 1]^{N_{\text{bands}}}$.
4. **Perceptual reconstruction** — gain is expanded back to linear STFT bins via $\mathbf{B}^\top \hat{\mathbf{g}}$ and multiplied by $|Y|$ to recover the estimated near-end magnitude; phase is inherited from $Y$.

## Representative Systems

| System | Year | Linear front-end | Perceptual scale | Neural backbone | Params | MACs/s | Notes |
|--------|------|------------------|------------------|-----------------|-------:|-------:|-------|
| [[concepts/percepnet|PercepNet]] (Valin et al.) | 2021 | [[concepts/multidelay-block-frequency-domain-adaptive-filter|MDF]] (SpeexDSP) | **32 ERB bands** | 2 conv + 5 GRU (8M weights, 8-bit quantized) | 8M | 800M | 1st place ICASSP 2021 AEC Challenge; [[concepts/pitch-coherence|pitch coherence]] + comb filter |
| Bark-AEC (Seidel et al.) | 2024 | Subband NLMS (oversampled FB) | 86 Bark bands | [[concepts/nsnet2|NSNet2]]-style FC + GRU | 1.58M | 235M | ICASSP 2024; CCMSE + STFT consistency loss |
| **EchoFree** (Li et al.) | 2025 | Partitioned-block FDAKF | 100 Bark bands | [[concepts/u-net-post-filter|U-Net]] | **0.28M** | **30M** | Two-stage SSL training; matches DeepVQE-S on ST FE/NE |

> **Note on Bark-AEC numbers**: The later [[sources/li-2025-echofree-neural-aec|EchoFree paper]] cites "Bark-AEC (Seidel et al. ICASSP 2024)" with 1.62M params / 107 MMACs/s, but the original Seidel 2024 paper reports **1.58M params / 235 MMACs/s / 86 Bark bands**. The table here uses the values from the original paper. The discrepancy may stem from different counting methodologies (inclusion/exclusion of LEC, mapping matrix, or different MACs/s protocols) or different model variants.

## Why Perceptual Features?

Perceptual-band projection $\mathbf{B}$ reduces the input dimension from $F = 257$ bins to a much smaller number of bands (32 ERB bands in the original PercepNet, 86–100 Bark bands in later works), an ~2.5×–8× compression. This compression is what makes sub-1000-MMACs/s AEC post filters feasible: the bulk of MACs in a neural masker scales with input dimension, so reducing 257 → 32–100 directly translates to ~2.5×–8× fewer MACs in the first encoder layer, with similar savings propagating through the rest of the network. The perceptual justification (ERB/Bark ≈ human auditory critical bands) ensures that the compression discards perceptually irrelevant detail rather than speech-discriminative information.

## Distinction from Other Hybrid AEC Patterns

| Pattern | Linear stage | Neural stage input | Representative |
|---------|--------------|--------------------|----------------|
| **PercepNet-style** | MDF / LAEC (linear only) | Perceptual-band features (ERB or Bark) | PercepNet, EchoFree, Bark-AEC |
| **Cross-attention hybrid** | Optional (alignment block replaces it) | Power-law compressed complex spectrum | [[sources/indenbom-2023-deepvqe|DeepVQE]] |
| **Sub-band interleaved** | LAEC | Sub-band stacked linear features | [[sources/shetu-2024-hybrid-low-complexity-aenr|ULCNet-AER]] |
| **End-to-end neural** | None | Raw mic + far-end STFT | EchoFilter (Ma 2021) |

PercepNet-style is the most parameter-efficient of these because it leverages perceptual-band compression plus a tiny backbone, at the cost of forgoing phase-aware processing and complex mask estimation. DeepVQE's cross-attention + CCM achieves higher absolute quality (especially DT metrics) but at 10× the compute of EchoFree.

## Related Concepts

- [[concepts/percepnet|PercepNet]]
- [[concepts/erb-scale|ERB Scale]] — perceptual scale used by the original PercepNet
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]] — perceptual scale used by Bark-AEC and EchoFree
- [[concepts/pitch-coherence|Pitch Coherence]]
- [[concepts/multidelay-block-frequency-domain-adaptive-filter|Multidelay Block Frequency-Domain Adaptive Filter (MDF)]]
- [[concepts/structured-sparsity|Structured Sparsity]]
- [[concepts/u-net-post-filter|U-Net Post Filter]]
- [[concepts/nsnet2|NSNet2]]
- [[concepts/complex-compressed-mse|Complex Compressed MSE (CCMSE)]]
- [[concepts/stft-consistency|STFT Consistency]]
- [[concepts/oversampled-filterbank|Oversampled Filterbank]]
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]]
- [[concepts/frequency-domain-kalman-filter|Frequency-Domain Kalman Filter]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]

## Related Sources

- [[sources/valin-2021-percepnet-joint-echo-control|Valin et al. 2021: PercepNet Joint Echo Control]] — the original PercepNet-style hybrid AEC system (ERB-based, 1st place ICASSP 2021 AEC Challenge)
- [[sources/seidel-2024-bark-scale-nn-residual-suppression|Seidel, Mowlaee & Fingscheidt 2024]] — Bark-AEC, later PercepNet-style variant using the Bark scale (86 bands) instead of ERB
- [[sources/li-2025-echofree-neural-aec|Li et al. 2025: EchoFree]] — latest PercepNet-style instance; introduces the U-Net variant and SSL two-stage training (100 Bark bands)
- [[sources/shetu-2024-hybrid-low-complexity-aenr|Shetu et al. 2024: Hybrid Low-Complexity AENR]] — ULCNet-AER, a non-PercepNet low-complexity baseline for comparison
- [[sources/indenbom-2023-deepvqe|Indenbom et al. 2023: DeepVQE]] — non-PercepNet SOTA used as upper-bound comparison in EchoFree
