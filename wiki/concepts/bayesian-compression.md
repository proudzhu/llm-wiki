---
type: concept
created: 2026-08-11
updated: 2026-08-11
sources:
  - raw/papers/le-2026-efficient-nn-tinyml-review/full-text.md
tags:
  - model-compression
  - pruning
  - quantization
  - bayesian-inference
  - sparsity
  - variational-inference
  - efficient-deep-learning
  - tinyml
---

# Bayesian Compression

**Bayesian compression** is a model-compression framework that uses Bayesian inference with sparsity- or low-precision-inducing priors to simultaneously (a) decide which parameters to prune and (b) decide how many bits to use for each remaining parameter. The distinctive contribution of the Lê, Wolinski & Arbel (2026) review is to present Bayesian compression as a *unifying* framework for both [[concepts/model-pruning|pruning]] and [[concepts/quantization-aware-training|quantization]] — two compression methods that prior surveys treated in isolation. The shared mechanism: choose a prior whose density concentrates at zero (or at a small set of quantization levels), perform variational inference to obtain a posterior, then prune or quantize parameters based on posterior mass.

## Sparsity-Inducing Priors for Pruning

Three priors are presented in the review, illustrated in its Figure 7:

### Spike-and-Slab Prior

A mixture between a Dirac at 0 (the "spike") and a continuous density (the "slab"), typically a zero-mean Gaussian:

$$p(x) = p_0 \delta(x) + (1 - p_0)(2\pi\sigma_0^2)^{-1/2} \exp\!\left(-x^2 / (2\sigma_0^2)\right)$$

with $p_0 \in (0,1)$, $\sigma_0 > 0$. "The spike-and-slab prior pushes the parameters toward 0." Introduced by Mitchell (1988) and applied to neural networks by Louizos et al. (2017).

### Horseshoe Prior

Designed to have an infinite density at 0 and Cauchy-like tails, encouraging parameters to be exactly 0 while still allowing extreme values:

$$X_i \mid \lambda_i, \tau \sim \mathcal{N}(0, \lambda_i^2 \tau^2), \quad \lambda_i \sim \mathcal{C}^+(0, a), \quad \tau \sim \mathcal{C}^+(0, b)$$

where $\mathcal{C}^+(0, a)$ is the half-Cauchy distribution with scale $a$. Carvalho et al. (2009); Ghosh et al. (2019).

### Log-Uniform Prior

Derived from dropout (Srivastava et al. 2014) by Gal & Ghahramani (2016) — "designed to be agnostic about the order of magnitude of the parameters." Improper, but made proper by restricting to an interval $[a, b]$:

$$p(x) = (2|x| \log(b/a))^{-1} \mathbf{1}_{[a,b]}(|x|)$$

with $0 < a < b$. "Its density tends to infinity at 0, so small values are encouraged."

![[raw/papers/le-2026-efficient-nn-tinyml-review/figures/0b910d1b2d8861f1321877ef3c3ae8902c0fa4211fa327d6fec63ee2a785cef9.jpg|Figure 7]]

*Figure 7: Prior densities promoting sparsity — spike-and-slab, horseshoe, and proper log-uniform.*

## Posterior Approximation via Variational Inference

Because "it is usually too costly to compute the exact posterior distribution of the parameters of large models such as NNs," Bayesian compression uses variational inference (Graves 2011). The search space of approximate posteriors is itself a design choice:

- **Independent Gaussians** over parameters — mean and variance trained.
- **Spike-and-slab mixtures** (Louizos et al. 2017) — for each parameter $\theta$, the candidate posterior is a mixture between $\delta(0)$ and $\mathcal{N}(\mu, \sigma^2)$ with mixture parameter $g$ (trained). The trained parameters are $g, \mu, \sigma$. "If $g = 0$, then $\theta = 0$, so $\theta$ can be pruned" — the value of $g$ directly controls sparsity.

## Bayesian Quantization

The same variational-inference framework extends to quantization by replacing the "prune vs keep" binary gate with a multi-level gate that selects the bit-width per parameter. Van Baalen et al. (2021) decompose each parameter as a sum of gated residuals:

$$x = z_2(x_2 + z_4(\epsilon_4 + z_8(\epsilon_8 + z_{16}(\epsilon_{16} + z_{32}\epsilon_{32}))))$$

where $x_2$ is the basic 2-bits approximation of $x$, $\epsilon_n$ are the $n$-bits residuals, and the $z_i$ are dependent Bernoulli random variables whose parameters are trained:

- If all $z_i \to 0$, then $x$ can be **pruned**.
- If $z_2 \to 1$ and others $\to 0$, then $x$ is efficiently approximated by its **2-bits** part.
- If all $z_i \to 1$, then $x$ should remain coded on **32 bits**.

"The optimal level of quantization (in a Bayesian sense) is discovered progressively during training and can be heterogeneous across the parameters." The allowed quantization levels span the full range from 32-bit down to pruning — making this a truly unified compression framework.

Yang et al. (2023) further use the full posterior distribution: each parameter's posterior is transformed by the prior CDF, then the mode is quantized with precision depending on its width — "if the mode has a large width, then a few bits are necessary to encode it."

Meng et al. (2020) train binary NNs using the Bayesian learning rule (Khan et al. 2018), enabling uncertainty quantification alongside state-of-the-art results.

## Why Bayesian Compression Matters for TinyML

The review positions Bayesian compression as particularly relevant for TinyML because:

1. **Heterogeneous precision**: MCU-friendly models benefit from per-parameter bit-width decisions, since uniform quantization wastes bits on insensitive weights. The gated-residual approach naturally produces mixed-precision models.
2. **Unified pruning + quantization**: The same variational framework simultaneously prunes and quantizes, eliminating the need to chain two separate compression pipelines that may interact destructively.
3. **Posterior information**: The posterior distribution "encompasses more information than a simple vector of optimal parameters: variance of the parameters, thickness of their tails" — useful for adaptive deployment under uncertainty.
4. **Empirical TinyML success**: Fedorov et al. (2019) used Bayesian structured pruning via variational inference to achieve 80× parameter reduction with 98.64% accuracy on MNIST, yielding a 2.77 kB model using 1.96 kB RAM — well within the Cortex-M0+ 8 kB SRAM envelope.

The main limitation: "it is usually too costly to compute the exact posterior distribution," and variational inference training infrastructure is not yet standard in [[concepts/tinymlops|TinyMLOps]] toolchains.

## Related Concepts

- [[concepts/model-pruning|Model Pruning]] — the pruning-side application of Bayesian compression
- [[concepts/quantization-aware-training|Quantization-Aware Training]] — the quantization-side application
- [[concepts/post-training-quantization|Post-Training Quantization]] — non-Bayesian alternative
- [[concepts/tinyml|TinyML]] — the deployment regime where heterogeneous precision matters most

## Related Sources

- [[sources/le-2026-efficient-nn-tinyml-review|Lê, Wolinski & Arbel 2026: Efficient NNs for TinyML — A Comprehensive Review]] — introduces the unifying Bayesian compression synthesis
