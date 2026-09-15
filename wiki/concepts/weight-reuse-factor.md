---
type: concept
created: 2026-09-15
updated: 2026-09-15
tags:
  - embedded-dsp
  - computational-efficiency
  - model-deployment
---

# Weight Reuse Factor

The weight reuse factor $\rho = C_{\mathrm{frame}}/W$ (MACs per frame divided by parameter count) measures how many times each weight of a neural network participates in multiply–accumulates per inference frame. Introduced by [[sources/li-2026-realtime-music-separation-dsp|Li et al. 2026]] as part of their embedded-deployment analysis, it explains why parameter count alone cannot predict the per-frame compute cost of a streaming model.

## The Identity and Where It Breaks

For a fully-connected or recurrent layer evaluated once per frame, each weight takes part in exactly one MAC, so $C_{\mathrm{frame}} = W$ identically ($\rho \approx 1$). Convolution over frequency breaks the identity: a kernel is reused at every frequency bin. Consequences:

- $\rho \approx 1$ for the TasNet/X-UMX family (dominated by frame-rate LSTMs and dense layers) — so their published parameter counts *are* per-frame MAC estimates, and a lower bound once their convolutional front ends are added.
- $\rho = 345$ for RT-STT, whose 383 k weights are evaluated across 384 frequency bins every frame.
- Validated on X-UMX: summing its layers gives 31.5 M MAC/frame against 31 M reported parameters.

Because $\rho$ spans two and a half orders of magnitude across architecture families, **no ordering by parameter count can predict per-frame cost or deployability**. At $\rho \approx 1$, being large *is* being expensive per frame.

## Worked Examples

**Example 1 (toy): a dense layer vs. a frequency-axis convolution.** A fully-connected layer mapping $512 \to 512$ features once per frame has $W = 512 \times 512 = 262{,}144$ weights and $C_{\mathrm{frame}} = 262{,}144$ MACs, so $\rho = 1$. A frequency-axis convolution kernel with $9$ weights slid across $F = 384$ STFT bins has $W = 9$ but $C_{\mathrm{frame}} = 9 \times 384 = 3456$ MACs, so $\rho = 384$: every weight is reused at every bin, once per frame. The tiny conv layer is "cheaper" in memory by 4.6 orders of magnitude yet each of its weights works $384\times$ harder per frame.

**Example 2 (RT-STT, computing $\rho$ from a published GMAC/s figure).** RT-STT reports needing $11.39$ GMAC/s at the $23$ ms operating point ($44.1$ kHz, hop $512$ $\Rightarrow$ $f_s/H = 86.1$ frames/s) with $W = 383$ k parameters. First recover per-frame cost from the rate:

$$
C_{\mathrm{frame}} = \frac{11.39 \times 10^9\ \mathrm{MAC/s}}{86.1\ \mathrm{frames/s}} \approx 132.3\ \mathrm{M\ MAC/frame},
$$

then

$$
\rho = \frac{132.3 \times 10^6}{383 \times 10^3} \approx 345 .
$$

The frequency-convolution backbone reuses each of its 383 k weights $\sim 345\times$ per frame — which is also why its 19%-of-L2 memory footprint says nothing about its compute: it needs $5.5\times$ the DSP's measured $2.07$ GMAC/s.

**Example 3 (deployed model of Li et al. 2026).** The deployed separator has $W = 131$ k parameters at $21.9$ M MAC/frame, giving $\rho = 21.9\times10^6 / 131\times10^3 \approx 167$; equivalently, $21.9\ \mathrm{M} \times 86.1\ \mathrm{frames/s} = 1.89$ GMAC/s — exactly the rate in the paper's Table 1. (Sanity-checking the other direction: $1.89 \times 10^9 / 86.1 \approx 21.95$ M MAC/frame.)

**Example 4 (inverse use at $\rho \approx 1$: estimating a baseline's compute from its parameter count).** HS-TasNet-S has $16$ M parameters and, being dominated by frame-rate dense/recurrent layers, $\rho \approx 1$. Its parameter count *is* its per-frame MAC estimate, so the required rate follows without profiling:

$$
R_{\mathrm{req}} = W \times f_s/H = 16\times10^6 \times 86.1 \approx 1.38\ \mathrm{GMAC/s},
$$

matching the $1.38$ GMAC/s entry in the paper's Table 1 — under the $2.07$ GMAC/s budget (it passes compute) yet overrunning the 2 MB L2 by $8.0\times$ (it fails memory).

**Example 5 (validating the identity on a fully specified architecture).** Summing X-UMX's layer-by-layer MACs gives $31.5$ M MAC/frame against its $31$ M reported parameters, i.e. $\rho = 31.5/31 \approx 1.02$ — the $\rho \approx 1$ identity holds to within 2% on a real architecture, which is what licenses using published parameter counts as per-frame MAC estimates for the dense/recurrent family.

## The Two-Constraint Embedded Budget

Li et al. state deployability of a streaming model on a low-power audio DSP as two hardware-independent constraints:

$$
W \cdot b \leq M_{\mathrm{L2}} \quad (\text{weight memory}), \qquad
C_{\mathrm{frame}} \cdot f_s / H \leq R \quad (\text{per-frame compute}),
$$

with $b$ bytes per weight, hop $H$, and $R$ the *measured sustained* MAC rate — not the datasheet peak, which assumes every issue slot retires a useful MAC with no cache miss, carried state, or serialisation (a hand-scheduled float runtime on the target SHARC-FX sustains 26% of peak, and a TFLite-Micro port spent ~90% of its time moving data). The analysis is parameterised by $(M_{\mathrm{L2}}, R)$ so it can be re-run for any target.

Applied to published real-time music separators on a 2 MB / 2.07 GMAC/s budget, the two constraints eliminate *different* systems and are close to anti-correlated across architecture families: memory rules out the 16–51 M parameter TasNet/X-UMX family (8.0–25.5× over L2) while compute rules out RT-STT (11.4 GMAC/s needed, 5.5× available) — HS-TasNet-S meets the frame deadline but overruns L2 by 8.0×; RT-STT is its mirror image. MAC count is necessary but not sufficient: at equal MAC a frequency-axis recurrence vectorises far worse than a time-axis one, so it must be paired with measured time.

## Related Concepts

- [[concepts/music-source-separation|Music Source Separation]]
- [[concepts/tinyml|TinyML]]
- [[concepts/hardware-dataflow-types|Hardware Dataflow Types]]

## Related Sources

- [[sources/li-2026-realtime-music-separation-dsp|Li, Liu, Malsky & Yi 2026: Real-Time Music Source Separation on a Low-Power Audio DSP]]
