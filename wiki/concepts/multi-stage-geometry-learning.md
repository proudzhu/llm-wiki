---
type: concept
created: 2026-10-27
updated: 2026-10-27
sources:
  - raw/papers/baek-2025-geometry-invariant-doa-estimation/full-text.md
tags:
  - training-strategy
  - microphone-arrays
  - geometry-invariant
  - direction-of-arrival
  - deep-learning
---

# Multi-Stage Geometry Learning (MSGL)

**Multi-Stage Geometry Learning (MSGL)** is the geometry-axis half of [[concepts/complexity-gradual-training|Complexity Gradual Training (CGT)]]: a three-stage schedule that moves the training microphone array from a single fixed geometry to a dynamically positioned array with a *variable number of channels*. It was introduced by Baek, Chang & Cohen (2025) as the ingredient that makes geometry-invariant DOA estimation trainable at all.

## The Three Stages

| Stage | Array | Purpose | Epochs | LR $\delta$ | Weight decay $\lambda$ |
|:------|:------|:--------|:-------|:------------|:-----------------------|
| 1 | Fixed **ReSpeaker** 4-channel | Learn DOA estimation itself; geometric encoding barely matters yet | 1–5 | $2.5\times10^{-4}$ | $1.0\times10^{-4}$ |
| 2 | **Dynamic 4-channel** | Learn to *use* the [[concepts/doa-microphone-positional-encoding|MPE]] with a restricted, constant channel count | 6–10 | $5.0\times10^{-4}$ | $1.0\times10^{-6}$ |
| 3 | **Dynamic 4–12-channel** | Generalize across the variable channel counts met in practice | 11–300 | $1.0\times10^{-3}$ | $1.0\times10^{-6}$ |

Design rationale:

- **Stages 1–2 are deliberately short** (5 epochs each) so the bulk of the budget goes to the variable-count stage; each still converges in that time.
- **Learning rate rises and weight decay falls** across stages: strong early regularization prevents overfitting to the single stage-1 geometry, while the later stages need plasticity to accommodate dynamic arrays. This ordering matters — a uniform $\delta = 10^{-3}, \lambda = 10^{-6}$ cost the GI-DOAEnet ~8.4° MAE on LOCATA.
- **Skipping stage 2 or training only on stage 3 diverges**, exactly like replacing MPE with a learnable encoder.

## Random Array Generation

Dynamic stages place microphones in 3-D space subject to pair-distance bounds (in cm):

$$R_{\min} = \left[\max\left(1, 4 - 3\cdot\frac{C-C_{\min}}{C_{\max}-C_{\min}}\right), 6\right], \qquad
R_{\max} = \left[7, \max\left(7, 9 + 4\cdot\frac{C-C_{\min}}{C_{\max}-C_{\min}}\right)\right]$$

with $C_{\min} = 4$, $C_{\max} = 12$ and a coordinate-origin jitter $R_{\mathrm{origin}} = [-0.5, 0.5]$ cm (the origin sits at the array centre). The bounds trade off two failure modes:

- **too close** → inter-microphone TDOAs become indistinguishable;
- **too far apart** → spatial aliasing at high frequencies.

Larger $C$ relaxes both bounds (lower $R_{\min}$ and higher $R_{\max}$) because a bigger aperture supports a bigger spread. Rooms and array placement are randomized per utterance (room, RT60, array rotation, ≥ 0.1 m from walls), and each training batch uses a single channel count when the geometry is dynamic.

## Evidence

- With MPE + MSGL, validation loss recovers from the stage-2 shock and keeps decreasing; without MSGL (stage 3 only), it diverges.
- MSGL benefits other architectures too (Unet with SRP-PHAT input, Neural-SRP), improving the synthetic datasets in both cases.
- On the real RSL Dev set, MSGL's benefit is small or negative for Neural-SRP — the paper notes a real-vs-synthetic trade-off when MSGL is added on top of DSCL.

## Related Concepts

- [[concepts/complexity-gradual-training|Complexity Gradual Training (CGT)]]
- [[concepts/deeply-supervised-curriculum-learning|Deeply Supervised Curriculum Learning (DSCL)]]
- [[concepts/doa-microphone-positional-encoding|DOA-Microphone Positional Encoding]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/array-invariant-speech-enhancement|Array-Invariant Speech Enhancement]]

## Related Sources

- [[sources/baek-2025-geometry-invariant-doa-estimation|Baek, Chang & Cohen 2025: DNN-Based Geometry-Invariant DOA Estimation With Microphone Positional Encoding and Complexity Gradual Training]]
