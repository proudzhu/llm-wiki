---
type: source
created: 2026-04-18
updated: 2026-04-18
url: https://lisyarus.github.io/blog/posts/its-ok-to-compare-floating-points-for-equality.html
author:
- - wiki/entities/lisyarus|lisyarus
sources:
- raw/articles/its-ok-to-compare-floating-points-for-equality.md
tags:
- computer-graphics
- floating-point
- numerical-stability
- software-engineering
---

# It's ok to compare floating points for equality

> **Source**: [lisyarus.github.io](https://lisyarus.github.io/blog/posts/its-ok-to-compare-floating-points-for-equality.html)
> **Author**: [[entities/lisyarus|lisyarus]] (Alexey)

## Summary

This article argues against the widespread "mantra" that floating-point numbers should never be compared for exact equality. The author, a graphics and physics programmer with 15+ years of experience, posits that "epsilon comparisons" (`abs(x - y) < epsilon`) are often a lazy hack that introduces more bugs than it solves. Instead, developers should understand the deterministic nature of [[concepts/ieee-754|IEEE 754]] and use exact equality or structural changes to their algorithms.

## Key Arguments

### 1. Floating-points are Deterministic
Floating-point numbers are not a "black box" of randomness. They follow highly standardized rules. While they are inexact (represent a finite set of real numbers), they are deterministic. Operations like addition are commutative ($a+b = b+a$) even if not always associative.

### 2. The Problems with Epsilons
- **Non-transitivity**: $a \approx b$ and $b \approx c$ does not imply $a \approx c$. This breaks algorithms like sorting and convex hull generation.
- **Cascading Invariants**: Different parts of a system using different epsilons lead to inconsistent data states.
- **Arbitrary Thresholds**: Most epsilons are "guessed" rather than derived from the precision requirements of the underlying math.

### 3. Case Studies for Exact Equality
- **Spherical Linear Interpolation (Slerp)**: Instead of `angle < 1e-4`, checking `dot(a, b) >= 1.f` is sufficient to prevent `NaN` while preserving full precision for all other cases.
- **Vector Length**: Using `if (M == 0.f)` after normalizing by the maximum coordinate component ($M$) preserves the invariant that only the zero vector has zero length.
- **Ray-Box Intersection**: Standard branchless algorithms work correctly with IEEE 754 infinities. Exact comparison and sorting of intersections handle parallel rays without epsilons.
- **Gaussian Elimination**: Using `if (M == 0.f)` to detect singular matrices is often better than an arbitrary epsilon, which might fail on poorly scaled but valid matrices.

### 4. When Epsilons are Appropriate
- **User Input Sanitization**: Filtering out points that are "too close" to be visually distinct (e.g., less than a pixel width).
- **Unit Testing**: Comparing computed results against reference values where small rounding errors are expected and acceptable.

## Technical Insights
- **Precision vs. Zero**: Often, what a programmer wants is to avoid a division by zero or a `NaN`. Exact comparison to `0.0f` or `1.0f` is the correct way to handle these boundary conditions in a conformant environment.
- **Structural Solutions**: In UI/UX (like grid movement), separate the "presentation" (interpolated position) from the "data model" (discrete cell position) to avoid needing any float comparisons at all.

## Related Concepts
- [[concepts/floating-point-comparison|Floating-point Comparison]]
- [[concepts/ieee-754|IEEE 754]]
- [[concepts/numerical-stability|Numerical Stability]]
- [[concepts/active-noise-control|Active Noise Control]] (for algorithm comparisons)

## Related Synthesis
