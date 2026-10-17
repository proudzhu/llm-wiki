---
type: concept
created: 2026-10-17
updated: 2026-10-17
sources:
  - raw/papers/maeda-1999-anc-simultaneous-perturbation/full-text.md
  - raw/papers/kajikawa-2003-fdsp-variable-perturbation/full-text.md
aliases:
- Simultaneous Perturbation Method
- SPSA
- Time Difference Simultaneous Perturbation
tags:
  - gradient-free-optimization
  - stochastic-approximation
  - optimization
  - active-noise-control
---

# Simultaneous Perturbation

The **simultaneous perturbation** method is a stochastic-approximation optimization scheme that minimizes an unknown objective function $J(\boldsymbol{w}) \in \Re$, $\boldsymbol{w} \in \Re^n$, using only **values** of the function — never its analytical gradient. All $n$ parameters are perturbed simultaneously by a random sign vector, and the gradient is *estimated from the observed function change*, in contrast to finite differences, which perturbs one parameter at a time and requires $n$ (or $2n$) evaluations per gradient.

The idea was discovered independently several times: Spall's SPSA (1987, 1992), Alspector et al.'s parallel gradient descent for analog VLSI (1992), Cauwenberghs' stochastic error descent (1992–1993), and Maeda's learning rules for neural networks (1993–1997), with hardware implementation in analog neural networks.

## Key Formulations

### Simultaneous Perturbation (two measurements)

$$
\boldsymbol{w}_{t+1} = \boldsymbol{w}_t - \alpha \Delta \boldsymbol{w}_t, \qquad
\Delta w_t^i = \frac{J(\boldsymbol{w}_t + c\boldsymbol{s}_t) - J(\boldsymbol{w}_t)}{c}\, s_t^i
$$

where $\boldsymbol{s}_t$ is a random sign vector ($s_t^i = \pm 1$, mutually independent, zero-mean: $E(s_t^i) = 0$, $E(s_t^i s_t^j) = 0$ for $i \neq j$), $c$ is the perturbation magnitude, and $\alpha$ the step size. Taylor expansion of $J(\boldsymbol{w}_t + c\boldsymbol{s}_t)$ shows that the estimate is unbiased in expectation:

$$
E(\Delta w_t^i) = \frac{\partial J(\boldsymbol{w}_t)}{\partial w_t^i}
$$

so the algorithm is a stochastic gradient method whose gradient is *measured* on the physical plant rather than computed from a model.

### Time Difference Simultaneous Perturbation (one measurement)

Proposed by Maeda (Electronics Letters, 1996), the time-difference variant needs only **one** objective evaluation per iteration by reusing the previous iterate's value:

$$
\boldsymbol{w}_{t+1} = \boldsymbol{w}_t - \alpha \Delta \boldsymbol{w}_t + c\boldsymbol{s}_t, \qquad
\Delta w_t^i = \operatorname{clip}\!\left(\frac{J(\boldsymbol{w}_t) - J(\boldsymbol{w}_{t-1})}{c\, s_{t-1}^i},\ \pm\Delta w_{\max}\right)
$$

The fresh perturbation $c\boldsymbol{s}_t$ is re-injected at every step so that the next time difference remains informative; the clip bounds the modification per step. A one-measurement variant of the plain simultaneous perturbation also exists ("one-measurement simultaneous perturbation").

### Frequency-Domain Simultaneous Perturbation (FDSP)

Kajikawa & Nomura's frequency-domain variant (IEICE Trans. E84-A 2001; variable-perturbation version [[sources/kajikawa-2003-fdsp-variable-perturbation|Kajikawa & Nomura 2003]]) moves only the *updating* to the frequency domain — filtering stays in the time domain for real-time operation. Within each block of $L = 2N$ samples, the perturbation filter is added to the control filter for **half** the block and removed for the other half, so perturbed ($\boldsymbol{e}_{1,n}$) and unperturbed ($\boldsymbol{e}_{2,n}$) error vectors are both measured within a single block. Their FFTs give per-bin error powers, and the update

