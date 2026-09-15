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
