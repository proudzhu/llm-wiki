---
type: source
created: 2026-08-08
updated: 2026-08-08
sources:
  - raw/papers/gil-cacho-2009-regularized-adaptive-notch-filters/full-text.md
  - https://ieeexplore.ieee.org/abstract/document/7077829
  - zotero://select/items/0_D4RBAKAU
tags:
  - acoustic-howling
  - notch-filter
  - adaptive-notch-filter
  - howling-detection
  - regularization
  - leaky-lms
  - pa-systems
---

# Gil-Cacho, van Waterschoot, Moonen & Jensen 2009: Regularized Adaptive Notch Filters for Acoustic Howling Suppression

- **Authors**: [[entities/pepe-gil-cacho|Pepe Gil-Cacho]], [[entities/toon-van-waterschoot|Toon van Waterschoot]], [[entities/marc-moonen|Marc Moonen]], [[entities/soren-holdt-jensen|Søren Holdt Jensen]]
- **Affiliations**: Katholieke Universiteit Leuven, ESAT-SCD, Leuven, Belgium (Gil-Cacho, van Waterschoot, Moonen); Aalborg University, Dept. Electronic Systems, Aalborg, Denmark (Jensen)
- **Venue**: Proceedings of the 17th European Signal Processing Conference (EUSIPCO '09), Glasgow, Scotland, August 2009
- **Type**: Conference paper
- **DOI / URL**: https://ieeexplore.ieee.org/abstract/document/7077829
- **Zotero**: [D4RBAKAU](zotero://select/items/0_D4RBAKAU)

## Summary

This paper introduces the **Regularized Adaptive Notch Filter (RANF)** method for [[concepts/notch-filter-based-howling-suppression|notch-filter-based howling suppression (NHS)]] in public address (PA) systems. Three direct-form adaptive notch filters (ANFs) run in parallel, each with a different signed regularization term ($+\lambda$, $0$, $-\lambda$). The sign of the regularization drives the three frequency estimates to diverge away from one another when no howling is present, and to converge to a common value when howling is present. This convergence/divergence pattern is used as a [[concepts/howling-detection|howling detection]] criterion, giving an ANF-based NHS method a detection capability comparable to frame-based FFT methods while preserving the low delay and low complexity of the sample-based ANF approach. The method is an early KU Leuven contribution in the research line that produced the 2010 JAES HD-feature survey and the 2011 *Proc. IEEE* survey of acoustic feedback control (here cited as the 2008 ESAT-SISTA technical report TR 08-13).

## Problem Formulation

Acoustic howling arises from the acoustic feedback path coupling a loudspeaker back to a microphone. With forward-path response $G_{\mathrm{FW}}(f)$ and feedback-path response $G_{\mathrm{FB}}(f)$, the closed-loop response is

$$G_{\mathrm{CL}}(f) = \frac{G_{\mathrm{FW}}(f)}{1 - G_{\mathrm{FB}}(f) G_{\mathrm{FW}}(f)} \tag{1}$$

with loop response $G_{\mathrm{L}}(f) = G_{\mathrm{FB}}(f) G_{\mathrm{FW}}(f)$ (Eq. 2). By the Nyquist stability criterion, the closed loop is unstable if there exists a frequency $f$ such that $|G_{\mathrm{FB}}(f) G_{\mathrm{FW}}(f)| \geq 1$ and $\angle G_{\mathrm{FB}}(f) G_{\mathrm{FW}}(f) = n 2\pi$; excitation at that critical frequency produces a very narrowband / sinusoidal howling component.

![[raw/papers/gil-cacho-2009-regularized-adaptive-notch-filters/figures/eeb16717d69d966ac29cc5afdc250b42ba3f0e42b9bd8054ababfacc6d633e34.jpg|Closed-loop system with one loudspeaker and one microphone]]
*Figure 1: Closed-loop system resulting from acoustic feedback in a scenario with one loudspeaker and one microphone.*

The paper targets PA systems, where [[concepts/notch-filter-based-howling-suppression|NHS]] is preferred over the [[concepts/adaptive-feedback-cancellation|adaptive feedback cancellation (AFC)]] used in hearing aids. NHS performs frequency analysis, howling detection, and howling suppression. Two implementation families exist:

- **Frame-based (FFT) methods** — two-stage (detection then suppression), accurate frequency estimates from long frames but large processing delay and high complexity; good howling detection from power-spectrum amplitude information.
- **ANF-based methods** — one-stage (simultaneous detection and suppression), sample-based so minimum delay and low complexity, and able to track howling frequency sample-by-sample; but historically weak howling detection because no power-spectrum information is available.

![[raw/papers/gil-cacho-2009-regularized-adaptive-notch-filters/figures/010e3e517346e37ef89a2efd4572ba56fb13615a8f262d9b338506b38effd076.jpg|Two-stage FFT-based NHS block scheme]]
*Figure 2: Detection and suppression block scheme in a typical two-stage FFT-based NHS system.*

![[raw/papers/gil-cacho-2009-regularized-adaptive-notch-filters/figures/0abd8550df153acbb19e25d875993603fbbbf0f21b99ba823328971f18495f14.jpg|One-stage ANF-based system]]
*Figure 3: Simultaneous detection and suppression in a one-stage ANF-based system.*

The paper's goal is to combine the ANF's low delay/complexity with an FFT-like detection capability, so that tonal components in the source signal are not affected.

## Methodology

### Second-order IIR notch filter

A second-order IIR notch filter with constrained poles and zeros (Nehorai 1985) is used, with zeros on the unit circle and poles at radius $0 < r < 1$ on the same radial direction:

$$H(z) = \frac{1 - 2 \cos(\omega_0) z^{-1} + z^{-2}}{1 - 2 r \cos(\omega_0) z^{-1} + r^2 z^{-2}} \tag{3}$$

A pole radius close to unity gives a very narrow notch (minimal surrounding distortion) but then requires very accurate frequency estimates, otherwise a signal component near — but not at — the howling frequency is suppressed.

### Direct-form ANF with gradient descent

For coefficient updating the transfer function is rewritten as

$$H(q) = \frac{1 - a(n) q^{-1} + q^{-2}}{1 - a(n) r q^{-1} + r^2 q^{-2}} \tag{4}$$

where the single parameter $a(n) \in (-2, 2)$ defines the instantaneous notch frequency $\omega_0(n) = \arccos(a(n)/2)$ (Eq. 5). The ANF estimates $a(n)$ by minimizing the mean square error of the notch-filter output $y(n)$, $\min_{a(n)} E[y(n)^2]$ (Eq. 6), via a gradient-descent update (Regalia 1995), Eqs. (7)–(11), with step-size $\mu$. A gradient-descent (rather than Gauss-Newton) implementation is chosen for minimal complexity: only $n$ parameters are estimated, where $n$ is the number of sinusoids.

### Regularized ANF (RANF) — the proposed method

The proposed NHS method runs **three RANFs in parallel** sharing one decision block. Each RANF is regularized with a term $\lambda_i$ taking a different value for $i = 1, 2, 3$. The regularized cost function is

$$\min_{a_i(n)} E[y_i(n)^2] + \lambda_i a_i(n)^2, \quad i = 1, 2, 3 \tag{12}$$

which yields a modified gradient-descent update equivalent to a **Leaky LMS** update (Mayyas & Aboulnasr 1997):

$$a_i(n+1) = a_i(n) - \mu \left\{ y_i(n) \nabla_{a_i}(n) + \lambda_i a_i(n) \right\} \tag{13}$$

The key idea is that the regularization term is **negligible when howling is present** (the gradient term $y_i(n)\nabla_{a_i}(n)$ dominates), but **dominates when howling is absent** (the gradient tends to zero). In the no-howling regime the update reduces to $a_i(n+1) \approx (1 - \mu \lambda_i) a_i(n)$, so the sign of $\lambda_i$ determines whether the coefficient estimate is *leaked towards zero* (positive $\lambda_i$) or *accumulated towards its bound* (negative $\lambda_i$).

The three RANFs are set with **signed regularization** $\lambda_1 = +\lambda$, $\lambda_2 = 0$, $\lambda_3 = -\lambda$. Therefore:

- **Howling present** — all three coefficients converge to the same value (the gradient term dominates in all three).
- **Howling absent** — the three coefficients diverge away from each other ($a_1 \to 0$, $a_3 \to$ bound, $a_2$ neutral).

![[raw/papers/gil-cacho-2009-regularized-adaptive-notch-filters/figures/8d963a9b576411f91ebf3de3ccd5a0b08beb92d820be3f553883d947d671f897.jpg|RANF frequency tracking over time showing convergence during howling and divergence otherwise]]
*Figure 4: Combined representation of the time-domain RANF input $x(n)$ (lower curve) and the three RANF normalized frequency estimates $f_i/f_s$ ($i=1,2,3$, upper curves). Framed signal fragments correspond to howling segments, during which the three estimates converge to a common frequency.*

This convergence behaviour is the [[concepts/howling-detection|howling detection]] mechanism — it does not rely on power-spectrum information, unlike frame-based methods, and so it does not confuse a desired tonal source component with howling (a held tonal source does not drive three independently-regularized estimates to a common frequency the way a loop-sustained howling tone does).

### Decision rule and parameter choice

The decision block monitors the three coefficient sequences $a_i(n)$. After buffering $L$ samples (a small number for minimum decision delay; e.g. $L = 5$ samples = 0.312 ms at 16 kHz), the mean and variance over the block are computed for each RANF. If the difference between two mean values (in Hz) is below a fixed threshold, howling is declared present; the output $y(n)$ is then taken as the RANF output with the smallest variance (the most reliable estimate). If all pairwise mean differences exceed the threshold, no howling is assumed and the output passes the input through directly.

The regularization magnitude $\lambda$ is chosen so that, over a period of $M$ samples, two coefficients diverge by a prescribed frequency threshold $\Delta f$ (in Hz). Under the small-angle approximation ($\Delta f \ll f_s$):

$$\lambda = \frac{1}{\mu} \left[ \sqrt[2M]{1 + \left(\frac{2\pi}{f_s} \Delta f\right)^2} - 1 \right] \tag{14}$$

![[raw/papers/gil-cacho-2009-regularized-adaptive-notch-filters/figures/9b7f8ea825d92256236bb39124fbcdc5bf4d17e9e2392be2dff39455fdea5744.jpg|RANF-based NHS block diagram]]
*Figure 5: Block diagram of the proposed RANF-based NHS method. The input $x(n)$ feeds three parallel RANFs; the decision block compares their coefficient estimates and selects the output or passes the input through.*

## Experimental Setup

| Item | Value |
|------|-------|
| Source signals | Clean speech (English female voice) and music (song fragment), 16 kHz |
| Feedback path | Synthetic — exponentially damped tone at a particular frequency; frequency and duration drawn from pre-defined distributions to simulate a dynamic feedback path |
| Forward gain | Adjusted per signal to reach a pre-specified loop gain |
| Scenarios | 'a' and 'b' — differ in howling frequency range, max loop gain, howling onset speed, exponential slope of howling amplitude, howling duration, and howling occurrence rate |
| Test signals | $\mathrm{Speech}_a$, $\mathrm{Speech}_b$, $\mathrm{Music}_a$, $\mathrm{Music}_b$ |
| $\lambda_1, \lambda_2, \lambda_3$ | $+0.0001$, $0$, $-0.0001$ |
| Step-size $\mu$ | $0.023$ |
| Pole radius $r$ | $0.85$ |
| Decision threshold | $5$ Hz |
| Block length $L$ | $5$ samples ($0.312$ ms at 16 kHz) |
| Metrics | $\mathrm{Att}_{\max}$, $\mathrm{Att}_{\min}$ (dB) — max/min attenuation around howling frequency; $\mathrm{SD}_{\max}$, $\mathrm{SD}_{\mathrm{mean}}$ — frequency-weighted log-spectral signal distortion (ERB weighting per ANSI S3.5-1997) |

The attenuation compares the post-suppression and original (howling-free) short-term power spectra around the howling frequency (Eq. 15); $\mathrm{Att}_{\max} \approx 0$ dB means distortion-free suppression. The signal distortion (Eq. 16, proposed in van Waterschoot & Moonen 2008) measures overall sound-quality degradation from both the notch filtering and the residual howling, weighted over auditory critical bands:

$$\mathrm{SD}(t) = \sqrt{\int_0^{f_s/2} w_{\mathrm{ERB}}(f) \left(10 \log_{10} \frac{S_y(f)}{S_x(f)}\right)^2 df} \tag{16}$$

## Results

Figure 6 shows spectrograms of the speech signal before and after suppression. For scenario 'a' (panels a→b) suppression is performed well across time and frequency. For scenario 'b' (panels c→d) suppression fails in the frequency range below 1.5 kHz.

![[raw/papers/gil-cacho-2009-regularized-adaptive-notch-filters/figures/03f6f28dca496f9b1184f01cc6d8bd9329fdd4ef6e404a346108ca685b5313a9.jpg|(a) Speech_a before suppression]]

![[raw/papers/gil-cacho-2009-regularized-adaptive-notch-filters/figures/f42ea0c93289b11fdbde66331434a570c34027c4347f6919d6eaf137494f33b9.jpg|(b) Speech_a after suppression]]

![[raw/papers/gil-cacho-2009-regularized-adaptive-notch-filters/figures/a9b91fb6af40e2c35f6e73c2f57161c25ce9acd4b4515470dde3ec9d1aa895d6.jpg|(c) Speech_b before suppression]]

![[raw/papers/gil-cacho-2009-regularized-adaptive-notch-filters/figures/ead73b093b41726eff621f3a9bd8dcd4477bdfee030daa2357af4f908bb2db43.jpg|(d) Speech_b after suppression]]
*Figure 6: Speech signal before and after howling suppression. Scenarios 'a' and 'b' differ in howling frequency range, gain, and time evolution. Suppression succeeds across time/frequency in (b) but fails below 1.5 kHz in (d).*

The music signal (Figure 7 in the paper) shows the same behaviour as speech. The quantitative results are:

| Signal | $\mathrm{SD}_{\mathrm{mean}}$ | $\mathrm{SD}_{\max}$ | $\mathrm{Att}_{\max}$ (dB) | $\mathrm{Att}_{\min}$ (dB) |
|--------|------|------|------|------|
| $\mathrm{Speech}_a$ | 1.66 | 14.78 | 5 | 6 |
| $\mathrm{Speech}_b$ | 4.32 | 28.83 | 5 | 40 |
| $\mathrm{Music}_a$ | 1.05 | 13.24 | 3 | 6 |
| $\mathrm{Music}_b$ | 3.61 | 17.83 | 1 | 40 |

Scenario 'b' is more problematic on every measure. The failure below 1.5 kHz is attributed to a known limitation of **direct-form ANFs**, which are not necessarily stable when the notch frequency approaches its extreme values ($0$ and $f_s/2$) (Regalia 1995). When the signal contains howling near these frequencies the proposed method cannot suppress it and additionally distorts a wider band through false howling detection. Lattice ANF implementations would address the stability issue but, as noted in the paper, their performance is acceptable only when tracking sinusoids immersed in white noise — not in coloured inputs such as speech or music.

## Key Contributions

1. **Signed-regularization detection mechanism.** Introduces the [[concepts/regularized-adaptive-notch-filter|RANF]]: three parallel direct-form ANFs regularized with $+\lambda$, $0$, $-\lambda$, so that coefficient convergence (howling present) vs. divergence (howling absent) becomes a detection criterion that does not rely on power-spectrum information.
2. **Bridging the ANF vs. FFT trade-off.** Combines the minimum processing delay and low computational complexity of sample-based ANFs with an howling-detection capability comparable to frame-based FFT methods, so that desired tonal source components are not suppressed.
3. **Closed-form regularization-to-divergence mapping.** Derives (Eq. 14, small-angle approximation) the regularization magnitude $\lambda$ that yields a prescribed coefficient-divergence rate $\Delta f$ over $M$ samples, linking the detection threshold directly to a tunable frequency separation.
4. **Leaky LMS connection.** Identifies the regularized update (Eq. 13) as a Leaky LMS update, and shows that the sign of the leakage coefficient produces either a leakage (towards zero) or an accumulation (towards the bound) effect on the coefficient estimate — the signed-regularization trick that powers the detection mechanism.
5. **Documented limitation of direct-form RANF.** Empirically shows the method fails for howling near 0 and $f_s/2$ (below 1.5 kHz in scenario 'b'), tracing it to direct-form ANF instability at frequency extremes and noting that lattice ANFs are not a satisfactory fix for coloured (speech/music) inputs.

## Related Concepts

- [[concepts/regularized-adaptive-notch-filter|Regularized Adaptive Notch Filter (RANF)]] — the proposed method (this paper introduces it)
- [[concepts/notch-filter-based-howling-suppression|Notch-Filter-Based Howling Suppression (NHS)]] — the broader solution family; this paper is an ANF-based (one-stage) variant
- [[concepts/howling-detection|Howling Detection]] — RANF coefficient convergence is a detection mechanism distinct from the spectral-feature and trial-and-verify paradigms
- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — broader AHS context
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the closed-loop instability the method addresses
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — NHS effectively raises the operable gain above the passive MSG

## Related Synthesis

_(None — the paper is a single-method NHS contribution; the ANC-focused synthesis pages do not gain a new comparison axis from it.)_
