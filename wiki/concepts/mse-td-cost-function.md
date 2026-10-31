---
type: concept
created: 2026-10-31
updated: 2026-10-31
sources:
  - raw/papers/forster-2022-optimal-microphone-positioning/full-text.txt
tags:
  - active-noise-control
  - multi-channel
  - wiener-filter
  - microphone-positioning
---

# MSE-TD Cost Function

The **MSE time-domain cost function (MSE-TD CF)** is a causality-aware evaluation criterion for multi-channel feedforward ANC, proposed by [[entities/jonas-forster|Forster]], [[entities/johannes-fabry|Fabry]] & [[entities/peter-jax|Jax]] (DAGA 2022) for selecting and positioning reference microphones on ANC headphones. It replaces the frequency-domain [[concepts/multiple-coherence-function|Multiple Coherence Function (MCF)]] — which bounds performance but ignores causality — with a time-domain multi-channel Wiener formulation whose resulting FIR filter coefficients are **causal**, so the criterion measures practically realizable performance.

## Formulation

For a MISO feedforward system with $J$ reference microphones, one error microphone, and one loudspeaker, define the filtered reference signal $r_j(n) = u_j(n) * s(n)$ (reference convolved with the secondary path) and its convolution matrix $\mathbf{r}_j \in \mathbb{R}^{L_{wr} \times L_w}$. The cost is the squared error at the error microphone:

$$
C = \left\| \mathbf{d} - \sum_{j \in \mathcal{J}} \mathbf{r}_j \tilde{\mathbf{w}}_j \right\|^2
$$

Minimizing over the feedforward filters $\tilde{\mathbf{w}}_j$ yields the recursive multi-channel Wiener solution per channel:

$$
\tilde{\mathbf{w}}_j = \left( \mathbf{r}_j^T \mathbf{r}_j \right)^{-1} \left( \mathbf{r}_j^T \mathbf{d} - \mathbf{r}_j^T \sum_{\nu \in \mathcal{J} \setminus j} \mathbf{r}_\nu \tilde{\mathbf{w}}_\nu \right)
$$

solvable by an extended Gauss–Jordan recursion. Structurally this is a MISO multi-channel Wiener filter on secondary-path-filtered references — the time-domain sibling of the [[concepts/filtered-x-mwf|Filtered-x MWF]] idea.

## Path-Based Form for Approximated Diffuse Fields

The decisive step is modeling the diffuse field as $M$ mutually uncorrelated white Gaussian noise sources in a horizontal ring around the headphone. Under this model, the correlation between filtered references,

$$
\phi_{r_j r_\nu}(\lambda) = \sum_{m=1}^{M} \phi^E_{\tilde{s}_j \tilde{s}_\nu}(\lambda),
$$

collapses to **impulse correlations between modified secondary paths** $\tilde{s}_j(n,\theta_m) = q_{\mathrm{ext},j}(n,\theta_m) * s(n)$ — the diffuse-field measurement is never needed. The cost becomes purely path-based:

$$
C = \sum_{m=1}^{M} \left\| q_{\mathrm{int}}(\theta_m) - \sum_{j \in \mathcal{J}} \tilde{\mathbf{s}}_j(\theta_m) \tilde{\mathbf{w}}_j \right\|^2
$$

so only per-DoA device-related impulse responses (DRIRs), measured in a lab, enter the criterion. This parallels the frequency-domain derivation of Elliott & Cheer (JASA 2015) for local active control with remote sensors in spatially random pressure fields, but in the time domain — which is what enforces causal filter coefficients.

## Why Causality Matters for Positioning

Applied to reference-microphone selection on a 12-microphone Bose QC25 (greedy search over measured DRIRs), the MSE-TD CF and the MCF agree while only ipsilateral microphones are being added, but **diverge on contralateral candidates**: the MCF predicts continued gains, while the causality-constrained MSE-TD CF shows contralateral microphones contribute essentially nothing — their useful filters would be **acausal**, needing to compensate the large group delay around the head (see [[concepts/causality|Causality in ANC]]). This makes the MSE-TD CF the honest criterion for [[concepts/reference-microphone-positioning|Reference Microphone Positioning]].

## Related Concepts

- [[concepts/multiple-coherence-function|Multiple Coherence Function (MCF)]] — the causality-blind upper bound it replaces
- [[concepts/reference-microphone-positioning|Reference Microphone Positioning]] — the application it was designed for
- [[concepts/wiener-filter|Wiener Filter]] — the underlying optimal-filter solution
- [[concepts/filtered-x-mwf|Filtered-x MWF (FxMWF)]] — the frequency-domain MWF on secondary-path-filtered references (hearing-aid NR + ANC)
- [[concepts/causality|Causality in ANC]]
- [[concepts/multi-reference-anc|Multi-Reference ANC]]

## Related Sources

- [[sources/forster-2022-optimal-microphone-positioning|Forster, Fabry & Jax 2022: Optimal Microphone Positioning for Multi-Channel Feedforward ANC Headphones]]
