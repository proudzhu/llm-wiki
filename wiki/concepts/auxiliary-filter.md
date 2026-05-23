---
type: concept
created: 2026-05-23
updated: 2026-05-23
tags:
  - active-noise-control
  - adaptive-filtering
---

# Auxiliary Filter

In feedforward active noise control ([[concepts/feedforward-anc|Feedforward ANC]]), an auxiliary filter is a filter that identifies the **overall path** from the noise control filter's input through the primary path, noise control filter, and secondary path, to the error microphone output.

## Role in the Simultaneous Equations Method

In the [[concepts/simultaneous-equations-method|Simultaneous Equations Method]], the auxiliary filter $S(z)$ serves as a substitute for the secondary path filter used in the filtered-x algorithm. Its key characteristic is:

$$
S(z) = P(z) + H(z) \tilde{C}(z)
$$

where $P(z)$ is the primary path, $\tilde{C}(z)$ is the effective secondary path (including feedback cancellation), and $H(z)$ is the noise control filter.

## How It Works

The auxiliary filter is updated adaptively (typically via frequency-domain adaptive algorithms, NLMS, or cross-spectrum methods) to match the overall system response. By obtaining two independent estimates $S_1(z)$ and $S_2(z)$ corresponding to two different noise control filter settings $H_1(z)$ and $H_2(z)$, the primary and secondary paths can be algebraically solved without explicit identification.

## Related Concepts

- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/simultaneous-equations-method|Simultaneous Equations Method]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]
- [[concepts/system-identification|System Identification]]

## Related Sources

- [[sources/fujii-2006-simultaneous-equations-anc|Fujii et al. 2006: Verification of Simultaneous Equations Method by an Experimental Active Noise Control System]]
