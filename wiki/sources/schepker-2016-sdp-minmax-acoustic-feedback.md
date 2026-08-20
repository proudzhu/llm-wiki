---
type: source
created: 2026-08-20
updated: 2026-08-20
sources:
  - raw/papers/schepker-2016-sdp-minmax-acoustic-feedback/full-text.md
  - https://doi.org/10.1109/TASLP.2015.2507940
  - zotero://select/items/0_ADNDYTV8
tags:
  - acoustic-feedback-cancellation
  - hearing-aids
  - semidefinite-programming
  - min-max-optimization
  - common-part-decomposition
  - maximum-stable-gain
  - lyapunov-stability
---

# Schepker & Doclo 2016: SDP Approach to Min-max Estimation of Common Part of Acoustic Feedback Paths

**Authors**: [[entities/henning-schepker|Henning Schepker]], [[entities/simon-doclo|Simon Doclo]]
**Institution**: University of Oldenburg, Department of Medical Physics and Acoustics, Germany
**Venue**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 24, no. 2, pp. 246–257, Feb. 2016
**Type**: Journal article
**DOI**: [10.1109/TASLP.2015.2507940](https://doi.org/10.1109/TASLP.2015.2507940)
**Zotero**: [ADNDYTV8](zotero://select/items/0_ADNDYTV8)

## Summary

This paper proposes a novel optimization approach for estimating the common part of acoustic feedback paths in hearing aids by directly maximizing the [[concepts/maximum-stable-gain|maximum stable gain (MSG)]] rather than minimizing the misalignment via least-squares. The min-max optimization problem is formulated as a semidefinite program (SDP) with a Lyapunov theory-based stability constraint, yielding 2–5 dB MSG improvement over the existing least-squares approach while enabling faster AFC convergence and reduced variable-part parameter counts.

## Problem Formulation

Consider a single-input-multiple-output (SIMO) system with $M$ acoustic transfer functions (ATFs) $H_m(z)$, each modeled as a causal all-zero filter of order $N_z^h$:

$$H_m(z) = \sum_{j=0}^{N_z^h} h_m[j] z^{-j}, \quad m = 1, \ldots, M$$

To reduce the number of adaptive parameters, each ATF is approximated by a [[concepts/common-part-decomposition|common part decomposition]] — the convolution of a time-invariant common part $\hat{H}^c(z)$ (pole-zero filter with $N_p^c$ poles and $N_z^c$ zeros) and a time-varying variable part $\hat{H}_m^v(z)$ (all-zero filter with $N_z^v$ zeros):

$$\hat{H}_m(z) = \frac{B^c(z)}{A^c(z)} B_m^v(z)$$

The output-error (frequency-domain difference between true and estimated ATFs) is:

$$\tilde{E}_m(e^{j\Omega}) = H_m(e^{j\Omega}) - \frac{B^c(e^{j\Omega})}{A^c(e^{j\Omega})} B_m^v(e^{j\Omega})$$

![[raw/papers/schepker-2016-sdp-minmax-acoustic-feedback/figures/0b94c312c8139c86ad679a1760658a5369818a3b6344a9604097b518949a5637.jpg|System models: (a) general SIMO system and (b) approximation using common part decomposition]]
*Figure 1: System models — (a) general SIMO system and (b) approximation using a common part.*

The two key performance measures are the **normalized misalignment** $\epsilon_m$ (measuring filter estimation accuracy) and the **MSG** $\mathcal{M}_m$ (measuring maximum applicable gain before instability):

$$\mathcal{M}_m = 10 \log_{10} \frac{1}{\max_{0 \leq \Omega \leq \pi} |\tilde{E}_m(e^{j\Omega})|^2}$$

## Methodology

### Existing LS Optimization

Existing approaches minimize the least-squares (LS) cost function (overall misalignment) using the iterative Steiglitz-McBride method, alternating between common-part and variable-part estimation via weighted least-squares. While this yields good misalignment, the MSG may remain limited.

### Proposed Min-max Optimization

Instead of minimizing misalignment, the paper proposes to directly maximize the MSG by minimizing the **maximum** absolute output-error across all frequencies and IRs:

$$J_{MM}(\mathbf{a}^c, \mathbf{b}^c, \mathbf{b}^v) = \max_{\substack{0 \leq \Omega \leq \pi \\ 1 \leq m \leq M}} |\tilde{E}_m(e^{j\Omega})|^2$$

Using the Steiglitz-McBride iteration, the non-linear cost is approximated by a weighted equation-error min-max problem, which is split into two alternating SDP subproblems:

**Step 1 — Variable part estimation**: With the common part fixed from the previous iteration, the variable part $\mathbf{b}_i^v$ is estimated by minimizing the maximum weighted equation-error. Using the Schur complement, this is reformulated as an SDP with linear matrix inequality (LMI) constraints:

$$\min_{t, \mathbf{b}_i^v} t \quad \text{subject to} \quad \begin{bmatrix} t & p_{m,i}^v(\Omega) & r_{m,i}^v(\Omega) \\ p_{m,i}^v(\Omega) & 1 & 0 \\ r_{m,i}^v(\Omega) & 0 & 1 \end{bmatrix} \succeq \mathbf{0} \quad \forall \Omega, m$$

**Step 2 — Common part estimation**: With the variable part fixed, the common part $\mathbf{a}_i^c, \mathbf{b}_i^c$ is estimated by a similar SDP, but with an additional **Lyapunov stability constraint** $\Gamma_i^{stab} \succeq \mathbf{0}$ to guarantee that the estimated common poles lie strictly inside the unit circle. The stability constraint is derived from Lyapunov theory: a pole-zero filter is stable iff there exists $\mathbf{P}_i \succ \mathbf{0}$ such that $\mathbf{P}_i - (\mathbf{A}_i^c)^T \mathbf{P}_i \mathbf{A}_i^c \succ \mathbf{0}$. Using the Schur complement, this is reformulated as the LMI:

$$\Gamma_i^{stab} = \begin{bmatrix} \tilde{\mathbf{P}}_i - \tau \mathbf{I} & (\mathbf{A}_i^c)^T \\ \mathbf{A}_i^c & \tilde{\mathbf{P}}_i^{-1} - \tau \mathbf{I} \end{bmatrix} \succeq \mathbf{0}$$

where $\tilde{\mathbf{P}}_i$ solves the Lyapunov equation from the previous iteration's canonical matrix, and $\tau$ controls the stability margin. The SDPs are solved using CVX (Matlab).

![[raw/papers/schepker-2016-sdp-minmax-acoustic-feedback/figures/b0771184f7ffd8ac953275453c30d1fafda33d86e4bf87c817e6297b252ea93b.jpg|AFC frameworks using (a) static feedback canceller and (b) adaptive feedback canceller with common part decomposition]]
*Figure 2: Acoustic feedback cancellation frameworks — (a) static feedback canceller and (b) adaptive feedback canceller using the proposed feedback path decomposition.*

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Hearing aid | Two-microphone behind-the-ear (BTE), open-fitting ear molds (vent size 2 mm) |
| Measurement | Dummy head with adjustable ear canals |
| Sampling rate | $f_s = 16$ kHz |
| IR truncation order | $N_z^h = 99$ |
| Feedback paths | 8 total: $m=1,2$ free-field (used for optimization), $m=3,4$ telephone <1 cm, $m=5,6$ repositioned, $m=7,8$ telephone ~24 cm |
| Common part parameters | $N_p^c, N_z^c \in \{0, 4, 8, \ldots, 24\}$; $N^c = N_p^c + N_z^c$ |
| Variable part parameters | $N_z^v \in \{0, \ldots, 36\}$ |
| Frequency discretization | $K = 2048$ |
| Stability margin | $\tau = 10^{-6}$ |
| Convergence criterion | $\delta = 10^{-4}$ |
| Initialization | LS optimization solution |
| AFC simulation | PEM-based, NLMS ($\mu = 0.002$), prediction filter order 20, $|G| = 10^{15/20}$, $d_G = 96$ (6 ms) |
| Speech signal | 80 s, multiple male/female speakers |
| Quality metric | PESQ |

## Results

### MSG Improvement

The proposed min-max optimization outperforms LS optimization in terms of overall MSG by **2–5 dB** across all values of $N^c$, with the improvement being largest for small $N^c$ and decreasing as $N^c$ grows. For exemplary parameters ($N_p^c = 8, N_z^c = 4, N_z^v = 12$), the min-max approach achieves 45.4 dB MSG vs. 42.2 dB / 44.7 dB for LS.

![[raw/papers/schepker-2016-sdp-minmax-acoustic-feedback/figures/a6205b6fcf96e5e90647f93fce61c3b526eaa574338449d9417024057419bc52.jpg|MSG of min-max optimization as a function of variable part parameters and common part parameters]]
*Figure 5: MSG of the proposed min-max optimization approach as a function of $N_z^v$ and $N^c$.*

![[raw/papers/schepker-2016-sdp-minmax-acoustic-feedback/figures/c822bd7f11504177b094e6b5b437e1cf4882e0a73b7e5732f7f5ac5d667d90ee.jpg|Average overall MSG comparison of LS and min-max approaches for N^c = 8]]
*Figure 7: Average overall MSG of the LS and proposed min-max optimization approaches for $N^c = 8$. Error bars indicate min/max.*

### Misalignment Trade-off

The LS optimization approach (which minimizes misalignment) outperforms the min-max approach in terms of overall misalignment by 1–4 dB. This is the expected trade-off: the min-max approach sacrifices misalignment performance to directly maximize MSG. However, MSG is directly related to the applicable hearing aid gain, whereas misalignment is not.

### Robustness to Unknown Feedback Paths

The common part estimated from free-field IRs ($m=1,2$) generalizes to unseen feedback paths ($m=3$–$8$), including telephone-receiver and repositioning conditions. Even for these unknown paths, including the common part increases MSG and reduces the required variable part parameters for desired MSGs of 25, 35, and 45 dB.

### Perceptual Quality (PESQ)

At the same broadband gain (MSG$_\text{LS}$ − 3 dB), both approaches yield similar PESQ scores. At a higher gain (MSG$_\text{MM}$ − 3 dB), the LS approach becomes unstable while the min-max approach maintains acceptable quality (~0.5 MOS lower). This confirms the min-max approach allows larger gain margins without quality degradation.

### AFC Convergence Speed

![[raw/papers/schepker-2016-sdp-minmax-acoustic-feedback/figures/a0277485e41091ebd63a45a28dc69a0193c15687df2f999bb66b6a82cd73a5dc.jpg|Misalignment and MSG as a function of time for standard AFC and AFC with common part decomposition]]
*Figure 14: Misalignment and MSG vs. time for standard AFC (without CP, $N_z^v=36$) and AFC with common part decomposition (with CP, $N_p^c=8, N_z^c=4, N_z^v=24$).*

Using the common part decomposition ($N_p^c=8, N_z^c=4, N_z^v=24$) in a [[concepts/prediction-error-method|PEM]]-based AFC algorithm increases both initial convergence speed and reconvergence speed after a feedback path change (at 40 s), while achieving similar steady-state performance compared to standard AFC without a common part ($N_z^v=36$).

## Key Contributions

1. **Min-max optimization for common part estimation**: Formulates the common part estimation problem as a min-max optimization directly maximizing the MSG, rather than minimizing the misalignment via least-squares as in prior work.
2. **SDP formulation with LMI constraints**: Reformulates the non-linear min-max problem as a semidefinite program using the Schur complement and linear matrix inequalities, solvable with standard convex optimization tools (CVX).
3. **Lyapunov stability constraint**: Incorporates a stability constraint based on Lyapunov theory (as an LMI) to guarantee that the estimated common pole-zero filter has all poles strictly inside the unit circle — a key improvement over the previous approach [10].
4. **Alternating optimization procedure**: Uses an iterative two-step alternating procedure (variable part → common part) based on the Steiglitz-McBride method, where each step is a convex SDP.
5. **Experimental validation**: Demonstrates 2–5 dB MSG improvement over LS optimization, robustness to unknown feedback paths, variable-part parameter reduction for desired MSGs, and faster AFC convergence when integrated with PEM-based adaptive feedback cancellation.

## Related Concepts

- [[concepts/common-part-decomposition|Common Part Decomposition]] — the feedback path decomposition into common + variable parts
- [[concepts/min-max-common-part-estimation|Min-max Common Part Estimation]] — the proposed SDP-based optimization approach
- [[concepts/adaptive-feedback-cancellation|Adaptive Feedback Cancellation (AFC)]] — the application context
- [[concepts/maximum-stable-gain|Maximum Stable Gain]] — the optimization objective directly maximized
- [[concepts/prediction-error-method|Prediction Error Method]] — used for the AFC simulations
- [[concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]] — the application domain
- [[concepts/acoustic-feedback|Acoustic Feedback]] — the underlying problem

## Related Synthesis

- [[synthesis/feedback-anc-filter-design|Feedback ANC Filter Design]]
