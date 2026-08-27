---
type: concept
created: 2026-08-27
updated: 2026-08-27
sources:
  - raw/papers/rafaely-2000-constrained-fdlms/full-text.md
  - raw/papers/guldenschuh-2014-secondary-path-irregularities/full-text.md
tags:
  - adaptive-filtering
  - frequency-domain
  - constrained-optimization
  - penalty-function
---

# Constrained FDLMS

**Constrained FDLMS** is a modification of the frequency-domain LMS algorithm, introduced by [[entities/boaz-rafaely|Rafaely]] and [[entities/stephen-j-elliott|Elliott]] (2000), that incorporates **convex frequency-domain constraints** on the adaptive filter — such as per-frequency magnitude limits, output-power limits, or robust-stability margins — via a **penalty-function formulation** and steepest-descent search. It converges to the constrained minimum at only a modest computational increase over conventional FDLMS, making it suitable for real-time DSP implementation.

## Base Algorithm

The underlying FDLMS uses time-domain filtering with frequency-domain adaptation (the delayless configuration of Morgan & Thi 1995), avoiding the one-block filtering delay of full frequency-domain implementations:

$$
\mathbf{w}_{m+1} = \mathbf{w}_m + \mu \cdot \mathrm{IFFT}\{X^*(k)\,E(k)\}_{+}
$$

with FFT size $2N$ for block size $N$, and $\{\cdot\}_{+}$ selecting the causal part (causality gradient constraint).

## Penalty-Function Formulation

Constraints $c_i(\mathbf{w}) < 0$ (assumed convex in $\mathbf{w}$) are folded into the cost function with a one-sided quadratic penalty weighted by $\sigma$:

$$
J = E[\mathbf{e}^T(n)\mathbf{e}(n)] + \sigma \sum_{i=1}^{I} \left\{\max[c_i(\mathbf{w}), 0]\right\}^2
$$

The penalized cost remains convex, so steepest descent finds its unique global minimum. The penalty gradient uses the sign-based operator $[c_i]_z = c_i\,(\mathrm{sign}(c_i)+1)/2$ (zero when the constraint holds, $c_i$ when violated) — cheap enough for real-time DSP:

$$
\mathbf{w}_{m+1} = \mathbf{w}_m + \mu \left(\mathrm{IFFT}\{X^*E\}_{+} + 2\sigma \sum_i [c_i]_z \frac{\partial c_i}{\partial \mathbf{w}}\right)
$$

## Supported Constraints

| Constraint | Form | Use case |
|:-----------|:-----|:---------|
| Magnitude limit | $c_k = \vert W(k)\vert^2 - L(k) < 0$ | Prevent excess amplification (e.g. room equalization gain limits) |
| Output power limit | $\frac{1}{N}\sum_k \vert X W \vert^2 < p$ | Actuator overload protection |
| Robust stability | $c_k = \vert W G B \vert^2 - 1 < 0$ | Stability of adaptive feedback controllers under plant uncertainty (IMC configuration) |

Each constraint's gradient term is expressible as an IFFT, so the update stays in the frequency domain at $O(N \log N)$ cost.

## Key Property: Frequency-Selective Penalty

Unlike the **leaky LMS**, whose leak factor $\gamma$ penalizes filter gain at *all* frequencies (and must be tuned by trial and error), the penalty-function constraint affects **only the frequencies violating the bound**. In the paper's sound-equalization study, both methods limited the filter to ≈4 dB, but the constrained FDLMS preserved equalization elsewhere while the leaky FDLMS degraded it across the whole spectrum.

## Historical Significance

Constrained FDLMS is the frequency-domain antecedent of the later time-domain [[concepts/output-constraint-anc-algorithms|output constraint ANC algorithm]] family: it was arguably the first to formulate adaptive-filter output/gain constraints as an online penalty-function optimization rather than a fixed leak, and it influenced subsequent work on gain-limited frequency-domain adaptive filters (e.g. Kozacky & Ogunfunmi 2009).

## Cost Benchmark

[[sources/guldenschuh-2014-secondary-path-irregularities|Guldenschuh & de Callafon 2014]] benchmark the constrained FDLMS (12-tap $W$, 2×24-pt FFTs + IFFT) against their own [[concepts/dc-gain-stability-constraint|DC-gain stability constraint]] on ANC headphones:

| | Constrained FDLMS | DC-gain constraint |
|:--|:--|:--|
| Cost per update | ≥ 661 MACs | 6 MACs |
| Narrowband noise reduction | **2–5 dB better** (close to 12-tap MMSE) | ~12.5% below MMSE |
| Broadband noise reduction | comparable | comparable |

The result illustrates the frequency-selective advantage of penalty-function constraints — better narrowband performance at two orders of magnitude higher computational cost.

## Related Concepts

- [[concepts/output-constraint-anc-algorithms|Output Constraint ANC Algorithms]] — time-domain descendants addressing output saturation
- [[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]] — the simpler global-penalty alternative
- [[concepts/robust-stability-constraint|Robust Stability Constraint]] — one of the supported constraint types
- [[concepts/internal-model-control|Internal Model Control]] — feedback configuration for the robust-stability constraint
- [[concepts/multidelay-block-frequency-domain-adaptive-filter|Multidelay Block Frequency-Domain Adaptive Filter]] — related block frequency-domain adaptation family
- [[concepts/active-noise-control|Active Noise Control]]

## Related Sources

- [[sources/rafaely-2000-constrained-fdlms|Rafaely & Elliott 2000: Computationally Efficient Frequency-Domain LMS with Constraints]]
