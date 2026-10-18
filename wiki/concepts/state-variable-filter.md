---
type: concept
created: 2026-10-18
updated: 2026-10-18
sources:
  - raw/papers/wishnick-2014-time-varying-filters-musical/full-text.md
tags:
  - filter-design
  - digital-filters
  - virtual-analog
  - time-varying-systems
  - audio-processing
---

# State Variable Filter

The **state variable filter (SVF)** is a second-order filter structure whose state variables directly expose lowpass, bandpass, and highpass outputs. Its continuous-time form places the center frequency at unity (normalized); the resonance parameter $R$ (equivalently $Q = 1/(2R)$) controls damping. In musical DSP it is valued for per-sample time-varying modulation (LFO/envelope-controlled EQ, phasers) because it remains stable and largely artifact-free while coefficients change — properties [[sources/wishnick-2014-time-varying-filters-musical|Wishnick 2014]] was first to prove.

## Continuous-Time Form

In [[concepts/state-space-model|state-space]] form (with input $u$):

$$
\dot{x}_1 = u - 2R x_1 - x_2, \qquad \dot{x}_2 = x_1
$$

so that $\mathbf{A} = \begin{bmatrix} -2R & -1 \\ 1 & 0 \end{bmatrix}$, $\mathbf{B} = [1 \; 0]^T$. The three canonical responses are taken from different nodes:

$$
H_{HP}(s) = \frac{s^2}{s^2 + 2Rs + 1}, \quad
H_{BP}(s) = \frac{s}{s^2 + 2Rs + 1}, \quad
H_{LP}(s) = \frac{1}{s^2 + 2Rs + 1}
$$

i.e., $\dot{x}_1$ = highpass, $x_1$ = bandpass, $x_2$ = lowpass. Frequency and resonance map to independent coefficients, giving low computational cost and intuitive interpolation between coefficient sets.

## Discretization: TDF-II Trapezoidal Integrator

Naive application of the bilinear transform to the SVF creates **delay-free loops** (a feedback path with no delay element). Smith and Dutilleux both concluded the bilinear transform was unusable for the SVF for this reason; the Chamberlin structure (Forward/Backward Euler integrators) avoids the loop but is unstable for some parameters. The modern solution — the topology popularized by Zavalishin's *The Art of VA Filter Design* and analyzed by Wishnick — discretizes with a **transposed Direct-Form II (TDF-II) trapezoidal integrator**, using the **K-Method** (Yeh; Borin, De Poli & Rocchesso) to solve the delay-free loop algebraically via a matrix inverse:

$$
\mathbf{H} = (\mathbf{I} - g\mathbf{A})^{-1}, \qquad
\mathbf{x}_n = g\mathbf{H}\mathbf{B}u_n + \mathbf{H}\mathbf{s}_{n-1}, \qquad
\mathbf{s}_n = \mathbf{s}_{n-1} + 2g\mathbf{A}\mathbf{x}_n + 2g\mathbf{B}u_n
$$

The integrator gain $g = \tan(\pi T f_c)/\omega_a$ implements **prewarping**, mapping a chosen analog frequency to its digital counterpart exactly. This is the same delay-free-loop problem solved structurally for [[concepts/warped-iir-filter|warped IIR filters]] by Härmä et al.'s modified structures; the K-Method instead resolves it generically for any state-space system.

## Matching Arbitrary Filter Shapes

A key advantage of the SVF is that **any** second-order transfer function can be realized as a linear combination of its three outputs, with frequency scaling $k$:

$$
H(s) = c_{HP} H_{HP}(ks) + c_{BP} H_{BP}(ks) + c_{LP} H_{LP}(ks)
$$

- **Audio-EQ shapes** (Bristow-Johnson cookbook): lowpass, bandpass, highpass are trivial ($R = 1/(2Q)$, $k=1$); peaking, low- and high-shelf follow by choosing $k = \sqrt{A}$ or $1/\sqrt{A}$ (gain $A = 10^{G/40}$) and setting the output gains, e.g. low shelf uses $(c_{HP}, c_{BP}, c_{LP}) = (1, A/Q, A^2)$. Wishnick's Table 2 closes the shelf-filter gap that Zavalishin had noted.
- **Arbitrary z-domain biquads**: solving the coefficient match against $H(z) = \frac{b_0 + b_1 z^{-1} + b_2 z^{-2}}{1 + a_1 z^{-1} + a_2 z^{-2}}$ yields closed forms, e.g.

$$
g = \sqrt{\tfrac{-1 - a_1 - a_2}{-1 + a_1 - a_2}}, \qquad
R = \tfrac{a_2 - 1}{\sqrt{-1 - a_1 - a_2}\sqrt{-1 + a_1 - a_2}}, \qquad
c_{HP} = \tfrac{b_0 - b_1 + b_2}{1 - a_1 + a_2}, \qquad
c_{LP} = \tfrac{b_0 + b_1 + b_2}{1 + a_1 + a_2}
$$

so any digital filter (designed by any method, decomposed into second-order sections) can be implemented as SVFs and inherit the time-varying behavior.

## Time-Varying Stability

Wishnick proved (via Laroche's Criterion 2 with a change of basis $\mathbf{T}$, $k > 0$) that the TDF-II SVF is time-varying BIBO stable for $g, R$ varying over **arbitrarily large bounded ranges** — see [[concepts/time-varying-filter|time-varying filter]] for the criteria. Additionally, in steady DC state the SVF's state $\mathbf{s}_n = [0 \; k]^T$ is independent of the filter parameters, so parameter changes produce no switching transients — an ideal DC response that competing structures (Direct-Form II, TDF-II, coupled form) do not share.

Empirically (MUSHRA, 21 subjects), the SVF performs well under parameter changes; its residual artifacts trace to abrupt changes in the **zero-setting gains** $c_{HP}, c_{BP}, c_{LP}$ (which jump with peaking-filter gain/resonance), while transients induced by **pole** changes are perceptually benign.

## Related Concepts

- [[concepts/time-varying-filter|Time-Varying Filter]] — the problem domain the SVF solves
- [[concepts/state-space-model|State-Space Model]] — the formulation used for discretization and stability analysis
- [[concepts/warped-iir-filter|Warped IIR Filter]] — related virtual-analog structure sharing the delay-free loop problem

## Related Sources

- [[sources/wishnick-2014-time-varying-filters-musical|Wishnick 2014: Time-Varying Filters for Musical Applications]] — proposes the TDF-II SVF for musical time-varying filtering; proves time-varying stability; derives the biquad-matching formulas
