---
type: source
created: 2026-10-18
updated: 2026-10-18
sources:
  - raw/papers/wishnick-2014-time-varying-filters-musical/full-text.md
  - https://www.dafx.de/paper-archive/2014/dafx14_aaron_wishnick_time_varying_filters_for_.pdf
  - zotero://select/items/0_PVUD9TVS
tags:
  - audio-effects
  - filter-design
  - digital-filters
  - time-varying-systems
  - virtual-analog
  - listening-test
  - audio-processing
---

# Wishnick 2014: Time-Varying Filters for Musical Applications

| | |
|---|---|
| **Authors** | [[entities/aaron-wishnick|Aaron Wishnick]] |
| **Affiliation** | iZotope, Inc., Cambridge, Massachusetts, USA |
| **Venue** | Proc. 17th Int. Conf. on Digital Audio Effects (DAFx-14), Erlangen, Germany |
| **Year** | 2014 |
| **Type** | Conference paper |
| **Zotero** | [PVUD9TVS](zotero://select/items/0_PVUD9TVS) |
| **Code** | [iZotope/time_varying_filters_paper](https://github.com/iZotope/time_varying_filters_paper) |

## Summary

Wishnick addresses per-sample **time-varying recursive filtering** for musical applications (LFO- or envelope-modulated equalizers, phasers), where requirements differ fundamentally from the speech-coding context that motivated most prior work: real-time per-sample coefficient updates, time-varying stability, artifact-free behavior, arbitrary filter shapes, and sensible intermediate shapes under coefficient interpolation. He proposes the **state variable filter (SVF)** discretized with a transposed Direct-Form II (TDF-II) trapezoidal integrator as the general-purpose solution, proves its time-varying stability for the first time via Laroche's Criterion 2 with a change of basis, and derives closed-form SVF coefficients for the common audio-EQ biquad shapes **and for any arbitrary second-order z-domain transfer function**, making the SVF a universal biquad implementation. Objective (steady-state DC response) and subjective (MUSHRA, 21 subjects) evaluations confirm the SVF's good quality — with ideal DC response, matched only by the explicitly stabilized variants — while showing that transient-minimization methods from the speech-coding literature (output switching) are *unsuitable* for musical applications, where **sideband energy**, not transient variance, correlates with perceived quality.

## Problem Formulation

A filter is time-variant as soon as it exposes a user-controllable parameter. In digital audio effects, parameters may be varied **every sample** (LFO or envelope control of a phaser or EQ), and the implementation must be computationally efficient at that rate, zero-latency, and real-time. The desired properties of a filter structure in this domain are:

1. **Time-varying stability** — bounded-input/bounded-output (BIBO) stability that holds *while coefficients change*, not just at each frozen coefficient set;
2. **Artifact-free time-varying behavior** — no perceptible clicks or distortion on parameter changes;
3. **Efficient per-sample coefficient updates**;
4. **Support for arbitrary filter shapes**;
5. **Sensible intermediate filter shapes** when coefficients are interpolated (magnitude responses should interpolate gracefully between the endpoint shapes).

The study is restricted to **second-order recursive filters**, since higher-order filters are typically decomposed into second-order sections. The choice of filter structure dominates time-varying behavior: structures such as Direct-Form II, lattice, and normalized ladder are *not necessarily stable* under coefficient change, while the coupled form (Gold & Rader) is. Even stable filters can produce objectionable artifacts (Sec. 6).

Prior approaches fall into two categories (see [[concepts/time-varying-filter|time-varying filter]]):

- **Transient minimization** — Zetterberg & Zhang's output-switching realization (1988, needs the entire input signal — not realtime), Välimäki & Laakso's finite-history approximation (1998, realtime but designed for *sparsely* occurring changes — audio-rate modulation would need many parallel filters), and Rabenstein's intermediate-coefficient method (1988, also for widely spaced changes). All target the **output switching model**, whose ideal response for a change from filter $\mathbf{S}_1$ to $\mathbf{S}_2$ at time $m$ is

$$
y[n] = \begin{cases} y_1[n] & : n < m \\ y_2[n] & : n \geq m \end{cases}
$$

- **Stabilization** — Rabenstein & Czarnach's state-vector transformation (1985) forces any structure to stay stable every sample, suitable for audio-rate changes, absorbable into the coefficient matrix (no per-sample filtering cost, but costlier coefficient computation).

## Methodology

### The state variable filter (SVF) and its discretization

The continuous-time SVF in state space form, with resonance parameter $R$ and unity (normalized) center frequency:

$$
\dot{x}_1 = u - 2R x_1 - x_2, \qquad \dot{x}_2 = x_1
\qquad\Longleftrightarrow\qquad
\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}u,\;
\mathbf{A} = \begin{bmatrix} -2R & -1 \\ 1 & 0 \end{bmatrix},\;
\mathbf{B} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}
$$

