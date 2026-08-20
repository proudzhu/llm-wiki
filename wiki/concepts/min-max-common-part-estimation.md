---
type: concept
created: 2026-08-20
updated: 2026-08-20
sources:
  - raw/papers/schepker-2016-sdp-minmax-acoustic-feedback/full-text.md
tags:
  - acoustic-feedback-cancellation
  - hearing-aids
  - semidefinite-programming
  - min-max-optimization
  - convex-optimization
  - lyapunov-stability
aliases:
  - SDP common part estimation
  - min-max common pole-zero filter estimation
---

# Min-max Common Part Estimation

**Min-max common part estimation** is a convex optimization approach for estimating the common part of acoustic feedback paths in hearing aids, proposed by [[entities/henning-schepker|Schepker]] & [[entities/simon-doclo|Doclo]] (2016). Unlike prior least-squares approaches that minimize the misalignment, this method directly maximizes the [[concepts/maximum-stable-gain|maximum stable gain (MSG)]] by formulating the estimation as a min-max optimization problem solved via semidefinite programming (SDP).

## Core Idea

The MSG is inversely related to the maximum absolute output-error across all frequencies. Instead of minimizing the sum of squared errors (least-squares), the min-max approach minimizes the **worst-case** error:

$$J_{MM}(\mathbf{a}^c, \mathbf{b}^c, \mathbf{b}^v) = \max_{\substack{0 \leq \Omega \leq \pi \\ 1 \leq m \leq M}} |\tilde{E}_m(e^{j\Omega})|^2$$

This directly corresponds to maximizing the overall MSG $\mathcal{M} = \min_m \mathcal{M}_m$.

## SDP Formulation

Using the Steiglitz-McBride iterative method, the non-linear min-max problem is approximated by a weighted equation-error minimax problem, split into two alternating SDP subproblems:

### Step 1: Variable Part Estimation

With the common part fixed, the variable part $\mathbf{b}_i^v$ is estimated via an SDP using the Schur complement to reformulate the quadratic constraint as a linear matrix inequality (LMI):

$$\min_{t, \mathbf{b}_i^v} t \quad \text{s.t.} \quad \begin{bmatrix} t & p_{m,i}^v(\Omega) & r_{m,i}^v(\Omega) \\ p_{m,i}^v(\Omega) & 1 & 0 \\ r_{m,i}^v(\Omega) & 0 & 1 \end{bmatrix} \succeq \mathbf{0} \quad \forall \Omega, m$$

where $p_{m,i}^v(\Omega)$ and $r_{m,i}^v(\Omega)$ are the real and imaginary parts of the pre-filtered equation-error frequency response.

### Step 2: Common Part Estimation with Lyapunov Stability

With the variable part fixed, the common part $\mathbf{a}_i^c, \mathbf{b}_i^c$ is estimated via a similar SDP, but with an additional stability constraint based on **Lyapunov theory** to guarantee all poles of the estimated common filter lie strictly inside the unit circle. The Lyapunov condition $\mathbf{P}_i - (\mathbf{A}_i^c)^T \mathbf{P}_i \mathbf{A}_i^c \succ \mathbf{0}$ is linearized using the previous iteration's Lyapunov matrix $\tilde{\mathbf{P}}_i$ and reformulated via the Schur complement as the LMI:

$$\Gamma_i^{stab} = \begin{bmatrix} \tilde{\mathbf{P}}_i - \tau \mathbf{I} & (\mathbf{A}_i^c)^T \\ \mathbf{A}_i^c & \tilde{\mathbf{P}}_i^{-1} - \tau \mathbf{I} \end{bmatrix} \succeq \mathbf{0}$$

where $\tau$ is a small positive constant controlling the stability margin.

## Key Properties

- **Convexity**: Each alternating subproblem is a convex SDP, solvable with standard tools (e.g., CVX)
- **Stability guarantee**: The Lyapunov constraint ensures the estimated common poles are always stable
- **MSG-optimality**: Directly optimizes the MSG rather than a proxy (misalignment)
- **Trade-off**: Yields larger MSG but larger misalignment compared to least-squares optimization — a favorable trade-off since MSG directly relates to applicable hearing aid gain while misalignment does not

## Performance

- **MSG improvement**: 2–5 dB over LS optimization across all common-part parameter counts $N^c$
- **Robustness**: Common part estimated from free-field measurements generalizes to unseen conditions (telephone, repositioning)
- **Parameter reduction**: Reduces required variable-part parameters for desired MSGs of 25/35/45 dB
- **AFC convergence**: Increases convergence speed by ~40% when integrated with [[concepts/prediction-error-method|PEM]]-based AFC (24 variable parameters + common part vs. 36 without)

## Related Concepts

- [[concepts/common-part-decomposition|Common Part Decomposition]] — the modeling framework this optimization applies to
- [[concepts/adaptive-feedback-cancellation|Adaptive Feedback Cancellation (AFC)]] — the application context
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — the optimization objective
- [[concepts/prediction-error-method|Prediction Error Method]] — used for AFC integration
- [[concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]] — the application domain

## Related Sources

- [[sources/schepker-2016-sdp-minmax-acoustic-feedback|Schepker & Doclo 2016: SDP Min-max Common Part Estimation]] — the paper proposing this approach
