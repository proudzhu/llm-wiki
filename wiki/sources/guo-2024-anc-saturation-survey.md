---
type: source
created: 2026-08-10
updated: 2026-08-10
sources:
  - raw/papers/guo-2024-anc-saturation-survey/full-text.md
  - https://doi.org/10.1016/j.sigpro.2024.109525
  - zotero://select/items/0_V7CFUJY4
tags:
  - active-noise-control
  - output-saturation
  - output-constraint-algorithms
  - nonlinear-adaptive-algorithms
  - adaptive-filters
  - fxlms
  - survey
---

# Guo, Shi, Shen, Ji & Gan 2024: ANC Algorithms Overcoming Output Saturation

**Authors**: [[entities/yu-guo|Yu Guo]], [[entities/dongyuan-shi|Dongyuan Shi]], [[entities/xiaoyi-shen|Xiaoyi Shen]], [[entities/junwei-ji|Junwei Ji]], [[entities/woon-seng-gan|Woon-Seng Gan]]
**Institution**: Digital Signal Processing Lab, School of Electrical and Electronic Engineering, Nanyang Technological University, Singapore
**Venue**: Signal Processing, Vol. 225, Article 109525
**Year**: 2024
**Type**: Survey / Journal Article
**DOI**: [10.1016/j.sigpro.2024.109525](https://doi.org/10.1016/j.sigpro.2024.109525)
**Zotero**: [V7CFUJY4](zotero://select/items/0_V7CFUJY4)

## Summary

This survey compares contemporary adaptive [[active-noise-control|ANC]] algorithms that mitigate the [[concepts/output-saturation-effect|output saturation effect]] caused by the power amplifier in the secondary path. It traces the saturation issue to a single physical origin — the amplifier entering its nonlinear region when desired output power exceeds the rated output — and shows analytically that this nonlinearity both deforms the anti-noise and drives the adaptive filter coefficients to diverge. The review then organizes the solution space into two complementary families — **output constraint algorithms** (which keep the amplifier in its linear region by limiting output power) and **nonlinear adaptive algorithms** (which model and pre-distort the saturation nonlinearity) — and compares them on computational complexity, stability under mild vs. severe saturation, and real-time feasibility, concluding that output constraint algorithms are the more practical choice.

## Taxonomy

The survey's central contribution is the following dichotomy of saturation-mitigation algorithms, each addressing the same physical problem from the opposite direction:

| Family | Strategy | Typical algorithms | Computational cost | Stability under severe saturation |
|:-------|:---------|:-------------------|:-------------------|:----------------------------------|
| **Output constraint** | Suppress output power so the amplifier stays linear | 2-GD FxLMS, Re-scaling FxLMS, Leaky FxLMS, Extended Leaky FxLMS, OLFxLMS, MOV FxLMS, MOV-Modified FxLMS | Low — comparable to FxLMS | Preserved (limits output power) |
| **Nonlinear adaptive (NANC)** | Model the saturation nonlinearity and pre-distort the control signal to cancel harmonic distortion | 2nd-VFxLMS, BFxLMS, FLANN-FsLMS, THF-FxLMS, MLPNN-FxLMS | High — quadratic or worse in filter length | Not guaranteed in severe saturation |

The two families correspond to two distinct operating regimes: NANC algorithms are advantageous under **mild saturation** (fundamental frequency still cancelable; only harmonics remain), whereas output constraint algorithms are required under **severe saturation** (fundamental cannot be fully attenuated and unconstrained filters diverge).

## Problem Formulation

### Origin of the Nonlinearity

The survey first rules out two of the three candidate sources of secondary-path nonlinearity:

1. **Error microphone / signal-conditioning circuit** — clipping only if disturbance SPL exceeds the input range. In practice disturbance SPL (40–90 dBA) is well within modern microphone ranges, so suitable circuit design prevents this.
2. **Acoustic path** — large-amplitude acoustic waves induce nonlinear propagation, but ANC disturbance levels (typically < 100 dBA) are too low to trigger it.
3. **Actuator (output amplifier + loudspeaker)** — the dominant source. When desired output power exceeds the amplifier's rated output, the amplifier enters a saturation mode that clips the control signal and destabilises the adaptive algorithm.

### Narrow-band Saturation Analysis

For a sinusoidal disturbance $d(n) = D\sin(\omega_o n)$ with amplifier threshold $V_\mathrm{thr}$ and secondary-path gain $A_s$:

- $D \in [0, V_\mathrm{thr}]$: disturbance fully cancelled.
- $D \in [V_\mathrm{thr}, 4A_s V_\mathrm{thr}/\pi]$: disturbance cancelled but high-frequency harmonics appear; the residual error becomes a function of $3\omega_o, 5\omega_o, \dots$ (Eq. 2).
- $D > 4A_s V_\mathrm{thr}/\pi$: fundamental cannot be fully attenuated; control filter coefficients overrun.

![[raw/papers/guo-2024-anc-saturation-survey/figures/2d9a1109909f68bb3c139f019c841764669fc27edd5f9271da6338ccf9b720c4.jpg|Figure 1]]
*Figure 1: Block diagram of feedforward narrow-band ANC system.*

### Broadband Saturation Analysis

The survey models the saturation by an S-shaped nonlinear function $f[\cdot]$ cascaded after the control filter (Eq. 7), giving the error signal

$$e(n) = d(n) - \sum_{l=0}^{L-1} s_l\, f[y(n-l)],$$

and the FxLMS update

$$\mathbf{w}(n+1) = \mathbf{w}(n) + \mu e(n)\mathbf{x}'(n).$$

When the disturbance cannot be fully cancelled because of the output limitation, the residual error retains the same phase as the filtered reference $\mathbf{x}'(n)$, so the magnitude of the control filter grows without bound (Eq. 12):

$$\lim_{n\to\infty} \mathbb{E}[\mathbf{w}(n+1)] = \infty.$$

This divergence result is the analytical motivation for the entire survey: unconstrained linear (and even nonlinear) adaptive filters cannot remain stable once the amplifier is driven into severe saturation.

![[raw/papers/guo-2024-anc-saturation-survey/figures/e0796a7a7ffc48bcbd75f85854add90332643143b49de4fab88322aa0ee2ab66.jpg|Figure 2]]
*Figure 2: Block diagram of the adaptive ANC system with saturation distortion, where $\sum$ represents the acoustic summation.*

## Methodology

### Output Constraint Algorithms (Section 3)

The first family imposes a constraint on the output signal so the amplifier stays in its linear region. The survey formulates the underlying optimisation as a quadratically constrained quadratic program (QCQP, Eq. 25):

$$\min_\mathbf{w} J(\mathbf{w}) = \mathbb{E}\!\left[\left|d(n) - \textstyle\sum_l s_l \mathbf{w}^T(n{-}l)\mathbf{x}(n{-}l)\right|^2\right] \quad \text{s.t.}\ \ g(\mathbf{w}) = \mathbb{E}[|\mathbf{w}^T(n)\mathbf{x}(n)|^2] \le \rho^2,$$

whose KKT solution (Eq. 26) is $\mathbf{w}_o = (\lambda_o \mathbf{R}_x + \mathbf{R}_{x'})^{-1} \mathbf{P}_{dx'}$, with the Lagrange factor $\lambda_o$ vanishing when the constraint is inactive. The surveyed algorithms differ in how they recursively realise this optimum:

| Algorithm | Mechanism | Key equation | Constraint type |
|:----------|:----------|:-------------|:----------------|
| **2-GD FxLMS** (Shi 2019) | Two gradient directions: standard FxLMS update when $|y(n)| \le C$, weight-reduction update otherwise | Eqs. 13–14 | Amplitude |
| **Re-scaling FxLMS** (Qiu & Hansen 2001) | Rescales $\mathbf{w}(n{+}1)$ and $y(n{+}1)$ by $C/|y(n{+}1)|$ when threshold exceeded | Eq. 15 | Amplitude |
| **Leaky FxLMS** | Scalar leakage factor $\lambda$ penalises $\mathbf{w}^T\mathbf{w}$ in the cost function | Eqs. 16–17 | Power (scalar) |
| **Extended Leaky FxLMS** (Wu 2018) | Matrix leakage factor $\boldsymbol{\gamma} = \mathbf{C}^T\mathbf{C}$ for more control freedom | Eqs. 18–21 | Power (matrix) |
| **MOV FxLMS** (Shi 2021) | Penalty on output variance $\alpha\,\mathbb{E}[y^2(n)]$ added to MSE cost | Eqs. 22–24 | Power |
| **OLFxLMS** (Optimal Leaky) | Sets $\boldsymbol{\gamma} = \Lambda_o \mathbf{R}_x$ so extended Leaky converges to the QCQP optimum; estimates $G_s$ via inverse modeling | Eqs. 28–32 | Optimal power |
| **Optimal MOV FxLMS** | Sets $\alpha = \Lambda_o$ so MOV converges to the QCQP optimum | Eq. 33 | Optimal power |
| **MOV-Modified FxLMS** (Lai 2023) | Online estimation of $G_s \approx \sigma_{x'}^2/\sigma_x^2$ via moving filter; variable penalty $\alpha(n)$ handles dynamic noise | Eqs. 34–35 | Optimal power (online) |

The online penalty factor of MOV-Modified FxLMS is the most recent advance: it removes the offline inverse-modeling bottleneck and lets the algorithm track time-varying noise and acoustic environments while still converging to the constrained optimum.

![[raw/papers/guo-2024-anc-saturation-survey/figures/b00a7bc4ea70bc73e4a083ae94b6dc8b5f2fbf1d39793df647adfcb1ed847fcf.jpg|Figure 4]]
*Figure 4: Block diagram of the modified FxLMS algorithm used by MOV-Modified FxLMS for online penalty-factor estimation.*

### Nonlinear Adaptive Algorithms (Section 4)

The second family cascades or embeds a nonlinear model in the adaptive filter so that the control signal pre-distorts the amplifier's saturation nonlinearity, cancelling the resulting harmonic distortion. The surveyed algorithms are:

| Algorithm | Nonlinear structure | Key feature | Limitation |
|:----------|:--------------------|:------------|:-----------|
| **2nd-VFxLMS** (Tan & Jiang 1997) | Second-order Volterra filter | Adds quadratic cross-terms to the linear filter; well-suited to mild high-order nonlinearities | $O(N^2)$ coefficients; convergence to local minima; poorer at low frequencies |
| **BFxLMS** (Kuo & Wu 2005) | Bilinear (IIR-style) filter with feedforward, feedback, and cross terms | Lower order than Volterra for strong saturation; output-error and equation-error variants | Stability depends on conditions; unstable for IIR case |
| **FLANN-FsLMS** (Das & Panda 2004; Patra 1999) | Functional-link ANN with trigonometric expansion | Single flat network; linear-in-parameters; much cheaper than Volterra | High training data and computation; not real-time friendly |
| **THF-FxLMS** (Sahib 2012) | Tangential hyperbolic function $f_\mathrm{THF}(y) = \alpha_f \tanh(\beta y)$ in a Hammerstein model | Lowest computational cost among NANC algorithms; models both linear and nonlinear parts | Effective only for periodic noise; requires small step size |
| **MLPNN-FxLMS** (Elliott 2001) | Multi-layer perceptron with backpropagation | Universal function approximator; strongest nonlinear modelling ability | Unachievable computational burden; gradient vanishing with depth |

## Applications Survey

### Computational Complexity Comparison

The survey's central quantitative result is the per-iteration complexity comparison (filter length $N$, secondary-path length $L$, moving filter $K$, expansion order $P$, MLPNN layers $M,L$). Output constraint algorithms scale linearly in $N$, while NANC algorithms scale quadratically (Volterra, bilinear, FLANN) or worse (MLPNN).

| Algorithm | Multiplications | Additions |
|:----------|:----------------|:----------|
| FxLMS (baseline) | $2N + L + 1$ | $2N + L - 2$ |
| **2-GD FxLMS** | $2N + L + 1$ | $2N + L - 2$ |
| Leaky FxLMS | $3N + L + 1$ | $2N + L - 2$ |
| Re-scaling FxLMS | $3N + L + 2$ | $2N + L - 2$ |
| Optimal MOV FxLMS | $4N + L + 7$ | $4N + L - 2$ |
| Modified MOV FxLMS | $4N + L + K + 7$ | $4N + L - 2$ |
| Optimal Leaky FxLMS | $2N^2 + 2N + L$ | $N^2 + 3N + L - 2$ |
| Extended Leaky FxLMS | $2N^2 + 2N + L + 1$ | $N^2 + 2N + L - 2$ |
| 2nd-VFxLMS | $(3N^2 + 9N + 2L + 2)/2$ | $N^2 + 2N + L - 3$ |
| BFxLMS | $3N^2 + 8N + 2L + 5$ | $2N^2 + 6N + 2L - 3$ |
| FLANN-FxLMS | $N(2P+1)(L+3) - L$ | $N(2P+1)(L+1) + 1$ |
| THF-FxLMS | $2N + 2L + 3$ | $2N + 2L - 3$ |
| MLPNN-FxLMS | $3M^2L + 4ML + 2L$ | $M^2L + 2ML + 4L + M$ |

For $N=L=K$ varying from 0 to 512, the multiplications and additions of NANC algorithms (especially MLPNN, BFxLMS, 2nd-VFxLMS, FLANN) grow one to two orders of magnitude faster than the output-constraint family.

(a) Number of Multiplications for different Algorithms
![[raw/papers/guo-2024-anc-saturation-survey/figures/8ce95dde723a8e35c936b1d154db80f7575275d386091bc4361161e8471367e5.jpg|Figure 12a]]

(b) Number of Addition for different Algorithms
![[raw/papers/guo-2024-anc-saturation-survey/figures/1c154eea3750c18131d15b7d214438cbeff3dfdb248298ff3efa3d2853289a90.jpg|Figure 12b]]
*Figure 12: Computational complexity of algorithms as a function of control filter length (32 to 512): (a) multiplications, (b) additions.*

### Stability and Real-time Performance

The survey distinguishes **mild saturation** (fundamental cancelable, harmonics remain) from **severe saturation** (fundamental not fully cancelable; unconstrained filters diverge):

- Under **mild saturation**, NANC algorithms are superior because their pre-distortion strategy can mitigate harmonic distortions, while linear algorithms converge but leave harmonics.
- Under **severe saturation**, neither linear nor nonlinear adaptive algorithms can maintain stability without an output constraint. Output constraint algorithms force the amplifier into its linear region and preserve stability, at the cost of not fully canceling the disturbance.

### Overall Recommendation

| Criterion | Best family | Reason |
|:----------|:------------|:-------|
| Computational efficiency | Output constraint | Linear complexity in $N$; 2-GD FxLMS matches FxLMS; only optimal-leaky variants go quadratic |
| Real-time feasibility | Output constraint | Implementable on standard DSPs; MOV-Modified supports online penalty tuning |
| Stability under severe saturation | Output constraint | Only family that prevents filter divergence when fundamental cannot be cancelled |
| Nonlinear distortion suppression (mild saturation) | NANC | Pre-distortion cancels harmonic distortions that linear constraint leaves behind |
| Modelling arbitrary nonlinearities | NANC (MLPNN) | Universal approximation, but at unachievable computational cost |

The survey concludes that output constraint algorithms achieve the best balance between real-time feasibility and nonlinear performance, and should be the practical default for handling output saturation in ANC systems.

## Key Contributions

1. **Unified physical attribution**: Traces the secondary-path nonlinearity in ANC systems to a single dominant source — output amplifier saturation — by ruling out microphone circuit and acoustic propagation nonlinearity at typical ANC disturbance levels.
2. **Divergence proof**: Shows analytically that once the amplifier enters severe saturation, the residual error retains the phase of the filtered reference, causing unconstrained FxLMS (and NANC) filter coefficients to diverge to infinity (Eq. 12).
3. **Two-family taxonomy**: Proposes the output-constraint vs. nonlinear-adaptive dichotomy as the organising principle for saturation-mitigation algorithms, with each family tied to a distinct saturation regime (mild vs. severe).
4. **QCQP formulation**: Casts optimal output-constrained ANC as a quadratically constrained quadratic program (Eq. 25) and derives the KKT optimum (Eq. 26), unifying the leaky and MOV algorithms as recursive approximations of the same optimum via the choice of leakage matrix or penalty factor.
5. **Complexity and stability comparison**: Provides side-by-side computational complexity tables (Tables 4–5) and stability/real-time evaluation tables (Tables 6–7) for all surveyed algorithms, establishing that output constraint algorithms are the practical choice.
6. **Online penalty-factor estimation**: Highlights MOV-Modified FxLMS (Lai 2023) as the first algorithm to estimate the optimal penalty factor online via a moving-filter estimate of the secondary-path power gain (Eq. 34), enabling operation under dynamic noise and varying acoustic environments.

## Limitations and Caveats

- **No new experiments**: The survey is purely a literature synthesis; all quantitative results are re-tabulated from prior work, not re-measured.
- **NANC stability under severe saturation is an open question**: The survey explicitly notes there are no experimental validations that NANC algorithms maintain stability when the amplifier enters the severe nonlinear region — the claim that output constraint is required under severe saturation is theoretical.
- **No quantitative nonlinear-representation metric**: The survey observes that "few indicators or measurement techniques can quantitatively reflect the strength of nonlinear representation ability" of NANC algorithms, so the NANC comparison is largely qualitative.
- **Coverage cutoff**: The survey was submitted in late 2023 and published in 2024; very recent deep-learning-based NANC algorithms (e.g., transformer-based controllers) are only briefly mentioned and not included in the complexity comparison.
- **Optimal-leaky computational cost**: The optimal leaky FxLMS (OLFxLMS) and extended leaky variants themselves incur $O(N^2)$ complexity, blunting the complexity advantage of the output-constraint family when those specific variants are used.

## Related Concepts

- [[concepts/output-saturation-effect|Output Saturation Effect]] — central topic of the survey
- [[concepts/output-constraint-anc-algorithms|Output Constraint ANC Algorithms]] — the survey's first taxonomy family
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — baseline for all surveyed algorithms
- [[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]]
- [[concepts/nonlinear-active-noise-control|Nonlinear Active Noise Control]] — the survey's second taxonomy family
- [[concepts/volterra-filter|Volterra Filter]] — 2nd-VFxLMS
- [[concepts/bilinear-filter|Bilinear Filter]] — BFxLMS
- [[concepts/flann-filter|FLANN Filter]] — FLANN-FsLMS
- [[concepts/secondary-path-modeling|Secondary Path Modeling]] — inverse modeling for power-gain estimation
- [[concepts/minimum-variance-control|Minimum Variance Control]] — related but distinct (output-variance vs. output-power constraint)
- [[concepts/quadratic-programming|Quadratic Programming]] — QCQP formulation

## Related Synthesis

- [[synthesis/nonlinear-anc-approaches|Nonlinear ANC Approaches]]
- [[synthesis/adaptive-algorithm-tradeoffs|Adaptive Algorithm Tradeoffs]]
