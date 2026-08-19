---
type: concept
created: 2026-06-04
updated: 2026-08-19
tags:
  - optimization-algorithms
  - blind-source-separation
  - independent-vector-analysis
  - computational-efficiency
---

# Iterative Source Steering

**Iterative Source Steering (ISS)** is a computationally efficient optimization method for [[concepts/independent-vector-analysis|Independent Vector Analysis]] that performs rank-one updates on demixing matrices without requiring matrix inversions.

## Overview

Traditional IVA optimization methods like Iterative Projection (IP) require matrix inversions at each iteration and frequency bin, leading to:
- High computational complexity: $O(M^3)$ per source per frequency bin
- Potential numerical instability
- Slow convergence in practice

ISS addresses these issues by using rank-one updates that:
- Avoid matrix inversions entirely
- Reduce computational complexity to $O(M^2)$
- Maintain numerical stability
- Achieve comparable or better separation performance

## Mathematical Formulation

### Rank-One Update

ISS updates the demixing matrix $\mathbf{W}_f$ using a rank-one modification:

$$\mathbf{W}_f \leftarrow \mathbf{W}_f - \mathbf{v}_{n, f}\mathbf{w}_{n, f}^{\mathsf{H}}$$

where $\mathbf{w}_{n, f}^{\mathsf{H}}$ is the $n$-th row of $\mathbf{W}_f$ and $\mathbf{v}_{n, f}$ is the update vector to be determined.

### Update Vector Optimization

The update vector $\mathbf{v}_{j, n}(f)$ is optimized by minimizing a sub-objective function. For off-diagonal elements ($i \neq n$), closed-form solutions are obtained through complex quadratic minimization.

For the diagonal element $v_{j, nn}(f)$, the solution depends on the spatial regularization term:

$$v_{j, n}(f) = \begin{cases} 1 - \alpha_{j, n}(f)^{-1/2}, & \beta_{j, n}(f) = 0 \\ \gamma_{j, n}(f), & \beta_{j, n}(f) \neq 0 \end{cases}$$

where:

$$\alpha_{j, n}(f) = \sum_t \delta_j(f, t) \frac{|\hat{s}_{j, n}(f, t)|^2}{v_n(f, t)} + 2\lambda_{\text{reg}}\|\mathbf{w}_{j, n}(f)\|^2$$

$$\beta_{j, n}(f) = \lambda_{\text{reg}}\mathbf{w}_{j, n}^{\mathsf{H}}(f)(\mathbf{w}_{j, n}(f) - \mathbf{a}_n(f))$$

### Demixing Matrix Update

Once $v_{j, n}(f)$ is obtained, all rows of the demixing matrix are updated:

$$\mathbf{w}_{j, i}^{\mathsf{H}}(f) \leftarrow \mathbf{w}_{j, i}^{\mathsf{H}}(f) - v_{j, n}(f)\mathbf{w}_{j, n}^{\mathsf{H}}(f)$$

and the separated signals are updated:

$$\mathbf{y}(f, t) \leftarrow \mathbf{y}(f, t) - \mathbf{v}_j(f)y_j(f, t)$$

## Advantages

1. **Computational Efficiency**: 5-7× faster than IP updates (2 ms vs 14 ms per iteration)
2. **Numerical Stability**: No matrix inversions required
3. **Separation Performance**: Comparable or slightly better than IP-based methods
4. **Scalability**: Suitable for real-time applications and limited microphone arrays

## Applications

ISS has been successfully applied to:
- Standard IVA for speech separation
- [[concepts/switching-independent-vector-analysis|Switching IVA]] (SR-SwIVA-ISS)
- Geometrically constrained IVA
- Online source extraction

## Related Concepts

- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/switching-independent-vector-analysis|Switching Independent Vector Analysis]]
- [[concepts/spatial-regularization|Spatial Regularization]]

## Related Sources

- [[sources/dong-2026-spatially-regularized-switching-iva|Dong et al. 2026: Spatially-Regularized Switching IVA with ISS]]
- [[sources/guo-2023-iva-survey|Guo, Luo & Li 2023: IVA Survey]]
