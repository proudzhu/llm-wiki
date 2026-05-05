---
type: concept
created: 2026-04-10
updated: 2026-04-10
sources:
- raw/articles/Why Mathematica does not simplify Sinh[ArcCosh[x]].md
tags:
- complex-analysis
- mathematics
---

# Analytic Continuation

## Overview

**Analytic continuation** is a technique in [[complex-analysis|Complex Analysis]] to extend the domain of an analytic function beyond its original definition, while preserving its analytic properties.

## How It Works

1. Start with a function defined on a small domain (e.g., positive real numbers for √z)
2. Remove a **branch cut** from the complex plane (e.g., (−∞, 0] for √z)
3. Extend the function to the rest of the plane (minus the cut) using the unique analytic extension
4. Define values on the cut by taking limits from one side (convention: from above)

## Example: arccosh(z)

1. Defined for real x > 1 as the positive real number y such that cosh(y) = x
2. Branch cut: (−∞, 1]
3. Extended to the rest of the complex plane by analytic continuation
4. Values on the cut defined by limit from above (positive imaginary direction)

This is why `ArcCosh[-2]` in Mathematica returns a complex number rather than a real number, and why the limit direction matters.

## Example: Square Root

1. Defined for positive reals as expected
2. Branch cut: (−∞, 0]
3. Extended by analytic continuation
4. On the cut: defined by limit from above

This is why √(x+1)² = x+1 is only true for x ≥ −1, not for all x.

## Related Concepts

- [[complex-analysis|Complex Analysis]]
- [[branch-cuts|Branch Cuts]]

## Related Sources
