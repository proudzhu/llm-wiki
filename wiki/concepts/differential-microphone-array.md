---
type: concept
created: 2026-05-13
updated: 2026-09-24
sources:
  - raw/papers/pan-2020-microphone-array-beamforming/full-text.txt
  - raw/papers/tashev-2008-sound-capture-spatial-filter/full-text.md
  - raw/papers/wechsler-2024-neural-directional-filtering/full-text.md
  - raw/papers/zhu-2025-kronecker-superdirective-beamforming/full-text.txt
  - raw/papers/cohen-2019-differential-kronecker-beamforming/full-text.txt
  - raw/papers/desena-2012-higher-order-differential/full-text.md
tags:
  - differential-microphone-array
  - beamforming
  - spatial-audio
---

# Differential Microphone Array

A differential microphone array (DMA) is a fixed beamformer that uses spatial differences between closely-spaced microphones to achieve directional sensitivity. DMAs can produce frequency-invariant directivity patterns.

## Types

| Type | Description |
|------|-------------|
| LDMA | Linear DMA - microphones arranged in a line |
| CDMA | Circular DMA - microphones arranged in a circle |

## Key Properties

- **Frequency invariance**: Directivity pattern remains constant across frequency
- **Order limitation**: Maximum order is limited by number of microphones
- **White noise gain**: Low WNG at low frequencies leads to noise amplification

## Kronecker Product Differential Beamforming

[[sources/cohen-2019-differential-kronecker-beamforming|Cohen, Benesty & Chen 2019]] introduced **differential Kronecker product beamformers**: when the physical array decomposes into two virtual ULAs ($M = M_1 M_2$, steering vector $\mathbf{d} = \mathbf{d}_1 \otimes \mathbf{d}_2$), the differential filter follows the same decomposition $\mathbf{h} = \mathbf{h}_1 \otimes \mathbf{h}_2$. This adds a new design axis to classical differential beamforming: the KP cardioid/dipole/hypercardioid/supercardioid achieve higher DF and WNG than the traditional designs with $M_2$ microphones, and occupy a more favorable DF–WNG tradeoff than minimum-norm designs with the same total $M$ — see [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]].

## Null-Constraint Design and Robustness

[[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020]] survey the design space beyond the traditional multistage cascade (an $N$th-order DMA as the difference of two $(N{-}1)$th-order DMAs, $N{+}1$ pressure microphones, fixed structure):

- **Null-constraint design** (Benesty & Chen): write the desired beampattern's null positions plus a distortionless constraint as a linear system $\mathbf{C}^T(\omega)\mathbf{h}(\omega) = \mathbf{g}_1$; solving it yields classical patterns (dipole, cardioid, hypercardioid, supercardioid, Chebyshev) without pre-specifying a target pattern. With $M > N{+}1$ microphones, the remaining degrees of freedom **maximize WNG** — so adding microphones directly attacks the white-noise amplification bottleneck (the $N$th-order minimum null position has a lower bound).
- **Multistage-cascade theory**: the cascade is equivalent to linear-constraint DMAs; adjacent stages can merge; the overall beampattern is the product of stage beampatterns; a robust DMA decomposes into a differential stage plus a robustness stage. Excess sensors introduce high-frequency extra nulls, so the differential order must be constrained to preserve frequency invariance.
- **Beyond integer order and linear geometry**: fractional-order DMAs (order computed from a target DF or WNG threshold); circular DMAs via Jacobi-series beampattern approximation; concentric circular arrays for high-frequency frequency invariance and robustness; planar and time-domain generalizations.
- **Steering limitation**: linear DMAs are end-fire by construction; steering off end-fire can yield negative gain, motivating circular/spherical geometries.

## Complex-Root Patterns and Sector-Based Design (De Sena et al. 2012)

