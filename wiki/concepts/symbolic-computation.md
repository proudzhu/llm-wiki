---
type: concept
created: 2026-04-10
updated: 2026-04-10
sources:
- raw/articles/Why Mathematica does not simplify Sinh[ArcCosh[x]].md
tags:
- computer-algebra
- mathematics
- simplification
---

# Symbolic Computation

## Overview

**Symbolic computation** (also called computer algebra) is the area of computer science and mathematics concerned with algorithms and software for manipulating mathematical expressions exactly — as opposed to numerical computation, which works with approximate floating-point values.

## Computer Algebra Systems (CAS)

Popular CAS tools include:
- **Mathematica** — Commercial, comprehensive system with powerful symbolic capabilities.
- **Maple** — Commercial, strong in differential equations and visualization.
- **SymPy** — Open-source Python library.
- **Maxima** — Open-source, descended from the original Macsyma.
- **Mathics** — Open-source Mathematica clone.

## Key Challenges

### Simplification and Domain Assumptions

A central challenge in symbolic computation is deciding **when to simplify**. An expression like √(x+1)² = x+1 is only valid for x ≥ −1. A CAS must choose between:
- **Returning a simpler form** — but implicitly assuming a restricted domain.
- **Returning a more complex form** — but being correct for all inputs.

Mathematica generally chooses the latter. See [Why Mathematica does not simplify Sinh[ArcCosh[x]]](../sources/why-mathematica-not-simplify-sinh-arccosh.md) for an example.

### Branch Cuts

Many functions require [[branch-cuts|Branch Cuts]] to be well-defined over the complex plane. A CAS must handle these consistently across all operations.

### Assumption Systems

Most CASs provide mechanisms for the user to declare assumptions (e.g., "x is real and positive") so that simplification can proceed accordingly. In Mathematica: `Simplify[expr, x > -1]`.

## Related Concepts

- [[branch-cuts|Branch Cuts]]
- [[complex-analysis|Complex Analysis]]
- [Why Mathematica does not simplify Sinh[ArcCosh[x]]](../sources/why-mathematica-not-simplify-sinh-arccosh.md)

## Related Sources
