---
type: concept
created: 2026-09-19
updated: 2026-09-19
sources:
  - raw/papers/pan-2025-data-driven-acoustics/full-text.md
tags:
  - loss-function
  - speech-enhancement
  - source-separation
  - signal-estimation
---

# SI-SDR (Scale-Invariant Signal-to-Distortion Ratio)

SI-SDR is a waveform-level distance and training loss for signal estimation (speech enhancement, separation) that is invariant to the scale of the estimate: if $\hat{\bm{s}}(t) = c \cdot \bm{s}(t)$ for a non-zero constant $c$, the distance is zero. Proposed by Le Roux et al. 2019 ("SDR — Half-Baked or Well Done?") to fix the ill-posedness of plain SNR/SDR under scale mismatch.

## Formulation

The optimal scale factor is obtained in closed form by projecting the estimate onto the target:

$$
\alpha_t = \arg\min_{\alpha} \|\alpha \bm{s}(t) - \hat{\bm{s}}(t)\|^{2} = \frac{\hat{\bm{s}}^{T}(t)\bm{s}(t)}{\|\bm{s}(t)\|^{2}}
$$

The SI-SDR loss treats the residual as noise and takes the (negative, per frame) log ratio:

$$
\mathcal{J} = -\sum_{t} 10\log\left(\frac{\|\alpha_t \bm{s}(t)\|^{2}}{\|\alpha_t \bm{s}(t) - \hat{\bm{s}}(t)\|^{2}}\right)
$$

## Equivalence to Correlation Maximization (Pan 2025)

Pan 2025 shows the loss simplifies to a monotone function of the Pearson correlation coefficient $\rho_{\bm{s}\hat{\bm{s}}}(t) = \hat{\bm{s}}^{T}(t)\bm{s}(t) / (\|\bm{s}(t)\| \cdot \|\hat{\bm{s}}(t)\|)$:

$$
\mathcal{J} = -\sum_{t} \frac{\rho_{\bm{s}\hat{\bm{s}}}^{2}(t)}{1 - \rho_{\bm{s}\hat{\bm{s}}}^{2}(t)}
$$

Minimizing SI-SDR loss is therefore **equivalent to maximizing the correlation coefficient** between the target and the estimate — a classical signal-processing criterion. This connects the deep-learning loss to the Pearson-correlation view of noise reduction (Cohen, Huang, Chen & Benesty 2009).

## Usage

- Standard evaluation metric and training loss for [[concepts/speech-enhancement|speech enhancement]] and [[concepts/blind-source-separation|source separation]] (e.g., ConvTasNet and successors train directly on SI-SDR).
- Appears throughout the diffusion-for-SE literature as a reporting metric (see [[concepts/diffusion-models-for-speech|diffusion models for speech]] benchmark tables).
- Scale invariance removes the degree of freedom that plain MSE wastes on amplitude matching, letting the network focus on waveform shape; the trade-off is insensitivity to overall level errors.

## Related Concepts

- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/permutation-invariant-training|Permutation Invariant Training]] — SI-SDR is the usual per-source distance $d[\cdot,\cdot]$ inside the PIT minimization
- [[concepts/frequency-domain-loss|Frequency-Domain Loss]] — the spectral-domain alternative
- [[concepts/wiener-filter|Wiener Filter]]

## Related Sources

- [[sources/pan-2025-data-driven-acoustics|Pan 2025: Fundamentals of Data-Driven Approaches to Acoustic Signal Detection, Filtering, and Transformation]] — derives the SI-SDR–correlation-coefficient equivalence in Section 7.2.3
