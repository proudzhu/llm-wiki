---
type: source
created: 2026-10-01
updated: 2026-10-01
sources:
  - raw/papers/cheng-2026-anc-gain-constraint/full-text.txt
  - https://doi.org/10.21437/Interspeech.2026-2202
  - zotero://select/items/0_9JVU9SEU
tags:
  - active-noise-control
  - fixed-filter-anc
  - frequency-response-constraint
  - micro-loudspeaker
  - convex-optimization
---

# Cheng, Zhou, Liu, Zhao & Shi 2026: Active Noise Control With a Gain Constraint for Micro-Loudspeakers

**Authors**: [[entities/zhenhua-cheng|Zhenhua Cheng]], [[entities/yi-zhou|Yi Zhou]], [[entities/yin-liu|Yin Liu]], [[entities/yu-zhao|Yu Zhao]], [[entities/liming-shi|Liming Shi]] (corresponding)
**Affiliation**: School of Communications and Information Engineering, Chongqing University of Posts and Telecommunications, Chongqing, China
**Venue**: Interspeech 2026, Sydney, Australia, pp. 4940–4944
**Type**: Conference paper
**DOI**: 10.21437/Interspeech.2026-2202
**Funding**: National Key R&D Program of China (2024QY2630), NSFC Grant 62301096, Natural Science Foundation of Chongqing (CSTB2023NSCQMSX0659)

## Summary

This paper proposes ANC-FRC, a method for pre-training fixed ANC control filters under a **frequency-response gain constraint**, so that the control signal stays within the limited low-frequency reproduction capability of micro-loudspeakers without adding group delay. An ∞-norm gain limit is imposed on the low-frequency DFT bins of the filter during design; because this hard constraint alone induces a Gibbs phenomenon that degrades noise reduction in the unconstrained band, an ℓ2 regularization term anchors the remaining frequency band to the unconstrained Wiener solution. Real-world anechoic-chamber experiments show ANC-FRC achieves the best practical band-wise NR among gain-limiting schemes, avoiding mechanical over-excursion that would degrade the loudspeaker's service life.

## Problem Formulation

A single-channel feedforward ANC system (reference microphone → control filter $\mathbf{w}$ → secondary loudspeaker → secondary path $s(n)$ → error microphone) has residual

$$e(n) = d(n) + \sum_{l=0}^{L-1} \mathbf{w}^T \mathbf{x}(n-l)\,s(l) = d(n) + \mathbf{w}^T \mathbf{x}'(n),$$