$$
\boldsymbol{U}_n = \mathrm{diag}[\boldsymbol{S}_n]\,\frac{\mathrm{diag}[\boldsymbol{E}_{2,n}^*]\boldsymbol{E}_{2,n} - \mathrm{diag}[\boldsymbol{E}_{1,n}^*]\boldsymbol{E}_{1,n}}{c}, \qquad
\boldsymbol{\Delta}\boldsymbol{w}_n = \text{first } N \text{ elements of } \mathrm{IFFT}[\boldsymbol{U}_n]
$$

estimates **all $N$ gradient components from one block** — the key structural difference from Maeda's time-domain version, where one block yields a single scalar difference shared by all taps. The sign vector $\boldsymbol{S}_n$ is complex (real and imaginary parts independently $\pm 1$), and the fixed perturbation magnitude must satisfy $c < \sqrt{P_v/P_x}$ (perturbation power below the additive-noise budget).

**Variable perturbation** ([[sources/kajikawa-2003-fdsp-variable-perturbation|Kajikawa & Nomura 2003]]) makes the magnitude track the error level, $c = \sqrt{\alpha P_{e2}/(G^2 P_x)}$, where $G$ is the **scalar gain** of the secondary path — large errors get a large perturbation (fast convergence far from the optimum), small errors a small one (low residual perturbation noise near it). This permits a step size ~75× larger than fixed-$c$ FDSP and much faster convergence after secondary-path changes, at $2N^2 + 34N + 16N\log_2 N + 4$ multiplications per $2N$ samples — roughly **3× cheaper** than the filtered-x LMS algorithm's $6N^2 + 2N$.

**Terminology collision**: Kajikawa's "TDSP" means *time-domain* simultaneous perturbation, while Maeda's "TDSP" means *time-difference* simultaneous perturbation — two different methods sharing an acronym.

## Application to ANC

In [[concepts/active-noise-control|Active Noise Control]], the objective is the block-summed squared error $J(\boldsymbol{w}) = \sum_{k=1}^{\lambda} e^2(k)$ measured at the error microphone, and the parameters are the control-filter coefficients. Because the gradient is *measured*, no secondary-path model $\hat{S}(z)$ and no filtered reference signal enter the adaptation — the defining property of [[sources/maeda-1999-anc-simultaneous-perturbation|Maeda & Yoshida 1999]]'s secondary-path-free ANC. A duct experiment attenuated a 200 Hz sinusoid by ~25 dB (SP) and ~15 dB (TDSP).

The approach was developed at Kansai University in two parallel lines: Maeda & Yoshida's time-domain version (ACTIVE 99), and Kajikawa & Nomura's closely related perturbation ANC (IEICE J82-A 1999; ISCAS 2000), later extended into frequency-domain variants with variable perturbation ([[sources/kajikawa-2003-fdsp-variable-perturbation|Kajikawa & Nomura 2003]]; Mori, Kajikawa & Nomura 2003) and improved stability/cancellation performance (Tokoro, Kajikawa & Nomura 2007).

## Relation to Other Gradient-Free Methods

Unlike [[concepts/heuristic-anc-algorithms|population-based heuristic methods]] (GA, PSO) that evaluate *many* candidate solutions per generation, simultaneous perturbation evaluates *one or two* points per iteration — cheaper per step and closer to a true stochastic gradient method, but with no global-optimum guarantee and a convergence speed that degrades as the disturbance frequency rises (the motivation for the frequency-domain, variable-perturbation extensions).

## Related Concepts

- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — the conventional approach whose secondary-path requirement this method eliminates
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]
- [[concepts/heuristic-anc-algorithms|Heuristic ANC Algorithms]]
- [[concepts/simultaneous-equations-method|Simultaneous Equations Method]] — the other route to secondary-path-model-free feedforward ANC

## Related Sources

- [[sources/maeda-1999-anc-simultaneous-perturbation|Maeda & Yoshida 1999: ANC Using Simultaneous Perturbation]] — first application to ANC; no secondary-path estimation, duct experiment on TMS320C30
- [[sources/kajikawa-2003-fdsp-variable-perturbation|Kajikawa & Nomura 2003: FDSP with Variable Perturbation]] — frequency-domain updating with per-bin gradient estimation and error-scaled perturbation magnitude; ~75× larger step size, ~3× cheaper than FxLMS
