---
type: concept
created: 2026-09-20
updated: 2026-09-20
sources:
  - raw/papers/uphaus-2026-directivity-low-latency/full-text.md
tags:
  - loss-function
  - speech-enhancement
  - binaural
  - phase-processing
  - neural-directional-filtering
---

# IPD Preservation Loss

The **IPD preservation loss** is a training objective proposed by [[entities/lennart-uphaus|Uphaus]] et al. (2026) for [[concepts/film-osn|FiLM-OSN]] binaural neural directional filtering. It penalizes deviations of the **interaural (cross-channel) phase difference** between prediction and target, and is shown to be essential for the network to actually realize the directivity pattern it is conditioned on.

## Formulation

$$
\mathcal{L}_{\mathrm{IPD}}=\frac{\sum_{f,t}\left|Y_{0}(f,t)\right|^{2}\left[1-\cos\!\left(\hat{\Phi}(f,t)-\Phi(f,t)\right)\right]}{\sum_{f,t}\left|Y_{0}(f,t)\right|^{2}+\epsilon},
$$

where $\hat{\Phi}(f,t)$ and $\Phi(f,t)$ are the cross-channel phase differences of the prediction and target. Design choices:

- **Cosine instead of raw phase difference**: avoids phase ambiguities (unwrapped-phase wrapping at $\pm\pi$), following directional statistics (Mardia & Jupp 1999).
- **Magnitude weighting by $|Y_0|^2$**: reduces the contribution of low-energy time-frequency regions, where phase is perceptually and estimation-wise unreliable.

It is combined additively with the batch-aggregated normalized $\mathcal{L}_1$ loss:

$$
\mathcal{L}_{1,\text{IPD}}=\mathcal{L}_{1}+\alpha\,\mathcal{L}_{\text{IPD}}, \qquad \alpha=0.03.
$$

## Why it matters

A time-domain $\mathcal{L}_1$ loss preserves the interaural time difference (ITD) but says nothing about **cross-channel spectral coherence**: a model trained with $\mathcal{L}_1$ alone (FiLM-OSN, Uphaus et al. 2026) achieves the *best* quality metrics (PESQ/ESTOI/SI-SDR) yet **entirely disregards the conditioned directivity pattern** and exhibits coherence behavior unrelated to the target. Adding the IPD term restores the spectral relations between channels, which aligns the estimated directivity pattern with the desired one — a case where objective speech-quality metrics fail to reveal a functional failure that a pattern-level analysis exposes.

## Related Concepts

- [[concepts/film-osn|FiLM-OSN]]
- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/spatial-coherence|Spatial Coherence]]

## Related Sources

- [[sources/uphaus-2026-directivity-low-latency|Uphaus et al. 2026: Directivity-Conditioned Low-Latency Neural Filtering]] — the introducing paper
