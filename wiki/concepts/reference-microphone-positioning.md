---
type: concept
created: 2026-10-31
updated: 2026-10-31
sources:
  - raw/papers/forster-2022-optimal-microphone-positioning/full-text.txt
tags:
  - active-noise-control
  - headphones
  - microphone-positioning
  - multi-channel
---

# Reference Microphone Positioning

**Reference microphone positioning** is the problem of choosing *where* (and *how many*) external reference microphones to place on a feedforward ANC device. While the placement of the internal **error** microphone is well studied (Kuo, Mitra & Gan 2006), literature on reference-microphone placement was sparse until systematic studies appeared: Meng et al. (2020) analyzed three positions in a single-channel system via particle-velocity measurements on the headphone shell, and MCF-based selection algorithms appear in patents (Nielsen 2020; Jensen et al. 2016). Placement matters increasingly as devices add multiple reference microphones to exploit the spatial properties of incoming noise.

## Criteria for Placement

Two families of evaluation criteria exist:

1. **Multiple coherence function (MCF)** — bounds achievable attenuation from measured cross-PSDs, but ignores causality; any position that raises $\eta_{ud}^2$ looks good on paper. See [[concepts/multiple-coherence-function|Multiple Coherence Function (MCF)]].
2. **MSE time-domain cost function (MSE-TD CF)** — [[sources/forster-2022-optimal-microphone-positioning|Forster, Fabry & Jax 2022]]'s causality-aware criterion: a path-based multi-channel Wiener formulation for an approximated diffuse field whose FIR filters are causal, so it scores only *realizable* performance. See [[concepts/mse-td-cost-function|MSE-TD Cost Function]].

## Key Placement Findings (Forster et al. 2022)

From a Bose QC25 equipped with 10 additional MEMS microphones (5 ipsilateral L1–L5, 5 contralateral R1–R5, plus built-ins L0/R0), evaluated by greedy selection over DRIRs measured at 5° azimuth resolution:

- **Ipsilateral shell distribution wins**: ~9 dB of additional active gain over the conventional single-channel system, using the ipsilateral microphones.
- **Contralateral placement is wasted**: contralateral microphones would need **acausal filters** to contribute significantly (their path around the head exceeds the usable causality margin) — the MCF still predicts gains there, the causal criterion correctly does not.
- **Distance diversity**: after the first pick, the causal criterion consistently prefers the *most distant* remaining microphone — low correlation with previous references while staying well-correlated with the error microphone, matching diffuse-field theory.
- **The first microphone** is best placed where correlation with the error microphone is strongest (L2 selected first under both criteria).

## Relation to Error-Microphone Placement and DOA Effects

Placement interacts with the DOA dependency of feedforward ANC: the optimal directional filter depends on the primary path, which varies with direction of arrival ([[concepts/primary-path-variability|Primary Path Variability]]). Multiple well-placed references can be understood as covering the causal spatial directions around the device — the wearable-scale analog of multi-reference road-noise systems (see [[concepts/multi-reference-anc|Multi-Reference ANC]]).

## Related Concepts

- [[concepts/mse-td-cost-function|MSE-TD Cost Function]] — causality-aware placement criterion
- [[concepts/multiple-coherence-function|Multiple Coherence Function (MCF)]] — causality-blind placement criterion
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/multi-reference-anc|Multi-Reference ANC]]
- [[concepts/causality|Causality in ANC]] — the constraint that makes contralateral references useless
- [[concepts/primary-path-variability|Primary Path Variability]]

## Related Sources

- [[sources/forster-2022-optimal-microphone-positioning|Forster, Fabry & Jax 2022: Optimal Microphone Positioning for Multi-Channel Feedforward ANC Headphones]]
