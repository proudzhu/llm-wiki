---
type: concept
created: 2026-11-01
updated: 2026-11-01
sources:
  - raw/papers/yan-2025-lisennet/full-text.md
tags:
  - phase
  - speech-enhancement
  - signal-processing
  - post-processing
---

# GLA Phase Refinement

**GLA phase refinement** is the use of the Griffin–Lim algorithm (GLA) as a **parameter-free post-processor** for magnitude-based speech enhancement: given the network's estimated magnitude $\hat{\mathbf{A}}_y$ and the noisy phase $\mathbf{P}_x$ as initialization, GLA iteratively projects onto the set of STFT-consistent spectra to refine the phase. Reintroduced for lightweight SE by [[concepts/lisennet|LiSenNet]] (Yan et al., ICASSP 2025) and independently adopted by the lightS4 framework (Jiang et al. 2026).

## Mechanism

Starting from $\mathbf{P}^{(0)} = \mathbf{P}_x$, each iteration applies:

$$\boldsymbol{P}^{(k)} = \angle\,\mathrm{STFT}\left(\mathrm{iSTFT}\left(\mathbf{A}\,e^{j\boldsymbol{P}^{(k-1)}}\right)\right)$$

i.e., synthesize a waveform from the (fixed) estimated magnitude and current phase, re-analyze it, and keep the resulting phase. This is the classic Griffin & Lim (1983) phase-retrieval iteration; the fast variant is Perraudin et al. (2013).

## Why it works now

GLA phase reconstruction was historically judged inaccurate for SE because **errors in the enhanced magnitude** (speech distortion, residual noise) propagate into the phase at each iteration (Mayer et al. 2017; it was used for blind source separation by Sturmel & Daudet 2012). LiSenNet's argument for revisiting it: **modern SE models produce sufficiently accurate magnitude estimates**, so GLA's spectral-consistency projection now improves the phase rather than amplifying errors. It also costs **zero parameters** — attractive when the MACs budget is binding and a learned complex-domain decoder (à la [[concepts/complex-spectrum-mapping|complex spectrum mapping]]) is unaffordable.

## Cost–Quality Profile

| Configuration | PESQ (VBD) | Note |
|----------------|------------|------|
| Noisy phase | 3.02 | baseline reconstruction |
| GLA, k = 1 | 3.06 | one iteration |
| **GLA, k = 2** | **3.07** | LiSenNet default — converged |
| GLA, k = 3 | 3.07 | no further gain |

**k = 2 iterations suffice for convergence** (+0.05 PESQ over noisy phase). The lightS4 framework (Jiang et al. 2026) independently reports GLA (+0.08 PESQ over noisy phase at k = 4) with the same zero-parameter argument — two 2025–2026 works converging on the same finding.

## Relation to STFT Consistency

GLA refinement is the inference-time analogue of training-time [[concepts/stft-consistency|STFT-consistency enforcement]]: both project onto the consistent STFT subspace, but consistency training puts the projection inside the loss while GLA refinement applies it at synthesis. It also addresses the [[concepts/invalid-stft-problem|invalid STFT problem]] (enhanced magnitude + noisy phase may not correspond to any real waveform) — GLA's output is consistent by construction.

## Related Concepts

- [[concepts/lisennet|LiSenNet]]
- [[concepts/stft-consistency|STFT Consistency]]
- [[concepts/invalid-stft-problem|Invalid STFT Problem]]
- [[concepts/phase-difference-feature|Phase Difference (PD) Feature]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]

## Related Sources

- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]]
- [[sources/jiang-2026-lightweight-speech-enhancement-ssm-dsc|Jiang, Gao, Wang, Zou & Liu 2026: Lightweight SE with SSM and DSConv]]
