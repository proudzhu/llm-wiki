---
type: concept
created: 2026-10-31
updated: 2026-10-31
sources:
  - raw/papers/forster-2022-optimal-microphone-positioning/full-text.txt
  - raw/papers/zhang-2020-coherence-mcanc-noise-reduction/full-text.txt
tags:
  - active-noise-control
  - multi-channel
  - signal-processing
  - microphone-positioning
---

# Multiple Coherence Function (MCF)

The **Multiple Coherence Function (MCF)** $\eta_{ud}^2$ is the multi-reference generalization of ordinary coherence: the fraction of the error-signal power that is *linearly explainable* by the full set of $J$ reference signals. In feedforward ANC it defines the **theoretical upper bound** of achievable attenuation (Nelson & Elliott, *Active Control of Sound*, 1992) and underlies patented multi-microphone placement algorithms (e.g., Nielsen 2020; Jensen et al. 2016). The MCF bounds a *single* error point; the fully multichannel (multi-reference, multi-source, multi-error) bound — which also isolates the uncontrollable null-space energy — is the [[concepts/anc-nr-potential-decomposition|ANC NR-potential decomposition]] of [[sources/zhang-2020-coherence-mcanc-noise-reduction|Zhang et al. 2020]], where $\sum_z C_{\hat{\mu}_r c_z}$ is exactly the multiple coherence of the projected primary signal on secondary-path eigen channel $r$ with respect to the eigen references.

## Definition

With $\Phi_{uu} \in \mathbb{R}^{J \times J}$ the matrix of cross-PSDs between all reference microphones and $\Phi_{ud} \in \mathbb{R}^{J \times 1}$ the vector of cross-PSDs between each reference and the error microphone, the ratio of filtered to unfiltered error-mic PSD is

$$
\frac{\Phi_{ee}}{\Phi_{dd}} = 1 - \frac{\Phi_{ud}^{H} \Phi_{uu}^{-1} \Phi_{ud}}{\Phi_{dd}} = 1 - \eta_{ud}^2
$$

so attenuation is bounded by $-10\log_{10}(1 - \eta_{ud}^2)$ dB — the $J$-channel version of the familiar single-reference coherence limit $NR_{max}(f) = -10\log_{10}[1 - \gamma^2_{xd}(f)]$.

## Placement Implication

To maximize the MCF, any additional reference microphone should be correlated **as little as possible with all previous reference microphones** but **as much as possible with the error microphone** (Bendat & Piersol 2010) — maximizing new information about the disturbance at the cancellation point.

## Limitation: Causality Blindness

The MCF is derived in the frequency domain and therefore **does not account for system causality** — a practical ANC filter must be causal. In an approximated diffuse field, [[sources/forster-2022-optimal-microphone-positioning|Forster, Fabry & Jax 2022]] show this matters for placement: the MCF projects continued performance gains from contralateral reference microphones on a headphone, but the corresponding filters would be acausal, so under the causality-constrained [[concepts/mse-td-cost-function|MSE-TD cost function]] the same microphones contribute essentially nothing. The MCF remains the correct *bound* (and both criteria coincide for ipsilateral microphones and for the single-channel case), but it overestimates realizable gains where causality binds.

## Related Concepts

- [[concepts/mse-td-cost-function|MSE-TD Cost Function]] — the causality-aware replacement used for positioning
- [[concepts/broad-band-feedforward-anc|Broad-Band Feedforward ANC]] — carries the single-reference version of the coherence bound
- [[concepts/anc-nr-potential-decomposition|ANC NR-Potential Decomposition]] — the multichannel/multi-error generalization: per-eigen-channel multiple coherence plus the secondary-path null-space term
- [[concepts/spatial-coherence|Spatial Coherence]] — the pairwise counterpart in speech-enhancement contexts
- [[concepts/multi-reference-anc|Multi-Reference ANC]]
- [[concepts/causality|Causality in ANC]]

## Related Sources

- [[sources/forster-2022-optimal-microphone-positioning|Forster, Fabry & Jax 2022: Optimal Microphone Positioning for Multi-Channel Feedforward ANC Headphones]] — quantifies the MCF's causality blindness on a 12-microphone headphone
- [[sources/zhang-2020-coherence-mcanc-noise-reduction|Zhang, Murata, Maeno, Samarasinghe, Abhayapala & Mitsufuji 2020: Coherence-Based Performance Analysis on Noise Reduction in Multichannel ANC]] — derives the per-eigen-channel multiple-coherence bound inside the $E_{T1}/E_{T2}/E_{T3}$ residual-energy decomposition, generalizing the MCF bound to multi-error systems
