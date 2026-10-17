---
type: concept
created: 2026-05-23
updated: 2026-10-17
sources:
  - raw/papers/maeda-1999-anc-simultaneous-perturbation/full-text.md
tags:
  - active-noise-control
  - adaptive-filtering
  - simultaneous-equations-method
---

# Simultaneous Equations Method

The simultaneous equations method is an approach for feedforward active noise control ([[concepts/feedforward-anc|Feedforward ANC]]) that estimates the optimal noise control filter coefficients **without requiring an explicit secondary path model**. Instead of the conventional filtered-x algorithm's secondary path filter, it uses an **auxiliary filter** that identifies the overall path from the noise control filter input to the error microphone output.

## Principle

In a feedforward ANC system, the auxiliary filter $S(z)$ identifies the overall path:

$$
S(z) = P(z) + H(z) \tilde{C}(z)
$$

where $P(z)$ is the primary path, $\tilde{C}(z)$ is the effective secondary path, and $H(z)$ is the noise control filter.

By giving **two different coefficient vectors** $H_1(z)$ and $H_2(z)$ to the noise control filter, two independent equations are obtained:

$$
\begin{aligned}
S_1(z) &= P(z) + H_1(z) \tilde{C}(z) \\
S_2(z) &= P(z) + H_2(z) \tilde{C}(z)
\end{aligned}
$$

Solving yields the optimal filter directly:

$$
H_{\text{opt}}(z) = \frac{S_1(z) H_2(z) - S_2(z) H_1(z)}{S_2(z) - S_1(z)}
$$

**Key insight**: No explicit secondary path model is needed — the auxiliary filter captures the current overall path, enabling automatic tracking of secondary path changes.

## Advantages Over Filtered-x Algorithm

| Aspect | Filtered-x LMS | Simultaneous Equations Method |
|--------|---------------|-------------------------------|
| **Secondary path model** | Required (must be re-identified when path changes) | Not required |
| **Extra noise injection** | May be needed for online modeling | Not needed |
| **Convergence speed** | Moderate | Higher (especially with frequency-domain adaptation) |
| **Automatic recovery** | Not built-in | Inherent via iterative updating |
| **Computational cost** | Lower per iteration | Can be lower overall (no separate path identification) |

## Frequency-Domain Implementation

The frequency-domain version estimates $S_1(k), S_2(k)$ using an adaptive algorithm and computes the optimal filter element-wise in the frequency domain:

$$
H_{\text{opt}}(k) = \frac{S_1(k) H_2(k) - S_2(k) H_1(k)}{S_2(k) - S_1(k)}
$$

The result is transformed back to the time domain via inverse FFT.

## Relation to the Perturbation Approach

Both the simultaneous equations method and the [[concepts/simultaneous-perturbation|simultaneous perturbation]] ANC of [[sources/maeda-1999-anc-simultaneous-perturbation|Maeda & Yoshida 1999]] eliminate the secondary path model from feedforward ANC, but by opposite means: this method *solves* for the optimal filter algebraically through an auxiliary overall-path filter (requiring two different control-filter vectors and path identification), whereas the perturbation method *measures* the gradient of the block error power by perturbing all taps at once (requiring no auxiliary filter, at the cost of perturbation noise in the output and block-granular convergence).

## Related Concepts

- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/auxiliary-filter|Auxiliary Filter]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]
- [[concepts/frequency-domain-anc|Frequency Domain ANC]]
- [[concepts/simultaneous-perturbation|Simultaneous Perturbation]] — the measurement-based route to the same secondary-path-model-free goal

## Related Sources

- [[sources/fujii-2006-simultaneous-equations-anc|Fujii et al. 2006: Verification of Simultaneous Equations Method by an Experimental Active Noise Control System]]
- [[sources/maeda-1999-anc-simultaneous-perturbation|Maeda & Yoshida 1999: ANC Using Simultaneous Perturbation]] — the sibling secondary-path-free approach: gradient measured by perturbation instead of solved algebraically