Taking different output nodes yields the three canonical second-order responses: $\dot{x}_1$ = highpass, $x_1$ = bandpass, $x_2$ = lowpass:

$$
H_{HP}(s) = \frac{s^2}{s^2 + 2Rs + 1}, \quad
H_{BP}(s) = \frac{s}{s^2 + 2Rs + 1}, \quad
H_{LP}(s) = \frac{1}{s^2 + 2Rs + 1}
$$

Applying the bilinear transform directly creates **delay-free loops** — the very problem that led Smith and Dutilleux to declare the bilinear transform unusable for the SVF, and that Härmä et al. solved differently for [[concepts/warped-iir-filter|warped IIR filters]]. The Chamberlin structure (Forward/Backward Euler discretization) avoids this but is unstable for some parameters. Wishnick instead applies the **K-Method** (Yeh; Borin, De Poli & Rocchesso) with a **TDF-II trapezoidal integrator**, the same topology as Zavalishin's "The Art of VA Filter Design". The delay-free loop is resolved by the linear solve

$$
\mathbf{H} = (\mathbf{I} - g\mathbf{A})^{-1}, \qquad
\mathbf{x}_n = g\mathbf{H}\mathbf{B}u_n + \mathbf{H}\mathbf{s}_{n-1}, \qquad
\mathbf{s}_n = \mathbf{s}_{n-1} + 2g\mathbf{A}\mathbf{x}_n + 2g\mathbf{B}u_n
$$

with the prewarping coefficient mapping an analog frequency $\omega_a$ to digital frequency $\omega_c$ at sample period $T$:

$$
g = \frac{\tan(\pi T f_c)}{\omega_a}
$$

Substituting the SVF matrices gives the discrete-time realization (Eq. 8), equivalent to Zavalishin's model where $x_1 = y_{BP}$ and $x_2 = y_{LP}$. An alternate realization computes $\dot{\mathbf{x}}_n$ first (needed for the highpass output), after which the generic TDF-II update depends only on $g$ — convenient for the coefficient-matching derivations below.

### Realizing audio-EQ filter shapes

Any of the common EQ biquad shapes (Bristow-Johnson cookbook: lowpass, bandpass, highpass, peaking, low shelf, high shelf, with $Q$ controlling resonance and $A = 10^{G/40}$ controlling gain in dB) can be written as a linear combination of the three SVF outputs with frequency scaling $k$:

$$
H(s) = c_{HP} H_{HP}(ks) + c_{BP} H_{BP}(ks) + c_{LP} H_{LP}(ks)
$$

Matching the denominator via $R$ and $k$ (then computing $g$ from $k$ by prewarping) and the numerator via the output gains yields **Table 2**:

| Type | $2R$ | $k$ | $c_{HP}$ | $c_{BP}$ | $c_{LP}$ |
|---|---|---|---|---|---|
| Lowpass | $1/Q$ | 1 | 0 | 0 | 1 |
| Bandpass | $1/Q$ | 1 | 0 | 1 | 0 |
| Highpass | $1/Q$ | 1 | 1 | 0 | 0 |
| Peaking | $1/Q$ | 1 | 1 | $A/Q$ | 1 |
| Low shelf | $1/Q$ | $\sqrt{A}$ | 1 | $A/Q$ | $A^2$ |
| High shelf | $1/Q$ | $1/\sqrt{A}$ | $A^2$ | $A/Q$ | 1 |

