---
type: concept
created: 2026-09-24
updated: 2026-09-24
sources:
  - raw/papers/desena-2012-higher-order-differential/full-text.md
tags:
  - differential-microphone-array
  - beamforming
  - microphone-arrays
  - fixed-beamformer
---

# Complex-Root Differential Array

A **complex-root differential array** is the second-order [[concepts/differential-microphone-array|differential microphone array]] structure proposed by [[sources/desena-2012-higher-order-differential|De Sena, Hacihabiboglu & Cvetkovic 2012]] to implement directivity patterns that are trigonometric polynomials with **complex-conjugate roots** — a class that conventional cascaded differential arrays (products of first-order stages, hence real roots only) cannot realize.

## The Restriction Being Lifted

A conventional $N$-th order differential microphone cascades $N$ first-order stages, each contributing a factor $(1 - \beta_i) + \beta_i \cos\theta$ with real coefficients. The overall pattern is therefore a product of first-order real-root polynomials. Yet optimal patterns from most design criteria — including large regions of the $(\alpha, \lambda)$ [[concepts/sector-directivity-design|sector-based design]] space and psychoacoustically motivated designs — have complex-conjugate roots. Constrained real-root optimization shrinks the design space and yields suboptimal solutions; the alternative (differential-integral arrays, Abhayapala & Gupta 2010) needs $2N+1$ microphones and covers only one octave band.

## Key Formulations

The structure uses **three** omnidirectional microphones at $[0, -d]$, $[0, 0]$, $[0, +d]$. The outer signals are delayed by $\tau$ and combined with a central branch filter $H_0(\omega)$ and correction filter $H_c(\omega)$:

$$
x(t, \omega, \theta) = P_0 e^{j\omega t} H_c(\omega) \left( e^{-jkd\cos\theta} - H_0(\omega) + e^{j(kd\cos\theta - \omega 2\tau)} \right)
$$

Under the second-order Taylor approximation ($|kd| \ll \pi/2$, $|\omega\tau| \ll \pi/2$), choosing

$$
H_0 (\omega) = e^{-j\omega\tau} (2 - \omega^2 \tau^2 + \omega^2 \kappa), \qquad
\kappa = \frac{1 - a_1 - a_2}{a_2} \tau_0^2, \qquad
\tau = -\frac{a_1}{a_2}\frac{\tau_0}{2}, \qquad \tau_0 = d/c
$$

with $H_c(\omega) = 1/\omega^2$ (double integrator) makes the array realize **any** second-order pattern $(1-a_1-a_2) + a_1\cos\theta + a_2\cos^2\theta$ with real coefficients — complex roots included. Since the $\omega^2$ part of $H_0$ cancels against $H_c$, the central branch reduces to a fractional delay, so the structure matches the conventional cascade in filter complexity. Fractional delays are implemented as maximally flat allpass filters (Laakso et al. 1996), with a common delay added when $a_1, a_2$ have the same sign (non-causal negative delay).

## Properties

- **WNG comparable to the conventional structure**: closed-form white noise gains for both structures depend on $(a_1, a_2)$ only through a product with $kd$, and are very similar in their respective (complex-root vs. real-root) regions of the $(a_1, a_2)$ plane. Both degrade as $kd$ shrinks — the familiar differential-array low-frequency noise amplification.
- **Operational bandwidth**: $f_{\min} = \gamma c / 2\pi d$ (WNG bound, $\gamma$ = smallest acceptable $kd$) to $f_{\max} = c/4d$ (Taylor-approximation bound); >2.5 octaves for $\gamma = 0.25$. Wider bands come from interleaving arrays with different spacings and crossover filters, sharing microphones between sub-arrays.
- **Higher orders**: an $N$-th order pattern is built as a cascade of second-order complex blocks (each absorbing a complex-conjugate root pair) and first-order real blocks — e.g., the paper's third-order design example uses two complex blocks + one real block.

## Validation

The paper's third-order example ($\alpha = \pi/2$, $\lambda = 0.5$; roots $1.85 \pm 2.05j$ and $\cos\theta = -0.86$) was simulated and physically built with AKG C 417 capsules; the measured directivity matched the ideal pattern over 5 octaves after merging a 1.27 cm and a 5.08 cm sub-array via crossover filters.

## Related Concepts

- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/sector-directivity-design|Sector-Based Directivity Design]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/frequency-invariant-beamforming|Frequency-Invariant Beamforming]]
- [[concepts/fixed-beamformer|Fixed Beamformer]]

## Related Sources

- [[sources/desena-2012-higher-order-differential|De Sena, Hacihabiboglu & Cvetkovic 2012: On the Design and Implementation of Higher Order Differential Microphones]] — introduces the structure, WNG analysis, and measurements