where $\mathbf{x}'(n) = x(n) * s(n)$ is the filtered reference. Minimizing the MSE $J = \mathbb{E}\{e^2(n)\} = \sigma_d^2 + 2\mathbf{w}^T\mathbf{r}_{dx'} + \mathbf{w}^T\mathbf{R}_{x'}\mathbf{w}$ yields the Wiener–Hopf solution

$$\mathbf{w}_{\mathrm{opt}} = -\mathbf{R}_{x'}^{-1}\mathbf{r}_{dx'},$$

which is optimal in the least-squares sense but ignores the output capability of the micro-loudspeaker. Because disturbances typically carry high low-frequency energy (e.g. pink noise) while the micro-loudspeaker's frequency response rolls off at low frequencies (poor reproduction efficiency), the unconstrained filter develops **excessively high low-frequency gain**: the dynamic range is wasted where the loudspeaker cannot physically cancel, and the diaphragm is driven into mechanical over-excursion.

The conventional remedy — cascading a high-pass (or band-stop) filter before/after the control filter — limits low-frequency output power but adds group delay, increasing electronic latency and lowering the NR upper bound; simple clipping produces high-frequency components.

## Methodology

### ANC-LF-FRC: low-frequency gain constraint

Impose an ∞-norm gain limit on the low-frequency bins of the control filter's frequency response at design time:

$$\min_{\mathbf{w}} \;\; \mathbb{E}\{e^2(n)\} \qquad \text{subject to} \quad \|\mathbf{F}_h \mathbf{w}\|_\infty \le \delta_{\mathrm{th}},$$

where $\mathbf{F}_h \in \mathbb{C}^{H \times N}$ is the DFT matrix restricted to bins from DC to $h$, and $\delta_{\mathrm{th}}$ is the gain limit. This bounds the maximum low-frequency gain without any added group delay.

### The Gibbs phenomenon problem

Because the strict frequency-domain constraint forces an abrupt transition at the boundary of the constrained region, a finite-length filter cannot realize the discontinuity and **oscillates in the unconstrained bands** (Gibbs phenomenon), degrading NR there — demonstrated in simulation.

### ANC-FRC: anchored soft constraint on the remaining band

To mitigate the Gibbs oscillations, a soft ℓ2 term pulls the unconstrained-band response toward the (unconstrained) Wiener optimum:

$$\min_{\mathbf{w}} \;\; \mathbb{E}\{e^2(n)\} + \lambda \|\mathbf{F}_{h+1}(\mathbf{w} - \mathbf{w}_{\mathrm{opt}})\|_2^2 \qquad \text{subject to} \quad \|\mathbf{F}_h \mathbf{w}\|_\infty \le \delta_{\mathrm{th}},$$

with $\mathbf{F}_{h+1}$ the DFT matrix for bins from $h+1$ to Nyquist and regularization factor $\lambda > 0$ (set to 0.2). Expanding the MSE term, the objective becomes $\mathbf{w}^T\mathbf{R}_{x'}\mathbf{w} + 2\mathbf{w}^T\mathbf{r}_{dx'} + \lambda\|\mathbf{F}_{h+1}(\mathbf{w}-\mathbf{w}_o)\|_2^2$: the quadratic MSE and the ℓ2 term are convex and the linear inequality constraint defines a convex feasible set, so the problem is a **convex QP with a unique global minimum**, solved with standard convex solvers (CVX).

The gain limit $\delta_{\mathrm{th}}$ is set to 10 dB. The combined formulation guarantees the dynamic range is spent where the micro-loudspeaker is physically capable of cancelling noise.

## Experimental Setup

| Item | Setting |
|:-----|:--------|
| Real-world rig | Anechoic chamber; Brüel & Kjær 4100-D dummy head 0.75 m from a KEF X300A primary loudspeaker; error microphone in the artificial ear, reference microphone on the smartphone; RME sound card, 48 kHz |
| Device under test | Smartphone micro-loudspeaker (low-frequency roll-off response) |
| Proposed methods | ANC-LF-FRC (∞-norm LF gain constraint only); ANC-FRC (constraint + ℓ2 anchor, $\lambda = 0.2$, $\delta_{\mathrm{th}} = 10$ dB) |
| Baselines | ANC-Wiener (unconstrained); ANC-Highpass (first-order Butterworth high-pass, 400 Hz cutoff, cascaded after the control filter) |
| Test noises | White noise (Noisex-92, stationary) and real-world train noise (non-stationary) |
| Simulation | 16 kHz; secondary path $[1, 0]^T$; primary path via MATLAB `fir2` frequency sampling (normalized breakpoints $[0, 0.0375, 0.0625, 0.0875, 0.1625, 0.25, 0.5, 1]^T$, magnitudes $[12, 10, 7, 3, 1, 1, 2, 1]^T$) approximating a micro-speaker response |
| Averaging | Band-wise NR averaged over 10 independent Monte Carlo runs |
| Metric | $NR(f) = 10\log_{10}(S_d(f)/S_e(f))$ (PSD ratio at the error microphone, ANC-off vs. ANC-on) |

## Results

**Average band-wise NR (dB), 10 Monte Carlo runs:**

| Method | Noise | 100–500 Hz | 500–1000 Hz | 1000–2000 Hz |
|:-------|:------|-----------:|------------:|-------------:|
| ANC-Wiener | Train | 4.0756 | 17.7700 | 20.6563 |
| ANC-Wiener | White | 4.0557 | 17.8185 | 21.3636 |
| ANC-Highpass | Train | −1.8496 | 6.0539 | 18.6060 |
| ANC-Highpass | White | −1.8596 | 6.0542 | 19.0473 |
| ANC-LF-FRC | Train | −0.1300 | 11.0092 | 15.6842 |
| ANC-LF-FRC | White | −0.1383 | 11.0322 | 16.0917 |
| **ANC-FRC** | Train | **1.5464** | **13.9615** | **18.5460** |
| **ANC-FRC** | White | **1.5356** | **14.0626** | **19.2252** |

Key findings:

1. **ANC-Wiener is nominally best but physically unusable**: its high low-frequency gain leads to mechanical overdrive of the micro-loudspeaker in practice, degrading NR and the loudspeaker's service life — its superior table numbers are not realizable.
2. **High-pass cascade fails by group delay**: the additional low-frequency group delay causes phase distortion, degrading NR well outside the constrained band (even negative NR at 100–500 Hz).
3. **LF-only constraint fails by the Gibbs phenomenon**: ANC-LF-FRC shows oscillation-induced degradation (slightly negative NR at 100–500 Hz, and 4–5 dB worse than ANC-FRC at 500–2000 Hz).
4. **ANC-FRC is the best practical method**: its control-filter frequency response closely matches the ANC-Wiener response within 400–2000 Hz thanks to the ℓ2 anchor, while remaining within the low-frequency gain limit; results are consistent across both noise types.

## Key Contributions

1. **Design-time frequency-response gain constraint (ANC-LF-FRC)**: instead of constraining the adaptive algorithm online or cascading a filter at runtime, the gain limit is imposed on the low-frequency bins of the *fixed* control filter during pre-training — limiting micro-loudspeaker overload with zero added group delay.
2. **Gibbs-mitigated formulation (ANC-FRC)**: an ℓ2 soft constraint anchoring the unconstrained band to the unconstrained Wiener solution, combined with the hard ∞-norm gain limit into a single convex QP (unique global minimum, CVX-solvable) — preventing the transition-band oscillations that the LF-only hard constraint induces.
3. **Empirical characterization of two failure modes**: quantitative demonstration that (i) a high-pass cascade trades loudspeaker protection for group-delay-induced phase distortion, and (ii) a hard constraint on only one band trades overload protection for Gibbs-oscillation NR loss — and that the combined hard + soft formulation avoids both.

## Limitations and Caveats

- Single-channel feedforward architecture; multichannel/feedback cases not treated.
- The gain limit $\delta_{\mathrm{th}}$ (10 dB) and regularization factor $\lambda$ (0.2) are fixed rather than derived from the loudspeaker's excursion limits.
- Mechanical over-excursion is argued via the filter's low-frequency gain and the loudspeaker response, not measured directly (no excursion or distortion measurements reported).
- NR evaluated at one error position with two noise types; no evaluation of the loudspeaker's service-life impact.

## Related Concepts

- [[concepts/frequency-response-constrained-anc|Frequency-Response Constrained ANC (ANC-FRC)]]
- [[concepts/mechanical-over-excursion|Mechanical Over-Excursion]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]]
- [[concepts/output-constraint-anc-algorithms|Output Constraint ANC Algorithms]]
- [[concepts/constrained-fdlms|Constrained FDLMS]]
- [[concepts/output-saturation-effect|Output Saturation Effect]]
- [[concepts/soft-constrained-anc|Soft-Constrained ANC]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/quadratic-programming|Quadratic Programming]]

## Related Synthesis

*(none yet)*