The output is formed per sample as $y[n] = c_{HP}\dot{x}_1[n] + c_{BP}x_1[n] + c_{LP}x_2[n]$. Notably, Zavalishin reported difficulty producing low/high shelves this way; Table 2 closes that gap.

### Matching any z-domain transfer function

For filter design methods that operate directly in the digital domain (Berchin, Christensen), Wishnick derives the discrete-time SVF transfer functions $H_{HP}(z), H_{BP}(z), H_{LP}(z)$ (all sharing the denominator $1 + g^2 + 2Rg + (2g^2-2)z^{-1} + (1 + g^2 - 2Rg)z^{-2}$) and solves the five-degree-of-freedom match to an arbitrary biquad $H(z) = \frac{b_0 + b_1 z^{-1} + b_2 z^{-2}}{1 + a_1 z^{-1} + a_2 z^{-2}}$:

$$
g = \sqrt{\frac{-1 - a_1 - a_2}{-1 + a_1 - a_2}}, \qquad
R = \frac{a_2 - 1}{\sqrt{-1 - a_1 - a_2}\,\sqrt{-1 + a_1 - a_2}}
$$

$$
c_{HP} = \frac{b_0 - b_1 + b_2}{1 - a_1 + a_2}, \qquad
c_{LP} = \frac{b_0 + b_1 + b_2}{1 + a_1 + a_2}
$$

(with $c_{BP}$ analogous, Eq. 16d). Any digital filter can therefore be designed by any method, decomposed into second-order sections, and realized as SVFs — inheriting the SVF's time-varying stability and artifact-free behavior.

### Proof of time-varying stability

The state transition matrix of the discretized SVF (derived by substituting the state update into itself) is

$$
\mathbf{P} = (\mathbf{I} + 2g\mathbf{A}\mathbf{H}) = \frac{1}{g^2 + 2Rg + 1}
\begin{bmatrix} 1 - g^2 - 2Rg & -2g \\ 2g & 1 - g^2 + 2Rg \end{bmatrix}
$$

Laroche's Criterion 1 ($\|\mathbf{P}\| \leq \gamma < 1$ in the Euclidean norm) fails: $\|\mathbf{P}\| = 1$ for $g, R > 0$. Wishnick instead uses **Criterion 2**, which permits a change of basis $\mathbf{T} = \begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$, $k > 0$, requiring $\|\mathbf{T}\mathbf{P}\mathbf{T}^{-1}\| \leq \gamma < 1$. With the substitutions $\alpha = \frac{\sqrt{16 + 4k^2 + k^4}}{2k}$, $\beta = \frac{4 + k^2}{2k}$ (derivation computer-algebra-assisted, Mathematica 8), the stable region is the union of the inequality families (19a)–(19h), which together contain

$$
0 < g < \alpha + \beta \;\;\land\;\; \frac{k}{2} < R < \beta
$$

Since $\alpha + \beta \to \infty$ and $\beta \to \infty$ as $k \to 0$, for **any** bounded parameter ranges $[g_{min}, g_{max}]$, $[R_{min}, R_{max}]$ one can choose $k > 0$ satisfying $\alpha + \beta > g_{max}$, $\frac{k}{2} < R_{min}$, $\beta > R_{max}$. Hence the TDF-II SVF is time-varying stable over arbitrarily large parameter ranges — the first such proof for this structure (a 2013 attempt by Bencina on the music-dsp list was not completed).

## Experimental Setup

