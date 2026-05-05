---
type: concept
created: 2026-04-10
updated: 2026-04-10
sources:
- raw/articles/Why Mathematica does not simplify Sinh[ArcCosh[x]].md
tags:
- analysis
- complex-numbers
- mathematics
---

# Complex Analysis

## Overview

**Complex analysis** is the branch of mathematics studying functions of complex variables. It provides the theoretical foundation for understanding [[branch-cuts|Branch Cuts]], [[analytic-continuation|Analytic Continuation]], and why computer algebra systems like Mathematica behave the way they do when simplifying expressions involving inverse functions.

## Key Ideas

### Analytic Functions

A function is **analytic** (holomorphic) at a point if it is complex differentiable in a neighborhood of that point. Analytic functions have remarkable properties:
- They are infinitely differentiable
- They can be represented by power series
- They satisfy the Cauchy-Riemann equations

### Multi-Valued Functions

Many important functions are inherently multi-valued in the complex plane:
- **Square root**: √z has two values for every nonzero z
- **Logarithm**: log(z) = ln|z| + i·arg(z), where arg(z) is defined modulo 2π
- **Inverse trig/hyperbolic functions**: arcsin(z), arccosh(z), etc.

### Branch Cuts

To make multi-valued functions single-valued (and thus analytic), we remove curves from the domain called **branch cuts**. See [[branch-cuts|Branch Cuts]] for details.

### Analytic Continuation

The process of extending a function defined on a small domain to a larger domain while preserving analyticity. This is how functions like arccosh and √z are defined over the entire complex plane (minus branch cuts).

## Relevance to Computation

When a CAS like Mathematica simplifies an expression, it must handle these complex-analytic issues correctly. See [Why Mathematica does not simplify Sinh[ArcCosh[x]]](../sources/why-mathematica-not-simplify-sinh-arccosh.md) for a concrete example where the "simpler" form is only valid on a restricted real domain, while Mathematica's output is correct for all complex inputs.

## Related Concepts

- [[branch-cuts|Branch Cuts]]
- [[analytic-continuation|Analytic Continuation]]
- [[symbolic-computation|Symbolic Computation]]
- [Why Mathematica does not simplify Sinh[ArcCosh[x]]](../sources/why-mathematica-not-simplify-sinh-arccosh.md)

## Related Sources
