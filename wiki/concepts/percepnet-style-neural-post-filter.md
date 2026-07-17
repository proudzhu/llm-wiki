---
type: concept
created: 2026-07-17
updated: 2026-07-17
sources:
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

A **PercepNet-style neural post filter** is a hybrid AEC / speech-enhancement architecture in which a traditional linear adaptive filter first removes the bulk of the (linear) echo, and a lightweight neural network operating on a [[concepts/bark-scale-spectral-features\|Bark-scale perceptual representation]] predicts a gain mask that suppresses residual echo and noise. The design originated with PercepNet (Valin et al. ICASSP 2021) for joint echo control and speech enhancement, and has since been refined by Bark-AEC (Seidel et al. ICASSP 2024) and EchoFree (Li et al. 2025).

## Design Pattern

All PercepNet-style post filters share four ingredients:

1. **Linear front-end** — adaptive filter (NLMS, RLS, or [[concepts/frequency-domain-kalman-filter\|frequency-domain Kalman filter]]) estimates the linear echo $\hat{e}(n)$ and produces a residual signal $z(n) = y(n) - \hat{e}(n)$.
2. **Perceptual feature extraction** — STFT magnitude is projected onto a Bark-scale filterbank (typically 100 sub-bands), log-compressed, optionally augmented with first/second-order derivatives.
3. **Lightweight neural masker** — small DNN (FC + GRU, or more recently a [[concepts/u-net-post-filter\|U-Net post filter]]) takes Bark features of $\{y, \hat{e}\}$ and predicts a bounded gain $\hat{\mathbf{g}} \in [0, 1]^{N_{\text{Bark}}}$.
4. **Perceptual reconstruction** — Bark gain is expanded back to linear STFT bins via $\mathbf{B}^\top \hat{\mathbf{g}}$ and multiplied by $|Y|$ to recover the estimated near-end magnitude; phase is inherited from $Y$.

## Representative Systems

| System | Year | Linear front-end | Neural backbone | Params | MACs/s | Notes |
|--------|------|------------------|-----------------|-------:|-------:|-------|
| PercepNet (Valin et al.) | 2021 | LAEC | PercepNet (pitch-conditioned) | — | — | Joint echo + noise; uses periodicity + aperiodicity |
| Bark-AEC (Seidel et al.) | 2024 | Subband NLMS (oversampled FB) | [[concepts/nsnet2\|NSNet2]]-style FC + GRU on 86-band Bark features | 1.58M | 235M | ICASSP 2024; CCMSE + STFT consistency loss |
| **EchoFree** (Li et al.) | 2025 | Partitioned-block FDAKF | [[concepts/u-net-post-filter\|U-Net]] on Bark features | **0.28M** | **30M** | Two-stage SSL training; matches DeepVQE-S on ST FE/NE |

> **Note on Bark-AEC numbers**: The later [[sources/li-2025-echofree-neural-aec\|EchoFree paper]] cites "Bark-AEC (Seidel et al. ICASSP 2024)" with 1.62M params / 107 MMACs/s, but the original Seidel 2024 paper reports **1.58M params / 235 MMACs/s / 86 Bark bands**. The table here uses the values from the original paper. The discrepancy may stem from different counting methodologies (inclusion/exclusion of LEC, mapping matrix, or different MACs/s protocols) or different model variants.

## Why Perceptual Features?

The Bark projection $\mathbf{B}$ reduces the input dimension from $F = 257$ bins to $N_{\text{Bark}} \approx 100$ bands, an ~2.5× compression. This compression is what makes sub-100-MMACs/s AEC post filters feasible: the bulk of MACs in a neural masker scales with input dimension, so reducing 257 → 100 directly translates to ~2.5× fewer MACs in the first encoder layer, with similar savings propagating through the rest of the network. The perceptual justification (Bark ≈ human auditory critical bands) ensures that the compression discards perceptually irrelevant detail rather than speech-discriminative information.

## Distinction from Other Hybrid AEC Patterns

| Pattern | Linear stage | Neural stage input | Representative |
|---------|--------------|--------------------|----------------|
| **PercepNet-style** | LAEC (linear only) | Bark-scale features | EchoFree, Bark-AEC, PercepNet |
| **Cross-attention hybrid** | Optional (alignment block replaces it) | Power-law compressed complex spectrum | [[sources/indenbom-2023-deepvqe\|DeepVQE]] |
| **Sub-band interleaved** | LAEC | Sub-band stacked linear features | [[sources/shetu-2024-hybrid-low-complexity-aenr\|ULCNet-AER]] |
| **End-to-end neural** | None | Raw mic + far-end STFT | EchoFilter (Ma 2021) |

PercepNet-style is the most parameter-efficient of these because it leverages the Bark compression plus a tiny backbone, at the cost of forgoing phase-aware processing and complex mask estimation. DeepVQE's cross-attention + CCM achieves higher absolute quality (especially DT metrics) but at 10× the compute of EchoFree.

## Related Concepts

- [[concepts/bark-scale-spectral-features\|Bark-Scale Spectral Features]]
- [[concepts/u-net-post-filter\|U-Net Post Filter]]
- [[concepts/nsnet2\|NSNet2]]
- [[concepts/complex-compressed-mse\|Complex Compressed MSE (CCMSE)]]
- [[concepts/stft-consistency\|STFT Consistency]]
- [[concepts/oversampled-filterbank\|Oversampled Filterbank]]
- [[concepts/acoustic-echo-cancellation\|Acoustic Echo Cancellation]]
- [[concepts/frequency-domain-kalman-filter\|Frequency-Domain Kalman Filter]]
- [[concepts/speech-enhancement\|Speech Enhancement]]
- [[concepts/adaptive-filtering\|Adaptive Filtering]]
- [[concepts/erb-scale\|ERB Scale]] — alternative perceptual scale used by DeepFilterNet / TANGO family

## Related Sources

- [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Seidel, Mowlaee & Fingscheidt 2024]] — Bark-AEC, the original 86-band NSNet2-style hybrid AEC postfilter
- [[sources/li-2025-echofree-neural-aec\|Li et al. 2025: EchoFree]] — latest PercepNet-style instance; introduces the U-Net variant and SSL two-stage training
- [[sources/shetu-2024-hybrid-low-complexity-aenr\|Shetu et al. 2024: Hybrid Low-Complexity AENR]] — ULCNet-AER, a non-PercepNet low-complexity baseline for comparison
- [[sources/indenbom-2023-deepvqe\|Indenbom et al. 2023: DeepVQE]] — non-PercepNet SOTA used as upper-bound comparison in EchoFree
