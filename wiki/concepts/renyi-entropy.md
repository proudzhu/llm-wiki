---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
tags:
- information-theory
- mathematics
---

# Rényi Entropy

**Rényi Entropy** is a family of functionals for quantifying the uncertainty, diversity, or randomness of a system. It generalizes the Shannon entropy.

## Definition

For a discrete random variable with probability distribution $\{p_1, \dots, p_n\}$, the Rényi entropy of order $q$ (where $q \geq 0$ and $q \neq 1$) is defined as:
$$ H_q(X) = \frac{1}{1-q} \log \left( \sum_{i=1}^n p_i^q \right) $$

## Special Cases

- **$q \to 1$**: Approaches the standard **Shannon Entropy**.
- **$q = 2$**: Known as **Quadratic Entropy**, which is the most widely used in **[[information-theoretic-learning|Information Theoretic Learning]]**.
- **$q \to \infty$**: Known as **Min-entropy**, which is determined by the most likely outcome.

## Role in Signal Processing

Rényi's Quadratic Entropy ($q=2$) is particularly valuable because it can be estimated directly from data samples using **Parzen Windows** (kernels) without first performing explicit density estimation. 

If we have samples $\{x_i\}$, the estimated quadratic entropy is related to the **Information Potential** (the sum of kernel interactions between samples). Minimizing this entropy (Information Theoretic Learning) forces samples to group together, which is equivalent to maximizing the system's certainty.

## Connection to Correntropy

In [[information-theoretic-learning|Information Theoretic Learning]], **[[correntropy|Correntropy]]** can be viewed as a local version of Rényi's quadratic entropy that measures the similarity of two random variables rather than the uncertainty of one.

## Related Concepts

- [[information-theoretic-learning|Information Theoretic Learning]]
- [[correntropy|Correntropy]]
- [[maximum-correntropy-criterion|Maximum Correntropy Criterion]]

## Related Sources

- [[../sources/chen-2016-generalized-correntropy-robust-adaptive-filtering|Chen 2016: Generalized Correntropy for Robust Adaptive Filtering]]
