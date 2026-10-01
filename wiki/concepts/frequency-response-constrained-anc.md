---
type: concept
created: 2026-10-01
updated: 2026-10-01
sources:
  - raw/papers/cheng-2026-anc-gain-constraint/full-text.txt
tags:
  - active-noise-control
  - fixed-filter-anc
  - constrained-optimization
  - micro-loudspeaker
---

# Frequency-Response Constrained ANC (ANC-FRC)

**ANC-FRC** ([[sources/cheng-2026-anc-gain-constraint|Cheng et al. 2026]]) is a method for pre-training **fixed** ANC control filters under a **frequency-response gain constraint**, so that the control signal respects the limited low-frequency reproduction capability of micro-loudspeakers without adding group delay. An ∞-norm gain limit is imposed on the low-frequency DFT bins of the filter during design, and an ℓ2 regularization term anchors the remaining frequency band to the unconstrained Wiener solution to suppress the Gibbs phenomenon that the hard constraint alone induces.

## Motivation

Unconstrained Wiener–Hopf ANC filters develop excessively high gain at low frequencies (where disturbance energy concentrates and the micro-loudspeaker response rolls off), driving the diaphragm into [[concepts/mechanical-over-excursion|mechanical over-excursion]]. The two conventional remedies both fail:

| Remedy | Failure mode |
|:-------|:-------------|
| Cascading a high-pass / band-stop filter at runtime | Added **group delay** increases electronic latency, causing phase distortion and lowering the NR upper bound |
| Clipping the output | Produces high-frequency components |

ANC-FRC instead constrains the filter **at design time**, keeping the runtime signal path delay-free.

## Key Formulations

**ANC-LF-FRC** — hard ∞-norm gain limit on the low-frequency bins only:

$$\min_{\mathbf{w}} \;\; \mathbb{E}\{e^2(n)\} \qquad \text{s.t.} \quad \|\mathbf{F}_h \mathbf{w}\|_\infty \le \delta_{\mathrm{th}},$$

where $\mathbf{F}_h \in \mathbb{C}^{H \times N}$ is the DFT matrix for bins DC to $h$. Because the constraint enforces an abrupt transition at the band boundary that a finite-length filter cannot realize, the response **oscillates in the unconstrained bands** (Gibbs phenomenon), degrading NR there.

**ANC-FRC** — adds a soft ℓ2 term anchoring the free band to the unconstrained Wiener optimum $\mathbf{w}_{\mathrm{opt}} = -\mathbf{R}_{x'}^{-1}\mathbf{r}_{dx'}$:

$$\min_{\mathbf{w}} \;\; \mathbb{E}\{e^2(n)\} + \lambda \|\mathbf{F}_{h+1}(\mathbf{w} - \mathbf{w}_{\mathrm{opt}})\|_2^2 \qquad \text{s.t.} \quad \|\mathbf{F}_h \mathbf{w}\|_\infty \le \delta_{\mathrm{th}},$$

with $\mathbf{F}_{h+1}$ covering bins $h{+}1$ to Nyquist. The MSE term, the ℓ2 term, and the linear inequality constraint are all convex, so the problem is a **convex QP with a unique global minimum**, solvable with standard tools (CVX). Cheng et al. used $\lambda = 0.2$, $\delta_{\mathrm{th}} = 10$ dB.

This is a combined **hard + soft** constrained design: the hard constraint guarantees the loudspeaker gain limit, while the soft term — an instance of the general [[concepts/soft-constrained-anc|soft-constrained ANC]] pattern — keeps the free-band response as close as possible to the unconstrained optimum.

## Empirical Evidence (Cheng et al. 2026)

Anechoic-chamber experiments (smartphone micro-loudspeaker, dummy head, 48 kHz; train and white noise):

- **ANC-Wiener**: nominally best NR, but physically unimplementable — its low-frequency gain overdrives the micro-loudspeaker.
- **ANC-Highpass** (1st-order Butterworth, 400 Hz): negative NR at 100–500 Hz and 4–8 dB worse mid-band NR — group-delay-induced phase distortion.
- **ANC-LF-FRC**: negative NR at 100–500 Hz and 4–5 dB worse than ANC-FRC at 500–2000 Hz — Gibbs oscillations.
- **ANC-FRC**: best practical band-wise NR (e.g. 1.55 / 13.96 / 18.55 dB at 100–500 / 500–1000 / 1000–2000 Hz for train noise), with a control-filter response closely matching the Wiener filter over 400–2000 Hz.

## Relation to Other Constrained ANC Families

ANC-FRC differs from the online constraint families in **when** and **what** is constrained:

| Family | When | Constraint target |
|:-------|:-----|:------------------|
| [[concepts/output-constraint-anc-algorithms\|Output constraint ANC algorithms]] | Online (adaptive) | Output **power/amplitude** (amplifier saturation) |
| [[concepts/constrained-fdlms\|Constrained FDLMS]] | Online (adaptive) | Per-bin magnitude / output power / stability margins, via penalty functions |
| **ANC-FRC** | **Design time (fixed filter)** | Filter **frequency-response gain** (loudspeaker mechanical limit) |

The design-time placement makes it a natural pre-training stage for [[concepts/selective-fixed-filter-anc|fixed-filter ANC]] libraries — every pre-trained filter can be guaranteed load-safe before deployment, with no per-condition online constraint logic.

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/selective-fixed-filter-anc|Selective Fixed-Filter ANC]]
- [[concepts/mechanical-over-excursion|Mechanical Over-Excursion]]
- [[concepts/output-constraint-anc-algorithms|Output Constraint ANC Algorithms]]
- [[concepts/constrained-fdlms|Constrained FDLMS]]
- [[concepts/output-saturation-effect|Output Saturation Effect]]
- [[concepts/soft-constrained-anc|Soft-Constrained ANC]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/quadratic-programming|Quadratic Programming]]

## Related Sources

- [[sources/cheng-2026-anc-gain-constraint|Cheng, Zhou, Liu, Zhao & Shi 2026: Active Noise Control With a Gain Constraint for Micro-Loudspeakers]]
