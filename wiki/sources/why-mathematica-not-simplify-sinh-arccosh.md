---
type: source
created: 2026-04-10
updated: 2026-04-10
sources:
- raw/articles/Why Mathematica does not simplify Sinh[ArcCosh[x]].md
tags:
- branch-cuts
- complex-analysis
- mathematica
- symbolic-computation
aliases:
- Why Mathematica does not simplify Sinh[ArcCosh[x]]
---

# Why Mathematica does not simplify Sinh[ArcCosh[x]]

**Original Source**: [John D. Cook Blog](https://www.johndcook.com/blog/2026/03/10/sinh-arccosh/)
**Author**: [[../entities/john-d-cook|John D. Cook]]
**Published**: 2026-03-10

## Summary

An exploration of why Mathematica returns seemingly unintuitive results when simplifying hyperbolic functions applied to inverse hyperbolic functions — specifically `Sinh[ArcCosh[x]]`. The answer reveals that Mathematica's output is **more correct**, not less: it handles complex inputs properly via careful branch cut definitions, while the "simpler" form √(x² − 1) is only valid for restricted domains.

## Key Takeaways

1. **Mathematica's behavior is sophisticated, not ignorant**: When `Sinh[ArcCosh[x]]` returns `√((x-1)/(x+1)) · (x+1)` instead of `√(x²-1)`, it's because the returned expression is correct for **all complex inputs**, not just real x ≥ 1.

2. **Branch cuts matter**: 
   - `ArcCosh` has a branch cut along (−∞, 1]. Values on the cut are defined by taking the limit from **above** (positive imaginary direction).
   - For example, `ArcCosh[-2]` does not return a simple real value — the behavior depends on which side of the branch cut you approach from.

3. **Square root also has a branch cut**: √(x+1)² = x+1 is only true when x ≥ −1. For smaller x, this assumption breaks down. Mathematica's expression correctly handles all cases.

4. **Making assumptions explicit**: If you only care about x ≥ −1, you can tell Mathematica this via `Simplify` with assumptions, and it will return the simpler form √(x² − 1).

5. **General lesson**: When a CAS "fails" to simplify something, it may be being **more rigorous** than you expect — preserving correctness across a broader domain rather than assuming your specific use case.

## Hyperbolic Composition Table

The expected identities (valid for real x where all functions are real-valued):

| | sinh⁻¹ | cosh⁻¹ | tanh⁻¹ |
|---|---|---|---|
| **sinh** | x | √(x²−1) | x/√(1−x²) |
| **cosh** | √(x²+1) | x | 1/√(1−x²) |
| **tanh** | x/√(x²+1) | √(x²−1)/x | x |

Mathematica reproduces most of these, **except** when applying sinh or cosh to arccosh — where it returns more general complex-safe expressions.

## Related Concepts

- [[../concepts/branch-cuts|Branch Cuts]] — How CASs define functions via branch cuts and analytic continuation
- [[../concepts/symbolic-computation|Symbolic Computation]] — How computer algebra systems handle simplification with implicit domain assumptions
- [[../concepts/complex-analysis|Complex Analysis]] — The mathematical foundation underlying these behaviors

## Related Entities

- [[../entities/john-d-cook|John D. Cook]] — Author, mathematician and blogger

## Related Synthesis
