---
type: concept
created: 2026-07-07
updated: 2026-07-07
tags:
  - number-theory
  - mathematics
sources:
  - raw/papers/rath-2026-minimum-delay-block-size/full-text.txt
---

# Bézout's Identity

**Bézout's identity** (also called Bézout's lemma) is a theorem in elementary number theory stating that for any integers $a$ and $b$, there exist integers $c_1$ and $c_2$ such that:

$$c_1 a + c_2 b = \gcd(a, b)$$

where $\gcd(a, b)$ is the [[concepts/greatest-common-divisor|greatest common divisor]] of $a$ and $b$.

## Historical Note

Despite being named after 18th-century mathematician Étienne Bézout, the identity (and the algorithm to compute it) was known much earlier; the Euclidean algorithm for computing GCD dates to around 300 BC, and Bézout coefficients can be found using the extended Euclidean algorithm.

## Corollary: Linear Combinations

An important corollary states that the set of all integer linear combinations of $a$ and $b$ is precisely the set of integer multiples of $\gcd(a, b)$:

$$\{c_1 a + c_2 b \mid c_1, c_2 \in \mathbb{Z}\} = \{k \cdot \gcd(a, b) \mid k \in \mathbb{Z}\}$$

In other words:
1. Every linear combination is a multiple of the GCD
2. Every multiple of the GCD can be expressed as a linear combination

## Extension to Non-Negative Multiples

[[sources/rath-2026-minimum-delay-block-size|Rath & Geier (2026)]] proved a small extension relevant to audio block processing: for positive integers $b_\text{host}$ and $b_\text{plugin}$, the set $S$ of differences of non-negative multiples

$$S = \{m b_\text{host} - n b_\text{plugin} \mid m, n \in \mathbb{N}_0\}$$

contains both $\gcd(b_\text{host}, b_\text{plugin})$ and $-\gcd(b_\text{host}, b_\text{plugin})$. This means the restricted set $S$ (using only non-negative $m, n$) already spans all integer multiples of the GCD, which is the key lemma needed to prove the tightness of the minimum delay formula for [[concepts/block-size-adaptation|block size adaptation]].

## Related Concepts

- [[concepts/greatest-common-divisor|Greatest Common Divisor (GCD)]]
- [[concepts/block-size-adaptation|Block Size Adaptation / Reblocking]]

## Related Sources

- [[sources/rath-2026-minimum-delay-block-size|Rath & Geier 2026: Minimum Required Delay for Realtime Block Size Adaptation]]
