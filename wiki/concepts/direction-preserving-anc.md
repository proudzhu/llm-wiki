---
type: concept
created: 2026-09-21
updated: 2026-09-21
sources:
  - raw/papers/yang-2026-direction-preserving-anc/full-text.txt
tags:
  - active-noise-control
  - direction-preserving-anc
  - spatial-filtering
  - deep-learning
  - control-filter-estimation
---

# Direction-Preserving ANC (DP-ANC)

**Direction-preserving active noise control (DP-ANC)** attenuates noise arriving from directions *other than* a specified desired direction while preserving the sound that naturally arrives *from* that direction. Unlike hear-through reproduction, the desired physical sound is never captured and re-played — it simply passes through undisturbed because the control filters generate (nearly) no secondary response to it.

Introduced and named by [[sources/yang-2026-direction-preserving-anc|Yang et al. 2026]], which realize it with a direction-conditioned control-filter estimation network.

## Cancellation–Preservation Objective

Decomposing the disturbance and secondary-path-filtered references into noise ($\mathbf{d}_n, \tilde{\mathbf{X}}_n$) and desired ($\mathbf{d}_d, \tilde{\mathbf{X}}_d$) components, the residual splits as $\mathbf{e} = (\mathbf{d}_n + \tilde{\mathbf{X}}_n\mathbf{w}) + (\mathbf{d}_d + \tilde{\mathbf{X}}_d\mathbf{w})$. DP-ANC minimizes the component-separated objective

$$\mathcal{L}_{\mathrm{DP}}(\mathbf{w}) = \|\bar{\mathbf{d}}_n + \bar{\mathbf{X}}_n\mathbf{w}\|_2^2 + \lambda \|\bar{\mathbf{X}}_d\mathbf{w}\|_2^2,$$

with per-component energy normalization (overbars) and a scalar weight $\lambda \ge 0$ that continuously trades cancellation against preservation. In the closed-form counterpart, the preservation term acts as a **direction-dependent quadratic regularizer** ($\lambda \tilde{\mathbf{X}}_d^T \tilde{\mathbf{X}}_d$ added to the normal equations) — filters that respond strongly to the desired direction are penalized, not hard-constrained.

## Learned Realization

Because the closed-form solution needs separated components and a fresh matrix solve per observation, Yang et al. train a [[concepts/film-layer|FiLM]]-conditioned convolutional network to output the complete multichannel FIR control-filter bank directly from a 0.5 s mixed-reference observation plus the desired direction, evaluated through a differentiable secondary-path-aware forward model (see [[concepts/end-to-end-differentiable-anc|differentiable ANC training]]) and independent signal realizations. Deployment keeps the conventional [[concepts/feedforward-anc|feedforward ANC]] signal path; no noise-direction label, filter bank, or matrix solve is needed, and filter-bank estimation costs ~0.01 GMACs vs ≈29 GMACs for the analytical solve.

## Positioning Among Directional ANC Methods

| Method family | Preservation mechanism | Recomputed per observation? | Delay on desired sound |
|:---------------|:----------------------|:---------------------------|:----------------------|
| Beamformer hear-through | Extract + reproduce via secondary source | Beamformer design | Yes (≈4 ms) |
| Analytical [[concepts/spatially-selective-anc|SSANC]] | Prescribed desired-direction response constraint | Yes (matrix solve) | Per prescribed response |
| Soft-constrained SSANC | Penalty on response deviation from prescribed model | Yes (matrix solve) | Per prescribed response |
| **DP-ANC (learned)** | Penalty on desired-induced control response | **No (single forward pass)** | None (natural arrival) |

DP-ANC is distinguished from [[concepts/generative-fixed-filter-anc|GFANC]]-style filter estimation by its explicit preservation objective, and from analytical SSANC by penalizing the control response itself rather than deviation from a prescribed target response.

## Performance Envelope

- Simulated 6-mic circular array ($r = 0.2$ m, 8 kHz): 22.8 dB mean NR at $D_{\mathrm{des}} = -11.4$ dB ($\lambda = 0.1$), dominating the analytical SSANC frontier by 0.7–3.1 dB NR at matched distortion.
- Measured Hearpiece/KEMAR paths (4 mics): 16.6 dB NR, $D_{\mathrm{des}} = -7.7$ dB.
- The achievable cancellation–preservation region is bounded by the reference array's spatial separability (manifold coherence $\eta \approx |J_0(2\kappa r \sin(\Delta\theta/2))|$): closely spaced desired/noise directions cannot be simultaneously cancelled and preserved by *any* design, learned or analytical.

## Related Concepts

- [[concepts/spatially-selective-anc|Spatially Selective ANC (SSANC)]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/generative-fixed-filter-anc|Generative Fixed-Filter ANC]]
- [[concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]]
- [[concepts/film-layer|FiLM Layer]]
- [[concepts/end-to-end-differentiable-anc|End-to-End Differentiable ANC]]
- [[concepts/speech-preserving-anc|Speech-Preserving ANC]]

## Related Sources

- [[sources/yang-2026-direction-preserving-anc|Yang et al. 2026: Direction-Preserving ANC with a Conditional Control-Filter Estimation Network]]
- [[sources/xiao-2023-spatially-selective-anc|Xiao, Xu & Zhao 2023: Spatially Selective ANC]]
- [[sources/xiao-2026-robust-spatially-selective-anc|Xiao 2026: Robust Soft-Constrained SSANC for Hearables]]
