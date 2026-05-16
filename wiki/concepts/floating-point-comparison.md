---
type: concept
created: 2026-04-18
updated: 2026-04-18
tags:
- floating-point
- numerical-stability
- software-engineering
sources: []
---
# Floating-point Comparison

**Floating-point Comparison** refers to the logic used to determine equality or order between floating-point numbers in computer programs. It is a critical aspect of [[numerical-stability|Numerical Stability]].

## The Comparison Dilemma

Traditional mathematical equality ($a = b$) is often problematic with floating-point numbers due to rounding errors during computations. The standard industry advice has long been to use "epsilon comparisons."

### Epsilon Comparison (Approximate Equality)
$$|a - b| < \epsilon$$
Where $\epsilon$ is a small threshold. This approach aims to catch cases where $a$ and $b$ should be equal but differ slightly due to accumulated precision loss.

## Problems with Universal Epsilons

As argued by [[entities/lisyarus|lisyarus]], the widespread and uncritical use of epsilons leads to several failure modes:

1.  **Non-transitivity**: $a \approx b$ and $b \approx c$ does not mean $a \approx c$. This can cause non-deterministic behavior in algorithms that require transitive relations (e.g., sorting, convex hulls).
2.  **Inconsistent Invariants**: When different parts of a large system use different epsilons (or some use none), the resulting logic can become contradictory, making it impossible to debug.
3.  **Hiding Structural Issues**: Epsilon checks often mask poor architectural decisions, such as mixing presentation state with core data models.

## Best Practices

- **Exact Equality for Boundary Checks**: Use `x == 0.0f` or `x == 1.0f` when checking for specific states that should be exactly representable or to avoid division by zero.
- **Normalize by Maximum Component**: When computing vector lengths, divide components by the maximum absolute coordinate to ensure the error stays in a predictable range.
- **Exploit IEEE 754 Determinism**: Understand the deterministic nature of [[ieee-754|IEEE 754]] instead of treating floating-points as random or unpredictable.
- **Surgical Epsilon Usage**: Only use epsilons when the goal is a "good enough" approximation (e.g., unit tests or UI rendering) and the exact value is not critical for algorithmic correctness.

## Related Concepts
- [[ieee-754|IEEE 754]]
- [[numerical-stability|Numerical Stability]]
- [[sources/its-ok-to-compare-floating-points|It's ok to compare floating points for equality]]

## Related Sources

- [[sources/its-ok-to-compare-floating-points|It's ok to compare floating points for equality]]
