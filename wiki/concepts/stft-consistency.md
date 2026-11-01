---
type: concept
created: 2026-07-17
updated: 2026-11-01
sources:
  - raw/papers/seidel-2024-bark-scale-nn-residual-suppression/full-text.md
  - raw/papers/yan-2025-lisennet/full-text.md
  - raw/papers/ahn-2026-fastenhancer/full-text.md
tags:
  - speech-enhancement
  - signal-processing
  - training-objective
  - deep-learning
---

# STFT Consistency

**STFT consistency** (or **STFT-consistency enforcement**) is a training technique for speech-enhancement neural networks in which the estimated time-domain signal $\hat{s}(n)$ is re-transformed to the STFT domain before the loss is computed. This enforces that the loss is evaluated on a signal that lies in the consistent STFT subspace — i.e., one that actually corresponds to a real time-domain waveform — rather than on a freely modified mask that may not correspond to any physical signal.

## Definition

Given a network that predicts a mask $M_\ell(k)$ applied to a noisy STFT, the masked output

$$
\hat{S}_\ell(k) = M_\ell(k) E_\ell(k)
$$

is in general **inconsistent** — that is, no single time-domain signal has $\hat{S}_\ell(k)$ as its STFT, because the mask modifies magnitude and/or phase in a way that violates the STFT redundancy (overlap-add structure).

To enforce consistency, the network output $\hat{S}_\ell(k)$ is first inverted to time domain via inverse STFT and overlap-add to obtain $\hat{s}(n)$, then re-transformed via a forward STFT to obtain $\tilde{S}_\ell(k)$. The loss is then computed on the **consistent** spectrum $\tilde{S}_\ell(k)$:

$$
\mathcal{L} = \mathrm{Loss}\bigl(\tilde{S}_\ell(k),\, S_\ell(k)\bigr).
$$

The re-analysis step "projects" the network's output onto the consistent STFT subspace before evaluation.

## Origin

The technique was formalized by Wisdom et al. (ICASSP 2019) — "Differentiable Consistency Constraints for Improved Deep Speech Enhancement" — and is sometimes called the **Wisdom consistency** or **STFT consistency constraint**.

## Role in Hybrid AEC Training

STFT consistency is used together with the [[concepts/complex-compressed-mse\|CCMSE]] loss in several hybrid AEC postfilters, including [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Seidel et al. 2024]], where it ensures that the loss is computed on a signal obtained by re-applying the square-root Hann window and DFT to the inverse-STFT output $\hat{s}(n)$.

## Why It Matters

- **Gradient quality**: Without consistency, the network may exploit the redundancy of the STFT (multiple masks producing the same loss) in pathological ways during training. Consistency constraints stabilize gradients.
- **Phase-aware losses**: When using complex (phase-aware) losses like CCMSE, evaluating on an inconsistent spectrum means the phase term is meaningless — the predicted phase may not correspond to any real signal. Consistency enforcement fixes this.
- **Better convergence**: Empirically, consistency-constrained training yields faster and more stable convergence than direct mask-domain losses.

FastEnhancer (Ahn et al. 2026) — uses a *training-time* consistency loss ($\mathcal{L}_{con} = \|\mathbf{Y}_c - \mathrm{STFT}_c(\hat{\mathbf{y}})\|_2^2$, weight 0.3) inside its five-term composite loss: the synthesized waveform's re-analyzed compressed spectrum is pulled toward the clean target, ensuring the mask output and the iSTFT output agree.

## Related Concepts

- [[concepts/complex-compressed-mse\|Complex Compressed MSE (CCMSE)]]
- [[concepts/nsnet2\|NSNet2]]
- [[concepts/speech-enhancement\|Speech Enhancement]]
- [[concepts/lisennet|LiSenNet]]
- [[concepts/phase-difference-feature|Phase Difference (PD) Feature]]
- [[concepts/gla-phase-refinement|GLA Phase Refinement]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]

## Related Sources

- [[sources/seidel-2024-bark-scale-nn-residual-suppression|Seidel, Mowlaee & Fingscheidt 2024]] — uses STFT consistency in conjunction with CCMSE for training the Bark-scale postfilter
- [[sources/liu-2023-iccrn|Liu & Zhang 2023: ICCRN]] — applies STFT consistency for the weighted L1 RI+amplitude loss in [[concepts/complex-spectrum-mapping|CSM]] training: the estimated complex spectrum is inverted to the time domain and re-transformed back to the TF domain before computing the loss
- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]] — the *inference-time* analogue: a 2-iteration Griffin–Lim projection onto the consistent STFT subspace refines the phase before synthesis (see [[concepts/gla-phase-refinement|GLA Phase Refinement]]), rather than enforcing consistency during training
- [[sources/ahn-2026-fastenhancer|Ahn, Han, Woo & Kim 2026: FastEnhancer]] — training-time consistency loss $\|\mathbf{Y}_c - \mathrm{STFT}_c(\hat{\mathbf{y}})\|_2^2$ (weight 0.3) inside the five-term composite loss
