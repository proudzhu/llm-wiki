---
type: concept
created: 2026-07-07
updated: 2026-07-07
tags:
  - number-theory
  - mathematics
  - algorithms
sources:
  - raw/papers/rath-2026-minimum-delay-block-size/full-text.txt
---

# Greatest Common Divisor (GCD)

The **greatest common divisor** (gcd or GCD) of two integers is the largest positive integer that divides both without leaving a remainder. It is a fundamental concept in elementary number theory and appears unexpectedly in practical engineering problems such as [[concepts/block-size-adaptation|audio block size adaptation]].

## Definition

For integers $a$ and $b$, not both zero, $\gcd(a, b)$ is the unique positive integer $d$ such that:
1. $d$ divides $a$ and $d$ divides $b$
2. Every common divisor of $a$ and $b$ divides $d$

Two numbers are **coprime** (or relatively prime) if $\gcd(a, b) = 1$.

## Key Properties and Theorems

- [[concepts/bezouts-identity|Bézout's identity]]: $\gcd(a, b)$ can be expressed as an integer linear combination of $a$ and $b$: there exist integers $c_1, c_2$ such that
$$\gcd(a, b) = c_1 a + c_2 b$$
- The set of all integer linear combinations of $a$ and $b$ is exactly the set of multiples of $\gcd(a, b)$:
$$\{c_1 a + c_2 b \mid c_1, c_2 \in \mathbb{Z}\} = \{k \cdot \gcd(a, b) \mid k \in \mathbb{Z}\}$$
- $\gcd(a, b) \cdot \text{lcm}(a, b) = |a \cdot b|$, where lcm is the least common multiple

## Computation: Euclidean Algorithm

The GCD can be computed efficiently in $O(\log \min(a, b))$ time using the Euclidean algorithm (known since ~300 BC):
```
function gcd(a, b):
    while b ≠ 0:
        a, b = b, a mod b
    return a
```

The extended Euclidean algorithm additionally finds the Bézout coefficients $c_1, c_2$.

## Application to Audio Block Size Adaptation

[[sources/rath-2026-minimum-delay-block-size|Rath & Geier (2026)]] showed that GCD gives the minimum latency when adapting between block sizes in realtime audio:
$$\Delta = b_\text{plugin} - \gcd(b_\text{host}, b_\text{plugin})$$

This result relies on the property that all differences $m b_\text{host} - n b_\text{plugin}$ (for non-negative $m, n$) are multiples of $\gcd(b_\text{host}, b_\text{plugin})$, and that the GCD itself is achievable as such a difference.

## Related Concepts

- [[concepts/bezouts-identity|Bézout's Identity]]
- [[concepts/block-size-adaptation|Block Size Adaptation / Reblocking]]

## Related Sources

- [[sources/rath-2026-minimum-delay-block-size|Rath & Geier 2026: Minimum Required Delay for Realtime Block Size Adaptation]]