| Item | Detail |
|---|---|
| **Trials** | 5, each with a different filter shape and a single discontinuous parameter change (Table 3: lowpass 80→120 Hz @ Q 6; lowpass 100 Hz @ Q 0.6→4; peaking 80→120 Hz @ Q 6, G 4 dB; peaking 100 Hz @ Q 6, G −4→4 dB; peaking 120 Hz @ Q 0.6→4, G 4 dB) |
| **Structures compared** | DF2 (Direct-Form II), GR (coupled form / Gold–Rader), SVF, SVFR (SVF + Rabenstein transient minimization), SVFRC (SVF + Rabenstein–Czarnach stabilization), TDF2, TDF2RC (TDF-II + Rabenstein–Czarnach), ZZ (Zetterberg–Zhang output switching) |
| **Objective test** | Steady-state DC response: constant DC input, instantaneous parameter change, $\ell_2$ norm of deviation from the output-switching ideal (method suggested by Berners) |
| **Subjective test** | MUSHRA (ITU-R BS.1534-1); 21 experienced subjects (many professional critical listeners), headphones, quiet room; test signal a 100 Hz sinusoid at 48 kHz (minimally masking so artifacts are audible) |
| **Reference / anchor** | Reference: gain envelope smoothed with 10 ms Hann kernel; anchor: unsmoothed gain envelope plus an impulse (3× max filter gain) at the coefficient change |

## Results

### Objective: DC response

The SVF and the Rabenstein–Czarnach-stabilized SVF (SVFRC) are the only structures (besides ZZ, which passes by definition) with **ideal DC response** ($-\infty$ dB error) in all five trials. This is provable: in steady DC state, both $\mathbf{x}_n$ and $\mathbf{s}_n = [0 \; k]^T$ are independent of the filter parameters, so parameter changes cause no switching transients in the state. Rabenstein transient minimization (SVFR) actually *worsens* the SVF's response; DF2, GR, TDF2, and TDF2RC perform acceptably in some trials and poorly in others.

![[raw/papers/wishnick-2014-time-varying-filters-musical/figures/3572ff4f26a00efcb5dbdf8a8516dc576ee9263e6634e0af71cdc50496b0e67f.jpg|Figure 1: SVF vs DF-II DC response]]
*Figure 1: Comparison between lowpass SVF and Direct-Form II steady-state DC response when parameters are changed. At sample 50, parameters change from $g = 0.0458$, $R = 0.4545$ to $g = 0.2679$, $R = 0.1111$. The SVF performs ideally; DF-II exhibits a large transient followed by ripple.*

### Subjective: MUSHRA listening test

The SVF's good audio quality is confirmed. Among time-varying stable structures supporting efficient per-sample updates, the **stabilized TDF-II (TDF2RC) scored best on average**, with the SVF close behind. The output-switching filter (ZZ) consistently scored "bad" to "poor". Rabenstein–Czarnach stabilization is effective (only a small decrease when applied to SVF or TDF-II) — ironically so, since the method derives from the Gold–Rader structure, which itself scored significantly worse.

![[raw/papers/wishnick-2014-time-varying-filters-musical/figures/8f4fe99e130a12e17aeaa757e5195dc5a26c24d0de7727b3727cd31e660522b0.jpg|Figure 3: Average MUSHRA scores]]
*Figure 3: Average MUSHRA scores and 95% confidence intervals for each filter structure over all trials. Time-varying stable structures supporting efficient per-sample coefficient update are in bold.*

Per-trial scores show the choice is a **trade-off**: the SVF outperforms TDF2RC in both lowpass trials and matches it for peaking-frequency changes, but is significantly worse when peaking **resonance or gain** is modulated — consistent with the theory that the zero-setting coefficients $c_{HP}, c_{BP}, c_{LP}$ change instantaneously with gain/resonance (Table 2), and abrupt zero changes cause the audible artifacts, while the transients from **pole** changes are perceptually benign.

### Output switching is the wrong goal for music

An instantaneous parameter change corresponds to an instantaneous amplitude/phase jump; the spectrum around the change point shows high sidebands, audible as a "click". Output switching removes state transients but *emphasizes* the discontinuity itself. Both transient-minimization methods (ZZ, SVFR) achieved their stated goals yet scored "poor" — confirming that the speech-coding objective does not transfer to musical equalization.

