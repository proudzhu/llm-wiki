---
type: concept
created: 2026-09-19
updated: 2026-09-19
sources:
  - raw/papers/pan-2020-microphone-array-beamforming/full-text.txt
tags:
  - beamforming
  - microphone-arrays
  - frequency-invariance
---

# Frequency-Invariant Beamforming

**Frequency-invariant beamforming** (频不变波束形成) designs a beamformer whose beampattern does not change with frequency — the array's spatial response is the same at every frequency in the operating band. For broadband acoustic signals (speech spans roughly 20 Hz–20 kHz), frequency invariance is what prevents the beamformer from imposing direction-dependent spectral coloration: if the beampattern varies across frequency, different directions receive different spectral weighting, which distorts wideband signals and degrades fidelity in high-fidelity pickup.

## Why It Is Hard

The review by [[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020]] frames frequency invariance as one vertex of a three-axis trade-off triangle — **directivity factor (DF)**, **white noise gain (WNG)**, and **frequency invariance** — that every fixed beamformer navigates:

- Delay-and-sum beamforming has maximal WNG but a strongly frequency-dependent beampattern (nearly omnidirectional at low frequencies).
- Superdirective beamforming has good frequency consistency for small apertures, but classical robustness remedies such as [[concepts/diagonal-loading|diagonal loading]] "seriously degrade the frequency consistency" — WNG is purchased at the price of frequency invariance.
- Joint optimization of frequency consistency, WNG, and DF is possible but yields low directivity and requires extensive trial-and-error tuning.

The review also lists frequency invariance as an open problem: there is (as of 2020) no established measure of frequency invariance nor a complete design theory for "truly" frequency-invariant beamformers.

## Method Families That Achieve It

| Family | Mechanism | Entry point |
|---|---|---|
| [[concepts/differential-microphone-array|Differential microphone arrays]] | Measure the differential sound field (pressure gradients); finite-order spatial differences give order-determined, frequency-independent directivity | Traditional approach; null-constraint designs |
| [[concepts/orthogonal-series-expansion-beamforming|Orthogonal series expansion]] | Approximate a fixed target beampattern via an orthogonal series (Chebyshev, Legendre, Jacobi, spherical harmonics) | Small-aperture, flexible sensor placement |
| [[concepts/kronecker-product-beamforming|Kronecker product beamforming]] | Decompose the filter into subfilters; one designs the pattern, the other is constrained flat (spatial all-pass) to absorb WNG improvement without disturbing the pattern | Cascade/two-stage designs and their generalizations |

A complementary classical approach in the wider array-processing literature (not the focus of Pan et al.'s review) is constant-beamwidth design, e.g., via Farrow-structure wideband beamformers.

## Related Concepts

- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/orthogonal-series-expansion-beamforming|Orthogonal Series Expansion Beamforming]]
- [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]]
- [[concepts/superdirective-beamforming|Superdirective Beamforming]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/fixed-beamformer|Fixed Beamformer]]

## Related Sources

- [[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020: Microphone Array Beamforming Methods for Speech Communication and Interaction]] — review that elevates frequency invariance to one of the field's three unifying performance axes
