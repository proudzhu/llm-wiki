---
type: concept
created: 2026-06-19
updated: 2026-06-19
tags:
  - statistical-modeling
  - unsupervised-learning
  - probability
---

# Gaussian Mixture Model (GMM)

A Gaussian Mixture Model (GMM) is a probabilistic model that represents a distribution as a weighted sum of $K$ Gaussian component densities. GMMs are widely used in speech processing for speaker modeling, voice activity detection, and—as in G-MaP-SE—building clean-speech embedding priors.

## Key Formulations

- $$p(e) = \sum_{k=1}^{K} \pi_k \, \mathcal{N}(e; \mu_k, \Sigma_k)$$
- $$\pi_k$ are mixture weights, $\mu_k$ and $\Sigma_k$ are the mean and covariance of each component$
- $Parameters estimated via Expectation-Maximization (EM) algorithm$

## Related Concepts

- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/prior-matching|Prior Matching]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]