[[sources/desena-2012-higher-order-differential|De Sena, Hacihabiboglu & Cvetkovic 2012]] identify a structural restriction of the conventional cascade: since each first-order stage contributes a real-root factor $(1-\beta_i) + \beta_i\cos\theta$, cascaded DMAs can only realize trigonometric polynomials with **real** roots — yet optimal patterns for most design criteria (including their [[concepts/sector-directivity-design|sector-based (α, λ) design framework]], which unifies omni/subcardioid/cardioid/hypercardioid/supercardioid as special cases) have complex-conjugate roots. Their [[concepts/complex-root-differential-array|complex-root differential array]] lifts the restriction with three omnidirectional microphones and a central branch filter, matching the conventional structure in filter complexity and WNG. The same paper derives the operational band $[\gamma c/2\pi d,\ c/4d]$ (WNG lower bound / Taylor-approximation upper bound) and shows how multi-spacing sub-arrays with crossover filters extend it — e.g., a measured third-order pattern over 5 octaves.

## Limitations

- Restricted to low-order patterns with compact arrays
- Cannot achieve higher-order directivity with limited microphones
- Performance degrades due to noise amplification at low frequencies

## Back-to-Back Unidirectional Variant

A distinct but related geometry is the [[concepts/back-to-back-microphone-array|back-to-back microphone array]] introduced by Tashev et al. (2008). The two variants differ in capsule type and primary cue:

| Property | Differential MA | Back-to-Back Array |
|---|---|---|
| Capsule type | Omnidirectional | Unidirectional (e.g. subcardioid) |
| Primary spatial cue | Pressure difference (delay) between omni mics | Directional response level difference |
| Beamformer target | Frequency-invariant directivity | Maximum front-back energy ratio |
| Sub-baseline reliability | Degrades at very small spacing (noise amplification) | Robust at very small spacing (e.g. 9.6 mm at 16 kHz) |

For very small baselines where delay-based features become unreliable (Tashev et al.'s optimizer effectively disabled both delay features at 9.6 mm / 16 kHz, where the inter-mic delay is only ~1/4 of the sampling period), the back-to-back geometry's reliance on the intrinsic directional response of each capsule becomes advantageous.

## Related Concepts

- [[concepts/fixed-beamformer|Fixed Beamformer]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]
- [[concepts/back-to-back-microphone-array|Back-to-Back Microphone Array]] — a related small-baseline geometry that uses unidirectional capsules (rather than omni) and front-back level differences
- [[concepts/frequency-invariant-beamforming|Frequency-Invariant Beamforming]] — the design goal DMAs achieve by measuring the differential field
- [[concepts/orthogonal-series-expansion-beamforming|Orthogonal Series Expansion Beamforming]] — beampattern-approximation design family closely related to null-constraint DMA design
- [[concepts/sector-directivity-design|Sector-Based Directivity Design]] — (α, λ) framework whose optimal patterns frequently require complex roots
- [[concepts/complex-root-differential-array|Complex-Root Differential Array]] — three-mic second-order structure realizing complex-root patterns

## Related Sources

- [[sources/cohen-2019-differential-kronecker-beamforming|Cohen, Benesty & Chen 2019: Differential Kronecker Product Beamforming]] — Kronecker-decomposed differential beamformers (KP cardioid/dipole/hypercardioid/supercardioid)
- [[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020: Microphone Array Beamforming Methods for Speech Communication and Interaction]] — survey of DMA design space: null-constraint and max-WNG designs, multistage-cascade theory, fractional orders, circular/concentric geometries, steering limits
- [[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024: Neural Directional Filtering]] — neural directional filtering surpasses the order-per-microphone limit: a 3rd-order DMA pattern (6-mic CDMA classically) realized with 4 microphones
- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
- [[sources/tashev-2008-sound-capture-spatial-filter|Tashev et al. 2008: Sound Capture System and Spatial Filter for Small Devices]] — back-to-back unidirectional variant (9.6 mm baseline)
- [[sources/desena-2012-higher-order-differential|De Sena, Hacihabiboglu & Cvetkovic 2012: On the Design and Implementation of Higher Order Differential Microphones]] — (α, λ) design framework unifying standard patterns; complex-root array structure; WNG/bandwidth analysis
