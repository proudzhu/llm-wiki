---
type: concept
created: 2026-04-10
updated: 2026-04-10
sources:
- raw/articles/Why Mathematica does not simplify Sinh[ArcCosh[x]].md
tags:
- cas
- complex-analysis
- mathematics
---

# Branch Cuts

## Overview

A **branch cut** is a curve (usually a line or ray) in the complex plane across which a multi-valued function is discontinuous. It is used to define a single-valued branch of a function that would otherwise be multi-valued.

## Why Branch Cuts Are Needed

Many functions in complex analysis are inherently multi-valued. For example:
- **Square root**: √z has two values for every nonzero z (e.g., √4 = 2 or −2).
- **Logarithm**: log(z) = ln|z| + i·arg(z), and arg(z) is defined only up to multiples of 2π.
- **Inverse functions**: arccosh(z), arcsin(z), etc., have multiple values because their forward functions (cosh, sin) are not injective.

To make these functions single-valued (and thus analytic), we remove a curve from the domain — the **branch cut** — and define the function on the remaining domain by choosing a specific branch.

## How Branch Cuts Work

1. **Define the function** on a region where it is single-valued and well-behaved (e.g., positive reals for √z).
2. **Remove a branch cut** (e.g., (−∞, 0] for √z, (−∞, 1] for arccosh).
3. **Extend by analytic continuation** to the rest of the plane minus the cut.
4. **Define values on the cut** by taking limits from one side (convention: from above / positive imaginary direction).

## Examples in Computer Algebra Systems

| Function | Branch Cut | Convention |
|----------|-----------|------------|
| √z | (−∞, 0] | Limit from above |
| arccosh(z) | (−∞, 1] | Limit from above |
| log(z) | (−∞, 0] | Principal branch, arg(z) ∈ (−π, π] |

## Why This Matters

When a CAS like Mathematica simplifies an expression, it must preserve correctness across the **entire complex domain**, not just the real axis. An apparently "simpler" form may only be valid on a restricted domain. Mathematica's choice of output reflects its commitment to correctness everywhere (except on the branch cut itself, where limits are carefully defined).

See [Why Mathematica does not simplify Sinh[ArcCosh[x]]](../sources/why-mathematica-not-simplify-sinh-arccosh.md) for a concrete example.

## Related Concepts

- [[complex-analysis|Complex Analysis]]
- [[symbolic-computation|Symbolic Computation]]
- [[analytic-continuation|Analytic Continuation]]

## Related Sources
