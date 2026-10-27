---
type: concept
created: 2026-10-27
updated: 2026-10-27
sources:
  - raw/papers/baek-2025-geometry-invariant-doa-estimation/full-text.md
tags:
  - curriculum-learning
  - deep-supervision
  - training-strategy
  - direction-of-arrival
  - deep-learning
---

# Deeply Supervised Curriculum Learning (DSCL)

**Deeply Supervised Curriculum Learning (DSCL)** is a training scheme for deep [[concepts/direction-of-arrival-estimation|DOA]] estimators that supervises **every output head** with a **soft spatial-spectrum label whose beamwidth anneals over training**. Proposed by Baek, Yang & Chang (Interspeech 2023) and adopted as the label-axis component of [[concepts/complexity-gradual-training|Complexity Gradual Training (CGT)]] in Baek, Chang & Cohen (2025).

## Soft Labels

Instead of a one-hot (or fixed-width Gaussian) angular target, the label is a cosine-distance gain function:

$$g(t, \gamma_o) = \begin{cases} \max_{\psi' \in \Psi_t} \left\{ e^{\kappa(\gamma_o)\left(\cos d(\psi,\psi') - 1\right)} \right\}, & |\Psi_t| > 0 \\ 0, & \text{otherwise} \end{cases}$$

$$d(\psi,\psi') = \left|\psi - \psi'\right|, \qquad \kappa(\gamma) = \frac{-\ln\sqrt{2}}{\cos\gamma - 1}$$

where $\Psi_t$ is the set of active target azimuths in frame $t$, $\psi$ the vector of $D$ candidate azimuths, and $\gamma_o$ the beamwidth of the $o$-th head's target. The constant $\kappa(\gamma)$ is chosen so that the gain equals $-3$ dB exactly at angular distance $\gamma$, matching the beamwidth definition.

$\gamma$ must be constrained to $[0°, 180°]$ to avoid ambiguity from the periodicity of the cosine.

## The Two Components

| Component | Mechanism | Effect |
|:----------|:----------|:-------|
| **Deep supervision (DS)** | Each of the $N_O$ spatial-spectrum heads is supervised, with its own beamwidth $\gamma_o$ (e.g. $[16°, 6°, 2.5°]$, widest at the shallowest head) | Supplies several spatial relationships simultaneously; each head learns a different resolution of the same target |
| **Curriculum learning (CL)** | $\gamma_o$ starts wide, is held for the first $E_{\text{CL}}$ epochs, then annealed to $\gamma_o^{\text{end}}$ (e.g. all $2.5°$) and fixed | Moves the task from easy/ambiguous to hard/distinct, focusing the output on the true peak |

The loss is **binary cross-entropy** between the soft label and each head's sigmoid output spectrum, summed over heads.

## Behaviour

- **Wide $\gamma$** → large target vicinities, smoothed spectra, more spatial context, faster and more robust learning, but a less distinct peak.
- **Narrow $\gamma$** → small target vicinities, harder to learn, but a sharply focused peak (which is what peak-picking decoding needs).
- Annealing **also lowers the loss floor**, so CL and no-CL validation curves are not directly comparable; a model that "converges" only under CL may still be unable to encode the conditioning signal (this is exactly how a learnable geometry encoder masqueraded as converged in Baek et al. 2025).

## Empirical Findings

- In Baek et al. 2025, a **static** narrow target ($\gamma = 2.5°$ throughout) fails to converge for the geometry-invariant GI-DOAEnet, whereas the annealed soft label trains stably — the wide-beamwidth phase is what makes the hard target learnable in the first place.
- Removing either DS or CL individually degraded most datasets (e.g. GI-DOAEnet^PM Dynamic MAE 14.59° → 17.69° without DS, → 16.25° without CL), with isolated metric wins — the pair is what matters.
- DSCL transfers to other architectures: Neural-SRP improved on all six datasets with DSCL (RSL Eval MAE 18.15° → 14.39°).

## Related Concepts

- [[concepts/complexity-gradual-training|Complexity Gradual Training (CGT)]]
- [[concepts/multi-stage-geometry-learning|Multi-Stage Geometry Learning (MSGL)]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/dnn-based-doa-classifier|DNN-based DoA Classifier]] — the hard-label, single-head alternative for per-bin speaker presence

## Related Sources

- [[sources/baek-2025-geometry-invariant-doa-estimation|Baek, Chang & Cohen 2025: DNN-Based Geometry-Invariant DOA Estimation With Microphone Positional Encoding and Complexity Gradual Training]]
