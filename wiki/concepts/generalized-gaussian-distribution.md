---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
tags:
- mathematics
- statistics
---

# Generalized Gaussian Distribution

The **Generalized Gaussian Distribution (GGD)** is a flexible family of symmetric probability distributions that includes the normal (Gaussian) and Laplace distributions as special cases.

## Probability Density Function (PDF)

The PDF of a zero-mean GGD is given by:
$$ f(x; \alpha, \beta) = \frac{\alpha}{2 \beta \Gamma(1/\alpha)} \exp\left( - \left( \frac{|x|}{\beta} \right)^\alpha \right) $$
Where:
- **$\alpha > 0$** is the **shape parameter**.
- **$\beta > 0$** is the **scale parameter**.
- **$\Gamma(\cdot)$** is the Gamma function.

## Special Cases

By varying the shape parameter $\alpha$, the GGD can represent different distribution types:
- **$\alpha = 2$**: The **Gaussian distribution**.
- **$\alpha = 1$**: The **Laplace distribution** (heavy-tailed).
- **$\alpha \to \infty$**: Approaches a **Uniform distribution**.
- **$\alpha \to 0$**: Becomes a highly impulsive, degenerate distribution.

## Importance in Robust Signal Processing

The GGD is used in [[robust-adaptive-filtering|Robust Adaptive Filtering]] to model non-Gaussian noise environments (see [[impulsive-noise|Impulsive Noise]]). 
1. **Kernel Function**: In **[[generalized-correntropy|Generalized Correntropy]]**, the GGD serves as the kernel function. By choosing $\alpha$, researchers can tailor the "local similarity" measure to the specific tail-behavior of the noise.
2. **Error Norms**: Minimizing the error under a GGD assumption with parameter $\alpha$ is equivalent to minimizing the **$L_\alpha$ norm** of the error.

## Related Concepts

- [[generalized-correntropy|Generalized Correntropy]]
- [[impulsive-noise|Impulsive Noise]]
- [[robust-adaptive-filtering|Robust Adaptive Filtering]]

## Related Sources

- [[../sources/chen-2016-generalized-correntropy-robust-adaptive-filtering|Chen 2016: Generalized Correntropy for Robust Adaptive Filtering]]
- [[../sources/zhu-2020-robust-gmcc-anc-paper-reading-note|Zhu 2020: Robust GMCC for ANC Paper Reading Note]]
