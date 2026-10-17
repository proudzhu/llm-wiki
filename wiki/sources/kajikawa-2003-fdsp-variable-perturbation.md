---
type: source
created: 2026-10-17
updated: 2026-10-17
sources:
  - raw/papers/kajikawa-2003-fdsp-variable-perturbation/full-text.md
  - zotero://select/items/0_6L2DYW65
tags:
  - active-noise-control
  - secondary-path
  - gradient-free-optimization
  - frequency-domain
  - simultaneous-perturbation
---

# Kajikawa & Nomura 2003: Frequency-Domain Simultaneous Perturbation ANC with Variable Perturbation

| Field | Detail |
|-------|--------|
| **Authors** | [[entities/yoshinobu-kajikawa|Yoshinobu Kajikawa]], [[entities/yasuo-nomura|Yasuo Nomura]] |
| **Institution** | Department of Electronics, Faculty of Engineering, Kansai University, Suita, Osaka, Japan |
| **Venue** | IEEE International Conference on Acoustics, Speech, and Signal Processing (ICASSP 2003), Hong Kong, China, April 6–10, 2003, pp. 580–583 |
| **DOI** | [10.1109/ICASSP.2003.1200036](https://doi.org/10.1109/ICASSP.2003.1200036) |
| **Zotero** | [Link](zotero://select/items/0_6L2DYW65) |

## Summary

This paper upgrades the Kansai line of secondary-path-model-free ANC with two ideas: (i) the **frequency-domain simultaneous perturbation (FDSP)** method — time-domain filtering, frequency-domain updating, with a perturbation filter added to the control filter for only *half* of each block so that both perturbed and unperturbed error vectors are measured within one block; and (ii) a **variable perturbation magnitude** that scales with the measured error power ($c = \sqrt{\alpha P_{e2}/(G^2 P_x)}$), permitting a step size ~75× larger than fixed-perturbation FDSP. Simulations with a 128-tap control filter show much faster convergence than fixed-perturbation FDSP and rapid recovery after an abrupt secondary-path change, at a computational cost (per 2N samples: $2N^2 + 34N + 16N\log_2 N + 4$ multiplications) nearly equal to FDSP and about 3× *cheaper* than the filtered-x LMS algorithm ($6N^2 + 2N$).

## Problem Formulation

The [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] requires a pre-estimated secondary path model; modeling errors destabilize or degrade it. Model-free alternatives exist — the [[concepts/simultaneous-equations-method|simultaneous equations method]] (Fujii et al., ACTIVE 99) converges fast but needs a complex system composition; the perturbation method ([[concepts/simultaneous-perturbation|simultaneous perturbation]], Kajikawa & Nomura ISCAS 2000 time-domain / IEICE E84-A 2001 frequency-domain) updates coefficients using only error signals but converges slowly. The slowness is structural: **the admissible step size is tied to the perturbation magnitude**. A large perturbation permits a large step size but is itself additive noise that hurts cancellation performance; forcing the perturbation small (for good steady-state cancellation) forces the step size small, hence slow convergence. The paper's answer: vary the perturbation magnitude with the error level.

## Methodology

### Conventional FDSP (fixed perturbation)

![[raw/papers/kajikawa-2003-fdsp-variable-perturbation/figures/95777c6773c8fe9e83d1df348444ba2681c4fc39470152964cd87894ae1c8a20.jpg|Figure 1: Block diagram of the ANC system using the FDSP method]]

*Figure 1: Block diagram of the ANC system using the FDSP method. $P(z)$: primary path, $C(z)$: secondary path, $W(z)$: time-domain control filter (TDCF), $S(z)$: perturbation filter.*

Filtering runs in the time domain (real-time requirement); updating runs in the frequency domain. The perturbation filter is added to the TDCF during the **first half** of each block (length $L = 2N$) and removed during the **rest half**, yielding two error vectors — perturbed ($\boldsymbol{e}_{1,n}$) and unperturbed ($\boldsymbol{e}_{2,n}$) — from a single block. At block end both are FFT'd and the update is:

$$
\boldsymbol{w}_{n+1} = \boldsymbol{w}_n - \mu \boldsymbol{\Delta}\boldsymbol{w}_n
$$

$$
\boldsymbol{\Delta}\boldsymbol{w}_n = \text{first } N \text{ elements of } \mathrm{IFFT}\big[\boldsymbol{U}_n\big], \qquad
\boldsymbol{U}_n = \mathrm{diag}[\boldsymbol{S}_n]\,\frac{\mathrm{diag}[\boldsymbol{E}_{2,n}^*]\boldsymbol{E}_{2,n} - \mathrm{diag}[\boldsymbol{E}_{1,n}^*]\boldsymbol{E}_{1,n}}{c}
$$

$$
\boldsymbol{E}_{1,n} = \mathrm{FFT}[\boldsymbol{e}_{1,n}], \quad \boldsymbol{E}_{2,n} = \mathrm{FFT}[\boldsymbol{e}_{2,n}]
$$

where $\boldsymbol{S}_n \in \mathbb{C}^{2N}$ is a complex sign vector whose real and imaginary parts are independently $\pm 1$, zero-mean, and mutually uncorrelated across time, frequency, and real/imaginary part — so $\mathrm{diag}[\boldsymbol{E}^*]\boldsymbol{E}$ yields **per-frequency-bin error power**, and every bin's gradient component is estimated from the same single perturbation experiment. The fixed perturbation magnitude must satisfy

$$
c < \sqrt{\frac{P_v}{P_x}}
$$

where $P_v$ is the power of the additive (perturbation) noise and $P_x$ the input power.

### FDSP with variable perturbation

The restructured block schedule (the paper's Fig. 2 is a text/table figure): (1) cancel **without** perturbation during the first half-block; (2) measure the error power $P_{e2}$; (3) compute the perturbation magnitude

$$
c = \sqrt{\frac{\alpha P_{e2}}{G^2 P_x}}
$$

where $G$ is the **gain of the secondary path** (a scalar, not a full transfer-function model), and $\alpha$ a constant; (4) cancel **with** the perturbation filter during the rest half-block; then FFT both error vectors, apply the same update equation, and IFFT back. The perturbation power thus tracks the error power: large errors → large perturbation (fast convergence far from the optimum); small errors → small perturbation (low residual perturbation noise near the optimum).

**Caveat**: the variable-perturbation rule needs the secondary-path *gain* $G$ — not the full $C(z)$ model, but a scalar that must still be roughly correct. The "no secondary path model" claim is thus slightly qualified in this variant.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Input signal** | White noise (power 1) |
| **Sampling frequency** | 2000 Hz |
| **Tap length** | 128 (primary path, secondary path, control filter, perturbation filter) |
| **Block length** | $L = 2N = 256$ |
| **S/N** | 20 dB |
| **Tuning (proposed)** | $\alpha = 0.5$, $\mu = 6.0 \times 10^{-5}$ |
| **Tuning (conventional FDSP)** | $c = 0.08$, $\mu = 8.0 \times 10^{-7}$ |
| **Disturbance** | Secondary path abruptly changed at sample 300,000 |

Both systems tuned for fastest convergence; metric is the block Reduction $10\log_{10}\left(\sum d_i^2 / \sum e_i^2\right)$.

## Results

![[raw/papers/kajikawa-2003-fdsp-variable-perturbation/figures/2d5e0522a726f3148864194cf86815ed145bf8ea127ef5dffdc4940514bfa8f9.jpg|Figure 3: Comparison of convergence properties between the proposed and the conventional ANC systems using FDSP]]

*Figure 3: Convergence properties — proposed (variable perturbation) vs conventional (fixed perturbation) FDSP.*

![[raw/papers/kajikawa-2003-fdsp-variable-perturbation/figures/583cc6e99bca1814594e41f62471ffc8505c47e5cdcfed06998f146109ec8ed9.jpg|Figure 4: Comparison of the perturbation magnitudes between the proposed and the conventional FDSP systems]]

*Figure 4: Perturbation magnitudes over time — the proposed system's $c$ shrinks as the error falls, the conventional system's stays fixed at 0.08.*

The proposed system converges **much faster** than fixed-$c$ FDSP — enabled by the ~75× larger step size ($6.0\times10^{-5}$ vs $8.0\times10^{-7}$) that variable perturbation makes stable — and both systems track the abrupt secondary-path change at sample 300,000, with the proposed system recovering faster.

## Computational Complexity

Multiplications per $2N$ samples:

| Algorithm | Multiplications |
|-----------|-----------------|
| **Proposed FDSP (variable perturbation)** | $2N^2 + 34N + 16N\log_2 N + 4$ |
| Conventional FDSP | $2N^2 + 32N + 16N\log_2 N$ |
| Filtered-x LMS | $6N^2 + 2N$ |
| TDSP (time-domain SP) | $2N^2 + 2N + 3$ |

![[raw/papers/kajikawa-2003-fdsp-variable-perturbation/figures/21f96b83400e1eb5fcc1ef147ad624e7c82402db9b3728c3b3562ca9c4dea0e0.jpg|Figure 5: Comparison of the number of multiplications in each algorithm]]

*Figure 5: Multiplication counts versus filter length — the proposed method costs nearly the same as conventional FDSP and less than FxLMS.*

Variable perturbation adds only $2N + 4$ multiplications per block over conventional FDSP (the error-power measurement and $c$ computation). All perturbation methods scale as $2N^2$ versus FxLMS's $6N^2$ — roughly **3× cheaper** at large $N$ — because no reference filtering through $\hat{S}(z)$ is needed.

## Key Contributions

1. **Variable perturbation magnitude**: perturbation power made proportional to measured error power ($c = \sqrt{\alpha P_{e2}/G^2 P_x}$), breaking the fixed-perturbation trade-off between convergence speed (wants large $c$, large $\mu$) and steady-state cancellation (wants small $c$) — enabling a step size ~75× larger while suppressing residual perturbation noise.
2. **Half-block perturbation schedule**: both perturbed and unperturbed error vectors measured within a *single* block, keeping the two-measurement SP gradient estimate at one-block update cadence.
3. **Complexity analysis**: per-bin frequency-domain gradient estimation costs $2N^2 + O(N\log N)$ — the perturbation family is ~3× cheaper than FxLMS, and variable perturbation adds a negligible $2N + 4$.
4. **Robustness data point**: continued convergence after an abrupt secondary-path change (sample 300,000), the property that motivates the whole model-free line.

**Terminology note**: this paper's "TDSP" means *time-domain* simultaneous perturbation (the Kajikawa–Nomura time-domain method), whereas Maeda's "TDSP" means *time-difference* simultaneous perturbation — two different methods sharing an acronym.

## Related Concepts

- [[concepts/simultaneous-perturbation|Simultaneous Perturbation]]
- [[concepts/frequency-domain-anc|Frequency Domain ANC]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/simultaneous-equations-method|Simultaneous Equations Method]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]

## Related Synthesis

- [[synthesis/secondary-path-modeling-evolution|Secondary Path Modeling: From Offline Identification to Model-Free Evolution]]
- [[queries/perturbation-anc-maeda-vs-kajikawa|扰动 ANC 对比：Maeda 1999 SP/TDSP vs Kajikawa 2000-2003 FDSP]]