![[raw/papers/wishnick-2014-time-varying-filters-musical/figures/58e5eb4b59547b6857f7dca543cbf82f87815cee294119fb8415553d5ea93123.jpg|Figure 2: Sidebands from output switching]]
*Figure 2: Spectrum of a filtered 100 Hz sinusoid during a parameter change with output switching (85 ms Hann window), with pre- and post-change spectra for reference. The high sidebands are audible as an impulsive click.*

### Sideband energy as a quality criterion

Transient-signal variance is essentially **uncorrelated** with MUSHRA scores (Pearson's $r = 0.11$, $p = 0.48$), whereas **sideband energy** (85 ms Hann window centered on the change, energy outside one ERB at 100 Hz) is negatively correlated ($r = -0.59$, $p = 7.02 \times 10^{-5}$). Wishnick proposes minimizing sideband energy, rather than transient variance, as the design objective for musical time-varying filters.

![[raw/papers/wishnick-2014-time-varying-filters-musical/figures/3df00dbdf02531f52a2fe080cefc1bcf079d9749f797dad865fb0ed5cb06939a.jpg|Figure 4: Transient variance vs MUSHRA]]
*Figure 4: Scatter plot of transient signal variance versus MUSHRA score (anchor and reference excluded), showing little correlation ($r = 0.11$, $p = 0.48$).*

![[raw/papers/wishnick-2014-time-varying-filters-musical/figures/3c7a8c95f5dc424990e93e87e0ebcc8b0a2715ff5e16548af496c922c0a504a3.jpg|Figure 5: Sideband energy vs MUSHRA]]
*Figure 5: Scatter plot of sideband energy versus MUSHRA score (anchor and reference excluded), showing correlation ($r = -0.59$, $p = 7.02 \times 10^{-5}$).*

## Key Contributions

1. **Novel stability proof** — first proof of time-varying (BIBO) stability of the TDF-II-discretized state variable filter, via Laroche's Criterion 2 with an explicit change-of-basis matrix covering arbitrarily large parameter ranges.
2. **Universal biquad realization** — closed-form SVF coefficients matching *any* second-order z-domain transfer function (Eqs. 16), so any digital filter design method + SOS decomposition can inherit the SVF's time-varying properties.
3. **Complete EQ cookbook for the SVF** — coefficient tables (Table 2) for lowpass, bandpass, highpass, peaking, low- and high-shelf shapes, closing the shelf-filter gap noted by Zavalishin.
4. **Ideal DC response** — proof and objective verification that the SVF's state is parameter-independent under steady DC, so parameter changes cause no switching transients (only ZZ matches this among the alternatives, and it is not realtime-suitable).
5. **Refutation of output switching for music** — MUSHRA evidence that transient-minimization methods from the speech-coding literature degrade musical quality, and identification of **sideband energy** as a better perceptual criterion (negative correlation with MUSHRA scores), motivating future structure design by sideband minimization.

## Limitations and Caveats

- Evaluation used a **single discontinuous parameter change** per trial, not continuous audio-rate modulation (the actual LFO use case); conclusions about smooth modulation are inferential.
- The listening test used a single stimulus type (100 Hz sinusoid at 48 kHz) chosen to minimize masking — results may differ for broadband musical signals.
- Restricted to **second-order** sections.
- Sideband energy is acknowledged as a "crude psychoacoustic measure"; the correlation does not establish a causal perceptual model.
- The stability proof relies on computer-algebra-assisted derivation (Mathematica 8), with intermediate results omitted from the paper.

## Related Concepts

- [[concepts/state-variable-filter|State Variable Filter]] — the proposed structure
- [[concepts/time-varying-filter|Time-Varying Filter]] — the problem domain and taxonomy of approaches
- [[concepts/state-space-model|State-Space Model]] — the formulation in which the SVF is discretized and its stability proven
- [[concepts/warped-iir-filter|Warped IIR Filter]] — shares the delay-free loop problem, solved there by structure modification rather than the K-Method

## Related Synthesis

- None yet — no existing synthesis page covers time-varying musical filter design.
