---
type: concept
created: 2026-05-17
updated: 2026-05-17
tags:
  - active-noise-control
  - distributed-systems
  - wireless-sensor-networks
---

# Distributed ANC

## Overview

**Distributed ANC** refers to ANC systems where multiple acoustic nodes cooperate over a network to cancel noise over a geographic region, as opposed to centralized multi-channel ANC. They are motivated by [[concepts/multi-channel-anc|Multi-channel ANC]] scalability limits and are designed for wireless acoustic sensor network (WASN) applications.

## Why Distributed?

Centralized multi-channel ANC requires all sensor data at a single processor, which is not scalable and requires restructuring hardware for each new configuration. Distributed ANC consumes less energy and communication resources and offers robustness to node failure.

## Collaborative Strategies

### Incremental Strategy (IFxLMS)

Nodes are arranged in a cyclic path. Each node receives the weight vector from its predecessor, updates it with local data, and passes it to the next node:

$$\boldsymbol{w}_k(n) = \boldsymbol{w}_{k-1}(n) + \mu_k \boldsymbol{X}_k(n) e_k(n)$$
$$\boldsymbol{w}(n) = \boldsymbol{w}_K(n)$$

- **Pro**: Lower communication overhead per node
- **Con**: Requires a cyclic path; sensitive to link failure

### Diffusion Strategy (DFxNLMS)

Each node communicates with a subset of neighbors $\mathcal{N}_k$. The update involves an adapt-then-combine step:

$$\boldsymbol{\varphi}_k(n+1) = \boldsymbol{w}_k(n) + \mu_k \frac{\boldsymbol{X}_k(n)}{\|\boldsymbol{X}_k(n)\|^2} e_k(n)$$
$$\boldsymbol{w}_k(n+1) = \sum_{l \in \mathcal{N}_k} a_{l,k} \boldsymbol{\varphi}_l(n+1)$$

where $a_{l,k}$ are combination weights satisfying $a_{l,k}=0$ if $l \notin \mathcal{N}_k$ and $\sum_k a_{l,k}=1$.

- **Pro**: Stable regardless of topology; robust to link failure
- **Con**: Higher communication overhead

### Diffusion FxAP (DFxAP)

Extends diffusion to affine projection updates for faster convergence with correlated inputs.

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/multi-channel-anc|Multi-channel ANC]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]

## Related Sources

- [[sources/lu-2021-survey-active-noise-control-linear|Lu et al. 2021: Survey on ANC — Part I: Linear Systems]]
