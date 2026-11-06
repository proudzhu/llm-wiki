---
type: concept
created: 2026-11-07
updated: 2026-11-07
tags:
  - convolution
  - efficiency
  - neural-networks
---

# Winograd Convolution

A family of minimal-filtering algorithms that compute convolutions with fewer multiplications by transforming inputs and filters into a domain where the convolution becomes element-wise multiplication. For small kernels (k = 3) and small tiles it reduces the multiply count by a constant factor; the canonical reference is Lavin & Gray (2016), "Fast Algorithms for Convolutional Neural Networks."

## The F(2, 3) Instance

The most common configuration — used by [[sources/kim-2026-faster-enhancer|Kim 2026]] for the k = 3 convolutions in the faster-enhancer.c runtime — tiles the input into 2-output-wide patches and computes each with 4 multiplications instead of the direct 6 (per dimension), a 1.5× multiply reduction in 1-D and 2.25× in 2-D.

## What faster-enhancer.c Shows About It

The faster-enhancer.c ablation is a pointed lesson in where the benefit actually comes from:

- Winograd cuts the multiply footprint **13%** (53.4 → 46.3 MMAC per frame).
- Removing it raises p50 runtime by **30.1%** (0.0692 → 0.0900) — far more than the multiply saving predicts — because the direct path also pays **im2col traffic and a layout change that the transform avoids**.

The takeaway stated in the paper: **multiplies are not the currency**. On CPU, memory layout and data movement frequently dominate arithmetic; a transform whose stated benefit is multiply reduction can be worth much more (or less) than that number alone suggests.

## Trade-Offs

- Numerical accuracy degrades with tile size (larger F(m, m+2) instances accumulate more rounding error), which is why small tiles dominate practice.
- The transformed-domain arithmetic differs bitwise from direct convolution, so Winograd changes outputs — in faster-enhancer.c's ablation table this is why the Winograd ablation is a *speed* measurement, not a quality-neutral substitution.

## Related Concepts

- [[concepts/faster-enhancer-c|faster-enhancer.c]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]] — an orthogonal multiply-reduction strategy

## Related Sources

- [[sources/kim-2026-faster-enhancer|Kim 2026: faster-enhancer.c]]
