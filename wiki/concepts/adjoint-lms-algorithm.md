---
type: concept
created: 2026-04-28
updated: 2026-04-28
sources:
  - raw/papers/wang-2024-computation-efficient-virtual-sensing/full-text.txt
tags:
  - active-noise-control
  - adjoint-lms
  - multichannel-anc
  - computational-efficiency
---

# Adjoint LMS Algorithm

The **Adjoint LMS (ALMS)** algorithm is a variant of the [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] that filters the **error signal** instead of the reference signal, achieving significant computational savings in multichannel ANC systems.

## Core Idea

In standard FxLMS, the reference signal is filtered through the estimated secondary path $\hat{S}(z)$:

$$\mathbf{w}(n+1) = \mathbf{w}(n) + \mu \cdot e(n) \cdot \mathbf{x}_f(n), \quad \mathbf{x}_f(n) = \hat{\mathbf{s}}(n) * \mathbf{x}(n)$$

In ALMS, the error signal is filtered through the time-reversed estimated secondary path:

$$\mathbf{w}(n+1) = \mathbf{w}(n) - \mu \cdot \mathbf{x}(n-L+1) \cdot e'(n)$$

where $e'(n) = \sum_{i=0}^{L-1} e(n-L+1+i) \hat{s}_i$ is the time-reversed filtered error signal.

## Computational Advantage

For a multichannel system with $J$ reference microphones, $K$ secondary sources, and $M$ error microphones:

| Algorithm | Multiplications | Scaling |
|:----------|:----------------|:--------|
| MCFxLMS | $JKM(L+N_x+1) + MJN_h$ | $O(JKM)$ — cubic |
| MCALMS | $K(LM+JN_x+1) + MJN_h$ | $O(K)$ — linear in K |

At 10 channels, MCALMS requires approximately **1/10 the computation** of MCFxLMS.

## Why It Works

The adjoint approach exploits the mathematical equivalence between filtering the reference signal forward and filtering the error signal backward (time-reversed). This is an application of the **adjoint operator** property in linear systems:

$$\langle \hat{S}\mathbf{x}, \mathbf{e} \rangle = \langle \mathbf{x}, \hat{S}^*\mathbf{e} \rangle$$

where $\hat{S}^*$ is the adjoint (time-reversed) operator of $\hat{S}$.

## Limitations

- Requires storing past $L-1$ error samples for causality
- The time-reversed filtering may be less intuitive to implement than forward filtering
- Performance is equivalent to FxLMS only when the secondary path estimate is accurate

## Related Concepts

- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[../concepts/multi-channel-anc|Multi-Channel ANC]]
- [[../concepts/virtual-sensing|Virtual Sensing]]

## Related Sources

- [[../sources/wang-2024-computation-efficient-virtual-sensing|Wang 2024: Computation-Efficient Virtual Sensing with MCALMS]]
