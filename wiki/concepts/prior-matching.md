---
type: concept
created: 2026-06-19
updated: 2026-06-19
tags:
  - speech-enhancement
  - representation-learning
---

# Prior Matching

Prior matching is a technique that refines a noisy or corrupted representation by matching it against a clean prior distribution learned from clean data. In G-MaP-SE, the prior is a GMM fit to clean-speech speaker embeddings; at inference, a noisy embedding is matched to this prior via soft cosine-similarity weighting over GMM components to produce a cleaner conditioning embedding.

## Key Formulations

- $Clean prior: $P = \{\mu_k\}_{k=1}^K$ from GMM means$
- $Soft assignment: $\gamma_k = \frac{\exp(\tilde{e}^{\top} \tilde{\mu}_k / \tau)}{\sum_j \exp(\tilde{e}^{\top} \tilde{\mu}_j / \tau)}$$
- $Matched prior: $e_{\text{prior}} = \sum_{k=1}^K \gamma_k \mu_k$$

## Related Concepts

- [[concepts/gaussian-mixture-model|Gaussian Mixture Model (GMM)]]
- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]