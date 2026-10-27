---
type: concept
created: 2026-10-27
updated: 2026-10-27
sources:
  - raw/papers/baek-2025-geometry-invariant-doa-estimation/full-text.md
tags:
  - training-strategy
  - curriculum-learning
  - deep-learning
  - microphone-arrays
  - direction-of-arrival
  - geometry-invariant
---

# Complexity Gradual Training (CGT)

**Complexity Gradual Training (CGT)** is a training paradigm for tasks whose difficulty is a *two-dimensional* function of (i) the *label sharpness* and (ii) the *input-geometry variability*. Introduced by Baek, Chang & Cohen (2025) for geometry-invariant DOA estimation, CGT = [[concepts/deeply-supervised-curriculum-learning|Deeply Supervised Curriculum Learning (DSCL)]] over the label axis + [[concepts/multi-stage-geometry-learning|Multi-Stage Geometry Learning (MSGL)]] over the geometry axis.

## Motivation

Training a geometry-invariant DOA network from scratch on mixtures of many array configurations **does not converge**. The network must simultaneously (a) learn to estimate a spatial spectrum from multichannel audio and (b) learn how to interpret the array-geometry encoding that steers its features. Baek et al. report that both failure modes of their GI-DOAEnet — replacing the [[concepts/doa-microphone-positional-encoding|MPE]] with a learnable coordinate encoder (MLE), and dropping the staged geometry schedule — show the same symptom: validation loss rises at the transition to multiple geometries and never recovers.

CGT therefore raises task difficulty along both axes in a coordinated schedule rather than all at once:

| Axis | Instrument | What is graded |
|:-----|:-----------|:---------------|
| **Labels** | DSCL soft labels | Beamwidth $\gamma_o$ of the target spectrum: wide/ambiguous → narrow/peaked, per output head and per epoch |
| **Geometry** | MSGL stages | Fixed single array → dynamic positions with fixed channel count → dynamic positions with variable channel count (4–12) |

## Formulation (Baek et al. 2025)

Soft target for frame $t$ and the $o$-th output head:

$$g(t, \gamma_o) = \max_{\psi' \in \Psi_t} e^{\kappa(\gamma_o)\left(\cos d(\psi,\psi') - 1\right)}, \qquad \kappa(\gamma) = \frac{-\ln\sqrt{2}}{\cos\gamma - 1}$$

so that a target azimuth receives 1 and any azimuth at angular distance $\gamma_o$ receives 3 dB down. The per-head beamwidth follows

$$\gamma_o = \gamma_o^{\text{init}} \ \text{(fixed until epoch } E_{\text{CL}}\text{)} \;\longrightarrow\; \gamma_o^{\text{end}},$$

with the geometry schedule advancing underneath. In the original instantiation: $\gamma^{\text{init}} = [16°, 6°, 2.5°]$, $\gamma^{\text{end}} = [2.5°, 2.5°, 2.5°]$, curriculum learning starting only after a few epochs of the final MSGL stage (epoch 20, annealed to $\gamma^{\text{end}}$ by epoch 45).

## Why Gradualism Works Here

1. **Decoupling**: stage 1 teaches DOA estimation under a fixed geometry where the geometric encoding is nearly irrelevant, so the DNN parameters converge before geometry starts moving.
2. **Anchoring**: wide beamwidths give a smooth, high-entropy objective with many informative gradient directions; narrow beamwidths alone (e.g. a static $\gamma = 2.5°$) fail to converge in the same setup.
3. **Lower loss floor**: CL also *lowers* the binary cross-entropy floor as $\gamma$ shrinks, which is why CL and no-CL validation curves are not directly comparable — a "converging" MLE run under CL is an artefact of the easier objective, not evidence that the geometry encoding works.

## Transferability

CGT is not architecture-specific: applying DSCL (and then MSGL) to a SRP-PHAT-input **Unet** and to **Neural-SRP** improved both in the same paper (Neural-SRP RSL Eval MAE 18.15° → 14.39° with DSCL; synthetic sets improved further with MSGL). The authors position CGT as a general recipe for "geometry-sensitive learning problems", and propose extending it to beamforming in future work.

## Design Knobs and Ablations (Baek et al. 2025, Table V)

- **Stage-wise learning rate / weight decay**: $\delta$ increases across stages (2.5e-4 → 5e-4 → 1e-3) while $\lambda$ drops (1e-4 → 1e-6). Fixing $\delta = 10^{-3}$, $\lambda = 10^{-6}$ everywhere degraded most metrics (LOCATA MAE 7.82° → 16.25°); smaller LRs under-converged. High early weight decay prevents overfitting to the single stage-1 array.
- **Stage lengths**: stages 1–2 are deliberately short (5 epochs each) because most training budget belongs to the variable-channel stage.
- **Removing deep supervision** or **removing curriculum learning** each degraded most datasets but produced isolated wins — neither component is individually load-bearing in every condition, but both together are.
- **Static narrow labels** ($\gamma = 2.5°$ from the start) fail outright.

## Related Concepts

- [[concepts/multi-stage-geometry-learning|Multi-Stage Geometry Learning (MSGL)]]
- [[concepts/deeply-supervised-curriculum-learning|Deeply Supervised Curriculum Learning (DSCL)]]
- [[concepts/doa-microphone-positional-encoding|DOA-Microphone Positional Encoding]]
- [[concepts/channel-wise-softmax-aggregation|Channel-Wise Softmax Aggregation (CWSA)]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/array-invariant-speech-enhancement|Array-Invariant Speech Enhancement]] — the SE-side analogue, where geometry variability is usually handled by architecture alone

## Related Sources

- [[sources/baek-2025-geometry-invariant-doa-estimation|Baek, Chang & Cohen 2025: DNN-Based Geometry-Invariant DOA Estimation With Microphone Positional Encoding and Complexity Gradual Training]]
